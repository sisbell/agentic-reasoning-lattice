"""Note convergence orchestrator (§6.2 of note-convergence-protocol.md).

Mechanical gate loop that drives one note through review/revise
cycles until the substrate predicate (`is_doc_converged`) holds or
`max_cycles` is exhausted. Each cycle: RetryOpenRevises → Review →
EmitFindings → Revise → check predicate. With a +1 confirmation
cycle when the work loop didn't observe natural convergence.

The substrate predicate is authoritative — the reviewer's textual
VERDICT line is one signal among others, but the cycle ends only
when both the predicate is true AND the most recent review filed
zero new revise comments.

Reusable helpers exported for the single-pass review and revise CLI
flows (lib/note_convergence/steps.py):

- `commit_note_review(session, asn_path, asn_label, text)` — write
  the review file, emit substrate links, return (review_path, findings)
- `collect_open_revises(session, note_rel)` — substrate query for
  unresolved revise comments on a note
- `process_resolved_issues(asn_number, review_text)` — sweep the
  ## RESOLVED section out of the open-issues file
- `log_usage(asn_label, elapsed, *, skill, data=None)` — telemetry
- `run_note_convergence(asn_num, ...)` — the gate loop entry
"""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path
from typing import Optional

from lib.agents.note_review import extract_note_findings, run_note_review
from lib.agents.note_revise import run_revise_pass
from lib.backend.emit import emit_review
from lib.protocols.febe.protocol import Session
from lib.protocols.febe.session import open_session
from lib.lattice.findings import record_one_finding
from lib.predicates import is_doc_converged, unresolved_revise_comments
from lib.shared.common import find_asn
from lib.shared.git_ops import step_commit_asn
from lib.shared.paths import (
    LATTICE, NOTE_DIR, NOTE_FINDINGS_DIR, REVIEWS_DIR,
    USAGE_LOG, WORKSPACE, open_issues_path, sorted_reviews,
)


# ---------------------------------------------------------------------------
# Reusable orchestration helpers


def collect_open_revises(session: Session, note_rel: str) -> list:
    """Return list of (comment_addr, title, body) for unresolved revise
    comments on the note.

    Reads each comment's source finding doc to get the finding text.
    Title is the first non-blank line of the body, stripped of `### `
    if present.
    """
    items = []
    note_addr = session.get_addr_for_path(note_rel)
    if note_addr is None:
        return items
    for c in unresolved_revise_comments(session, note_addr):
        if not c.from_set:
            continue
        finding_addr = c.from_set[0]
        finding_rel = session.get_path_for_addr(finding_addr)
        if not finding_rel:
            continue
        finding_full = LATTICE / finding_rel
        if not finding_full.exists():
            print(
                f"  [SKIP] finding doc missing: {finding_rel}",
                file=sys.stderr,
            )
            continue
        body = finding_full.read_text().strip()
        first_line = body.splitlines()[0] if body else ""
        title = re.sub(r"^#+\s*", "", first_line).strip() or "(untitled)"
        items.append((c.addr, title, body))
    return items


def commit_note_review(
    session: Session, asn_path: Path, asn_label: str, text: str,
):
    """Write the review file (sequential numbering) and emit substrate
    links: `review` classifier on the file, `comment.{revise|out-of-scope}`
    per finding. Returns (review_path, findings).
    """
    (REVIEWS_DIR / asn_label).mkdir(parents=True, exist_ok=True)
    existing = sorted_reviews(asn_label)
    next_num = 1
    for f in existing:
        m = re.search(r"review-(\d+)\.md$", f.name)
        if m:
            next_num = max(next_num, int(m.group(1)) + 1)
    output_path = REVIEWS_DIR / asn_label / f"review-{next_num}.md"
    body = text + "\n"

    findings = extract_note_findings(text)
    review_stem = f"review-{next_num}"
    lattice_root = session.store.lattice_dir.resolve()
    output_rel = str(output_path.resolve().relative_to(lattice_root))
    asn_rel = str(asn_path.resolve().relative_to(lattice_root))

    # 1. Document write (review aggregate)
    session.update_document(output_rel, body)

    # 2. Substrate facts
    output_addr = session.register_path(output_rel)
    asn_addr = session.register_path(asn_rel)
    emit_review(session.store, output_addr)

    findings_root = NOTE_FINDINGS_DIR / asn_label / review_stem
    for n, (_title, cls, body) in enumerate(findings):
        finding_rel = str(
            (findings_root / f"{n}.md").resolve().relative_to(lattice_root)
        )
        cls_normalized = (cls or "REVISE").upper()
        comment_kind = (
            "out-of-scope" if cls_normalized == "OUT_OF_SCOPE" else "revise"
        )
        record_one_finding(
            session,
            finding_path_rel=finding_rel,
            body=body,
            target_addr=asn_addr,
            review_addr=output_addr,
            comment_kind=comment_kind,
        )
    return output_path, findings


