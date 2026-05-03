"""Version-chain predicates.

Walk the version-parent map for sibling enumeration and head selection.
No retraction filtering applies — version edges are structural, not
link-typed. The substrate primitive is `Session.version_children`;
`version_head` and `is_head_version` compose on it.
"""

from __future__ import annotations

from typing import List

from lib.backend.addressing import Address
from lib.febe.protocol import Session


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
