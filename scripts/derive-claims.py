#!/usr/bin/env python3
"""
Claim derivation — full pipeline:
    decompose → enrich → transclude → produce-contract → validate-gate.

Runs the complete claim-derivation pipeline on an ASN. Each stage commits
its output automatically. The final phase is the validate-revise gate
(same gate claim convergence runs before each review cycle): a bounded
loop that runs the comprehensive validator and dispatches structural-
only fix recipes until the Claim File Contract holds — or max iterations
exhausted, in which case derivation fails with the unresolved findings
left in place for diagnosis.

Usage:
    python scripts/derive-claims.py 36
"""

import argparse
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.claim_derivation.decompose import decompose_asn
from lib.claim_derivation.enrich import enrich_asn
from lib.claim_derivation.produce_contract import (
    find_claims_needing_quality, produce_contract,
)
from lib.claim_derivation.transclude import transclude_asn
from lib.shared.common import find_asn, step_commit_asn
from lib.shared.validate_gate import run_validate_gate


def _step_produce_contract(asn_num):
    """Phase 4 — synthesize Formal Contract for every claim that lacks one
    (or whose prose has changed since last run).

    Calls produce_contract per claim. Logs failures but continues; the
    final validate gate catches any contract-related violations."""
    candidates, _hashes = find_claims_needing_quality(
        asn_num, force_all=True, force_rebuild=False,
    )
    if not candidates:
        print(f"  [PRODUCE-CONTRACT] No claims need contract synthesis",
              file=sys.stderr)
        return True

    _, asn_label = find_asn(str(asn_num))
    n_ok = 0
    n_failed = 0
    any_changed = False
    for item in candidates:
        label = item["label"]
        section = item["section"]
        claim_path = item.get("path")
        ok, file_changed, _response = produce_contract(
            asn_num, label, section, claim_path=claim_path, max_cycles=3,
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
    Returns True iff the final state is clean."""
    _, asn_label = find_asn(str(asn_num))
    result = run_validate_gate(asn_label, scope_labels=None)
    if result == "clean":
        return True
    print(f"\n  [VALIDATE-GATE] result={result}; structural violations remain",
          file=sys.stderr)
    return False


def run_pipeline(asn_num):
    """Run full claim derivation pipeline."""
    start = time.time()

    # Phase 1: Decompose — mechanical ## split + per-section LLM
    ok = decompose_asn(asn_num)
    if not ok:
        print(f"\n  [DERIVE] FAILED at decompose", file=sys.stderr)
        return False

    # Phase 2: Enrich — 3 per-claim LLM passes (type, deps, vocab)
    ok = enrich_asn(asn_num)
    if not ok:
        print(f"\n  [DERIVE] FAILED at enrich", file=sys.stderr)
        return False

    # Phase 3: Transclude — project source-note regions as per-claim docs;
    # emit substrate links (claim, contract.<kind>, citation, label, name,
    # provenance.derivation)
    ok = transclude_asn(asn_num)
    if not ok:
        print(f"\n  [DERIVE] FAILED at transclude", file=sys.stderr)
        return False

    # Phase 4: Produce-contract — synthesize Formal Contract sections
    ok = _step_produce_contract(asn_num)
    if not ok:
        print(f"\n  [DERIVE] FAILED at produce-contract", file=sys.stderr)
        return False

    # Phase 5: Validate-gate — comprehensive validator + bounded
    # structural-only fix recipes. Same gate claim convergence runs
    # before each review cycle.
    ok = _step_validate_gate(asn_num)

    elapsed = time.time() - start
    if ok:
        print(f"\n  [DERIVE] COMPLETE ({elapsed:.0f}s)", file=sys.stderr)
    else:
        print(f"\n  [DERIVE] COMPLETE with validation violations "
              f"({elapsed:.0f}s) — Claim File Contract does not hold; "
              f"derivation must be addressed before claim convergence.",
              file=sys.stderr)

    return ok


def main():
    parser = argparse.ArgumentParser(
        description="Run full claim derivation pipeline: "
                    "decompose → enrich → transclude → produce-contract → validate-gate")
    parser.add_argument("asn", help="ASN number (e.g., 36)")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    ok = run_pipeline(asn_num)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
