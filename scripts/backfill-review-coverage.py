#!/usr/bin/env python3
"""One-shot backfill of `review.coverage` for historical reviews.

The `covered_addrs` parameter was introduced to `emit_review_doc` on
2026-05-06. Reviews emitted before that landed have no
`review.coverage` links recording which docs they cover — a systemic
data gap the lattice-doctor's `review-coverage-completeness` check
surfaces.

This script reconstructs coverage where possible by walking the
substrate's existing structure:

    review --provenance.derivation--> finding --comment.<kind>--> claim

The union of every finding's comment target gives the set of claims
the review touched (at least, those that produced findings).
Emissions are idempotent on `(review, covered)` so re-runs are
safe.

Limitations:
  - A review that produced ZERO findings has no derivation→finding
    chain to walk. Such reviews stay uncovered after this backfill.
    They represent clean reviews; the only way to recover their
    intended coverage is to re-fire the reviewer.
  - A review whose findings have been retracted contributes nothing
    (active_links filter).

Usage:
    python scripts/backfill-review-coverage.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.backend.emit import emit_review_coverage
from lib.protocols.febe.session import open_session
from lib.shared.paths import LATTICE


_COMMENT_SUBTYPES = (
    "comment.observe",
    "comment.revise",
    "comment.out-of-scope",
    "comment.violation",
)


def main() -> int:
    with open_session(LATTICE) as session:
        store = session.store

        review_addrs = set()
        for classifier in ("review.content", "review.structural"):
            for link in session.active_links(classifier):
                if link.to_set:
                    review_addrs.add(link.to_set[0])

        if not review_addrs:
            print("  no review docs found")
            return 0

        emitted = 0
        already = 0
        no_findings = 0

        for review in sorted(review_addrs, key=lambda a: a.digits):
            existing_cov = {
                target
                for link in session.active_links(
                    "review.coverage", from_set=[review],
                )
                for target in link.to_set
            }

            findings = []
            for link in session.active_links(
                "provenance.derivation", from_set=[review],
            ):
                findings.extend(link.to_set)

            covered_claims = set()
            for finding in findings:
                for subtype in _COMMENT_SUBTYPES:
                    for link in session.active_links(
                        subtype, from_set=[finding],
                    ):
                        for target in link.to_set:
                            covered_claims.add(target)

            if not covered_claims:
                no_findings += 1
                continue

            for claim in covered_claims:
                if claim in existing_cov:
                    already += 1
                    continue
                emit_review_coverage(store, review, claim)
                emitted += 1

        print(
            f"  reviews scanned: {len(review_addrs)}\n"
            f"  coverage emitted: {emitted}\n"
            f"  already covered (idempotent skip): {already}\n"
            f"  no inferable coverage (zero findings): {no_findings}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
