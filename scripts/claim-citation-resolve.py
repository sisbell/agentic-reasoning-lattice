#!/usr/bin/env python3
"""
Citation Resolve — type each claim-label reference in a claim's prose
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

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.runner import Scope, run_until_quiescent
from lib.triggers import claim_citation_resolve


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Drive the claim-citation-resolve producer over an ASN's claims.",
    )
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument(
        "--claim", metavar="LABEL",
        help="Restrict to one claim label",
    )
    parser.add_argument(
        "--max-iterations", type=int, default=10,
        help="Max runner passes (default: 10)",
    )
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    asn_label = f"ASN-{asn_num:04d}"
    labels = (
        frozenset({args.claim}) if args.claim else None
    )
    scope = Scope(asn_label=asn_label, labels=labels)

    result = run_until_quiescent(
        triggers=[claim_citation_resolve],
        scope=scope,
        max_iterations=args.max_iterations,
    )

    print(
        f"\n  [CITATION-RESOLVE] iterations={result.iterations} "
        f"fires={len(result.fires)} errors={len(result.errors)} "
        f"quiescent={result.quiescent}",
        file=sys.stderr,
    )
    return 0 if result.quiescent and not result.errors else 1


if __name__ == "__main__":
    sys.exit(main())
