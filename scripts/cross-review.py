#!/usr/bin/env python3
"""
Cross-cutting Review — deep structural analysis with convergence.

Reads the whole ASN + foundation and finds issues that per-property
pipelines can't catch: carrier-set conflation, precondition chain gaps,
arguments that assume what they prove, missing cases that hold by
coincidence in examples.

Whole-ASN review, not per-property. Convergence: review → fix findings →
re-review → converge.

Usage:
    python scripts/cross-review.py 40
    python scripts/cross-review.py 40 --max-cycles 1     # single pass, no fixing
    python scripts/cross-review.py 40 --dry-run           # review only
"""

import argparse
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import WORKSPACE, FORMALIZATION_DIR, next_review_number, load_manifest
from lib.shared.common import find_asn, assemble_readonly, step_commit_asn
from lib.formalization.cross_review.review import run_review, extract_findings
from lib.formalization.cross_review.revise import revise


def run_cross_review(asn_num, max_cycles=10, dry_run=False):
    """Run the cross-cutting review pipeline.

    Returns "converged" or "not_converged".
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return "failed"

    manifest = load_manifest(asn_num)
    depends = manifest.get("depends", []) if manifest else []
    if not depends:
        print(f"  {asn_label} has no dependencies — nothing to review",
              file=sys.stderr)
        return "converged"

    review_dir = FORMALIZATION_DIR / asn_label / "reviews"

    print(f"\n  [CROSS-REVIEW] {asn_label}", file=sys.stderr)

    prop_dir = FORMALIZATION_DIR / asn_label
    if not prop_dir.exists():
        print(f"  No formalization directory for {asn_label}", file=sys.stderr)
        return "failed"

    print(f"  Directory: {prop_dir.relative_to(WORKSPACE)}", file=sys.stderr)

    start_time = time.time()
    converged = False
    previous_findings = ""
    had_findings = False

    for cycle in range(1, max_cycles + 1):
        print(f"\n  [CYCLE {cycle}/{max_cycles}]", file=sys.stderr)

        # Assemble per-property files for whole-ASN review
        asn_content = assemble_readonly(asn_label)

        # Run review
        findings_text, elapsed = run_review(
            asn_num, asn_content, asn_label, previous_findings)

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
            rf.write(f"# Cross-cutting Review — {asn_label} (cycle {cycle})\n\n")
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
            ok = revise(asn_num, title, finding_text, prop_dir=prop_dir)
            if ok:
                any_changed = True

        if not any_changed:
            print(f"  No changes made — stopping.", file=sys.stderr)
            break

        # Commit
        step_commit_asn(asn_num,
                        f"cross-review(asn): {asn_label} — cycle {cycle}")

        # Accumulate findings for next cycle's "existing open issues"
        previous_findings = (previous_findings + "\n\n" + findings_text).strip()

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
                        f"cross-review(asn): {asn_label} — not converged")

    return "converged" if converged else "not_converged"


def main():
    parser = argparse.ArgumentParser(
        description="Cross-cutting Review — deep structural analysis")
    parser.add_argument("asn", help="ASN number (e.g., 40)")
    parser.add_argument("--max-cycles", type=int, default=3,
                        help="Maximum convergence cycles (default: 3)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Review only, don't fix")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    result = run_cross_review(asn_num, max_cycles=args.max_cycles,
                               dry_run=args.dry_run)
    sys.exit(0 if result == "converged" else 1)


if __name__ == "__main__":
    main()
