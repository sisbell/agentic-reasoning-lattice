#!/usr/bin/env python3
"""Backfill `depends:` in inquiry frontmatter from substrate citations.

For LEGACY or MIXED ASNs (per `scripts/diagnostics/citation_depends_audit.py`),
the inquiry has no `depends:` field but substrate carries the truth in
`citation.depends` links. This tool resolves those substrate citations
to ASN ids and writes them into the inquiry frontmatter so the new
declarative-source convention has something to read.

After backfill, run `scripts/asn-sync-deps.py <asn>` to reconcile the
substrate into the target end state (one fan-out, zero note-side).

Hard-fail when:
  - Inquiry file missing
  - Inquiry frontmatter already has `depends:` (use --overwrite to replace)
  - No substrate citations exist on either side (nothing to backfill)
  - Inquiry-side and note-side disagree on dep set (MIXED with diff)

Usage:
    python scripts/asn-backfill-depends.py 86
    python scripts/asn-backfill-depends.py 86 --dry-run
    python scripts/asn-backfill-depends.py 36 40 42 --dry-run
"""

import argparse
import sys
from pathlib import Path
from typing import List

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.backend.predicates import active_links
from lib.lattice.labels import format_label, label_pattern
from lib.protocols.febe.session import open_session
from lib.shared.frontmatter import read_doc_with_frontmatter, write_frontmatter
from lib.shared.paths import LATTICE, NOTE_DIR, WORKSPACE, inquiry_doc_path


def _collect_dep_ids_from(store, addr, pattern) -> List[int]:
    """Resolve active citation.depends from addr to sorted ASN ids."""
    out: set[int] = set()
    if addr is None:
        return []
    for link in active_links(
        store.state, "citation.depends", from_set=[addr],
    ):
        for target in link.to_set:
            tpath = store.path_for_addr(target)
            if not tpath:
                continue
            m = pattern.search(tpath)
            if m:
                out.add(int(m.group(1)))
    return sorted(out)


def _find_note_addr(store, asn_num: int):
    label = format_label(asn_num)
    prefix = str(NOTE_DIR.relative_to(WORKSPACE)) + f"/{label}-"
    for path, addr in store.path_to_addr.items():
        if path.startswith(prefix) and not path.endswith(".statements.md"):
            return addr
    return None


def backfill(asn_num: int, *, dry_run: bool = False, overwrite: bool = False) -> int:
    label = format_label(asn_num)
    inq_path = inquiry_doc_path(asn_num)

    if not inq_path.exists():
        print(f"  [{label}] [ERROR] inquiry missing: {inq_path}", file=sys.stderr)
        return 1

    fm, body = read_doc_with_frontmatter(inq_path)
    if "depends" in fm and not overwrite:
        existing = fm["depends"]
        print(
            f"  [{label}] [ERROR] frontmatter already declares depends={existing} "
            f"— use --overwrite to replace",
            file=sys.stderr,
        )
        return 1

    with open_session(LATTICE) as session:
        store = session.store
        pattern = label_pattern()
        inq_rel = str(inq_path.resolve().relative_to(WORKSPACE.resolve()))
        inq_addr = store.path_to_addr.get(inq_rel)
        note_addr = _find_note_addr(store, asn_num)
        inq_deps = _collect_dep_ids_from(store, inq_addr, pattern)
        note_deps = _collect_dep_ids_from(store, note_addr, pattern)

    if inq_deps and note_deps and set(inq_deps) != set(note_deps):
        print(
            f"  [{label}] [ERROR] substrate disagreement — "
            f"inquiry-side {inq_deps} != note-side {note_deps}. "
            f"Resolve manually before backfilling.",
            file=sys.stderr,
        )
        return 1

    deps = inq_deps or note_deps
    if not deps:
        print(
            f"  [{label}] [ERROR] no substrate citation.depends found on "
            f"inquiry or note — nothing to backfill",
            file=sys.stderr,
        )
        return 1

    source = "inquiry-side" if inq_deps else "note-side"
    dep_labels = ", ".join(f"ASN-{d:04d}" for d in deps)
    print(
        f"  [{label}] backfilling depends from {source} substrate: {dep_labels}",
        file=sys.stderr,
    )

    if dry_run:
        print(f"  [{label}] [DRY RUN] no file write", file=sys.stderr)
        return 0

    fm["depends"] = deps
    inq_path.write_text(write_frontmatter(fm, body))
    print(
        f"  [{label}] wrote depends to "
        f"{inq_path.relative_to(WORKSPACE)}",
        file=sys.stderr,
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "asn", nargs="+", type=int,
        help="One or more ASN numbers to backfill",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would be written without modifying files",
    )
    parser.add_argument(
        "--overwrite", action="store_true",
        help="Replace existing `depends:` if already present in frontmatter",
    )
    args = parser.parse_args()

    rc = 0
    for n in args.asn:
        rc = backfill(n, dry_run=args.dry_run, overwrite=args.overwrite) or rc
    return rc


if __name__ == "__main__":
    sys.exit(main())
