#!/usr/bin/env python3
"""Full Review — drive whole-ASN deep structural analysis to quiescence.

Walks [full_review, claim_findings, claim_revise] over the whole ASN.
Findings include cross-claim issues that per-claim pipelines can't
catch: carrier-set conflation, precondition chain gaps, arguments
that assume what they prove, missing cases that hold by coincidence
in examples.

The trigger-driven runner walks the same triggers automatically when
predicates fire; this script is the manual operator entry.

For single-apex cone work, see `claim-cone-sweep.py --force LABEL`
(same triggers, scoped to one apex).

Usage:
    python scripts/claim-full-review.py 40
    python scripts/claim-full-review.py 40 --max-iterations 4
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.cli.runner_walk import run_trigger_cli
from lib.triggers import (
    claim_describe_refresh,
    claim_findings,
    claim_revise,
    claim_signature_refresh,
    claims_statements_refresh,
    full_review,
)


if __name__ == "__main__":
    sys.exit(run_trigger_cli(
        name="full-review",
        triggers=[
            full_review, claim_findings, claim_revise,
            claim_describe_refresh, claim_signature_refresh,
            claims_statements_refresh,
        ],
        default_max_iterations=8,
        support_claim_filter=False,
        description=(
            "Drive full-review convergence to quiescence, then refresh "
            "stale descriptions and advance the claims.statements assembly."
        ),
    ))
