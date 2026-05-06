"""Claim derivation orchestrator — manual decompose, then runner-driven.

After the annotate / transclude / produce-contract phases were lifted
into predicate-fired producers, the derivation arc collapses to:

    1. decompose      — operator-gated producer (manual fire). Writes
                        claim mds + emits identity (claim, label, name,
                        derivation, transclusion.claim-statements).
    2. runner walk    — predicate-fired producers fire on stale state
                        post-decompose:
                          claim_contract            → contract.<kind>
                          claim_formal_contract     → Formal Contract section
                          claim_describe            → description sidecar
                          claim_signature_resolve   → signature sidecar
                          claim_citation_resolve    → citations + references
                        The trigger order above is also the natural
                        causal order: claim_formal_contract waits on
                        claim_contract via predicate; sidecar
                        producers re-attest after produce-contract
                        advances the claim chain.
    3. validate-gate  — runner-driven scout + refiner pair
                        (claim_structural_audit + claim_structural_revise);
                        runs until structurally clean or quiescent with
                        violations.

Each phase commits its output. Halts on the first failed phase.
Returns True iff the final state is clean (Claim Document Contract
holds).
"""

import sys
import time

from lib.claim_derivation.decompose import decompose_asn
from lib.runner import Scope, run_until_quiescent
from lib.shared.common import find_asn
from lib.shared.validate_gate import run_validate_gate
from lib.triggers import (
    claim_citation_resolve, claim_contract, claim_describe,
    claim_formal_contract, claim_signature_resolve,
)


def _step_post_decompose_producers(asn_num):
    """Phase 2 — runner walk over the post-decompose producers."""
    asn_label = f"ASN-{asn_num:04d}"
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


def _step_validate_gate(asn_num):
    """Phase 3 — bounded validate-revise gate.

    Runs the comprehensive validator. If actionable findings surface,
    dispatches structural-only fix recipes (validate-revise) and
    re-validates. Continues until clean or max iterations exhausted.
    Returns True iff the final state is clean.
    """
    _, asn_label = find_asn(str(asn_num))
    result = run_validate_gate(asn_label, scope_labels=None)
    if result == "clean":
        return True
    print(
        f"\n  [VALIDATE-GATE] result={result}; structural violations remain",
        file=sys.stderr,
    )
    return False


def run_pipeline(asn_num):
    """Run the full claim derivation pipeline. Returns True on clean exit."""
    start = time.time()

    if not decompose_asn(asn_num):
        print("\n  [DERIVE] FAILED at decompose", file=sys.stderr)
        return False

    if not _step_post_decompose_producers(asn_num):
        print(
            "\n  [DERIVE] FAILED at post-decompose runner walk",
            file=sys.stderr,
        )
        return False

    ok = _step_validate_gate(asn_num)
    elapsed = time.time() - start
    if ok:
        print(f"\n  [DERIVE] COMPLETE ({elapsed:.0f}s)", file=sys.stderr)
    else:
        print(
            f"\n  [DERIVE] COMPLETE with validation violations "
            f"({elapsed:.0f}s) — Claim Document Contract does not hold; "
            f"derivation must be addressed before claim convergence.",
            file=sys.stderr,
        )
    return ok
