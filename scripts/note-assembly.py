#!/usr/bin/env python3
"""
Discovery Export — extract claim-statements.md from a discovery ASN.

Uses LLM to parse narrative reasoning into structured formal
statements; commits the artifact. Dependencies are sourced from
substrate citation links and don't need a separate generation step.

Usage:
    python scripts/note-assembly.py 40
    python scripts/note-assembly.py 34 36 40          # multiple ASNs
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import WORKSPACE, claim_statements
from lib.note_convergence.produce_interface import export_one

COMMIT_SCRIPT = WORKSPACE / "scripts" / "commit.py"


def main():
    parser = argparse.ArgumentParser(
        description="Discovery Export — claim-statements.md from discovery ASNs")
    parser.add_argument("asns", nargs="+",
                        help="ASN numbers (e.g., 55 56 34) or paths")
    parser.add_argument("--model", "-m", default="sonnet",
                        choices=["opus", "sonnet"],
                        help="Model for statement extraction (default: sonnet)")
    parser.add_argument("--effort", default="high",
                        help="Thinking effort level (default: high)")
    args = parser.parse_args()

    succeeded = []
    failed = []

    for asn_id in args.asns:
        label, ok = export_one(asn_id, model=args.model, effort=args.effort)
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
               f"Export statements {labels}"]
        subprocess.run(cmd, capture_output=True, text=True, cwd=str(WORKSPACE))

    if failed:
        print(f"\n  FAILED: {', '.join(failed)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
