#!/usr/bin/env python3
"""One-shot backfill: emit `synthesis` links for already-drafted notes.

The consultation protocol records inquiry-to-note provenance via a
`synthesis` substrate link from the inquiry md to its drafted note md
(per docs/protocols/consultation-protocol.md §6.4 and C7). For new
inquiries this is wired in note-draft.py; existing 27 inquiries pre-date
the wiring and have no synthesis link.

This script walks every inquiry doc, resolves its drafted note, and
emits a `synthesis` link. Idempotent — re-runs are no-ops.

Run AFTER backfill-note-classifiers.py so notes have substrate
classifiers (the link target paths are the note md paths regardless,
but checking that the note exists on disk is enough).

Usage:
    python3 scripts/backfill-synthesis-links.py
    python3 scripts/backfill-synthesis-links.py --apply
    LATTICE=materials python3 scripts/backfill-synthesis-links.py --apply
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from shared.paths import INQUIRY_DIR, NOTES_DIR, WORKSPACE
from store.emit import emit_synthesis
from store.store import Store


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    grp = ap.add_mutually_exclusive_group()
    grp.add_argument("--apply", action="store_true",
                     help="emit synthesis links (default is dry-run)")
    grp.add_argument("--dry-run", action="store_true", default=True)
    args = ap.parse_args()
    apply_mode = args.apply

    label = "APPLY" if apply_mode else "DRY-RUN"
    print(f"[backfill-synthesis-links] {label}")
    print(f"  INQUIRY_DIR = {INQUIRY_DIR.relative_to(WORKSPACE)}")
    print(f"  NOTES_DIR     = {NOTES_DIR.relative_to(WORKSPACE)}")
    print()

    if not INQUIRY_DIR.exists():
        print(f"  no INQUIRY_DIR at {INQUIRY_DIR}", file=sys.stderr)
        return 1

    inquiries = sorted(INQUIRY_DIR.glob("ASN-*.md"))
    print(f"  Found {len(inquiries)} inquiry doc(s)")
    print()

    plan = []  # (asn_label, inquiry_path, note_path)
    for inq in inquiries:
        m = re.match(r"(ASN-\d+)", inq.stem)
        if not m:
            continue
        asn_label = m.group(1)
        candidates = sorted(NOTES_DIR.glob(f"{asn_label}-*.md"))
        if not candidates:
            print(f"  ! {asn_label} inquiry has no drafted note — skipping",
                  file=sys.stderr)
            continue
        if len(candidates) > 1:
            print(f"  ! {asn_label} has {len(candidates)} candidate notes — "
                  f"taking first ({candidates[0].name})",
                  file=sys.stderr)
        plan.append((asn_label, inq, candidates[0]))

    print(f"  Planned ({len(plan)} link(s)):")
    for asn_label, inq, note in plan[:5]:
        print(f"    {asn_label}: {inq.name} → {note.name}")
    if len(plan) > 5:
        print(f"    ... and {len(plan) - 5} more")
    print()

    if not apply_mode:
        print("  (dry-run; no changes made. Use --apply to backfill.)")
        return 0

    created_count = 0
    skipped_count = 0
    with Store() as store:
        for asn_label, inq, note in plan:
            _, created = emit_synthesis(store, inq, note)
            if created:
                created_count += 1
            else:
                skipped_count += 1

    print(f"  emitted:    {created_count} new synthesis link(s)")
    print(f"  idempotent: {skipped_count} already-present link(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
