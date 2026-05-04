#!/usr/bin/env python3
"""Print one-line predicate status for a note.

Output (single line, machine-readable):
    NOTE=<asn-label> REVISES_TOTAL=<n> REVISES_OPEN=<n> RESOLUTIONS=<n> PREDICATE_HOLDS=<true|false>

Usage:
    python3 scripts/agent_tools/predicate_status.py <asn>
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.predicates import unresolved_revise_comments
from lib.protocols.febe.session import open_session
from lib.shared.common import find_asn
from lib.shared.paths import LATTICE


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("asn", help="ASN number or label (e.g. 1, 0001, ASN-0001)")
    args = ap.parse_args()

    asn_path, asn_label = find_asn(args.asn)
    if asn_path is None:
        print(f"ERROR: ASN not found: {args.asn}", file=sys.stderr)
        sys.exit(1)

    note_rel = str(asn_path.resolve().relative_to(LATTICE.resolve()))
    with open_session(LATTICE) as session:
        note_addr = session.get_addr_for_path(note_rel)

        revises = session.active_links("comment.revise", to_set=[note_addr])
        open_items = unresolved_revise_comments(session, note_addr)
        open_count = len(open_items)
        total_count = len(revises)
        resolutions_count = total_count - open_count

        predicate = "true" if open_count == 0 else "false"
        print(
            f"NOTE={asn_label} "
            f"REVISES_TOTAL={total_count} "
            f"REVISES_OPEN={open_count} "
            f"RESOLUTIONS={resolutions_count} "
            f"PREDICATE_HOLDS={predicate}"
        )


if __name__ == "__main__":
    main()
