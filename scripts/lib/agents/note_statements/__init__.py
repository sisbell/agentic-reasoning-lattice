"""Note-statements agent — LLM-extract a note's formal statements.

Public:
- NoteStatementsAgent — Agent class fired by the note-statements trigger.
"""

from __future__ import annotations

from .agent import STATEMENTS_MODEL, NoteStatementsAgent


__all__ = [
    "STATEMENTS_MODEL",
    "NoteStatementsAgent",
]
