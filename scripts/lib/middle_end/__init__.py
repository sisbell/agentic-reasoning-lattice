"""Middle end — Nelson's term for what we'd call middleware today.

Per Literary Machines 4/72: the middle end parses user commands and
passes through standard FEBE commands; scanning, search, and complex
queries execute here rather than in the back end.

Modern N-tier mapping: this is the application middleware tier between
FEBE clients and the substrate back end. Houses search, scan, version
comparison, probe primitives, bridge analysis — operations that
compose multiple substrate primitives or add capability the back end
doesn't have.

Current contents:

- `similarity` — the SimilarityService Protocol (stable interface for
  claim-similarity scoring) plus pluggable implementations
  (LLMJudgeSimilarity today; embeddings, s-components, hybrid later).
- `probe` — probe-agent primitives (probe_remote, confirm_connection,
  mark_saturated). Consumes a SimilarityService.
- `bridge` — bridge analysis (analyze_bridge, suggest_probe_targets).

All three are stubbed at present. The architectural commitments
(stable interface for similarity, probe-agent contract, bridge
analysis surface) are in place; concrete implementations land in
follow-up commits.

See `docs/hypergraph-protocol/architecture.md` for the N-tier picture
and `docs/hypergraph-protocol/bridges.md` for the probe-agent design.
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
