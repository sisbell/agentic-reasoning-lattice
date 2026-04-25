#!/usr/bin/env python3
"""
Promote Blueprint — copy blueprint claims to claim convergence.

Copies per-claim files from lattices/xanadu/blueprinting/ASN-NNNN/claims/
to lattices/xanadu/claim-convergence/ASN-NNNN/ where claim convergence operates on
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
    WORKSPACE, CLAIM_CONVERGENCE_DIR, blueprint_claims_dir,
)
from lib.shared.common import find_asn, step_commit_asn


def promote_blueprint(asn_num, dry_run=False):
    """Copy blueprint claims to claim convergence."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return False

    src = blueprint_claims_dir(asn_label)
    if not src.exists():
        print(f"  No blueprint found for {asn_label}", file=sys.stderr)
        return False

    dst = CLAIM_CONVERGENCE_DIR / asn_label

    print(f"\n  [PROMOTE] {asn_label}", file=sys.stderr)
    print(f"  Source: {src.relative_to(WORKSPACE)}", file=sys.stderr)
    print(f"  Target: {dst.relative_to(WORKSPACE)}", file=sys.stderr)

    # Collect files: per-claim .yaml + .md pairs + structural _*.md
    yaml_files = sorted(f for f in src.glob("*.yaml"))
    md_files = sorted(f for f in src.glob("*.md")
                      if not f.name.startswith("_"))
    structural_files = sorted(f for f in src.glob("_*.md"))
    files = yaml_files + md_files + structural_files
    print(f"  Files:  {len(files)} ({len(yaml_files)} yaml, {len(md_files)} md, "
          f"{len(structural_files)} structural)", file=sys.stderr)

    if dst.exists():
        print(f"  WARNING: {dst.relative_to(WORKSPACE)} already exists — will overwrite",
              file=sys.stderr)

    if dry_run:
        for f in files:
            print(f"    {f.name}", file=sys.stderr)
        return True

    # Copy selected files
    dst.mkdir(parents=True, exist_ok=True)
    for f in files:
        shutil.copy2(f, dst / f.name)

    print(f"\n  [PROMOTE] Done — {len(files)} files copied", file=sys.stderr)

    step_commit_asn(asn_num, hint="promote-blueprint")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Promote blueprint to claim convergence")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be done")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    ok = promote_blueprint(asn_num, dry_run=args.dry_run)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
