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

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.agents.producers.claim_patch import ClaimPatchAgent
from lib.protocols.febe.session import open_session
from lib.shared.common import find_asn
from lib.shared.paths import LATTICE, PATCH_INBOX_CLAIM


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Apply a targeted patch to an ASN's claim files.",
    )
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument(
        "--patch", required=True,
        help=(
            "Patch filename in _workspace/patches/claim/ASN-NNNN/. "
            "Operator drops the patch md there before running."
        ),
    )
    parser.add_argument(
        "--model", "-m", default="opus", choices=["opus", "sonnet"],
    )
    parser.add_argument(
        "--effort", default="max", help="Thinking effort level",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  [ERROR] ASN-{asn_num:04d} not found", file=sys.stderr)
        return 1

    patch_path = PATCH_INBOX_CLAIM / asn_label / args.patch
    if not patch_path.exists():
        print(
            f"  [ERROR] Patch not found in workspace: {patch_path}",
            file=sys.stderr,
        )
        print(
            f"  Drop the patch md at {patch_path} and re-run.",
            file=sys.stderr,
        )
        return 1

    if args.dry_run:
        print(
            f"  [DRY RUN] Steps: promote → apply → patch-scoped "
            f"review (emits findings) → done",
            file=sys.stderr,
        )
        print(f"  Patch: {patch_path}", file=sys.stderr)
        print(f"  Content:\n{patch_path.read_text()}", file=sys.stderr)
        return 0

    print(f"  [PATCH] {asn_label} ← {args.patch}", file=sys.stderr)

    with open_session(LATTICE) as session:
        note_rel = str(asn_path.resolve().relative_to(LATTICE.resolve()))
        note_addr = session.get_addr_for_path(note_rel)
        if note_addr is None:
            note_addr = session.register_path(note_rel)

        agent = ClaimPatchAgent(model=args.model, effort=args.effort)
        result = agent(session, note_addr, patch_filename=args.patch)

    print(f"\n  [DONE] {result.detail}", file=sys.stderr)
    print(
        f"  [NEXT] Drive convergence on the findings the patch "
        f"reviewer filed:\n"
        f"         python scripts/claim-full-review.py {asn_num}",
        file=sys.stderr,
    )
    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
