#!/usr/bin/env python3
"""
Revise pipeline — consult → revise → commit, optionally repeated.

Takes an existing review (from review.py or Dafny review) and runs the
revision loop: consult on REVISE findings, revise the ASN, commit.
Multiple cycles re-review between revisions.

Usage:
    python scripts/revise.py 9              # 1 cycle: consult → revise → commit (latest review)
    python scripts/revise.py 9 --cycle 3    # 3 cycles (first uses latest review, rest do review → revise)
    python scripts/revise.py 9 --converge   # loop until CONVERGED (max 15)
    python scripts/revise.py 9 --converge 8 # loop until CONVERGED (max 8)
    python scripts/revise.py 9 --resume revise  # skip consult, go straight to revise
"""

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from paths import sorted_reviews

from lib.review_pipeline import (
    find_asn,
    step_review,
    step_consult_revision,
    step_revise,
    step_commit,
    has_revise_items,
)

MECHANICAL_REVIEW_MARKERS = [
    "Based on Dafny verification",
    "Based on Alloy",
]


def is_mechanical_review(review_path):
    """Detect reviews from mechanical sources (Dafny, Alloy).

    These reviews are grounded in counterexamples or proof divergences —
    no expert consultation needed.
    """
    try:
        # Markers appear on line 2-3 of the review; check the first 5 lines
        with open(review_path) as f:
            for _, line in zip(range(5), f):
                if any(marker in line for marker in MECHANICAL_REVIEW_MARKERS):
                    return True
        return False
    except (FileNotFoundError, OSError):
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Revise pipeline — consult and revise from existing review")
    parser.add_argument("asn", help="ASN number (e.g., 9, 0009, ASN-0009)")
    parser.add_argument("--cycle", "-n", type=int, default=1,
                        help="Number of revise cycles (default: 1)")
    parser.add_argument("--converge", nargs="?", type=int, const=15,
                        metavar="MAX",
                        help="Loop until CONVERGED verdict (default max: 15)")
    parser.add_argument("--resume", choices=["revise"],
                        help="Resume from revise (skip consult)")
    args = parser.parse_args()

    # --converge overrides --cycle
    max_cycles = args.converge if args.converge is not None else args.cycle

    # Find ASN
    asn_path, asn_label = find_asn(args.asn)
    if asn_path is None:
        print(f"  No ASN found for {args.asn} in vault/1-reasoning-docs/", file=sys.stderr)
        sys.exit(1)

    asn_number = int(asn_label.replace("ASN-", ""))
    print(f"  [REVISE] {asn_label} ({asn_path.name})", file=sys.stderr)
    if args.converge is not None:
        print(f"  [REVISE] converge mode (max {max_cycles} cycles)",
              file=sys.stderr)
    else:
        print(f"  [REVISE] {max_cycles} cycle(s): consult → revise → commit",
              file=sys.stderr)

    start = time.time()

    for cycle in range(1, max_cycles + 1):
        if max_cycles > 1:
            print(f"\n  ──── Cycle {cycle}/{max_cycles} ────",
                  file=sys.stderr)

        review_path = None
        converged = False

        if cycle == 1:
            # Cycle 1: use latest existing review
            reviews = sorted_reviews(asn_label)
            if not reviews:
                print(f"  [REVISE] No reviews found for {asn_label}",
                      file=sys.stderr)
                print(f"  Run: python scripts/review.py {args.asn}",
                      file=sys.stderr)
                sys.exit(1)
            review_path = str(reviews[-1])
            print(f"  [REVISE] Using review: {Path(review_path).name}",
                  file=sys.stderr)

            if not has_revise_items(review_path):
                print(f"  [REVISE] No REVISE items in latest review — nothing to do",
                      file=sys.stderr)
                sys.exit(0)
        else:
            # Cycles 2+: run review first
            review_path, converged = step_review(args.asn)
            if review_path is None:
                print(f"  [REVISE] Review failed, retrying once...",
                      file=sys.stderr)
                review_path, converged = step_review(args.asn)
                if review_path is None:
                    print(f"  [REVISE] Review failed again, stopping",
                          file=sys.stderr)
                    sys.exit(1)
            print(f"  [REVIEW] {review_path}", file=sys.stderr)

            if converged:
                print(f"  [REVISE] CONVERGED — review found no significant issues",
                      file=sys.stderr)
                step_commit(f"Review {asn_label} — converged", asn_id=asn_number)
                asn_num = asn_label.replace("ASN-", "").lstrip("0") or "0"
                print(f"\n  [NEXT] Export statements: python scripts/export.py {asn_num}",
                      file=sys.stderr)
                break

            if not has_revise_items(review_path):
                print(f"  [REVISE] No REVISE items — ASN is clean",
                      file=sys.stderr)
                step_commit(f"Review {asn_label} — no revisions needed", asn_id=asn_number)
                break

        # Consult (skip for mechanical reviews — findings are grounded in proofs/counterexamples)
        consultation_path = None
        skip_consult = (args.resume == "revise") or is_mechanical_review(review_path)
        if skip_consult and is_mechanical_review(review_path):
            print(f"  [REVISE] Mechanical review — skipping consultation",
                  file=sys.stderr)
        if not skip_consult:
            consultation_path = step_consult_revision(args.asn, review_path)
            if consultation_path is None:
                print(f"  [REVISE] Consultation failed, stopping",
                      file=sys.stderr)
                sys.exit(1)
            args.resume = None  # clear resume after first cycle

        # Revise
        asn_result, revise_converged = step_revise(
            args.asn, consultation_path=consultation_path)
        if asn_result is None:
            print(f"  [REVISE] Revise failed, stopping", file=sys.stderr)
            sys.exit(1)
        args.resume = None  # clear resume after first cycle

        if revise_converged:
            print(f"  [REVISE] Revise made no changes — converged",
                  file=sys.stderr)
            step_commit(f"Revise {asn_label} — converged (cycle {cycle})", asn_id=asn_number)
            break

        # Commit
        step_commit(f"Revise {asn_label} (cycle {cycle})", asn_id=asn_number)

    else:
        # Loop exhausted without convergence
        if args.converge is not None:
            print(f"\n  [REVISE] Max cycles ({max_cycles}) reached without convergence",
                  file=sys.stderr)
            elapsed = time.time() - start
            print(f"\n  [REVISE] Done ({elapsed:.0f}s)", file=sys.stderr)
            sys.exit(1)

    elapsed = time.time() - start
    print(f"\n  [REVISE] Done ({elapsed:.0f}s)", file=sys.stderr)


if __name__ == "__main__":
    main()
