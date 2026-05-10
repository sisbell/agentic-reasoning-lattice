"""Note-consult agent — channel-assign + gather evidence for the
latest review that still has uncovered revise findings.

Fires when at least one open `comment.revise` finding on the note
lacks a `consultation.coverage` link. Per fire:

  1. Walk the note's review dirs newest-to-oldest, find the latest
     `review-N` that owns an uncovered open revise.
  2. Channel-assign each REVISE item via the assign-channels LLM,
     decide which channels (theory/evidence) each finding needs.
  3. Run targeted consultations (theory parallel, evidence sequential).
  4. Persist per-Q/A answer docs, emit `consultation.assessment`,
     `consultation.answer.<role>`, and `consultation.coverage` links.
  5. Commit.

Picking the newest uncovered review (not just the latest review)
avoids re-running consult on a review that's already fully covered,
while still progressing toward the predicate flipping True. The
runner handles iteration if multiple reviews have uncovered findings.

Channel-name parsing tolerates both the generic role labels
("Theory"/"Evidence" — shared prompt) and the capitalized channel
names ("Nelson"/"Gregory"/"Maxwell-1867"/…) that lattice-specific
overrides may use. Channel name itself, title-cased by '-', IS the
label for convention-based parsing.
"""

from __future__ import annotations

import re
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import ClassVar

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.backend.emit import (
    emit_consultation_answer, emit_consultation_assessment,
    emit_consultation_coverage,
)
from lib.consultation.consult import invoke_claude
from lib.consultation.plugin import load_channel_plugin
from lib.predicates import (
    is_finding_consulted, unresolved_revise_comments,
)
from lib.protocols.febe.protocol import Session
from lib.protocols.febe.session import open_session
from lib.lattice.labels import extract_label_digits, format_label
from lib.shared.campaign import resolve_campaign
from lib.shared.common import read_file
from lib.shared.git_ops import step_commit_asn
from lib.shared.invoke_claude import get_total_usage
from lib.shared.paths import (
    LATTICE, NOTE_FINDINGS_DIR, REVIEWS_DIR,
    consultation_dir, load_channel_meta, prompt_path,
)


# ─── Channel assignment ────────────────────────────────────────


_ASSIGN_PROMPT_TEMPLATE = prompt_path("agents/producers/note_consult.md")

# Always-recognized role labels, regardless of channels bound.
_ROLE_LABELS = {"Theory": "theory", "Evidence": "evidence"}


def _capitalize_channel(name):
    """Title-case a channel name by its '-' separators.
    nelson → Nelson, maxwell-1867 → Maxwell-1867."""
    return "-".join(p[:1].upper() + p[1:] for p in name.split("-"))


def _channel_description(channel_name):
    desc = (load_channel_meta(channel_name).get("description") or "").strip()
    if not desc:
        raise ValueError(
            f"channel {channel_name} meta.yaml missing `description:` field")
    return desc


def _display_names(asn_id):
    """Return {role: capitalized_channel_name} for the ASN's bound channels.
    Used for category labels in log output."""
    campaign = resolve_campaign(asn_id)
    return {
        "theory": _capitalize_channel(campaign.theory_channel),
        "evidence": _capitalize_channel(campaign.evidence_channel),
    }


def _category_label(roles, asn_id):
    """Derive a display category from the set of channels a finding needs."""
    if not roles:
        return "INTERNAL"
    if len(roles) >= 2:
        return "BOTH"
    return _display_names(asn_id)[next(iter(roles))].upper()


def _build_assign_prompt(asn_content, revise_section, asn_id):
    """Build the channel-assignment prompt by reading each bound channel's
    description from meta.yaml and substituting into the prompt template."""
    template = read_file(_ASSIGN_PROMPT_TEMPLATE)
    if not template:
        raise FileNotFoundError(
            f"prompt template not found: {_ASSIGN_PROMPT_TEMPLATE}",
        )
    campaign = resolve_campaign(asn_id)
    return template.format(
        asn_content=asn_content,
        revise_section=revise_section,
        theory_description=_channel_description(campaign.theory_channel),
        evidence_description=_channel_description(campaign.evidence_channel),
    )


