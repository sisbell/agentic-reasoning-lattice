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

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.agents.producers.note_clone import NoteCloneAgent
from lib.protocols.febe.session import open_session
from lib.shared.paths import CLONE_INBOX, LATTICE


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Clone an ASN under a new ASN number.",
    )
    parser.add_argument(
        "--spec", required=True,
        help=(
            "Spec filename in _workspace/clones/. "
            "Operator drops the spec md there before running."
        ),
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    spec_path = CLONE_INBOX / args.spec
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
            f"copy note/inquiry/consultations → emit lineage",
            file=sys.stderr,
        )
        print(f"  Spec: {spec_path}", file=sys.stderr)
        print(f"  Content:\n{spec_path.read_text()}", file=sys.stderr)
        return 0

    print(f"  [CLONE] {args.spec}", file=sys.stderr)

    with open_session(LATTICE) as session:
        agent = NoteCloneAgent()
        # Operator-gated pure producer: addr is unused by the agent
        # but required by the Agent dispatch surface. Pass the
        # lattice root as a stand-in.
        lattice_addr = session.store.account
        result = agent(session, lattice_addr, spec_filename=args.spec)

    print(f"\n  [DONE] {result.detail}", file=sys.stderr)
    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
