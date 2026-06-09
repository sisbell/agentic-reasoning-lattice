"""Substrate predicate primitives.

Two atoms over `State.find_links` that the centralized predicate layer
(`lib/predicates/`) and `Session` both compose on:

- `active_links` — links of a given type that haven't been retracted
- `retracted_link_addrs` — set of link addresses nullified by a retraction

Composite predicates (alignment, version, citation graph, classifier
enumeration, quiescence) live under `lib/predicates/` grouped by the
question they answer. Keep this module small.
"""

from __future__ import annotations

from typing import List, Optional, Set

from .addressing import Address
from .links import Link
from .state import State


_RETRACTED_CACHE: dict[int, tuple[int, Set[Address]]] = {}


def retracted_link_addrs(state: State) -> Set[Address]:
    """Set of link addresses that have been retracted.

    A retraction is a `retraction`-typed link whose to_set contains
    the address of the link being nullified.

    Memoized per State by (id, link count). The link log is append-only,
    so a matching count means the retraction set is unchanged. Callers
    must treat the returned set as read-only.
    """
    inner = getattr(state, "state", state)
    key = id(inner)
    n = len(getattr(inner, "links", ())) if hasattr(inner, "links") else -1
    cached = _RETRACTED_CACHE.get(key)
    if cached is not None and cached[0] == n:
        return cached[1]
    out: Set[Address] = set()
    for r in state.find_links(type_="retraction"):
        out.update(r.to_set)
    _RETRACTED_CACHE[key] = (n, out)
    return out


def active_links(
    state: State,
    type_: str,
    from_set: Optional[List[Address]] = None,
    to_set: Optional[List[Address]] = None,
) -> List[Link]:
    """Links of the given type whose addresses haven't been retracted."""
    retracted = retracted_link_addrs(state)
    candidates = state.find_links(from_set=from_set, to_set=to_set, type_=type_)
    return [link for link in candidates if link.addr not in retracted]
