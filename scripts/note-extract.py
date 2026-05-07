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

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.agents.producers.note_extract import NoteExtractAgent
from lib.protocols.febe.session import open_session
from lib.shared.paths import EXTRACT_INBOX, LATTICE


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract claims from an origin ASN into a new workshop ASN.",
    )
    parser.add_argument(
        "--spec", required=True,
        help=(
            "Spec filename in _workspace/extracts/. "
            "Operator drops the spec md there before running."
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

    spec_path = EXTRACT_INBOX / args.spec
    if not spec_path.exists():
        print(
            f"  [ERROR] Spec not found in workspace: {spec_path}",
            file=sys.stderr,
        )
        print(
            f"  Drop the spec md at {spec_path} and re-run.",
            file=sys.stderr,
        )
        return 1

    if args.dry_run:
        print(
            f"  [DRY RUN] Steps: promote → validate → "
            f"derive names → build prompt → LLM → write → emit lineage",
            file=sys.stderr,
        )
        print(f"  Spec: {spec_path}", file=sys.stderr)
        print(f"  Content:\n{spec_path.read_text()}", file=sys.stderr)
        return 0

    print(f"  [EXTRACT] {args.spec}", file=sys.stderr)

    with open_session(LATTICE) as session:
        agent = NoteExtractAgent(model=args.model, effort=args.effort)
        # Pure operator-gated producer: addr is unused by the agent
        # but is required by the Agent dispatch surface. Pass the
        # lattice root as a stand-in.
        lattice_addr = session.store.account
        result = agent(session, lattice_addr, spec_filename=args.spec)

    print(f"\n  [DONE] {result.detail}", file=sys.stderr)
    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
