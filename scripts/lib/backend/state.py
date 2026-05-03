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
        self._owner: Dict[Address, Allocator] = {}
        self._link_allocators: Dict[Address, Allocator] = {}
        self.parent: Dict[Address, Optional[Address]] = {}
        self.kind: Dict[Address, str] = {}
        self.content: Dict[Address, str] = {}
        self.links = LinkStore()
        # Bootstrap the type-registry doc as the first emission. The
        # registry doc precedes the type system itself, so it gets no
        # classifier link — its role is recovered from being the anchor
        # of every type address.
        registry_addr = self._emit(self.doc_allocator)
        self.parent[registry_addr] = None
        self.kind[registry_addr] = "type-registry"
        self.content[registry_addr] = ""
        self._registry_doc = registry_addr
        self.types = TypeRegistry(registry_addr)

    @property
    def registry_doc(self) -> Address:
        return self._registry_doc

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
        self.parent[addr] = None
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
        self.parent[addr] = doc
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
    ) -> Link:
        if homedoc not in self._owner:
            raise ValueError(f"unknown homedoc {homedoc}")
        if homedoc not in self._link_allocators:
            self._link_allocators[homedoc] = Allocator(link_subspace_base(homedoc))
        link_alloc = self._link_allocators[homedoc]
        link_addr = link_alloc.emit_sibling()
        self._owner[link_addr] = link_alloc
        self.parent[link_addr] = None
        type_addrs = self._resolve_types(type_)
        return self.links.emit(link_addr, from_set, to_set, type_addrs)

    def make_link_version(
        self,
        link_addr: Address,
        from_set: Optional[Iterable[Address]] = None,
        to_set: Optional[Iterable[Address]] = None,
        type_: Optional[TypeArg] = None,
    ) -> Link:
        if link_addr not in self._owner:
            raise ValueError(f"unknown link address {link_addr}")
        original = self.links.get(link_addr)
        new_addr = self._allocate_child(link_addr)
        self.parent[new_addr] = link_addr
        new_from = tuple(from_set) if from_set is not None else original.from_set
        new_to = tuple(to_set) if to_set is not None else original.to_set
        new_type = (
            tuple(self._resolve_types(type_))
            if type_ is not None
            else original.type_set
        )
        return self.links.emit(new_addr, new_from, new_to, new_type)

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
