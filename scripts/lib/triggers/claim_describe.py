"""Claim-describe trigger — fires on claims whose description is stale.

  scope:     each claim derived from the requested ASN's source note
  predicate: description_is_fresh
  agent:     ClaimDescribeAgent
"""

from __future__ import annotations

from typing import Iterator

from lib.agents.claim_describe import ClaimDescribeAgent
from lib.backend.addressing import Address
from lib.predicates import derived_claims, description_is_fresh
from lib.protocols.febe.protocol import Session
from lib.runner import Scope, Trigger, asn_note_addr


def _scope_query(session: Session, scope: Scope) -> Iterator[Address]:
    """Yield each claim-classified derivation of the ASN's source note.

    Filters out non-claim derivations (e.g., the claim-statements
    view doc) so the agent only describes actual claims.
    """
    note_addr = asn_note_addr(session, scope)
    if note_addr is None:
        return
    # One classifier scan, then set-membership per derivation.
    claim_addrs = {
        link.to_set[0]
        for link in session.active_links("claim")
        if link.to_set
    }
    for derived_addr in derived_claims(session, note_addr):
        if derived_addr in claim_addrs:
            yield derived_addr


claim_describe = Trigger(
    name="claim-describe",
    scope_query=_scope_query,
    predicate=description_is_fresh,
    agent=ClaimDescribeAgent(),
)
