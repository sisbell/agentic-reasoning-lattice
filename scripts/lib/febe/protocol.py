"""Session Protocol — the substrate's public interface contract.

Captures the binding contract described in
`docs/hypergraph-protocol/binding.md`. Every client (Python protocol
code, CLI scripts, prompts via CLI) reaches the substrate through a
Session. No client imports `lib.backend.*` directly. The Session
implementation can be in-process, FEBE-wire-bound, or anything else;
clients cannot tell which.

This module defines the contract as a `typing.Protocol`. The
in-process `lib.febe.session.Session` class implements it; future
implementations (wire-bound FEBE clients) implement it as well.

## Layering

Methods are grouped by which architectural tier they hit (per
`docs/hypergraph-protocol/architecture.md` — Nelson's FEBE / BEBE /
middle-end terms mapped onto modern N-tier):

- **FEBE atomic** — direct substrate operations. find_links,
  read_document, make_link, create_document, etc. The bulk of the
  interface.
- **Working-copy hooks** — materialize (BEBE-dispatched for peer
  addresses) and capture_delta (slot for working-copy edit deltas).
- **Provenance scope** — as_agent, attributed_to. Domain-neutral
  attribution wrapper.
- **Middleware** — search_content, probe_remote, analyze_bridge,
  etc. (deferred; add to this Protocol when `lib/middle_end/`
  begins.)

## BEBE dispatch

Read/query operations whose Address arguments resolve to a peer
node dispatch through BEBE (`lib/bebe/`) at the routing seam inside
the implementation. Callers don't see this — they call
`session.read_document(addr)` and the implementation routes by
inspecting the Address's allocator prefix. Per
`architecture.md`'s "Which Session operations dispatch through BEBE"
section.

## Schema types

`Address` and `Link` are the only `lib.backend` types that legitimately
appear in this Protocol's signatures. They are part of the schema,
not implementation details. Internal types (`State`, `LinkStore`,
allocator state) stay private to the implementation.
"""

from __future__ import annotations

from contextlib import AbstractContextManager
from pathlib import Path
from typing import (
    Iterator,
    List,
    Optional,
    Protocol,
    Sequence,
    Union,
    runtime_checkable,
)

from lib.backend.addressing import Address
from lib.backend.links import Link


