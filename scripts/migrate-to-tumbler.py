#!/usr/bin/env python3
"""Migrate the legacy path-keyed substrate to a tumbler-keyed substrate.

Reads `lattices/<lattice>/_docuverse/links.jsonl` and writes
`lattices/<lattice>/_substrate/{links.jsonl,paths.json}`.

Usage:
    python3 scripts/migrate-to-tumbler.py [--lattice xanadu] [--dry-run]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from backend.migrate import migrate  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--lattice",
        default="xanadu",
        help="lattice directory under lattices/ to migrate",
    )
    parser.add_argument(
        "--legacy-jsonl",
        default=None,
        help="override path to legacy links.jsonl",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="override output directory (defaults to lattices/<lattice>/_substrate)",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    lattice_dir = repo_root / "lattices" / args.lattice
    legacy = (
        Path(args.legacy_jsonl)
        if args.legacy_jsonl
        else lattice_dir / "_docuverse" / "links.jsonl"
    )
    output = (
        Path(args.output_dir)
        if args.output_dir
        else lattice_dir / "_substrate"
    )

    if not legacy.exists():
        print(f"ERROR: legacy JSONL not found: {legacy}", file=sys.stderr)
        return 2

    print(f"Migrating: {legacy}")
    print(f"Output dir: {output}")
    counts = migrate(legacy, output, lattice_name=args.lattice)
    print(f"\nResults:")
    print(f"  Docs allocated:        {counts['docs']:>6}")
    print(f"  Lattice links emitted: {counts['lattice_links']:>6}")
    print(f"  Legacy links replayed: {counts['legacy_links']:>6}")
    print(f"  Total links written:   "
          f"{counts['lattice_links'] + counts['legacy_links']:>6}")
    print(f"\nWritten:")
    print(f"  {output / 'links.jsonl'}")
    print(f"  {output / 'paths.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
