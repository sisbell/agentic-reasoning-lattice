#!/usr/bin/env python3
"""Note-extract CLI — operator dispatcher for NoteExtractAgent.

The operator:
  1. Drops a spec md into `_workspace/extracts/<filename>.md`.
     Frontmatter declares intent (create_note, extract_from,
     absorb_into, claims); body holds the rationale prose.
  2. Runs `python scripts/note-extract.py --spec <filename>`.

Example spec doc:

    ---
    create_note: 57
    extract_from: 53
    absorb_into: 34
    claims: [D0, D1, D2]
    ---

    # Why these claims belong as their own ASN

    [Operator's scout-reasoning prose...]

The agent promotes the spec to substrate (`_docuverse/documents/extract/`),
generates the new workshop ASN via LLM extraction, and emits lineage
(note classifier; extends → absorb_into; source → extract_from;
provenance.extract → new note).

Usage:
    python scripts/note-extract.py --spec asn34-T5-extract.md
    python scripts/note-extract.py --spec asn34-T5-extract.md --dry-run
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.agents.producers.note_extract import NoteExtractAgent
from lib.cli.spec_dispatch import run_spec_cli
from lib.shared.paths import EXTRACT_INBOX


if __name__ == "__main__":
    sys.exit(run_spec_cli(
        name="extract",
        agent_cls=NoteExtractAgent,
        inbox=EXTRACT_INBOX,
        description="Extract claims from an origin ASN into a new workshop ASN.",
        dry_run_steps=(
            "promote → validate → derive names → build prompt → "
            "LLM → write → emit lineage"
        ),
    ))
