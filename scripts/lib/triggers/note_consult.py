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
from lib.predicates import all_open_revises_consulted
from lib.runner import Trigger
from lib.triggers.scope import per_active_note


note_consult = Trigger(
    name="note-consult",
    scope_query=per_active_note,
    predicate=all_open_revises_consulted,
    agent=NoteConsultAgent(),
)
