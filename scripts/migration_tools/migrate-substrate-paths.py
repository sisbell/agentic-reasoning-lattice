#!/usr/bin/env python3
"""One-shot migration: rewrite path-string prefixes in a substrate JSONL.

Used after a directory rename inside a lattice leaves substrate links
pointing at old paths. Pure mechanical prefix substitution applied to
every string in each link's `from_set` and `to_set`.

Default substitution corresponds to the formalization → claim-convergence
rename:

    lattices/xanadu/formalization/ → lattices/xanadu/claim-convergence/

Override or add substitutions with `--substitution OLD=NEW` (repeatable).

Usage:
    python scripts/migration_tools/migrate-substrate-paths.py
    python scripts/migration_tools/migrate-substrate-paths.py --dry-run
    python scripts/migration_tools/migrate-substrate-paths.py --substitution old/=new/

After migration, the SQLite index is rebuilt from the migrated JSONL.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from shared.paths import DOCUVERSE_LOG
from shared.migrate_substrate_paths import migrate_paths
from store.store import Store


DEFAULT_SUBSTITUTIONS = {
    "lattices/xanadu/formalization/": "lattices/xanadu/claim-convergence/",
}


def _parse_substitution(s):
    if "=" not in s:
        raise argparse.ArgumentTypeError(
            f"--substitution must be OLD=NEW, got: {s!r}"
        )
    old, new = s.split("=", 1)
    return old, new


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Report the change count without writing.",
    )
    parser.add_argument(
        "--substitution", action="append", type=_parse_substitution,
        metavar="OLD=NEW", default=None,
        help="Add a prefix substitution. Repeatable. If any --substitution "
             "is given, the default substitution is replaced.",
    )
    parser.add_argument(
        "--jsonl", default=str(DOCUVERSE_LOG),
        help=f"Path to substrate JSONL (default: {DOCUVERSE_LOG}).",
    )
    args = parser.parse_args()

    if args.substitution:
        substitutions = dict(args.substitution)
    else:
        substitutions = DEFAULT_SUBSTITUTIONS

    print("Substitutions:", file=sys.stderr)
    for old, new in substitutions.items():
        print(f"  {old} → {new}", file=sys.stderr)
    print(f"Target JSONL: {args.jsonl}", file=sys.stderr)

    changed = migrate_paths(args.jsonl, substitutions, dry_run=args.dry_run)

    if args.dry_run:
        print(f"[dry-run] Would change {changed} link(s).", file=sys.stderr)
        return 0

    print(f"Migrated {changed} link(s).", file=sys.stderr)

    if changed == 0:
        print("No changes — index rebuild skipped.", file=sys.stderr)
        return 0

    print("Rebuilding SQLite index from migrated JSONL...", file=sys.stderr)
    store = Store()
    try:
        store.rebuild_index()
    finally:
        store.close()
    print("Done.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
