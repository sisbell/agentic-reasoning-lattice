"""Claim-structural-audit trigger — fires per claim with stale audit.

  scope:     each claim derived from the requested ASN's source note
             (CLI mode), or every active claim (daemon mode)
  predicate: is_claim_audit_fresh (skip if latest audit was clean OR
             its findings are still being closed by the refiner)
  agent:     ClaimStructuralAuditAgent

The first scout-caste trigger in the system. Mirrors claim_describe
and claim_revise scope shapes — walks claim addresses derived from
the ASN's note. Predicate is closure-style staleness: re-fire when
the latest audit's violations have all been resolved (need re-audit
on post-fix state) or when no audit exists yet.
"""

from __future__ import annotations

from typing import Iterator

from lib.agents.scouts.claim_structural_audit import ClaimStructuralAuditAgent
from lib.backend.addressing import Address
from lib.predicates import derived_claims, is_claim_audit_fresh
from lib.protocols.febe.protocol import Session
from lib.runner import Scope, Trigger, asn_note_addr


def _scope_query(session: Session, scope: Scope) -> Iterator[Address]:
    """Yield each claim-classified derivation of the ASN's source note."""
    if scope.asn_label is not None:
        note_addr = asn_note_addr(session, scope)
        if note_addr is None:
            return
        claim_addrs = {
            link.to_set[0]
            for link in session.active_links("claim")
            if link.to_set
        }
        for derived_addr in derived_claims(session, note_addr):
            if derived_addr in claim_addrs:
                yield derived_addr
        return

    for link in session.active_links("claim"):
        if link.to_set:
            yield link.to_set[0]


claim_structural_audit = Trigger(
    name="claim-structural-audit",
    scope_query=_scope_query,
    predicate=is_claim_audit_fresh,
    agent=ClaimStructuralAuditAgent(),
)
