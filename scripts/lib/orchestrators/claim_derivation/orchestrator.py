"""Claim derivation orchestrator — six-phase sequential pipeline.

Runs the full claim-derivation flow on an ASN:
    1. decompose      — mechanical ## split + per-section LLM analysis
    2. annotate       — 3 per-claim LLM passes (type, deps, signature)
    3. transclude     — project source-note regions as per-claim docs;
                        emit substrate links (claim, contract.<kind>,
                        citation, label, name, provenance.derivation)
    3.5. validate-transclude — quick byte-substring check; the
         content-preservation invariant is transition-checkable here
         only, before produce_contract intentionally diverges bodies
    4. produce-contract — synthesize Formal Contract sections
    5. validate-gate    — comprehensive validator + bounded structural-
                          only fix recipes; same gate claim convergence
                          runs before each review cycle

Each phase commits its output via the lib functions it dispatches to.
Halts on the first failed phase. Returns True iff the final state is
clean (Claim Document Contract holds).
"""

import sys
import time

from lib.claim_derivation.decompose import decompose_asn
from lib.claim_derivation.annotate import annotate_asn
from lib.claim_derivation.produce_contract import (
    find_claims_needing_quality, produce_contract,
)
from lib.claim_derivation.transclude import transclude_asn
from lib.claim_derivation.validate_transclude import (
    print_validation as validate_transclude,
)
from lib.shared.common import find_asn, step_commit_asn
from lib.shared.validate_gate import run_validate_gate


def _step_produce_contract(asn_num):
    """Phase 4 — synthesize Formal Contract for every claim that lacks
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
    """Phase 5 — bounded validate-revise gate.

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

    if not annotate_asn(asn_num):
        print("\n  [DERIVE] FAILED at annotate", file=sys.stderr)
        return False

    if not transclude_asn(asn_num):
        print("\n  [DERIVE] FAILED at transclude", file=sys.stderr)
        return False

    if not validate_transclude(asn_num):
        print(
            "\n  [DERIVE] FAILED at validate-transclude — transclude "
            "produced output that is not a byte-substring of the source "
            "note. Halting before produce_contract.",
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
