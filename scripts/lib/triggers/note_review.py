"""Note-review trigger — fires when a note's review state is stale.

  scope:     each active non-retired note (CLI: one ASN's note;
             daemon: every active note)
  predicate: is_doc_quiescent AND has_been_reviewed AND
             last_n_reviews_were_clean(n=2) — don't fire if there
             are no open revises and the most recent TWO reviews
             came up clean. Initial state (no review yet) has
             has_been_reviewed=False, so the predicate is False and
             review fires once.
  agent:     NoteReviewAgent
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from lib.agents.producers.note_review import NoteReviewAgent
from lib.backend.addressing import Address
from lib.lattice.labels import format_label, label_pattern
from lib.predicates import (
    has_been_reviewed, is_doc_quiescent, is_note_cascade_fresh,
    last_n_reviews_were_clean,
)
from lib.protocols.febe.protocol import Session
from lib.runner import Trigger
from lib.shared.paths import NOTE_FINDINGS_DIR, NOTE_REVIEWS_DIR, WORKSPACE
from lib.triggers.scope import per_active_note


NOTE_REVIEW_CONVERGENCE_DEPTH = 2


def _max_reviews_cap() -> int | None:
    """Read MAX_REVIEWS env var (operator-set bound on review count
    per note). Returns int cap or None for "no cap" (default).

    The cap is a target: once a note's active content-review count
    reaches the cap, the predicate skips firing. Operator workflow is
    "set MAX_REVIEWS, run, inspect, bump MAX_REVIEWS, re-run."

    Raises SystemExit on bad config (non-numeric or negative) — loud
    failure is preferable to silent default since the cap is operator
    intent and a typo would silently disable bounding.
    """
    raw = os.environ.get("MAX_REVIEWS", "").strip()
    if not raw:
        return None
    try:
        cap = int(raw)
    except ValueError:
        print(
            f"  [note_review] MAX_REVIEWS={raw!r} is not numeric",
            file=sys.stderr,
        )
        raise SystemExit(1)
    if cap < 0:
        print(
            f"  [note_review] MAX_REVIEWS={raw} must be >= 0",
            file=sys.stderr,
        )
        raise SystemExit(1)
    return cap


def _count_content_reviews(session: Session, note_addr: Address) -> int:
    """Count active content-review docs covering note_addr.

    Mirrors `last_n_reviews_were_clean`'s counting: walks
    `review.coverage` links targeting the note, keeps only those whose
    source review carries the `review.content` classifier (excludes
    structural-only reviews).
    """
    n = 0
    for link in session.active_links("review.coverage", to_set=[note_addr]):
        if not link.from_set:
            continue
        if session.active_links("review.content", to_set=[link.from_set[0]]):
            n += 1
    return n


def _predicate(session: Session, addr: Address) -> bool:
    """True (skip) iff there's nothing for review to do *now*.

    Four skip conditions:

      - MAX_REVIEWS env-var cap reached. Operator-set target; when
        the note has already received MAX_REVIEWS content-reviews,
        no more fire. Bumping MAX_REVIEWS and restarting the runner
        re-opens the gate.
      - Open revises pending. The previous review's findings haven't
        been resolved yet — note_revise is the trigger that should
        run, not another review on the same unrevised text. Without
        this clause, note_review would re-fire each runner pass
        while revises pile up, producing redundant findings on the
        same prose.
      - The last N reviews were all clean AND the cascade anchor on
        the latest review still points at head versions of every
        cited foundation. Per `docs/design-notes/stochastic-quiescence.md`,
        single CONVERGED is a statistically unstable gate for a
        stochastic LLM reviewer — the empirical note-scope threshold
        is two consecutive CONVERGED draws. The cascade-fresh check
        re-opens the skip when any upstream foundation has advanced
        since the last review's anchor was emitted; this is how
        dependency-change detection re-fires review/revise on stale
        notes.

    Fire iff under-cap AND doc is quiescent AND (fewer than N
    consecutive reviews came up clean OR an upstream foundation has
    advanced since the latest review's cascade anchor).
    """
    cap = _max_reviews_cap()
    if cap is not None and _count_content_reviews(session, addr) >= cap:
        return True

    return (
        not is_doc_quiescent(session, addr)
        or (
            has_been_reviewed(session, addr)
            and last_n_reviews_were_clean(
                session, addr, n=NOTE_REVIEW_CONVERGENCE_DEPTH,
            )
            and is_note_cascade_fresh(session, addr)
        )
    )


def _asn_label_for_note(session: Session, note_addr: Address) -> str | None:
    """Extract ASN label from a note's registered path. None if unresolvable."""
    path = session.get_path_for_addr(note_addr)
    if not path:
        return None
    m = label_pattern().search(path)
    return m.group(0) if m else None


def _commit_paths(session: Session, note_addr: Address) -> list[str]:
    """The review + finding directories this fire owns for the target note.

    note_review emits one review-N.md and zero or more finding docs under
    review-N/, both keyed by the target ASN.
    """
    asn_label = _asn_label_for_note(session, note_addr)
    if asn_label is None:
        return []
    return [
        str((NOTE_REVIEWS_DIR / asn_label).relative_to(WORKSPACE)),
        str((NOTE_FINDINGS_DIR / asn_label).relative_to(WORKSPACE)),
    ]


note_review = Trigger(
    name="note-review",
    scope_query=per_active_note,
    predicate=_predicate,
    agent=NoteReviewAgent(),
    commit_paths=_commit_paths,
)
