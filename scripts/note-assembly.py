#!/usr/bin/env python3
"""
Discovery Export — extract a note's formal-statements sidecar.

Manual entry into the NoteStatementsAgent. The trigger-driven path
runs the same agent automatically when an ASN is confirmed and its
statements chain is shorter than the note's chain.

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
from lib.agents.note_statements import NoteStatementsAgent
from lib.protocols.febe.session import open_session
from lib.shared.common import find_asn
from lib.shared.paths import LATTICE, WORKSPACE, claim_statements


COMMIT_SCRIPT = WORKSPACE / "scripts" / "commit.py"


def _run_one(session, agent, asn_id):
    """Run the note-statements agent on one ASN. Returns (label, ok)."""
    asn_path, asn_label = find_asn(asn_id)
    if asn_path is None:
        print(f"  No ASN found for {asn_id}", file=sys.stderr)
        return asn_id, False
    note_rel = str(asn_path.relative_to(LATTICE))
    note_addr = session.get_addr_for_path(note_rel)
    if note_addr is None:
        print(f"  Note not registered in substrate: {note_rel}",
              file=sys.stderr)
        return asn_label, False
    result = agent(session, note_addr)
    return asn_label, result.success


def main():
    parser = argparse.ArgumentParser(
        description="Discovery Export — note's formal-statements sidecar")
    parser.add_argument("asns", nargs="+",
                        help="ASN numbers (e.g., 55 56 34) or paths")
    args = parser.parse_args()

    agent = NoteStatementsAgent()
    succeeded = []
    failed = []

    with open_session(LATTICE) as session:
        for asn_id in args.asns:
            label, ok = _run_one(session, agent, asn_id)
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
