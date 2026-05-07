#!/usr/bin/env python3
"""Signature Resolve — populate per-claim non-logical symbol signatures.

For each claim, Sonnet identifies which symbols the claim introduces
(distinct from symbols borrowed from upstream deps and notation
primitives). The lifted ClaimSignatureResolveAgent (producer) writes
the `<label>.signature.md` sidecar and emits the `signature` substrate
link via attest_attribute. Predicate-fired by the runner on stale
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

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.cli.runner_walk import run_trigger_cli
from lib.triggers import claim_signature_resolve


if __name__ == "__main__":
    sys.exit(run_trigger_cli(
        name="sig-resolve",
        triggers=[claim_signature_resolve],
        default_max_iterations=10,
        description=(
            "Drive the claim-signature-resolve producer over an ASN's "
            "claims to quiescence."
        ),
    ))
