"""Decompose ASN — operator-gated entry point to claim derivation.

Thin wrapper: resolves an ASN number to its note address and dispatches
to lib/agents/workers/claim_decompose.py::ClaimDecomposeAgent. The agent owns
the actual work (mechanical split, parallel LLM analysis, workspace
writes, commit).

Usage (standalone):
    python scripts/lib/claim_derivation/decompose.py 36
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.agents.workers.claim_decompose import ClaimDecomposeAgent
from lib.protocols.febe.session import open_session
from lib.shared.common import find_asn
from lib.shared.paths import LATTICE


def decompose_asn(asn_num):
    """Run ClaimDecomposeAgent on the note for the given ASN number.

    Returns True iff the agent completed successfully.
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return False

    with open_session(LATTICE) as session:
        note_rel = str(asn_path.resolve().relative_to(LATTICE.resolve()))
        note_addr = session.get_addr_for_path(note_rel)
        if note_addr is None:
            note_addr = session.register_path(note_rel)
        result = ClaimDecomposeAgent()(session, note_addr)
        return result.success


def main():
    parser = argparse.ArgumentParser(
        description="Decompose ASN into sections with YAML analysis")
    parser.add_argument("asn", help="ASN number (e.g., 36)")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    sys.exit(0 if decompose_asn(asn_num) else 1)


if __name__ == "__main__":
    main()
