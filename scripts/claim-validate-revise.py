"""claim-validate-revise — apply mechanical fixes driven by validator findings.

Paired with claim-validate.py: that script finds structural-invariant
violations; this one drives the lifted ClaimStructuralReviseAgent (refiner)
via the runner. Each agent fire walks the apply-mode passes per claim:
body-uniqueness, declaration-label-mismatch, declared-symbols-resolve,
depends-agreement, references-resolve. Acyclic-depends propose mode
was retired in the lift; cycle findings still surface in validator
output but are not actioned.

Usage:
    python scripts/claim-validate-revise.py 34
    python scripts/claim-validate-revise.py 34 --max-iterations 5
    python scripts/claim-validate-revise.py 34 --claim T7

The fine-grained orchestrator flags (--rule, --file, --from-pass,
--to-pass, --dry-run vs --apply) retired with the orchestrator.
Apply is the only mode now; if dry-run / per-rule / per-file
inspection is needed, run the validator directly:

    python scripts/claim-validate.py 34
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.runner import Scope, run_until_quiescent
from lib.triggers import claim_structural_audit, claim_structural_revise


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Drive the claim-structural-revise refiner over an ASN's claims."
        ),
    )
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument(
        "--claim", metavar="LABEL",
        help="restrict to one claim label",
    )
    parser.add_argument(
        "--max-iterations", type=int, default=10,
        help="max runner passes (default: 10)",
    )
    args = parser.parse_args()

    asn_num = int(re.sub(r"\D", "", args.asn))
    asn_label = f"ASN-{asn_num:04d}"
    labels = (
        frozenset({args.claim}) if args.claim else None
    )
    scope = Scope(asn_label=asn_label, labels=labels)

    result = run_until_quiescent(
        triggers=[claim_structural_audit, claim_structural_revise],
        scope=scope,
        max_iterations=args.max_iterations,
    )

    print(
        f"\n  [VALIDATE-REVISE] iterations={result.iterations} "
        f"fires={len(result.fires)} errors={len(result.errors)} "
        f"quiescent={result.quiescent}",
        file=sys.stderr,
    )
    return 0 if result.quiescent and not result.errors else 1


if __name__ == "__main__":
    sys.exit(main())
