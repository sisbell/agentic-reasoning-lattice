#!/usr/bin/env python3
"""Note-import CLI — operator dispatcher for NoteImportAgent.

The operator:
  1. Drops a spec md into `_workspace/imports/<filename>.md`.
     Frontmatter declares create_note / title / source_doc / depends;
     body holds the rationale prose for the import.
  2. Runs `python scripts/note-import.py --spec <filename>`.

Example spec doc:

    ---
    create_note: 86
    title: "Substrate Type Registry"
    source_doc: "docs/protocols/substrate/types.md"
    depends: [34, 36, 43]
    ---

    # Why I'm importing this doc

    [Operator's rationale: what experiment, what hypothesis,
     why promote this doc to the lattice...]

The agent promotes the spec to substrate (`_docuverse/.../import/`),
copies the source doc to the note path under the new ASN identity
(with H1 retitled), emits the `note` classifier + declared
`citation.depends` edges, and emits `provenance.import` for the audit
trail. Source doc stays in place.

Usage:
    python scripts/note-import.py --spec import-types-md.md
    python scripts/note-import.py --spec import-types-md.md --dry-run
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.agents.producers.note_import import NoteImportAgent
from lib.cli.spec_dispatch import run_spec_cli
from lib.shared.paths import IMPORT_INBOX


if __name__ == "__main__":
    sys.exit(run_spec_cli(
        name="import",
        agent_cls=NoteImportAgent,
        inbox=IMPORT_INBOX,
        description="Import an external doc into the note set as a new ASN.",
        dry_run_steps=(
            "promote spec → copy source → register note → "
            "emit classifier + deps + lineage"
        ),
        accepts_model=False,
    ))
