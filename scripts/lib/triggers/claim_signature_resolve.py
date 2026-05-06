"""Claim-signature-resolve trigger — fires per claim with stale signature sidecar.

  scope:     each claim derived from the requested ASN's source note
             (CLI mode), or every active claim (daemon mode)
  predicate: signature_is_fresh (skip if the sidecar's supersession
             chain is at least as long as the claim's chain)
  agent:     ClaimSignatureResolveAgent

Per-claim granularity. Predicate is the standard chain-length
comparison shared with description_is_fresh / statements_is_fresh:
each claim md edit advances the claim chain; emit_attribute advances
the sidecar chain; equal lengths mean "every edit attested." Lower
sidecar count means at least one edit is unattested → fire.
"""

from __future__ import annotations

from typing import Iterator

from lib.agents.producers.claim_signature_resolve import (
    ClaimSignatureResolveAgent,
)
from lib.backend.addressing import Address
from lib.predicates import derived_claims, signature_is_fresh
from lib.protocols.febe.protocol import Session
from lib.runner import Scope, Trigger, asn_note_addr


def _scope_query(session: Session, scope: Scope) -> Iterator[Address]:
    """Yield each claim-classified derivation of the ASN's source note.

    Mirrors claim-describe / claim-revise / claim-structural-revise
    scope shapes: walk derived_claims, filter to claim-classified
    addresses.
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


claim_signature_resolve = Trigger(
    name="claim-signature-resolve",
    scope_query=_scope_query,
    predicate=signature_is_fresh,
    agent=ClaimSignatureResolveAgent(),
)
