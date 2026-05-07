"""Note-draft trigger — fires when an inquiry has consultation done
but no note synthesized yet.

  scope:     each active inquiry in scope (CLI: one ASN's inquiry;
             daemon: every active inquiry)
  predicate: has_note_for_inquiry OR not has_consultation_for_inquiry —
             fire only when consult is done AND no note exists
  agent:     NoteDraftAgent
"""

from __future__ import annotations

from lib.agents.producers.note_draft import NoteDraftAgent
from lib.backend.addressing import Address
from lib.predicates import (
    has_consultation_for_inquiry, has_note_for_inquiry,
)
from lib.protocols.febe.protocol import Session
from lib.runner import Trigger
from lib.triggers.scope import per_inquiry_of_asn


def _predicate(session: Session, addr: Address) -> bool:
    """True (skip) iff draft has nothing to do — either consult hasn't
    run yet (wait for inquiry-consult) or the note already exists."""
    return (
        not has_consultation_for_inquiry(session, addr)
        or has_note_for_inquiry(session, addr)
    )


note_draft = Trigger(
    name="note-draft",
    scope_query=per_inquiry_of_asn,
    predicate=_predicate,
    agent=NoteDraftAgent(),
)
