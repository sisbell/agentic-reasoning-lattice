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

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.agents.refiners.note_absorb import NoteAbsorbAgent
from lib.protocols.febe.session import open_session
from lib.shared.paths import ABSORB_INBOX, LATTICE


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Absorb an extension ASN's claims back into its base.",
    )
    parser.add_argument(
        "--spec", required=True,
        help=(
            "Spec filename in _workspace/absorbs/. "
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

    spec_path = ABSORB_INBOX / args.spec
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
            f"  [DRY RUN] Steps: promote → integrate → "
            f"one-shot review (emits findings) → re-export → "
            f"update source citations → retire extension",
            file=sys.stderr,
        )
        print(f"  Spec: {spec_path}", file=sys.stderr)
        print(f"  Content:\n{spec_path.read_text()}", file=sys.stderr)
        return 0

    print(f"  [ABSORB] {args.spec}", file=sys.stderr)

    with open_session(LATTICE) as session:
        agent = NoteAbsorbAgent(model=args.model, effort=args.effort)
        # Operator-gated refiner: addr is unused by the agent but
        # required by the Agent dispatch surface. Pass the lattice
        # root as a stand-in.
        lattice_addr = session.store.account
        result = agent(session, lattice_addr, spec_filename=args.spec)

    print(f"\n  [DONE] {result.detail}", file=sys.stderr)
    print(
        f"  [NEXT] Drive convergence on integration findings:\n"
        f"         python scripts/note-refine.py <base-asn>",
        file=sys.stderr,
    )
    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
