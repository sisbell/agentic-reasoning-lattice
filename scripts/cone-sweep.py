#!/usr/bin/env python3
"""
Cone Sweep — proactive regional review of high-dependency properties.

Walks the dependency DAG bottom-up, running focused cone reviews on
properties with >= N same-ASN dependencies. Each cone review assembles
just the apex + its dependencies, with narrowed foundation loading.

This is the "regional" optimization stage in the V-cycle:
  proof-review (local) → contract-review (local) → cone-sweep (regional) → cross-review (global)

Usage:
    python scripts/cone-sweep.py 36
    python scripts/cone-sweep.py 36 --min-deps 3
    python scripts/cone-sweep.py 36 --dry-run
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.formalization.cone import run_cone_sweep


def main():
    parser = argparse.ArgumentParser(
        description="Cone Sweep — proactive regional review of high-dependency properties")
    parser.add_argument("asn", help="ASN number (e.g., 36)")
    parser.add_argument("--min-deps", type=int, default=4,
                        help="Minimum same-ASN dependencies to qualify (default: 4)")
    parser.add_argument("--max-cycles", type=int, default=3,
                        help="Max convergence cycles per cone (default: 3)")
    parser.add_argument("--model", default="opus",
                        help="Model for review (default: opus)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Review only, don't fix")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    result = run_cone_sweep(asn_num, min_deps=args.min_deps,
                             max_cycles=args.max_cycles,
                             dry_run=args.dry_run, model=args.model)
    sys.exit(0 if result == "converged" else 1)


if __name__ == "__main__":
    main()
