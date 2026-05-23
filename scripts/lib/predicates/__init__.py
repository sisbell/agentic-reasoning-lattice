"""Centralized predicate layer.

Predicates are pure functions over link state. They read the active
link set (via Session) and compute verdicts from its shape; they are
never stored as facts. The substrate primitives they compose on
(`active_links`, `retracted_link_addrs`) live in
`lib/backend/predicates.py`; everything above that — the composite
predicates that other code depends on — lives here, grouped by the
question being asked.

Module organization (by domain concept):
- `convergence.py`     — convergence-protocol predicates
- `attributes.py`      — attribute-link presence
- `citations.py`       — citation graph
- `versions.py`        — version-chain helpers
- `classifiers.py`     — classifier enumeration
- `reconciliation.py`  — partial-failure detection (orphan / dangling)

For convenience, every public predicate is re-exported here so callers
can `from lib.predicates import X` without choosing a submodule.
Submodule imports work too and may be preferred for clarity.
"""

from .attributes import (
    description_is_fresh,
    description_sidecar_of,
    has_description,
    has_label,
    has_name,
    has_signature,
    has_statements,
    references_is_fresh,
    references_sidecar_of,
    signature_is_fresh,
    signature_sidecar_of,
    statements_is_fresh,
    statements_sidecar_of,
)
from .agents import (
    agent_scope_for, is_held, resolve_to_scope, stale_holdings,
)
from .cascade import (
    claims_statements_for_note,
    description_is_fresh_after_asn_confirmation,
    is_cascade_fresh_one_hop,
    is_claims_statements_fresh,
    is_note_cascade_fresh,
    is_upstream_settled_one_hop,
    signature_is_fresh_after_asn_confirmation,
)
from .citations import depends, dependents
from .consultation import (
    all_open_revises_consulted,
    has_consultation_for_inquiry,
    has_note_for_inquiry,
    is_finding_consulted,
)
from .classifiers import (
    all_claim_addrs,
    all_classified,
    claim_formal_contract_is_fresh,
    current_contract_kind,
    has_contract_kind,
    has_formal_contract,
    is_review_decomposed,
    is_retired,
)
from .quiescence import (
    derived_claims,
    has_been_reviewed,
    has_resolution,
    is_asn_confirmed,
    is_asn_quiescent,
    is_claim_audit_fresh,
    is_claim_confirmed,
    is_claim_quiescent,
    is_claim_structurally_clean,
    is_quiescent,
    is_doc_quiescent,
    last_n_reviews_were_clean,
    latest_review_for_addr,
    latest_structural_audit_for_claim,
    latest_review_was_clean,
    unresolved_revise_comments,
)
from .reconciliation import (
    dangling_attribute_links,
    dangling_claim_finding_links,
    dangling_note_finding_links,
    orphan_claim_finding_docs,
    orphan_note_finding_docs,
    orphan_sidecars,
)
from .versions import (
    is_head_version, supersession_chain_length, supersession_head,
    version_children, version_head, version_root,
)

__all__ = [
    "all_claim_addrs",
    "all_classified",
    "all_open_revises_consulted",
    "claim_formal_contract_is_fresh",
    "claims_statements_for_note",
    "description_is_fresh_after_asn_confirmation",
    "current_contract_kind",
    "has_contract_kind",
    "has_formal_contract",
    "dangling_attribute_links",
    "dangling_claim_finding_links",
    "dangling_note_finding_links",
    "depends",
    "dependents",
    "derived_claims",
    "description_is_fresh",
    "description_sidecar_of",
    "has_been_reviewed",
    "has_consultation_for_inquiry",
    "has_description",
    "has_label",
    "has_name",
    "has_note_for_inquiry",
    "has_resolution",
    "has_signature",
    "has_statements",
    "agent_scope_for",
    "is_asn_confirmed",
    "is_asn_quiescent",
    "is_cascade_fresh_one_hop",
    "is_held",
    "resolve_to_scope",
    "stale_holdings",
    "is_claim_audit_fresh",
    "is_claim_confirmed",
    "is_claim_quiescent",
    "is_claim_structurally_clean",
    "is_claims_statements_fresh",
    "is_note_cascade_fresh",
    "is_review_decomposed",
    "is_quiescent",
    "is_doc_quiescent",
    "is_finding_consulted",
    "is_head_version",
    "is_retired",
    "is_upstream_settled_one_hop",
    "last_n_reviews_were_clean",
    "latest_review_for_addr",
    "latest_review_was_clean",
    "latest_structural_audit_for_claim",
    "orphan_claim_finding_docs",
    "orphan_note_finding_docs",
    "orphan_sidecars",
    "references_is_fresh",
    "references_sidecar_of",
    "signature_is_fresh",
    "signature_is_fresh_after_asn_confirmation",
    "signature_sidecar_of",
    "statements_is_fresh",
    "statements_sidecar_of",
    "supersession_chain_length",
    "supersession_head",
    "unresolved_revise_comments",
    "version_children",
    "version_head",
    "version_root",
]
