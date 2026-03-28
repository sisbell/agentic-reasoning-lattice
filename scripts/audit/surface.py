#!/usr/bin/env python3
"""
Surface check — foundation consistency audit.

Checks stale labels, structural drift, local redefinitions, registry
misclassification, missing dependencies, exhaustiveness gaps.

Usage:
    python scripts/audit/surface.py 36
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.shared.common import find_asn
from lib.discovery.rebase import step_surface_check


def main():
    parser = argparse.ArgumentParser(
        description="Surface check — foundation consistency audit")
    parser.add_argument("asn", help="ASN number (e.g., 36)")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        sys.exit(1)

    found = step_surface_check(asn_num, asn_path, asn_label)
    sys.exit(0 if not found else 1)


if __name__ == "__main__":
    main()
