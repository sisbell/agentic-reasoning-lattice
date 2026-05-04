"""Cone-review agent — wraps the run_cone_review orchestrator.

Fired by the cone-review trigger (lib/triggers/cone_review.py) on
each apex claim that hasn't converged. The agent resolves the apex's
same-ASN dep chain from the substrate and dispatches the existing
orchestrator function with that context. Returns AgentResult.
"""

from __future__ import annotations

from typing import ClassVar

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.lattice.labels import build_cross_asn_label_index
from lib.orchestrators.cone_review import run_cone_review
from lib.protocols.febe.protocol import Session
from lib.shared.claim_files import build_label_index
from lib.shared.paths import CLAIM_DIR


CONE_MAX_CYCLES = 8
CONE_MODEL = "sonnet"


class ConeReviewAgent(Agent):
    """Resolve apex context and dispatch the cone-review orchestrator."""

    role: ClassVar[str] = "cone-review"

    def run(self, session: Session, addr: Address) -> AgentResult:
        label_index = build_cross_asn_label_index(session.store)
        rev_index = {a: lbl for lbl, a in label_index.items()}

        apex_label = rev_index.get(addr)
        if apex_label is None:
            return AgentResult(success=False, detail="apex label not found")

        asn_path = session.get_path_for_addr(addr)
        if asn_path is None:
            return AgentResult(success=False, detail="path not found for addr")
        # _docuverse/documents/claim/<ASN>/<label>.md
        asn_label_str = asn_path.split("/")[3]
        asn_num = int(asn_label_str[4:])

        claim_dir = CLAIM_DIR / asn_label_str
        asn_labels = set(build_label_index(claim_dir).keys())
        same_deps = [
            rev_index[link.to_set[0]]
            for link in session.active_links(
                "citation.depends", from_set=[addr],
            )
            if link.to_set and rev_index.get(link.to_set[0]) in asn_labels
        ]

        outcome = run_cone_review(
            asn_num, apex_label, same_deps,
            max_cycles=CONE_MAX_CYCLES, model=CONE_MODEL,
        )
        return AgentResult(success=outcome == "converged", detail=outcome)
