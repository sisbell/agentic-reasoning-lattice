#!/usr/bin/env python3
"""
Blueprint — full pipeline: decompose → enrich → disassemble → validate.

Runs the complete blueprinting pipeline on an ASN. Each stage commits
its output automatically.

Usage:
    python scripts/note-decompose.py 36
"""

import argparse
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.note_decomposition.decompose import decompose_asn
from lib.note_decomposition.enrich import enrich_asn
from lib.note_decomposition.disassemble import disassemble_asn
from lib.note_decomposition.validate import print_validation


def run_blueprint(asn_num):
    """Run full blueprinting pipeline."""
    start = time.time()

    # Step 1: Decompose — mechanical ## split + per-section LLM
    ok = decompose_asn(asn_num)
    if not ok:
        print(f"\n  [BLUEPRINT] FAILED at decompose", file=sys.stderr)
        return False

    # Step 2: Enrich — 3 per-claim LLM passes (type, deps, vocab)
    ok = enrich_asn(asn_num)
    if not ok:
        print(f"\n  [BLUEPRINT] FAILED at enrich", file=sys.stderr)
        return False

    # Step 3: Disassemble — section YAMLs → per-claim .yaml + .md pairs
    ok = disassemble_asn(asn_num)
    if not ok:
        print(f"\n  [BLUEPRINT] FAILED at disassemble", file=sys.stderr)
        return False

    # Step 4: Validate — structural integrity checks
    ok = print_validation(asn_num)

    elapsed = time.time() - start
    if ok:
        print(f"\n  [BLUEPRINT] COMPLETE ({elapsed:.0f}s)", file=sys.stderr)
        print(f"  Next: python scripts/promote-blueprint.py {asn_num}",
              file=sys.stderr)
    else:
        print(f"\n  [BLUEPRINT] COMPLETE with validation errors ({elapsed:.0f}s)",
              file=sys.stderr)

    return ok


def main():
    parser = argparse.ArgumentParser(
        description="Run full blueprinting pipeline: decompose → enrich → disassemble → validate")
    parser.add_argument("asn", help="ASN number (e.g., 36)")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    ok = run_blueprint(asn_num)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
