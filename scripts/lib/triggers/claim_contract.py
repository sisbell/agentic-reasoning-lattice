"""Claim-contract trigger — fires per claim missing a contract.<kind>.

  scope:     each claim derived from the requested ASN's source note
             (CLI mode), or every active claim (daemon mode)
  predicate: has_contract_kind (skip if any contract.<kind> classifier
             already targets the claim)
  agent:     ClaimContractAgent

Per-claim granularity. Once-and-done — the predicate is a one-shot
existence check. Subsequent claim edits do not re-fire (contract
kind is structural metadata, rarely changes after initial
classification). If a re-classification is needed, retract the
existing contract.<kind> link first; the predicate flips False and
the agent fires again.
"""

from __future__ import annotations

from typing import Iterator

from lib.agents.producers.claim_contract import ClaimContractAgent
from lib.backend.addressing import Address
from lib.predicates import derived_claims, has_contract_kind
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


claim_contract = Trigger(
    name="claim-contract",
    scope_query=_scope_query,
    predicate=has_contract_kind,
    agent=ClaimContractAgent(),
)
