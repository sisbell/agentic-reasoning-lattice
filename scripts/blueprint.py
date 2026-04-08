#!/usr/bin/env python3
"""
Blueprint — format normalization + name population.

Prepares a monolithic ASN for disassembly. Runs format review/revise,
populates the Name column, and commits.

Usage:
    python scripts/blueprint.py 34
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.common import find_asn, step_commit_asn
from lib.blueprinting.format import normalize_format
from lib.blueprinting.names import step_populate_names


def run_blueprint(asn_num):
    """Run the blueprinting pipeline: format → names → commit."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return False

    print(f"\n  [BLUEPRINT] {asn_label}", file=sys.stderr)

    # 1. Format normalization
    ok = normalize_format(asn_num)
    if not ok:
        return False

    # 2. Name population
    ok = step_populate_names(asn_num)
    if not ok:
        return False

    # 3. Commit format + names
    step_commit_asn(asn_num, hint="blueprint")

    print(f"\n  [BLUEPRINT] Done. Next step:",
          file=sys.stderr)
    print(f"  python scripts/disassemble.py {asn_num}", file=sys.stderr)
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Blueprint — format + names + lint")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    ok = run_blueprint(asn_num)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
