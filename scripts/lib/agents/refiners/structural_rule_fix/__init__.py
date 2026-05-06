"""Claim structural-rule-fix agent — refiner for structural validator findings.

Public surface:
- ClaimStructuralFixAgent — Agent class fired by the claim-structural-fix
  trigger. One fire = one claim's structural quiescence work.
- fix_structural_rule, propose_structural_fix — LLM-call helpers used
  by the agent. propose_structural_fix is legacy (orchestrator-only;
  retired alongside acyclic-depends); kept while the orchestrator
  still imports it. Will retire when the orchestrator is deleted.
"""

from .agent import ClaimStructuralFixAgent
from .helpers import (
    StructuralRuleFixResult,
    fix_structural_rule,
    propose_structural_fix,
)

__all__ = [
    "ClaimStructuralFixAgent",
    "StructuralRuleFixResult",
    "fix_structural_rule",
    "propose_structural_fix",
]
