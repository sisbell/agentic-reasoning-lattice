#!/usr/bin/env python3
"""One-shot backfill: register the note's `statements` attribute
sidecar from the legacy `manifests/<asn>/claim-statements.md` file,
then emit supersession from the extracted doc to the existing
view.claim-statements view doc.

ASNs that went through note-assembly under the old workflow have
their LLM-extracted formal statements at
`manifests/<asn>/claim-statements.md` — outside docuverse, not a
substrate citizen. The new architecture lives the extraction at
`_docuverse/documents/note/<note-stem>.statements.md` with a
`statements` attribute link from note → sidecar; post-derivation,
a supersession link makes the view doc the chain's head.

Idempotent — re-running is safe (emit_attribute is content-
idempotent; emit_supersession is idempotent on the (from, to) pair).

Usage:
    python scripts/migrate-note-statements.py 34
    python scripts/migrate-note-statements.py 34 36
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.backend.emit import emit_supersession
from lib.lattice.attributes import emit_attribute
from lib.predicates import statements_sidecar_of, supersession_head
from lib.protocols.febe.session import open_session
from lib.shared.common import find_asn
from lib.shared.paths import LATTICE, MANIFESTS_DIR, view_path


def migrate_asn(session, asn_label: str) -> dict:
    """Backfill statements + supersession for one ASN."""
    asn_num = int(asn_label[4:])
    asn_path, _ = find_asn(str(asn_num))
    if asn_path is None:
        return {"error": f"no note found for {asn_label}"}

    legacy = MANIFESTS_DIR / asn_label / "claim-statements.md"
    if not legacy.exists():
        return {"error": f"no legacy file: {legacy}"}

    note_rel = str(asn_path.relative_to(LATTICE))
    note_addr = session.get_addr_for_path(note_rel)
    if note_addr is None:
        return {"error": f"note not registered: {note_rel}"}

    body = legacy.read_text()
    # 1. Emit the statements attribute (creates sidecar doc + link).
    _, attr_created = emit_attribute(
        session, note_rel, "statements", body,
    )

    # 2. Find the view doc, emit supersession from extracted_head → view.
    view_rel = str(
        view_path(asn_label, "claim-statements")
        .resolve().relative_to(LATTICE.resolve())
    )
    view_addr = session.get_addr_for_path(view_rel)

    sup_created = False
    if view_addr is not None:
        stmt_addr = statements_sidecar_of(session, note_addr)
        if stmt_addr is not None:
            head = supersession_head(session, stmt_addr)
            _, sup_created = emit_supersession(
                session.store, head, view_addr,
            )

    return {
        "statements_attr_emitted": attr_created,
        "supersession_emitted": sup_created,
        "view_found": view_addr is not None,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Backfill note→statements + supersession→view.",
    )
    parser.add_argument("asns", nargs="+", help="ASN numbers (e.g., 34)")
    args = parser.parse_args()

    session = open_session(LATTICE)

    for raw in args.asns:
        asn_num = int(re.sub(r"\D", "", raw))
        asn_label = f"ASN-{asn_num:04d}"
        print(f"\n=== {asn_label} ===", file=sys.stderr)
        stats = migrate_asn(session, asn_label)
        if "error" in stats:
            print(f"  {stats['error']}", file=sys.stderr)
            continue
        print(
            f"  {asn_label}: stmt_attr_new={stats['statements_attr_emitted']} "
            f"supersession_new={stats['supersession_emitted']} "
            f"view_found={stats['view_found']}",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
