#!/usr/bin/env python3
"""
Regional Sweep — proactive regional-scale review of high-dependency claims.

Walks the dependency DAG bottom-up, running focused regional reviews on
claims with >= N same-ASN dependencies. Each regional review assembles
just the apex + its dependencies (the cone), with narrowed foundation loading.

This is the "regional" optimization stage in the V-cycle:
  local-review (local) → contract-review (local) → regional-sweep (regional) → full-review (global)

Usage:
    python scripts/regional-sweep.py 36
    python scripts/regional-sweep.py 36 --min-deps 3
    python scripts/regional-sweep.py 36 --cone GlobalUniqueness
    python scripts/regional-sweep.py 36 --dry-run
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.formalization.regional import run_regional_sweep, run_regional_review
from lib.shared.common import find_asn, build_label_index
from lib.shared.paths import FORMALIZATION_DIR
from lib.store.store import Store
from lib.store.populate import build_cross_asn_label_index


def main():
    parser = argparse.ArgumentParser(
        description="Regional Sweep — proactive regional-scale review of high-dependency claims")
    parser.add_argument("asn", help="ASN number (e.g., 36)")
    parser.add_argument("--cone", metavar="LABEL",
                        help="Run a single regional review on a specific cone apex")
    parser.add_argument("--min-deps", type=int, default=4,
                        help="Minimum same-ASN dependencies to qualify (default: 4)")
    parser.add_argument("--max-cycles", type=int, default=8,
                        help="Max convergence cycles per cone (default: 8)")
    parser.add_argument("--model", default="opus",
                        help="Model for review (default: opus)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Review only, don't fix")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))

    if args.cone:
        _, asn_label = find_asn(str(asn_num))
        claim_dir = FORMALIZATION_DIR / asn_label
        asn_labels = set(build_label_index(claim_dir).keys())
        if args.cone not in asn_labels:
            print(f"  Claim {args.cone} not found", file=sys.stderr)
            sys.exit(1)
        store = Store()
        try:
            label_index = build_cross_asn_label_index()
            apex_path = label_index.get(args.cone)
            rev_index = {p: l for l, p in label_index.items()}
            cites = store.find_links(
                from_set=[apex_path], type_set=["citation"],
            ) if apex_path else []
            dep_labels = [
                rev_index[link["to_set"][0]]
                for link in cites
                if link["to_set"] and rev_index.get(link["to_set"][0]) in asn_labels
            ]
        finally:
            store.close()
        result = run_regional_review(asn_num, args.cone, dep_labels,
                                      max_cycles=args.max_cycles,
                                      dry_run=args.dry_run, model=args.model)
        sys.exit(0 if result == "converged" else 1)

    result = run_regional_sweep(asn_num, min_deps=args.min_deps,
                                 max_cycles=args.max_cycles,
                                 dry_run=args.dry_run, model=args.model)
    sys.exit(0 if result == "converged" else 1)


if __name__ == "__main__":
    main()
