"""Claim-signature-resolve trigger — fires per claim with stale signature sidecar.

  scope:     each claim-classified derivation of the ASN's source note
             (CLI), or every claim (daemon)
  predicate: signature_is_fresh (skip if the sidecar's supersession
             chain is at least as long as the claim's chain)
  agent:     ClaimSignatureResolveAgent

Per-claim granularity. Predicate is the standard chain-length
comparison shared with description_is_fresh / statements_is_fresh:
each claim md edit advances the claim chain; attest_attribute
advances the sidecar chain on each fire; equal lengths mean "every
edit attested." Lower sidecar count means at least one edit is
unattested → fire.
"""

from __future__ import annotations

from lib.agents.producers.claim_signature_resolve import (
    ClaimSignatureResolveAgent,
)
from lib.predicates import signature_is_fresh
from lib.runner import Trigger
from lib.triggers.scope import per_claim_of_asn


claim_signature_resolve = Trigger(
    name="claim-signature-resolve",
    scope_query=per_claim_of_asn,
    predicate=signature_is_fresh,
    agent=ClaimSignatureResolveAgent(),
    supports_claim_filter=True,
)
