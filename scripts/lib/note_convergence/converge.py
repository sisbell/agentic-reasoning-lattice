"""Note convergence orchestrator (§6.2 of note-convergence-protocol.md).

Drives one note through review/revise cycles until the substrate
predicate (`is_doc_converged`) holds or `max_cycles` is exhausted, with
a +1 confirmation cycle when the work loop didn't observe natural
convergence.

The substrate predicate is authoritative — the reviewer's textual
VERDICT line is one signal among others, but the cycle ends only when
both the predicate is true AND the most recent review filed zero new
revise comments.
"""

import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.common import find_asn, step_commit_asn
from lib.shared.paths import NOTE_DIR, WORKSPACE, LATTICE
from lib.note_convergence.review import (
    commit_note_review, run_note_review,
)
from lib.note_convergence.revise import (
    collect_open_revises, log_usage, run_revise_pass,
)
from lib.claim_convergence.predicates import is_doc_converged
from lib.febe.session import open_session


def run_note_convergence(asn_num, max_cycles=15, dry_run=False, model="opus",
                         effort="max"):
    """Iterative review/revise cycle on one note. Returns
    "converged" | "not_converged" | "failed".
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found in {NOTE_DIR.relative_to(WORKSPACE)}/",
              file=sys.stderr)
        return "failed"

    note_rel = str(asn_path.resolve().relative_to(LATTICE.resolve()))
    print(f"\n  [NOTE-CONVERGE] {asn_label} ({asn_path.name})", file=sys.stderr)

    start_time = time.time()
    naturally_converged = False
    last_cycle_revise_count = -1
    last_review_path = None
    failed = False

    for cycle in range(1, max_cycles + 1):
        print(f"\n  ──── Cycle {cycle}/{max_cycles} ────", file=sys.stderr)

        # RetryOpenRevises (§6.3): re-feed any unresolved comments from
        # prior cycles or invocations to the reviser before the new review.
        with open_session(LATTICE) as session:
            open_findings = collect_open_revises(session, note_rel)
        if open_findings and not dry_run:
            print(f"  [RETRY] {len(open_findings)} unresolved comment(s) "
                  f"from prior cycle(s)", file=sys.stderr)
            data, elapsed = run_revise_pass(
                asn_path, asn_label, open_findings,
                model=model, effort=effort,
            )
            if data is not None:
                log_usage(asn_label, elapsed, data)

        # Review (§6.4)
        verdict, text, elapsed = run_note_review(
            asn_path, asn_label, model=model, effort=effort,
        )
        if verdict == "ERROR" or not text:
            print(f"  [NOTE-CONVERGE] FAILED on cycle {cycle} (review error)",
                  file=sys.stderr)
            failed = True
            break

        # EmitFindings (§6.5)
        with open_session(LATTICE) as session:
            review_path, findings = commit_note_review(
                session.store, asn_path, asn_label, text,
            )
        last_review_path = review_path
        revise_findings = [f for f in findings if f[1] == "REVISE"]
        last_cycle_revise_count = len(revise_findings)
        oos_count = len(findings) - last_cycle_revise_count
        print(f"  [REVIEW] {Path(review_path).name} — "
              f"{last_cycle_revise_count} REVISE, {oos_count} OUT_OF_SCOPE, "
              f"verdict={verdict} ({elapsed:.0f}s)",
              file=sys.stderr)

        if dry_run:
            print(f"  [DRY RUN] cycle {cycle} stopping after review",
                  file=sys.stderr)
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
                log_usage(asn_label, elapsed, data)
            step_commit_asn(asn_num, f"note-converge: {asn_label} cycle {cycle}")

        # Natural convergence: this cycle's review filed zero revises AND
        # the substrate predicate is true. The cycle's review is the
        # natural confirmation; no +1 needed.
        with open_session(LATTICE) as session:
            predicate_true = is_doc_converged(session, session.get_addr_for_path(note_rel)) if session.get_addr_for_path(note_rel) is not None else True
        if last_cycle_revise_count == 0 and predicate_true:
            print(f"\n  [NOTE-CONVERGE] Natural convergence at cycle {cycle}",
                  file=sys.stderr)
            naturally_converged = True
            break

    confirmation_revise_count = 0
    if not failed and not dry_run and not naturally_converged:
        print(f"\n  ──── Confirmation review ────", file=sys.stderr)
        with open_session(LATTICE) as session:
            open_findings = collect_open_revises(session, note_rel)
        if open_findings:
            data, elapsed = run_revise_pass(
                asn_path, asn_label, open_findings,
                model=model, effort=effort,
            )
            if data is not None:
                log_usage(asn_label, elapsed, data)

        verdict, text, elapsed = run_note_review(
            asn_path, asn_label, model=model, effort=effort,
        )
        if verdict == "ERROR" or not text:
            print(f"  [NOTE-CONVERGE] confirmation failed", file=sys.stderr)
            failed = True
        else:
            with open_session(LATTICE) as session:
                review_path, findings = commit_note_review(
                    session.store, asn_path, asn_label, text,
                )
            last_review_path = review_path
            confirmation_revise_count = sum(
                1 for f in findings if f[1] == "REVISE"
            )
            oos_count = len(findings) - confirmation_revise_count
            print(f"  [CONFIRM] {Path(review_path).name} — "
                  f"{confirmation_revise_count} REVISE, "
                  f"{oos_count} OUT_OF_SCOPE, verdict={verdict} "
                  f"({elapsed:.0f}s)", file=sys.stderr)

    elapsed_total = time.time() - start_time
    if failed:
        outcome = "failed"
    elif naturally_converged:
        outcome = "converged"
    elif dry_run:
        outcome = "converged" if last_cycle_revise_count == 0 else "not_converged"
    else:
        with open_session(LATTICE) as session:
            predicate_true = is_doc_converged(session, session.get_addr_for_path(note_rel)) if session.get_addr_for_path(note_rel) is not None else True
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

    print(f"\n  [NOTE-CONVERGE] {outcome.upper()} — "
          f"{elapsed_total:.0f}s", file=sys.stderr)

    if not failed and not dry_run:
        step_commit_asn(asn_num, f"note-converge: {asn_label} — final")

    return outcome
