"""Claim-describe trigger — fires on claims whose description is stale.

  scope:     each claim-classified derivation of the ASN's source note
             (CLI), or every claim (daemon)
  predicate: description_is_fresh
  agent:     ClaimDescribeAgent
"""

from __future__ import annotations

from lib.agents.producers.claim_describe import ClaimDescribeAgent
from lib.predicates import description_is_fresh
from lib.runner import Trigger
from lib.triggers._commit_paths import per_claim_commit_paths
from lib.triggers.scope import per_claim_of_asn


claim_describe = Trigger(
    name="claim-describe",
    scope_query=per_claim_of_asn,
    predicate=description_is_fresh,
    agent=ClaimDescribeAgent(),
    supports_claim_filter=True,
    commit_paths=per_claim_commit_paths,
)
