#!/usr/bin/env python3
"""
Claim derivation — full pipeline: decompose → enrich → transclude → validate.

Runs the complete claim-derivation pipeline on an ASN. Each stage commits
its output automatically.

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
from lib.claim_derivation.transclude import transclude_asn
from lib.claim_derivation.validate import print_validation


def run_blueprint(asn_num):
    """Run full claim derivation pipeline."""
    start = time.time()

    # Step 1: Decompose — mechanical ## split + per-section LLM
    ok = decompose_asn(asn_num)
    if not ok:
        print(f"\n  [DERIVE] FAILED at decompose", file=sys.stderr)
        return False

    # Step 2: Enrich — 3 per-claim LLM passes (type, deps, vocab)
    ok = enrich_asn(asn_num)
    if not ok:
        print(f"\n  [DERIVE] FAILED at enrich", file=sys.stderr)
        return False

    # Step 3: Transclude — section YAMLs → per-claim .yaml + .md pairs
    ok = transclude_asn(asn_num)
    if not ok:
        print(f"\n  [DERIVE] FAILED at transclude", file=sys.stderr)
        return False

    # Step 4: Validate — structural integrity checks
    ok = print_validation(asn_num)

    elapsed = time.time() - start
    if ok:
        print(f"\n  [DERIVE] COMPLETE ({elapsed:.0f}s)", file=sys.stderr)
        print(f"  Next: python scripts/promote-blueprint.py {asn_num}",
              file=sys.stderr)
    else:
        print(f"\n  [DERIVE] COMPLETE with validation errors ({elapsed:.0f}s)",
              file=sys.stderr)

    return ok


def main():
    parser = argparse.ArgumentParser(
        description="Run full claim derivation pipeline: decompose → enrich → transclude → validate")
    parser.add_argument("asn", help="ASN number (e.g., 36)")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    ok = run_blueprint(asn_num)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
