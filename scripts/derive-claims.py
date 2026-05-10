#!/usr/bin/env python3
"""Claim derivation CLI — runs the full derivation pipeline on an ASN.

Three phases:
    1. decompose      — operator-gated producer (manual fire). Writes
                        claim mds + emits identity (claim, label, name,
                        derivation, transclusion.claim-statements).
    2. runner walk    — predicate-fired producers fire on stale state
                        post-decompose:
                          claim_contract            → contract.<kind>
                          claim_formal_contract     → Formal Contract
                          claim_describe            → description sidecar
                          claim_signature_resolve   → signature sidecar
                          claim_citation_resolve    → citations + references
    3. validate-gate  — runner-driven scout + refiner pair until
                        structurally clean or quiescent with violations.

Each phase commits its output. Halts on the first failed phase.
Returns 0 iff the final state is clean (Claim Document Contract holds).

Usage:
    python scripts/derive-claims.py 36
"""

import argparse
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.agents.producers.claim_decompose import ClaimDecomposeAgent
from lib.lattice.labels import format_label
from lib.protocols.febe.session import open_session
from lib.runner import Scope, run_until_quiescent
from lib.shared.common import find_asn
from lib.shared.paths import LATTICE
from lib.shared.validate_gate import run_validate_gate
from lib.triggers import (
    claim_citation_resolve, claim_contract, claim_describe,
    claim_formal_contract, claim_signature_resolve,
)


def _phase_decompose(asn_num: int) -> bool:
    """Phase 1 — operator-gated decompose fire."""
    asn_path, _ = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  {format_label(asn_num)} not found", file=sys.stderr)
        return False

    with open_session(LATTICE) as session:
        note_rel = str(asn_path.resolve().relative_to(LATTICE.resolve()))
        note_addr = session.get_addr_for_path(note_rel)
        if note_addr is None:
            note_addr = session.register_path(note_rel)
        result = ClaimDecomposeAgent()(session, note_addr)
        return result.success


def _phase_post_decompose(asn_num: int) -> bool:
    """Phase 2 — runner walk over post-decompose producers."""
    asn_label = format_label(asn_num)
    scope = Scope(asn_label=asn_label)

    result = run_until_quiescent(
        triggers=[
            claim_contract,
            claim_formal_contract,
            claim_describe,
            claim_signature_resolve,
            claim_citation_resolve,
        ],
        scope=scope,
        max_iterations=20,
    )
    print(
        f"\n  [POST-DECOMPOSE] iterations={result.iterations} "
        f"fires={len(result.fires)} errors={len(result.errors)} "
        f"quiescent={result.quiescent}",
        file=sys.stderr,
    )
    return result.quiescent and not result.errors


def _phase_validate_gate(asn_num: int) -> bool:
    """Phase 3 — runner-driven validate-revise gate."""
    _, asn_label = find_asn(str(asn_num))
    result = run_validate_gate(asn_label, scope_labels=None)
    if result == "clean":
        return True
    print(
        f"\n  [VALIDATE-GATE] result={result}; structural violations remain",
        file=sys.stderr,
    )
    return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run full claim derivation pipeline.",
    )
    parser.add_argument("asn", help="ASN number (e.g., 36)")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    start = time.time()

    if not _phase_decompose(asn_num):
        print("\n  [DERIVE] FAILED at decompose", file=sys.stderr)
        return 1

    if not _phase_post_decompose(asn_num):
        print(
            "\n  [DERIVE] FAILED at post-decompose runner walk",
            file=sys.stderr,
        )
        return 1

    ok = _phase_validate_gate(asn_num)
    elapsed = time.time() - start
    if ok:
        print(f"\n  [DERIVE] COMPLETE ({elapsed:.0f}s)", file=sys.stderr)
        return 0
    print(
        f"\n  [DERIVE] COMPLETE with validation violations "
        f"({elapsed:.0f}s) — Claim Document Contract does not hold; "
        f"derivation must be addressed before claim convergence.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
