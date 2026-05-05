"""Consultation-coverage predicates.

`consultation.coverage` is the substrate link from a consultation doc
(assessment or per-Q/A answer) to the finding it is about. These
predicates answer queries grounded in that link:

- "Has this finding been covered by any consultation yet?"
- "Are all of a note's open revise findings consulted?"

Used to fence note-consult firing (don't fire if every open revise is
already covered) and note-revise firing (don't fire on findings whose
consult phase hasn't run yet).
"""

from __future__ import annotations

from lib.backend.addressing import Address
from lib.protocols.febe.protocol import Session

from .convergence import unresolved_revise_comments


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
    with this should also check `is_doc_converged` if it cares about
    distinguishing "nothing to do" from "all consulted, ready to revise."
    """
    for c in unresolved_revise_comments(session, note_addr):
        if not c.from_set:
            continue
        if not is_finding_consulted(session, c.from_set[0]):
            return False
    return True
