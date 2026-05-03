"""Label-index helpers and ASN-aware citation aggregation.

Project-level lattice conventions: the project organizes claims into
ASN-NNNN groups, names individual claims via `label` attribute links
to sidecar docs, and stores notes under `_docuverse/documents/note/`.
None of these are substrate primitives — they're how this project
structures its lattices, recovered from substrate state by:

- Substrate `label` attribute links pointing at sidecar docs
- The first line of each label sidecar's filesystem content (which
  holds the canonical label string)
- The legacy filesystem path (recovered via `paths.json`'s
  path↔tumbler map), parsed with regex for `ASN-\\d+`

This module composes substrate primitives (active_links, path_for_addr)
with the project's lattice conventions to produce useful indexes.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional

from lib.backend.addressing import Address
from lib.backend.predicates import active_links
from lib.backend.store import Store

ASN_PATTERN = re.compile(r"ASN-(\d+)")


def _read_first_line(path: Path) -> Optional[str]:
    """Read the first non-empty line of a file, or None if missing."""
    if not path.exists():
        return None
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                return line
    return None


def build_cross_asn_label_index(store: Store) -> Dict[str, Address]:
    """Return {label_string: claim_doc_addr} across the substrate.

    Walks every `label` attribute link, reads the sidecar's first line
    for the canonical label string, maps it to the doc the label
    annotates (the link's from_set entry).

    Cross-ASN dependencies use bare labels — no ASN prefix — so a flat
    index works.
    """
    lattice_root = store.lattice_dir.resolve()
    out: Dict[str, Address] = {}
    for link in active_links(store.state, "label"):
        if not link.from_set or not link.to_set:
            continue
        annotated_doc = link.from_set[0]
        sidecar_doc = link.to_set[0]
        sidecar_path = store.path_for_addr(sidecar_doc)
        if sidecar_path is None:
            continue
        full = lattice_root / sidecar_path
        label_str = _read_first_line(full)
        if label_str:
            out[label_str] = annotated_doc
    return out


def build_note_label_index(store: Store) -> Dict[str, Address]:
    """Return {ASN-NNNN: note_doc_addr} for every note-classified doc.

    Notes use their ASN label (e.g. "ASN-0009") as the citation target
    — there is no separate label primitive at note scale. We extract
    the ASN id from each note's filesystem path (recovered via paths
    map).
    """
    out: Dict[str, Address] = {}
    for link in active_links(store.state, "note"):
        if not link.to_set:
            continue
        note_addr = link.to_set[0]
        note_path = store.path_for_addr(note_addr)
        if note_path is None:
            continue
        m = ASN_PATTERN.search(Path(note_path).name)
        if m:
            out[f"ASN-{m.group(1)}"] = note_addr
    return out


def aggregate_asn_deps(
    store: Store, asn_label: str,
) -> List[int]:
    """Cross-ASN ASN ids derived from per-claim citations.

    For every claim whose path matches the given asn_label, walk active
    `citation.depends` links from it; extract the cited claim's ASN id
    from its path; collect the set, excluding self-references. Returns
    a sorted list of int ASN ids.
    """
    asn_pattern = re.compile(rf"/{re.escape(asn_label)}/")
    deps_set: set[int] = set()

    # Find every doc whose path is under this ASN's directory
    own_addrs: set[Address] = set()
    for path, addr in store.path_to_addr.items():
        if asn_pattern.search(path):
            own_addrs.add(addr)

    for src_addr in own_addrs:
        for link in active_links(
            store.state, "citation.depends", from_set=[src_addr],
        ):
            for cited in link.to_set:
                cited_path = store.path_for_addr(cited)
                if cited_path is None:
                    continue
                m = ASN_PATTERN.search(cited_path)
                if not m:
                    continue
                cited_asn = m.group(1).lstrip("0") or "0"
                # Skip self-references (within-ASN citations)
                if f"ASN-{m.group(1)}" == asn_label:
                    continue
                deps_set.add(int(cited_asn))
    return sorted(deps_set)


def note_dep_asn_ids(store: Store, note_addr: Address) -> List[int]:
    """ASN ids cited by a note via active `citation.depends` links.

    Returns sorted list of int ASN ids. Self-references included or not
    is irrelevant since note depends are inter-note.
    """
    note_path = store.path_for_addr(note_addr)
    own_asn = None
    if note_path:
        m = ASN_PATTERN.search(note_path)
        if m:
            own_asn = m.group(1)

    deps: set[int] = set()
    for link in active_links(
        store.state, "citation.depends", from_set=[note_addr],
    ):
        for cited in link.to_set:
            cited_path = store.path_for_addr(cited)
            if cited_path is None:
                continue
            m = ASN_PATTERN.search(cited_path)
            if not m:
                continue
            asn_digits = m.group(1)
            if asn_digits == own_asn:
                continue
            deps.add(int(asn_digits.lstrip("0") or "0"))
    return sorted(deps)


def is_note_path(doc_path: str) -> bool:
    """True iff doc_path is under any lattice's substrate-managed note dir."""
    return (
        "/_docuverse/documents/note/" in doc_path
        or doc_path.startswith("_docuverse/documents/note/")
    )


def build_doc_label_index(store: Store, doc_path: str) -> Dict[str, Address]:
    """Pick the label index appropriate for the given doc.

    Note docs cite ASN-NNNN labels; claim docs cite claim labels.
    """
    if is_note_path(doc_path):
        return build_note_label_index(store)
    return build_cross_asn_label_index(store)
