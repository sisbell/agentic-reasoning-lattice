#!/usr/bin/env python3
"""
Note Convergence — drive a note through review/revise cycles.

Implements §6.2 of docs/protocols/note-convergence-protocol.md. Each
cycle: RetryOpenRevises → Review → EmitFindings → Revise → check
predicate. If a cycle files zero revises AND the substrate predicate
holds, we converged naturally. Otherwise, after max-cycles, run a +1
confirmation review.

Usage:
    python scripts/note-converge.py 9                  # default 15 cycles, opus
    python scripts/note-converge.py 9 --max-cycles 8
    python scripts/note-converge.py 9 --dry-run        # one review, no revise
    python scripts/note-converge.py 9 --model sonnet
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.orchestrators.note_converge import run_note_convergence
from lib.provenance import attributed_to


@attributed_to("note-review")
def main():
    parser = argparse.ArgumentParser(
        description="Drive a note through review/revise cycles to convergence.",
    )
    parser.add_argument("asn", help="ASN number (e.g., 9, 0009, ASN-0009)")
    parser.add_argument("--max-cycles", type=int, default=15,
                        help="Maximum cycles before giving up (default 15)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Run one review, skip revise; exit converged "
                             "iff zero revises were filed.")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"],
                        help="Model (default: opus)")
    parser.add_argument("--effort", default="max",
                        help="Thinking effort level (low/medium/high/max)")
    args = parser.parse_args()

    outcome = run_note_convergence(
        args.asn, max_cycles=args.max_cycles,
        dry_run=args.dry_run, model=args.model, effort=args.effort,
    )

    # Exit codes mirror cone-sweep / full-review:
    #   0  — converged
    #   1  — not converged or failed
    #   2  — converged + signal (kept for symmetry with note-revise.py
    #         which uses 2 to indicate convergence; here we just use 0)
    if outcome == "converged":
        sys.exit(0)
    sys.exit(1)


if __name__ == "__main__":
    main()
