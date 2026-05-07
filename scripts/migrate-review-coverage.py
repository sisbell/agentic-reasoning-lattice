#!/usr/bin/env python3
"""One-shot backfill: emit review.coverage for past cone reviews.

Cone reviews emitted before the review.coverage link type existed have
no substrate coverage record. The quiescence predicate
`is_claim_confirmed` reads that record to decide whether to re-fire,
so without backfill, every previously-quiescent cone gets one extra
review pass on the next sweep.

This script walks every active `review` classifier, parses the meta
doc's title, and — for titles matching the cone-review patterns —
emits `review.coverage` links for the apex + its current same-ASN deps.

Coverage scope is reconstructed from the CURRENT dep graph
(transitive citation.depends from the apex). For long-stable ASNs
this matches the scope at review time. For actively-evolving ASNs the
reconstructed scope may differ from the original; that's an
acceptable cost for a one-shot migration.

Usage:
    python scripts/migrate-review-coverage.py 34
    python scripts/migrate-review-coverage.py 34 36 40
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.agents.producers.cone_review import transitive_same_asn_deps
from lib.backend.emit import emit_review_coverage
from lib.lattice.labels import build_cross_asn_label_index
from lib.protocols.febe.session import open_session
from lib.shared.claim_files import build_label_index
from lib.shared.paths import CLAIM_DIR, LATTICE


# Title patterns:
#   # Cone Review — ASN-0034/T7
#   # Cone Review — ASN-0034/T7 (cycle 3)
#   # Cone Review (Confirmation) — ASN-0034/T7
_CONE_TITLE = re.compile(
    r"^#\s+Cone Review(?:\s*\(Confirmation\))?\s*—\s*"
    r"(ASN-\d{4})/(\S+?)(?:\s*\(cycle\s+\d+\))?\s*$"
)


def _parse_cone_title(first_line: str) -> tuple[str, str] | None:
    """Return (asn_label, apex_label) or None if not a cone review."""
    m = _CONE_TITLE.match(first_line.strip())
    if not m:
        return None
    return m.group(1), m.group(2)


def migrate_asn(session, asn_label: str) -> dict:
    """Backfill review.coverage for one ASN. Returns stats dict."""
    label_index = build_cross_asn_label_index(session.store)
    rev_index = {a: lbl for lbl, a in label_index.items()}

    claim_dir = CLAIM_DIR / asn_label
    if not claim_dir.exists():
        return {"error": f"no claim dir for {asn_label}"}
    asn_labels = set(build_label_index(claim_dir).keys())

    lattice_root = session.store.lattice_dir.resolve()

    stats = {
        "reviewed": 0,
        "skipped_non_cone": 0,
        "skipped_unknown_apex": 0,
        "cone_reviews": 0,
        "coverage_links_emitted": 0,
    }

    for link in session.active_links("review"):
        for meta_addr in link.to_set:
            stats["reviewed"] += 1

            meta_path = session.get_path_for_addr(meta_addr)
            if meta_path is None:
                continue

            # Filter to this ASN's reviews
            if f"/{asn_label}/" not in meta_path:
                continue

            full_path = lattice_root / meta_path
            if not full_path.exists():
                continue

            try:
                first_line = full_path.read_text().split("\n", 1)[0]
            except OSError:
                continue

            parsed = _parse_cone_title(first_line)
            if parsed is None:
                stats["skipped_non_cone"] += 1
                continue

            parsed_asn, apex_label = parsed
            if parsed_asn != asn_label:
                # Title says different ASN; skip
                continue

            apex_addr = label_index.get(apex_label)
            if apex_addr is None:
                stats["skipped_unknown_apex"] += 1
                print(
                    f"  [SKIP] {meta_path}: apex {apex_label!r} not in "
                    f"current label index",
                    file=sys.stderr,
                )
                continue

            stats["cone_reviews"] += 1

            # Reconstruct cone scope from current substrate state
            dep_labels = transitive_same_asn_deps(
                session, apex_addr, asn_labels, rev_index,
            )
            covered = [apex_addr] + [
                label_index[d] for d in dep_labels if d in label_index
            ]

            for target in covered:
                _, created = emit_review_coverage(
                    session.store, meta_addr, target,
                )
                if created:
                    stats["coverage_links_emitted"] += 1

            print(
                f"  [BACKFILL] {Path(meta_path).name}: apex={apex_label} "
                f"+ {len(dep_labels)} deps "
                f"({len(covered)} coverage links checked)",
                file=sys.stderr,
            )

    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Backfill review.coverage for past cone reviews.",
    )
    parser.add_argument("asns", nargs="+", help="ASN numbers (e.g., 34 36)")
    args = parser.parse_args()

    session = open_session(LATTICE)
    overall = {
        "reviewed": 0,
        "skipped_non_cone": 0,
        "skipped_unknown_apex": 0,
        "cone_reviews": 0,
        "coverage_links_emitted": 0,
    }

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
            f"  {asn_label}: {stats['cone_reviews']} cone reviews, "
            f"{stats['coverage_links_emitted']} coverage links emitted",
            file=sys.stderr,
        )

    print(
        f"\n[TOTAL] reviewed={overall['reviewed']} "
        f"cone={overall['cone_reviews']} "
        f"non-cone={overall['skipped_non_cone']} "
        f"unknown-apex={overall['skipped_unknown_apex']} "
        f"links-emitted={overall['coverage_links_emitted']}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
