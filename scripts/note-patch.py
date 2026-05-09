#!/usr/bin/env python3
"""Note Patch — apply a targeted patch to an ASN, emit findings as
substrate, hand off to standard runner walk for convergence.

Reads a patch md from `_workspace/patches/note/<ASN-NNNN>/<filename>`
(operator input drop), promotes it to a substrate-citizen `patch.note`
doc under `_docuverse/documents/patch/note/<ASN-NNNN>/<filename>`,
applies the fix, runs a one-shot patch-scoped review that emits findings
as proper substrate, re-exports, commits.

The agent emits a `patch.note` classifier on the substrate doc + a
`provenance.derivation(F=[patch], G=[note])` audit edge. The
patch-scoped review's findings sit in substrate as open
`comment.revise` links waiting for `note_revise` to fire on the next
runner walk.

Usage:
    python scripts/note-patch.py 63 --patch patch-1.md
    python scripts/note-patch.py 63 --patch patch-1.md --dry-run
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.agents.producers.note_patch import NotePatchAgent
from lib.cli.spec_dispatch import run_patch_cli
from lib.shared.paths import PATCH_INBOX_NOTE


if __name__ == "__main__":
    sys.exit(run_patch_cli(
        name="patch",
        agent_cls=NotePatchAgent,
        inbox_root=PATCH_INBOX_NOTE,
        description="Apply a targeted patch to an ASN with scoped review.",
        dry_run_steps=(
            "promote → apply → patch-scoped review (emits findings) → "
            "re-export"
        ),
        next_hint_template=(
            "Drive convergence on the findings the patch reviewer filed\n"
            "         via per-trigger CLIs: note_review, note_consult,\n"
            "         note_revise — each `python scripts/run-trigger.py "
            "NAME {asn}`."
        ),
    ))
