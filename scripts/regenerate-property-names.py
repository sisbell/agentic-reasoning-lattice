#!/usr/bin/env python3
"""Regenerate _property_names.md for an ASN.

Reads _table.md, applies label_to_filename() to each label, verifies
the file exists, and writes the mapping. Works for both blueprinting
and formalization directories.

Usage:
    python scripts/regenerate-property-names.py --blueprinting 36
    python scripts/regenerate-property-names.py --formalization 34
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.common import generate_property_names
from lib.shared.paths import WORKSPACE

BLUEPRINTS_DIR = WORKSPACE / "vault" / "2-blueprints"
FORMALIZATION_DIR = WORKSPACE / "vault" / "3-formalization"


def main():
    parser = argparse.ArgumentParser(
        description="Regenerate _property_names.md for an ASN")
    parser.add_argument("asn", help="ASN number (e.g., 34, 36)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--blueprinting", action="store_true",
                       help="Target vault/2-blueprints/ASN-NNNN/properties/")
    group.add_argument("--formalization", action="store_true",
                       help="Target vault/3-formalization/ASN-NNNN/")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    asn_label = f"ASN-{asn_num:04d}"

    if args.blueprinting:
        prop_dir = BLUEPRINTS_DIR / asn_label / "properties"
    else:
        prop_dir = FORMALIZATION_DIR / asn_label

    if not prop_dir.exists():
        print(f"  Directory not found: {prop_dir.relative_to(WORKSPACE)}",
              file=sys.stderr)
        sys.exit(1)

    print(f"  [PROPERTY-NAMES] {asn_label} ({prop_dir.relative_to(WORKSPACE)})",
          file=sys.stderr)

    mapping, warnings = generate_property_names(prop_dir)

    for w in warnings:
        print(f"    WARNING: {w}", file=sys.stderr)

    print(f"  [PROPERTY-NAMES] {len(mapping)} labels mapped", file=sys.stderr)

    if warnings:
        sys.exit(1)


if __name__ == "__main__":
    main()
