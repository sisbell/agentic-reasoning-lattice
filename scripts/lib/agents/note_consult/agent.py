"""Note-consult agent — channel-assign + gather evidence for the
latest review that still has uncovered revise findings.

Fires when at least one open `comment.revise` finding on the note
lacks a `consultation.coverage` link. Per fire:

  1. Walk the note's review dirs newest-to-oldest, find the latest
     `review-N` that owns an uncovered open revise.
  2. Run `run_consult_for_review` for that review — produces the
     channel-assignment doc + per-Q/A answer docs, emits
     `consultation.assessment`, `consultation.answer`, and
     `consultation.coverage` links.
  3. Commit.

Picking the newest uncovered review (not just the latest review)
avoids re-running consult on a review that's already fully covered,
while still progressing toward the predicate flipping True. The
runner handles iteration if multiple reviews have uncovered findings.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import ClassVar

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.consultation.gather_evidence import run_consult_for_review
from lib.predicates import (
    is_finding_consulted, unresolved_revise_comments,
)
from lib.protocols.febe.protocol import Session
from lib.shared.git_ops import step_commit_asn
from lib.shared.paths import LATTICE, NOTE_FINDINGS_DIR, REVIEWS_DIR


def _review_num_from_finding_path(path: str) -> int | None:
    """Extract N from `_docuverse/.../review-N/<n>.md`."""
    m = re.search(r"review-(\d+)/\d+\.md$", path)
    return int(m.group(1)) if m else None


def _latest_uncovered_review(session: Session, note_addr: Address):
    """Return (review_num, review_path) of the highest-numbered review
    that owns at least one uncovered open revise. None if all open
    revises are already covered.
    """
    best_num = -1
    best_review_path = None
    for c in unresolved_revise_comments(session, note_addr):
        if not c.from_set:
            continue
        finding_addr = c.from_set[0]
        if is_finding_consulted(session, finding_addr):
            continue
        finding_path = session.get_path_for_addr(finding_addr)
        if not finding_path:
            continue
        review_num = _review_num_from_finding_path(finding_path)
        if review_num is None:
            continue
        if review_num > best_num:
            best_num = review_num

    if best_num < 0:
        return None

    note_path = session.get_path_for_addr(note_addr)
    m = re.search(r"(ASN-\d{4})", note_path or "")
    if m is None:
        return None
    asn_label = m.group(1)
    review_path = REVIEWS_DIR / asn_label / f"review-{best_num}.md"
    if not review_path.exists():
        return None
    return best_num, review_path


class NoteConsultAgent(Agent):
    """One channel-assignment + gather-evidence pass on the latest
    uncovered review of a note."""

    role: ClassVar[str] = "note-consult"

    def __init__(self, *, model: str = "opus"):
        self.model = model

    def run(self, session: Session, note_addr: Address) -> AgentResult:
        note_path_rel = session.get_path_for_addr(note_addr)
        if note_path_rel is None:
            return AgentResult(success=False, detail="no-note-path")

        asn_path = session.store.lattice_dir / note_path_rel
        if not asn_path.exists():
            return AgentResult(success=False, detail="no-note-file")

        m = re.search(r"(ASN-\d{4})", note_path_rel)
        if m is None:
            return AgentResult(success=False, detail="no-asn-label")
        asn_label = m.group(1)
        asn_number = int(asn_label[4:])

        target = _latest_uncovered_review(session, note_addr)
        if target is None:
            return AgentResult(
                success=True, detail="all-revises-already-covered",
            )
        review_num, review_path = target

        print(
            f"  [NOTE-CONSULT] {asn_label} review-{review_num}",
            file=sys.stderr,
        )

        results_path = run_consult_for_review(
            asn_path, asn_label, review_path, model=self.model,
        )
        if results_path is None:
            return AgentResult(success=False, detail="consult-failed")

        step_commit_asn(
            asn_number,
            f"note-consult(asn): {asn_label} review-{review_num}",
        )

        return AgentResult(
            success=True,
            detail=f"review-{review_num} | {Path(results_path).name}",
        )
