"""Consultation-coverage predicates.

`consultation.coverage` is the substrate link from a consultation doc
(assessment, questions, or per-Q/A answer) to the inquiry/finding it
is about. Predicates here answer queries grounded in that link:

  Revise-stage:
    - is_finding_consulted          — has any consult covered the finding?
    - all_open_revises_consulted    — gate for note-revise

  Initial-draft stage:
    - has_consultation_for_inquiry  — gate for inquiry-consult firing
    - has_note_for_inquiry          — gate for note-draft firing
"""

from __future__ import annotations

from lib.backend.addressing import Address
from lib.protocols.febe.protocol import Session

from .quiescence import unresolved_revise_comments


def is_finding_consulted(session: Session, finding_addr: Address) -> bool:
    """True iff at least one active `consultation.coverage` link
    targets the finding (assessment or answer doc, doesn't matter)."""
    return bool(
        session.active_links("consultation.coverage", to_set=[finding_addr])
    )


def all_open_revises_consulted(
    session: Session, note_addr: Address,
) -> bool:
    """True iff every open `comment.revise` finding on the note has at
    least one active `consultation.coverage` link.

    Vacuously true when the note has no open revises — no findings
    means no findings-without-coverage. The runner predicate paired
    with this should also check `is_doc_quiescent` if it cares about
    distinguishing "nothing to do" from "all consulted, ready to revise."
    """
    for c in unresolved_revise_comments(session, note_addr):
        if not c.from_set:
            continue
        if not is_finding_consulted(session, c.from_set[0]):
            return False
    return True


def has_consultation_for_inquiry(
    session: Session, inquiry_addr: Address,
) -> bool:
    """True iff at least one `consultation.answer.*` doc covers the
    inquiry. Initial-draft consult done = at least one answer exists.

    Walks consultation.coverage backward from the inquiry; filters
    sources that have a `consultation.answer` classifier (parent-prefix
    match catches both .theory and .evidence subtypes). Questions /
    assessment docs alone don't satisfy — only actual Q/A answers count.
    """
    for link in session.active_links(
        "consultation.coverage", to_set=[inquiry_addr],
    ):
        if not link.from_set:
            continue
        source_addr = link.from_set[0]
        if session.active_links(
            "consultation.answer", to_set=[source_addr],
        ):
            return True
    return False


def has_note_for_inquiry(
    session: Session, inquiry_addr: Address,
) -> bool:
    """True iff a note has been drafted from this inquiry — recorded
    as `provenance.synthesis` from inquiry → note.
    """
    return bool(
        session.active_links(
            "provenance.synthesis", from_set=[inquiry_addr],
        )
    )
