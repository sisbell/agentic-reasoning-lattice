#!/usr/bin/env python3
"""Claim derivation CLI — runs the full derivation pipeline on an ASN.

Pipeline stages: decompose → annotate → transclude → validate-transclude
→ produce-contract → validate-gate. Each stage commits its output. See
lib/orchestrators/claim_derivation/orchestrator.py for the body.

Usage:
    python scripts/derive-claims.py 36
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.orchestrators.claim_derivation import run_pipeline


def main():
    parser = argparse.ArgumentParser(
        description="Run full claim derivation pipeline.",
    )
    parser.add_argument("asn", help="ASN number (e.g., 36)")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    sys.exit(0 if run_pipeline(asn_num) else 1)


if __name__ == "__main__":
    main()
