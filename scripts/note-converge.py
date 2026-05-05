#!/usr/bin/env python3
"""Note Convergence — drive a note through review/revise cycles via the
trigger runner.

Walks the note-review and note-revise triggers until quiescent. Each
cycle: fire any trigger whose predicate is unsatisfied. Convergence is
when a full pass fires nothing (predicates are satisfied: no open
revises AND the most recent review filed zero new revises).

Usage:
    python scripts/note-converge.py 9                  # default 100 max passes
    python scripts/note-converge.py 9 --max-iterations 8
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.runner import asn, run_until_quiescent
from lib.triggers import note_review, note_revise


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Drive a note through review/revise cycles to convergence "
            "via the trigger runner."
        ),
    )
    parser.add_argument("asn", help="ASN number (e.g., 9, 0009, ASN-0009)")
    parser.add_argument(
        "--max-iterations", type=int, default=100,
        help="Safety cap on convergence passes (default 100)",
    )
    args = parser.parse_args()

    asn_num = int(re.sub(r"\D", "", args.asn))

    result = run_until_quiescent(
        triggers=[note_review, note_revise],
        scope=asn(asn_num),
        max_iterations=args.max_iterations,
    )

    print(
        f"\n  [NOTE-CONVERGE] iterations={result.iterations} "
        f"fires={len(result.fires)} errors={len(result.errors)} "
        f"quiescent={result.quiescent}",
        file=sys.stderr,
    )
    sys.exit(0 if result.quiescent and not result.errors else 1)


if __name__ == "__main__":
    main()
