"""Note-revise trigger — fires when a note has unresolved revise
comments AND every such finding has been consulted.

  scope:     each active non-retired note (CLI: one ASN's note;
             daemon: every active note)
  predicate: is_doc_quiescent OR not all_open_revises_consulted —
             skip when there's nothing to revise, or when consult
             hasn't yet covered every open revise (wait for
             note-consult to fire first)
  agent:     NoteReviseAgent
"""

from __future__ import annotations

from lib.agents.refiners.note_revise import NoteReviseAgent
from lib.backend.addressing import Address
from lib.predicates import all_open_revises_consulted, is_doc_quiescent
from lib.protocols.febe.protocol import Session
from lib.runner import Trigger
from lib.triggers.scope import per_active_note


def _predicate(session: Session, addr: Address) -> bool:
    """True (skip) iff revise has nothing to do — either no open
    revises, or revise should wait for note-consult to cover them
    first."""
    return (
        is_doc_quiescent(session, addr)
        or not all_open_revises_consulted(session, addr)
    )


note_revise = Trigger(
    name="note-revise",
    scope_query=per_active_note,
    predicate=_predicate,
    agent=NoteReviseAgent(),
)
