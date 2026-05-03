"""FEBE Session — front-end interface to the substrate backend.

Mirrors worktrees/40-f1/udanax-test-harness/febe/client.py:XuSession's
shape: one method per FEBE command, with names matching the spec
(CREATEDOCUMENT → create_document, MAKELINK → create_link, etc.).
Methods delegate to backend primitives; the verb difference between
this layer and the backend is *not* the boundary — the boundary is
that this layer takes/returns wire-protocol shapes (eventually
SpecSets, command codes) while the backend takes/returns resolved
addresses.

Lattices have no separate creation primitive: a doc is a lattice
when other docs link to it via the substrate-owned `lattice` relation.
The session offers `use_lattice(addr)` to set an active lattice for
ergonomic `create_document` calls (mirrors how a real FEBE session
has an authenticated user context).

Future evolution:
- SpecSet / VSpec / Span types as method arguments (the actual wire
  protocol shapes).
- Wire encoding (Number_write, String_write, Address_write per the
  88.1 protocol — see test-harness client.py:Number_write etc.).
- Stream backend (TCP, pipe, in-memory) for cross-process FEBE.
"""

from __future__ import annotations

from typing import Iterable, List, Optional

from lib.backend.addressing import Address
from lib.backend.links import Link
from lib.backend.state import State, TypeArg


class Session:
    """In-process FEBE session bound to a backend State.

    A real FEBE session would be bound to a network or pipe stream;
    this binding to a local State is the in-process equivalent.
    """

    def __init__(
        self,
        backend: State,
        default_lattice: Optional[Address] = None,
    ) -> None:
        self.backend = backend
        self.default_lattice = default_lattice

    # ----- session control -----

    def use_lattice(self, lattice: Address) -> None:
        """Set the active lattice for subsequent create_document calls."""
        self.default_lattice = lattice

    # ----- doc operations -----

    def create_document(
        self,
        kind: str = "doc",
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
        return self.backend.create_doc(kind=kind, lattice=target_lattice)

    def create_version(self, docid: Address) -> Address:
        """CREATEVERSION (code 13): create a new version of an existing doc."""
        return self.backend.create_version(docid)

    # ----- link operations -----

    def create_link(
        self,
        docid: Address,
        sourcespecs: Iterable[Address],
        targetspecs: Iterable[Address],
        typespecs: TypeArg,
    ) -> Link:
        """MAKELINK (code 27): create a link in the given homedoc.

        Argument names match the test-harness client.py signature:
        sourcespecs = from_set, targetspecs = to_set, typespecs = type_set.
        Real FEBE takes SpecSets (collections of spans); this in-process
        version takes flat address lists for now.
        """
        return self.backend.make_link(
            homedoc=docid,
            from_set=sourcespecs,
            to_set=targetspecs,
            type_=typespecs,
        )

    def find_links(
        self,
        sourcespecs: Optional[Iterable[Address]] = None,
        targetspecs: Optional[Iterable[Address]] = None,
        typespecs: Optional[TypeArg] = None,
        homedocids: Optional[Address] = None,
    ) -> List[Link]:
        """FINDLINKSFROMTOTHREE (code 30): query the link store.

        Same prefix-matching on type addresses as the backend (per L10).
        """
        return self.backend.find_links(
            from_set=sourcespecs,
            to_set=targetspecs,
            type_=typespecs,
            homedoc=homedocids,
        )
