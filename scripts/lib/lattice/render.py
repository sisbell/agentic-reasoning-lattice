"""Renderer registry + dispatch for substrate-citizen virtual documents.

A virtual document has a substrate address (so it's a citizen of the
link graph — citable, classifiable) but no on-disk content. Its
content is produced by a registered renderer at read time. The
renderer walks the substrate (provenance edges, citations, classifiers)
and assembles markdown live; the doc never goes stale because there's
nothing to keep in sync.

Convention: a doc is virtual iff it carries an active `view.<kind>`
classifier where `<kind>` has a registered renderer. The registry is
keyed by sub-kind (e.g., `claim-statements`); the parent `view`
classifier is reserved for future audit/UI affordances.
"""

from __future__ import annotations

from typing import Callable, Optional

from lib.backend.addressing import Address
from lib.protocols.febe.protocol import Session


Renderer = Callable[[Session, Address], str]
_RENDERERS: dict[str, Renderer] = {}


def register_renderer(view_kind: str, fn: Renderer) -> None:
    """Register a renderer for a view sub-kind.

    The doc is recognized as virtual when it carries an active
    `view.<view_kind>` classifier link.
    """
    _RENDERERS[view_kind] = fn


def view_kind_for(session: Session, addr: Address) -> Optional[str]:
    """Return the view sub-kind classifier on this addr, or None.

    Walks each registered kind and checks for an active
    `view.<kind>` classifier on the doc.
    """
    for kind in _RENDERERS:
        if session.active_links(f"view.{kind}", to_set=[addr]):
            return kind
    return None


def read_doc(session: Session, addr: Address) -> str:
    """Read a substrate doc's content.

    If the doc carries a `view.<kind>` classifier with a registered
    renderer, invoke the renderer. Otherwise read the file at the
    doc's registered path.

    Raises `KeyError` if the address has no registered path and is
    not virtual.
    """
    kind = view_kind_for(session, addr)
    if kind is not None:
        return _RENDERERS[kind](session, addr)

    path = session.get_path_for_addr(addr)
    if path is None:
        raise KeyError(f"no path for address {addr}")
    full = session.store.lattice_dir / path
    return full.read_text()
