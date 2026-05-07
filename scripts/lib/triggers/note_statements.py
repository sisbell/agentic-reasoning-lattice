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
from lib.predicates import statements_is_fresh
from lib.runner import Trigger
from lib.triggers.scope import per_asn_note


note_statements = Trigger(
    name="note-statements",
    scope_query=per_asn_note,
    predicate=statements_is_fresh,
    agent=NoteStatementsAgent(),
)
