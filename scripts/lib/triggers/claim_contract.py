"""Claim-contract trigger — fires per claim missing a contract.<kind>.

  scope:     each claim-classified derivation of the ASN's source note
             (CLI), or every claim (daemon)
  predicate: has_contract_kind (skip if any contract.<kind> classifier
             already targets the claim — once-and-done)
  agent:     ClaimContractAgent
"""

from __future__ import annotations

from lib.agents.producers.claim_contract import ClaimContractAgent
from lib.predicates import has_contract_kind
from lib.runner import Trigger
from lib.triggers.scope import per_claim_of_asn


claim_contract = Trigger(
    name="claim-contract",
    scope_query=per_claim_of_asn,
    predicate=has_contract_kind,
    agent=ClaimContractAgent(),
)
