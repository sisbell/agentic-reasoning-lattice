#!/usr/bin/env python3
"""Revert an ASN's substrate + filesystem state back to discovery.

Identifies everything claim-derivation has produced for the named
ASN — per-claim files + sidecars, the claims.statements aggregate,
review / finding / audit / citation-resolve / signature-resolve /
claim-contract / claim-formal-contract docs scoped to this ASN —
and removes them from both disk and substrate. Keeps the note
itself and its operator-drafted `statements` sidecar (discovery
input).

Pre-check: scans for citations from OUTSIDE the revert set pointing
INTO it. Refuses to proceed if any are found, unless `--force`
(in which case the orphaned cites become the operator's problem
to clean up).

Substrate cleanup is destructive (rewrites `links.jsonl` and
`paths.json`), not retraction-based. This is a dev tool; in
append-only-pure mode, every removed link would need an emitted
retraction. For testing flows where the ASN's derivation is being
re-run from scratch, destructive is cleaner.

Usage:
    python scripts/revert-to-discovery.py 36
    python scripts/revert-to-discovery.py 36 --dry-run
    python scripts/revert-to-discovery.py 36 --force
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.backend.addressing import Address
from lib.lattice.labels import format_label
from lib.protocols.febe.session import open_session
from lib.shared.paths import (
    DOCUVERSE_DIR, LATTICE, LATTICE_NODE, LATTICE_USER,
)


# Subdirectories of the author tree whose ASN-keyed subdirectories
# hold derivation byproducts. The note's own dir (`note/`) and
# inquiry (`inquiry/`) are NOT included — those are discovery inputs.
_DERIVATION_SUBDIRS = (
    "claim",
    "review/claims",
    "finding/claims",
    "audit/claims",
    "citation-resolve/claims",
    "signature-resolve/claims",
    "claim-contract/claims",
    "claim-formal-contract/claims",
)

_CITATION_TYPES = ("citation.depends", "citation.forward", "citation.resolve")


def _walk_to_base(session, addr: Address) -> Address:
    parent_map = session.store.state.parent
    cur = addr
    while parent_map.get(cur) is not None:
        cur = parent_map[cur]
    return cur


def _collect_versions(session, base: Address) -> set:
    """Walk version_children DFS from base; return base + every descendant."""
    out = {base}
    stack = [base]
    while stack:
        cur = stack.pop()
        children = session.version_children(cur)
        for c in children:
            if c not in out:
                out.add(c)
                stack.append(c)
    return out


def _collect_revert_set(session, asn_label: str) -> tuple[set, list[Path]]:
    """Return (addresses_to_remove, dirs_to_delete) for `asn_label`."""
    author_root = (
        DOCUVERSE_DIR / "documents" / LATTICE_NODE / LATTICE_USER
    )
    dirs = [
        author_root / sub / asn_label
        for sub in _DERIVATION_SUBDIRS
    ]
    dirs = [d for d in dirs if d.exists()]

    # Paths in paths.json registered under any of the target dirs.
    docuverse_rel_prefixes = tuple(
        str(d.resolve().relative_to(DOCUVERSE_DIR.parent.resolve())) + "/"
        for d in dirs
    )

    addrs: set = set()
    for path, addr in session.store.path_to_addr.items():
        if path.startswith(docuverse_rel_prefixes):
            base = addr
            for v in _collect_versions(session, base):
                addrs.add(v)
    return addrs, dirs


def _find_external_cites(
    session, target_set: set,
) -> list[tuple[Address, Address, Address]]:
    """Citations whose `to_set` lands in `target_set` but `from_set` doesn't."""
    dangling = []
    for cit_type in _CITATION_TYPES:
        for link in session.active_links(cit_type):
            target_hit = False
            for t in link.to_set:
                if _walk_to_base(session, t) in target_set:
                    target_hit = True
                    break
            if not target_hit:
                continue
            external_from = False
            for f in link.from_set:
                if _walk_to_base(session, f) not in target_set:
                    external_from = True
                    break
            if external_from:
                dangling.append((link.addr, link.from_set[0], link.to_set[0]))
    return dangling


