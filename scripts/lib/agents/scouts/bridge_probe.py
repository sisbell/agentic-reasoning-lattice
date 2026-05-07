"""Bridge-probe scout — discover cross-lattice bridges via similarity.

Caste: scout. Working surface = the bridge subgraph: cross-lattice
citation links, bridge-member edges, saturation markers. Per fire on
a (local_claim, remote_lattice) pair, the scout selects candidate
remote claims via a SimilarityService, confirms high-scoring matches
as cross-lattice citations, and — when the resulting bridge graph is
dense enough by s-component analysis — files a saturation marker that
downstream synthesis can key on.

Per docs/hypergraph-protocol/bridges.md, the discovery loop is:

    1. Similarity hypothesis-probe (similarity service)
    2. Structural expansion (cones)
    3. Region-bounded hypothesis-probes
    4. Confirmation and citation (cross-lattice citation links)
    5. Bridge-graph gap analysis (lib/scout_services/bridge.py)

Identity grants per fire:

  - cross-lattice `citation` links from confirmed matches
  - `bridge_member` edges tying citations to a bridge doc (when
    bridges aggregate multiple confirmed matches)
  - saturation marker on the bridge doc when the gap analysis says
    the bridge is mature; the runner reads the marker and dispatches
    synthesis downstream

This scout does NOT run synthesis or extraction — those are downstream
producers triggered by the saturation marker.

STUB. The architectural skeleton is in place (Agent class, helper
service split between this scout and `lib/scout_services/`), but the
discovery loop's body is not yet implemented. `run()` raises
NotImplementedError. Real implementation lands when probe-agent work
begins.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, List, Optional

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.backend.links import Link
from lib.protocols.febe.protocol import Session
from lib.scout_services.similarity import (
    CandidateMatch, LLMJudgeSimilarity, SimilarityService,
)


@dataclass
class ProbeResult:
    """Outcome of a single per-fire bridge-probe call."""
    matches: List[CandidateMatch] = field(default_factory=list)


class BridgeProbeAgent(Agent):
    """One (local_claim, remote_lattice) probe per fire.

    Stub. The Agent class shape is settled; the run() body will be
    filled in when probe-agent work begins. Until then, run() raises
    NotImplementedError to make accidental fires loud.
    """

    role: ClassVar[str] = "bridge-probe"

    def __init__(
        self, *,
        similarity: Optional[SimilarityService] = None,
        max_candidates: int = 10,
    ):
        self.similarity = similarity or LLMJudgeSimilarity()
        self.max_candidates = max_candidates

    def run(
        self, session: Session, local_claim: Address,
        *, remote_lattice: str,
    ) -> AgentResult:
        raise NotImplementedError(
            "bridge_probe scout not yet implemented; this is the "
            "architectural skeleton only"
        )


# ─── Lower-level primitives (scout-internal) ────────────────────────
#
# Kept as free functions so individual phases of the discovery loop
# are testable and replaceable independently. The Agent class above
# composes them in run(); callers outside the scout caste should
# generally go through the Agent class, not these primitives.


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
    raise NotImplementedError("bridge-probe connection-confirm not yet implemented")


def mark_saturated(session: Session, bridge: Address) -> Link:
    """File the saturation marker on a bridge.

    The scout's terminal action. The runner detects the marker via
    structural trigger and dispatches synthesis discovery (per
    architecture.md's trigger-graph model).

    Real implementation: emit a `bridge.saturated` classifier link on
    the bridge doc (or a separate saturation link, depending on the
    substrate-shape decision in bridges.md's open questions).
    """
    raise NotImplementedError("bridge-probe saturation marker not yet implemented")
