"""Quiescence predicates implementing the convergence protocol.

The convergence protocol's load-bearing definition (per
`docs/protocols/claim-convergence-protocol.md`):

    For every document with a `claim` classifier, every active
    `comment.revise` link targeting that claim has a matching active
    `resolution` link.

A link is *active* if no `retraction` link nullifies it. Retracted
revises drop out of the predicate; retracted resolutions stop
satisfying it.

These predicates know what specific link types *mean* in the
convergence protocol — `comment.revise`, `resolution`, the
revise-resolution pairing — so they're protocol code, not substrate
primitive.

Per Pass 1.5's binding discipline: predicates take a Session (not a
State or Store directly), and compose Session methods rather than
reaching into substrate internals. Callers hold a Session and pass it
through.
"""

from __future__ import annotations

from typing import Optional

from lib.backend.addressing import Address
from lib.protocols.febe.protocol import Session

from .factory import (
    all_resolved, latest_via_coverage, unresolved_comments_of_kind,
)


def has_resolution(session: Session, comment_addr: Address) -> bool:
    """True iff at least one active `resolution` link targets this comment.

    Substrate convention (matches legacy and migrated data): the
    resolution link has `from_set=[revised_doc]`, `to_set=[comment_addr]`.
    """
    return bool(session.active_links("resolution", to_set=[comment_addr]))


unresolved_revise_comments = unresolved_comments_of_kind("comment.revise")
is_doc_quiescent = all_resolved("comment.revise")
# Doc-neutral alias matching the legacy queries.py pattern.
is_claim_quiescent = is_doc_quiescent

latest_structural_audit_for_claim = latest_via_coverage(
    "review.coverage", "review.structural",
)


def is_claim_audit_fresh(
    session: Session, claim_addr: Address,
) -> bool:
    """Skip predicate for the claim-structural-audit scout.

    Mirrors `is_claim_confirmed`'s closure-style freshness: the audit
    is fresh iff the latest structural audit covering this claim was
    clean (zero `comment.violation` findings derived from it) OR its
    findings are still in flight (some unresolved → refiner is still
    working). The scout re-fires only when the latest audit's
    findings have all closed and the post-fix state needs re-audit.

    Returns True (skip) iff:
      - The latest structural audit covering this claim found zero
        violations (clean), OR
      - The latest audit's violations include at least one unresolved
        comment.violation (refiner is still closing them).

    Returns False (fire scout) iff:
      - No structural audit has covered this claim yet, OR
      - The latest audit's violations have all been resolved
        (need to re-audit on post-fix state).
    """
    latest_audit = latest_structural_audit_for_claim(session, claim_addr)
    if latest_audit is None:
        return False

    finding_addrs = {
        target
        for link in session.active_links(
            "provenance.derivation", from_set=[latest_audit],
        )
        for target in link.to_set
    }
    if not finding_addrs:
        return True  # Clean audit — quiescence

    for finding in finding_addrs:
        for violation in session.active_links(
            "comment.violation", from_set=[finding],
        ):
            if not has_resolution(session, violation.addr):
                return True  # Refiner still working
    return False  # All resolved → re-audit


is_claim_structurally_clean = all_resolved("comment.violation")


def is_quiescent(session: Session) -> bool:
    """The protocol predicate at lattice scope.

    Vacuously true on an empty graph — coverage (have reviews actually
    happened?) is choreography's responsibility, not the predicate's.
    """
    return not unresolved_revise_comments(session)


latest_review_for_addr = latest_via_coverage(
    "review.coverage", "review.content",
)


def has_been_reviewed(session: Session, addr: Address) -> bool:
    """True iff some review covered `addr`. Used to distinguish
    'never reviewed' from 'reviewed clean' in confirmation logic.
    """
    return latest_review_for_addr(session, addr) is not None


def latest_review_was_clean(session: Session, addr: Address) -> bool:
    """True iff the most recent review on `addr`'s scope filed zero
    `comment.revise` findings (none of its derived findings own a
    comment.revise link).

    Returns False when no review has covered `addr`.
    """
    review_meta = latest_review_for_addr(session, addr)
    if review_meta is None:
        return False
    finding_addrs = {
        target
        for link in session.active_links(
            "provenance.derivation", from_set=[review_meta],
        )
        for target in link.to_set
    }
    for finding in finding_addrs:
        if session.active_links("comment.revise", from_set=[finding]):
            return False
    return True


def is_claim_confirmed(session: Session, addr: Address) -> bool:
    """The convergence-protocol's confirmation condition: claim is
    quiescent AND the most recent review on its scope was clean.

    Per `docs/hypergraph-protocol/convergence.md`: a clean review IS
    the confirmation. The orchestrator's "+1 review-only after N
    cycles" collapses into "the next cycle that comes up clean."
    """
    return (
        is_claim_quiescent(session, addr)
        and has_been_reviewed(session, addr)
        and latest_review_was_clean(session, addr)
    )


def derived_claims(session: Session, note_addr: Address):
    """Yield substrate addresses of claims derived from a source note.

    Walks `provenance.derivation` forward from the note address.
    Emitted by transclude during claim derivation; the union of these
    targets is the note's claim cluster.
    """
    for link in session.active_links(
        "provenance.derivation", from_set=[note_addr],
    ):
        for derived in link.to_set:
            yield derived


def is_asn_quiescent(session: Session, note_addr: Address) -> bool:
    """Conjunction of `is_claim_quiescent` over every derived claim."""
    return all(
        is_doc_quiescent(session, derived)
        for derived in derived_claims(session, note_addr)
    )


def is_asn_confirmed(session: Session, note_addr: Address) -> bool:
    """Conjunction of `is_claim_confirmed` over every derived claim.

    ASN-level analog of `is_claim_confirmed`: each derived claim has
    quiescent AND its most recent review was clean. Used as the
    full-review trigger's quiescence predicate — mirrors how cone-review
    uses `is_claim_confirmed`.
    """
    return all(
        is_claim_confirmed(session, derived)
        for derived in derived_claims(session, note_addr)
    )
