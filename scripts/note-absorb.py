#!/usr/bin/env python3
"""Note-absorb CLI — operator dispatcher for NoteAbsorbAgent.

The operator:
  1. Drops a spec md into `_workspace/absorbs/<filename>.md`.
     Frontmatter declares which extension to absorb; body holds the
     rationale prose.
  2. Runs `python scripts/note-absorb.py --spec <filename>`.

Example spec doc:

    ---
    absorb: 57
    ---

    # Why this extension is ready to merge back

    [Operator's scout-reasoning prose: convergence evidence,
     integration readiness, etc.]

The agent promotes the spec to substrate (`_docuverse/documents/absorb/`),
integrates the extension's claims into base, files a one-shot
integration review (emitting findings as substrate), updates source
citations, retires the extension, and emits provenance.absorb.

Usage:
    python scripts/note-absorb.py --spec absorb-asn57.md
    python scripts/note-absorb.py --spec absorb-asn57.md --dry-run
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.agents.refiners.note_absorb import NoteAbsorbAgent
from lib.cli.spec_dispatch import run_spec_cli
from lib.shared.paths import ABSORB_INBOX


if __name__ == "__main__":
    sys.exit(run_spec_cli(
        name="absorb",
        agent_cls=NoteAbsorbAgent,
        inbox=ABSORB_INBOX,
        description="Absorb an extension ASN's claims back into its base.",
        dry_run_steps=(
            "promote → integrate → one-shot review (emits findings) → "
            "re-export → update source citations → retire extension"
        ),
        next_hint=(
            "Drive convergence on integration findings via per-trigger\n"
            "         CLIs: note_review, note_consult, note_revise —\n"
            "         each `python scripts/run-trigger.py NAME "
            "<base-asn>`."
        ),
    ))
