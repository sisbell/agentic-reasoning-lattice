"""Document creation in a multi-lattice substrate, plus MAKELINK.

The substrate hosts arbitrarily many lattices in one shared address
space. Every doc is emitted from the same global doc-allocator
(T10a-conforming). A doc's role in the substrate (its kind, its
lattice membership, its versioning ancestry) is recorded in substrate
links — the typed-dict caches kept on State are read-throughs over
those links plus addresses.

Two doc-creation operations:

    create_doc(kind, lattice=None)
        Emit a sibling at the global allocator. When `kind` matches a
        Classifier-shape type in the catalog, emit the corresponding
        classifier link (F=∅, G=[doc]). When `lattice` is given, emit
        a `lattice` link (F=[doc], G=[lattice_doc]).

    create_version(doc, content=None)
        Emit a child of <doc> via inc(·, 1) per VER3. Re-emits the
        source's classifier (each version owns its own classifier link)
        and re-emits its lattice memberships. Copies content per VER1
        unless overridden.

There is no separate `create_lattice` — lattices ARE docs that other
docs link to via `lattice` links. To make doc D a lattice, just emit
lattice links from other docs to D.

Two link operations:

    make_link(homedoc, from_set, to_set, type_) — allocate a fresh link
        address in homedoc's link subspace, resolving `type_` (a string
        name, an Address, or a list of those) to type-registry addresses
        per ASN-0043 L8.

    make_link_version(link_addr, ...) — emit an edited version of a
        link at a child address (D.0.2.N.M) per VER3; inherits
        unspecified fields from the original.

A type-registry doc is bootstrapped automatically as the first doc
emitted (Gregory's "Document 1" convention). Every link's type_set
references addresses anchored at this registry.
"""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Sequence, Union

from .addressing import Address, inc
from .allocator import Allocator
from .links import Link, LinkStore
from .types import CLASSIFIER_TYPES, TypeRegistry


TypeArg = Union[str, Address, Sequence[Union[str, Address]]]


def link_subspace_base(homedoc: Address) -> Address:
    """ASN-0043 L0: link addresses live in subspace s_L=2 of a doc's
    element field. The first link emitted in a doc has local address
    .0.2.1 — separator zero into the element field, subspace
    identifier 2, first position 1.
    """
    return Address(homedoc.digits + (0, 2, 1))


