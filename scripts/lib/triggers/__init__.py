"""Trigger declarations — wire substrate predicates to agents.

Each trigger declares: scope query, predicate, agent. The runner
walks them. Adding a trigger means writing a new module here; it
does not change the runner.
"""

from .claim_citation_resolve import claim_citation_resolve
from .claim_contract import claim_contract
from .claim_describe_refresh import claim_describe_refresh
from .claim_signature_refresh import claim_signature_refresh
from .claims_statements_refresh import claims_statements_refresh
from .claim_describe import claim_describe
from .claim_formal_contract import claim_formal_contract
from .claim_findings import claim_findings
from .claim_revise import claim_revise
from .claim_signature_resolve import claim_signature_resolve
from .claim_structural_audit import claim_structural_audit
from .claim_structural_revise import claim_structural_revise
from .cone_review import apex_labels_in_topological_order, cone_review
from .full_review import full_review
from .inquiry_consult import inquiry_consult
from .note_consult import note_consult
from .note_draft import note_draft
from .note_review import note_review
from .note_revise import note_revise
from .note_statements import note_statements
from .patch_apply import patch_apply

__all__ = [
    "apex_labels_in_topological_order",
    "claim_citation_resolve",
    "claim_contract",
    "claim_describe_refresh",
    "claim_signature_refresh",
    "claims_statements_refresh",
    "claim_describe",
    "claim_formal_contract",
    "claim_findings",
    "claim_revise",
    "claim_signature_resolve",
    "claim_structural_audit",
    "claim_structural_revise",
    "cone_review",
    "full_review",
    "inquiry_consult",
    "note_consult",
    "note_draft",
    "note_review",
    "note_revise",
    "note_statements",
    "patch_apply",
]
