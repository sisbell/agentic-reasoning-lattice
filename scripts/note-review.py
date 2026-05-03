#!/usr/bin/env python3
"""
Discovery Review — produce a Dijkstra-style review of an ASN.

Runs a single review pass: analyze the ASN for rigor, produce structured
findings, commit the review file, and stop. Revision is handled separately
by revise.py / discover.py.

Usage:
    python scripts/note-review.py 9
"""

import argparse
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.note_convergence.steps import (
    find_asn, step_review, step_commit, has_revise_items,
)
from lib.shared.paths import WORKSPACE, NOTE_DIR
from lib.agent import attributed_to


@attributed_to("note-review")
def main():
    parser = argparse.ArgumentParser(
        description="Review an ASN — produce findings and stop")
    parser.add_argument("asn", help="ASN number (e.g., 9, 0009, ASN-0009)")
    args = parser.parse_args()

    # Find ASN
    asn_path, asn_label = find_asn(args.asn)
    if asn_path is None:
        print(f"  No ASN found for {args.asn} in {NOTE_DIR.relative_to(WORKSPACE)}/", file=sys.stderr)
        sys.exit(1)

    print(f"  [REVIEW] {asn_label} ({asn_path.name})", file=sys.stderr)
    asn_number = int(asn_label.replace("ASN-", ""))

    start = time.time()

    # Review
    review_path, converged = step_review(args.asn)
    if review_path is None:
        print(f"  [REVIEW] Review failed, retrying once...", file=sys.stderr)
        review_path, converged = step_review(args.asn)
        if review_path is None:
            print(f"  [REVIEW] Review failed again", file=sys.stderr)
            sys.exit(1)
    print(f"  [REVIEW] {review_path}", file=sys.stderr)

    # Converged — commit and exit 2
    if converged:
        print(f"  [REVIEW] CONVERGED — no significant issues",
              file=sys.stderr)
        step_commit(f"Review {asn_label} — converged", asn_id=asn_number)
        elapsed = time.time() - start
        print(f"\n  [REVIEW] Done ({elapsed:.0f}s)", file=sys.stderr)
        sys.exit(2)

    # Check for REVISE items
    if has_revise_items(review_path):
        step_commit(f"Review {asn_label}", asn_id=asn_number)
        elapsed = time.time() - start
        print(f"\n  [REVIEW] Done ({elapsed:.0f}s)", file=sys.stderr)
        print(f"  REVISE items found. Run: python scripts/note-revise.py {args.asn}",
              file=sys.stderr)
        sys.exit(0)

    # No REVISE items — commit and exit
    step_commit(f"Review {asn_label} — no revisions needed", asn_id=asn_number)
    elapsed = time.time() - start
    print(f"\n  [REVIEW] Done ({elapsed:.0f}s)", file=sys.stderr)


if __name__ == "__main__":
    main()
