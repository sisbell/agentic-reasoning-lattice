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


def version_root(session: Session, addr: Address) -> Address:
    """Walk up the version-parent map to find addr's identity.

    For an identity address (None parent), returns addr itself. For
    a version address (sibling of identity in fan-out, or descendant
    in legacy linear chains), walks parent map up until reaching the
    root. Uses State.parent dict directly — O(depth_up) with the
    children-index in place.
    """
    cur = addr
    state = session._state
    while True:
        parent = state.parent.get(cur)
        if parent is None:
            return cur
        cur = parent


def version_head(session: Session, doc_addr: Address) -> Address:
    """Walk forward to the latest version.

    Normalizes doc_addr to its version root (identity) first, then
    walks parent map down picking the max-tumbler sibling at each
    level. Returns the same address whether the caller passes
    identity, a prior version, or — in legacy mixed mode — any node
    inside a deep chain rooted at identity.1.

    Cost: O(depth_up + depth_down). For fan-out, depth_down=1. For
    legacy linear chains, depth_down equals chain depth.
    """
    cur = version_root(session, doc_addr)
    while True:
        children = session.version_children(cur)
        if not children:
            return cur
        cur = children[-1]


def is_head_version(session: Session, doc_addr: Address) -> bool:
    """True iff doc_addr is the latest version of its doc.

    Walk-up + compare: normalizes to identity, finds the head from
    there, returns whether doc_addr equals it. Works uniformly for
    fan-out (head is max sibling of identity), legacy linear chains
    (head is the deepest descendant), and any stale-version reference
    (returns False).

    The prior implementation `not session.version_children(addr)`
    returned True for any leaf in the parent map — which under
    fan-out is every sibling and under legacy linear chains is the
    deepest descendant. After fan-out lands, a non-head sibling
    has no version_children of its own but is still not the head;
    leaf-check returns True incorrectly. Walk-up + compare is
    structurally correct in all three regimes.
    """
    return doc_addr == version_head(session, doc_addr)


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

    Walks the supersession link graph, not the parent map. The two
    representations agree for register_version-generated chains
    (parent map and supersession links are co-maintained), but
    sidecar↔aggregate relationships use ONLY supersession links —
    the aggregate is a separate doc joined to its sidecar via an
    explicit `supersession` link, not via parent-map versioning.
    Callers (motif, foundation, cascade `_assembly_artifact_or_self`)
    rely on this to surface the aggregate from a sidecar base.
    """
    last = doc_addr
    for addr in _walk_supersession(session, doc_addr):
        last = addr
    return last


def latest_doc_head(session: Session, doc_addr: Address) -> Address:
    """Latest path-bearing (identity) address in the supersession chain.

    Version markers emitted by `register_version` are internal chain
    nodes: they record that a doc's content advanced, but they have no
    file path of their own (`path_for_addr(marker) = None`). Callers
    that READ the doc — foundation loader, motif citation targets,
    anyone calling `read_doc` on the result — need the latest *identity*
    address, not the raw chain head.

    Implementation: walk `supersession_head` then normalize through
    `version_root`. The composition handles all three chain shapes:

      - Sidecar edited, no decompose: `head = sidecar.v_N` (version
        marker); `version_root → sidecar` (base).
      - Sidecar decomposed: `head = claims.statements` (already
        identity); `version_root` is a no-op.
      - Sidecar decomposed, aggregate refreshed: `head =
        claims.statements.v_N`; `version_root → claims.statements`.

    For callers tracking chain *advancement* (cascade-fresh predicates
    via `is_head_version`), use `supersession_head` directly — those
    callers handle version markers internally.
    """
    return version_root(session, supersession_head(session, doc_addr))


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
