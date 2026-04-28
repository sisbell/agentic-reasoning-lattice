#!/usr/bin/env python3
"""
Full Review — deep structural analysis with convergence.

Reads the whole ASN + foundation and finds issues that per-claim
pipelines can't catch: carrier-set conflation, precondition chain gaps,
arguments that assume what they prove, missing cases that hold by
coincidence in examples.

Whole-ASN review, not per-claim. Convergence: review → fix findings →
re-review → converge.

Includes dependency cone detection: when one claim keeps getting
revised while its dependencies are stable, switches to a focused
regional review/revise loop to accelerate convergence.

Usage:
    python scripts/full-review.py 40
    python scripts/full-review.py 40 --max-cycles 1     # single pass, no fixing
    python scripts/full-review.py 40 --dry-run           # review only
    python scripts/full-review.py 36 --cone S8           # force regional review on cone apex S8
"""

import argparse
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import (
    WORKSPACE, CLAIM_CONVERGENCE_DIR, CLAIM_FINDINGS_DIR,
    agent_doc_path, next_review_number, review_meta_path,
)
from lib.shared.common import find_asn, assemble_readonly, step_commit_asn
from lib.claim_convergence.full_review.review import (
    run_review, extract_findings, filter_revise,
    cycle_verdict, findings_summary,
)
from lib.claim_convergence.full_review.revise import revise
from lib.claim_convergence.gate import run_validate_gate
from lib.claim_convergence.cone import (
    detect_dependency_cone, run_cone_review, _retry_unresolved_revises,
)
from lib.store.store import agent_context, default_store
from lib.store.emit import emit_findings, emit_meta
from lib.store.populate import build_cross_asn_label_index
from lib.store.queries import is_asn_converged


def run_full_review(asn_num, max_cycles=8, dry_run=False, model="opus"):
    """Run the full review pipeline.

    Returns "converged" or "not_converged".

    Operations are attributed to the full-review agent: substrate writes
    inside the block (review/comment/resolution links) get a `manages`
    link from the agent doc, and subprocess tools (decide.py, etc.)
    inherit `XANADU_AGENT_DOC` so their writes are attributed too.
    """
    with agent_context(agent_doc_path("full-review")):
        return _run_full_review_attributed(
            asn_num, max_cycles=max_cycles, dry_run=dry_run, model=model,
        )


