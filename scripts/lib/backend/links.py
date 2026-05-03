"""Link store: MAKELINK + FINDLINKS over the substrate.

Per ASN-0043 and Nelson's FEBE protocol, a link's address structurally
extends the homedoc into its link subspace. The link's address is its
identity; the homedoc is recoverable via Address.split() (last-zero cut).

The link's value is three sets:

    from_set, to_set, type_set

Per L8 (TypeByAddress) every type entry in `type_set` is itself a
tumbler address pointing into a type-registry doc; type matching is by
address identity. Subtype hierarchies are recovered by L10 — a query
at a parent type's address matches every subtype that extends it via
tumbler-prefix containment.

L11a / L12 / L12a guarantee link permanence and the link store's
monotonic growth. There is no UPDATELINK or DELETELINK — only
MAKELINK. Edits become version-bearing child link addresses (see
make_link_version in state.py).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple

from .addressing import Address


def _is_prefix_or_equal(query: Address, candidate: Address) -> bool:
    """True iff query's digits are a prefix of (or equal to) candidate's."""
    return candidate.digits[: len(query.digits)] == query.digits


@dataclass(frozen=True)
class Link:
    addr: Address
    from_set: Tuple[Address, ...]
    to_set: Tuple[Address, ...]
    type_set: Tuple[Address, ...]

    @property
    def homedoc(self) -> Address:
        """ASN-0043: link addr structurally extends homedoc.
        split() at last zero → (homedoc, in-doc-link-local)."""
        return self.addr.split()[0]


class LinkStore:
    """Append-only log of MAKELINK emissions."""

    def __init__(self) -> None:
        self._links: List[Link] = []

    def __len__(self) -> int:
        return len(self._links)

    def __iter__(self) -> Iterable[Link]:
        return iter(self._links)

    def get(self, addr: Address) -> Link:
        for link in self._links:
            if link.addr == addr:
                return link
        raise KeyError(f"no link at {addr}")

    def emit(
        self,
        addr: Address,
        from_set: Iterable[Address],
        to_set: Iterable[Address],
        type_set: Iterable[Address],
    ) -> Link:
        link = Link(
            addr=addr,
            from_set=tuple(from_set),
            to_set=tuple(to_set),
            type_set=tuple(type_set),
        )
        self._links.append(link)
        return link

    def find_links(
        self,
        from_set: Optional[Iterable[Address]] = None,
        to_set: Optional[Iterable[Address]] = None,
        type_set: Optional[Iterable[Address]] = None,
        homedoc: Optional[Address] = None,
    ) -> List[Link]:
        """FINDLINKS: scan with optional from/to/type/homedoc filters.

        type_set filter is **prefix-match per L10** on type addresses —
        a query at a parent type's address matches every subtype whose
        address extends the parent's. To get an exact-subtype match,
        pass the leaf type's address.

        from_set / to_set match if any query address appears in the
        corresponding link endset (set intersection, non-empty).

        homedoc filter compares against link.homedoc (derived from the
        link's address per ASN-0043).
        """
        from_filter = set(from_set) if from_set is not None else None
        to_filter = set(to_set) if to_set is not None else None
        type_queries = list(type_set) if type_set is not None else None

        out: List[Link] = []
        for link in self._links:
            if homedoc is not None and link.homedoc != homedoc:
                continue
            if from_filter is not None and from_filter.isdisjoint(link.from_set):
                continue
            if to_filter is not None and to_filter.isdisjoint(link.to_set):
                continue
            if type_queries is not None:
                if not any(
                    _is_prefix_or_equal(q, t)
                    for q in type_queries
                    for t in link.type_set
                ):
                    continue
            out.append(link)
        return out
