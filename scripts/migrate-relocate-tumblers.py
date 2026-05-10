#!/usr/bin/env python3
"""Relocate every tumbler under a source prefix to a target prefix.

One-shot migration tool for the unified-docuverse arc. Each lattice's
substrate today allocates tumblers under `1.1.0.x`. Merging two
substrates into one root requires that they occupy disjoint tumbler
ranges. This tool rewrites every tumbler matching `<src>.X` to
`<dst>.X` across `paths.json` and `links.jsonl`. The dormant
`index.db` is left alone (no code opens it).

Relocation rule:

    addr `<src>` or `<src>.<rest>` → `<dst>` or `<dst>.<rest>`
    addrs not starting with `<src>` → unchanged

Where rewrite happens:

  - paths.json: `_meta.lattice_doc` (single tumbler) + every value in
    the `paths` map.
  - links.jsonl, every record:
    `id`, `homedoc` (if present), every entry in `from_set`,
    `to_set`, `type_set`.

Idempotent only if src/dst are disjoint (don't run twice with the
same dst as a new src). Dry-run reports counts without writing.

Usage:

    python scripts/migrate-relocate-tumblers.py \\
        --substrate lattices/materials/_docuverse \\
        --src 1.1.0 --dst 1.2.0 [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List


def relocate(addr: str, src: str, dst: str) -> str:
    """Apply the relocation rule to a single tumbler string.

    `addr` matching exactly `src` or starting with `src.` is rewritten
    by replacing the leading `src` with `dst`. Anything else passes
    through unchanged.
    """
    if addr == src:
        return dst
    if addr.startswith(src + "."):
        return dst + addr[len(src):]
    return addr


def _relocate_list(addrs: List[str], src: str, dst: str) -> List[str]:
    return [relocate(a, src, dst) for a in addrs]


def _rewrite_record(record: Dict[str, Any], src: str, dst: str) -> Dict[str, Any]:
    """Return a record with every tumbler-typed field relocated."""
    out = dict(record)
    if "id" in out and isinstance(out["id"], str):
        out["id"] = relocate(out["id"], src, dst)
    if "homedoc" in out and isinstance(out["homedoc"], str):
        out["homedoc"] = relocate(out["homedoc"], src, dst)
    for key in ("from_set", "to_set", "type_set"):
        if key in out and isinstance(out[key], list):
            out[key] = _relocate_list(out[key], src, dst)
    return out


def relocate_paths_json(
    path: Path, src: str, dst: str, *, dry_run: bool,
) -> int:
    """Rewrite paths.json in place. Returns count of tumblers changed."""
    data = json.loads(path.read_text())
    changed = 0

    meta = data.get("_meta", {})
    if "lattice_doc" in meta:
        new = relocate(meta["lattice_doc"], src, dst)
        if new != meta["lattice_doc"]:
            meta["lattice_doc"] = new
            changed += 1

    paths = data.get("paths", {})
    for key, value in list(paths.items()):
        new = relocate(value, src, dst)
        if new != value:
            paths[key] = new
            changed += 1

    if not dry_run and changed:
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(json.dumps(data, indent=2) + "\n")
        tmp.replace(path)
    return changed


def relocate_links_jsonl(
    path: Path, src: str, dst: str, *, dry_run: bool,
) -> tuple[int, int]:
    """Rewrite links.jsonl in place. Returns (records_processed, fields_changed)."""
    fields_changed = 0
    records = 0
    new_lines: List[str] = []

    with path.open() as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                new_lines.append(line)
                continue
            rec = json.loads(line)
            new_rec = _rewrite_record(rec, src, dst)
            records += 1
            if new_rec != rec:
                fields_changed += 1
            new_lines.append(json.dumps(new_rec))

    if not dry_run and fields_changed:
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text("\n".join(new_lines) + "\n")
        tmp.replace(path)
    return records, fields_changed


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="migrate-relocate-tumblers",
        description=(
            "Relocate every tumbler under a source prefix to a target "
            "prefix across paths.json + links.jsonl."
        ),
    )
    parser.add_argument(
        "--substrate", type=Path, required=True,
        help="Substrate directory (the _docuverse/ that holds paths.json + links.jsonl).",
    )
    parser.add_argument(
        "--src", required=True,
        help="Source tumbler prefix to match (e.g., '1.1.0').",
    )
    parser.add_argument(
        "--dst", required=True,
        help="Target tumbler prefix (e.g., '1.2.0').",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Report counts without writing.",
    )
    args = parser.parse_args()

    if args.src == args.dst:
        print("error: src and dst are identical", file=sys.stderr)
        return 1

    substrate: Path = args.substrate.resolve()
    paths_json = substrate / "paths.json"
    links_jsonl = substrate / "links.jsonl"

    if not paths_json.exists():
        print(f"error: {paths_json} not found", file=sys.stderr)
        return 1
    if not links_jsonl.exists():
        print(f"error: {links_jsonl} not found", file=sys.stderr)
        return 1

    print(
        f"  [RELOCATE] substrate={substrate} src={args.src} dst={args.dst}"
        + (" (dry-run)" if args.dry_run else ""),
        file=sys.stderr,
    )

    paths_changed = relocate_paths_json(
        paths_json, args.src, args.dst, dry_run=args.dry_run,
    )
    print(
        f"  [RELOCATE] paths.json: {paths_changed} tumbler(s) "
        f"{'would be ' if args.dry_run else ''}rewritten",
        file=sys.stderr,
    )

    records, fields_changed = relocate_links_jsonl(
        links_jsonl, args.src, args.dst, dry_run=args.dry_run,
    )
    print(
        f"  [RELOCATE] links.jsonl: {fields_changed}/{records} record(s) "
        f"{'would be ' if args.dry_run else ''}rewritten",
        file=sys.stderr,
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
