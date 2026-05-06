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
    signature_sidecar_of,
    statements_is_fresh,
    statements_sidecar_of,
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
    current_contract_kind,
    is_decomposed,
    is_retired,
)
from .quiescence import (
    derived_claims,
    has_been_reviewed,
    has_resolution,
    is_asn_confirmed,
    is_asn_quiescent,
    is_claim_confirmed,
    is_claim_quiescent,
    is_claim_structurally_clean,
    is_quiescent,
    is_doc_quiescent,
    latest_review_for_addr,
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
    version_children, version_head,
)

__all__ = [
    "all_claim_addrs",
    "all_classified",
    "all_open_revises_consulted",
    "current_contract_kind",
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
    "is_asn_confirmed",
    "is_asn_quiescent",
    "is_claim_confirmed",
    "is_claim_quiescent",
    "is_claim_structurally_clean",
    "is_decomposed",
    "is_quiescent",
    "is_doc_quiescent",
    "is_finding_consulted",
    "is_head_version",
    "is_retired",
    "latest_review_for_addr",
    "latest_review_was_clean",
    "orphan_claim_finding_docs",
    "orphan_note_finding_docs",
    "orphan_sidecars",
    "signature_sidecar_of",
    "statements_is_fresh",
    "statements_sidecar_of",
    "supersession_chain_length",
    "supersession_head",
    "unresolved_revise_comments",
    "version_children",
    "version_head",
]
