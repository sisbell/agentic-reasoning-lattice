#!/usr/bin/env python3
"""One-shot backfill: emit `decomposed` marker on existing claim review docs.

The claim-findings producer's trigger predicate is
`is_decomposed(review_addr)` — skip if the marker is present.
Reviews emitted before the producer was lifted to a runner-driven
trigger have no marker; without backfill, the trigger would re-fire
finding-emit on every historical review and emit duplicate
`comment.<kind>` links per finding.

This script walks every active `review` classifier whose path is
under `_docuverse/documents/review/claims/`, and emits the
`decomposed` marker on each (idempotent — re-emits are no-ops).

Run once after the claim-findings cutover lands. After this commit,
the trigger predicate evaluates True on existing reviews and the
runner skips them.

Usage:
    python scripts/migrate-decomposed-marker.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.backend.emit import emit_decomposed
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
        review_path = session.get_path_for_addr(review_addr)
        if review_path is None:
            continue
        if "/review/claims/" not in review_path:
            continue
        _, created = emit_decomposed(store, review_addr)
        if created:
            marked += 1
            print(f"  [DECOMPOSED] {review_path}", file=sys.stderr)
        else:
            skipped += 1
    print(
        f"\n  marked={marked} already-marked={skipped}",
        file=sys.stderr,
    )
    if marked:
        step_commit(
            f"migrate(substrate): backfill decomposed marker on {marked} reviews",
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
