#!/usr/bin/env python3
"""Note Refinement — drive a note through review/revise cycles via the
trigger runner.

Walks the note-review, note-consult, and note-revise triggers until
quiescent. Each cycle fires any trigger whose predicate is unsatisfied;
quiescence is when a full pass fires nothing (no open revises AND the
most recent review filed zero new revises).

Usage:
    python scripts/note-refine.py 9                   # default 100 max passes
    python scripts/note-refine.py 9 --max-iterations 8
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.cli.runner_walk import run_trigger_cli
from lib.triggers import note_consult, note_review, note_revise


if __name__ == "__main__":
    sys.exit(run_trigger_cli(
        name="note-refine",
        triggers=[note_review, note_consult, note_revise],
        support_claim_filter=False,
        description=(
            "Drive a note through review/consult/revise cycles to "
            "quiescence via the trigger runner."
        ),
    ))
