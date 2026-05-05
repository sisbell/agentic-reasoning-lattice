"""Inquiry-consult trigger — fires when an inquiry has no consultation
answers covering it.

  scope:     each active inquiry in scope (CLI: one ASN's inquiry;
             daemon: every active inquiry)
  predicate: has_consultation_for_inquiry — fire when no
             consultation.answer.* doc covers the inquiry
  agent:     InquiryConsultAgent
"""

from __future__ import annotations

from typing import Iterator

from lib.agents.inquiry_consult import InquiryConsultAgent
from lib.backend.addressing import Address
from lib.predicates import has_consultation_for_inquiry
from lib.protocols.febe.protocol import Session
from lib.runner import Scope, Trigger
from lib.shared.paths import LATTICE, inquiry_doc_path


def _scope_query(session: Session, scope: Scope) -> Iterator[Address]:
    """Yield inquiry doc addresses to consider this pass.

    CLI mode (scope.asn_label set): the single ASN's inquiry doc.
    Daemon mode (scope.asn_label is None): every active inquiry.
    """
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


inquiry_consult = Trigger(
    name="inquiry-consult",
    scope_query=_scope_query,
    predicate=has_consultation_for_inquiry,
    agent=InquiryConsultAgent(),
)
