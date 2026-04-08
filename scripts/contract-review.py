#!/usr/bin/env python3
"""
Contract Review — validate formal contracts against proofs.

Runs contract validation (sonnet, ~4s per property) on all properties
with formal contracts. On MISMATCH, re-runs produce-contract (opus)
to rewrite the contract with full proof + deps context.

Usage:
    python scripts/contract-review.py 34
    python scripts/contract-review.py 34 --label T1
    python scripts/contract-review.py 34 --dry-run
    python scripts/contract-review.py 34 --max-cycles 1
"""

import argparse
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import WORKSPACE, FORMALIZATION_DIR, REVIEWS_DIR, next_review_number
from lib.shared.common import find_asn, step_commit_asn
from lib.formalization.assembly.validate_contracts import validate_contract
from lib.formalization.formalize.produce_contract import (
    _has_formal_contract, quality_rewrite)


def run_contract_review(asn_num, max_cycles=5, dry_run=False,
                         single_label=None):
    """Run contract review — validate and fix contracts.

    Returns "converged" or "not_converged".
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return "failed"

    print(f"\n  [CONTRACT-REVIEW] {asn_label}", file=sys.stderr)

    prop_dir = FORMALIZATION_DIR / asn_label
    if not prop_dir.exists():
        print(f"  No formalization directory for {asn_label}", file=sys.stderr)
        return "failed"

    print(f"  Directory: {prop_dir.relative_to(WORKSPACE)}", file=sys.stderr)

    start_time = time.time()
    converged = False
    had_findings = False

    for cycle in range(1, max_cycles + 1):
        # Read per-property files
        prop_files = sorted(
            f for f in prop_dir.glob("*.md")
            if not f.name.startswith("_")
        )

        if single_label:
            prop_files = [f for f in prop_files
                          if f.name.replace(".md", "") == single_label]

        # Validate each property
        mismatches = []
        checked = 0

        print(f"\n  [CYCLE {cycle}/{max_cycles}] {len(prop_files)} properties",
              file=sys.stderr)

        for f in prop_files:
            label = f.name.replace(".md", "")
            content = f.read_text()
            if not content or not _has_formal_contract(content):
                continue
            checked += 1

            match, detail = validate_contract(label, content)
            if match:
                print(f"    {label}: MATCH", file=sys.stderr)
            else:
                print(f"    {label}: MISMATCH", file=sys.stderr)
                for line in detail.split('\n')[:3]:
                    if line.strip():
                        print(f"      {line.strip()}", file=sys.stderr)
                mismatches.append((label, detail, f))

        print(f"\n  {checked} checked, {len(mismatches)} mismatches",
              file=sys.stderr)

        if not mismatches:
            converged = True
            print(f"\n  Converged after {cycle} cycle{'s' if cycle > 1 else ''}.",
                  file=sys.stderr)
            if not had_findings:
                print(f"  Nothing to do.", file=sys.stderr)
            break

        had_findings = True

        if dry_run:
            print(f"\n  {len(mismatches)} mismatches reported.",
                  file=sys.stderr)
            break

        # Fix mismatches via produce-contract (opus, full context)
        for label, detail, prop_path in mismatches:
            content = prop_path.read_text()
            print(f"  [FIX] {label} — re-running produce-contract...",
                  file=sys.stderr)
            ok, changed, response = quality_rewrite(
                asn_num, label, content, prop_path=prop_path, max_cycles=1)
            if changed:
                step_commit_asn(asn_num,
                                hint=f"{label} contract fix")

        # Write review
        (REVIEWS_DIR / asn_label).mkdir(parents=True, exist_ok=True)
        review_num = next_review_number(asn_label)
        review_path = REVIEWS_DIR / asn_label / f"review-{review_num}.md"
        with open(review_path, "w") as rf:
            rf.write(f"# Contract Review — {asn_label} (cycle {cycle})\n\n")
            rf.write(f"*{time.strftime('%Y-%m-%d %H:%M')}*\n\n")
            for label, detail, _ in mismatches:
                rf.write(f"### {label}\n\n{detail}\n\n")
            rf.write(f"{len(mismatches)} mismatches.\n")

    elapsed = time.time() - start_time
    print(f"  Elapsed: {elapsed:.0f}s", file=sys.stderr)

    return "converged" if converged else "not_converged"


def main():
    parser = argparse.ArgumentParser(
        description="Contract Review — validate and fix formal contracts")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument("--max-cycles", type=int, default=5,
                        help="Maximum convergence cycles (default: 5)")
    parser.add_argument("--label", help="Review a single property only")
    parser.add_argument("--dry-run", action="store_true",
                        help="Report mismatches without fixing")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    result = run_contract_review(asn_num, max_cycles=args.max_cycles,
                                  dry_run=args.dry_run,
                                  single_label=args.label)
    sys.exit(0 if result == "converged" else 1)


if __name__ == "__main__":
    main()
