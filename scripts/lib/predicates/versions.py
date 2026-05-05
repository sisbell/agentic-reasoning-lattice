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


def supersession_head(session: Session, doc_addr: Address) -> Address:
    """Walk outgoing `supersession` link chain to the head version.

    Each step picks the highest-tumbler outgoing target. Cycle-
    protected. Head = address with no outgoing supersession link.

    This is the link-based head walk (per LM 4/52-4/53). For docs
    whose versioning lives in the tumbler version field, use
    `version_head` instead — the substrate currently lacks
    version-bearing addresses, so `supersession` links carry the
    version progression explicitly.
    """
    visited = {doc_addr}
    current = doc_addr
    while True:
        outgoing = session.active_links("supersession", from_set=[current])
        if not outgoing:
            return current
        targets = [t for link in outgoing for t in link.to_set]
        if not targets:
            return current
        next_addr = max(targets, key=lambda a: a.digits)
        if next_addr in visited:
            return current
        visited.add(next_addr)
        current = next_addr
