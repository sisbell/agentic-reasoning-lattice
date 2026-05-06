#!/usr/bin/env python3
"""One-shot backfill: emit `review.content` classifier on existing review docs.

Adds the `review.content` subtype classifier alongside every active
bare `review` classifier in the lattice. Bare `review` stays in
place — predicates can be migrated to `review.content` after this
backfill lands. Eventually bare `review` retires, but that's a
separate cleanup.

Why: with `review.coverage` shared between content reviews
(claim_review producer) and structural audits (claim_structural_audit
scout), predicates need a way to filter by analysis kind. The
review.content / review.structural subtypes provide that
distinguisher. After this backfill, every existing review doc
carries the content-review classifier; new emits already do (per
the producer change in lib/lattice/findings.py).

Usage:
    python scripts/migrate-review-content.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.backend.emit import emit_review_content
from lib.protocols.febe.session import open_session
from lib.shared.git_ops import step_commit
from lib.shared.paths import LATTICE


def main() -> int:
    session = open_session(LATTICE)
    store = session.store
    marked = 0
    skipped = 0
    for link in session.active_links("review"):
        if not link.to_set:
            continue
        review_addr = link.to_set[0]
        # Skip if this is itself review.content (parent-type query
        # matches subtypes too).
        review_path = session.get_path_for_addr(review_addr)
        if review_path is None:
            continue
        existing = session.active_links(
            "review.content", to_set=[review_addr],
        )
        if existing:
            skipped += 1
            continue
        emit_review_content(store, review_addr)
        marked += 1
        print(f"  [REVIEW.CONTENT] {review_path}", file=sys.stderr)
    print(
        f"\n  marked={marked} already-marked={skipped}",
        file=sys.stderr,
    )
    if marked:
        step_commit(
            f"migrate(substrate): backfill review.content on {marked} review docs",
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
