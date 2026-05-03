"""Version-chain predicates over the parent map.

VER3 version chains are stored on `state.parent`; these helpers walk
that map for sibling enumeration and head selection. No retraction
filtering applies — version edges are structural, not link-typed.
"""

from __future__ import annotations

from typing import List

from lib.backend.addressing import Address
from lib.backend.state import State


def version_children(state: State, doc_addr: Address) -> List[Address]:
    """Immediate version-children of this doc, sorted by sibling order."""
    return sorted(
        (a for a, p in state.parent.items() if p == doc_addr),
        key=lambda a: a.digits,
    )


def version_head(state: State, doc_addr: Address) -> Address:
    """Walk forward to the deepest descendant in the linear chain.

    At each level, picks the highest-numbered sibling. Branches
    (versions of an earlier version that aren't the latest) are not
    followed.
    """
    cur = doc_addr
    while True:
        children = version_children(state, cur)
        if not children:
            return cur
        cur = children[-1]


def is_head_version(state: State, doc_addr: Address) -> bool:
    return not version_children(state, doc_addr)
