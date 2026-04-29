#!/usr/bin/env python3
"""One-off migration: move substrate-managed documents under _store/documents/.

Before:
    lattices/<lattice>/_store/findings/<asn>/...
    lattices/<lattice>/_store/rationales/...
    lattices/<lattice>/_store/agents/<role>.md  (just-added; usually empty)

After:
    lattices/<lattice>/_store/documents/findings/<asn>/...
    lattices/<lattice>/_store/documents/rationales/...
    lattices/<lattice>/_store/documents/agents/<role>.md

links.jsonl is rewritten so every from_set / to_set entry matching the old
prefix uses the new prefix. Link ids stay untouched (they're content-hashed
and we don't re-derive). The index.db is dropped and rebuilt from the
migrated JSONL.

Idempotent: re-running on a migrated store is a no-op.

Usage:
    python3 scripts/migration_tools/migrate-store-documents-dir.py --apply
    python3 scripts/migration_tools/migrate-store-documents-dir.py --dry-run  (default)
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from shared.paths import LATTICE, WORKSPACE, DOCUVERSE_DIR, DOCUVERSE_DOCS_DIR, DOCUVERSE_LOG
from store.store import Store


OLD_KIND_DIRS = ("findings", "rationales", "agents")


def _path_replace(s, prefix_old, prefix_new):
    if isinstance(s, str) and s.startswith(prefix_old):
        return prefix_new + s[len(prefix_old):]
    return s


def migrate_jsonl(jsonl_path, prefix_old_to_new, dry_run=True):
    """Read jsonl_path; rewrite from_set/to_set entries using the prefix map.
    Returns the number of records modified.
    """
    if not jsonl_path.exists():
        return 0
    out_lines = []
    modified = 0
    with open(jsonl_path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                out_lines.append(line)
                continue
            record = json.loads(line)
            changed = False
            for field in ("from_set", "to_set"):
                if field in record:
                    new_list = []
                    for entry in record[field]:
                        rewritten = entry
                        for old_pref, new_pref in prefix_old_to_new.items():
                            rewritten = _path_replace(rewritten, old_pref, new_pref)
                        if rewritten != entry:
                            changed = True
                        new_list.append(rewritten)
                    record[field] = new_list
            out_lines.append(json.dumps(record, sort_keys=True))
            if changed:
                modified += 1
    if not dry_run:
        with open(jsonl_path, "w") as f:
            for line in out_lines:
                f.write(line + "\n")
    return modified


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    grp = ap.add_mutually_exclusive_group()
    grp.add_argument("--apply", action="store_true",
                     help="perform the migration (default is dry-run)")
    grp.add_argument("--dry-run", action="store_true", default=True)
    args = ap.parse_args()
    apply_mode = args.apply

    label = "APPLY" if apply_mode else "DRY-RUN"
    print(f"[migrate-store-documents-dir] {label}")
    print(f"  DOCUVERSE_DIR        = {DOCUVERSE_DIR.relative_to(WORKSPACE)}")
    print(f"  DOCUVERSE_DOCS_DIR   = {DOCUVERSE_DOCS_DIR.relative_to(WORKSPACE)}")
    print()

    if not DOCUVERSE_DIR.exists():
        print(f"  no DOCUVERSE_DIR found at {DOCUVERSE_DIR}", file=sys.stderr)
        return 1

    # Plan the moves.
    moves = []
    for kind in OLD_KIND_DIRS:
        old = DOCUVERSE_DIR / kind
        new = DOCUVERSE_DOCS_DIR / kind
        if old.exists() and not new.exists():
            moves.append((old, new))
        elif old.exists() and new.exists():
            print(f"  ! both exist: {old} and {new}; skipping",
                  file=sys.stderr)

    print(f"  Moves planned ({len(moves)}):")
    for old, new in moves:
        print(f"    {old.relative_to(WORKSPACE)}  →  "
              f"{new.relative_to(WORKSPACE)}")
    print()

    # Plan JSONL prefix rewrites. JSONL stores paths relative to WORKSPACE.
    lattice_rel = LATTICE.relative_to(WORKSPACE)
    prefix_old_to_new = {}
    for kind in OLD_KIND_DIRS:
        old_pref = f"{lattice_rel}/_store/{kind}/"
        new_pref = f"{lattice_rel}/_store/documents/{kind}/"
        prefix_old_to_new[old_pref] = new_pref

    print(f"  JSONL prefix rewrites:")
    for old, new in prefix_old_to_new.items():
        print(f"    {old}  →  {new}")
    print()

    # Dry-run JSONL pass.
    modified = migrate_jsonl(DOCUVERSE_LOG, prefix_old_to_new, dry_run=True)
    print(f"  links.jsonl: {modified} records would be rewritten")
    print()

    if not apply_mode:
        print("  (dry-run; no changes made. Use --apply to migrate.)")
        return 0

    # APPLY.
    DOCUVERSE_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    for old, new in moves:
        new.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(old), str(new))
        print(f"  moved {old.relative_to(WORKSPACE)} → "
              f"{new.relative_to(WORKSPACE)}")

    actual = migrate_jsonl(DOCUVERSE_LOG, prefix_old_to_new, dry_run=False)
    print(f"  links.jsonl: rewrote {actual} records")

    # Rebuild the index from the migrated JSONL.
    store = Store()
    try:
        store.rebuild_index()
    finally:
        store.close()
    print(f"  index.db: rebuilt from migrated JSONL")
    print()
    print("  Migration applied. Substrate diff under "
          f"{DOCUVERSE_DIR.relative_to(WORKSPACE)}/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
