#!/usr/bin/env python3
"""
Promote Proofs — copy verified .dfy files to vault/4-proofs-staging/ASN-NNNN/.

After a Dafny build produces verified .dfy files in modeling-N/,
this script promotes them so downstream ASNs can reference them.

Usage:
    python scripts/promote-proofs.py 34                  # latest modeling-N
    python scripts/promote-proofs.py 34 --modeling 9     # specific directory
    python scripts/promote-proofs.py 34 --dry-run        # show what would be copied
"""

import argparse
import glob
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import WORKSPACE, DAFNY_DIR

PROOFS_DIR = WORKSPACE / "vault" / "4-proofs-staging"


def find_latest_modeling(asn_label):
    """Find the latest modeling-N directory for an ASN."""
    asn_dir = DAFNY_DIR / asn_label
    if not asn_dir.exists():
        return None
    dirs = sorted(asn_dir.glob("modeling-*"),
                  key=lambda d: int(re.search(r"(\d+)$", d.name).group(1))
                  if re.search(r"(\d+)$", d.name) else 0)
    return dirs[-1] if dirs else None


def main():
    parser = argparse.ArgumentParser(
        description="Promote verified .dfy files to vault/5-proofs/")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument("--modeling", type=int, default=None,
                        help="Specific modeling-N directory")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be done")
    args = parser.parse_args()

    asn_number = int(re.sub(r"[^0-9]", "", str(args.asn)))
    asn_label = f"ASN-{asn_number:04d}"

    # Find source directory
    if args.modeling is not None:
        src_dir = DAFNY_DIR / asn_label / f"modeling-{args.modeling}"
    else:
        src_dir = find_latest_modeling(asn_label)

    if src_dir is None or not src_dir.exists():
        print(f"  No modeling directory found for {asn_label}",
              file=sys.stderr)
        sys.exit(1)

    # Find .dfy files
    dfy_files = sorted(src_dir.glob("*.dfy"))
    if not dfy_files:
        print(f"  No .dfy files in {src_dir.name}", file=sys.stderr)
        sys.exit(1)

    dest_dir = PROOFS_DIR / asn_label

    print(f"\n  [PROMOTE-PROOFS] {asn_label} \u2190 {src_dir.name}",
          file=sys.stderr)

    # Clean old files
    old_files = list(dest_dir.glob("*.dfy")) if dest_dir.exists() else []
    if old_files:
        print(f"  Cleaning {dest_dir.relative_to(WORKSPACE)} "
              f"({len(old_files)} old files)", file=sys.stderr)
        if not args.dry_run:
            for f in old_files:
                f.unlink()

    # Copy new files
    print(f"  Copying {len(dfy_files)} .dfy files", file=sys.stderr)
    if not args.dry_run:
        dest_dir.mkdir(parents=True, exist_ok=True)
        for f in dfy_files:
            shutil.copy2(str(f), str(dest_dir / f.name))

    if args.dry_run:
        for f in dfy_files:
            print(f"    {f.name}", file=sys.stderr)
        return

    # Commit
    subprocess.run(
        ["git", "add", str(dest_dir)],
        capture_output=True, text=True, cwd=str(WORKSPACE))
    commit_script = WORKSPACE / "scripts" / "commit.py"
    subprocess.run(
        [sys.executable, str(commit_script),
         f"promote-proofs: {asn_label} from {src_dir.name}"],
        capture_output=True, text=True, cwd=str(WORKSPACE))

    print(f"\n  [DONE] {len(dfy_files)} files \u2192 "
          f"{dest_dir.relative_to(WORKSPACE)}", file=sys.stderr)


if __name__ == "__main__":
    main()
