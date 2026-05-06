#!/usr/bin/env python3
"""Drive an inquiry through consult → draft via the trigger runner.

Walks the inquiry-consult and note-draft triggers until quiescent.
Each cycle: fire any trigger whose predicate is unsatisfied. Exits
when consult is done AND a note has been drafted (or when the
runner cap is hit).

Usage:
    python scripts/note-draft.py 4              # one inquiry by ASN num
    python scripts/note-draft.py --inquiries 1,2,3   # batch
    python scripts/note-draft.py --max-iterations 8
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.runner import asn, run_until_quiescent
from lib.triggers import inquiry_consult, note_draft


def _parse_asn_nums(args):
    if args.asn:
        return [int(re.sub(r"\D", "", args.asn))]
    if args.inquiries:
        return [
            int(re.sub(r"\D", "", x))
            for x in args.inquiries.split(",")
            if x.strip()
        ]
    return []


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Drive an inquiry through consult → draft via the trigger "
            "runner."
        ),
    )
    parser.add_argument(
        "asn", nargs="?",
        help="ASN number (e.g., 4, 0004, ASN-0004)",
    )
    parser.add_argument(
        "--inquiries",
        help="Comma-separated ASN numbers for batch processing",
    )
    parser.add_argument(
        "--max-iterations", type=int, default=100,
        help="Safety cap on refinement passes per inquiry (default 100)",
    )
    args = parser.parse_args()

    asn_nums = _parse_asn_nums(args)
    if not asn_nums:
        parser.error("Provide an ASN number or --inquiries")

    triggers = [inquiry_consult, note_draft]
    overall_quiescent = True
    overall_errors: list = []
    for asn_num in asn_nums:
        print(f"\n=== ASN-{asn_num:04d} ===", file=sys.stderr)
        result = run_until_quiescent(
            triggers=triggers,
            scope=asn(asn_num),
            max_iterations=args.max_iterations,
        )
        print(
            f"  iterations={result.iterations} fires={len(result.fires)} "
            f"errors={len(result.errors)} quiescent={result.quiescent}",
            file=sys.stderr,
        )
        overall_quiescent = overall_quiescent and result.quiescent
        overall_errors.extend(result.errors)

    sys.exit(0 if overall_quiescent and not overall_errors else 1)


if __name__ == "__main__":
    main()
