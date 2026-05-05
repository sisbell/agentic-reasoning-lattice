"""Inquiry-consult agent — initial-draft channel consultation.

Fires when an inquiry has no consultation answer covering it yet.
One fire = decompose the inquiry into questions, run theory +
evidence consultations on each, persist per-Q/A answer docs, emit
substrate facts (consultation.questions, consultation.answer.<role>,
consultation.coverage).

Distinct from `NoteConsultAgent`, which handles the revise-stage
consult on review findings. Both agents share the same backend
(per-Q/A answer docs, channel-specific consult primitives) but
operate on different inputs and at different points in the flow.
"""

from __future__ import annotations

import re
import sys
from typing import ClassVar

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.consultation.decompose import run_consult_for_inquiry
from lib.protocols.febe.protocol import Session
from lib.shared.git_ops import step_commit_asn


class InquiryConsultAgent(Agent):
    """One initial-draft consult pass on an inquiry that lacks coverage."""

    role: ClassVar[str] = "inquiry-consult"

    def __init__(self, *, model: str = "opus"):
        self.model = model

    def run(self, session: Session, inquiry_addr: Address) -> AgentResult:
        inquiry_path_rel = session.get_path_for_addr(inquiry_addr)
        if inquiry_path_rel is None:
            return AgentResult(success=False, detail="no-inquiry-path")

        m = re.search(r"ASN-(\d{4})", inquiry_path_rel)
        if m is None:
            return AgentResult(success=False, detail="no-asn-label")
        asn_num = int(m.group(1))
        asn_label = f"ASN-{asn_num:04d}"

        print(
            f"  [INQUIRY-CONSULT] {asn_label}", file=sys.stderr,
        )

        consult_dir = run_consult_for_inquiry(asn_num, model=self.model)
        if consult_dir is None:
            return AgentResult(success=False, detail="consult-failed")

        step_commit_asn(
            asn_num,
            f"inquiry-consult(asn): {asn_label}",
        )

        return AgentResult(
            success=True,
            detail=f"consult dir {consult_dir.name}",
        )
