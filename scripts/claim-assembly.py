#!/usr/bin/env python3
"""
Formalization Assembly — re-emit claim-statements.md from edited claims.

Reads each claim's substrate-sourced sidecars (`<stem>.name.md`,
`<stem>.description.md`) and the formal contract from its .md body,
then mechanically assembles the condensed ASN summary that
downstream ASN discovery consumes as a dependency. No LLM calls.

Usage:
    python scripts/claim-assembly.py 34
    python scripts/claim-assembly.py 34 36 40
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import WORKSPACE, claim_statements
from lib.shared.common import find_asn
from lib.claim_convergence.produce_interface import assemble_claim_statements

COMMIT_SCRIPT = WORKSPACE / "scripts" / "commit.py"


def _export_one(asn_id):
    """Re-assemble claim-statements.md for one ASN.

    Returns (asn_label, True) on success, (asn_id, False) on failure.
    """
    asn_path, asn_label = find_asn(asn_id)
    if asn_path is None:
        print(f"  No ASN found for {asn_id}", file=sys.stderr)
        return asn_id, False

    asn_num = int(re.sub(r"[^0-9]", "", str(asn_id)))

    path = assemble_claim_statements(asn_num)
    if path is None:
        print(f"  [ERROR] Assembly failed for {asn_label}", file=sys.stderr)
        return asn_label, False

    print(str(path))
    return asn_label, True


def main():
    parser = argparse.ArgumentParser(
        description="Formalization Assembly — claim-statements.md")
    parser.add_argument("asns", nargs="+",
                        help="ASN numbers (e.g., 34 36 40) or paths")
    args = parser.parse_args()

    succeeded = []
    failed = []

    for asn_id in args.asns:
        label, ok = _export_one(asn_id)
        if ok:
            succeeded.append(label)
        else:
            failed.append(label)

    if succeeded:
        labels = ", ".join(sorted(succeeded))
        print(f"\n  === COMMIT ({labels}) ===", file=sys.stderr)
        for lbl in sorted(succeeded):
            lbl_num = int(re.sub(r"[^0-9]", "", lbl))
            subprocess.run(
                ["git", "add", str(claim_statements(lbl_num))],
                capture_output=True, text=True, cwd=str(WORKSPACE))
        cmd = [sys.executable, str(COMMIT_SCRIPT),
               f"Export formal statements {labels}"]
        subprocess.run(cmd, capture_output=True, text=True, cwd=str(WORKSPACE))

    if failed:
        print(f"\n  FAILED: {', '.join(failed)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
