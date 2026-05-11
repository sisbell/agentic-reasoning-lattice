"""Note-review trigger — fires when a note's review state is stale.

  scope:     each active non-retired note (CLI: one ASN's note;
             daemon: every active note)
  predicate: is_doc_quiescent AND has_been_reviewed AND
             latest_review_was_clean — don't fire if there are no
             open revises and the most recent review came up clean.
             Initial state (no review yet) has has_been_reviewed=False,
             so the predicate is False and review fires once.
  agent:     NoteReviewAgent
"""

from __future__ import annotations

from lib.agents.producers.note_review import NoteReviewAgent
from lib.backend.addressing import Address
from lib.predicates import (
    has_been_reviewed, is_doc_quiescent, latest_review_was_clean,
)
from lib.protocols.febe.protocol import Session
from lib.runner import Trigger
from lib.triggers.scope import per_active_note


def _predicate(session: Session, addr: Address) -> bool:
    """True (skip) iff there's nothing for review to do *now*.

    Two skip conditions:

      - Open revises pending. The previous review's findings haven't
        been resolved yet — note_revise is the trigger that should
        run, not another review on the same unrevised text. Without
        this clause, note_review would re-fire each runner pass
        while revises pile up, producing redundant findings on the
        same prose.
      - Latest review was clean (and any review has happened). The
        confirmation +1 pattern: a clean review on the current state
        ends the review→revise cycle.

    Fire iff doc is quiescent AND latest review was not clean (or no
    review yet exists).
    """
    return (
        not is_doc_quiescent(session, addr)
        or (
            has_been_reviewed(session, addr)
            and latest_review_was_clean(session, addr)
        )
    )


note_review = Trigger(
    name="note-review",
    scope_query=per_active_note,
    predicate=_predicate,
    agent=NoteReviewAgent(),
)
