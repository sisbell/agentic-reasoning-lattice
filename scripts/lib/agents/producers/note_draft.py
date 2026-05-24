"""Note-draft agent — synthesizes consultation answers into a note.

Fires when an inquiry has consultation done (≥1 active
`consultation.answer.*` covering it) but no note yet (no active
`provenance.synthesis` from the inquiry). One fire = build the
discovery prompt with consultation content walked from substrate at
runtime, invoke Claude, write the note md, emit the `note`
classifier + `provenance.synthesis` link.

The methodology prompt template
(prompts/<lattice>/agents/_shared/methodology.md) is the single source
of truth — shared between note_draft (initial write) and note_revise
(per-finding refinement). Placeholders supplied here:
{{consultation_answers}}, {{asn_number}}, {{title}}, {{question}},
{{slug}}, {{foundation_section}}, {{vocabulary_section}},
{{out_of_scope_note}}.
"""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path
from typing import ClassVar

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.backend.emit import emit_note, emit_synthesis
from lib.protocols.febe.protocol import Session
from lib.protocols.febe.session import open_session
from lib.lattice.labels import extract_label_digits, format_label
from lib.shared.campaign import resolve_campaign
from lib.shared.common import read_file
from lib.shared.foundation import load_foundation_for_note
from lib.shared.invoke_claude import invoke_claude_agent
from lib.shared.paths import (
    LATTICE, NOTE_DIR, USAGE_LOG, WORKSPACE,
    inquiry_doc_path,
    load_inquiry as load_inquiry_frontmatter,
    prompt_path,
)


METHODOLOGY_PROMPT = prompt_path("agents/_shared/methodology.md")

MODEL = "claude-opus-4-7[1m]"


# ─── Helpers ────────────────────────────────────────────────────


def _load_prompt(path):
    """Load prompt template file. Aborts the run on missing template."""
    content = read_file(path)
    if not content:
        print(f"  [ERROR] Prompt not found: {path}", file=sys.stderr)
        return None
    return content


def _load_inquiry_record(inquiry_id):
    """Load inquiry content from substrate-managed inquiry doc."""
    fm = load_inquiry_frontmatter(inquiry_id)
    if not fm:
        return None
    return {
        "id": inquiry_id,
        "title": fm.get("title", ""),
        "question": fm.get("question", ""),
        "out_of_scope": fm.get("out_of_scope", ""),
    }


def _slugify(title):
    """Convert title to filename-safe slug."""
    return title.lower().replace(" ", "-").replace("(", "").replace(")", "")


