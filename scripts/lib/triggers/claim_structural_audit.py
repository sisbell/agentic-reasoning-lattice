"""Claim-structural-audit trigger — fires per claim with stale audit.

  scope:     each claim-classified derivation of the ASN's source note
             (CLI), or every claim (daemon)
  predicate: skip if claim has no Formal Contract section yet, or
             the latest structural audit was clean, or its findings
             are still in flight
  agent:     ClaimStructuralAuditAgent

The FC gate keeps the validator from running on a contract-less
claim. The validator's checks (depends agreement, declared symbols
resolve, references resolve, etc.) all operate on the Formal
Contract block — without one, the validator returns zero violations
on an empty FC and emits a false-clean audit. Wait for
`claim_formal_contract` to land before auditing.
"""

from __future__ import annotations

from lib.agents.scouts.claim_structural_audit import (
    ClaimStructuralAuditAgent,
)
from lib.backend.addressing import Address
from lib.predicates import has_formal_contract, is_claim_audit_fresh
from lib.protocols.febe.protocol import Session
from lib.runner import Trigger
from lib.triggers._commit_paths import per_asn_claim_review_paths
from lib.triggers.scope import per_claim_of_asn


def _predicate(session: Session, addr: Address) -> bool:
    """True (skip) iff:
      - claim has no Formal Contract section yet, OR
      - latest structural audit was clean / findings in flight
        (`is_claim_audit_fresh`).
    """
    if not has_formal_contract(session, addr):
        return True
    return is_claim_audit_fresh(session, addr)


claim_structural_audit = Trigger(
    name="claim-structural-audit",
    scope_query=per_claim_of_asn,
    predicate=_predicate,
    agent=ClaimStructuralAuditAgent(),
    supports_claim_filter=True,
    commit_paths=per_asn_claim_review_paths,
)
