#!/usr/bin/env python3
"""Decompose ASN — operator-gated entry to claim derivation.

Phase 1 of the derivation arc, run standalone. Mechanically splits the
source note at `## ` headers, runs the decompose LLM in parallel on
each non-structural section, resolves each LLM-proposed body against
the source note, and emits per-claim identity to substrate (claim md,
label, name, provenance.derivation, transclusion.claim-statements).

For the full pipeline (decompose + runner walk + validate-gate), run
scripts/derive-claims.py instead.

Usage:
    python scripts/derive-claims-split.py <ASN>
    python scripts/derive-claims-split.py 36
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.agents.producers.claim_decompose import ClaimDecomposeAgent
from lib.lattice.labels import format_label
from lib.protocols.febe.session import open_session
from lib.shared.common import find_asn
from lib.shared.paths import LATTICE


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Decompose ASN into claim mds + identity facts.",
    )
    parser.add_argument("asn", help="ASN number (e.g., 36)")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    asn_path, _ = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  {format_label(asn_num)} not found", file=sys.stderr)
        return 1

    with open_session(LATTICE) as session:
        note_rel = str(asn_path.resolve().relative_to(LATTICE.resolve()))
        note_addr = session.get_addr_for_path(note_rel)
        if note_addr is None:
            note_addr = session.register_path(note_rel)
        result = ClaimDecomposeAgent()(session, note_addr)
        return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
