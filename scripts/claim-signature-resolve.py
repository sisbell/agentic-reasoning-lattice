#!/usr/bin/env python3
"""
Signature Resolve — populate per-claim non-logical symbol signatures.

For each claim, Sonnet identifies which symbols the claim introduces
(distinct from symbols borrowed from upstream deps and notation
primitives). The orchestrator writes the `<label>.signature.md` sidecar
and emits the `signature` substrate link.

Without populated signatures, the existing `declared-symbols-resolve`
validator can't trace symbol uses to their owners — that's the gap
that let claims like OrdinalDisplacement and T1 use ℕ without citing
NAT-carrier across 600+ reviews.

Usage:
    python scripts/claim-signature-resolve.py 34
    python scripts/claim-signature-resolve.py 34 --claim NAT-carrier
    python scripts/claim-signature-resolve.py 34 --model sonnet
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.claim_convergence.signature_resolve import run_resolve, run_sweep


def main():
    parser = argparse.ArgumentParser(
        description="Signature Resolve — populate per-claim non-logical symbol signatures.",
    )
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument(
        "--claim", metavar="LABEL",
        help="Resolve a single claim instead of the full sweep",
    )
    parser.add_argument(
        "--model", default="sonnet",
        help="Model for the resolve call (default: sonnet)",
    )
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))

    if args.claim:
        result = run_resolve(asn_num, args.claim, model=args.model)
    else:
        result = run_sweep(asn_num, model=args.model)

    sys.exit(0 if result == "ok" else 1)


if __name__ == "__main__":
    main()
