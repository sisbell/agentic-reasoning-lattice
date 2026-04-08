#!/usr/bin/env python3
"""
Formalization Review — orchestrate proof, contract, cross, and dependency reviews.

Runs the four review steps in order, repeating cycles until all converge
or max cycles reached.

Usage:
    python scripts/formalization-review.py 34
    python scripts/formalization-review.py 34 --max-cycles 1
    python scripts/formalization-review.py 34 --dry-run
"""

import argparse
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.common import find_asn

import importlib
_proof_review = importlib.import_module("proof-review")
_contract_review = importlib.import_module("contract-review")
_cross_review = importlib.import_module("cross-review")

run_proof_review = _proof_review.run_proof_review
run_contract_review = _contract_review.run_contract_review
run_cross_review = _cross_review.run_cross_review


def run_formalization_review(asn_num, max_cycles=3, dry_run=False):
    """Run all four review steps in a convergence loop."""
    _, asn_label = find_asn(str(asn_num))
    if asn_label is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return "failed"

    print(f"\n  [FORMALIZATION-REVIEW] {asn_label}", file=sys.stderr)
    start_time = time.time()

    for cycle in range(1, max_cycles + 1):
        print(f"\n  ========== CYCLE {cycle}/{max_cycles} ==========",
              file=sys.stderr)

        all_converged = True

        # 1. Proof review
        result = run_proof_review(asn_num, max_cycles=1, dry_run=dry_run)
        if result != "converged":
            all_converged = False

        # 2. Contract review
        result = run_contract_review(asn_num, max_cycles=1, dry_run=dry_run)
        if result != "converged":
            all_converged = False

        # 3. Cross-cutting review
        result = run_cross_review(asn_num, max_cycles=1, dry_run=dry_run)
        if result != "converged":
            all_converged = False

        # 4. Dependency review
        try:
            from lib.dependency_review.pipeline import run_dependency_review
            result = run_dependency_review(asn_num, max_cycles=1, dry_run=dry_run)
            if result != "converged":
                all_converged = False
        except Exception as e:
            print(f"  [DEPENDENCY-REVIEW] Skipped: {e}", file=sys.stderr)

        if all_converged:
            elapsed = time.time() - start_time
            print(f"\n  ========== CONVERGED ==========",
                  file=sys.stderr)
            print(f"  All reviews clean after {cycle} cycle{'s' if cycle > 1 else ''}.",
                  file=sys.stderr)
            print(f"  Elapsed: {elapsed:.0f}s", file=sys.stderr)
            return "converged"

        if dry_run:
            break

    elapsed = time.time() - start_time
    print(f"\n  ========== NOT CONVERGED ==========",
          file=sys.stderr)
    print(f"  {max_cycles} cycles completed. Re-run or increase --max-cycles.",
          file=sys.stderr)
    print(f"  Elapsed: {elapsed:.0f}s", file=sys.stderr)
    return "not_converged"


def main():
    parser = argparse.ArgumentParser(
        description="Formalization Review — orchestrate all review steps")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument("--max-cycles", type=int, default=3,
                        help="Maximum outer cycles (default: 3)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Review only, don't fix")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    result = run_formalization_review(asn_num, max_cycles=args.max_cycles,
                                      dry_run=args.dry_run)
    sys.exit(0 if result == "converged" else 1)


if __name__ == "__main__":
    main()
