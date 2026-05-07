#!/usr/bin/env python3
"""Citation Resolve — type each claim-label reference in a claim's prose
as either depends (backward) or forward.

For each claim, Sonnet identifies label references and types each.
The lifted ClaimCitationResolveAgent (producer) edits the claim md's
*Depends:* / *Forward References:* sections, emits substrate
citation.depends/forward + retraction links, and writes the
references sidecar via attest_attribute. Predicate-fired by the
runner on stale sidecars (references_is_fresh False).

Usage:
    python scripts/claim-citation-resolve.py 34
    python scripts/claim-citation-resolve.py 34 --claim NAT-carrier
    python scripts/claim-citation-resolve.py 34 --max-iterations 10
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.cli.runner_walk import run_trigger_cli
from lib.triggers import claim_citation_resolve


if __name__ == "__main__":
    sys.exit(run_trigger_cli(
        name="citation-resolve",
        triggers=[claim_citation_resolve],
        default_max_iterations=10,
        description=(
            "Drive the claim-citation-resolve producer over an ASN's "
            "claims to quiescence."
        ),
    ))
