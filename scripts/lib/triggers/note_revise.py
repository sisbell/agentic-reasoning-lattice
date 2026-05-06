"""Note-revise trigger — fires when a note has unresolved revise
comments AND every such finding has been consulted.

  scope:     each active non-retired note in scope (CLI: one ASN's note;
             daemon: every active note)
  predicate: is_doc_quiescent OR not all_open_revises_consulted —
             don't fire if there's nothing to do, and don't fire
             until note-consult has produced consultation.coverage
             links for every open revise.
  agent:     NoteReviseAgent
"""

from __future__ import annotations

from typing import Iterator

from lib.agents.note_revise import NoteReviseAgent
from lib.backend.addressing import Address
from lib.predicates import (
    all_open_revises_consulted, is_doc_quiescent, is_retired,
)
from lib.protocols.febe.protocol import Session
from lib.runner import Scope, Trigger, asn_note_addr


def _scope_query(session: Session, scope: Scope) -> Iterator[Address]:
    """Yield note addresses to consider this pass.

    CLI mode: the single ASN's note. Daemon mode: every active
    non-retired note.
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
    """True iff revise has nothing to do — either no open revises, or
    revise should wait for note-consult to cover them first."""
    return (
        is_doc_quiescent(session, addr)
        or not all_open_revises_consulted(session, addr)
    )


note_revise = Trigger(
    name="note-revise",
    scope_query=_scope_query,
    predicate=_predicate,
    agent=NoteReviseAgent(),
)
