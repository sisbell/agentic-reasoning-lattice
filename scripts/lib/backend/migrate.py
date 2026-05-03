"""Migrate a legacy path-keyed substrate to a tumbler-keyed substrate.

Reads a legacy `links.jsonl` (whose endset refs are filesystem paths and
link ids are random hex like `l_<hex>`) and produces:

  - <output_dir>/links.jsonl  — new tumbler-based substrate
  - <output_dir>/paths.json   — path ↔ tumbler mapping

Migration conventions:

- A type-registry doc is auto-bootstrapped as the first emission
  (Gregory's LINK_TYPES_DOC convention), at `1.1.0.1.0.1`.
- A xanadu lattice doc is allocated next, at `1.1.0.1.0.2`. (No
  classifier link — lattice-ness is recoverable from being targeted
  by `lattice` links per the spec we settled on.)
- Each unique legacy path gets a fresh doc tumbler, allocated in
  first-appearance order through the legacy log.
- Each migrated doc gets a `lattice` relation link to the xanadu
  lattice doc.
- Legacy link IDs (`l_<hex>`) appearing in endsets are translated via
  a `legacy_id → tumbler` map built during replay. Legacy chronology
  is preserved (legacy log is processed in file order), so a link
  referenced via `l_<hex>` always exists by the time it's referenced.
- Original timestamps preserved on every replayed link record.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

from .addressing import Address
from .links import Link
from .state import State


def _is_legacy_link_id(ref: str) -> bool:
    return ref.startswith("l_")


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _link_record(link: Link, ts: str) -> dict:
    return {
        "op": "create",
        "id": str(link.addr),
        "from_set": [str(a) for a in link.from_set],
        "to_set": [str(a) for a in link.to_set],
        "type_set": [str(a) for a in link.type_set],
        "ts": ts,
    }


def _write_record(out_file, link: Link, ts: str) -> None:
    out_file.write(json.dumps(_link_record(link, ts), sort_keys=True) + "\n")


def collect_legacy_paths(legacy_path: Path) -> List[str]:
    """Walk legacy JSONL once, return unique non-link-id refs in
    first-appearance order. Preserves chronology — paths referenced
    by earlier links get earlier tumblers."""
    seen: List[str] = []
    seen_set = set()
    with open(legacy_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            for ref in r.get("from_set", []) + r.get("to_set", []):
                if not _is_legacy_link_id(ref) and ref not in seen_set:
                    seen.append(ref)
                    seen_set.add(ref)
    return seen


def migrate(
    legacy_path: str | Path,
    output_dir: str | Path,
    *,
    lattice_name: str = "xanadu",
) -> Dict[str, int]:
    """Run the migration end-to-end.

    Returns a summary dict with counts of docs allocated, lattice
    links emitted, and legacy links replayed.
    """
    legacy_path = Path(legacy_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_jsonl = output_dir / "links.jsonl"
    output_paths = output_dir / "paths.json"

    paths = collect_legacy_paths(legacy_path)

    state = State(account=Address("1.1.0.1"))
    lattice_doc = state.create_doc()  # the xanadu lattice doc

    path_to_tumbler: Dict[str, Address] = {}
    legacy_id_to_tumbler: Dict[str, Address] = {}
    counts = {"docs": 0, "lattice_links": 0, "legacy_links": 0}

    migration_ts = _utcnow_iso()

    with open(output_jsonl, "w") as out:
        # Phase A: docs + their lattice links
        for path in paths:
            doc = state.create_doc()
            path_to_tumbler[path] = doc
            counts["docs"] += 1

            link = state.make_link(
                homedoc=doc,
                from_set=[doc],
                to_set=[lattice_doc],
                type_="lattice",
            )
            counts["lattice_links"] += 1
            _write_record(out, link, migration_ts)

        # Phase B: replay legacy links with translated refs
        with open(legacy_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                r = json.loads(line)
                if r.get("op") != "create":
                    continue

                from_set = _translate_refs(
                    r.get("from_set", []),
                    path_to_tumbler,
                    legacy_id_to_tumbler,
                )
                to_set = _translate_refs(
                    r.get("to_set", []),
                    path_to_tumbler,
                    legacy_id_to_tumbler,
                )

                # Homedoc convention: F[0] if F nonempty (relation,
                # attribute, finding, etc.), else G[0] (classifier
                # shape — F=∅, doc owns its own classifier link).
                if from_set:
                    homedoc = from_set[0]
                elif to_set:
                    homedoc = to_set[0]
                else:
                    raise ValueError(
                        f"legacy link {r['id']} has empty from_set and to_set"
                    )

                type_str = r["type_set"][0]
                link = state.make_link(homedoc, from_set, to_set, type_str)
                legacy_id_to_tumbler[r["id"]] = link.addr
                counts["legacy_links"] += 1
                _write_record(out, link, r["ts"])

    # Path-map sidecar
    with open(output_paths, "w") as f:
        out_data = {
            "_meta": {
                "registry_doc": str(state.registry_doc),
                "lattice_doc": str(lattice_doc),
                "lattice_name": lattice_name,
                "migrated_at": migration_ts,
                "legacy_source": str(legacy_path),
            },
            "paths": {
                p: str(t) for p, t in sorted(path_to_tumbler.items())
            },
        }
        json.dump(out_data, f, indent=2, sort_keys=True)

    return counts


def _translate_refs(
    refs: List[str],
    path_to_tumbler: Dict[str, Address],
    legacy_id_to_tumbler: Dict[str, Address],
) -> List[Address]:
    out: List[Address] = []
    for ref in refs:
        if _is_legacy_link_id(ref):
            if ref not in legacy_id_to_tumbler:
                raise ValueError(
                    f"forward reference to unallocated legacy link id {ref!r}"
                )
            out.append(legacy_id_to_tumbler[ref])
        else:
            if ref not in path_to_tumbler:
                raise ValueError(f"path {ref!r} missing from path_to_tumbler")
            out.append(path_to_tumbler[ref])
    return out
