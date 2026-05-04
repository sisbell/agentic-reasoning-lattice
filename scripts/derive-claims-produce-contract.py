#!/usr/bin/env python3
"""
Run the claim-derivation produce-contract phase standalone.

Synthesizes the Formal Contract section in each claim's body markdown.
Runs across every claim in the ASN that lacks a contract or whose
prose hash has changed since the last run.

Usage:
    python scripts/derive-claims-produce-contract.py <ASN>
    python scripts/derive-claims-produce-contract.py 36
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.claim_derivation.produce_contract import (
    find_claims_needing_quality, produce_contract,
)
from lib.shared.common import find_asn
from lib.shared.git_ops import step_commit_asn


def main():
    parser = argparse.ArgumentParser(
        description="Synthesize Formal Contract sections for claims that "
                    "lack one (or whose prose has changed since last run).")
    parser.add_argument("asn", help="ASN number (e.g., 36)")
    parser.add_argument("--force", action="store_true",
                        help="Force rebuild for every claim, ignoring hashes.")
    parser.add_argument("--label",
                        help="Restrict to a single claim label.")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    candidates, _ = find_claims_needing_quality(
        asn_num, force_all=True, force_rebuild=args.force,
    )
    if args.label:
        candidates = [c for c in candidates if c["label"] == args.label]

    if not candidates:
        print("  No claims need contract synthesis", file=sys.stderr)
        return 0

    _, asn_label = find_asn(str(asn_num))
    n_ok = 0
    n_failed = 0
    any_changed = False
    for item in candidates:
        label = item["label"]
        section = item["section"]
        claim_path = item.get("path")
        ok, file_changed, _response = produce_contract(
            asn_num, label, section, claim_path=claim_path, max_cycles=3,
        )
        if ok:
            n_ok += 1
        else:
            n_failed += 1
        if file_changed:
            any_changed = True

    if any_changed:
        step_commit_asn(asn_num, hint="produce-contract")

    print(f"\n  [PRODUCE-CONTRACT] {n_ok} ok, {n_failed} failed",
          file=sys.stderr)
    return 0 if n_failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
