#!/usr/bin/env python3
"""
Promote Blueprint — copy blueprint properties to formalization.

Copies per-property files from vault/2-blueprints/ASN-NNNN/properties/
to vault/3-formalization/ASN-NNNN/ where formalization operates on
the files in place.

Usage:
    python scripts/promote-blueprint.py 34
    python scripts/promote-blueprint.py 34 --dry-run
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import (
    WORKSPACE, FORMALIZATION_DIR, blueprint_properties_dir,
)
from lib.shared.common import find_asn


def promote_blueprint(asn_num, dry_run=False):
    """Copy blueprint properties to formalization."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return False

    src = blueprint_properties_dir(asn_label)
    if not src.exists():
        print(f"  No blueprint found for {asn_label}", file=sys.stderr)
        return False

    dst = FORMALIZATION_DIR / asn_label

    print(f"\n  [PROMOTE] {asn_label}", file=sys.stderr)
    print(f"  Source: {src.relative_to(WORKSPACE)}", file=sys.stderr)
    print(f"  Target: {dst.relative_to(WORKSPACE)}", file=sys.stderr)

    # Count files
    files = list(src.glob("*.md"))
    print(f"  Files:  {len(files)}", file=sys.stderr)

    if dst.exists():
        print(f"  WARNING: {dst.relative_to(WORKSPACE)} already exists — will overwrite",
              file=sys.stderr)

    if dry_run:
        print(f"\n  [DRY RUN] Would copy {len(files)} files", file=sys.stderr)
        return True

    # Copy
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

    print(f"\n  [PROMOTE] Done — {len(files)} files copied", file=sys.stderr)
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Promote blueprint to formalization")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be done")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    ok = promote_blueprint(asn_num, dry_run=args.dry_run)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
