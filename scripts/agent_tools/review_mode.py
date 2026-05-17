#!/usr/bin/env python3
"""Operator CLI: apply or retract the `review-mode.anti-bloat` classifier
on a note.

When the classifier is present, `NoteReviewAgent` appends the
forward-reference accretion patterns from
`prompts/shared/agents/producers/note_review_anti_bloat.md` to the
standard note-review prompt for that note. Operator-driven on/off:

    # Tag a note for anti-bloat-augmented review
    python scripts/agent_tools/review_mode.py --asn 47 --apply

    # Remove the tag (return note to standard review)
    python scripts/agent_tools/review_mode.py --asn 47 --retract

    # Check status
    python scripts/agent_tools/review_mode.py --asn 47

Tag lifecycle is binary (off default, on explicit). State transitions
are real substrate facts (emit classifier = apply; emit retraction =
retract); no toggling.

Exits non-zero if the target ASN has no note in the substrate.
"""

import argparse
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.backend.emit import emit_retraction, emit_review_mode_anti_bloat
from lib.lattice.labels import format_label
from lib.protocols.febe.session import open_session
from lib.shared.common import find_asn
from lib.shared.paths import LATTICE, WORKSPACE


def _resolve_note_addr(session, asn_num):
    """Return the note's substrate address, or None if no note registered."""
    asn_path, _ = find_asn(str(asn_num))
    if asn_path is None:
        return None
    note_rel = str(asn_path.relative_to(WORKSPACE))
    return session.get_addr_for_path(note_rel)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--asn", required=True, type=int,
        help="ASN number to tag (e.g., 47).",
    )
    action = parser.add_mutually_exclusive_group()
    action.add_argument(
        "--apply", action="store_true",
        help="Apply the review-mode.anti-bloat classifier.",
    )
    action.add_argument(
        "--retract", action="store_true",
        help="Retract the active review-mode.anti-bloat classifier.",
    )
    args = parser.parse_args()

    asn_label = format_label(args.asn)
    session = open_session(LATTICE)
    note_addr = _resolve_note_addr(session, args.asn)
    if note_addr is None:
        print(
            f"error: no note registered for {asn_label}",
            file=sys.stderr,
        )
        return 1

    active = session.active_links(
        "review-mode.anti-bloat", to_set=[note_addr],
    )

    if args.retract:
        if not active:
            print(
                f"  {asn_label}: not tagged (no-op)",
                file=sys.stderr,
            )
            return 0
        for link in active:
            emit_retraction(session.store, note_addr, link.addr)
        print(
            f"  {asn_label}: anti-bloat tag retracted "
            f"({len(active)} link(s))",
            file=sys.stderr,
        )
        return 0

    if args.apply:
        if active:
            print(
                f"  {asn_label}: already tagged (no-op)",
                file=sys.stderr,
            )
            return 0
        link, _ = emit_review_mode_anti_bloat(session.store, note_addr)
        print(link.addr)
        print(
            f"  {asn_label}: anti-bloat tag applied",
            file=sys.stderr,
        )
        return 0

    # No action — report status
    if active:
        print(f"  {asn_label}: tagged (anti-bloat review mode)")
        for link in active:
            print(f"    link: {link.addr}")
    else:
        print(f"  {asn_label}: not tagged (standard review mode)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
