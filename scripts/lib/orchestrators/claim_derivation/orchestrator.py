"""Claim derivation orchestrator — manual decompose, then runner-driven.

After the annotate/transclude phases were lifted into predicate-fired
producers, the derivation arc collapses to:

    1. decompose      — operator-gated producer (manual fire). Writes
                        claim mds + emits identity (claim, label, name,
                        derivation, transclusion.claim-statements).
    2. runner walk    — predicate-fired producers fire on stale state
                        post-decompose: claim_contract, claim_describe,
                        claim_signature_resolve, claim_citation_resolve.
                        Each emits its own substrate fact.
    3. produce-contract — synthesizes Formal Contract sections per claim
                        (still imperative; lift queued).
    4. validate-gate  — runner-driven scout + refiner pair
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
from lib.claim_derivation.produce_contract import (
    find_claims_needing_quality, produce_contract,
)
from lib.runner import Scope, run_until_quiescent
from lib.shared.common import find_asn
from lib.shared.git_ops import step_commit_asn
from lib.shared.validate_gate import run_validate_gate
from lib.triggers import (
    claim_citation_resolve, claim_contract, claim_describe,
    claim_signature_resolve,
)


def _step_post_decompose_producers(asn_num):
    """Phase 2 — runner walk over the post-decompose producers.

    After decompose grants per-claim identity, four predicate-fired
    producers fire on stale state and bring the substrate to
    quiescence on description / signature / citations / contract:
    """
    asn_label = f"ASN-{asn_num:04d}"
    scope = Scope(asn_label=asn_label)

    result = run_until_quiescent(
        triggers=[
            claim_contract,
            claim_signature_resolve,
            claim_citation_resolve,
            claim_describe,
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


def _step_produce_contract(asn_num):
    """Phase 3 — synthesize Formal Contract for every claim that lacks
    one (or whose prose has changed since last run).

    Calls produce_contract per claim. Logs failures but continues; the
    final validate gate catches any contract-related violations.
    """
    candidates, _hashes = find_claims_needing_quality(
        asn_num, force_all=True, force_rebuild=False,
    )
    if not candidates:
        print("  [PRODUCE-CONTRACT] No claims need contract synthesis",
              file=sys.stderr)
        return True

    n_ok = 0
    n_failed = 0
    any_changed = False
    for item in candidates:
        ok, file_changed, _response = produce_contract(
            asn_num, item["label"], item["section"],
            claim_path=item.get("path"), max_cycles=3,
        )
        if ok:
            n_ok += 1
        else:
            n_failed += 1
        if file_changed:
            any_changed = True

    if any_changed:
        step_commit_asn(asn_num, hint="produce-contract")

    print(f"\n  [PRODUCE-CONTRACT] {n_ok} ok, {n_failed} failed",
          file=sys.stderr)
    return n_failed == 0


def _step_validate_gate(asn_num):
    """Phase 4 — bounded validate-revise gate.

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

    if not _step_produce_contract(asn_num):
        print("\n  [DERIVE] FAILED at produce-contract", file=sys.stderr)
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
