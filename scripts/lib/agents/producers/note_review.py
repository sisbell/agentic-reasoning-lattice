"""Note-review agent — assemble prompt, invoke Claude, write review doc,
emit substrate facts.

`NoteReviewAgent` is the class-form entry point the trigger runner
invokes. One fire = one full review pass: build prompt, invoke
Claude, validate the response structure, write the review aggregate
doc, emit the `review` classifier + `review.coverage` to the note
+ `comment.<kind>` per finding. Returns AgentResult.

`extract_note_findings(text)` is a pure helper for parsing a stored
review's REVISE / OUT_OF_SCOPE sections.
"""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path
from typing import ClassVar, List, Tuple

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.backend.emit import (
    emit_citation_bundle, emit_review_content, emit_review_coverage,
)
from lib.predicates import version_head
from lib.lattice.config import lattice_config
from lib.lattice.findings import record_one_finding
from lib.lattice.labels import (
    extract_label_digits,
    format_label,
    label_pattern,
)
from lib.protocols.febe.protocol import Session
from lib.shared.campaign import resolve_campaign
from lib.shared.common import read_file
from lib.shared.foundation import (
    FoundationError, foundation_dep_addrs, load_foundation,
)
from lib.shared.invoke_claude import invoke_claude
from lib.shared.paths import (
    NOTE_FINDINGS_DIR, REVIEWS_DIR, USAGE_LOG, WORKSPACE,
    load_inquiry, next_review_number, prompt_path,
)


REVIEW_TEMPLATE = prompt_path("agents/producers/note_review.md")
ANTI_BLOAT_BLOCK = prompt_path(
    "agents/producers/note_review_anti_bloat.md",
)


def extract_note_findings(text: str) -> List[Tuple[str, str, str]]:
    """Extract note-review findings, classified by parent section.

    Note reviews have top-level `## REVISE` and `## OUT_OF_SCOPE` sections,
    each containing `### Title` subheadings. Returns list of
    (title, cls, body) tuples where cls ∈ {"REVISE", "OUT_OF_SCOPE"}.
    Other top-level sections (e.g. `## RESOLVED`) are ignored — they
    are not findings against the note.
    """
    findings = []
    parts = re.split(r"^## ", text, flags=re.MULTILINE)
    for part in parts[1:]:  # skip preamble before first ##
        section_lines = part.split("\n", 1)
        section_header = section_lines[0].strip()
        section_body = section_lines[1] if len(section_lines) > 1 else ""
        if section_header == "REVISE":
            cls = "REVISE"
        elif section_header == "OUT_OF_SCOPE":
            cls = "OUT_OF_SCOPE"
        else:
            continue
        finding_parts = re.split(r"^### ", section_body, flags=re.MULTILINE)
        for fpart in finding_parts[1:]:
            lines = fpart.strip().split("\n", 1)
            title = lines[0].strip()
            body = lines[1].strip() if len(lines) > 1 else ""
            findings.append((title, cls, f"### {title}\n{body}"))
    return findings


# ---------------------------------------------------------------------------
# Prompt context loaders


def _load_out_of_scope(asn_number: int) -> str:
    """Look up out_of_scope for an ASN from its inquiry frontmatter."""
    return load_inquiry(asn_number).get("out_of_scope", "")


# ---------------------------------------------------------------------------
# Prompt rendering


def _build_prompt(
    asn_content: str, vocabulary: str, out_of_scope: str = "",
    foundation: str = "", anti_bloat: bool = False,
) -> str:
    """Assemble review prompt from template + injected content.

    Caller supplies `foundation` directly. The template's foundation
    slot can be empty if the ASN has no upstream deps.

    `anti_bloat=True` appends the forward-reference accretion patterns
    from `note_review_anti_bloat.md` (used when the note carries the
    `review-mode.anti-bloat` classifier).
    """
    template_path = REVIEW_TEMPLATE
    template = read_file(template_path)
    if not template:
        import sys
        print(
            f"  Review prompt template not found at "
            f"{template_path.relative_to(WORKSPACE)}",
            file=sys.stderr,
        )
        sys.exit(1)

    scope_note = (
        f"\n\n## Scope\n\nThe following topics are OUT OF SCOPE for this "
        f"ASN. Do not flag missing coverage for them. If the ASN defines "
        f"claims for these topics, flag them as OUT_OF_SCOPE: "
        f"{out_of_scope}"
        if out_of_scope else ""
    )

    anti_bloat_section = ""
    if anti_bloat:
        anti_bloat_section = "\n\n" + read_file(ANTI_BLOAT_BLOCK)

    return template.replace(
        "{{asn_content}}", asn_content
    ).replace(
        "{{vocabulary}}", vocabulary
    ).replace(
        "{{foundation_statements}}", foundation
    ) + scope_note + anti_bloat_section


