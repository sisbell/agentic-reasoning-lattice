#!/usr/bin/env python3
"""One-shot backfill of cascade anchors for historical note reviews.

The cascade-anchor feature emits a bundled `citation.depends` from each
new review-N doc to the version_head of every foundation when
note_review fires. Pre-feature reviews have no such anchor, so the
`is_note_cascade_fresh` predicate treats them as vacuously fresh —
including notes whose foundations have advanced post-import.

This script backfills: for each note's latest review (or every review
on its supersession chain — see Discussion), emits one bundled
`citation.depends` from the review_addr to the *base* addresses of
every foundation the note declares as a dep. The cascade-fresh
predicate then checks `is_head_version(base)` per target — a base
with version-children (i.e., the foundation has been version-
registered after the note was imported) returns False, re-firing
note_review.

Why bases rather than version_heads:
  - Emitting at version_head would freeze the anchor at "current"
    state, masking any staleness that's already present at script
    runtime. Notes like ASN-0051 — whose foundations have actually
    advanced — would be erroneously marked fresh.
  - Emitting at base correctly detects staleness: `is_head_version`
    returns False whenever a foundation's base has been version-
    registered, which is exactly the condition the feature exists
    to catch.
  - After the first post-backfill re-review fires, the agent emits
    a fresh anchor pointing at the current version_head and the
    normal head-comparison pattern takes over.

Idempotent: skips a review whose outgoing `citation.depends` already
includes every dep target.

Usage:
    python scripts/backfill-cascade-anchors.py            # all notes
    python scripts/backfill-cascade-anchors.py 51         # just ASN-0051
    python scripts/backfill-cascade-anchors.py 51 86 94   # batch
    python scripts/backfill-cascade-anchors.py --dry-run
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.backend.emit import emit_citation_bundle
from lib.lattice.labels import format_label, label_pattern
from lib.predicates import depends, latest_review_for_addr
from lib.protocols.febe.session import open_session
from lib.shared.git_ops import step_commit
from lib.shared.paths import DOCUVERSE_DIR, LATTICE, NOTE_DIR, WORKSPACE


def _is_note_classifier(session, addr):
    return bool(session.active_links("note", to_set=[addr]))


def _iter_active_note_addrs(session, asn_filter=None):
    """Yield (asn_label, note_addr) for each path-registered note."""
    store = session.store
    pattern = label_pattern()
    note_prefix = str(NOTE_DIR.relative_to(WORKSPACE)) + "/"
    for path, addr in store.path_to_addr.items():
        if not path.startswith(note_prefix):
            continue
        if path.endswith(".statements.md"):
            continue
        if not _is_note_classifier(session, addr):
            continue
        m = pattern.search(path)
        if not m:
            continue
        label = m.group(0)
        if asn_filter is not None and label not in asn_filter:
            continue
        yield label, addr


def _existing_anchor_targets(session, review_addr):
    """Set of targets already cited via citation.depends from review_addr."""
    cited = set()
    for link in session.active_links(
        "citation.depends", from_set=[review_addr],
    ):
        cited.update(link.to_set)
    return cited


def backfill(asn_filter=None, dry_run=False):
    """Walk notes, emit cascade anchors for latest reviews. Returns
    (emitted_count, skipped_count, missing_review_count)."""
    emitted = 0
    skipped = 0
    no_review = 0

    with open_session(LATTICE) as session:
        for label, note_addr in _iter_active_note_addrs(
            session, asn_filter=asn_filter,
        ):
            review_addr = latest_review_for_addr(session, note_addr)
            if review_addr is None:
                no_review += 1
                print(
                    f"  [{label}] no review yet — skipping",
                    file=sys.stderr,
                )
                continue

            dep_bases = depends(session, note_addr)
            if not dep_bases:
                skipped += 1
                print(
                    f"  [{label}] no foundation deps — skipping",
                    file=sys.stderr,
                )
                continue

            existing = _existing_anchor_targets(session, review_addr)
            missing = [b for b in dep_bases if b not in existing]
            if not missing:
                skipped += 1
                print(
                    f"  [{label}] anchor already covers all "
                    f"{len(dep_bases)} deps — skipping",
                    file=sys.stderr,
                )
                continue

            print(
                f"  [{label}] backfilling anchor on latest review "
                f"({len(missing)}/{len(dep_bases)} targets missing)",
                file=sys.stderr,
            )
            emitted += 1
            if dry_run:
                continue

            emit_citation_bundle(
                session.store, review_addr, missing,
                direction="depends",
            )

    return emitted, skipped, no_review


def _stage_for_commit():
    paths = [
        str((DOCUVERSE_DIR / "links.jsonl").resolve().relative_to(
            WORKSPACE.resolve())),
        str((DOCUVERSE_DIR / "paths.json").resolve().relative_to(
            WORKSPACE.resolve())),
    ]
    subprocess.run(
        ["git", "add"] + paths,
        cwd=str(WORKSPACE), capture_output=True, text=True,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "asn", nargs="*", type=int,
        help="Optional ASN numbers to restrict the backfill to "
             "(e.g., 51 86 94). Default: all notes.",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show which notes would be backfilled without writing.",
    )
    parser.add_argument(
        "--no-commit", action="store_true",
        help="Skip the post-backfill commit step.",
    )
    args = parser.parse_args()

    asn_filter = None
    if args.asn:
        asn_filter = {format_label(n) for n in args.asn}

    emitted, skipped, no_review = backfill(
        asn_filter=asn_filter, dry_run=args.dry_run,
    )
    print(
        f"\n  backfill: emitted={emitted}, skipped={skipped}, "
        f"no-review={no_review}",
        file=sys.stderr,
    )

    if emitted and not args.dry_run and not args.no_commit:
        _stage_for_commit()
        step_commit(
            f"backfill(cascade-anchors): emit citation.depends from "
            f"latest reviews to foundation bases ({emitted} notes)"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
