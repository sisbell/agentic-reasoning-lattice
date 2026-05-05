#!/usr/bin/env python3
"""One-shot backfill: register the claim-statements view doc for
existing ASNs.

`transclude.py` emits the view substrate facts (path registration,
`view.claim-statements` classifier, `provenance.derivation`
note→view) for every ASN it processes. ASNs that were transcluded
before that change need backfill — without it, the renderer has
nothing to dispatch on.

Idempotent: re-running on an already-backfilled ASN is a no-op
(`emit_view` and `emit_derivation` both early-return on existing
links; `register_path` is get-or-allocate).

Usage:
    python scripts/migrate-claim-statements-view.py 34
    python scripts/migrate-claim-statements-view.py 34 36
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.backend.emit import emit_derivation, emit_view
from lib.protocols.febe.session import open_session
from lib.shared.common import find_asn
from lib.shared.paths import LATTICE, view_path


def migrate_asn(session, asn_label: str) -> dict:
    """Backfill the view doc + classifier + derivation for one ASN."""
    asn_num = int(asn_label[4:])
    asn_path, _ = find_asn(str(asn_num))
    if asn_path is None:
        return {"error": f"no note found for {asn_label}"}

    note_rel = str(asn_path.relative_to(LATTICE))
    note_addr = session.get_addr_for_path(note_rel)
    if note_addr is None:
        return {"error": f"note path not registered: {note_rel}"}

    view_rel = str(
        view_path(asn_label, "claim-statements")
        .resolve().relative_to(LATTICE.resolve())
    )
    view_addr = session.register_path(view_rel)

    _, view_created = emit_view(
        session.store, view_addr, "claim-statements",
    )
    _, deriv_created = emit_derivation(
        session.store, note_addr, view_addr,
    )

    return {
        "view_addr": str(view_addr),
        "view_classifier_emitted": view_created,
        "derivation_emitted": deriv_created,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Backfill claim-statements view docs.",
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
            f"  {asn_label}: view_addr={stats['view_addr']} "
            f"classifier_new={stats['view_classifier_emitted']} "
            f"derivation_new={stats['derivation_emitted']}",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
