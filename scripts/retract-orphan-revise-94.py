#!/usr/bin/env python3
"""One-shot retraction of orphan comment.revise links on ASN-0094.

The session of 2026-05-23 left six orphan finding-doc registrations at
substrate addresses 10746–10756 — file paths
`_docuverse/documents/1.1/1/finding/notes/ASN-0094/review-31/{0-5}.md`
that no longer exist on disk (the files were moved to review-33/ but
the substrate path-bindings were never updated). Each orphan finding
has an active `comment.revise` link targeting ASN-0094.

This script retracts those 6 links so the runner stops seeing them as
unresolved revise comments and stops looping on note-consult attempts
against a CONVERGED review-31.md.

The script is keyed to the specific corruption — it walks finding/notes/
ASN-0094/review-31/, identifies bindings whose file is missing, and
retracts each outgoing comment.revise. Idempotent: re-running after
the first emit retracts no further links (active set already empty).

Usage:
    python scripts/retract-orphan-revise-94.py
    python scripts/retract-orphan-revise-94.py --dry-run
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.backend.emit import emit_retraction
from lib.protocols.febe.session import open_session
from lib.shared.git_ops import step_commit
from lib.shared.paths import DOCUVERSE_DIR, LATTICE, WORKSPACE


def retract_orphans(dry_run: bool = False) -> int:
    emitted = 0
    with open_session(LATTICE) as session:
        orphans = []
        for path, addr in session.store.path_to_addr.items():
            if 'finding/notes/ASN-0094/review-31/' not in path:
                continue
            if (Path(WORKSPACE) / path).exists():
                continue
            orphans.append((path, addr))

        if not orphans:
            print("  no orphan finding registrations found — nothing to do",
                  file=sys.stderr)
            return 0

        print(f"  found {len(orphans)} orphan finding registrations",
              file=sys.stderr)

        for path, finding_addr in orphans:
            revise_links = session.active_links(
                'comment.revise', from_set=[finding_addr],
            )
            if not revise_links:
                print(f"    {finding_addr} ({path}) — no active comment.revise",
                      file=sys.stderr)
                continue
            for link in revise_links:
                print(f"    retract comment.revise {link.addr} "
                      f"(from={finding_addr} to={list(link.to_set)})",
                      file=sys.stderr)
                if dry_run:
                    continue
                emit_retraction(session.store, finding_addr, link.addr)
                emitted += 1

    return emitted


def _stage_for_commit():
    paths = [
        str((DOCUVERSE_DIR / "links.jsonl").resolve().relative_to(
            WORKSPACE.resolve())),
        str((DOCUVERSE_DIR / "paths.json").resolve().relative_to(
            WORKSPACE.resolve())),
    ]
    subprocess.run(
        ["git", "add"] + paths,
        cwd=str(WORKSPACE), capture_output=True, text=True,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show which links would be retracted without writing.",
    )
    parser.add_argument(
        "--no-commit", action="store_true",
        help="Skip the post-retraction commit step.",
    )
    args = parser.parse_args()

    emitted = retract_orphans(dry_run=args.dry_run)
    print(f"\n  retracted {emitted} comment.revise links", file=sys.stderr)

    if emitted and not args.dry_run and not args.no_commit:
        _stage_for_commit()
        step_commit(
            "retract(asn-94): orphan comment.revise links from "
            "review-31 finding registrations (substrate cleanup)"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
