#!/usr/bin/env python3
"""One-shot migration: rewrite bare `citation` links to `citation.depends`.

Until now, all citation links recorded a backward dependency under the
bare `citation` type. The schema now requires a subtype: `citation.depends`
for backward and `citation.forward` for forward references. Existing data
needs to be migrated to the new naming.

The migration mutates the JSONL log in place — it changes only the
`type_set` field on `create` records whose type is exactly `citation`.
The link `id` is preserved (so retraction targets and other link-to-link
references stay valid). The SQLite index is rebuilt from the migrated
JSONL.

Usage:
    python3 scripts/migration_tools/migrate-citation-subtypes.py --dry-run
    python3 scripts/migration_tools/migrate-citation-subtypes.py --apply
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from shared.paths import LATTICE
from store.store import Store


LATTICES_ROOT = Path(__file__).resolve().parent.parent.parent / "lattices"


def lattice_log_paths():
    """Return list of links.jsonl paths across all lattices in the repo."""
    return sorted(LATTICES_ROOT.glob("*/_docuverse/links.jsonl"))


def migrate_log(log_path, *, apply):
    """Rewrite bare `citation` records in `log_path` to `citation.depends`.

    Returns (rewritten_count, total_records).
    """
    if not log_path.exists():
        return 0, 0

    rewritten = 0
    total = 0
    out_lines = []
    with open(log_path) as f:
        for line in f:
            stripped = line.rstrip("\n")
            if not stripped.strip():
                out_lines.append(line)
                continue
            total += 1
            record = json.loads(stripped)
            if (record.get("op") == "create"
                    and record.get("type_set") == ["citation"]):
                record["type_set"] = ["citation.depends"]
                rewritten += 1
                out_lines.append(json.dumps(record) + "\n")
            else:
                out_lines.append(line if line.endswith("\n") else line + "\n")

    if apply and rewritten:
        log_path.write_text("".join(out_lines))

    return rewritten, total


def rebuild_lattice_index(log_path):
    """Rebuild the SQLite index for the lattice that owns `log_path`.

    Sets the substrate root to the lattice directory and calls
    `Store.rebuild_index()`.
    """
    import os
    lattice_dir = log_path.parent.parent
    prior = os.environ.get("XANADU_LATTICE_ROOT")
    os.environ["XANADU_LATTICE_ROOT"] = str(lattice_dir)
    try:
        store = Store()
        try:
            store.rebuild_index()
        finally:
            store.close()
    finally:
        if prior is None:
            os.environ.pop("XANADU_LATTICE_ROOT", None)
        else:
            os.environ["XANADU_LATTICE_ROOT"] = prior


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true",
                        help="Write changes (default: dry-run)")
    args = parser.parse_args()

    apply = args.apply
    mode = "APPLY" if apply else "DRY-RUN"
    print(f"[{mode}] migrating bare citation → citation.depends across all lattices")

    grand_rewritten = 0
    grand_total = 0
    for log_path in lattice_log_paths():
        rewritten, total = migrate_log(log_path, apply=apply)
        grand_rewritten += rewritten
        grand_total += total
        rel = log_path.relative_to(LATTICES_ROOT.parent)
        print(f"  {rel}: {rewritten} / {total} records rewritten")
        if apply and rewritten:
            rebuild_lattice_index(log_path)
            print(f"  {rel}: SQLite index rebuilt")

    print(f"\nTotal: {grand_rewritten} citation links rewritten "
          f"across {grand_total} records")
    if not apply:
        print("(dry-run — re-run with --apply to write changes)")


if __name__ == "__main__":
    main()
