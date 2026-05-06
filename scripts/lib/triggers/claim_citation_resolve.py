"""Claim-citation-resolve trigger — fires per claim with stale references sidecar.

  scope:     each claim derived from the requested ASN's source note
             (CLI mode), or every active claim (daemon mode)
  predicate: references_is_fresh (skip if the sidecar's supersession
             chain is at least as long as the claim's chain)
  agent:     ClaimCitationResolveAgent

Per-claim granularity. Predicate is the standard chain-length
comparison shared with signature_is_fresh / description_is_fresh /
statements_is_fresh: each claim md edit advances the claim chain;
attest_attribute advances the sidecar chain on each fire; equal
lengths mean "every edit attested." Lower sidecar count means at
least one edit is unattested → fire.
"""

from __future__ import annotations

from typing import Iterator

from lib.agents.producers.citation_resolve import ClaimCitationResolveAgent
from lib.backend.addressing import Address
from lib.predicates import derived_claims, references_is_fresh
from lib.protocols.febe.protocol import Session
from lib.runner import Scope, Trigger, asn_note_addr


def _scope_query(session: Session, scope: Scope) -> Iterator[Address]:
    """Yield each claim-classified derivation of the ASN's source note.

    Mirrors claim-describe / claim-signature-resolve scope shapes:
    walk derived_claims, filter to claim-classified addresses.
    """
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


claim_citation_resolve = Trigger(
    name="claim-citation-resolve",
    scope_query=_scope_query,
    predicate=references_is_fresh,
    agent=ClaimCitationResolveAgent(),
)