def _filter_links_jsonl(jsonl_path: Path, target_set: set) -> tuple[int, int]:
    """Rewrite `jsonl_path` keeping only links untouched by `target_set`.
    Returns (kept, dropped) line counts."""
    target_strs = {str(a) for a in target_set}
    kept_lines = []
    dropped = 0
    with open(jsonl_path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                kept_lines.append(line)
                continue
            touched = False
            for key in ("addr", "homedoc"):
                if rec.get(key) in target_strs:
                    touched = True
                    break
            if not touched:
                for key in ("from_set", "to_set"):
                    for a in rec.get(key, []):
                        if a in target_strs:
                            touched = True
                            break
                    if touched:
                        break
            if touched:
                dropped += 1
            else:
                kept_lines.append(line)
    jsonl_path.write_text("\n".join(kept_lines) + "\n")
    return len(kept_lines), dropped


def _filter_paths_json(paths_json: Path, target_set: set) -> int:
    """Rewrite `paths_json` dropping path entries whose addr is in
    `target_set`. Returns count dropped."""
    target_strs = {str(a) for a in target_set}
    with open(paths_json) as f:
        data = json.load(f)
    before = len(data["paths"])
    data["paths"] = {
        p: a for p, a in data["paths"].items()
        if a not in target_strs
    }
    after = len(data["paths"])
    with open(paths_json, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)
    return before - after


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "asn", help="ASN number to revert (e.g., 36, 0036, ASN-0036)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Report what would be deleted; no changes.",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Proceed even if external citations would dangle.",
    )
    args = parser.parse_args()

    import re
    asn_num = int(re.sub(r"\D", "", args.asn))
    asn_label = format_label(asn_num)

    with open_session(LATTICE) as session:
        addrs, dirs = _collect_revert_set(session, asn_label)
        if not addrs and not dirs:
            print(f"  nothing to revert for {asn_label}", file=sys.stderr)
            return 0

        print(
            f"  [REVERT] {asn_label}: {len(addrs)} addresses across "
            f"{len(dirs)} directories",
            file=sys.stderr,
        )

        dangling = _find_external_cites(session, addrs)
        if dangling:
            print(
                f"  [REVERT] {len(dangling)} external citation(s) "
                f"would dangle after revert:",
                file=sys.stderr,
            )
            for link, frm, to in dangling[:5]:
                print(
                    f"    link={link}  from={frm}  to={to}",
                    file=sys.stderr,
                )
            if len(dangling) > 5:
                print(
                    f"    (+{len(dangling) - 5} more)", file=sys.stderr,
                )
            if not args.force:
                print(
                    "  [REVERT] aborting; use --force to proceed anyway",
                    file=sys.stderr,
                )
                return 1

        if args.dry_run:
            print(
                f"  [DRY-RUN] would delete {len(dirs)} directories, "
                f"{len(addrs)} substrate addresses",
                file=sys.stderr,
            )
            for d in dirs:
                print(f"    {d.relative_to(Path.cwd())}", file=sys.stderr)
            return 0

    # 1. Disk: delete the directories.
    for d in dirs:
        shutil.rmtree(d)
        print(f"  [DELETED] {d.relative_to(Path.cwd())}", file=sys.stderr)

    # 2. Substrate: strip links.jsonl + paths.json.
    jsonl_path = DOCUVERSE_DIR / "links.jsonl"
    paths_json = DOCUVERSE_DIR / "paths.json"
    kept, dropped_links = _filter_links_jsonl(jsonl_path, addrs)
    dropped_paths = _filter_paths_json(paths_json, addrs)
    print(
        f"  [REVERT] links.jsonl: kept {kept}, dropped {dropped_links}",
        file=sys.stderr,
    )
    print(
        f"  [REVERT] paths.json: dropped {dropped_paths} entries",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