def _run_full_review_attributed(asn_num, max_cycles=8, dry_run=False, model="opus"):
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return "failed"

    review_dir = CLAIM_CONVERGENCE_DIR / asn_label / "reviews"

    print(f"\n  [FULL-REVIEW] {asn_label}", file=sys.stderr)

    claim_dir = CLAIM_CONVERGENCE_DIR / asn_label
    if not claim_dir.exists():
        print(f"  No claim-convergence directory for {asn_label}", file=sys.stderr)
        return "failed"

    print(f"  Directory: {claim_dir.relative_to(WORKSPACE)}", file=sys.stderr)

    start_time = time.time()
    previous_findings = ""
    naturally_converged = False
    last_cycle_revise_count = -1
    final_review_path = None
    verdict = "CONVERGED"

    store = default_store()
    label_index = build_cross_asn_label_index(store=store)

    _ATTR_SUFFIXES = (".label.md", ".name.md", ".description.md")
    asn_claim_md_paths = [
        str(md_path.relative_to(WORKSPACE))
        for md_path in claim_dir.glob("*.md")
        if not md_path.name.startswith("_")
        and not md_path.name.endswith(_ATTR_SUFFIXES)
    ]

    for cycle in range(1, max_cycles + 1):
        print(f"\n  [CYCLE {cycle}/{max_cycles}]", file=sys.stderr)

        # Retry pass: re-feed any open revise comments to the reviser
        if not dry_run:
            _retry_unresolved_revises(store, asn_num, claim_dir, asn_claim_md_paths)

        gate_result = run_validate_gate(asn_label, scope_labels=None)
        if gate_result != "clean":
            print(f"  [GATE] halted — structural violations remain "
                  f"({gate_result}); aborting full-review",
                  file=sys.stderr)
            store.close()
            return "failed"

        # Assemble per-claim files for whole-ASN review
        asn_content = assemble_readonly(asn_label)

        # Run review
        verdict, findings_text, elapsed = run_review(
            asn_num, asn_content, asn_label, previous_findings, model=model)

        if verdict == "ERROR":
            print(f"\n  [FULL-REVIEW] FAILED on cycle {cycle} (review error).",
                  file=sys.stderr)
            break

        review_num = next_review_number(asn_label, kind="claim", reviews_dir=review_dir)
        review_stem = f"review-{review_num}"
        meta_path = review_meta_path(asn_label, review_num, kind="claim")

        findings = extract_findings(findings_text)
        emitted_findings = emit_findings(
            store, meta_path, findings,
            asn_label, review_stem, label_index,
            findings_dir=CLAIM_FINDINGS_DIR,
        )
        emitted_by_title = {e["title"]: e for e in emitted_findings}

        revise_count = len(filter_revise(findings))
        emit_meta(
            store, asn_label, review_num,
            title=f"Full Review — {asn_label} (cycle {cycle})",
            timestamp=time.strftime("%Y-%m-%d %H:%M"),
            scope=f"{asn_label} (full)",
            verdict=cycle_verdict(verdict, revise_count),
            findings_summary=findings_summary(findings, revise_count),
            emitted_findings=emitted_findings,
            elapsed_seconds=elapsed,
            findings_dir=CLAIM_FINDINGS_DIR,
        )
        final_review_path = meta_path

        for title, cls, _ in findings:
            print(f"\n  ### [{cls}] {title}", file=sys.stderr)

        # Accumulate findings for next cycle's "existing open issues"
        previous_findings = (previous_findings + "\n\n" + findings_text).strip()

        revise_findings = filter_revise(findings)
        last_cycle_revise_count = len(revise_findings)

        if dry_run or max_cycles == 1:
            if dry_run:
                print(f"\n  [DRY RUN] {len(revise_findings)} revise finding(s), no fixes.",
                      file=sys.stderr)
            else:
                print(f"\n  Single pass — {len(revise_findings)} revise finding(s), no fixes.",
                      file=sys.stderr)
            break

        # Revise each REVISE-class finding
        any_changed = False
        for title, _cls, finding_text in revise_findings:
            emitted = emitted_by_title.get(title)
            comment_id = emitted["comment_id"] if emitted else None
            claim_path = emitted["claim_path"] if emitted else None
            ok = revise(asn_num, title, finding_text, claim_dir=claim_dir,
                        comment_id=comment_id, claim_path=claim_path)
            if ok:
                any_changed = True
                if comment_id:
                    resolutions = store.find_links(
                        to_set=[comment_id], type_set=["resolution"],
                    )
                    if not resolutions:
                        print(
                            f"  [WARN] revise succeeded but no resolution "
                            f"link emitted for finding '{title}' "
                            f"(comment {comment_id})",
                            file=sys.stderr,
                        )

        if revise_findings or any_changed:
            step_commit_asn(asn_num,
                            f"full-review(asn): {asn_label} — cycle {cycle}")

        # Check for dependency cone (existing thrash detection)
        cone = detect_dependency_cone(asn_num)
        if cone:
            apex, deps = cone
            run_cone_review(asn_num, apex, deps, max_cycles=3,
                            dry_run=dry_run, model=model)

        # Natural convergence check: this cycle's reviewer filed no revises
        # AND predicate True. The cycle's review is the natural confirmation.
        if last_cycle_revise_count == 0 and is_asn_converged(store, asn_label):
            print(f"\n  [FULL-REVIEW] Natural convergence at cycle {cycle}.",
                  file=sys.stderr)
            naturally_converged = True
            break

        # No-progress short-circuit: revises filed but reviser couldn't fix any
        if revise_findings and not any_changed:
            print(f"  [FULL-REVIEW] Revises filed but no fixes applied this cycle. "
                  f"Breaking to confirmation.", file=sys.stderr)
            break

    failed = (verdict == "ERROR")

    # +1 confirmation cycle (only if not naturally converged, not failed, not dry-run/single-pass)
    confirmation_revise_count = 0
    if not failed and not dry_run and max_cycles > 1 and not naturally_converged:
        print(f"\n  [CONFIRMATION REVIEW]", file=sys.stderr)
        _retry_unresolved_revises(store, asn_num, claim_dir, asn_claim_md_paths)

        gate_result = run_validate_gate(asn_label, scope_labels=None)
        if gate_result != "clean":
            print(f"  [GATE] halted on confirmation — structural violations "
                  f"({gate_result})", file=sys.stderr)
            failed = True
        else:
            asn_content = assemble_readonly(asn_label)
            confirm_verdict, confirm_findings_text, confirm_elapsed = run_review(
                asn_num, asn_content, asn_label, previous_findings, model=model,
            )
            if confirm_verdict == "ERROR":
                failed = True
            else:
                review_num = next_review_number(asn_label, kind="claim", reviews_dir=review_dir)
                review_stem = f"review-{review_num}"
                confirm_meta_path = review_meta_path(asn_label, review_num, kind="claim")

                confirm_findings = extract_findings(confirm_findings_text)
                emitted_findings = emit_findings(
                    store, confirm_meta_path, confirm_findings,
                    asn_label, review_stem, label_index,
                    findings_dir=CLAIM_FINDINGS_DIR,
                )
                confirmation_revise_count = len(filter_revise(confirm_findings))
                emit_meta(
                    store, asn_label, review_num,
                    title=f"Full Review (Confirmation) — {asn_label}",
                    timestamp=time.strftime("%Y-%m-%d %H:%M"),
                    scope=f"{asn_label} (full)",
                    verdict=cycle_verdict(confirm_verdict, confirmation_revise_count),
                    findings_summary=findings_summary(
                        confirm_findings, confirmation_revise_count,
                    ),
                    emitted_findings=emitted_findings,
                    elapsed_seconds=confirm_elapsed,
                    findings_dir=CLAIM_FINDINGS_DIR,
                )
                final_review_path = confirm_meta_path

    elapsed = time.time() - start_time
    if failed:
        converged = False
    elif naturally_converged:
        converged = True
    elif dry_run or max_cycles == 1:
        converged = (last_cycle_revise_count == 0)
    else:
        converged = (
            confirmation_revise_count == 0
            and is_asn_converged(store, asn_label)
        )

    if final_review_path is not None and not failed:
        with open(final_review_path, "a") as rf:
            rf.write(f"\n## Result\n\n")
            if converged:
                rf.write(f"Converged.\n")
            else:
                rf.write(f"Not converged after {cycle} cycle(s).\n")
            rf.write(f"\n*Elapsed: {elapsed:.0f}s*\n")

        print(f"\n  Review: {final_review_path.relative_to(WORKSPACE)}",
              file=sys.stderr)

    print(f"  Elapsed: {elapsed:.0f}s", file=sys.stderr)

    if not dry_run:
        hint = (f"full-review(asn): {asn_label}"
                f"{'' if converged else ' — not converged'}")
        step_commit_asn(asn_num, hint)

    store.close()
    if failed:
        return "failed"
    return "converged" if converged else "not_converged"


