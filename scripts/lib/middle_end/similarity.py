"""SimilarityService — claim-similarity scoring as a middleware service.

The probe agent (and any other consumer) calls into a similarity
service via the SimilarityService Protocol. The implementation is
pluggable: today we provide LLMJudgeSimilarity (Claude scores a pair
0-100 with rationale); future implementations may use embeddings,
s-components, or hybrids — all behind the same interface.

Architectural commitments:

- Similarity is a *middleware* operation (per architecture.md), not
  a substrate primitive. It composes substrate reads (claim bodies)
  with whatever scoring algorithm the implementation provides.
- The interface takes claim *references* (Addresses + remote-lattice
  identifier), not claim bodies. Implementations read bodies via
  Session — which routes through BEBE for peer-node addresses
  transparently.
- The output is a stable shape: `SimilarityScore(score, rationale)`
  per pair, and `CandidateMatch` for multi-candidate results.
- Probe-agent code consumes the Protocol, never a specific
  implementation. Swapping algorithms is a configuration change.

Stubbed today: LLMJudgeSimilarity returns score=0 with rationale
"stub". Real implementation lands when probe-agent work begins.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from lib.backend.addressing import Address
from lib.febe.protocol import Session


@dataclass
class SimilarityScore:
    """Result of a single pairwise similarity judgment."""
    score: float          # 0-100; higher means more similar
    rationale: str        # short explanation of the score


@dataclass
class CandidateMatch:
    """A scored candidate match between a local claim and a remote claim."""
    local: Address
    remote: Address
    remote_lattice: str
    similarity: SimilarityScore


@runtime_checkable
class SimilarityService(Protocol):
    """Stable interface for claim-similarity scoring.

    Implementations: LLMJudgeSimilarity today. Future: embeddings,
    s-components on shared-symbol hypergraph, hybrid approaches.

    The service reads claim bodies via the passed Session (which
    routes through BEBE for peer-node addresses). Callers don't
    need to materialize bodies themselves.
    """

    def score(
        self,
        session: Session,
        local: Address,
        remote: Address,
        remote_lattice: str,
    ) -> SimilarityScore:
        """Score similarity between two claims by their addresses."""
        ...


class LLMJudgeSimilarity:
    """LLM-as-judge implementation. Claude scores a claim pair 0-100.

    Stub implementation returns score=0 with rationale "stub".
    Real implementation (loads claim bodies, prompts Claude with
    structured output, parses score + rationale) lands when probe-
    agent work begins.
    """

    def __init__(self, model: str = "claude-haiku-4-5") -> None:
        self.model = model

    def score(
        self,
        session: Session,
        local: Address,
        remote: Address,
        remote_lattice: str,
    ) -> SimilarityScore:
        # Stub. Real implementation:
        #   1. local_body = session.read_document(local)
        #   2. remote_body = session.read_document(remote)
        #      (BEBE-dispatched if remote is on a peer node)
        #   3. prompt = render_judge_template(local_body, remote_body)
        #   4. text = invoke_claude(prompt, model=self.model)
        #   5. score, rationale = parse(text)
        return SimilarityScore(score=0.0, rationale="stub")
