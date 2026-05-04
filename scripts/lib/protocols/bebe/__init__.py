"""BEBE — Back End-Back End protocol.

Nelson's node-to-node protocol for connecting servers in the Xanadu
network (Literary Machines 4/70-4/75). Two functions per the spec:

1. **Forwarding** — user requests fan out from local server to peer
   servers that can supply; replies funnel back through the local
   server.
2. **Subrepresentations** — each server maintains a partial map of
   the rest of the docuverse (structural index) plus a content cache
   of materialized peer docs. Maps grow/shrink with demand.

This package is currently **stubs only**. The simulator is single-
node today; cross-node dispatch returns UNREACHABLE for any peer.
The interface is reserved so Session method implementations can
route reads/queries to peer nodes when address-prefix inspection
indicates a peer dispatch is needed. Real implementation arrives
when first cross-node work begins (likely alongside the probe-agent
/ bridges design).

See `docs/hypergraph-protocol/architecture.md` for the BEBE tier in
context (between back end and operational layer), the operation
set, and which Session methods dispatch through BEBE.

The simulator can be extended to exercise real cross-node protocol
shapes by configuring multiple `lattices/<name>/` directories with
distinct allocator prefixes and wiring this dispatcher to route
reads against peer-prefix Addresses to the peer's substrate. That's
the next stage of work; today these are no-op placeholders.
"""

from .dispatcher import BEBEDispatcher, IndexSummary, NodeId, PeerStatus

__all__ = ["BEBEDispatcher", "IndexSummary", "NodeId", "PeerStatus"]
