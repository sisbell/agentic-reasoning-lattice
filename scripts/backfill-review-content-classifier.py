#!/usr/bin/env python3
"""One-shot backfill: `review.content` classifier on historical bare-review docs.

Before commit `08873ace` ("fix(note-review): emit review.content,
not bare review classifier"), `note_review` emitted only the bare
`review` parent classifier on its review docs. The predicate
`has_been_reviewed` walks `review.content` specifically, so reviews
filed under the bare-only emission path do not satisfy it — the
trigger's "skip if clean" branch stays dead code for those docs.

This script adds a `review.content` classifier alongside any review
doc that currently carries only the bare `review` parent type
(`type_set == {review}` exactly). The old bare classifier link is
left active; it is a structural fact about what was emitted and when.

Emissions are idempotent via `emit_review_content` — re-runs are safe.

Usage:
    python scripts/backfill-review-content-classifier.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.backend.emit import emit_review_content
from lib.protocols.febe.session import open_session
from lib.shared.paths import LATTICE


def main() -> int:
    with open_session(LATTICE) as session:
        types = session.store.state.types
        review_addr = types.address_for("review")

        # Links carrying only the bare review parent type (no subtype).
        bare_only_links = [
            link for link in session.active_links("review")
            if link.type_set == (review_addr,)
        ]
        if not bare_only_links:
            print("  no bare-only review classifiers found")
            return 0

        emitted = 0
        already = 0
        for link in bare_only_links:
            if not link.to_set:
                continue
            review_doc = link.to_set[0]
            # Skip if review.content already covers this doc.
            existing = session.active_links(
                "review.content", to_set=[review_doc],
            )
            if existing:
                already += 1
                continue
            emit_review_content(session.store, review_doc)
            emitted += 1

        print(
            f"  bare-only review classifiers scanned: {len(bare_only_links)}\n"
            f"  review.content emitted: {emitted}\n"
            f"  already had review.content (idempotent skip): {already}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
