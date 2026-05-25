#!/usr/bin/env python3
"""One-shot backfill of cascade anchors for historical note reviews.

The cascade-anchor feature emits a bundled `citation.depends` from each
new review-N doc to the version_head of every foundation when
note_review fires. Pre-feature reviews have no such anchor, so the
`is_note_cascade_fresh` predicate treats them as vacuously fresh.

The substrate does not preserve "what was head when this review
emitted" for legacy data (cross-allocator address comparison is not
structural; timestamp comparison is against the freshness discipline).
So this backfill takes operator-supplied knowledge as the source of
truth via the `--target` flag:

  --target=version-head (default)
      Anchor at each foundation's current `version_head`. Operator
      affirms "this review is valid against current foundation state."
      Predicate stays fresh until a foundation advances post-backfill;
      future advances correctly trigger re-review. Use for ASNs you
      know are currently up-to-date.

  --target=base
      Anchor at each foundation's base address. `is_head_version(base)`
      returns False for any foundation that has been version-registered,
      so the predicate immediately flags the note for re-review. Use
      for ASNs you know need to be re-reviewed under current foundation
      state.

Idempotent: skips a review whose outgoing `citation.depends` already
includes every dep target.

Usage:
    # ASNs operator affirms as up-to-date — anchor at current heads:
    python scripts/backfill-cascade-anchors.py 36 40 42 43 ...

    # ASNs operator knows need re-review — anchor at bases:
    python scripts/backfill-cascade-anchors.py 51 86 --target=base

    python scripts/backfill-cascade-anchors.py 51 --dry-run --target=base
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.backend.emit import emit_citation_bundle
from lib.lattice.labels import format_label, label_pattern
from lib.predicates import latest_review_for_addr, version_head
from lib.protocols.febe.session import open_session
from lib.shared.foundation import FoundationError, foundation_dep_addrs
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


def _resolve_targets(session, dep_bases, target_mode):
    """Map foundation bases to the anchor targets per --target mode."""
    if target_mode == "version-head":
        return [version_head(session, b) for b in dep_bases]
    return list(dep_bases)


def backfill(asn_filter=None, dry_run=False, target_mode="version-head"):
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

            # Canonical dep lookup (inquiry-primary + LEGACY fallback)
            # via foundation_dep_addrs. Querying citation.depends from
            # note_addr would silently return empty for HEALTHY ASNs.
            asn_num = int(label.split("-")[1])
            try:
                dep_bases = foundation_dep_addrs(session, asn_num)
            except FoundationError as e:
                skipped += 1
                print(
                    f"  [{label}] foundation deps unresolvable — "
                    f"skipping ({e})",
                    file=sys.stderr,
                )
                continue
            if not dep_bases:
                skipped += 1
                print(
                    f"  [{label}] no foundation deps — skipping",
                    file=sys.stderr,
                )
                continue

            targets = _resolve_targets(session, dep_bases, target_mode)
            existing = _existing_anchor_targets(session, review_addr)
            missing = [t for t in targets if t not in existing]
            if not missing:
                skipped += 1
                print(
                    f"  [{label}] anchor already covers all "
                    f"{len(targets)} deps — skipping",
                    file=sys.stderr,
                )
                continue

            print(
                f"  [{label}] backfilling anchor on latest review "
                f"({len(missing)}/{len(targets)} targets, "
                f"mode={target_mode})",
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
        "--target", choices=("version-head", "base"),
        default="version-head",
        help="Anchor target. version-head (default) snapshots current "
             "head per dep — use for ASNs operator affirms as up-to-date. "
             "base anchors at foundation base — predicate flags any "
             "foundation that has been version-registered, forcing "
             "re-review. Use for ASNs known to need re-review.",
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
        target_mode=args.target,
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
            f"latest reviews to foundation {args.target} "
            f"({emitted} notes)"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
