#!/usr/bin/env python3
"""
Generate a Dafny review from the current modeling state.

Verifies all .dfy files, extracts divergences, and calls the review agent
on verified files with divergences. Human-triggered — run when ready to
triage divergences after fixing verification failures.

Usage:
    python scripts/model.py review 1
    python scripts/model.py review 1 --modeling 2
    python scripts/model.py review 1 --model sonnet
"""

import argparse
import re
import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from paths import (WORKSPACE, DAFNY_DIR, formal_stmts,
                    find_latest_modeling_dir)
from lib.model_dafny import (extract_divergences, find_asn_path,
                               generate_dafny_review, run_commit)
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
        description="Generate a Dafny review from current modeling state")
    parser.add_argument("asn",
                        help="ASN number (e.g., 1, 0001, ASN-0001)")
    parser.add_argument("--modeling", type=int, default=None,
                        help="Target specific modeling-N directory")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"],
                        help="Model for review generation (default: opus)")
    args = parser.parse_args()

    gen_dir, asn_label = find_modeling_dir(args.asn, args.modeling)
    if gen_dir is None:
        print(f"  No modeling directory found for {args.asn}", file=sys.stderr)
        sys.exit(1)

    print(f"[REVIEW] {asn_label} — {gen_dir.relative_to(WORKSPACE)}",
          file=sys.stderr)

    # Find extract for context
    asn_num = int(re.search(r'\d+', asn_label).group())
    extract_path = formal_stmts(asn_num)
    if not extract_path.exists():
        print(f"  No statements extract found for {asn_label}", file=sys.stderr)
        print(f"  Run: python scripts/export.py {args.asn}",
              file=sys.stderr)
        sys.exit(1)
    extract_text = extract_path.read_text()

    # Verify all .dfy files and collect results
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

        # Parse ASN label from filename (proof_label is the stem)
        results.append({
            "label": dfy_path.stem,
            "proof_label": dfy_path.stem,
            "dfy_path": dfy_path,
            "verified": ok,
            "divergences": divergences,
        })

    # Filter to verified files only — unverified files need fixing first
    verified_results = [r for r in results if r["verified"]]
    verified_divs = [r for r in verified_results if r["divergences"]]

    verified = sum(1 for r in results if r["verified"])
    total = len(results)
    print(f"\n  {verified}/{total} verified, "
          f"{len(verified_divs)} with divergences", file=sys.stderr)

    if not verified_results:
        print(f"  No verified files to review — run model.py fix first",
              file=sys.stderr)
        sys.exit(1)

    # Generate review
    asn_path = find_asn_path(asn_label)
    review_path = generate_dafny_review(
        asn_label, verified_results, extract_text,
        asn_path=asn_path, model=args.model,
    )

    if review_path:
        print(f"\n  [REVIEW] {review_path.relative_to(WORKSPACE)}",
              file=sys.stderr)
        run_commit(f"{asn_label} dafny review")
    else:
        print(f"  Review generation failed", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
