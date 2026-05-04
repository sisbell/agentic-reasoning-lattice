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
    python scripts/claim-full-review.py 40
    python scripts/claim-full-review.py 40 --max-cycles 1
    python scripts/claim-full-review.py 40 --dry-run
    python scripts/claim-full-review.py 36 --cone S8
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.orchestrators.claim_full_review import (
    run_full_review, run_revise_from_review,
)
from lib.orchestrators.cone_review import run_cone_review
from lib.shared.common import find_asn
from lib.shared.paths import CLAIM_DIR


def main():
    parser = argparse.ArgumentParser(
        description="Full Review — deep structural analysis",
    )
    parser.add_argument("asn", help="ASN number (e.g., 40)")
    parser.add_argument(
        "--max-cycles", type=int, default=8,
        help="Maximum convergence cycles (default: 8)",
    )
    parser.add_argument(
        "--model", default="opus",
        help="Model for review (default: opus)",
    )
    parser.add_argument(
        "--review", metavar="PATH",
        help="Revise findings from an existing review file",
    )
    parser.add_argument(
        "--cone", metavar="LABEL",
        help="Force regional review on a specific cone apex",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Review only, don't fix",
    )
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))

    if args.review:
        ok = run_revise_from_review(asn_num, args.review)
        sys.exit(0 if ok else 1)

    if args.cone:
        _, asn_label = find_asn(str(asn_num))
        claim_dir = CLAIM_DIR / asn_label
        from lib.shared.claim_files import build_label_index, load_claim_metadata
        asn_labels = set(build_label_index(claim_dir).keys())
        meta = load_claim_metadata(claim_dir, label=args.cone)
        if not meta:
            print(f"  Claim {args.cone} not found", file=sys.stderr)
            sys.exit(1)
        dep_labels = [d for d in meta.get("depends", []) if d in asn_labels]
        result = run_cone_review(
            asn_num, args.cone, dep_labels,
            max_cycles=args.max_cycles,
            dry_run=args.dry_run, model=args.model,
        )
        sys.exit(0 if result == "converged" else 1)

    result = run_full_review(
        asn_num, max_cycles=args.max_cycles,
        model=args.model, dry_run=args.dry_run,
    )
    sys.exit(0 if result == "converged" else 1)


if __name__ == "__main__":
    main()
