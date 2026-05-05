"""FEBE Session — front-end interface to the substrate backend.

In-process implementation of the Session Protocol (lib.protocols.febe.protocol).
A real FEBE session would be bound to a network or pipe stream;
this binds to a local backend (Store or State).

Method names follow Nelson's wire-protocol heritage: create_document
(CREATEDOCUMENT), create_version (CREATEVERSION), make_link
(MAKELINK), find_links (FINDLINKSFROMTOTHREE). The make/create
distinction is principled — create for entities (documents,
versions), make for relations (links).

Backend types accepted:
- `Store` — filesystem-backed; full Protocol works including
  read_document, materialize, register_path, etc.
- `State` — in-memory; in-memory subset works (create_document,
  make_link, find_links). Filesystem-touching methods raise
  NotImplementedError when backed by State alone.

Lattices have no separate creation primitive: a doc is a lattice
when other docs link to it via the substrate-owned `lattice` relation.
The session offers `use_lattice(addr)` to set an active lattice for
ergonomic `create_document` calls (mirrors how a real FEBE session
has an authenticated user context).

BEBE dispatch: the Session holds a BEBEDispatcher (lib.protocols.bebe). For
peer-node Addresses, read/query operations forward through BEBE.
For local-node Addresses, operations hit the backend directly. The
dispatcher's stub returns "not available" defaults today — when
real cross-node work begins, only the dispatcher's internals fill in.

Future evolution:
- SpecSet / VSpec / Span types as method arguments (the actual wire
  protocol shapes).
- Wire encoding (Number_write, String_write, Address_write per the
  88.1 protocol — see test-harness client.py:Number_write etc.).
- Stream backend (TCP, pipe, in-memory) for cross-process FEBE.
"""

from __future__ import annotations

import contextlib
from pathlib import Path
from typing import Iterator, List, Optional, Sequence, Union

from lib.backend.addressing import Address
from lib.backend.links import Link
from lib.backend.state import State, TypeArg
from lib.backend.store import Store
from lib.protocols.bebe import BEBEDispatcher


