"""Full-review trigger — fires when the ASN is quiescent but not confirmed.

The reviewer holds at quiescence: it doesn't re-fire while open
`comment.revise` links pend, even if they pre-date the most recent
review. Open revises are the runner's job (claim_revise refiner);
the reviewer fires only after they close, on a state that's stable
but not yet covered by a fresh review.

  scope:     the source note for the requested ASN
  predicate: skip if confirmed, or revises pending, or any derived
             claim is still missing its Formal Contract section
  agent:     FullReviewAgent

The `not is_asn_quiescent` clause produces the review→revise→review
alternation under the predicate-fired model without any agent-to-
agent coordination — the reviewer reads substrate state, finds open
revises, and waits.

The Formal Contract gate keeps the reviewer from firing on a freshly-
decomposed ASN where claims exist but `claim_formal_contract` hasn't
landed yet — without Formal Contract sections there's nothing
substantive to review.
"""

from __future__ import annotations

from lib.agents.producers.full_review import FullReviewAgent
from lib.backend.addressing import Address
from lib.predicates import (
    derived_claims, has_formal_contract,
    is_asn_confirmed, is_asn_quiescent, is_held,
)
from lib.protocols.febe.protocol import Session
from lib.runner import Trigger
from lib.triggers.scope import per_asn_note


def _predicate(session: Session, addr: Address) -> bool:
    """True (skip) iff already confirmed, revises pending, the note is
    held by another agent (mutex with cone-review), or any derived
    claim is missing its Formal Contract section."""
    if is_asn_confirmed(session, addr):
        return True
    if not is_asn_quiescent(session, addr):
        return True
    if is_held(session, addr):
        return True
    classified_claims = {
        link.to_set[0]
        for link in session.active_links("claim")
        if link.to_set
    }
    for claim in derived_claims(session, addr):
        if claim not in classified_claims:
            continue
        if not has_formal_contract(session, claim):
            return True
    return False


full_review = Trigger(
    name="full-review",
    scope_query=per_asn_note,
    predicate=_predicate,
    agent=FullReviewAgent(),
)
