"""Note-draft trigger — fires when an inquiry has consultation done
but no note synthesized yet.

  scope:     each active inquiry in scope (CLI: one ASN's inquiry;
             daemon: every active inquiry)
  predicate: has_note_for_inquiry OR not has_consultation_for_inquiry —
             fire only when consult is done AND no note exists
  agent:     NoteDraftAgent
"""

from __future__ import annotations

from typing import Iterator

from lib.agents.note_draft import NoteDraftAgent
from lib.backend.addressing import Address
from lib.predicates import (
    has_consultation_for_inquiry, has_note_for_inquiry,
)
from lib.protocols.febe.protocol import Session
from lib.runner import Scope, Trigger
from lib.shared.paths import LATTICE, inquiry_doc_path


def _scope_query(session: Session, scope: Scope) -> Iterator[Address]:
    """Yield inquiry doc addresses to consider this pass."""
    if scope.asn_label is not None:
        asn_num = int(scope.asn_label[4:])
        path = inquiry_doc_path(asn_num)
        if not path.exists():
            return
        rel = str(path.resolve().relative_to(LATTICE.resolve()))
        addr = session.get_addr_for_path(rel)
        if addr is not None:
            yield addr
        return
    for link in session.active_links("inquiry"):
        if link.to_set:
            yield link.to_set[0]


def _predicate(session: Session, addr: Address) -> bool:
    """True iff draft has nothing to do — either consult hasn't run
    yet (wait for inquiry-consult) or the note already exists."""
    return (
        not has_consultation_for_inquiry(session, addr)
        or has_note_for_inquiry(session, addr)
    )


note_draft = Trigger(
    name="note-draft",
    scope_query=_scope_query,
    predicate=_predicate,
    agent=NoteDraftAgent(),
)