class Session:
    """In-process FEBE session bound to a backend (Store or State).

    Implements lib.protocols.febe.protocol.Session. Production callers pass a
    Store (filesystem-backed); unit tests may pass a State (in-memory
    only — filesystem-requiring methods will raise).
    """

    def __init__(
        self,
        backend: Union[Store, State],
        default_lattice: Optional[Address] = None,
        *,
        bebe: Optional[BEBEDispatcher] = None,
    ) -> None:
        self.backend = backend
        self.default_lattice = default_lattice
        self.bebe = bebe or BEBEDispatcher()

    # ── Backend access (for protocol-helper interop during Pass 2) ──

    @property
    def state(self) -> State:
        """The underlying State.

        Exposed for interop with substrate primitives that take a
        State directly (substrate-level predicates in lib/backend/
        predicates.py, etc.). Client-side compositions (convergence
        predicates, etc.) take a Session and don't need this.
        """
        if isinstance(self.backend, Store):
            return self.backend.state
        if hasattr(self.backend, "state"):
            # AttributingStore delegates via __getattr__
            return self.backend.state
        return self.backend

    @property
    def store(self) -> Store:
        """The underlying Store, when this Session is store-backed.

        Exposed for interop with protocol-helper functions in
        lib/backend/emit.py that take a Store argument (until Pass 2
        moves them to their respective protocol packages and routes
        them through Session). Raises if Session is State-backed.
        """
        return self._require_store("store")

    # ── Internals ──────────────────────────────────────────────────

    @property
    def _state(self) -> State:
        """Deprecated alias for `state`. Kept for in-class call sites."""
        return self.state

    def _require_store(self, op: str) -> Store:
        """Assert the backend is a Store; required for filesystem ops."""
        # AttributingStore wraps Store via __getattr__ delegation. Check for
        # Store attributes rather than strict isinstance.
        if hasattr(self.backend, "lattice_dir") and hasattr(
            self.backend, "path_to_addr"
        ):
            return self.backend
        raise NotImplementedError(
            f"{op} requires a filesystem-backed Store; "
            f"this Session is bound to a State (in-memory only)."
        )

    # ── Session control ────────────────────────────────────────────

    def use_lattice(self, lattice: Address) -> None:
        """Set the active lattice for subsequent create_document calls."""
        self.default_lattice = lattice

    # ── Lifecycle ──────────────────────────────────────────────────

    def __enter__(self) -> "Session":
        return self

    def __exit__(self, *args) -> None:
        self.close()

    def close(self) -> None:
        """Release any resources held by this Session."""
        backend = self.backend
        # AttributingStore delegates to Store via __getattr__; either way
        # close() is exposed.
        if hasattr(backend, "close"):
            backend.close()

    def commit(self) -> None:
        """Append-only backend has no transaction concept; no-op."""
        return None

    def rollback(self) -> None:
        """Append-only backend has no transaction concept; no-op."""
        return None

    # ── Schema queries ─────────────────────────────────────────────

    def list_link_types(self) -> List[str]:
        """The catalog of recognized link type names."""
        from lib.backend.types import CANONICAL_POSITIONS
        return sorted(CANONICAL_POSITIONS.keys())

    def validate_type(
        self,
        type_: str,
        subtype: Optional[str] = None,
    ) -> None:
        """Raise if (type_, subtype) isn't a valid catalog entry."""
        from lib.backend.schema import validate_type
        full_type = f"{type_}.{subtype}" if subtype else type_
        validate_type(full_type)

    def type_name_for(self, addr: Address) -> Optional[str]:
        """The catalog name for a type-registry Address, or None."""
        return self._state.types.name_for(addr)

    # ── Address & document creation ────────────────────────────────

    def register_path(self, path: str) -> Address:
        """Map a filesystem path to an Address; allocate one if needed."""
        store = self._require_store("register_path")
        return store.register_path(path)

    def register_version(self, prev_addr: Address) -> Address:
        """Allocate a new tumbler version of an existing doc.

        Same disk path, different tumbler — path resolution returns the
        head version after this call. Emits the substrate facts that
        make the new version a first-class citizen (classifier, lattice
        membership, supersession from the previous version).
        """
        store = self._require_store("register_version")
        return store.register_version(prev_addr)

    def create_document(
        self,
        kind: Optional[str] = None,
        lattice: Optional[Address] = None,
    ) -> Address:
        """CREATEDOCUMENT (code 11): create a doc.

        If `lattice` is given, the new doc is linked to that lattice.
        If omitted, the session's active lattice (if any) is used.
        Pass lattice=False explicitly to skip lattice linking.
        """
        target_lattice: Optional[Address]
        if lattice is False:
            target_lattice = None
        elif lattice is not None:
            target_lattice = lattice
        else:
            target_lattice = self.default_lattice
        return self._state.create_doc(
            kind=kind or "doc", lattice=target_lattice,
        )

    def create_version(
        self,
        doc: Address,
        content: Optional[str] = None,
    ) -> Address:
        """CREATEVERSION (code 13): create a new version of an existing doc."""
        return self._state.create_version(doc, content=content)

    def get_addr_for_path(self, path: str) -> Optional[Address]:
        """Look up the Address registered for a path, or None."""
        store = self._require_store("get_addr_for_path")
        return store.path_to_addr.get(path)

    def get_path_for_addr(self, addr: Address) -> Optional[str]:
        """Look up the path registered for an Address, or None."""
        store = self._require_store("get_path_for_addr")
        return store.path_for_addr(addr)

    def version_children(self, doc: Address) -> List[Address]:
        """Immediate version-children of this doc, sorted by sibling order."""
        return sorted(
            (a for a, p in self._state.parent.items() if p == doc),
            key=lambda a: a.digits,
        )

    # ── Document content ───────────────────────────────────────────

    def read_document(self, addr_or_path: Union[Address, str]) -> str:
        """Read a document's content.

        For peer-node Addresses, would dispatch through BEBE; today
        the BEBE stub returns None for forward_read, so peer
        addresses raise.
        """
        store = self._require_store("read_document")
        if isinstance(addr_or_path, Address):
            # Check if this is a peer-node address; if so, BEBE dispatch
            peer = self.bebe.peer_for_address(addr_or_path)
            if peer is not None:
                content = self.bebe.forward_read(peer, addr_or_path)
                if content is None:
                    raise FileNotFoundError(
                        f"peer {peer} unreachable for {addr_or_path}"
                    )
                return content
            path = store.path_for_addr(addr_or_path)
            if path is None:
                raise KeyError(f"no path registered for {addr_or_path}")
        else:
            path = addr_or_path
        full = store.lattice_dir / path
        return full.read_text()

    def update_document(self, path: str, body: str) -> Address:
        """Write content to a working-copy file. Local-only.

        Cross-node content is read-only; this method always targets
        the local node's working copy.
        """
        store = self._require_store("update_document")
        full = store.lattice_dir / path
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(body)
        return store.register_path(path)

    # ── Working-copy hooks ─────────────────────────────────────────

    def materialize(self, addr: Address) -> str:
        """Ensure a document is available on the local filesystem.

        For local-node Addresses: returns the existing path. For
        peer-node Addresses: dispatches into BEBE for forward_read +
        subrepresentation cache. See protocol.py docstring for the
        FEBE/BEBE layering rationale.
        """
        store = self._require_store("materialize")
        peer = self.bebe.peer_for_address(addr)
        if peer is None:
            # Local-node address — file already exists in working copy
            path = store.path_for_addr(addr)
            if path is None:
                raise KeyError(f"no path registered for {addr}")
            full = store.lattice_dir / path
            if not full.exists():
                raise FileNotFoundError(f"document not on local disk: {full}")
            return str(full)
        # Peer-node address — BEBE dispatch
        content = self.bebe.forward_read(peer, addr)
        if content is None:
            raise FileNotFoundError(f"peer {peer} unreachable for {addr}")
        # Cache as subrepresentation
        subrep = store.lattice_dir / "_subrep" / peer / f"{addr}.md"
        subrep.parent.mkdir(parents=True, exist_ok=True)
        subrep.write_text(content)
        return str(subrep)

    def capture_delta(
        self,
        *,
        doc: Address,
        before: Optional[str],
        after: str,
    ) -> None:
        """Capture a working-copy edit as Istream/Vstream delta.

        Stub: real implementation arrives when the storage model adds
        Istream/Vstream versioning. Today a no-op.
        """
        # Reserved API slot; populated when full Vstream/Istream
        # versioning lands.
        return None

    # ── Link queries (find_link primitives) ────────────────────────

    def find_links(
        self,
        *,
        from_set: Optional[Sequence[Address]] = None,
        to_set: Optional[Sequence[Address]] = None,
        type_: Optional[str] = None,
        subtype: Optional[str] = None,
        homedoc: Optional[Address] = None,
    ) -> List[Link]:
        """Return links matching the given filters.

        For peer-node Addresses in filter sets: BEBE dispatch (today
        the stub returns []).
        """
        # Detect peer dispatch
        for filt in (from_set or [], to_set or []):
            for addr in filt:
                peer = self.bebe.peer_for_address(addr)
                if peer is not None:
                    return self.bebe.forward_find_links(
                        peer, from_set=from_set, to_set=to_set,
                        type_=type_, subtype=subtype, homedoc=homedoc,
                    )
        # Local dispatch — collapse type_+subtype into the backend's type form
        full_type = f"{type_}.{subtype}" if (type_ and subtype) else type_
        return self._state.find_links(
            from_set=from_set, to_set=to_set,
            type_=full_type, homedoc=homedoc,
        )

    def active_links(
        self,
        type_: str,
        *,
        from_set: Optional[Sequence[Address]] = None,
        to_set: Optional[Sequence[Address]] = None,
    ) -> List[Link]:
        """Like find_links, but excluding retracted links."""
        from lib.backend.predicates import active_links as _active_links
        return _active_links(
            self._state, type_,
            from_set=list(from_set) if from_set else None,
            to_set=list(to_set) if to_set else None,
        )

    def get_link(self, addr: Address) -> Link:
        """Retrieve a link by its Address."""
        peer = self.bebe.peer_for_address(addr)
        if peer is not None:
            # BEBE dispatch — stub returns []; can't return a Link
            raise FileNotFoundError(f"peer {peer} unreachable for {addr}")
        return self._state.links.get(addr)

    # ── Link emissions (make_link primitives) ──────────────────────

    def make_link(
        self,
        *,
        homedoc: Address,
        from_set: Sequence[Address],
        to_set: Sequence[Address],
        type_: str,
        subtype: Optional[str] = None,
    ) -> Link:
        """MAKELINK (code 27): emit a new link. Always lands locally.

        Dispatches to backend.make_link directly — works for State
        (in-memory), Store (with JSONL persistence), and AttributingStore
        (with auto-emit of manages for provenance).
        """
        full_type = f"{type_}.{subtype}" if subtype else type_
        return self.backend.make_link(
            homedoc=homedoc, from_set=from_set,
            to_set=to_set, type_=full_type,
        )

    def make_link_version(self, parent: Address) -> Address:
        """Allocate a new version of an existing link."""
        # Link versioning uses the same VER3 inc(·, 1) child-allocator
        # pattern as documents. The State exposes this via
        # make_link_version, if implemented; otherwise raise.
        if hasattr(self._state, "make_link_version"):
            return self._state.make_link_version(parent)
        raise NotImplementedError(
            "make_link_version not yet implemented in backend State"
        )

    def retract(self, link: Address) -> Link:
        """File a `retraction` link nullifying the given link."""
        # Retraction is a link with type=retraction, to_set=[link_addr].
        # The retraction is homed in the doc that owns the original
        # link's homedoc.
        original = self._state.links.get(link)
        return self.make_link(
            homedoc=original.homedoc,
            from_set=[],
            to_set=[link],
            type_="retraction",
        )

    # ── Provenance scope ───────────────────────────────────────────

    def as_agent(self, agent_doc: Address) -> "Session":
        """Return a Session that auto-emits `manages` for every link."""
        store = self._require_store("as_agent")
        wrapped = AttributingStore(store, agent_doc)
        # Construct a new Session whose backend is the wrapper
        # (which delegates to Store via __getattr__).
        return Session(
            wrapped, default_lattice=self.default_lattice, bebe=self.bebe,
        )

    @contextlib.contextmanager
    def attributed_to(self, agent_doc: Address) -> Iterator["Session"]:
        """Context manager: scope agent attribution for a block."""
        yield self.as_agent(agent_doc)


