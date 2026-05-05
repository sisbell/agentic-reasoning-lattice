#!/usr/bin/env python3
"""
Clone an ASN under a new ASN number.

Used when an existing ASN already has expensive consultation work
attached and you want to tweak it without disturbing the original.
The source remains unchanged; the clone is fully independent
afterward, with a `provenance.clone` audit edge from origin → clone.

Usage:
    python scripts/note-clone.py --source 48 --target 59
    python scripts/note-clone.py -s 48 -t 59 --dry-run
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.maturation.clone import (
    validate, copy_note_md, copy_inquiry_doc, copy_consultations,
    emit_substrate_facts,
)
from lib.protocols.febe.session import open_session
from lib.shared.git_ops import step_commit
from lib.shared.paths import LATTICE


def main():
    parser = argparse.ArgumentParser(
        description="Clone an ASN under a new ASN number.")
    parser.add_argument("-s", "--source", type=int, required=True,
                        help="Source ASN number to clone")
    parser.add_argument("-t", "--target", type=int, required=True,
                        help="New ASN number for the clone")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would happen without doing it")
    args = parser.parse_args()

    source_label, target_label = validate(args.source, args.target)

    print(f"  [CLONE] {source_label} → {target_label}", file=sys.stderr)

    if args.dry_run:
        print(f"  [DRY RUN] Would copy note md, inquiry doc, "
              f"consultations, citations + emit provenance.clone",
              file=sys.stderr)
        return

    target_note = copy_note_md(
        args.source, args.target, source_label, target_label,
    )
    target_inquiry = copy_inquiry_doc(
        args.source, args.target, source_label, target_label,
    )
    copy_consultations(source_label, target_label)

    from lib.shared.common import find_asn
    source_note, _ = find_asn(str(args.source))
    from lib.shared.paths import inquiry_doc_path
    source_inquiry = inquiry_doc_path(args.source)
    if not source_inquiry.exists():
        source_inquiry = None
        target_inquiry = None

    with open_session(LATTICE) as session:
        emit_substrate_facts(
            session,
            source_note_path=source_note,
            target_note_path=target_note,
            source_inquiry_path=source_inquiry,
            target_inquiry_path=target_inquiry,
        )
    print(f"  [LINEAGE] provenance.clone {source_label} → {target_label}",
          file=sys.stderr)

    step_commit(f"clone(asn): {source_label} → {target_label}")


if __name__ == "__main__":
    main()
