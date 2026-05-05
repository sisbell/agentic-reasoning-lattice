#!/usr/bin/env python3
"""Reviser-callable CLI to mark an ASN's source note as retired,
or revive it.

    python scripts/substrate/retire.py --asn 47
    python scripts/substrate/retire.py --asn 47 --revive

Retired ASNs are filtered out of every trigger's scope (per
`lib/runner/scope.py::asn_note_addr`) — the runner won't fire any
agent on them. Lifecycle is reversible: revive emits a retraction
on the active retired link.

Lifecycle is binary (active default, retired explicit). State
transitions are real substrate facts (emit retired = retire; emit
retraction on retired = revive); no toggling.

Prints the link id on success; exits non-zero on error.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.backend.emit import emit_retired, emit_retraction
from lib.predicates import is_retired
from lib.protocols.febe.session import open_session
from lib.shared.common import find_asn
from lib.shared.paths import LATTICE


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--asn", required=True, type=int,
        help="ASN number to retire (e.g., 47).",
    )
    parser.add_argument(
        "--revive", action="store_true",
        help="Revive a retired ASN (emit retraction on the retired link).",
    )
    args = parser.parse_args()

    asn_path, asn_label = find_asn(str(args.asn))
    if asn_path is None:
        print(f"error: no note found for ASN-{args.asn:04d}",
              file=sys.stderr)
        return 1

    session = open_session(LATTICE)
    note_rel = str(asn_path.relative_to(LATTICE))
    note_addr = session.get_addr_for_path(note_rel)
    if note_addr is None:
        print(f"error: note not registered in substrate: {note_rel}",
              file=sys.stderr)
        return 1

    if args.revive:
        retired_links = session.active_links(
            "retired", to_set=[note_addr],
        )
        if not retired_links:
            print(f"  {asn_label}: not retired (no-op)", file=sys.stderr)
            return 0
        for link in retired_links:
            emit_retraction(session.store, note_addr, link.addr)
        print(f"  {asn_label}: revived ({len(retired_links)} link(s) "
              f"retracted)", file=sys.stderr)
        return 0

    if is_retired(session, note_addr):
        print(f"  {asn_label}: already retired (no-op)", file=sys.stderr)
        return 0
    link, created = emit_retired(session.store, note_addr)
    print(link.addr)
    print(f"  {asn_label}: retired", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
