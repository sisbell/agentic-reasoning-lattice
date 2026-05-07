"""Inquiry-consult trigger — fires when an inquiry has no consultation
answers covering it.

  scope:     each active inquiry in scope (CLI: one ASN's inquiry;
             daemon: every active inquiry)
  predicate: has_consultation_for_inquiry — fire when no
             consultation.answer.* doc covers the inquiry
  agent:     InquiryConsultAgent
"""

from __future__ import annotations

from lib.agents.producers.inquiry_consult import InquiryConsultAgent
from lib.predicates import has_consultation_for_inquiry
from lib.runner import Trigger
from lib.triggers.scope import per_inquiry_of_asn


inquiry_consult = Trigger(
    name="inquiry-consult",
    scope_query=per_inquiry_of_asn,
    predicate=has_consultation_for_inquiry,
    agent=InquiryConsultAgent(),
)