# ---------------------------------------------------------------------------
# Response validation


def _strip_preamble(text: str) -> str:
    """Strip any tool-use preamble before the review header."""
    marker = re.search(rf"^# Review of {label_pattern().pattern}", text, re.MULTILINE)
    if marker:
        return text[marker.start():]
    return text


def _validate_review(text: str):
    """Check that review text has required structure. Returns error message or None."""
    if not re.search(rf"^# Review of {label_pattern().pattern}", text, re.MULTILINE):
        return f"missing '# Review of {lattice_config().label_prefix}-NNNN' header"
    verdict_match = re.search(r"^VERDICT:\s*(\w+)", text, re.MULTILINE)
    if not verdict_match:
        return "missing VERDICT line"
    verdict = verdict_match.group(1).upper()
    has_sections = bool(
        re.search(r"^## REVISE", text, re.MULTILINE)
        or re.search(r"^## OUT_OF_SCOPE", text, re.MULTILINE)
    )
    # CONVERGED reviews have nothing to enumerate; empty section headers
    # are bureaucratic. Sections required only when verdict != CONVERGED.
    if verdict != "CONVERGED" and not has_sections:
        return "missing ## REVISE or ## OUT_OF_SCOPE section (required when VERDICT != CONVERGED)"
    return None


# ---------------------------------------------------------------------------
# Trigger-runner entry: class form


def _log_review_usage(asn_label: str, elapsed: float) -> None:
    """Append a review-usage entry to the lattice usage log."""
    entry = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "skill": "note-review",
        "asn": asn_label,
        "elapsed_s": round(elapsed, 1),
    }
    try:
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