class State:
    def __init__(self, account: Address) -> None:
        self.account = account
        if account.zeros() != 1:
            raise ValueError(
                f"account must be a user address (zeros=1), got {account} "
                f"with zeros={account.zeros()}"
            )
        self.doc_allocator = Allocator(inc(account, 2))
        # Multi-account doc allocators (one per (node, user) pair). The
        # primary `doc_allocator` above stays as the legacy interface;
        # `_doc_allocators` is the dict register_path consults to route
        # new emissions by path prefix. Populated lazily by
        # `get_or_create_doc_allocator`. The primary account's allocator
        # is registered up-front so existing single-account code paths
        # find it without going through the dict.
        self._doc_allocators: Dict[Address, Allocator] = {
            account: self.doc_allocator
        }
        self._owner: Dict[Address, Allocator] = {}
        self._link_allocators: Dict[Address, Allocator] = {}
        self.parent: Dict[Address, Optional[Address]] = {}
        # Reverse index over `parent`: maps each non-None parent address
        # to its list of children. Maintained in sync with `parent` via
        # `_set_parent`. Enables O(1) version-children lookup instead
        # of an O(N) scan over the whole parent map (where N = total
        # addresses), which previously made `version_head` on deep
        # chains scale as O(depth × N).
        self._children_index: Dict[Address, List[Address]] = {}
        self.kind: Dict[Address, str] = {}
        self.content: Dict[Address, str] = {}
        self.links = LinkStore()
        # Bootstrap the type-registry doc as the first emission. The
        # registry doc precedes the type system itself, so it gets no
        # classifier link — its role is recovered from being the anchor
        # of every type address.
        registry_addr = self._emit(self.doc_allocator)
        self._set_parent(registry_addr, None)
        self.kind[registry_addr] = "type-registry"
        self.content[registry_addr] = ""
        self._registry_doc = registry_addr
        self.types = TypeRegistry(registry_addr)

    @property
    def registry_doc(self) -> Address:
        return self._registry_doc

    def get_or_create_doc_allocator(self, account: Address) -> Allocator:
        """Return the doc allocator for a given account, creating it on
        first request.

        Each (node, user) account has its own doc allocator rooted at
        `inc(account, 2)`. Substrate auto-routing (register_path) parses
        the (node, user) from a file path and calls this to pick the
        allocator. The primary account's allocator is the one created
        in `__init__`; secondary accounts are created on demand.

        Account must have `zeros()==1` (user-level address), matching
        the constructor's invariant.
        """
        if account in self._doc_allocators:
            return self._doc_allocators[account]
        if account.zeros() != 1:
            raise ValueError(
                f"account must be a user address (zeros=1), got {account} "
                f"with zeros={account.zeros()}"
            )
        allocator = Allocator(inc(account, 2))
        self._doc_allocators[account] = allocator
        return allocator

    # ----- parent map (with children index) -----

    def _set_parent(
        self, child: Address, parent: Optional[Address],
    ) -> None:
        """Set child's version-parent and update the children index.

        Direct `self.parent[child] = parent` mutation is no longer
        used outside this method — the children index mirrors the
        non-None parent edges for O(1) child lookup, and using this
        helper keeps the two in sync.

        Idempotent: re-setting the same (child, parent) pair is a
        no-op against the index. Re-parenting (rare; mostly reload
        and tests) removes the child from the old parent's list
        before inserting into the new one.
        """
        old_parent = self.parent.get(child)
        if old_parent is not None and old_parent != parent:
            siblings = self._children_index.get(old_parent)
            if siblings is not None and child in siblings:
                siblings.remove(child)
                if not siblings:
                    del self._children_index[old_parent]
        self.parent[child] = parent
        if parent is not None:
            children = self._children_index.setdefault(parent, [])
            if child not in children:
                children.append(child)

    def version_children(self, doc: Address) -> List[Address]:
        """Immediate version-children of doc, sorted by tumbler order.

        O(1) lookup + O(k log k) sort over k = direct children, vs the
        prior O(N) scan over the full parent map. For docs with many
        siblings (fan-out) or deep linear chains, this is a structural
        speedup, not a marginal one.
        """
        children = self._children_index.get(doc)
        if not children:
            return []
        return sorted(children, key=lambda a: a.digits)

    # ----- doc creation -----

    def _emit(self, allocator: Allocator) -> Address:
        addr = allocator.emit_sibling()
        self._owner[addr] = allocator
        return addr

    def _allocate_child(self, parent: Address) -> Address:
        if parent not in self._owner:
            raise ValueError(f"unknown parent address {parent}")
        owner = self._owner[parent]
        child_alloc = owner.get_or_spawn_child(parent, k_prime=1)
        return self._emit(child_alloc)

    def _emit_classifier(self, doc: Address, kind: str) -> None:
        """Emit a classifier link (F=∅, G=[doc], type=kind) homed in doc.
        Skips if kind is not a Classifier-shape type in the catalog."""
        if kind in CLASSIFIER_TYPES:
            self.make_link(
                homedoc=doc,
                from_set=[],
                to_set=[doc],
                type_=kind,
            )

    def _emit_lattice_link(self, doc: Address, lattice: Address) -> None:
        """Emit a `lattice` relation link (F=[doc], G=[lattice]) homed in doc."""
        self.make_link(
            homedoc=doc,
            from_set=[doc],
            to_set=[lattice],
            type_="lattice",
        )

    def create_doc(
        self,
        kind: str = "doc",
        lattice: Optional[Address] = None,
    ) -> Address:
        addr = self._emit(self.doc_allocator)
        self._set_parent(addr, None)
        self.kind[addr] = kind
        self.content[addr] = ""
        self._emit_classifier(addr, kind)
        if lattice is not None:
            self._emit_lattice_link(addr, lattice)
        return addr

    def create_version(
        self, doc: Address, content: Optional[str] = None
    ) -> Address:
        if doc not in self._owner:
            raise ValueError(f"unknown doc address {doc}")
        addr = self._allocate_child(doc)
        self._set_parent(addr, doc)
        kind = self.kind.get(doc, "doc")
        self.kind[addr] = kind
        self.content[addr] = (
            content if content is not None else self.content.get(doc, "")
        )
        self._emit_classifier(addr, kind)
        # Inherit lattice memberships from source: each lattice the
        # source is in gets a fresh `lattice` link from the new version.
        for lattice in self.lattices_of(doc):
            self._emit_lattice_link(addr, lattice)
        return addr

    # ----- type resolution -----

    def _resolve_types(self, type_: TypeArg) -> List[Address]:
        if isinstance(type_, Address):
            return [type_]
        if isinstance(type_, str):
            return [self.types.address_for(type_)]
        out: List[Address] = []
        for entry in type_:
            if isinstance(entry, Address):
                out.append(entry)
            else:
                out.append(self.types.address_for(entry))
        return out

    # ----- links -----

    def make_link(
        self,
        homedoc: Address,
        from_set: Iterable[Address],
        to_set: Iterable[Address],
        type_: TypeArg,
        *,
        ts: Optional[int] = None,
    ) -> Link:
        if homedoc not in self._owner:
            raise ValueError(f"unknown homedoc {homedoc}")
        if homedoc not in self._link_allocators:
            self._link_allocators[homedoc] = Allocator(link_subspace_base(homedoc))
        link_alloc = self._link_allocators[homedoc]
        link_addr = link_alloc.emit_sibling()
        self._owner[link_addr] = link_alloc
        self._set_parent(link_addr, None)
        type_addrs = self._resolve_types(type_)
        if ts is None:
            import time
            ts = int(time.time())
        return self.links.emit(link_addr, from_set, to_set, type_addrs, ts=ts)

    def make_link_version(
        self,
        link_addr: Address,
        from_set: Optional[Iterable[Address]] = None,
        to_set: Optional[Iterable[Address]] = None,
        type_: Optional[TypeArg] = None,
        *,
        ts: Optional[int] = None,
    ) -> Link:
        if link_addr not in self._owner:
            raise ValueError(f"unknown link address {link_addr}")
        original = self.links.get(link_addr)
        new_addr = self._allocate_child(link_addr)
        self._set_parent(new_addr, link_addr)
        new_from = tuple(from_set) if from_set is not None else original.from_set
        new_to = tuple(to_set) if to_set is not None else original.to_set
        new_type = (
            tuple(self._resolve_types(type_))
            if type_ is not None
            else original.type_set
        )
        if ts is None:
            import time
            ts = int(time.time())
        return self.links.emit(new_addr, new_from, new_to, new_type, ts=ts)

    # ----- queries -----

    def find_links(
        self,
        from_set: Optional[Iterable[Address]] = None,
        to_set: Optional[Iterable[Address]] = None,
        type_: Optional[TypeArg] = None,
        homedoc: Optional[Address] = None,
    ) -> List[Link]:
        """Wrapper over LinkStore.find_links that resolves string type
        names to type-registry addresses before delegating."""
        type_addrs = (
            self._resolve_types(type_) if type_ is not None else None
        )
        return self.links.find_links(
            from_set=from_set,
            to_set=to_set,
            type_set=type_addrs,
            homedoc=homedoc,
        )

    def lattices_of(self, addr: Address) -> List[Address]:
        """All lattices this doc is in. Multi-lattice membership is
        natural — multiple `lattice` links from the same doc."""
        out: List[Address] = []
        for link in self.find_links(from_set=[addr], type_="lattice"):
            for la in link.to_set:
                if la not in out:
                    out.append(la)
        return out

    def lattice_of(self, addr: Address) -> Optional[Address]:
        """The first lattice this doc is in, or None. For multi-lattice
        docs, use lattices_of() instead."""
        lattices = self.lattices_of(addr)
        return lattices[0] if lattices else None

    def docs_in(self, lattice: Address) -> List[Address]:
        out: List[Address] = []
        for link in self.find_links(to_set=[lattice], type_="lattice"):
            for d in link.from_set:
                if d not in out:
                    out.append(d)
        return out

    def version_chain(self, addr: Address) -> List[Address]:
        """VER-P chain back to canonical source; address structure
        already encodes this per VER3, this materializes it."""
        chain: List[Address] = []
        cur: Optional[Address] = self.parent.get(addr)
        while cur is not None:
            chain.append(cur)
            cur = self.parent.get(cur)
        return chain