def run_revise_from_review(asn_num, review_spec):
    """Read an existing review file and revise each finding.

    review_spec can be:
      - a number (e.g., "7" → review-7.md)
      - a filename (e.g., "review-7.md")
      - a full path
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return False

    claim_dir = CLAIM_CONVERGENCE_DIR / asn_label
    if not claim_dir.exists():
        print(f"  No claim-convergence directory for {asn_label}", file=sys.stderr)
        return False

    # Resolve review spec to path
    review_dir = claim_dir / "reviews"
    review_path = Path(review_spec)
    if not review_path.exists():
        # Try as number or filename
        if review_spec.isdigit():
            review_path = review_dir / f"review-{review_spec}.md"
        elif not review_spec.endswith(".md"):
            review_path = review_dir / f"{review_spec}.md"
        else:
            review_path = review_dir / review_spec

    if not review_path.exists():
        print(f"  Review file not found: {review_path}", file=sys.stderr)
        return False

    review_text = review_path.read_text()
    findings = extract_findings(review_text)

    if not findings:
        print(f"  No findings in {review_path}", file=sys.stderr)
        return False

    print(f"\n  [REVISE] {asn_label} — {len(findings)} findings from {review_path}",
          file=sys.stderr)

    any_changed = False
    for title, finding_text in findings:
        print(f"\n  ### {title}", file=sys.stderr)
        ok = revise(asn_num, title, finding_text, claim_dir=claim_dir)
        if ok:
            any_changed = True

    if any_changed:
        step_commit_asn(asn_num, hint="full-review revise")

    return any_changed


def main():
    parser = argparse.ArgumentParser(
        description="Full Review — deep structural analysis")
    parser.add_argument("asn", help="ASN number (e.g., 40)")
    parser.add_argument("--max-cycles", type=int, default=8,
                        help="Maximum convergence cycles (default: 8)")
    parser.add_argument("--model", default="opus",
                        help="Model for review (default: opus)")
    parser.add_argument("--review", metavar="PATH",
                        help="Revise findings from an existing review file")
    parser.add_argument("--cone", metavar="LABEL",
                        help="Force regional review on a specific cone apex")
    parser.add_argument("--dry-run", action="store_true",
                        help="Review only, don't fix")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))

    if args.review:
        ok = run_revise_from_review(asn_num, args.review)
        sys.exit(0 if ok else 1)

    if args.cone:
        # Force regional review — load deps from YAML, skip detection
        _, asn_label = find_asn(str(asn_num))
        claim_dir = CLAIM_CONVERGENCE_DIR / asn_label
        from lib.shared.common import load_claim_metadata, build_label_index
        asn_labels = set(build_label_index(claim_dir).keys())
        meta = load_claim_metadata(claim_dir, label=args.cone)
        if not meta:
            print(f"  Claim {args.cone} not found", file=sys.stderr)
            sys.exit(1)
        dep_labels = [d for d in meta.get("depends", []) if d in asn_labels]
        result = run_cone_review(asn_num, args.cone, dep_labels,
                                  max_cycles=args.max_cycles,
                                  dry_run=args.dry_run,
                                  model=args.model)
        sys.exit(0 if result == "converged" else 1)

    result = run_full_review(asn_num, max_cycles=args.max_cycles,
                               model=args.model,
                               dry_run=args.dry_run)
    sys.exit(0 if result == "converged" else 1)


if __name__ == "__main__":
    main()
