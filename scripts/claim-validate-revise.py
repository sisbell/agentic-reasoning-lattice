"""claim-validate-revise — drive structural-fix refinement to quiescence.

Walks the claim_structural_audit (scout) and claim_structural_revise
(refiner) triggers until quiescent. Each refiner fire walks the
apply-mode passes per claim: body-uniqueness, declaration-label-mismatch,
declared-symbols-resolve, depends-agreement, references-resolve.
Acyclic-depends propose mode was retired in the lift; cycle findings
still surface in validator output but are not actioned.

Usage:
    python scripts/claim-validate-revise.py 34
    python scripts/claim-validate-revise.py 34 --claim T7
    python scripts/claim-validate-revise.py 34 --max-iterations 5
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.cli.runner_walk import run_trigger_cli
from lib.triggers import claim_structural_audit, claim_structural_revise


if __name__ == "__main__":
    sys.exit(run_trigger_cli(
        name="validate-revise",
        triggers=[claim_structural_audit, claim_structural_revise],
        default_max_iterations=10,
        description=(
            "Drive the claim-structural-audit + claim-structural-revise "
            "refiner over an ASN's claims to quiescence."
        ),
    ))
