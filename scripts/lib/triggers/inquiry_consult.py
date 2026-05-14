"""Inquiry-consult trigger — fires only at the pre-draft stage.

  scope:     each active inquiry in scope (CLI: one ASN's inquiry;
             daemon: every active inquiry)
  predicate: skip if a note already exists for the inquiry (stage
             has advanced past discovery), or if consultation answers
             already cover the inquiry. Fire only when no draft and
             no answers yet.
  agent:     InquiryConsultAgent
"""

from __future__ import annotations

from lib.agents.producers.inquiry_consult import InquiryConsultAgent
from lib.backend.addressing import Address
from lib.lattice.labels import label_pattern
from lib.predicates import (
    has_consultation_for_inquiry, has_note_for_inquiry,
)
from lib.protocols.febe.protocol import Session
from lib.runner import Trigger
from lib.shared.paths import CONSULTATIONS_DIR, WORKSPACE
from lib.triggers.scope import per_inquiry_of_asn


def _predicate(session: Session, addr: Address) -> bool:
    """Skip iff stage has advanced past inquiry consultation:

      - A note draft already exists for this inquiry (hard stage gate
        — going back to inquiry consultation post-draft is wrong).
      - Or consultation answers already cover this inquiry.
    """
    return (
        has_note_for_inquiry(session, addr)
        or has_consultation_for_inquiry(session, addr)
    )


def _commit_paths(session: Session, inquiry_addr: Address) -> list[str]:
    """Consultation subtree for the inquiry's ASN."""
    path = session.get_path_for_addr(inquiry_addr)
    if not path:
        return []
    m = label_pattern().search(path)
    if not m:
        return []
    return [str((CONSULTATIONS_DIR / m.group(0)).relative_to(WORKSPACE))]


inquiry_consult = Trigger(
    name="inquiry-consult",
    scope_query=per_inquiry_of_asn,
    predicate=_predicate,
    agent=InquiryConsultAgent(),
    commit_paths=_commit_paths,
)
