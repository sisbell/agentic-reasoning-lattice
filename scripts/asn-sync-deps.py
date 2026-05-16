#!/usr/bin/env python3
"""Sync substrate `citation.depends` from an inquiry's frontmatter.

The inquiry md is the declarative spec for an ASN — title, question,
out_of_scope, and (per this tool) `depends`. Substrate links are the
runtime state. This tool bridges spec → substrate.

For an inquiry whose frontmatter declares `depends: [34, 36, 47]`,
this emits `citation.depends` from the inquiry's address to the
`version_head` of each dep's note. Idempotent — `emit_citation`
won't double-emit on the active set, so re-running is safe and
cheap.

Use cases:
  - After running `asn-migrate.py`, the new inquiry copy may not
    have the right deps yet. Edit its frontmatter, run this.
  - When you decide an existing inquiry needs a new (or fewer)
    deps: edit frontmatter, run this. (Note: this tool only ADDS
    missing links. To remove a dep, use retraction tooling.)

Usage:
    python scripts/asn-sync-deps.py 89
    python scripts/asn-sync-deps.py 89 90 91 92        # batch
    python scripts/asn-sync-deps.py 89 --dry-run
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.backend.emit import emit_citation
from lib.lattice.labels import format_label
from lib.protocols.febe.session import open_session
from lib.shared.frontmatter import read_doc_with_frontmatter
from lib.shared.git_ops import step_commit
from lib.shared.paths import (
    DOCUVERSE_DIR, INQUIRY_DIR, LATTICE, NOTE_DIR, WORKSPACE,
)
import subprocess


def _find_note_addr(store, asn_num: int):
    """Find the path-registered note address for an ASN. Picks the
    first match (legacy data may have multiple files for one ASN —
    e.g., .statements.md alongside the main note)."""
    label = format_label(asn_num)
    prefix = str(NOTE_DIR.relative_to(WORKSPACE)) + f"/{label}-"
    for path, addr in store.path_to_addr.items():
        if path.startswith(prefix) and not path.endswith(".statements.md"):
            return addr
    return None


def sync(asn_num: int, dry_run: bool = False) -> int:
    label = format_label(asn_num)
    inquiry_path = INQUIRY_DIR / f"{label}.md"
    if not inquiry_path.exists():
        print(
            f"  [ERROR] inquiry not found: "
            f"{inquiry_path.relative_to(WORKSPACE)}",
            file=sys.stderr,
        )
        return 1

    fm, _body = read_doc_with_frontmatter(inquiry_path)
    declared = fm.get("depends") if fm else None
    if not declared:
        print(
            f"  [{label}] no `depends` field in inquiry frontmatter — "
            f"nothing to sync",
            file=sys.stderr,
        )
        return 0
    try:
        declared_ids = sorted({int(d) for d in declared})
    except (ValueError, TypeError) as e:
        print(
            f"  [{label}] invalid depends list: {declared!r} ({e})",
            file=sys.stderr,
        )
        return 1

    inquiry_rel = str(inquiry_path.resolve().relative_to(WORKSPACE.resolve()))

    print(
        f"  [{label}] declared depends: "
        f"{', '.join(f'ASN-{d:04d}' for d in declared_ids)}",
        file=sys.stderr,
    )
    if dry_run:
        print("    [DRY RUN] no substrate changes", file=sys.stderr)
        return 0

    with open_session(LATTICE) as session:
        store = session.store
        inquiry_addr = store.path_to_addr.get(inquiry_rel)
        if inquiry_addr is None:
            print(
                f"  [{label}] inquiry not path-registered — skipping",
                file=sys.stderr,
            )
            return 1

        emitted = 0
        skipped = 0
        for dep_id in declared_ids:
            dep_note_addr = _find_note_addr(store, dep_id)
            if dep_note_addr is None:
                print(
                    f"    [WARN] ASN-{dep_id:04d} note not found in substrate; "
                    f"skipping",
                    file=sys.stderr,
                )
                skipped += 1
                continue
            # Cite the BASE/identity address, not version_head — matches
            # the note_import convention and what `note_dep_asn_ids`
            # expects (direct `path_for_addr` lookup; version-marker
            # addresses aren't path-registered).
            _link, created = emit_citation(
                store, inquiry_addr, dep_note_addr, direction="depends",
            )
            if created:
                emitted += 1
                print(
                    f"    + citation.depends → ASN-{dep_id:04d} "
                    f"(base={dep_note_addr})",
                    file=sys.stderr,
                )
            else:
                skipped += 1
                print(
                    f"      already cited: ASN-{dep_id:04d}",
                    file=sys.stderr,
                )

    print(
        f"  [{label}] sync: emitted={emitted}, already-active={skipped}",
        file=sys.stderr,
    )
    return 0


def _stage_for_commit(asn_nums: list[int]) -> None:
    """Stage the inquiry mds + substrate metadata so the LLM-driven
    commit sees the right cached diff."""
    paths = []
    for n in asn_nums:
        label = format_label(n)
        paths.append(str(
            (INQUIRY_DIR / f"{label}.md").resolve().relative_to(WORKSPACE.resolve())
        ))
    paths += [
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
        "asn", nargs="+", type=int,
        help="One or more ASN numbers to sync deps for (e.g., 89 90 91)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show declared deps without writing substrate",
    )
    parser.add_argument(
        "--no-commit", action="store_true",
        help="Skip the post-sync commit step (operator commits separately)",
    )
    args = parser.parse_args()

    rc = 0
    for n in args.asn:
        rc = sync(n, dry_run=args.dry_run) or rc

    if rc == 0 and not args.dry_run and not args.no_commit:
        _stage_for_commit(args.asn)
        label_str = ", ".join(format_label(n) for n in args.asn)
        step_commit(f"sync-deps(asn): citation.depends for {label_str}")

    return rc


if __name__ == "__main__":
    sys.exit(main())
