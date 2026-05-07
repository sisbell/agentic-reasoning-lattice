"""Runner-walk CLI helper — collapses a recurring CLI shape into one call.

Several top-level scripts wrap `run_until_quiescent` over a curated
list of triggers, scoped to a single ASN, with an optional per-claim
filter. The shape is uniform: argparse for `asn` + `--max-iterations`
(+ sometimes `--claim`), build a Scope, fire the runner, print a
status line, exit on quiescence.

This helper packages that shape. Each consuming CLI shrinks to a
config block:

    if __name__ == "__main__":
        sys.exit(run_trigger_cli(
            name="note-refine",
            triggers=[note_review, note_consult, note_revise],
            support_claim_filter=False,
        ))

Anything beyond the standard shape (extra modes like
claim-cone-sweep's `--force` and `--apexes`) calls `run_until_quiescent`
directly — this helper covers the simple case, not every case.
"""

from __future__ import annotations

import argparse
import re
import sys
from typing import List, Optional

from lib.runner import Scope, Trigger, run_until_quiescent


def run_trigger_cli(
    *,
    name: str,
    triggers: List[Trigger],
    default_max_iterations: int = 100,
    support_claim_filter: bool = True,
    description: Optional[str] = None,
) -> int:
    """Run the standard runner-walk CLI shape.

    Parses argv, builds the scope, dispatches `run_until_quiescent`,
    prints a one-line status to stderr, and returns the exit code.

    Args:
      name: Short label printed in the status line and used as the CLI
        program name (e.g. "note-refine"). Will be uppercased in
        the [TAG] output.
      triggers: Trigger objects to walk.
      default_max_iterations: Default value for `--max-iterations`.
        Per-claim refinement walks tend to use 10; whole-note review
        loops tend to use 100.
      support_claim_filter: When True, adds a `--claim LABEL` flag that
        restricts the scope to a single claim. Use for claim-level
        walks; off for note-level walks.
      description: argparse description; defaults to a stock message
        naming the trigger list.

    Returns:
      0 on quiescent + no errors, 1 otherwise.
    """
    if description is None:
        trigger_names = ", ".join(t.name for t in triggers)
        description = f"Drive [{trigger_names}] over an ASN to quiescence."

    parser = argparse.ArgumentParser(prog=name, description=description)
    parser.add_argument("asn", help="ASN number (e.g., 34, 0034, ASN-0034)")
    if support_claim_filter:
        parser.add_argument(
            "--claim", metavar="LABEL",
            help="Restrict to one claim label",
        )
    parser.add_argument(
        "--max-iterations", type=int, default=default_max_iterations,
        help=f"Max runner passes (default: {default_max_iterations})",
    )
    args = parser.parse_args()

    asn_num = int(re.sub(r"\D", "", args.asn))
    asn_label = f"ASN-{asn_num:04d}"
    labels = (
        frozenset({args.claim})
        if support_claim_filter and getattr(args, "claim", None)
        else None
    )
    scope = Scope(asn_label=asn_label, labels=labels)

    result = run_until_quiescent(
        triggers=triggers,
        scope=scope,
        max_iterations=args.max_iterations,
    )

    print(
        f"\n  [{name.upper()}] iterations={result.iterations} "
        f"fires={len(result.fires)} errors={len(result.errors)} "
        f"quiescent={result.quiescent}",
        file=sys.stderr,
    )
    return 0 if result.quiescent and not result.errors else 1