def _parse_assignment(response, asn_id):
    """Parse a channel-assignment response into finding dicts.

    Each returned finding has: number (int), title (str), reason
    (str or None), questions (dict[role, question_text]; empty when
    internal).
    """
    campaign = resolve_campaign(asn_id)
    # Channel names first; hardcoded role labels last so they always win
    # if a channel name happens to collide with "Theory"/"Evidence".
    authority_to_role = {
        _capitalize_channel(campaign.theory_channel): "theory",
        _capitalize_channel(campaign.evidence_channel): "evidence",
    }
    authority_to_role.update(_ROLE_LABELS)

    items = []
    current = None
    for line in response.split("\n"):
        line = line.strip()

        m = re.match(r"##\s+Issue\s+(\d+):\s*(.+)", line)
        if m:
            if current:
                items.append(current)
            current = {
                "number": int(m.group(1)),
                "title": m.group(2).strip(),
                "reason": None,
                "questions": {},
            }
            continue
        if current is None:
            continue

        m = re.match(r"Reason:\s*(.+)", line)
        if m:
            current["reason"] = m.group(1).strip()
            continue

        m = re.match(r"(\w[\w-]*)\s+question:\s*(.+)", line)
        if m:
            role = authority_to_role.get(m.group(1))
            if role:
                current["questions"][role] = m.group(2).strip()

    if current:
        items.append(current)
    return items


# ─── Review parsing ────────────────────────────────────────────


def _get_review_number(review_path):
    """Extract N from filename like review-6.md."""
    m = re.search(r"review-(\d+)", Path(review_path).stem)
    return int(m.group(1)) if m else 1


def _extract_revise_section(review_content):
    """Return the body under the review's `## REVISE` header."""
    lines = review_content.split("\n")
    in_revise = False
    revise_lines = []

    for line in lines:
        if line.strip() == "## REVISE":
            in_revise = True
            continue
        if in_revise and line.startswith("## ") and line.strip() != "## REVISE":
            break
        if in_revise:
            revise_lines.append(line)

    return "\n".join(revise_lines).strip()


# ─── Per-Q/A answer files ──────────────────────────────────────


def _answer_path(consult_subdir, issue_number, role):
    """Per-answer file path; mirrors the inquiry-consult layout."""
    return consult_subdir / f"answer-{issue_number:02d}-{role}.md"


def _save_answer(consult_subdir, item, role, answer):
    """Persist one Q+A pair to its own doc.

    Format:
        ## Question N [role]

        > <question text>

        <answer body>
    """
    question = item.get("questions", {}).get(role, "")
    path = _answer_path(consult_subdir, item["number"], role)
    body = answer.strip() if answer else "[No answer]"
    path.write_text(
        f"## Question {item['number']} [{role}]\n\n"
        f"> {question}\n\n"
        f"{body}\n"
    )


def _run_targeted_consultations(items, asn_id, consult_subdir, model="opus"):
    """Run channel consultations for items with assigned questions.

    Theory consultations run in parallel (no tools).
    Evidence consultations run sequentially (each runs KB + code in
    parallel internally). Mutates items in place; eagerly persists each
    answer to its own substrate-citizen doc.
    """
    campaign = resolve_campaign(asn_id)
    theory_channel = campaign.theory_channel
    evidence_channel = campaign.evidence_channel

    theory_work = []
    evidence_work = []

    for i, item in enumerate(items):
        item.setdefault("answers", {})
        for role, question in item.get("questions", {}).items():
            if role == "theory":
                theory_work.append((i, question))
            elif role == "evidence":
                evidence_work.append((i, question))

    if theory_work:
        print(f"  [THEORY] Firing {len(theory_work)} consultations in parallel...",
              file=sys.stderr)
        threads = []

        for idx, (item_idx, question) in enumerate(theory_work):
            def run_t(ii=item_idx, q=question, n=idx + 1):
                answer = load_channel_plugin(theory_channel).consult(
                    q, label=f"Q{n}:theory",
                    model=model, effort="max")
                items[ii]["answers"]["theory"] = answer
                _save_answer(consult_subdir, items[ii], "theory", answer)
            t = threading.Thread(target=run_t)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
        print(f"  [THEORY] All done", file=sys.stderr)

    if evidence_work:
        print(f"  [EVIDENCE] Running {len(evidence_work)} consultations sequentially...",
              file=sys.stderr)
        for idx, (item_idx, question) in enumerate(evidence_work):
            answer = load_channel_plugin(evidence_channel).consult(
                question, label=f"Q{idx + 1}:evidence",
                model="sonnet", effort="max")
            items[item_idx]["answers"]["evidence"] = answer
            _save_answer(consult_subdir, items[item_idx], "evidence", answer)
        print(f"  [EVIDENCE] All done", file=sys.stderr)


# ─── Finding-address pairing ───────────────────────────────────


