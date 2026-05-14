"""Note-statements trigger — fires on the source note when its
formal-statements sidecar is stale relative to its confirmed state.

  scope:     the source note for the requested ASN
  predicate: statements_is_fresh
  agent:     NoteStatementsAgent

Fires at the +1 boundary of the N+1 refinement pattern: only when
the note has no open revises AND the latest review was clean. During
active revise cycles the predicate stays True (quiescent) — we don't
re-extract on every accept, only when the note has settled.
"""

from __future__ import annotations

from lib.agents.producers.note_statements import NoteStatementsAgent
from lib.backend.addressing import Address
from lib.predicates import statements_is_fresh
from lib.protocols.febe.protocol import Session
from lib.runner import Trigger
from lib.triggers.scope import per_asn_note


def _commit_paths(session: Session, note_addr: Address) -> list[str]:
    """The statements sidecar this fire owns.

    note_statements extracts <note>.statements.md from the note body.
    The sidecar lives adjacent to the note on disk.
    """
    note_path = session.get_path_for_addr(note_addr)
    if not note_path:
        return []
    # sidecar is the note path with .statements appended before .md
    if note_path.endswith(".md"):
        sidecar_path = note_path[:-3] + ".statements.md"
    else:
        sidecar_path = note_path + ".statements.md"
    return [sidecar_path]


note_statements = Trigger(
    name="note-statements",
    scope_query=per_asn_note,
    predicate=statements_is_fresh,
    agent=NoteStatementsAgent(),
    commit_paths=_commit_paths,
)
