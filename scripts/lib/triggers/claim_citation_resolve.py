"""Claim-citation-resolve trigger — fires per claim with stale references sidecar.

  scope:     each claim-classified derivation of the ASN's source note
             (CLI), or every claim (daemon)
  predicate: references_is_fresh
  agent:     ClaimCitationResolveAgent
"""

from __future__ import annotations

from lib.agents.producers.citation_resolve import ClaimCitationResolveAgent
from lib.predicates import references_is_fresh
from lib.runner import Trigger
from lib.triggers._commit_paths import per_claim_commit_paths
from lib.triggers.scope import per_claim_of_asn


claim_citation_resolve = Trigger(
    name="claim-citation-resolve",
    scope_query=per_claim_of_asn,
    predicate=references_is_fresh,
    agent=ClaimCitationResolveAgent(),
    supports_claim_filter=True,
    commit_paths=per_claim_commit_paths,
)
