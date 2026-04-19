#!/usr/bin/env python3
"""
Formalization Review — orchestrate local, contract, full, and dependency reviews.

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
_local_review = importlib.import_module("local-review")
_contract_review = importlib.import_module("contract-review")
_full_review = importlib.import_module("full-review")

run_local_review = _local_review.run_local_review
run_contract_review = _contract_review.run_contract_review
run_full_review = _full_review.run_full_review


def run_formalization_review(asn_num, max_cycles=3, dry_run=False,
                             keep_cache=False):
    """Run all four review steps in a convergence loop.

    keep_cache: if True, don't invalidate hash caches between outer cycles.
    Only changed claims get re-checked — useful when iterating on
    full-review findings where most claims are untouched.
    """
    _, asn_label = find_asn(str(asn_num))
    if asn_label is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return "failed"

    from lib.shared.paths import FORMALIZATION_DIR
    claim_dir = FORMALIZATION_DIR / asn_label

    print(f"\n  [FORMALIZATION-REVIEW] {asn_label}", file=sys.stderr)
    start_time = time.time()

    for cycle in range(1, max_cycles + 1):
        print(f"\n  ========== CYCLE {cycle}/{max_cycles} ==========",
              file=sys.stderr)

        # Invalidate caches so each outer cycle re-checks everything
        # (prior steps may have changed files that affect later steps)
        # With --keep-cache, only claims whose source hash changed
        # will be re-checked — much faster for full-review convergence.
        if not keep_cache:
            for cache_name in ("_verify-cache.json", "_contract-cache.json"):
                cache_path = claim_dir / cache_name
                if cache_path.exists():
                    cache_path.unlink()

        all_converged = True

        # 1. Local review (find → fix → converge)
        result = run_local_review(asn_num, max_cycles=5, dry_run=dry_run)
        if result != "converged":
            all_converged = False

        # 2. Contract review (validate → fix → converge)
        result = run_contract_review(asn_num, max_cycles=5, dry_run=dry_run)
        if result != "converged":
            all_converged = False

        # 3. Full review (whole-ASN → fix → converge)
        result = run_full_review(asn_num, max_cycles=3, dry_run=dry_run)
        if result != "converged":
            all_converged = False

        # 4. Dependency review (validate refs → fix → converge)
        try:
            from lib.dependency_review.pipeline import run_dependency_review
            result = run_dependency_review(asn_num, max_cycles=3, dry_run=dry_run)
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
    parser.add_argument("--keep-cache", action="store_true",
                        help="Don't invalidate caches between cycles — "
                             "only re-check claims whose source changed")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    result = run_formalization_review(asn_num, max_cycles=args.max_cycles,
                                      dry_run=args.dry_run,
                                      keep_cache=args.keep_cache)
    sys.exit(0 if result == "converged" else 1)


if __name__ == "__main__":
    main()
