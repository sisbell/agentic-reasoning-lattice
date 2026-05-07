"""Scout services — middleware helpers consumed by scout-caste agents.

Scouts (per docs/hypergraph-protocol/agent-castes.md) operate on the
*graph structure* of the substrate. They patrol the link graph, detect
anomalies and structural conditions, and emit findings or
classifications. This module houses the helpers they call: claim
similarity scoring, bridge-graph analysis, and (later) reconciliation
predicates, s-component analysis, duplicate detection.

Modern N-tier mapping: this is the application middleware tier between
FEBE clients and the substrate back end. Nelson's term for the same
slot is "middle end" (Literary Machines 4/72: scanning, search, and
complex queries execute here rather than in the back end). The naming
foregrounds *who consumes these helpers* — the scout caste — over the
historical positional name.

Current contents:

- `similarity` — the SimilarityService Protocol (stable interface for
  claim-similarity scoring) plus pluggable implementations
  (LLMJudgeSimilarity today; embeddings, s-components, hybrid later).
- `bridge` — bridge analysis (analyze_bridge, suggest_probe_targets).
  Consumed by the bridge_probe scout (lib/agents/scouts/bridge_probe.py).

Both are stubbed at present. The architectural commitments (stable
similarity interface, bridge analysis surface) are in place; concrete
implementations land in follow-up commits.

The scouts that consume these services live in `lib/agents/scouts/`.
This module provides the substrate-graph analytical primitives; the
scout agents themselves provide the predicate-fired loops and identity
emission.

See `docs/hypergraph-protocol/agent-castes.md` for the caste taxonomy,
`docs/hypergraph-protocol/architecture.md` for the N-tier picture,
and `docs/hypergraph-protocol/bridges.md` for the bridge_probe design.
"""

from .similarity import (
    CandidateMatch,
    LLMJudgeSimilarity,
    SimilarityScore,
    SimilarityService,
)

__all__ = [
    "CandidateMatch",
    "LLMJudgeSimilarity",
    "SimilarityScore",
    "SimilarityService",
]
