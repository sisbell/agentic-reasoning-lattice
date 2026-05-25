"""Label-index helpers and lattice-prefix-aware citation aggregation.

Project-level lattice conventions: the project organizes claims into
labeled groups (xanadu uses `ASN-NNNN`, materials would use `MAT-NNNN`,
etc.), names individual claims via `label` attribute links to sidecar
docs, and stores notes under `_docuverse/documents/note/`. None of
these are substrate primitives — they're how this project structures
its lattices, recovered from substrate state by:

- Substrate `label` attribute links pointing at sidecar docs
- The first line of each label sidecar's filesystem content (which
  holds the canonical label string)
- The legacy filesystem path (recovered via `paths.json`'s
  path↔tumbler map), parsed with a `<prefix>-<digits>` regex driven
  by the active lattice's `label_prefix` config field

This module composes substrate primitives (active_links, path_for_addr)
with the project's lattice conventions to produce useful indexes. The
`label_pattern`, `format_label`, and `extract_label_digits` helpers are
the lattice-aware extension points; pass an explicit `prefix` to
override the active lattice's setting.
"""

from __future__ import annotations

import functools
import re
from pathlib import Path
from typing import Dict, List, Optional

from lib.backend.addressing import Address
from lib.backend.predicates import active_links
from lib.backend.store import Store


def _active_prefix() -> str:
    """The active lattice's label_prefix (lazy import to avoid cycles)."""
    from lib.lattice.config import lattice_config
    return lattice_config().label_prefix


@functools.lru_cache(maxsize=8)
def _compiled_pattern(prefix: str) -> re.Pattern[str]:
    return re.compile(rf"{re.escape(prefix)}-(\d+)")


def label_pattern(prefix: Optional[str] = None) -> re.Pattern[str]:
    """Compiled regex matching `<prefix>-<digits>`.

    Without `prefix`, uses the active lattice's `label_prefix` config.
    Cached per prefix string.
    """
    return _compiled_pattern(prefix or _active_prefix())


def format_label(
    num: int, prefix: Optional[str] = None, width: int = 4,
) -> str:
    """Format a numeric id as `<prefix>-<zero-padded-digits>`."""
    return f"{prefix or _active_prefix()}-{int(num):0{width}d}"


def extract_label_digits(
    text: str, prefix: Optional[str] = None,
) -> Optional[str]:
    """First `<prefix>-<digits>` match in text → the digits group, or None."""
    m = label_pattern(prefix).search(text)
    return m.group(1) if m else None


@functools.lru_cache(maxsize=8)
def _compiled_doc_path_pattern(prefix: str) -> re.Pattern[str]:
    return re.compile(
        rf"({re.escape(prefix)}-(\d+))/([^/]+)\.md$"
    )


def parse_claim_doc_path(
    path: str, prefix: Optional[str] = None,
) -> Optional[tuple[str, str, int]]:
    """Parse `<...>/<prefix>-<digits>/<basename>.md`.

    Returns (asn_label, basename, asn_num) on match, else None. Used
    across producers/refiners that derive ASN context from a doc's
    lattice-relative path.
    """
    m = _compiled_doc_path_pattern(prefix or _active_prefix()).search(path)
    if m is None:
        return None
    return m.group(1), m.group(3), int(m.group(2))


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
    """Return {<prefix>-NNNN: note_doc_addr} for every note-classified doc.

    Notes use their lattice label (e.g. "ASN-0009") as the citation
    target — there is no separate label primitive at note scale. We
    extract the numeric id from each note's filesystem path (recovered
    via paths map).
    """
    out: Dict[str, Address] = {}
    pattern = label_pattern()
    prefix = _active_prefix()
    for link in active_links(store.state, "note"):
        if not link.to_set:
            continue
        note_addr = link.to_set[0]
        note_path = store.path_for_addr(note_addr)
        if note_path is None:
            continue
        m = pattern.search(Path(note_path).name)
        if m:
            out[f"{prefix}-{m.group(1)}"] = note_addr
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
    pattern = label_pattern()

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
                m = pattern.search(cited_path)
                if not m:
                    continue
                cited_asn = m.group(1).lstrip("0") or "0"
                # Skip self-references (within-ASN citations)
                if format_label(int(cited_asn)) == asn_label:
                    continue
                deps_set.add(int(cited_asn))
    return sorted(deps_set)


def note_dep_asn_ids(store: Store, note_addr: Address) -> List[int]:
    """Substrate-side query: ASN ids of citation.depends from note_addr.

    **NOT for general "what are ASN X's deps?" lookups.** Under the
    post-2026-05-24 convention, citation.depends for HEALTHY ASNs
    lives on inquiry_addr, not note_addr — this helper returns empty
    for them and silently misleads callers. For canonical dep lookups
    use `lib.shared.foundation.foundation_dep_ids(session, asn_id)`,
    which routes through the inquiry-primary + LEGACY-fallback
    resolution path AND filters retired deps with a warning.

    Legitimate uses of this helper:
      - The LEGACY fallback inside `_resolve_declared_deps` (needs
        raw note-side substrate query; retirement filter applied
        centrally upstream)
      - The audit (`citation_depends_audit.py`) which inspects both
        sides on purpose

    Returns sorted list of int ASN ids. Does NOT filter retired —
    that's done centrally by `_filter_retired_with_warning`.
    """
    pattern = label_pattern()
    note_path = store.path_for_addr(note_addr)
    own_asn = None
    if note_path:
        m = pattern.search(note_path)
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
            m = pattern.search(cited_path)
            if not m:
                continue
            asn_digits = m.group(1)
            if asn_digits == own_asn:
                continue
            deps.add(int(asn_digits.lstrip("0") or "0"))
    return sorted(deps)


def is_note_path(doc_path: str) -> bool:
    """True iff doc_path is under any author's substrate-managed note dir.

    With path partitioning by (node, user), note dirs live at
    `_docuverse/documents/<node>/<user>/note/` rather than directly
    under `documents/`. The check uses the `/note/` segment under the
    author subtree.
    """
    return (
        "/_docuverse/documents/" in doc_path
        and "/note/" in doc_path.split("/_docuverse/documents/", 1)[1]
    ) or (
        doc_path.startswith("_docuverse/documents/")
        and "/note/" in doc_path[len("_docuverse/documents/"):]
    )


def build_doc_label_index(store: Store, doc_path: str) -> Dict[str, Address]:
    """Pick the label index appropriate for the given doc.

    Note docs cite labeled-note targets; claim docs cite claim labels.
    """
    if is_note_path(doc_path):
        return build_note_label_index(store)
    return build_cross_asn_label_index(store)
