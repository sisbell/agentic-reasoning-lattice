"""Convergence-protocol predicates over the substrate.

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

import re
from typing import List, Optional

from lib.backend.addressing import Address
from lib.backend.links import Link
from lib.protocols.febe.protocol import Session


def has_resolution(session: Session, comment_addr: Address) -> bool:
    """True iff at least one active `resolution` link targets this comment.

    Substrate convention (matches legacy and migrated data): the
    resolution link has `from_set=[revised_doc]`, `to_set=[comment_addr]`.
    """
    return bool(session.active_links("resolution", to_set=[comment_addr]))


def unresolved_revise_comments(
    session: Session,
    doc_addr: Optional[Address] = None,
) -> List[Link]:
    """Every active `comment.revise` link without an active resolution.

    Retracted revises are excluded (the retraction nullifies the
    complaint). A resolution that has itself been retracted does not
    satisfy the predicate. If `doc_addr` is given, scopes to comments
    targeting that doc; otherwise spans the whole substrate.

    This is the load-bearing predicate for the convergence model —
    every "is the lattice done?" question reduces to this set being
    empty over the appropriate scope.
    """
    revises = session.active_links(
        "comment.revise",
        to_set=[doc_addr] if doc_addr is not None else None,
    )
    return [c for c in revises if not has_resolution(session, c.addr)]


def is_doc_converged(session: Session, doc_addr: Address) -> bool:
    """The protocol predicate, restricted to one document."""
    return not unresolved_revise_comments(session, doc_addr)


# Doc-neutral alias matching the legacy queries.py pattern.
is_claim_converged = is_doc_converged


def is_converged(session: Session) -> bool:
    """The protocol predicate at lattice scope.

    Vacuously true on an empty graph — coverage (have reviews actually
    happened?) is choreography's responsibility, not the predicate's.
    """
    return not unresolved_revise_comments(session)


def latest_review_for_addr(
    session: Session, addr: Address,
) -> Optional[Address]:
    """Return the review_meta of the most recent review whose
    `review.coverage` link covers `addr`, or None if none exist.

    "Most recent" is the `review.coverage` link with the largest
    tumbler address (links are allocated monotonically, so the
    largest-addressed active link is the latest emission).
    """
    coverage_links = [
        link for link in session.active_links(
            "review.coverage", to_set=[addr],
        )
        if link.from_set
    ]
    if not coverage_links:
        return None
    latest = max(coverage_links, key=lambda link: link.addr.digits)
    return latest.from_set[0]


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
    converged AND the most recent review on its scope was clean.

    Per `docs/hypergraph-protocol/convergence.md`: a clean review IS
    the confirmation. The orchestrator's "+1 review-only after N
    cycles" collapses into "the next cycle that comes up clean."
    """
    return (
        is_claim_converged(session, addr)
        and has_been_reviewed(session, addr)
        and latest_review_was_clean(session, addr)
    )


def is_asn_converged(session: Session, asn_label: str) -> bool:
    """Conjunction of `is_doc_converged` over every claim md under an ASN.

    Identifies an ASN's claim docs by walking the active `claim`
    classifier links and filtering by path pattern. Vacuously true on
    an ASN with no matching claims — coverage is choreography's
    responsibility.
    """
    asn_path_pattern = re.compile(
        rf"_docuverse/documents/claim/{re.escape(asn_label)}/[^/]+\.md$"
    )
    from lib.backend.schema import ATTRIBUTE_SUFFIXES
    for link in session.active_links("claim"):
        for claim_addr in link.to_set:
            path = session.get_path_for_addr(claim_addr)
            if path is None:
                continue
            if not asn_path_pattern.search(path):
                continue
            if path.endswith(ATTRIBUTE_SUFFIXES):
                continue
            if "/_" in path:
                continue
            if not is_doc_converged(session, claim_addr):
                return False
    return True