def process_resolved_issues(asn_number: int, review_text: str) -> None:
    """Remove resolved issues from the open issues file.

    Parses the ## RESOLVED section of a review. For each resolved
    issue, removes the matching ### heading and its content from
    the open issues file.
    """
    resolved_match = re.search(
        r"^## RESOLVED\s*\n(.*?)(?=^## |\Z)",
        review_text, re.MULTILINE | re.DOTALL,
    )
    if not resolved_match:
        return

    resolved_titles = re.findall(
        r"^### (.+)$", resolved_match.group(1), re.MULTILINE,
    )
    if not resolved_titles:
        return

    issues_path = open_issues_path(asn_number)
    if not issues_path.exists():
        return

    content = issues_path.read_text()
    original = content

    for title in resolved_titles:
        pattern = rf"^### {re.escape(title)}\s*\n.*?(?=^### |\Z)"
        content = re.sub(
            pattern, "", content, flags=re.MULTILINE | re.DOTALL,
        )
        print(f"  [RESOLVED] Removed: {title}", file=sys.stderr)

    content = content.strip()
    if content != original.strip():
        if content:
            issues_path.write_text(content + "\n")
        else:
            issues_path.unlink()
            print(
                "  [RESOLVED] All open issues resolved — file removed",
                file=sys.stderr,
            )


def log_usage(
    asn_label: str,
    elapsed: float,
    *,
    skill: str,
    data: Optional[dict] = None,
) -> None:
    """Append a usage entry to the log.

    `skill` is the operation name ("review" / "revise"). `data` is
    optional — if provided (revise's Claude-SDK output), token and
    cost stats are included.
    """
    entry = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "skill": skill,
        "asn": asn_label,
        "elapsed_s": round(elapsed, 1),
    }
    if data is not None:
        usage = data.get("usage", {})
        cost = data.get("total_cost_usd", 0)
        inp = (
            usage.get("input_tokens", 0)
            + usage.get("cache_read_input_tokens", 0)
            + usage.get("cache_creation_input_tokens", 0)
        )
        out = usage.get("output_tokens", 0)
        entry.update({
            "input_tokens": inp,
            "output_tokens": out,
            "num_turns": data.get("num_turns", 0),
            "cost_usd": cost,
        })
    try:
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


# ---------------------------------------------------------------------------
# Gate loop


