#!/usr/bin/env python3
"""One-off migration: split substrate findings by kind (claim vs note).

Before:
    lattices/<lattice>/_store/documents/findings/<asn>/...

After:
    lattices/<lattice>/_store/documents/findings/claims/<asn>/...
    (notes/ created lazily when note-convergence first emits findings)

Existing findings come from claim convergence — there's no historical note
findings to relocate. The migration moves every direct-child ASN dir under
findings/ into findings/claims/, then rewrites links.jsonl prefixes and
rebuilds the index.

Idempotent: re-running on a migrated store is a no-op.

Usage:
    python3 scripts/migrate-findings-by-kind.py --apply
    python3 scripts/migrate-findings-by-kind.py --dry-run  (default)
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from shared.paths import (
    LATTICE, WORKSPACE, DOCUVERSE_DOCS_DIR, DOCUVERSE_LOG,
    CLAIM_FINDINGS_DIR,
)
from store.store import Store


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    grp = ap.add_mutually_exclusive_group()
    grp.add_argument("--apply", action="store_true",
                     help="perform the migration (default is dry-run)")
    grp.add_argument("--dry-run", action="store_true", default=True)
    args = ap.parse_args()
    apply_mode = args.apply

    label = "APPLY" if apply_mode else "DRY-RUN"
    print(f"[migrate-findings-by-kind] {label}")
    print(f"  DOCUVERSE_DOCS_DIR     = {DOCUVERSE_DOCS_DIR.relative_to(WORKSPACE)}")
    print(f"  CLAIM_FINDINGS_DIR = {CLAIM_FINDINGS_DIR.relative_to(WORKSPACE)}")
    print()

    findings_dir = DOCUVERSE_DOCS_DIR / "findings"
    if not findings_dir.exists():
        print(f"  no findings/ dir found at {findings_dir}", file=sys.stderr)
        return 1

    # Plan moves: every direct-child of findings/ that is an ASN-NNNN dir
    # gets relocated under findings/claims/. claims/ and notes/ are skipped.
    moves = []
    for child in sorted(findings_dir.iterdir()):
        if not child.is_dir():
            continue
        if child.name in ("claims", "notes"):
            continue
        target = CLAIM_FINDINGS_DIR / child.name
        if target.exists():
            print(f"  ! both exist: {child} and {target}; skipping",
                  file=sys.stderr)
            continue
        moves.append((child, target))

    print(f"  Moves planned ({len(moves)}):")
    for old, new in moves:
        print(f"    {old.relative_to(WORKSPACE)}  →  "
              f"{new.relative_to(WORKSPACE)}")
    print()

    # Plan JSONL prefix rewrite.
    lattice_rel = LATTICE.relative_to(WORKSPACE)
    prefix_old = f"{lattice_rel}/_store/documents/findings/"
    prefix_new = f"{lattice_rel}/_store/documents/findings/claims/"

    # Skip entries already under claims/ or notes/ (idempotency): the
    # _path_replace test only matches the bare prefix, so a path that already
    # starts with `findings/claims/` would be doubly-rewritten to
    # `findings/claims/claims/`. Guard against that here.
    print(f"  JSONL prefix rewrite:")
    print(f"    {prefix_old}  →  {prefix_new}")
    print(f"    (skipping entries already under findings/claims/ or "
          f"findings/notes/)")
    print()

    modified = _count_modified(DOCUVERSE_LOG, prefix_old, prefix_new)
    print(f"  links.jsonl: {modified} records would be rewritten")
    print()

    if not apply_mode:
        print("  (dry-run; no changes made. Use --apply to migrate.)")
        return 0

    # APPLY.
    CLAIM_FINDINGS_DIR.mkdir(parents=True, exist_ok=True)
    for old, new in moves:
        new.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(old), str(new))
        print(f"  moved {old.relative_to(WORKSPACE)} → "
              f"{new.relative_to(WORKSPACE)}")

    actual = _rewrite_jsonl(DOCUVERSE_LOG, prefix_old, prefix_new)
    print(f"  links.jsonl: rewrote {actual} records")

    # Rebuild the index from the migrated JSONL.
    store = Store()
    try:
        store.rebuild_index()
    finally:
        store.close()
    print(f"  index.db: rebuilt from migrated JSONL")
    print()
    print("  Migration applied.")
    return 0


def _should_rewrite(entry, prefix_old, prefix_new):
    """True iff entry starts with prefix_old AND is not already under one
    of the kind subdirs (claims/, notes/)."""
    if not isinstance(entry, str) or not entry.startswith(prefix_old):
        return False
    rest = entry[len(prefix_old):]
    return not (rest.startswith("claims/") or rest.startswith("notes/"))


def _count_modified(jsonl_path, prefix_old, prefix_new):
    if not jsonl_path.exists():
        return 0
    modified = 0
    with open(jsonl_path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            record = json.loads(line)
            changed = False
            for field in ("from_set", "to_set"):
                if field in record:
                    for entry in record[field]:
                        if _should_rewrite(entry, prefix_old, prefix_new):
                            changed = True
                            break
                if changed:
                    break
            if changed:
                modified += 1
    return modified


def _rewrite_jsonl(jsonl_path, prefix_old, prefix_new):
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
                        if _should_rewrite(entry, prefix_old, prefix_new):
                            entry = prefix_new + entry[len(prefix_old):]
                            changed = True
                        new_list.append(entry)
                    record[field] = new_list
            out_lines.append(json.dumps(record, sort_keys=True))
            if changed:
                modified += 1
    with open(jsonl_path, "w") as f:
        for line in out_lines:
            f.write(line + "\n")
    return modified


if __name__ == "__main__":
    sys.exit(main())
