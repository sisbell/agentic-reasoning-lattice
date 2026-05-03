"""Centralized predicate layer.

Predicates are pure functions over link state. They read the active
link set (via Session or State) and compute verdicts from its shape;
they are never stored as facts. The substrate primitives they compose
on (`active_links`, `retracted_link_addrs`) live in
`lib/backend/predicates.py`; everything above that — the composite
predicates that other code depends on — lives here, grouped by the
question being asked.

Module organization (by domain concept):
- `convergence.py` — convergence-protocol predicates
  (`is_doc_converged`, `is_claim_converged`, `is_converged`,
  `is_asn_converged`, `has_resolution`, `unresolved_revise_comments`)
- `attributes.py`  — attribute-link presence
  (`has_description`, `has_signature`, `has_name`, `has_label`,
  `description_sidecar_of`, `signature_sidecar_of`)
- `citations.py`   — citation graph (`depends`, `dependents`)
- `versions.py`    — version-chain helpers
  (`version_children`, `version_head`, `is_head_version`)
- `classifiers.py` — classifier enumeration
  (`all_claim_addrs`, `current_contract_kind`, `all_classified`)

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
    has_resolution,
    is_asn_converged,
    is_claim_converged,
    is_converged,
    is_doc_converged,
    unresolved_revise_comments,
)
from .versions import is_head_version, version_children, version_head

__all__ = [
    "all_claim_addrs",
    "all_classified",
    "current_contract_kind",
    "depends",
    "dependents",
    "description_sidecar_of",
    "has_description",
    "has_label",
    "has_name",
    "has_resolution",
    "has_signature",
    "is_asn_converged",
    "is_claim_converged",
    "is_converged",
    "is_doc_converged",
    "is_head_version",
    "signature_sidecar_of",
    "unresolved_revise_comments",
    "version_children",
    "version_head",
]
