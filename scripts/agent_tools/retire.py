#!/usr/bin/env python3
"""Reviser-callable CLI to mark an ASN's source note as retired,
or revive it.

    python scripts/agent_tools/retire.py --asn 47
    python scripts/agent_tools/retire.py --asn 47 --revive

Retired ASNs are filtered out of every trigger's scope (per
`lib/runner/scope.py::asn_note_addr`) — the runner won't fire any
agent on them. Lifecycle is reversible: revive emits a retraction
on the active retired link.

When the target ASN has only an inquiry (pre-draft state, no note),
retires the inquiry address instead. The walker and `note_draft`
predicate filter retired inquiries the same way they filter retired
notes.

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
from lib.lattice.labels import format_label
from lib.predicates import is_retired
from lib.protocols.febe.session import open_session
from lib.shared.common import find_asn
from lib.shared.paths import INQUIRY_DIR, LATTICE, WORKSPACE


def _resolve_target(session, asn_num: int) -> tuple[str, str]:
    """Return (target_addr, kind) where kind ∈ {note, inquiry}.

    Prefer the note address when one exists. Fall back to the
    inquiry address for inquiry-only (pre-draft) ASNs.
    """
    asn_path, _ = find_asn(str(asn_num))
    if asn_path is not None:
        note_rel = str(asn_path.relative_to(WORKSPACE))
        note_addr = session.get_addr_for_path(note_rel)
        if note_addr is not None:
            return note_addr, "note"

    inq_path = INQUIRY_DIR / f"{format_label(asn_num)}.md"
    if inq_path.exists():
        inq_rel = str(inq_path.relative_to(WORKSPACE))
        inq_addr = session.get_addr_for_path(inq_rel)
        if inq_addr is not None:
            return inq_addr, "inquiry"

    return None, None


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

    asn_label = format_label(args.asn)
    session = open_session(LATTICE)
    target_addr, kind = _resolve_target(session, args.asn)
    if target_addr is None:
        print(
            f"error: no note OR inquiry registered in substrate for "
            f"{asn_label}",
            file=sys.stderr,
        )
        return 1

    if args.revive:
        retired_links = session.active_links(
            "retired", to_set=[target_addr],
        )
        if not retired_links:
            print(f"  {asn_label}: not retired (no-op)", file=sys.stderr)
            return 0
        for link in retired_links:
            emit_retraction(session.store, target_addr, link.addr)
        print(
            f"  {asn_label} ({kind}): revived "
            f"({len(retired_links)} link(s) retracted)",
            file=sys.stderr,
        )
        return 0

    if is_retired(session, target_addr):
        print(f"  {asn_label} ({kind}): already retired (no-op)",
              file=sys.stderr)
        return 0
    link, created = emit_retired(session.store, target_addr)
    print(link.addr)
    print(f"  {asn_label} ({kind}): retired", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