@runtime_checkable
class Session(Protocol):
    """The substrate's public interface contract.

    A Session abstracts whatever connection makes the substrate
    available — in-process backend, FEBE wire client, or any future
    transport. Clients hold a Session and call its methods; the
    implementation routes operations to the right place (local back
    end, peer node via BEBE, middleware service, etc.).
    """

    # ── Lifecycle ───────────────────────────────────────────────────

    def close(self) -> None:
        """Release any resources held by this Session."""
        ...

    def commit(self) -> None:
        """Commit pending writes (if the implementation is transactional).

        Default implementations may treat this as a no-op when the
        backend is append-only with no transaction concept.
        """
        ...

    def rollback(self) -> None:
        """Discard pending writes (if transactional).

        For append-only backends, may be implemented as a tail-truncate
        or a best-effort no-op.
        """
        ...

    # ── Schema queries ──────────────────────────────────────────────

    def list_link_types(self) -> List[str]:
        """The catalog of recognized link type names."""
        ...

    def validate_type(
        self,
        type_: str,
        subtype: Optional[str] = None,
    ) -> None:
        """Raise if (type_, subtype) isn't a valid catalog entry."""
        ...

    def type_name_for(self, addr: Address) -> Optional[str]:
        """The catalog name for a type-registry Address, or None.

        Inverse of the implicit Address-for-name mapping inside the
        type registry. Used by classifier predicates that need to
        recover the subtype string ("axiom", "theorem", etc.) from a
        link's `type_set[0]` Address.
        """
        ...

    # ── Address & document creation ─────────────────────────────────

    def register_path(self, path: str) -> Address:
        """Map a filesystem path to an Address; allocate one if needed."""
        ...

    def create_document(
        self,
        kind: Optional[str] = None,
        lattice: Optional[Address] = None,
    ) -> Address:
        """Allocate a new document. Optionally classify and lattice-bind."""
        ...

    def create_version(
        self,
        doc: Address,
        content: Optional[str] = None,
    ) -> Address:
        """Allocate a new version of an existing document."""
        ...

    def get_addr_for_path(self, path: str) -> Optional[Address]:
        """Look up the Address registered for a path, or None."""
        ...

    def get_path_for_addr(self, addr: Address) -> Optional[str]:
        """Look up the path registered for an Address, or None."""
        ...

    def version_children(self, doc: Address) -> List[Address]:
        """Immediate version-children of this doc, sorted by sibling order.

        Returns the addresses whose version-parent is `doc`. Empty if
        `doc` is a head (no children). The version-parent map is a
        substrate primitive separate from the link store; this method
        is the public surface for querying it.
        """
        ...

    # ── Document content ────────────────────────────────────────────

    def read_document(self, addr_or_path: Union[Address, str]) -> str:
        """Return the document's bytes/text.

        For peer-node Addresses, dispatches through BEBE
        (forward_read), caching the result as a subrepresentation
        on first access.
        """
        ...

    def update_document(self, path: str, body: str) -> Address:
        """Write content to a working-copy file. Local-only.

        Cross-node content is read-only by construction; this method
        always targets the local node's working copy.
        """
        ...

    # ── Working-copy hooks ──────────────────────────────────────────

    def materialize(self, addr: Address) -> str:
        """Ensure a document is available on the local filesystem.

        This is the FEBE-level entry point that triggers BEBE
        subrepresentation when the addressed doc lives on a peer
        node. From the caller's perspective: "put this doc on disk
        as a file so I can grep/Read it natively."

        Architecturally:
        - **Session is the public interface.** Clients reach the
          substrate through Session methods; they never call BEBE
          directly. BEBE is implementation tier (per
          architecture.md).
        - **BEBE dispatch happens inside this method.** For local-
          node Addresses (matching the local allocator prefix) this
          is a no-op — the file already exists in the local working
          copy. For peer-node Addresses, the implementation
          dispatches to lib/bebe/ to forward-read from the peer and
          cache the result as a subrepresentation under
          lattices/<this-node>/_subrep/<peer>/ as read-only.

        Why a separate method (not folded into read_document):
        callers (LLM tooling, prompts driving cone-sweep, etc.)
        often want to trigger "make this doc available on disk"
        without immediately reading its content — they intend to
        subsequently grep/Read the file natively. read_document
        returns bytes; materialize ensures filesystem availability.

        Returns the local filesystem path to the (now-available)
        document.
        """
        ...

    def capture_delta(
        self,
        *,
        doc: Address,
        before: Optional[str],
        after: str,
    ) -> None:
        """Capture a working-copy edit as Istream/Vstream delta operations.

        Stub initially; populated when the storage model adds full
        Istream/Vstream versioning. The trigger mechanism (substrate-
        mediated edit primitive, filesystem watcher, post-edit
        orchestrator hook) is implementation-specific.
        """
        ...

    # ── Link queries (find_link primitives) ─────────────────────────

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

        Dispatches through BEBE for peer-node Addresses in the filter
        sets — when from_set or to_set references a peer-node
        Address, the query forwards to that peer's substrate.
        """
        ...

    def active_links(
        self,
        type_: str,
        *,
        from_set: Optional[Sequence[Address]] = None,
        to_set: Optional[Sequence[Address]] = None,
    ) -> List[Link]:
        """Like find_links, but excluding retracted links."""
        ...

    def get_link(self, addr: Address) -> Link:
        """Retrieve a link by its Address. Dispatches through BEBE for
        peer-node link Addresses."""
        ...

    # ── Link emissions (make_link primitives) ───────────────────────

    def make_link(
        self,
        *,
        homedoc: Address,
        from_set: Sequence[Address],
        to_set: Sequence[Address],
        type_: str,
        subtype: Optional[str] = None,
    ) -> Link:
        """Emit a new link. Always lands in the local substrate.

        The link's from_set/to_set may reference peer-node Addresses;
        the link record itself is local. No BEBE dispatch on writes.
        """
        ...

    def make_link_version(self, parent: Address) -> Address:
        """Allocate a new version of an existing link."""
        ...

    def retract(self, link: Address) -> Link:
        """File a `retraction` link nullifying the given link."""
        ...

    # ── Provenance scope ────────────────────────────────────────────

    def as_agent(self, agent_doc: Address) -> "Session":
        """Return a Session that auto-emits `manages` for every link.

        The wrapped Session attributes every emission to the given
        agent_doc. Mirrors the AgentStore wrapper semantics; the
        provenance protocol is captured at the binding interface so
        it inherits to any backend.
        """
        ...

    def attributed_to(
        self,
        agent_doc: Address,
    ) -> AbstractContextManager["Session"]:
        """Context manager: scope agent attribution for a block."""
        ...
