"""Scouts — substrate-bearing agents that analyze structural conditions.

Per `docs/hypergraph-protocol/agent-castes.md`: scouts patrol the link
graph (or, more broadly, structural conditions across artifacts),
detect anomalies and structural violations, and emit findings or
classifications about what they find — but they don't author the
content of artifacts.

Caste-defining axes:
- Create-side (grant new substrate identity — finding docs)
- Working surface: structural form / graph patterns, not content prose

The agent-castes doc earmarks `lib/middle_end/` as the architectural
home for the caste; this directory is the practical home for scout
Agent classes that participate in the runner. Future scouts:
reconciliation predicates, claim-s-components, duplicate-detection.
"""
