"""Claim-structural-audit trigger — fires per claim with stale audit.

  scope:     each claim-classified derivation of the ASN's source note
             (CLI), or every claim (daemon)
  predicate: is_claim_audit_fresh (skip if the latest structural audit
             was clean or its findings are still in flight)
  agent:     ClaimStructuralAuditAgent
"""

from __future__ import annotations

from lib.agents.scouts.claim_structural_audit import (
    ClaimStructuralAuditAgent,
)
from lib.predicates import is_claim_audit_fresh
from lib.runner import Trigger
from lib.triggers.scope import per_claim_of_asn


claim_structural_audit = Trigger(
    name="claim-structural-audit",
    scope_query=per_claim_of_asn,
    predicate=is_claim_audit_fresh,
    agent=ClaimStructuralAuditAgent(),
    supports_claim_filter=True,
)
