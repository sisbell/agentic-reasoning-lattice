"""Full-review trigger — fires when the ASN is quiescent but not confirmed.

The reviewer holds at quiescence: it doesn't re-fire while open
`comment.revise` links pend, even if they pre-date the most recent
review. Open revises are the runner's job (claim_revise refiner);
the reviewer fires only after they close, on a state that's stable
but not yet covered by a fresh review.

  scope:     the source note for the requested ASN
  predicate: is_asn_confirmed OR not is_asn_quiescent
             (skip if confirmed, or if revises are still pending)
  agent:     FullReviewAgent

The `not is_asn_quiescent` clause is what produces the
review→revise→review alternation under the predicate-fired model
without any agent-to-agent coordination — the reviewer reads
substrate state, finds open revises, and waits.
"""

from __future__ import annotations

from typing import Iterator

from lib.agents.producers.full_review import FullReviewAgent
from lib.backend.addressing import Address
from lib.predicates import is_asn_confirmed, is_asn_quiescent
from lib.protocols.febe.protocol import Session
from lib.runner import Scope, Trigger, asn_note_addr


def _scope_query(session: Session, scope: Scope) -> Iterator[Address]:
    """Yield the source note address for the requested ASN, if any."""
    addr = asn_note_addr(session, scope)
    if addr is not None:
        yield addr


def _predicate(session: Session, addr: Address) -> bool:
    """True (skip) iff already confirmed, or open revises are pending."""
    return (
        is_asn_confirmed(session, addr)
        or not is_asn_quiescent(session, addr)
    )


full_review = Trigger(
    name="full-review",
    scope_query=_scope_query,
    predicate=_predicate,
    agent=FullReviewAgent(),
)
