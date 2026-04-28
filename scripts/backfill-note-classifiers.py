#!/usr/bin/env python3
"""One-shot backfill: emit `note` classifier for every existing note doc.

Notes drafted before draft.py started emitting `note` classifiers are
present on disk but absent from the substrate's note classifier index.
This script walks NOTES_DIR and calls emit_note on each ASN-NNNN-*.md
file. Idempotent — re-running is a no-op (emit_note returns the existing
classifier id).

Usage:
    python3 scripts/backfill-note-classifiers.py --apply
    python3 scripts/backfill-note-classifiers.py --dry-run  (default)
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from shared.paths import NOTES_DIR, WORKSPACE
from store.emit import emit_note
from store.store import Store


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    grp = ap.add_mutually_exclusive_group()
    grp.add_argument("--apply", action="store_true",
                     help="emit classifiers (default is dry-run)")
    grp.add_argument("--dry-run", action="store_true", default=True)
    args = ap.parse_args()
    apply_mode = args.apply

    label = "APPLY" if apply_mode else "DRY-RUN"
    print(f"[backfill-note-classifiers] {label}")
    print(f"  NOTES_DIR = {NOTES_DIR.relative_to(WORKSPACE)}")
    print()

    if not NOTES_DIR.exists():
        print(f"  no NOTES_DIR found at {NOTES_DIR}", file=sys.stderr)
        return 1

    notes = sorted(NOTES_DIR.glob("ASN-*.md"))
    print(f"  Found {len(notes)} note files")
    print()

    if not apply_mode:
        for n in notes[:5]:
            print(f"    {n.name}")
        if len(notes) > 5:
            print(f"    ... and {len(notes) - 5} more")
        print()
        print("  (dry-run; no changes made. Use --apply to backfill.)")
        return 0

    created_count = 0
    skipped_count = 0
    with Store() as store:
        for note_path in notes:
            _, created = emit_note(store, note_path)
            if created:
                created_count += 1
            else:
                skipped_count += 1

    print(f"  emitted:    {created_count} new classifiers")
    print(f"  idempotent: {skipped_count} already-classified notes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
