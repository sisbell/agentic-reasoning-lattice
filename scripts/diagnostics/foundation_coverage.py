#!/usr/bin/env python3
"""Audit foundation coverage across the lattice.

For each active note, simulate `load_foundation_for_note`'s dep
resolution and report any dep that would silently drop. Mirrors the
loader's resolution path exactly (find_asn → path_to_addr →
statements_sidecar_of → latest_doc_head) so what this reports is
literally what the reviewer would not see at fire time.

This is the audit complement to the loader-side stderr warning landed
on the same date — the loader surfaces skips at fire time; this
diagnostic surfaces them on demand against the full lattice.

The bug that motivated this tool (2026-05-23): a register_version'd
statements sidecar walked via `supersession_head` returned a version
marker with no registered file path. The loader's try/except on
read_doc silently dropped the dep. Fixed by introducing
`latest_doc_head` and removing the silent fallback. This tool would
have flagged the dropped dep before the false review finding was ever
filed.

Output:
    ASN-NNNN  declared=N  resolved=M  skipped=[(dep, reason), ...]

Notes with no foundation deps or no resolution issues are suppressed
unless --verbose. Exit 0 if no skips found across the lattice; exit 1
on any skip (suitable for CI gates).

Usage:
    python scripts/diagnostics/foundation_coverage.py
    python scripts/diagnostics/foundation_coverage.py 51
    python scripts/diagnostics/foundation_coverage.py 51 94
    python scripts/diagnostics/foundation_coverage.py --verbose
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.lattice.labels import (
    format_label, label_pattern, note_dep_asn_ids,
)
from lib.predicates import latest_doc_head, statements_sidecar_of
from lib.protocols.febe.session import open_session
from lib.shared.common import find_asn
from lib.shared.paths import LATTICE, NOTE_DIR, WORKSPACE


def _audit_one_note(session, note_addr):
    """Replicate load_foundation_for_note's resolution; return
    (declared_count, resolved_count, skipped_list)."""
    store = session.store
    dep_ids = note_dep_asn_ids(store, note_addr)

    declared = len(dep_ids)
    resolved = 0
    skipped = []

    for dep_id in dep_ids:
        dep_path, _ = find_asn(str(dep_id))
        if dep_path is None:
            skipped.append((dep_id, "no on-disk note file"))
            continue
        dep_rel = str(dep_path.resolve().relative_to(WORKSPACE.resolve()))
        dep_note_addr = store.path_to_addr.get(dep_rel)
        if dep_note_addr is None:
            skipped.append((dep_id, "note not path-registered"))
            continue
        sidecar = statements_sidecar_of(session, dep_note_addr)
        if sidecar is None:
            skipped.append((dep_id, "no statements sidecar"))
            continue
        # Loader uses latest_doc_head + read_doc; we don't run read_doc
        # itself because the audit doesn't need the prose, but we do
        # check that latest_doc_head returns a path-bearing address.
        head = latest_doc_head(session, sidecar)
        if store.path_for_addr(head) is None:
            skipped.append((dep_id, f"head {head} has no registered path"))
            continue
        resolved += 1

    return declared, resolved, skipped


def _iter_active_notes(session, asn_filter):
    pattern = label_pattern()
    note_prefix = str(NOTE_DIR.relative_to(WORKSPACE)) + "/"
    for path, addr in session.store.path_to_addr.items():
        if not path.startswith(note_prefix):
            continue
        if path.endswith(".statements.md"):
            continue
        if not session.active_links("note", to_set=[addr]):
            continue
        m = pattern.search(path)
        if not m:
            continue
        label = m.group(0)
        if asn_filter is not None and label not in asn_filter:
            continue
        yield label, addr


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "asn", nargs="*", type=int,
        help="Optional ASN numbers to restrict the audit to. "
             "Default: every active note.",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Also print notes whose deps fully resolve (default: only "
             "report notes with at least one skip).",
    )
    args = parser.parse_args()

    asn_filter = None
    if args.asn:
        asn_filter = {format_label(n) for n in args.asn}

    total_notes = 0
    notes_with_skips = 0
    total_skips = 0

    with open_session(LATTICE) as session:
        for label, note_addr in _iter_active_notes(session, asn_filter):
            total_notes += 1
            declared, resolved, skipped = _audit_one_note(session, note_addr)
            if not skipped and not args.verbose:
                continue
            if skipped:
                notes_with_skips += 1
                total_skips += len(skipped)
            skip_repr = (
                ", ".join(
                    f"ASN-{d:04d}:{r}" for d, r in skipped
                ) if skipped else "(none)"
            )
            print(
                f"  {label}  declared={declared}  resolved={resolved}  "
                f"skipped=[{skip_repr}]",
                file=sys.stderr,
            )

    print(
        f"\n  audit: {total_notes} notes scanned, "
        f"{notes_with_skips} with skips, {total_skips} total skips",
        file=sys.stderr,
    )

    return 1 if notes_with_skips else 0


if __name__ == "__main__":
    sys.exit(main())
