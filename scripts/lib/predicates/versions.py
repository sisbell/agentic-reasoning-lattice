"""Version-chain predicates.

Walk the version-parent map for sibling enumeration and head selection.
No retraction filtering applies — version edges are structural, not
link-typed. The substrate primitive is `Session.version_children`;
`version_head` and `is_head_version` compose on it.
"""

from __future__ import annotations

from typing import List

from lib.backend.addressing import Address
from lib.protocols.febe.protocol import Session


def version_children(session: Session, doc_addr: Address) -> List[Address]:
    """Immediate version-children of this doc, sorted by sibling order."""
    return session.version_children(doc_addr)


def version_head(session: Session, doc_addr: Address) -> Address:
    """Walk forward to the deepest descendant in the linear chain.

    At each level, picks the highest-numbered sibling. Branches
    (versions of an earlier version that aren't the latest) are not
    followed.
    """
    cur = doc_addr
    while True:
        children = session.version_children(cur)
        if not children:
            return cur
        cur = children[-1]


def is_head_version(session: Session, doc_addr: Address) -> bool:
    return not session.version_children(doc_addr)


def _walk_supersession(session: Session, doc_addr: Address):
    """Yield each node in the supersession chain starting at doc_addr.

    Cycle-protected. At each step picks the highest-tumbler outgoing
    target as the next node. Per LM 4/52-4/53.
    """
    visited = {doc_addr}
    current = doc_addr
    yield current
    while True:
        outgoing = session.active_links("supersession", from_set=[current])
        if not outgoing:
            return
        targets = [t for link in outgoing for t in link.to_set]
        if not targets:
            return
        next_addr = max(targets, key=lambda a: a.digits)
        if next_addr in visited:
            return
        visited.add(next_addr)
        current = next_addr
        yield current


def supersession_head(session: Session, doc_addr: Address) -> Address:
    """Head version (terminal node) of doc_addr's supersession chain.

    For docs whose versioning lives in the tumbler version field,
    use `version_head` instead — the substrate currently lacks
    version-bearing addresses, so supersession links carry the
    version progression explicitly.
    """
    last = doc_addr
    for addr in _walk_supersession(session, doc_addr):
        last = addr
    return last


def supersession_chain_length(session: Session, doc_addr: Address) -> int:
    """Number of nodes in doc_addr's supersession chain.

    Returns 1 if doc_addr has no outgoing supersession. Each
    register_version emission advances the count by one.

    Use chain length to compare "how many edits / attestations" has
    X had across docs in different allocator subspaces — direct
    tumbler comparison doesn't give cross-subspace allocation-time
    ordering, but chain length is purely structural counting.
    """
    return sum(1 for _ in _walk_supersession(session, doc_addr))
