#!/usr/bin/env python3
"""
Cone Sweep — proactive regional review of high-dependency properties.

Walks the dependency DAG bottom-up, running focused cone reviews on
properties with >= N same-ASN dependencies. Each cone review assembles
just the apex + its dependencies, with narrowed foundation loading.

This is the "regional" optimization stage in the V-cycle:
  local-review (local) → contract-review (local) → cone-sweep (regional) → full-review (global)

Usage:
    python scripts/cone-sweep.py 36
    python scripts/cone-sweep.py 36 --min-deps 3
    python scripts/cone-sweep.py 36 --cone GlobalUniqueness
    python scripts/cone-sweep.py 36 --dry-run
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.formalization.cone import run_cone_sweep, run_cone_review
from lib.shared.common import find_asn, build_label_index, load_property_metadata
from lib.shared.paths import FORMALIZATION_DIR


def main():
    parser = argparse.ArgumentParser(
        description="Cone Sweep — proactive regional review of high-dependency properties")
    parser.add_argument("asn", help="ASN number (e.g., 36)")
    parser.add_argument("--cone", metavar="LABEL",
                        help="Run a single cone on a specific property")
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
        prop_dir = FORMALIZATION_DIR / asn_label
        asn_labels = set(build_label_index(prop_dir).keys())
        meta = load_property_metadata(prop_dir, label=args.cone)
        if not meta:
            print(f"  Property {args.cone} not found", file=sys.stderr)
            sys.exit(1)
        dep_labels = [d for d in meta.get("depends", []) if d in asn_labels]
        result = run_cone_review(asn_num, args.cone, dep_labels,
                                  max_cycles=args.max_cycles,
                                  dry_run=args.dry_run, model=args.model)
        sys.exit(0 if result == "converged" else 1)

    result = run_cone_sweep(asn_num, min_deps=args.min_deps,
                             max_cycles=args.max_cycles,
                             dry_run=args.dry_run, model=args.model)
    sys.exit(0 if result == "converged" else 1)


if __name__ == "__main__":
    main()
