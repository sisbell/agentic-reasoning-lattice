"""Claim-formal-contract trigger — fires per claim missing Formal Contract.

  scope:     each claim derived from the requested ASN's source note
             (CLI mode), or every active claim (daemon mode)
  predicate: claim_formal_contract_is_fresh (skip if no contract.<kind>
             yet, or kind is definition/axiom/design-requirement, or
             claim md already has the *Formal Contract:* section)
  agent:     ClaimFormalContractAgent

Per-claim granularity. Once-and-done — the predicate is existence-only
on the section marker. Subsequent body edits don't re-fire (drift
caught by the structural validator if applicable).

Naturally orders after `claim_contract`: the predicate skips while
no contract.<kind> exists, so produce-contract waits for type
classification before firing.
"""

from __future__ import annotations

from typing import Iterator

from lib.agents.producers.claim_formal_contract import (
    ClaimFormalContractAgent,
)
from lib.backend.addressing import Address
from lib.predicates import claim_formal_contract_is_fresh, derived_claims
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


claim_formal_contract = Trigger(
    name="claim-formal-contract",
    scope_query=_scope_query,
    predicate=claim_formal_contract_is_fresh,
    agent=ClaimFormalContractAgent(),
)
