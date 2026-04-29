"""Library: rewrite path-string prefixes in a substrate JSONL log.

Used when a lattice subdirectory rename leaves substrate links pointing at
old paths. Pure mechanical prefix substitution applied to every string in
each link's `from_set` and `to_set`. Other fields (id, ts, type_set, op)
are untouched.

Atomic: writes to a temp file in the same directory, fsyncs, then renames.
Idempotent: a second pass with the same substitutions is a no-op.

The library function is callable from tests; the CLI wrapper lives in
`scripts/migration_tools/migrate-substrate-paths.py`.
"""

import json
import os
from pathlib import Path


def transform_string(s, substitutions):
    """Apply the first matching prefix substitution. Returns s unchanged if no prefix matches."""
    for old_prefix, new_prefix in substitutions.items():
        if s.startswith(old_prefix):
            return new_prefix + s[len(old_prefix):]
    return s


def transform_link(link, substitutions):
    """Return a new link dict with from_set/to_set strings substituted. Other fields unchanged."""
    out = dict(link)
    out["from_set"] = [transform_string(s, substitutions) for s in link.get("from_set", [])]
    out["to_set"] = [transform_string(s, substitutions) for s in link.get("to_set", [])]
    return out


def migrate_paths(jsonl_path, substitutions, dry_run=False):
    """Rewrite path prefixes in a substrate JSONL.

    Args:
        jsonl_path: Path to the JSONL file (read and overwritten).
        substitutions: dict of {old_prefix: new_prefix}. First match wins.
        dry_run: if True, return the count without writing.

    Returns:
        int — number of lines whose serialized form changed.
    """
    jsonl_path = Path(jsonl_path)
    if not jsonl_path.exists():
        raise FileNotFoundError(f"JSONL not found: {jsonl_path}")

    changed_count = 0
    out_lines = []

    with open(jsonl_path) as f:
        for line in f:
            stripped = line.rstrip("\n")
            if not stripped:
                out_lines.append(stripped)
                continue
            link = json.loads(stripped)
            new_link = transform_link(link, substitutions)
            new_line = json.dumps(new_link, sort_keys=True)
            if new_line != stripped:
                changed_count += 1
            out_lines.append(new_line)

    if dry_run:
        return changed_count

    if changed_count == 0:
        return 0

    tmp_path = jsonl_path.with_suffix(jsonl_path.suffix + ".tmp")
    with open(tmp_path, "w") as f:
        f.write("\n".join(out_lines))
        if out_lines:
            f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, jsonl_path)
    return changed_count
