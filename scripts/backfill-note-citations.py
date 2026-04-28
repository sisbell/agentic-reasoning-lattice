#!/usr/bin/env python3
"""One-shot backfill: emit substrate citation links from manifest depends:.

Each note manifest has a `depends:` field listing ASN ids the note
depends on (e.g., `depends: [34, 36, 47]`). Pre-substrate, this field
was the canonical citation graph. Post-substrate, the graph lives in
`citation` links between note md docs.

This script walks every note manifest, looks up the from-note via the
substrate `note` classifier, looks up each declared dep via the same
classifier index, and emits a citation link from from-note to dep-note.
Idempotent — re-running on a populated graph is a no-op.

Run this AFTER backfill-note-classifiers.py (which establishes the
note classifier index this script reads).

Usage:
    python3 scripts/backfill-note-citations.py --apply
    python3 scripts/backfill-note-citations.py --dry-run  (default)
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from shared.paths import MANIFESTS_DIR, WORKSPACE, load_manifest
from store.cite import emit_citation
from store.populate import build_note_label_index
from store.store import Store


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    grp = ap.add_mutually_exclusive_group()
    grp.add_argument("--apply", action="store_true",
                     help="emit citations (default is dry-run)")
    grp.add_argument("--dry-run", action="store_true", default=True)
    args = ap.parse_args()
    apply_mode = args.apply

    label = "APPLY" if apply_mode else "DRY-RUN"
    print(f"[backfill-note-citations] {label}")
    print(f"  MANIFESTS_DIR = {MANIFESTS_DIR.relative_to(WORKSPACE)}")
    print()

    if not MANIFESTS_DIR.exists():
        print(f"  no MANIFESTS_DIR found at {MANIFESTS_DIR}", file=sys.stderr)
        return 1

    manifests = sorted(MANIFESTS_DIR.glob("ASN-*/note.yaml"))
    print(f"  Found {len(manifests)} manifest(s)")
    print()

    store = Store()
    note_index = build_note_label_index(store)
    if not note_index:
        print("  no `note` classifier links in substrate — "
              "run backfill-note-classifiers.py first", file=sys.stderr)
        store.close()
        return 1

    plan = []
    for path in manifests:
        from_label = path.parent.name  # ASN-NNNN
        if from_label not in note_index:
            print(f"  ! {from_label} has no note classifier — skipping",
                  file=sys.stderr)
            continue
        from_path = note_index[from_label]
        asn_id = int(from_label.split("-")[1])
        manifest = load_manifest(asn_id)
        depends = manifest.get("depends", []) or []
        for dep_id in depends:
            dep_label = f"ASN-{int(dep_id):04d}"
            if dep_label not in note_index:
                print(f"  ! {from_label} depends on {dep_label} but it has "
                      f"no note classifier — skipping",
                      file=sys.stderr)
                continue
            plan.append((from_path, from_label, dep_label))

    print(f"  Planned: {len(plan)} citation(s) across {len(manifests)} manifest(s)")
    print()
    if not apply_mode:
        for fp, fl, dl in plan[:10]:
            print(f"    {fl} → {dl}")
        if len(plan) > 10:
            print(f"    ... and {len(plan) - 10} more")
        print()
        print("  (dry-run; no changes made. Use --apply to backfill.)")
        store.close()
        return 0

    created_count = 0
    skipped_count = 0
    for from_path, from_label, dep_label in plan:
        try:
            _, created = emit_citation(store, from_path, dep_label, note_index)
        except KeyError as e:
            print(f"  ! {from_label} → {dep_label} failed: {e}",
                  file=sys.stderr)
            continue
        if created:
            created_count += 1
        else:
            skipped_count += 1
    store.close()

    print(f"  emitted:    {created_count} new citations")
    print(f"  idempotent: {skipped_count} already-present citations")
    return 0


if __name__ == "__main__":
    sys.exit(main())
