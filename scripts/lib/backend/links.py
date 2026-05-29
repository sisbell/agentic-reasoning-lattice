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
    """One MAKELINK emission.

    `ts` is Unix-epoch seconds (int) marking emission time. Scoped
    to agentic concerns (stuck-detection, in-flight observability,
    leases) per `feedback_ts_scoped_to_agentic.md` — substrate-side
    structural reasoning uses tumbler-address sequence, not ts.

    ts defaults to None for in-memory test fixtures that don't model
    persistence; production paths always populate it (Store sets ts
    on every emission; load_jsonl parses ts from the persisted record).
    """

    addr: Address
    from_set: Tuple[Address, ...]
    to_set: Tuple[Address, ...]
    type_set: Tuple[Address, ...]
    ts: Optional[int] = None

    @property
    def homedoc(self) -> Address:
        """ASN-0043: link addr structurally extends homedoc.
        split() at last zero → (homedoc, in-doc-link-local)."""
        return self.addr.split()[0]


class LinkStore:
    """Append-only log of MAKELINK emissions.

    Maintains inverted indexes on link emit so find_links runs in O(query
    result size) instead of O(total link count). The substrate today has
    ~47k links; predicates make hundreds of find_links calls per ASN per
    filter pass — the indexed lookup turns minutes of scheduling
    overhead into seconds.

    Indexes (populated lazily in `emit`):
      _by_from[addr]    → set of link.addr where addr ∈ from_set
      _by_to[addr]      → set of link.addr where addr ∈ to_set
      _by_type[addr]    → set of link.addr where addr ∈ type_set (exact)
      _by_addr[addr]    → Link with that addr (O(1) get)

    Type prefix-match (L10) is handled in find_links by walking the
    _by_type keyset for prefixes when a query type has no exact-match
    hit; this keeps the common-case (exact-match) path O(1) while
    preserving subtype semantics.
    """

    def __init__(self) -> None:
        self._links: List[Link] = []
        self._by_from: dict[Address, set[Address]] = {}
        self._by_to: dict[Address, set[Address]] = {}
        self._by_type: dict[Address, set[Address]] = {}
        self._by_addr: dict[Address, Link] = {}

    def __len__(self) -> int:
        return len(self._links)

    def __iter__(self) -> Iterable[Link]:
        return iter(self._links)

    def get(self, addr: Address) -> Link:
        link = self._by_addr.get(addr)
        if link is None:
            raise KeyError(f"no link at {addr}")
        return link

    def emit(
        self,
        addr: Address,
        from_set: Iterable[Address],
        to_set: Iterable[Address],
        type_set: Iterable[Address],
        ts: Optional[int] = None,
    ) -> Link:
        link = Link(
            addr=addr,
            from_set=tuple(from_set),
            to_set=tuple(to_set),
            type_set=tuple(type_set),
            ts=ts,
        )
        self._links.append(link)
        self._by_addr[addr] = link
        for a in link.from_set:
            self._by_from.setdefault(a, set()).add(addr)
        for a in link.to_set:
            self._by_to.setdefault(a, set()).add(addr)
        for a in link.type_set:
            self._by_type.setdefault(a, set()).add(addr)
        return link

    def find_links(
        self,
        from_set: Optional[Iterable[Address]] = None,
        to_set: Optional[Iterable[Address]] = None,
        type_set: Optional[Iterable[Address]] = None,
        homedoc: Optional[Address] = None,
    ) -> List[Link]:
        """FINDLINKS: optional from/to/type/homedoc filters with
        inverted-index acceleration.

        type_set filter is **prefix-match per L10** on type addresses —
        a query at a parent type's address matches every subtype whose
        address extends the parent's. To get an exact-subtype match,
        pass the leaf type's address.

        from_set / to_set match if any query address appears in the
        corresponding link endset (set intersection, non-empty).

        homedoc filter compares against link.homedoc (derived from the
        link's address per ASN-0043).

        Algorithm: pick the smallest filter as the seed candidate set
        (union of inverted-index buckets for each query value), then
        apply the remaining filters in-memory against that subset. The
        cost is O(matching_subset) instead of O(total_link_count).

        When no filter is provided, falls back to a full scan (rare —
        most callers filter by at least one of from/to/type).
        """
        # Collect candidate addrs from any provided filters.
        # The smallest candidate set wins; subsequent filters run as
        # in-memory predicates over that set.
        candidate_sets: List[set[Address]] = []
        from_list = list(from_set) if from_set is not None else None
        to_list = list(to_set) if to_set is not None else None
        type_list = list(type_set) if type_set is not None else None

        if from_list is not None:
            seed: set[Address] = set()
            for a in from_list:
                seed.update(self._by_from.get(a, ()))
            candidate_sets.append(seed)
        if to_list is not None:
            seed = set()
            for a in to_list:
                seed.update(self._by_to.get(a, ()))
            candidate_sets.append(seed)
        if type_list is not None:
            seed = set()
            exact_hits_only = True
            for q in type_list:
                exact = self._by_type.get(q)
                if exact is not None:
                    seed.update(exact)
                # Prefix-match per L10: walk the index keyset for any
                # registered type whose addr extends the query.
                for t_addr, bucket in self._by_type.items():
                    if t_addr == q:
                        continue
                    if _is_prefix_or_equal(q, t_addr):
                        seed.update(bucket)
                        exact_hits_only = False
            candidate_sets.append(seed)

        if not candidate_sets:
            # No filters → full scan with only homedoc test.
            return [
                link for link in self._links
                if homedoc is None or link.homedoc == homedoc
            ]

        # Pick the smallest seed (best selectivity), then intersect
        # against the others.
        candidate_sets.sort(key=len)
        candidates = candidate_sets[0]
        for other in candidate_sets[1:]:
            candidates &= other
            if not candidates:
                return []

        # Apply the original filters in-memory against the surviving
        # candidates. Cheaper than re-iterating since most queries land
        # only a few links.
        from_filter = set(from_list) if from_list is not None else None
        to_filter = set(to_list) if to_list is not None else None

        out: List[Link] = []
        for addr in candidates:
            link = self._by_addr.get(addr)
            if link is None:
                continue
            if homedoc is not None and link.homedoc != homedoc:
                continue
            if from_filter is not None and from_filter.isdisjoint(link.from_set):
                continue
            if to_filter is not None and to_filter.isdisjoint(link.to_set):
                continue
            # type_list already enforced via seed-set; no re-check needed.
            out.append(link)
        return out