def _revise_finding_addrs_for_review(session, asn_label, review_num):
    """Return REVISE finding doc addresses for this review, in document order.

    Walks `finding/notes/<asn>/review-N/` by filename (0.md, 1.md, …)
    and keeps only those that have an active `comment.revise` link.
    Aligns by position with `_parse_assignment`'s items — both filter
    the same review's findings to REVISE-only in the same document order.
    """
    findings_dir = NOTE_FINDINGS_DIR / asn_label / f"review-{review_num}"
    if not findings_dir.exists():
        return []

    def _key(p):
        try:
            return int(p.stem)
        except ValueError:
            return 9999

    addrs = []
    for path in sorted(findings_dir.glob("*.md"), key=_key):
        rel = str(path.resolve().relative_to(LATTICE.resolve()))
        finding_addr = session.get_addr_for_path(rel)
        if finding_addr is None:
            continue
        if session.active_links("comment.revise", from_set=[finding_addr]):
            addrs.append(finding_addr)
    return addrs


# ─── Run for one (asn, review) ─────────────────────────────────


def _run_consult_for_review(
    asn_path,
    asn_label,
    review_path,
    *,
    model: str = "opus",
):
    """Run the consult flow for one specific review of one ASN.

    Returns the consult subdirectory path, or None if no REVISE
    section / channel-assignment failed.

    Substrate emits:
      - consultation.assessment classifier on assessment.md
      - consultation.answer.<role> classifier on each answer file
      - consultation.coverage from assessment → each REVISE finding
      - consultation.coverage from each answer → its finding

    No aggregate results doc — downstream consumers (NoteReviseAgent)
    construct consultation content at runtime by walking
    consultation.coverage links to find their answers.
    """
    review_content = Path(review_path).read_text()
    review_num = _get_review_number(review_path)

    revise_section = _extract_revise_section(review_content)
    if not revise_section:
        print(
            f"  No REVISE section in {Path(review_path).name}",
            file=sys.stderr,
        )
        return None

    asn_content = asn_path.read_text()

    print(
        f"  [CONSULT-REVISION] {asn_label} + {Path(review_path).name}",
        file=sys.stderr,
    )

    total_start = time.time()

    print(f"  [ASSIGN] Building prompt...", file=sys.stderr)
    prompt = _build_assign_prompt(asn_content, revise_section, asn_label)
    print(f"  [ASSIGN] Prompt: {len(prompt) // 1024}KB", file=sys.stderr)

    result = invoke_claude(
        prompt, model=model, effort="max",
        allow_tools=False, label="assign",
        skill="gather-evidence:assign",
    )

    if not result.text:
        print(f"  [ASSIGN] Failed", file=sys.stderr)
        return None

    output_dir = consultation_dir(asn_label)
    output_dir.mkdir(parents=True, exist_ok=True)
    consult_subdir = output_dir / f"consultation-{review_num}"
    consult_subdir.mkdir(parents=True, exist_ok=True)
    cat_path = consult_subdir / "assessment.md"
    cat_path.write_text(
        f"# Channel Assignment — {asn_label} review-{review_num}\n\n"
        f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        f"{result.text}\n"
    )
    print(f"  [ASSIGN] Saved to {cat_path}", file=sys.stderr)

    session = open_session(LATTICE)
    store = session.store
    cat_rel = str(cat_path.resolve().relative_to(LATTICE.resolve()))
    cat_addr = store.register_path(cat_rel)
    emit_consultation_assessment(store, cat_addr)

    items = _parse_assignment(response, asn_label)
    if not items:
        print(f"  [ASSIGN] No items parsed from response", file=sys.stderr)
        return None

    finding_addrs = _revise_finding_addrs_for_review(
        session, asn_label, review_num,
    )
    if len(finding_addrs) != len(items):
        print(
            f"  [WARN] item/finding count mismatch: "
            f"{len(items)} items, {len(finding_addrs)} REVISE findings — "
            f"coverage links may be incomplete",
            file=sys.stderr,
        )
    for item, finding_addr in zip(items, finding_addrs):
        item["finding_addr"] = finding_addr
        emit_consultation_coverage(store, cat_addr, finding_addr)

    internal_count = sum(1 for it in items if not it["questions"])
    consult_count = len(items) - internal_count
    print(
        f"  [ASSIGN] {len(items)} items: "
        f"{internal_count} internal, {consult_count} need consultation",
        file=sys.stderr,
    )

    for item in items:
        tag = _category_label(item["questions"].keys(), asn_label)
        print(
            f"    Issue {item['number']}: {tag} — {item['title']}",
            file=sys.stderr,
        )

    if consult_count > 0:
        print(f"", file=sys.stderr)
        _run_targeted_consultations(items, asn_label, consult_subdir, model=model)
    else:
        print(
            f"  [CONSULT] All items internal, no consultations needed",
            file=sys.stderr,
        )

    session = open_session(LATTICE)
    store = session.store
    for item in items:
        finding_addr = item.get("finding_addr")
        for role in item.get("questions", {}).keys():
            answer_md = _answer_path(consult_subdir, item["number"], role)
            if not answer_md.exists():
                continue
            answer_rel = str(answer_md.resolve().relative_to(LATTICE.resolve()))
            answer_addr = store.register_path(answer_rel)
            emit_consultation_answer(store, answer_addr, role)
            if finding_addr is not None:
                emit_consultation_coverage(store, answer_addr, finding_addr)

    total_elapsed = time.time() - total_start

    print(f"", file=sys.stderr)
    print(f"  {'=' * 50}", file=sys.stderr)
    print(f"  REVISION CONSULTATION COMPLETE", file=sys.stderr)
    print(f"  {'=' * 50}", file=sys.stderr)
    print(
        f"  Items: {len(items)} ({internal_count} internal, "
        f"{consult_count} consulted)", file=sys.stderr,
    )
    print(
        f"  Total: {total_elapsed:.0f}s ({total_elapsed/60:.1f}min)",
        file=sys.stderr,
    )

    totals = get_total_usage()
    if totals["calls"] > 0:
        print(
            f"  Total cost: ${totals['cost_usd']:.4f} "
            f"({totals['calls']} calls)", file=sys.stderr,
        )

    print(f"  Output: {consult_subdir}", file=sys.stderr)
    return consult_subdir


