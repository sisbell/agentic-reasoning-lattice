#!/usr/bin/env python3
"""Full Review — deep structural analysis with convergence.

Default mode walks [full_review, claim_findings, claim_revise] over
the whole ASN to quiescence. Findings include cross-claim issues that
per-claim pipelines can't catch: carrier-set conflation, precondition
chain gaps, arguments that assume what they prove, missing cases that
hold by coincidence in examples.

`--cone LABEL` instead force-passes [cone_review, claim_findings,
claim_revise] restricted to a single apex. Same shape as
claim-cone-sweep.py --force LABEL.

The trigger-driven runner walks the same triggers automatically when
predicates fire; this script is the manual operator entry.

Usage:
    python scripts/claim-full-review.py 40
    python scripts/claim-full-review.py 40 --max-iterations 4
    python scripts/claim-full-review.py 36 --cone S8
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.runner import Scope, asn, run_force_pass, run_until_quiescent
from lib.triggers import (
    claim_findings, claim_revise, cone_review, full_review,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Full review — deep structural analysis with convergence.",
    )
    parser.add_argument("asn", help="ASN number (e.g., 40)")
    parser.add_argument(
        "--cone", metavar="LABEL",
        help="Force-pass on a specific cone apex instead of full review",
    )
    parser.add_argument(
        "--max-iterations", type=int, default=8,
        help="Max runner passes for the default mode (default: 8)",
    )
    args = parser.parse_args()

    asn_num = int(re.sub(r"\D", "", args.asn))
    asn_label = f"ASN-{asn_num:04d}"

    if args.cone:
        scope = Scope(asn_label=asn_label, labels=frozenset({args.cone}))
        result = run_force_pass(
            triggers=[cone_review, claim_findings, claim_revise],
            scope=scope,
        )
        print(
            f"\n  [FULL-REVIEW] cone={args.cone} fires={len(result.fires)} "
            f"errors={len(result.errors)}",
            file=sys.stderr,
        )
        return 0 if not result.errors else 1

    result = run_until_quiescent(
        triggers=[full_review, claim_findings, claim_revise],
        scope=asn(asn_num),
        max_iterations=args.max_iterations,
    )
    print(
        f"\n  [FULL-REVIEW] iterations={result.iterations} "
        f"fires={len(result.fires)} errors={len(result.errors)} "
        f"quiescent={result.quiescent}",
        file=sys.stderr,
    )
    return 0 if result.quiescent and not result.errors else 1


if __name__ == "__main__":
    sys.exit(main())
