"""Probe-agent primitives — find similar claims, file bridges, mark saturated.

The probe agent's contract (per docs/hypergraph-protocol/bridges.md):

    Given a local lattice and one or more remote lattices, discover
    structural bridges via the discovery loop, file a saturation
    marker when a bridge matures, exit. Synthesis is dispatched
    downstream by the runner via structural trigger; this agent
    does not run synthesis or extraction.

This module provides the operations the probe agent calls. They
consume a SimilarityService (pluggable scoring) and a Session
(substrate access). All are stubbed; real implementations land
when probe-agent work begins.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from lib.backend.addressing import Address
from lib.backend.links import Link
from lib.protocols.febe.protocol import Session

from .similarity import CandidateMatch, SimilarityService


@dataclass
class ProbeResult:
    """Outcome of a single probe_remote call."""
    matches: List[CandidateMatch] = field(default_factory=list)


def probe_remote(
    session: Session,
    local_claim: Address,
    remote_lattice: str,
    similarity: SimilarityService,
    max_candidates: int = 10,
) -> ProbeResult:
    """Find similar claims in a remote lattice via the similarity service.

    Real implementation:
      1. Select candidate set in remote lattice (full scan / ASN-filter
         / cascade — strategy is implementation choice).
      2. For each candidate, similarity.score(session, local, candidate,
         remote_lattice).
      3. Rank by score, return top max_candidates as CandidateMatch list.

    Stub: returns empty matches.
    """
    return ProbeResult(matches=[])


def confirm_connection(
    session: Session,
    local: Address,
    remote: Address,
    remote_lattice: str,
    bridge: Optional[Address] = None,
) -> Link:
    """File a cross-lattice citation; optionally tag as bridge member.

    Real implementation: emit citation link with cross-node target
    address; if `bridge` is given, also emit a bridge_member link
    from bridge doc to the citation. Idempotent on (local, remote,
    bridge).
    """
    raise NotImplementedError("probe-agent connection-confirm not yet implemented")


def mark_saturated(session: Session, bridge: Address) -> Link:
    """File the saturation marker on a bridge.

    The probe agent's terminal action. The runner detects the
    marker via structural trigger and dispatches synthesis
    discovery (per architecture.md's trigger-graph model).

    Real implementation: emit a `bridge.saturated` classifier link
    on the bridge doc (or a separate saturation link, depending on
    the substrate-shape decision in bridges.md's open questions).
    """
    raise NotImplementedError("probe-agent saturation marker not yet implemented")
