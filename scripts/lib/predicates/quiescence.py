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

    This is the load-bearing predicate for the quiescence model —
    every "is the lattice done?" question reduces to this set being
    empty over the appropriate scope.
    """
    revises = session.active_links(
        "comment.revise",
        to_set=[doc_addr] if doc_addr is not None else None,
    )
    return [c for c in revises if not has_resolution(session, c.addr)]


def is_doc_quiescent(session: Session, doc_addr: Address) -> bool:
    """The protocol predicate, restricted to one document."""
    return not unresolved_revise_comments(session, doc_addr)


# Doc-neutral alias matching the legacy queries.py pattern.
is_claim_quiescent = is_doc_quiescent


def is_claim_structurally_clean(
    session: Session, claim_addr: Address,
) -> bool:
    """True iff the structural validator finds no actionable violations
    on the claim's directory that target this claim.

    Runs the validator (no LLM, just static analysis) and filters
    findings to those whose `file` stem matches the claim label.
    Used as the skip predicate for the claim-structural-fix trigger.

    Cycle findings (acyclic-depends; propose-only and retired) are
    excluded — they don't make the claim "dirty" under the lifted
    fix-mode contract.

    Defined here rather than in classifiers.py because the predicate
    runs the validator (an external module) rather than reading
    substrate. Keep close to other claim-state predicates so callers
    looking for "claim X clean?" find both quiescence and structural.
    """
    import importlib.util
    import re as _re
    from pathlib import Path
    from lib.shared.paths import CLAIM_DIR, WORKSPACE

    claim_rel = session.get_path_for_addr(claim_addr)
    if claim_rel is None:
        return True
    m = _re.search(r"(ASN-\d{4})/([^/]+)\.md$", claim_rel)
    if m is None:
        return True
    asn_label = m.group(1)
    claim_label = m.group(2)
    claim_dir = CLAIM_DIR / asn_label
    if not claim_dir.exists():
        return True

    spec = importlib.util.spec_from_file_location(
        "claim_validate", WORKSPACE / "scripts" / "claim-validate.py",
    )
    validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validator)
    pairs = validator.load_pairs(claim_dir)
    findings = validator.run_all_checks(pairs, claim_dir=claim_dir)

    for f in findings:
        if f["rule"] == "acyclic-depends":
            continue
        filename = f.get("file")
        if filename and Path(filename).stem == claim_label:
            return False
        if not filename and claim_label in f.get("detail", ""):
            return False
    return True


def is_quiescent(session: Session) -> bool:
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
