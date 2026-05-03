"""Citation-graph predicates.

Outgoing/incoming citation traversal over `citation.depends` links.
Retracted citations drop from the graph automatically.

These predicates take a `State` directly today; the planned port to
`Session` lands in a follow-up commit.
"""

from __future__ import annotations

from typing import List, Set

from lib.backend.addressing import Address
from lib.backend.predicates import active_links
from lib.backend.state import State


def depends(state: State, doc_addr: Address) -> List[Address]:
    """Docs this doc depends on (active `citation.depends` from doc)."""
    out: Set[Address] = set()
    for link in active_links(state, "citation.depends", from_set=[doc_addr]):
        out.update(link.to_set)
    return sorted(out, key=lambda a: a.digits)


def dependents(state: State, doc_addr: Address) -> List[Address]:
    """Docs that depend on this doc (active `citation.depends` to doc)."""
    out: Set[Address] = set()
    for link in active_links(state, "citation.depends", to_set=[doc_addr]):
        out.update(link.from_set)
    return sorted(out, key=lambda a: a.digits)