class NoteReviewAgent(Agent):
    """One LLM-driven review pass over a note.

    Fires on a note address that's not yet in the
    `is_doc_quiescent AND latest_review_was_clean` state. One fire =
    one review aggregate doc + one `comment.<kind>` per finding.
    """

    role: ClassVar[str] = "note-review"

    def __init__(self, *, model: str = "opus", effort: str = "max"):
        self.model = model
        self.effort = effort

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

        # Assemble + invoke
        asn_content = asn_path.read_text()
        vocabulary = read_file(resolve_campaign(asn_label).vocabulary_path)
        out_of_scope = _load_out_of_scope(asn_number)
        try:
            foundation = load_foundation(asn_number)
        except FoundationError as e:
            print(
                f"  [FOUNDATION] {asn_label}: {e}",
                file=sys.stderr,
            )
            return AgentResult(
                success=False,
                detail=f"foundation-load-failed: {e}",
            )
        anti_bloat = bool(
            session.active_links(
                "review-mode.anti-bloat", to_set=[note_addr],
            )
        )
        if anti_bloat:
            print(
                f"  [NOTE-REVIEW] anti-bloat mode enabled for {asn_label}",
                file=sys.stderr,
            )
        prompt = _build_prompt(
            asn_content, vocabulary,
            out_of_scope=out_of_scope,
            foundation=foundation,
            anti_bloat=anti_bloat,
        )
        response = invoke_claude(
            prompt, model=self.model, effort=self.effort,
            tools="", output_format=None,
        )
        if not response.text:
            return AgentResult(
                success=False, elapsed=response.elapsed, detail="llm-failed",
            )
        text = _strip_preamble(response.text)
        validation_error = _validate_review(text)
        if validation_error:
            print(f"  MALFORMED REVIEW: {validation_error}", file=sys.stderr)
            # Capture raw output to workspace for debugging malformed reviews.
            from lib.shared.paths import WORKSPACE_DIR
            from datetime import datetime, timezone
            debug_dir = WORKSPACE_DIR / "debug" / "malformed-reviews"
            debug_dir.mkdir(parents=True, exist_ok=True)
            ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
            debug_path = debug_dir / f"{asn_label}-{ts}.md"
            debug_path.write_text(
                f"# Malformed review capture — {asn_label}\n\n"
                f"*{ts}* / model={self.model}, effort={self.effort}, "
                f"anti_bloat={anti_bloat}, elapsed={response.elapsed:.0f}s, "
                f"prompt_kb={len(prompt)/1024:.1f}*\n\n"
                f"## Validation error\n\n{validation_error}\n\n"
                f"## Raw response (length={len(response.text)} chars)\n\n"
                f"```\n{response.text}\n```\n"
            )
            print(
                f"  [DEBUG] raw output captured: "
                f"{debug_path.relative_to(WORKSPACE_DIR.parent)}",
                file=sys.stderr,
            )
            return AgentResult(
                success=False, elapsed=response.elapsed,
                detail=f"malformed: {validation_error}",
            )

        # Persist review aggregate doc + emit substrate facts
        next_n = next_review_number(asn_label, kind="note")
        review_dir = REVIEWS_DIR / asn_label
        review_dir.mkdir(parents=True, exist_ok=True)
        review_path = review_dir / f"review-{next_n}.md"
        body = text + "\n"

        review_rel = str(review_path.relative_to(session.store.lattice_dir))
        session.update_document(review_rel, body)
        review_addr = session.register_path(review_rel)
        emit_review_content(session.store, review_addr)
        emit_review_coverage(session.store, review_addr, note_addr)

        # Cascade anchor: record which foundation version each upstream
        # was at when this review read the note. The cascade-fresh
        # predicate walks this bundled link's to_set checking
        # is_head_version per target; any non-head target means an
        # upstream advanced since the anchor was emitted, re-firing
        # note_review on the stale note.
        #
        # Dep addresses come via `foundation_dep_addrs` — the same
        # resolution path the loader just used. Querying citation.depends
        # from note_addr would silently return empty for HEALTHY ASNs
        # (citations live on inquiry_addr); the helper consults the
        # canonical source.
        foundation_heads = [
            version_head(session, dep)
            for dep in foundation_dep_addrs(session, asn_number)
        ]
        if foundation_heads:
            emit_citation_bundle(
                session.store, review_addr, foundation_heads,
                direction="depends",
            )

        findings = extract_note_findings(text)
        findings_root = NOTE_FINDINGS_DIR / asn_label / f"review-{next_n}"
        for n, (_title, cls, fbody) in enumerate(findings):
            finding_rel = str(
                (findings_root / f"{n}.md").relative_to(
                    session.store.lattice_dir,
                )
            )
            comment_kind = (
                "out-of-scope" if (cls or "REVISE").upper() == "OUT_OF_SCOPE"
                else "revise"
            )
            record_one_finding(
                session,
                finding_path_rel=finding_rel,
                body=fbody,
                target_addr=note_addr,
                review_addr=review_addr,
                comment_kind=comment_kind,
            )

        revise_count = sum(
            1 for _, c, _ in findings if (c or "").upper() == "REVISE"
        )
        oos_count = len(findings) - revise_count

        _log_review_usage(asn_label, response.elapsed)
        print(
            f"  [NOTE-REVIEW] {asn_label} {review_path.name} — "
            f"{revise_count} REVISE, {oos_count} OUT_OF_SCOPE "
            f"({response.elapsed:.0f}s)",
            file=sys.stderr,
        )

        # Commit the review aggregate + finding docs + substrate emits
        # as a discrete pipeline event (matches cone-review pattern).

        return AgentResult(
            success=True,
            elapsed=response.elapsed,
            detail=(
                f"review-{next_n} | revise={revise_count} oos={oos_count}"
            ),
        )
