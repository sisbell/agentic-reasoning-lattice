#!/usr/bin/env python3
"""
Signature Resolve — populate per-claim non-logical symbol signatures.

For each claim, Sonnet identifies which symbols the claim introduces
(distinct from symbols borrowed from upstream deps and notation
primitives). The lifted ClaimSignatureResolveAgent (producer) writes
the `<label>.signature.md` sidecar and emits the `signature` substrate
link via emit_attribute. Predicate-fired by the runner on stale
sidecars (signature_is_fresh False).

Without populated signatures, the existing `declared-symbols-resolve`
validator can't trace symbol uses to their owners — that's the gap
that let claims like OrdinalDisplacement and T1 use ℕ without citing
NAT-carrier across 600+ reviews.

Usage:
    python scripts/claim-signature-resolve.py 34
    python scripts/claim-signature-resolve.py 34 --claim NAT-carrier
    python scripts/claim-signature-resolve.py 34 --max-iterations 10
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.runner import Scope, run_until_quiescent
from lib.triggers import claim_signature_resolve


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Drive the claim-signature-resolve producer over an ASN's claims.",
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
        triggers=[claim_signature_resolve],
        scope=scope,
        max_iterations=args.max_iterations,
    )

    print(
        f"\n  [SIG-RESOLVE] iterations={result.iterations} "
        f"fires={len(result.fires)} errors={len(result.errors)} "
        f"quiescent={result.quiescent}",
        file=sys.stderr,
    )
    return 0 if result.quiescent and not result.errors else 1


if __name__ == "__main__":
    sys.exit(main())
