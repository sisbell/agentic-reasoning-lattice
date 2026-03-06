#!/usr/bin/env python3
"""
Generate STATUS.md for a modeling directory by verifying all .dfy files.

Usage:
    python scripts/model.py status 1
    python scripts/model.py status 1 --modeling 2
"""

import argparse
import re
import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from paths import (WORKSPACE, DAFNY_DIR, find_latest_modeling_dir)
from lib.model_dafny import write_status_file, extract_divergences, run_commit
from lib.model_fix import verify_dafny


def find_modeling_dir(asn_id, modeling_num=None):
    num = re.sub(r"[^0-9]", "", str(asn_id))
    if not num:
        return None, None
    label = f"ASN-{int(num):04d}"

    if modeling_num is not None:
        d = DAFNY_DIR / label / f"modeling-{modeling_num}"
        return (d if d.exists() else None), label

    return find_latest_modeling_dir(label), label


def main():
    parser = argparse.ArgumentParser(
        description="Generate STATUS.md for a modeling directory")
    parser.add_argument("asn",
                        help="ASN number (e.g., 1, 0001, ASN-0001)")
    parser.add_argument("--modeling", type=int, default=None,
                        help="Target specific modeling-N directory")
    args = parser.parse_args()

    gen_dir, asn_label = find_modeling_dir(args.asn, args.modeling)
    if gen_dir is None:
        print(f"  No modeling directory found for {args.asn}", file=sys.stderr)
        sys.exit(1)

    print(f"[STATUS] {asn_label} — {gen_dir.relative_to(WORKSPACE)}",
          file=sys.stderr)

    dfy_files = sorted(gen_dir.glob("*.dfy"))
    if not dfy_files:
        print(f"  No .dfy files found", file=sys.stderr)
        sys.exit(1)

    results = []
    for dfy_path in dfy_files:
        ok, vout = verify_dafny(dfy_path)
        divergences = extract_divergences(dfy_path)
        status = "verified" if ok else "UNVERIFIED"
        div_tag = f" +{len(divergences)}div" if divergences else ""
        print(f"  [{status}] {dfy_path.stem}{div_tag}", file=sys.stderr)

        results.append({
            "proof_label": dfy_path.stem,
            "verified": ok,
            "divergences": divergences,
        })

    write_status_file(gen_dir, results, source="generate")

    verified = sum(1 for r in results if r["verified"])
    print(f"\n  {verified}/{len(results)} verified", file=sys.stderr)
    print(f"  Written: {gen_dir.name}/STATUS.md", file=sys.stderr)

    run_commit(f"{asn_label} status update")


if __name__ == "__main__":
    main()