# ── Convenience constructor ────────────────────────────────────────


def open_session(
    lattice_dir: Union[str, Path],
    *,
    bebe: Optional[BEBEDispatcher] = None,
) -> Session:
    """Open a Session bound to the given lattice's filesystem-backed
    substrate. Honors the XANADU_AGENT_DOC env var: if set, the
    underlying Store is wrapped in `AttributingStore` for provenance
    auto-emission. Standalone runs (no env var) get a plain Store.

    The standard caller pattern is:

        with open_session(LATTICE) as session:
            session.make_link(...)
    """
    return Session(default_store(lattice_dir), bebe=bebe)


# ── Provenance plumbing (substrate-tier) ───────────────────────────


_ATTRIBUTION_SKIP_PARENTS = frozenset({"agent", "manages"})


class AttributingStore:
    """Wraps a Store; auto-files `manages` for every emitted link.

    Internal plumbing used by `Session.as_agent()` and `default_store()`
    to add provenance attribution to substrate writes. Skips
    self-attribution on the `agent` and `manages` parent types — without
    that the wrapper would recurse on its own emission.

    Not a public class. Callers reach this behavior through Session
    (`session.as_agent(doc)` or `open_session(LATTICE)` with the
    `XANADU_AGENT_DOC` env var set).
    """

    def __init__(self, store: "Store", agent_doc: Address) -> None:
        from lib.backend.emit import emit_agent
        self._store = store
        self._agent_doc = agent_doc
        emit_agent(store, agent_doc)

    @property
    def agent_doc(self) -> Address:
        return self._agent_doc

    @property
    def state(self):
        return self._store.state

    def make_link(
        self,
        homedoc: Address,
        from_set,
        to_set,
        type_,
    ) -> Link:
        link = self._store.make_link(homedoc, from_set, to_set, type_)
        # Determine the parent of the type for the skip check. type_
        # may be a string ("citation.depends") or an Address. In the
        # Address case we bypass the skip since lookup is non-trivial;
        # production callers pass strings.
        parent = None
        if isinstance(type_, str):
            parent = type_.split(".", 1)[0]
        if parent not in _ATTRIBUTION_SKIP_PARENTS:
            self._store.make_link(
                homedoc=self._agent_doc,
                from_set=[self._agent_doc],
                to_set=[link.addr],
                type_="manages",
            )
        return link

    def __getattr__(self, name):
        # Delegate everything else (find_links, addr_for_path, etc.)
        # to the wrapped store.
        return getattr(self._store, name)


def default_store(lattice_dir: Union[str, Path]):
    """Return a Store, wrapped in `AttributingStore` if XANADU_AGENT_DOC
    is set.

    Orchestrators set the env var so subprocess tools that emit
    substrate links inherit the agent identity and attribute every
    operation back to it. Standalone runs (no env var) get a plain
    Store.
    """
    import os
    from lib.provenance import AGENT_DOC_ENV_VAR
    store = Store(lattice_dir)
    agent_doc_path = os.environ.get(AGENT_DOC_ENV_VAR)
    if not agent_doc_path:
        return store
    # Translate the agent doc's filesystem path to its tumbler. The
    # env var holds a lattice-relative path string; if not yet in the
    # path map, register it.
    agent_addr = store.register_path(agent_doc_path)
    return AttributingStore(store, agent_addr)
