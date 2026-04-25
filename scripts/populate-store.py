#!/usr/bin/env python3
"""Populate the protocol substrate's structural layer from claim YAML/MD artifacts.

Walks every ASN under the lattice's claim-convergence directory and ensures
claim, contract.<kind>, and citation links exist in the store.
Idempotent: re-running adds only newly-discovered links.

Usage:
    python3 scripts/populate-store.py [--dry-run]

Exit code:
    0   normal completion
    1   completion with unresolved labels (some `depends:` entry referenced
        a label not found in any ASN; check stderr for the (claim, label) list)
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from store.store import Store
from store.populate import populate_structural


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Inspect what would be created without writing to the store.",
    )
    args = parser.parse_args()

    if args.dry_run:
        return _dry_run()
    return _live_run()


def _live_run():
    store = Store()
    try:
        stats = populate_structural(store)
    finally:
        store.close()
    return _report(stats)


def _dry_run():
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        store = Store(
            log_path=Path(tmp) / "links.jsonl",
            index_path=Path(tmp) / "index.db",
        )
        try:
            stats = populate_structural(store)
        finally:
            store.close()
    print("(dry run — no changes written to the live store)", file=sys.stderr)
    return _report(stats)


def _report(stats):
    print(file=sys.stderr)
    print(f"  claims_seen:       {stats['claims_seen']}", file=sys.stderr)
    print(f"  claims_added:      {stats['claims_added']}", file=sys.stderr)
    print(f"  contracts_added:   {stats['contracts_added']}", file=sys.stderr)
    print(f"  citations_seen:    {stats['citations_seen']}", file=sys.stderr)
    print(f"  citations_added:   {stats['citations_added']}", file=sys.stderr)

    unresolved = stats["unresolved_labels"]
    if unresolved:
        print(file=sys.stderr)
        print(f"  unresolved labels ({len(unresolved)}):", file=sys.stderr)
        for claim_label, dep_label in unresolved:
            print(f"    {claim_label} → {dep_label}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
