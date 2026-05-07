"""Scouts — substrate-bearing agents that analyze structural conditions.

Per `docs/hypergraph-protocol/agent-castes.md`: scouts patrol the link
graph (or, more broadly, structural conditions across artifacts),
detect anomalies and structural violations, and emit findings or
classifications about what they find — but they don't author the
content of artifacts.

Caste-defining axes:
- Create-side (grant new substrate identity — finding docs)
- Working surface: structural form / graph patterns, not content prose

Helpers consumed by scouts (similarity scoring, bridge analysis,
future s-components / reconciliation primitives) live in
`lib/scout_services/`. The scouts themselves — predicate-fired Agent
classes that the runner walks — live here.

Current scouts:
- `claim_structural_audit` — runs the structural validator per claim
- `bridge_probe` — discovers cross-lattice bridges via similarity probes

Future: reconciliation, s-components, duplicate-detection.
"""