def run_note_convergence(
    asn_num, max_cycles: int = 15, dry_run: bool = False,
    model: str = "opus", effort: str = "max",
) -> str:
    """Iterative review/revise cycle on one note. Returns
    "converged" | "not_converged" | "failed".
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(
            f"  ASN-{asn_num:04d} not found in "
            f"{NOTE_DIR.relative_to(WORKSPACE)}/",
            file=sys.stderr,
        )
        return "failed"

    note_rel = str(asn_path.resolve().relative_to(LATTICE.resolve()))
    print(
        f"\n  [NOTE-CONVERGE] {asn_label} ({asn_path.name})",
        file=sys.stderr,
    )

    start_time = time.time()
    naturally_converged = False
    last_cycle_revise_count = -1
    last_review_path = None
    failed = False

    for cycle in range(1, max_cycles + 1):
        print(f"\n  ──── Cycle {cycle}/{max_cycles} ────", file=sys.stderr)

        # RetryOpenRevises (§6.3)
        with open_session(LATTICE) as session:
            open_findings = collect_open_revises(session, note_rel)
        if open_findings and not dry_run:
            print(
                f"  [RETRY] {len(open_findings)} unresolved comment(s) "
                f"from prior cycle(s)", file=sys.stderr,
            )
            data, elapsed = run_revise_pass(
                asn_path, asn_label, open_findings,
                model=model, effort=effort,
            )
            if data is not None:
                log_usage(asn_label, elapsed, skill="revise", data=data)

        # Review (§6.4)
        verdict, text, elapsed = run_note_review(
            asn_path, asn_label, model=model, effort=effort,
        )
        if verdict == "ERROR" or not text:
            print(
                f"  [NOTE-CONVERGE] FAILED on cycle {cycle} (review error)",
                file=sys.stderr,
            )
            failed = True
            break

        # EmitFindings (§6.5)
        with open_session(LATTICE) as session:
            review_path, findings = commit_note_review(
                session, asn_path, asn_label, text,
            )
        last_review_path = review_path
        revise_findings = [f for f in findings if f[1] == "REVISE"]
        last_cycle_revise_count = len(revise_findings)
        oos_count = len(findings) - last_cycle_revise_count
        print(
            f"  [REVIEW] {Path(review_path).name} — "
            f"{last_cycle_revise_count} REVISE, {oos_count} OUT_OF_SCOPE, "
            f"verdict={verdict} ({elapsed:.0f}s)", file=sys.stderr,
        )

        if dry_run:
            print(
                f"  [DRY RUN] cycle {cycle} stopping after review",
                file=sys.stderr,
            )
            break

        # Revise (§6.6)
        if revise_findings:
            with open_session(LATTICE) as session:
                cycle_findings = collect_open_revises(session, note_rel)
            data, elapsed = run_revise_pass(
                asn_path, asn_label, cycle_findings,
                model=model, effort=effort,
            )
            if data is not None:
                log_usage(asn_label, elapsed, skill="revise", data=data)
            step_commit_asn(
                asn_num,
                f"note-converge: {asn_label} cycle {cycle}",
            )

        # Natural convergence
        with open_session(LATTICE) as session:
            note_addr = session.get_addr_for_path(note_rel)
            predicate_true = (
                is_doc_converged(session, note_addr)
                if note_addr is not None else True
            )
        if last_cycle_revise_count == 0 and predicate_true:
            print(
                f"\n  [NOTE-CONVERGE] Natural convergence at cycle {cycle}",
                file=sys.stderr,
            )
            naturally_converged = True
            break

    confirmation_revise_count = 0
    if not failed and not dry_run and not naturally_converged:
        print("\n  ──── Confirmation review ────", file=sys.stderr)
        with open_session(LATTICE) as session:
            open_findings = collect_open_revises(session, note_rel)
        if open_findings:
            data, elapsed = run_revise_pass(
                asn_path, asn_label, open_findings,
                model=model, effort=effort,
            )
            if data is not None:
                log_usage(asn_label, elapsed, skill="revise", data=data)

        verdict, text, elapsed = run_note_review(
            asn_path, asn_label, model=model, effort=effort,
        )
        if verdict == "ERROR" or not text:
            print(f"  [NOTE-CONVERGE] confirmation failed", file=sys.stderr)
            failed = True
        else:
            with open_session(LATTICE) as session:
                review_path, findings = commit_note_review(
                    session, asn_path, asn_label, text,
                )
            last_review_path = review_path
            confirmation_revise_count = sum(
                1 for f in findings if f[1] == "REVISE"
            )
            oos_count = len(findings) - confirmation_revise_count
            print(
                f"  [CONFIRM] {Path(review_path).name} — "
                f"{confirmation_revise_count} REVISE, "
                f"{oos_count} OUT_OF_SCOPE, verdict={verdict} "
                f"({elapsed:.0f}s)", file=sys.stderr,
            )

    elapsed_total = time.time() - start_time
    if failed:
        outcome = "failed"
    elif naturally_converged:
        outcome = "converged"
    elif dry_run:
        outcome = (
            "converged" if last_cycle_revise_count == 0 else "not_converged"
        )
    else:
        with open_session(LATTICE) as session:
            note_addr = session.get_addr_for_path(note_rel)
            predicate_true = (
                is_doc_converged(session, note_addr)
                if note_addr is not None else True
            )
        outcome = (
            "converged"
            if confirmation_revise_count == 0 and predicate_true
            else "not_converged"
        )

    if last_review_path is not None and not failed:
        with open(last_review_path, "a") as rf:
            rf.write(f"\n## Result\n\n")
            if outcome == "converged":
                rf.write("Note converged.\n")
            else:
                rf.write(f"Note not converged after {cycle} cycle(s).\n")
            rf.write(f"\n*Elapsed: {elapsed_total:.0f}s*\n")

    print(
        f"\n  [NOTE-CONVERGE] {outcome.upper()} — "
        f"{elapsed_total:.0f}s", file=sys.stderr,
    )

    if not failed and not dry_run:
        step_commit_asn(asn_num, f"note-converge: {asn_label} — final")

    return outcome
