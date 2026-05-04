#!/usr/bin/env python3
"""One-shot backfill: emit provenance.derivation from notes to claims.

transclude.py emits `provenance.derivation` from a source note to
each claim it produces. Existing ASNs predate that emission, so the
substrate has no note-rooted derivations — only review→finding and
citation-resolve→claim derivations.

The new Address-keyed `is_asn_converged` walks note→claim derivations
forward to find an ASN's claim cluster. Without these links, the
predicate trivially returns True on every existing note.

This script files the missing links for one or more ASNs by walking
the filesystem (`_docuverse/documents/claim/<ASN>/*.md`, excluding
attribute sidecars) and emitting one derivation per claim.

Idempotent — re-running is safe.

Usage:
    python scripts/migrate-note-claim-derivation.py 34
    python scripts/migrate-note-claim-derivation.py 34 36
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.backend.emit import emit_derivation
from lib.backend.schema import ATTRIBUTE_SUFFIXES
from lib.protocols.febe.session import open_session
from lib.shared.common import find_asn
from lib.shared.paths import CLAIM_DIR, LATTICE


def migrate_asn(session, asn_label: str) -> dict:
    """Backfill note→claim derivations for one ASN."""
    asn_num = int(asn_label[4:])
    asn_path, _ = find_asn(str(asn_num))
    if asn_path is None:
        return {"error": f"no note found for {asn_label}"}

    note_rel = str(asn_path.relative_to(LATTICE))
    note_addr = session.get_addr_for_path(note_rel)
    if note_addr is None:
        return {"error": f"note path not registered: {note_rel}"}

    claim_dir = CLAIM_DIR / asn_label
    if not claim_dir.exists():
        return {"error": f"no claim dir: {claim_dir}"}

    stats = {"claims_seen": 0, "links_emitted": 0, "already_present": 0}
    for md_path in sorted(claim_dir.glob("*.md")):
        if md_path.name.startswith("_"):
            continue
        if md_path.name.endswith(ATTRIBUTE_SUFFIXES):
            continue
        stats["claims_seen"] += 1

        claim_rel = str(md_path.relative_to(LATTICE))
        claim_addr = session.get_addr_for_path(claim_rel)
        if claim_addr is None:
            print(
                f"  [SKIP] {claim_rel}: not registered in substrate",
                file=sys.stderr,
            )
            continue

        _, created = emit_derivation(session.store, note_addr, claim_addr)
        if created:
            stats["links_emitted"] += 1
        else:
            stats["already_present"] += 1

    print(
        f"  {asn_label}: {stats['claims_seen']} claims, "
        f"{stats['links_emitted']} new links, "
        f"{stats['already_present']} already present",
        file=sys.stderr,
    )
    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Backfill provenance.derivation note→claim links.",
    )
    parser.add_argument("asns", nargs="+", help="ASN numbers (e.g., 34)")
    args = parser.parse_args()

    session = open_session(LATTICE)
    overall = {"claims_seen": 0, "links_emitted": 0, "already_present": 0}

    for raw in args.asns:
        asn_num = int(re.sub(r"\D", "", raw))
        asn_label = f"ASN-{asn_num:04d}"
        print(f"\n=== {asn_label} ===", file=sys.stderr)
        stats = migrate_asn(session, asn_label)
        if "error" in stats:
            print(f"  {stats['error']}", file=sys.stderr)
            continue
        for k, v in stats.items():
            overall[k] += v

    print(
        f"\n[TOTAL] claims={overall['claims_seen']} "
        f"emitted={overall['links_emitted']} "
        f"already-present={overall['already_present']}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
