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
from lib.shared.paths import WORKSPACE, FORMALIZATION_DIR, next_review_number
from lib.shared.common import find_asn, assemble_readonly, step_commit_asn
from lib.formalization.full_review.review import run_review, extract_findings
from lib.formalization.full_review.revise import revise
from lib.formalization.gate import run_validate_gate
from lib.formalization.regional import detect_dependency_cone, run_regional_review


def run_full_review(asn_num, max_cycles=8, dry_run=False, model="opus"):
    """Run the full review pipeline.

    Returns "converged" or "not_converged".
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return "failed"

    review_dir = FORMALIZATION_DIR / asn_label / "reviews"

    print(f"\n  [FULL-REVIEW] {asn_label}", file=sys.stderr)

    claim_dir = FORMALIZATION_DIR / asn_label
    if not claim_dir.exists():
        print(f"  No formalization directory for {asn_label}", file=sys.stderr)
        return "failed"

    print(f"  Directory: {claim_dir.relative_to(WORKSPACE)}", file=sys.stderr)

    start_time = time.time()
    converged = False
    previous_findings = ""
    had_findings = False

    for cycle in range(1, max_cycles + 1):
        print(f"\n  [CYCLE {cycle}/{max_cycles}]", file=sys.stderr)

        gate_result = run_validate_gate(asn_label, scope_labels=None)
        if gate_result != "clean":
            print(f"  [GATE] halted — structural violations remain "
                  f"({gate_result}); aborting full-review",
                  file=sys.stderr)
            return "failed"

        # Assemble per-claim files for whole-ASN review
        asn_content = assemble_readonly(asn_label)

        # Run review
        findings_text, elapsed = run_review(
            asn_num, asn_content, asn_label, previous_findings, model=model)

        if findings_text is None:
            converged = True
            print(f"\n  Converged after {cycle} cycle{'s' if cycle > 1 else ''}.",
                  file=sys.stderr)
            if not had_findings:
                print(f"  Nothing to do.", file=sys.stderr)
            break

        had_findings = True

        # New review file per cycle
        review_dir.mkdir(parents=True, exist_ok=True)
        review_num = next_review_number(asn_label, reviews_dir=review_dir)
        review_path = review_dir / f"review-{review_num}.md"
        with open(review_path, "w") as rf:
            rf.write(f"# Full Review — {asn_label} (cycle {cycle})\n\n")
            rf.write(f"*{time.strftime('%Y-%m-%d %H:%M')}*\n\n")
            rf.write(findings_text + "\n")

        # Parse individual findings
        findings = extract_findings(findings_text)

        # Print findings
        for title, _ in findings:
            print(f"\n  ### {title}", file=sys.stderr)

        if dry_run or max_cycles == 1:
            if dry_run:
                print(f"\n  [DRY RUN] {len(findings)} findings, no fixes.",
                      file=sys.stderr)
            else:
                print(f"\n  Single pass — {len(findings)} findings, no fixes.",
                      file=sys.stderr)
            break

        # Revise each finding
        any_changed = False
        for title, finding_text in findings:
            ok = revise(asn_num, title, finding_text, claim_dir=claim_dir)
            if ok:
                any_changed = True

        if not any_changed:
            print(f"  No changes made — stopping.", file=sys.stderr)
            break

        # Commit
        step_commit_asn(asn_num,
                        f"full-review(asn): {asn_label} — cycle {cycle}")

        # Accumulate findings for next cycle's "existing open issues"
        previous_findings = (previous_findings + "\n\n" + findings_text).strip()

        # Check for dependency cone
        cone = detect_dependency_cone(asn_num)
        if cone:
            apex, deps = cone
            run_regional_review(asn_num, apex, deps, max_cycles=3,
                            dry_run=dry_run, model=model)

    # Append final result to last review file
    elapsed = time.time() - start_time
    if had_findings:
        with open(review_path, "a") as rf:
            rf.write(f"\n## Result\n\n")
            if converged:
                rf.write(f"Converged after {cycle} cycle{'s' if cycle > 1 else ''}.\n")
            else:
                rf.write(f"Not converged after {cycle} cycles.\n")
            rf.write(f"\n*Elapsed: {elapsed:.0f}s*\n")

        print(f"\n  Review: {review_path.relative_to(WORKSPACE)}",
              file=sys.stderr)

    print(f"  Elapsed: {elapsed:.0f}s", file=sys.stderr)

    if had_findings and not dry_run and not converged:
        step_commit_asn(asn_num,
                        f"full-review(asn): {asn_label} — not converged")

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

    claim_dir = FORMALIZATION_DIR / asn_label
    if not claim_dir.exists():
        print(f"  No formalization directory for {asn_label}", file=sys.stderr)
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
        claim_dir = FORMALIZATION_DIR / asn_label
        from lib.shared.common import load_claim_metadata, build_label_index
        asn_labels = set(build_label_index(claim_dir).keys())
        meta = load_claim_metadata(claim_dir, label=args.cone)
        if not meta:
            print(f"  Claim {args.cone} not found", file=sys.stderr)
            sys.exit(1)
        dep_labels = [d for d in meta.get("depends", []) if d in asn_labels]
        result = run_regional_review(asn_num, args.cone, dep_labels,
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