def _log_usage(skill, asn_label, inquiry_title, area, elapsed, data):
    """Append a usage entry to the log."""
    usage = data.get("usage", {})
    cost = data.get("total_cost_usd", 0)
    inp = (usage.get("input_tokens", 0) +
           usage.get("cache_read_input_tokens", 0) +
           usage.get("cache_creation_input_tokens", 0))
    out = usage.get("output_tokens", 0)

    num_turns = data.get("num_turns", 0)
    print(f"  [{elapsed:.0f}s] in:{inp} out:{out} turns:{num_turns} ${cost:.4f}",
          file=sys.stderr)

    entry = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "skill": skill,
        "asn": asn_label,
        "inquiry": inquiry_title,
        "area": area,
        "elapsed_s": round(elapsed, 1),
        "input_tokens": inp,
        "output_tokens": out,
        "num_turns": num_turns,
        "cost_usd": cost,
    }
    with open(USAGE_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


def _build_discovery_prompt(inquiry, asn_number, slug, answers_content,
                            foundation, vocab, scope_note):
    """Build the discovery prompt by substituting placeholders in the template."""
    template = _load_prompt(METHODOLOGY_PROMPT)
    if template is None:
        return None
    vocab_section = f"\n\n## Shared Vocabulary\n\n{vocab}" if vocab else ""
    foundation_section = f"\n\n{foundation}" if foundation else ""
    notes_dir = str(NOTE_DIR.relative_to(WORKSPACE))
    return (template
        .replace("{{consultation_answers}}", answers_content)
        .replace("{{asn_number}}", format_label(asn_number))
        .replace("{{title}}", inquiry["title"])
        .replace("{{question}}", inquiry["question"])
        .replace("{{slug}}", slug)
        .replace("{{foundation_section}}", foundation_section)
        .replace("{{vocabulary_section}}", vocab_section)
        .replace("{{out_of_scope_note}}", scope_note)
        .replace("{{notes_dir}}", notes_dir))


def _build_consultation_content(asn_number):
    """Walk consultation.coverage backward from the inquiry to find every
    consultation.answer doc covering it. Read each in tumbler order,
    concatenate. Returns (content, count). Substrate-grounded — no
    filename inspection.
    """
    inquiry_rel = str(
        inquiry_doc_path(asn_number).resolve().relative_to(WORKSPACE.resolve())
    )
    parts = []
    count = 0
    with open_session(LATTICE) as session:
        inquiry_addr = session.get_addr_for_path(inquiry_rel)
        if inquiry_addr is None:
            return "", 0
        coverage = sorted(
            session.active_links(
                "consultation.coverage", to_set=[inquiry_addr],
            ),
            key=lambda link: link.addr.digits,
        )
        for link in coverage:
            if not link.from_set:
                continue
            source_addr = link.from_set[0]
            if not session.active_links(
                "consultation.answer", to_set=[source_addr],
            ):
                continue
            source_rel = session.get_path_for_addr(source_addr)
            if not source_rel:
                continue
            full = WORKSPACE / source_rel
            if not full.exists():
                continue
            parts.append(full.read_text().strip())
            count += 1
    return "\n\n".join(parts), count


def _run_discovery(inquiry, asn_number, slug, force=False):
    """Invoke the discovery LLM and write the ASN file. Returns path or None."""
    outfile = NOTE_DIR / f"{format_label(asn_number)}-{slug}.md"

    if outfile.exists() and not force:
        print(f"  [SKIP] {outfile.name} already exists (use force=True to overwrite)",
              file=sys.stderr)
        return outfile

    answers_content, answer_count = _build_consultation_content(asn_number)
    if answer_count == 0:
        print(
            f"  [ERROR] No consultation answers found in substrate for "
            f"{format_label(asn_number)} — run inquiry-consult first",
            file=sys.stderr,
        )
        return None

    print(
        f"  [DISCOVERY] {answer_count} consultation answer(s) from substrate",
        file=sys.stderr,
    )

    vocab = read_file(resolve_campaign(asn_number).vocabulary_path)
    # Foundation deps come from substrate citations on the inquiry md.
    foundation = load_foundation_for_note(
        inquiry_doc_path(asn_number), asn_number,
    )
    out_of_scope = inquiry.get("out_of_scope", "")
    scope_note = (f"\n5. The following topics are OUT OF SCOPE for this ASN — "
                  f"do not define claims or operations for them, even if the "
                  f"consultation answers discuss them: {out_of_scope}"
                  if out_of_scope else "")

    prompt = _build_discovery_prompt(
        inquiry, asn_number, slug, answers_content,
        foundation, vocab, scope_note,
    )
    if prompt is None:
        return None
    print(f"  [DISCOVERY] {len(prompt)} chars (~{len(prompt)//4} tokens)",
          file=sys.stderr)

    response = invoke_claude_agent(
        prompt,
        model=MODEL,
        tools="Bash,Write,Read,Glob,Grep",
        max_turns=30,
    )
    data = response.data
    if data is None:
        return None

    _log_usage("discovery", format_label(asn_number), inquiry["title"],
               inquiry.get("area", ""), response.elapsed, data)

    if outfile.exists():
        print(f"  [OK] {outfile.name} ({outfile.stat().st_size} bytes)",
              file=sys.stderr)
        return outfile

    written = list(NOTE_DIR.glob(f"{format_label(asn_number)}-*.md"))
    if written:
        actual = written[0]
        print(
            f"  [OK] {actual.name} ({actual.stat().st_size} bytes) "
            f"[different filename]",
            file=sys.stderr,
        )
        return actual

    print(f"  [WARN] ASN file not found — saving raw response", file=sys.stderr)
    response = data.get("result", "")
    if response:
        fallback = NOTE_DIR / f"{format_label(asn_number)}-{slug}-response.md"
        fallback.write_text(response)
        return fallback

    return None


def _run_draft_for_inquiry(asn_id, *, force: bool = False):
    """Synthesize the consultation content into a formal ASN note.

    Reads the inquiry's metadata + the consultation answers (walked from
    substrate at runtime), invokes Claude to write the note md, then
    emits the `note` classifier and `provenance.synthesis` from inquiry
    → note. Returns the note path on success, None on failure.
    """
    inquiry = _load_inquiry_record(asn_id)
    if not inquiry:
        print(f"  [ERROR] No inquiry found for {format_label(asn_id)}",
              file=sys.stderr)
        return None

    asn_number = inquiry.get("id", asn_id)
    slug = _slugify(inquiry["title"])

    NOTE_DIR.mkdir(parents=True, exist_ok=True)
    print(f"{format_label(asn_number)}: {inquiry['title']}", file=sys.stderr)

    asn_path = _run_discovery(inquiry, asn_number, slug, force=force)
    if not asn_path:
        return None

    session = open_session(LATTICE)
    store = session.store
    asn_rel = str(Path(asn_path).resolve().relative_to(WORKSPACE.resolve()))
    note_addr = store.register_path(asn_rel)
    _, note_created = emit_note(store, note_addr)
    if note_created:
        print(f"  [NOTE] classifier emitted", file=sys.stderr)
    inq_path = inquiry_doc_path(asn_number)
    if inq_path.exists():
        inq_rel = str(inq_path.resolve().relative_to(WORKSPACE.resolve()))
        inq_addr = store.register_path(inq_rel)
        _, syn_created = emit_synthesis(store, inq_addr, note_addr)
        if syn_created:
            print(f"  [SYNTHESIS] inquiry → note link emitted",
                  file=sys.stderr)
    return asn_path


# ─── Agent class ────────────────────────────────────────────────


class NoteDraftAgent(Agent):
    """One initial-draft synthesis pass on a consulted inquiry."""

    role: ClassVar[str] = "note-draft"

    def run(self, session: Session, inquiry_addr: Address) -> AgentResult:
        inquiry_path_rel = session.get_path_for_addr(inquiry_addr)
        if inquiry_path_rel is None:
            return AgentResult(success=False, detail="no-inquiry-path")

        digits = extract_label_digits(inquiry_path_rel)
        if digits is None:
            return AgentResult(success=False, detail="no-asn-label")
        asn_num = int(digits)
        asn_label = format_label(asn_num)

        print(f"  [NOTE-DRAFT] {asn_label}", file=sys.stderr)

        note_path = _run_draft_for_inquiry(asn_num)
        if note_path is None:
            return AgentResult(success=False, detail="draft-failed")

        return AgentResult(
            success=True,
            detail=f"note {Path(note_path).name}",
        )
