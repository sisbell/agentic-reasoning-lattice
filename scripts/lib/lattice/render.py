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


def _resolve_version_to_base_path(
    session: Session, addr: Address,
) -> Optional[str]:
    """Walk intra-doc version-parents from a version address until we
    find one with a registered path; return that path.

    Intra-doc means the parent is a tumbler-prefix of the child (the
    usual `<base>.<n>.<n>...` version naming). A cross-doc
    supersession bridge (parent is a sibling identity, not a prefix)
    breaks the walk — we never cross into a superseded identity.

    Returns None if no intra-doc ancestor has a registered path. Used
    only as a fallback inside `read_doc` for the current substrate's
    "single file per identity, shared by all versions" storage
    convention.
    """
    parent_map = session.store.state.parent
    cur = addr
    while True:
        parent = parent_map.get(cur)
        if parent is None:
            return None
        # Intra-doc only: parent must be a strict tumbler-prefix.
        if parent.digits != cur.digits[:len(parent.digits)]:
            return None
        cur = parent
        path = session.get_path_for_addr(cur)
        if path is not None:
            return path


def read_doc(session: Session, addr: Address) -> str:
    """Read a substrate doc's content.

    If the doc carries a `transclusion.<kind>` tag with a registered
    renderer, invoke the renderer. Otherwise read the file at the
    doc's registered path.

    When the address has no direct path registration (a version
    address — versions are substrate identity markers without their
    own path entry today), walk intra-doc version-parents to find
    the identity's base and read from there. The intra-doc walk
    uses the tumbler-prefix test to distinguish version-parent
    edges (parent is a strict prefix of child) from cross-doc
    supersession bridges (sibling identities); only the former are
    followed so we resolve to the head identity's base, never a
    superseded identity's.

    NOTE: the version-to-base fallback encodes today's storage
    convention (per-doc-identity file at the base's path; versions
    share that storage). A future Xanadu substrate with per-version
    content addressing would drop the fallback and resolve version
    addresses directly. This is the one place that knows about that
    convention — callers express substrate-pure intent and let
    `read_doc` handle the resolution.

    Raises `KeyError` if neither the address nor any intra-doc
    parent has a registered path, and the doc isn't
    transclusion-rendered.
    """
    kind = _transclusion_kind(session, addr)
    if kind is not None:
        return _RENDERERS[kind](session, addr)

    path = session.get_path_for_addr(addr)
    if path is None:
        path = _resolve_version_to_base_path(session, addr)
    if path is None:
        raise KeyError(f"no path for address {addr}")
    full = session.store.lattice_dir / path
    return full.read_text()
