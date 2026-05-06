"""Trigger declarations — wire substrate predicates to agents.

Each trigger declares: scope query, predicate, agent. The runner
walks them. Adding a trigger means writing a new module here; it
does not change the runner.
"""

from .claim_describe import claim_describe
from .claim_findings import claim_findings
from .claim_revise import claim_revise
from .claim_structural_fix import claim_structural_fix
from .cone_review import apex_labels_in_topological_order, cone_review
from .full_review import full_review
from .inquiry_consult import inquiry_consult
from .note_consult import note_consult
from .note_draft import note_draft
from .note_review import note_review
from .note_revise import note_revise
from .note_statements import note_statements

__all__ = [
    "apex_labels_in_topological_order",
    "claim_describe",
    "claim_findings",
    "claim_revise",
    "claim_structural_fix",
    "cone_review",
    "full_review",
    "inquiry_consult",
    "note_consult",
    "note_draft",
    "note_review",
    "note_revise",
    "note_statements",
]
