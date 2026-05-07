"""Claim-formal-contract trigger — fires per claim missing Formal Contract.

  scope:     each claim-classified derivation of the ASN's source note
             (CLI), or every claim (daemon)
  predicate: claim_formal_contract_is_fresh (skip if the kind doesn't
             need a Formal Contract section, or if the section is
             already present)
  agent:     ClaimFormalContractAgent
"""

from __future__ import annotations

from lib.agents.producers.claim_formal_contract import (
    ClaimFormalContractAgent,
)
from lib.predicates import claim_formal_contract_is_fresh
from lib.runner import Trigger
from lib.triggers.scope import per_claim_of_asn


claim_formal_contract = Trigger(
    name="claim-formal-contract",
    scope_query=per_claim_of_asn,
    predicate=claim_formal_contract_is_fresh,
    agent=ClaimFormalContractAgent(),
)
