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
    description_sidecar_of,
    has_description,
    has_label,
    has_name,
    has_signature,
    signature_sidecar_of,
)
from .citations import depends, dependents
from .classifiers import (
    all_claim_addrs,
    all_classified,
    current_contract_kind,
)
from .convergence import (
    has_been_reviewed,
    has_resolution,
    is_asn_converged,
    is_claim_confirmed,
    is_claim_converged,
    is_converged,
    is_doc_converged,
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
from .versions import is_head_version, version_children, version_head

__all__ = [
    "all_claim_addrs",
    "all_classified",
    "current_contract_kind",
    "dangling_attribute_links",
    "dangling_claim_finding_links",
    "dangling_note_finding_links",
    "depends",
    "dependents",
    "description_sidecar_of",
    "has_been_reviewed",
    "has_description",
    "has_label",
    "has_name",
    "has_resolution",
    "has_signature",
    "is_asn_converged",
    "is_claim_confirmed",
    "is_claim_converged",
    "is_converged",
    "is_doc_converged",
    "is_head_version",
    "latest_review_for_addr",
    "latest_review_was_clean",
    "orphan_claim_finding_docs",
    "orphan_note_finding_docs",
    "orphan_sidecars",
    "signature_sidecar_of",
    "unresolved_revise_comments",
    "version_children",
    "version_head",
]
