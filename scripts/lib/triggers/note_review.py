"""Note-review trigger — fires when a note's review state is stale.

  scope:     each active non-retired note in scope (one ASN under
             CLI mode, every active note under daemon mode)
  predicate: is_doc_quiescent AND latest_review_was_clean — don't fire
             if there are no open revises and the most recent review
             came up clean. Initial state (no review yet) has
             latest_review_was_clean=False, so the predicate is False
             and review fires once.
  agent:     NoteReviewAgent
"""

from __future__ import annotations

from typing import Iterator

from lib.agents.producers.note_review import NoteReviewAgent
from lib.backend.addressing import Address
from lib.predicates import (
    has_been_reviewed, is_doc_quiescent, is_retired,
    latest_review_was_clean,
)
from lib.protocols.febe.protocol import Session
from lib.runner import Scope, Trigger, asn_note_addr


def _scope_query(session: Session, scope: Scope) -> Iterator[Address]:
    """Yield note addresses to consider this pass.

    CLI mode (scope.asn_label set): the single ASN's note.
    Daemon mode (scope.asn_label is None): every active non-retired note.
    """
    if scope.asn_label is not None:
        addr = asn_note_addr(session, scope)
        if addr is not None:
            yield addr
        return
    for link in session.active_links("note"):
        if not link.to_set:
            continue
        addr = link.to_set[0]
        if not is_retired(session, addr):
            yield addr


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
    scope_query=_scope_query,
    predicate=_predicate,
    agent=NoteReviewAgent(),
)
