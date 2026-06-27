"""Full-review trigger — fires when the ASN is quiescent but not confirmed.

The reviewer holds at quiescence: it doesn't re-fire while open
`comment.revise` links pend, even if they pre-date the most recent
review. Open revises are the runner's job (claim_revise refiner);
the reviewer fires only after they close, on a state that's stable
but not yet covered by a fresh review.

  scope:     one canonical claim of the ASN (first by tumbler) —
             the agent multi-holds every classified claim, so the
             initial address just needs to anchor the fire.
  predicate: skip if confirmed, revises pending, any derived claim
             is held by another agent (mutex with cone-review), or
             any derived claim still missing its Formal Contract.
  agent:     FullReviewAgent

The `not is_asn_quiescent` clause produces the review→revise→review
alternation under the predicate-fired model without any agent-to-
agent coordination — the reviewer reads substrate state, finds open
revises, and waits.

Mutex with cone-review is enforced through per-claim holds: full-review
holds every classified claim of the ASN, so a concurrent cone-review's
apex hold (or the predicate-check it does before firing) will collide.

The Formal Contract gate keeps the reviewer from firing on a freshly-
decomposed ASN where claims exist but `claim_formal_contract` hasn't
landed yet — without Formal Contract sections there's nothing
substantive to review.
"""

from __future__ import annotations

from lib.agents.producers.full_review import FullReviewAgent
from lib.backend.addressing import Address
from lib.predicates import (
    asn_claim_addrs, asn_label_for_claim, has_formal_contract,
    is_asn_confirmed, is_asn_quiescent, is_held,
)
from lib.protocols.febe.protocol import Session
from lib.runner import Trigger
from lib.triggers.scope import asn_first_claim


def _predicate(session: Session, addr: Address) -> bool:
    """True (skip) iff already confirmed, revises pending, any claim
    of the ASN is held by another agent, or any claim that REQUIRES a
    Formal Contract is still missing it.

    The Formal Contract gate waits for `claim_formal_contract` to land
    before the first whole-ASN review. But only theorem/lemma/corollary
    claims get a Formal Contract — axiom/definition/design-requirement
    claims never do (KINDS_REQUIRING_CONTRACT). The gate must therefore
    check the kind first; otherwise a single definition claim (which is
    permanently FC-less) blocks full-review forever, leaving every
    non-apex claim of the ASN unreviewed (cone-review covers only apex
    cones)."""
    from lib.agents.producers.claim_formal_contract import (
        KINDS_REQUIRING_CONTRACT,
    )
    from lib.predicates import current_contract_kind

    # ASN identity is PATH-derived from the claim addr — the note is never
    # consulted post-derivation. Claims are enumerated from the claim region
    # (asn_claim_addrs), so claims that refinement created (which carry no
    # note provenance) are included; a note-anchored walk would miss them
    # and confirm prematurely.
    asn_label = asn_label_for_claim(session, addr)
    if asn_label is None:
        return True
    if is_asn_confirmed(session, asn_label):
        return True
    if not is_asn_quiescent(session, asn_label):
        return True
    for claim in asn_claim_addrs(session, asn_label):
        if is_held(session, claim):
            return True
        # FC gate: a claim blocks the whole-ASN review only if it lacks a
        # Formal Contract AND it is not an FC-exempt kind. Theorem/lemma/
        # corollary need an FC (wait for claim_formal_contract); an
        # unclassified claim (kind=None) is mid-construction (claim_contract
        # runs first) and also waits. Axiom/definition/design-requirement
        # never get an FC, so a missing FC there is the permanent correct
        # state and must NOT block — otherwise one definition claim wedges
        # full-review forever, leaving every non-apex claim unreviewed.
        kind = current_contract_kind(session, claim)
        fc_exempt = kind is not None and kind not in KINDS_REQUIRING_CONTRACT
        if not fc_exempt and not has_formal_contract(session, claim):
            return True
    return False


from lib.triggers._commit_paths import per_asn_claim_review_paths


full_review = Trigger(
    name="full-review",
    scope_query=asn_first_claim,
    predicate=_predicate,
    agent=FullReviewAgent(),
    commit_paths=per_asn_claim_review_paths,
)
