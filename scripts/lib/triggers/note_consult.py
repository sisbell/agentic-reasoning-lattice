"""Note-consult trigger — fires when a note has open revises lacking
consultation coverage.

  scope:     each active non-retired note (CLI: one ASN's note;
             daemon: every active note)
  predicate: all_open_revises_consulted — fires when any open revise's
             finding lacks at least one `consultation.coverage` link
  agent:     NoteConsultAgent
"""

from __future__ import annotations

from lib.agents.producers.note_consult import NoteConsultAgent
from lib.backend.addressing import Address
from lib.lattice.labels import label_pattern
from lib.predicates import all_open_revises_consulted
from lib.protocols.febe.protocol import Session
from lib.runner import Trigger
from lib.shared.paths import CONSULTATIONS_DIR, WORKSPACE
from lib.triggers.scope import per_active_note


def _commit_paths(session: Session, note_addr: Address) -> list[str]:
    """The consultation subtree this fire owns for the target ASN.

    note_consult emits consultation-N/ subdirs (assessment + per-finding
    answers) under the target ASN's consultation namespace.
    """
    path = session.get_path_for_addr(note_addr)
    if not path:
        return []
    m = label_pattern().search(path)
    if not m:
        return []
    asn_label = m.group(0)
    return [str((CONSULTATIONS_DIR / asn_label).relative_to(WORKSPACE))]


note_consult = Trigger(
    name="note-consult",
    scope_query=per_active_note,
    predicate=all_open_revises_consulted,
    agent=NoteConsultAgent(),
    commit_paths=_commit_paths,
)
