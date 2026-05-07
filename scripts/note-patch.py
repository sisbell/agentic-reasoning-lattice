#!/usr/bin/env python3
"""Note Patch — apply a targeted patch to an ASN with scoped review/revise.

Reads a patch md from `_workspace/patches/<ASN-NNNN>/<filename>` (operator
input drop), promotes it to a substrate-citizen `patch` doc under
`_docuverse/documents/patch/<ASN-NNNN>/<filename>`, applies the fix, drives
patch-scoped review/revise to convergence, re-exports the note, commits.

The agent emits a `patch` classifier on the substrate doc + a
`provenance.derivation(F=[patch], G=[note])` audit edge. The note md is
edited; its supersession chain advances via `register_version`.

Usage:
    python scripts/note-patch.py 63 --patch patch-1.md
    python scripts/note-patch.py 63 --patch patch-1.md --dry-run
    python scripts/note-patch.py 63 --patch patch-1.md --report
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.agents.producers.note_patch import NotePatchAgent
from lib.protocols.febe.session import open_session
from lib.shared.common import find_asn, read_file
from lib.shared.invoke_claude import invoke_claude
from lib.shared.paths import LATTICE, PATCH_INBOX, prompt_path


def _print_report(asn_num, asn_path, patch_path, *, model, effort):
    """--report: show impact analysis without applying."""
    template = read_file(prompt_path("discovery/patch/report.md"))
    if not template:
        print("  [ERROR] Patch report prompt not found", file=sys.stderr)
        return 1
    asn_content = asn_path.read_text()
    patch_content = patch_path.read_text()
    prompt = (
        template
        .replace("{{patch_content}}", patch_content)
        .replace("{{asn_content}}", asn_content)
    )
    print(f"  [REPORT] Analyzing impact...", file=sys.stderr)
    result = invoke_claude(prompt, model=model, effort=effort)
    if result.text:
        print(f"\n{result.text}\n", file=sys.stderr)
        return 0
    print("  [ERROR] No report produced", file=sys.stderr)
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Apply a targeted patch to an ASN with scoped review.",
    )
    parser.add_argument("asn", type=int, help="ASN number to patch")
    parser.add_argument(
        "--patch", required=True,
        help=(
            "Patch filename in _workspace/patches/ASN-NNNN/. "
            "Operator drops the patch md there before running."
        ),
    )
    parser.add_argument(
        "--model", "-m", default="opus", choices=["opus", "sonnet"],
    )
    parser.add_argument(
        "--effort", default="max", help="Thinking effort level",
    )
    parser.add_argument(
        "--max-cycles", type=int, default=10,
        help="Max review/revise cycles (default: 10)",
    )
    parser.add_argument(
        "--report", action="store_true",
        help="Show impact report without applying",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    asn_path, asn_label = find_asn(str(args.asn))
    if asn_path is None:
        print(f"  [ERROR] ASN-{args.asn:04d} not found", file=sys.stderr)
        return 1

    patch_path = PATCH_INBOX / asn_label / args.patch
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

    if args.report:
        return _print_report(
            args.asn, asn_path, patch_path,
            model=args.model, effort=args.effort,
        )

    if args.dry_run:
        print(
            f"  [DRY RUN] Steps: promote → apply → patch-scoped "
            f"review/revise → re-export",
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

        agent = NotePatchAgent(
            model=args.model,
            effort=args.effort,
            max_cycles=args.max_cycles,
        )
        result = agent(session, note_addr, patch_filename=args.patch)

    print(f"\n  [DONE] {result.detail}", file=sys.stderr)
    print(
        f"  [NEXT] Optional full review: "
        f"python scripts/note-refine.py {args.asn}",
        file=sys.stderr,
    )
    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
