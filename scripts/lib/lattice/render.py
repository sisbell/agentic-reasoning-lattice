"""Renderer registry + read_doc dispatch for transclusion-rendered docs.

A transclusion-rendered document has a substrate address (so it's a
citizen of the link graph — citable, classifiable) but no on-disk
content. Its content is produced by a registered renderer at read
time. The renderer walks the substrate (provenance edges, citations,
attributes) and assembles markdown live; the doc never goes stale
because there's nothing to keep in sync.

Convention: a doc is transclusion-rendered iff it carries an active
`transclusion.<kind>` classifier where `<kind>` has a registered
renderer. The classifier is a runtime tag — present so `read_doc`
knows to dispatch — and is NOT a structural fact. Substrate
predicates and chain walks should treat transclusion-rendered docs
like any other doc; do not branch on the tag.
"""

from __future__ import annotations

from typing import Callable, Optional

from lib.backend.addressing import Address
from lib.protocols.febe.protocol import Session


Renderer = Callable[[Session, Address], str]
_RENDERERS: dict[str, Renderer] = {}


def register_renderer(kind: str, fn: Renderer) -> None:
    """Register a renderer for a transclusion sub-kind.

    The doc is recognized at read time when it carries an active
    `transclusion.<kind>` classifier link.
    """
    _RENDERERS[kind] = fn


def _transclusion_kind(session: Session, addr: Address) -> Optional[str]:
    """Internal dispatch helper for `read_doc`.

    Returns the transclusion sub-kind classifier on this addr, or
    None. NOT a substrate predicate — used only inside `read_doc`
    to pick the renderer. Don't import this elsewhere.
    """
    for kind in _RENDERERS:
        if session.active_links(f"transclusion.{kind}", to_set=[addr]):
            return kind
    return None


def read_doc(session: Session, addr: Address) -> str:
    """Read a substrate doc's content.

    If the doc carries a `transclusion.<kind>` tag with a registered
    renderer, invoke the renderer. Otherwise read the file at the
    doc's registered path.

    Raises `KeyError` if the address has no registered path and is
    not transclusion-rendered.
    """
    kind = _transclusion_kind(session, addr)
    if kind is not None:
        return _RENDERERS[kind](session, addr)

    path = session.get_path_for_addr(addr)
    if path is None:
        raise KeyError(f"no path for address {addr}")
    full = session.store.lattice_dir / path
    return full.read_text()
