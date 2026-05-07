#!/usr/bin/env python3
"""Note-clone CLI — operator dispatcher for NoteCloneAgent.

The operator:
  1. Drops a spec md into `_workspace/clones/<filename>.md`.
     Frontmatter declares clone_from / create_note; body holds the
     rationale prose for the clone.
  2. Runs `python scripts/note-clone.py --spec <filename>`.

Example spec doc:

    ---
    clone_from: 48
    create_note: 59
    ---

    # Why I'm cloning ASN-48

    [Operator's rationale: what experiment, what hypothesis, etc.]

The agent promotes the spec to substrate (`_docuverse/documents/clone/`),
copies origin's note / inquiry / consultations under the clone's ASN
identity, mirrors citation.depends, and emits provenance.clone.

Usage:
    python scripts/note-clone.py --spec clone-asn48-experiment.md
    python scripts/note-clone.py --spec clone-asn48-experiment.md --dry-run
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.agents.producers.note_clone import NoteCloneAgent
from lib.cli.spec_dispatch import run_spec_cli
from lib.shared.paths import CLONE_INBOX


if __name__ == "__main__":
    sys.exit(run_spec_cli(
        name="clone",
        agent_cls=NoteCloneAgent,
        inbox=CLONE_INBOX,
        description="Clone an ASN under a new ASN number.",
        dry_run_steps=(
            "promote → validate → copy note/inquiry/consultations → "
            "emit lineage"
        ),
        accepts_model=False,
    ))
