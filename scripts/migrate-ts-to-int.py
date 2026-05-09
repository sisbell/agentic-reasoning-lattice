#!/usr/bin/env python3
"""One-time migration: rewrite JSONL `ts` fields from ISO-8601 strings
to Unix epoch seconds (int).

Substrate now stores `ts` as Unix int seconds (compact + fast
comparison; per `feedback_ts_scoped_to_agentic.md` for the agentic-
concerns scope of ts use). Existing JSONL records carry `ts` as
ISO-8601 strings; this script rewrites them in place.

Backward-compat at read time means data loads correctly without
running this script — it's a cleanup pass for storage compactness
and consistency. Safe to run multiple times (already-int records
are left untouched).

Usage:
    python scripts/migrate-ts-to-int.py [LATTICE_PATH ...]

If no arguments are given, migrates the default lattice.
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


def _parse_ts(raw):
    if isinstance(raw, int):
        return raw
    if isinstance(raw, float):
        return int(raw)
    if isinstance(raw, str):
        try:
            normalized = raw.replace("Z", "+00:00")
            dt = datetime.fromisoformat(normalized)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return int(dt.timestamp())
        except ValueError:
            return None
    return None


def migrate_jsonl(jsonl_path: Path) -> tuple[int, int]:
    """Rewrite `ts` fields in `jsonl_path` from ISO to Unix int.

    Returns (rewritten_count, already_int_count).
    """
    if not jsonl_path.exists():
        return (0, 0)

    rewritten = 0
    already_int = 0
    out_lines = []

    with open(jsonl_path) as f:
        for line in f:
            stripped = line.strip()
            if not stripped:
                out_lines.append(line)
                continue
            record = json.loads(stripped)
            raw_ts = record.get("ts")
            if isinstance(raw_ts, int):
                already_int += 1
                out_lines.append(line)
                continue
            new_ts = _parse_ts(raw_ts)
            if new_ts is None:
                # Unparseable — leave unchanged
                out_lines.append(line)
                continue
            record["ts"] = new_ts
            rewritten += 1
            out_lines.append(json.dumps(record, sort_keys=True) + "\n")

    if rewritten > 0:
        # Atomic write via tempfile + rename
        tmp_path = jsonl_path.with_suffix(jsonl_path.suffix + ".migrate-tmp")
        with open(tmp_path, "w") as f:
            f.writelines(out_lines)
        tmp_path.replace(jsonl_path)

    return (rewritten, already_int)


def main() -> int:
    if len(sys.argv) > 1:
        lattice_paths = [Path(p) for p in sys.argv[1:]]
    else:
        # Default: the canonical lattice in this repo
        repo_root = Path(__file__).resolve().parent.parent
        lattice_paths = [repo_root / "lattices" / "xanadu"]

    total_rewritten = 0
    total_already_int = 0

    for lattice in lattice_paths:
        jsonl_path = lattice / "_docuverse" / "links.jsonl"
        if not jsonl_path.exists():
            print(
                f"  [MIGRATE-TS] no JSONL at {jsonl_path}; skipping",
                file=sys.stderr,
            )
            continue

        start = time.time()
        rewritten, already_int = migrate_jsonl(jsonl_path)
        elapsed = time.time() - start
        total_rewritten += rewritten
        total_already_int += already_int

        print(
            f"  [MIGRATE-TS] {jsonl_path}: rewrote {rewritten}, "
            f"left {already_int} already-int ({elapsed:.1f}s)",
            file=sys.stderr,
        )

    print(
        f"  [MIGRATE-TS] total rewritten: {total_rewritten}; "
        f"total already-int: {total_already_int}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
