"""Note-statements trigger — fires on the source note when its
formal-statements sidecar is stale relative to its confirmed state.

  scope:     the source note for the requested ASN
  predicate: statements_is_fresh
  agent:     NoteStatementsAgent

Fires at the +1 boundary of the N+1 convergence pattern: only when
the note has no open revises AND the latest review was clean. During
active revise cycles the predicate stays True (quiescent) — we don't
re-extract on every accept, only when the note has settled.
"""

from __future__ import annotations

from typing import Iterator

from lib.agents.note_statements import NoteStatementsAgent
from lib.backend.addressing import Address
from lib.predicates import statements_is_fresh
from lib.protocols.febe.protocol import Session
from lib.runner import Scope, Trigger, asn_note_addr


def _scope_query(session: Session, scope: Scope) -> Iterator[Address]:
    """Yield the source note address for the requested ASN, if any."""
    addr = asn_note_addr(session, scope)
    if addr is not None:
        yield addr


note_statements = Trigger(
    name="note-statements",
    scope_query=_scope_query,
    predicate=statements_is_fresh,
    agent=NoteStatementsAgent(),
)
