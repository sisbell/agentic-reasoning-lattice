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
    """True iff review is satisfied — predicate matches the +1
    confirmation pattern. Don't fire if no open revises remain AND
    the most recent review filed zero new revises.
    """
    return (
        is_doc_quiescent(session, addr)
        and has_been_reviewed(session, addr)
        and latest_review_was_clean(session, addr)
    )


note_review = Trigger(
    name="note-review",
    scope_query=per_active_note,
    predicate=_predicate,
    agent=NoteReviewAgent(),
)
