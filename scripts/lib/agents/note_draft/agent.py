"""Note-draft agent — synthesizes consultation answers into a note.

Fires when an inquiry has consultation done (≥1 active
`consultation.answer.*` covering it) but no note yet (no active
`provenance.synthesis` from the inquiry). One fire = build the
discovery prompt with consultation content walked from substrate at
runtime, invoke Claude, write the note md, emit the `note`
classifier + `provenance.synthesis` link.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import ClassVar

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.consultation.draft import run_draft_for_inquiry
from lib.protocols.febe.protocol import Session
from lib.shared.git_ops import step_commit_asn


class NoteDraftAgent(Agent):
    """One initial-draft synthesis pass on a consulted inquiry."""

    role: ClassVar[str] = "note-draft"

    def run(self, session: Session, inquiry_addr: Address) -> AgentResult:
        inquiry_path_rel = session.get_path_for_addr(inquiry_addr)
        if inquiry_path_rel is None:
            return AgentResult(success=False, detail="no-inquiry-path")

        m = re.search(r"ASN-(\d{4})", inquiry_path_rel)
        if m is None:
            return AgentResult(success=False, detail="no-asn-label")
        asn_num = int(m.group(1))
        asn_label = f"ASN-{asn_num:04d}"

        print(f"  [NOTE-DRAFT] {asn_label}", file=sys.stderr)

        note_path = run_draft_for_inquiry(asn_num)
        if note_path is None:
            return AgentResult(success=False, detail="draft-failed")

        step_commit_asn(asn_num, f"note-draft(asn): {asn_label}")

        return AgentResult(
            success=True,
            detail=f"note {Path(note_path).name}",
        )
