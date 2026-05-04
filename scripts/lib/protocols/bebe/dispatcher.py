"""BEBE dispatcher — routes cross-node operations to peer nodes.

Stubs only. The simulator runs single-node today; every cross-node
dispatch returns UNREACHABLE. The interface is reserved so Session
method implementations can call into BEBE at the routing seam when
address-prefix inspection identifies a peer dispatch.

When real cross-node work begins, populate the methods to actually
forward operations to peer substrates. The Session call sites won't
need to change — they already call into the dispatcher; only the
dispatcher's internals change.

See `docs/hypergraph-protocol/architecture.md` for the operation set
specification and the dispatch rule (read/query operations forward;
writes stay local).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from lib.backend.addressing import Address
from lib.backend.links import Link


# A node identifier. Simulator uses the lattice directory name
# ("xanadu", "materials"); real Xanadu would use whatever node-naming
# scheme the deployment establishes.
NodeId = str


class PeerStatus(str, Enum):
    """Reachability of a peer node.

    Per Nelson 4/75: networks are always broken. Standard operating
    procedure for unreachable peers — fall back to backup copies if
    redundancy exists, otherwise return "not currently available."
    """

    REACHABLE = "reachable"
    UNREACHABLE = "unreachable"
    PARTIAL = "partial"


@dataclass
class IndexSummary:
    """Structural map of a peer's substrate.

    Per Nelson 4/71: each server holds a "continuously valid model
    or subrepresentation of the entire docuverse." This is the
    structural component of subrepresentation — link counts by type,
    document index, partial address ranges. Cheap to maintain;
    doesn't require materializing peer content.
    """

    node: NodeId
    captured_at: datetime
    doc_count: int = 0
    link_counts: Dict[str, int] = field(default_factory=dict)
    # Future: partial address range coverage, classifier counts,
    # versioning chain depths, etc.


class BEBEDispatcher:
    """Routes cross-node operations to peer nodes.

    Single-node simulator default: no peers configured. Every method
    returns the "not available" path. Real implementation populates
    these when first cross-node work begins.
    """

    def __init__(self, peers: Optional[Dict[NodeId, str]] = None):
        # Map of node id → lattice directory path (or eventually a
        # connection descriptor / wire endpoint).
        self.peers: Dict[NodeId, str] = peers or {}

    # ── Forwarding operations ──────────────────────────────────────

    def forward_read(self, peer: NodeId, addr: Address) -> Optional[str]:
        """Pull a doc's bytes from peer's substrate.

        Returns the doc content as bytes/str, or None if peer is
        unreachable. Stub implementation always returns None.
        """
        return None

    def forward_find_links(self, peer: NodeId, **filters: Any) -> List[Link]:
        """Query peer's substrate for matching links.

        Used when citation-following crosses a node boundary — agent
        wants the outgoing/incoming links of a peer-owned doc.
        Returns matching links from peer's substrate, or empty list
        if peer is unreachable. Stub returns empty list.
        """
        return []

    def forward_middleware(
        self,
        peer: NodeId,
        op: str,
        **args: Any,
    ) -> Optional[Any]:
        """Forward a middleware operation to peer's middleware tier.

        Generic dispatch for cross-node middleware calls — probe_remote,
        search, version comparison, etc. The op string names the
        middleware operation; args are operation-specific. Returns
        whatever the peer's middleware returns, or None if unreachable.
        Stub returns None.
        """
        return None

    # ── Peer state ─────────────────────────────────────────────────

    def peer_status(self, peer: NodeId) -> PeerStatus:
        """Current reachability of a peer node.

        Stub returns UNREACHABLE for any unconfigured peer (i.e., all
        peers in single-node simulator).
        """
        if peer in self.peers:
            return PeerStatus.UNREACHABLE  # configured but unreachable in stub
        return PeerStatus.UNREACHABLE  # unknown peer

    def peer_index_summary(self, peer: NodeId) -> Optional[IndexSummary]:
        """Cached structural map of peer's substrate.

        The structural component of subrepresentation — supports
        queries like "is this Address resolvable on peer X?" without
        materializing content. Stub returns None (no summary cached).
        """
        return None

    # ── Address routing ────────────────────────────────────────────

    def peer_for_address(self, addr: Address) -> Optional[NodeId]:
        """Identify which peer node owns a given Address.

        Inspects the Address's prefix and matches against configured
        peer prefixes. Returns the peer's NodeId, or None if the
        Address belongs to the local node (or no peer matches).
        Stub returns None — no peer prefixes configured.
        """
        return None
