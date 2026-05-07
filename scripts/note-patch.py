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

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.agents.producers.note_patch import NotePatchAgent
from lib.protocols.febe.session import open_session
from lib.shared.common import find_asn
from lib.shared.paths import LATTICE, PATCH_INBOX_NOTE


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Apply a targeted patch to an ASN with scoped review.",
    )
    parser.add_argument("asn", type=int, help="ASN number to patch")
    parser.add_argument(
        "--patch", required=True,
        help=(
            "Patch filename in _workspace/patches/note/ASN-NNNN/. "
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

    asn_path, asn_label = find_asn(str(args.asn))
    if asn_path is None:
        print(f"  [ERROR] ASN-{args.asn:04d} not found", file=sys.stderr)
        return 1

    patch_path = PATCH_INBOX_NOTE / asn_label / args.patch
    if not patch_path.exists():
        print(
            f"  [ERROR] Patch not found in workspace: "
            f"{patch_path}",
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
            f"review (emits findings) → re-export",
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

        agent = NotePatchAgent(model=args.model, effort=args.effort)
        result = agent(session, note_addr, patch_filename=args.patch)

    print(f"\n  [DONE] {result.detail}", file=sys.stderr)
    print(
        f"  [NEXT] Drive convergence on the findings the patch "
        f"reviewer filed:\n"
        f"         python scripts/note-refine.py {args.asn}",
        file=sys.stderr,
    )
    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
