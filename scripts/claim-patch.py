#!/usr/bin/env python3
"""Claim Patch — apply a targeted fix to an ASN's claim files, emit
findings as substrate, hand off to standard claim convergence.

Reads a patch md from `_workspace/patches/claim/<ASN-NNNN>/<filename>`
(operator input drop), promotes it to a substrate-citizen `patch.claim`
doc under `_docuverse/documents/patch/claim/<ASN-NNNN>/<filename>`,
applies the fix to claim files, runs a one-shot patch-scoped review
that emits findings as proper substrate, commits.

The agent stops there. `claim_findings` decomposes the review on the
next runner pass; `claim_revise` picks up the open `comment.revise`
findings. Operator drives convergence via the claim-refinement runner
walk (e.g., `python scripts/claim-full-review.py <asn>`).

Usage:
    python scripts/claim-patch.py 34 --patch patch-ta5.md
    python scripts/claim-patch.py 34 --patch patch-ta5.md --dry-run
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.agents.producers.claim_patch import ClaimPatchAgent
from lib.cli.spec_dispatch import run_patch_cli
from lib.shared.paths import PATCH_INBOX_CLAIM


if __name__ == "__main__":
    sys.exit(run_patch_cli(
        name="patch",
        agent_cls=ClaimPatchAgent,
        inbox_root=PATCH_INBOX_CLAIM,
        description="Apply a targeted patch to an ASN's claim files.",
        dry_run_steps=(
            "promote → apply → patch-scoped review (emits findings) → done"
        ),
        next_hint_template=(
            "Drive convergence on the findings the patch reviewer filed:\n"
            "         python scripts/claim-full-review.py {asn}"
        ),
    ))
