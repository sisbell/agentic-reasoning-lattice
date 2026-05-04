"""Structural-rule-fix agent — repairs per-rule violations in claim files.

Pairs with the structural validator (`scripts/claim-validate.py`).
The validator finds violations of structural invariants (label
matching, declaration uniqueness, depends agreement, reference
resolution, dependency acyclicity); this agent applies per-rule
fixes via Claude's Edit tool.

Each rule has its own prompt under
`prompts/shared/claim-convergence/validate-revise/<rule>.md`. The
agent loads the right template, renders findings + metadata into it,
and invokes Claude with Read+Edit (apply mode) or Read-only (propose
mode for `acyclic-depends`).
"""

from .body import (
    StructuralRuleFixResult,
    fix_structural_rule,
    propose_structural_fix,
)

__all__ = [
    "StructuralRuleFixResult",
    "fix_structural_rule",
    "propose_structural_fix",
]