# ─── Review-picker helper ─────────────────────────────────────


def _review_num_from_finding_path(path: str) -> int | None:
    """Extract N from `_docuverse/.../review-N/<n>.md`."""
    m = re.search(r"review-(\d+)/\d+\.md$", path)
    return int(m.group(1)) if m else None


def _latest_uncovered_review(session: Session, note_addr: Address):
    """Return (review_num, review_path) of the highest-numbered review
    that owns at least one uncovered open revise. None if all open
    revises are already covered.
    """
    best_num = -1
    for c in unresolved_revise_comments(session, note_addr):
        if not c.from_set:
            continue
        finding_addr = c.from_set[0]
        if is_finding_consulted(session, finding_addr):
            continue
        finding_path = session.get_path_for_addr(finding_addr)
        if not finding_path:
            continue
        review_num = _review_num_from_finding_path(finding_path)
        if review_num is None:
            continue
        if review_num > best_num:
            best_num = review_num

    if best_num < 0:
        return None

    note_path = session.get_path_for_addr(note_addr)
    digits = extract_label_digits(note_path or "")
    if digits is None:
        return None
    asn_label = format_label(int(digits))
    review_path = REVIEWS_DIR / asn_label / f"review-{best_num}.md"
    if not review_path.exists():
        return None
    return best_num, review_path


# ─── Agent class ──────────────────────────────────────────────


class NoteConsultAgent(Agent):
    """One channel-assignment + gather-evidence pass on the latest
    uncovered review of a note."""

    role: ClassVar[str] = "note-consult"

    def __init__(self, *, model: str = "opus"):
        self.model = model

    def run(self, session: Session, note_addr: Address) -> AgentResult:
        note_path_rel = session.get_path_for_addr(note_addr)
        if note_path_rel is None:
            return AgentResult(success=False, detail="no-note-path")

        asn_path = session.store.lattice_dir / note_path_rel
        if not asn_path.exists():
            return AgentResult(success=False, detail="no-note-file")

        digits = extract_label_digits(note_path_rel)
        if digits is None:
            return AgentResult(success=False, detail="no-asn-label")
        asn_number = int(digits)
        asn_label = format_label(asn_number)

        target = _latest_uncovered_review(session, note_addr)
        if target is None:
            return AgentResult(
                success=True, detail="all-revises-already-covered",
            )
        review_num, review_path = target

        print(
            f"  [NOTE-CONSULT] {asn_label} review-{review_num}",
            file=sys.stderr,
        )

        consult_subdir = _run_consult_for_review(
            asn_path, asn_label, review_path, model=self.model,
        )
        if consult_subdir is None:
            return AgentResult(success=False, detail="consult-failed")

        step_commit_asn(
            asn_number,
            f"note-consult(asn): {asn_label} review-{review_num}",
        )

        return AgentResult(
            success=True,
            detail=f"review-{review_num} | {Path(consult_subdir).name}",
        )
