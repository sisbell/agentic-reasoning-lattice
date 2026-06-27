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


def _safe_path_for_addr(session: Session, addr: Address) -> Optional[str]:
    """Best-effort lattice-relative path for `addr`, or None.

    In-memory (State-only) sessions raise NotImplementedError because they
    have no filesystem path map; an unregistered addr raises KeyError.
    Either way, there's no cone-claims path to recognize, so the cone
    distinguisher falls back to "not a cone review." Used by the
    exclude_cone path check; mirrors the defensive resolution the old
    `manages`-based gate used for get_addr_for_path.
    """
    try:
        return session.get_path_for_addr(addr)
    except (NotImplementedError, KeyError, AttributeError):
        return None


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


def _review_filed_revise(session: Session, review_addr: Address) -> bool:
    """True iff `review_addr` originally emitted any `comment.revise`
    findings — including comment.revise links that have since been
    retracted (e.g., by note_revise closing them).

    Stochastic-quiescence cleanness is about the reviewer's emit-time
    verdict, not the current resolution state. A review with 5 REVISE
    findings does not become "clean" because those findings were later
    addressed — it's still a non-CONVERGED draw, and n-consecutive-clean
    must require a fresh CONVERGED draw on top.

    Walks find_links (including retracted) on each finding doc derived
    from the review.
    """
    state = session._state
    finding_addrs = {
        target
        for link in session.active_links(
            "provenance.derivation", from_set=[review_addr],
        )
        for target in link.to_set
    }
    for finding in finding_addrs:
        if state.find_links(from_set=[finding], type_="comment.revise"):
            return True
    return False


def latest_review_was_clean(session: Session, addr: Address) -> bool:
    """True iff the most recent review on `addr`'s scope filed zero
    `comment.revise` findings at emit time (retracted findings still
    count — see `_review_filed_revise`).

    Returns False when no review has covered `addr`.
    """
    review_meta = latest_review_for_addr(session, addr)
    if review_meta is None:
        return False
    return not _review_filed_revise(session, review_meta)


def last_n_reviews_were_clean(
    session: Session, addr: Address, n: int, *, exclude_cone: bool = False,
) -> bool:
    """True iff the most recent N reviews on `addr`'s scope all filed
    zero `comment.revise` findings.

    Generalizes `latest_review_was_clean` (n=1 case). Used by triggers
    that gate on multi-draw evidence for stochastic reviewers — single
    CONVERGED is statistically unstable, two-consecutive is the empirical
    note-scope gate. See `docs/design-notes/stochastic-quiescence.md`.

    `exclude_cone`: skip cone reviews — `review.coverage` whose review doc
    lives under `review/cone-claims/` (`is_cone_review_path`). The
    claim/global confirmation gate (`is_claim_confirmed`) sets this so it
    counts WHOLE-ASN full reviews only — the cone phase has its own n=2
    stream (`_clean_cone_review_streak`). Counting cone reviews here too
    couples the phases: a cone-phase REVISE would linger in this gate and
    re-open `is_asn_confirmed`, re-firing the global phase next outer
    pass. The distinguisher is the review-doc PATH (set at emit time), not
    `manages` attribution — the in-process claim runner never emits that
    tag, so the old exclusion was a silent no-op. Notes never live under
    cone-claims, so the default (False) leaves the note path — and the
    generic attribute gates in factory.py — unchanged.

    Returns False when fewer than N reviews have covered `addr`.
    n <= 0 is vacuously True.
    """
    if n <= 0:
        return True
    from lib.shared.paths import is_cone_review_path
    coverage_links = []
    for link in session.active_links("review.coverage", to_set=[addr]):
        if not link.from_set:
            continue
        if not session.active_links(
            "review.content", to_set=[link.from_set[0]],
        ):
            continue
        if exclude_cone and is_cone_review_path(
            _safe_path_for_addr(session, link.from_set[0]),
        ):
            continue  # cone review → counted by the cone gate, not here
        coverage_links.append(link)
    if len(coverage_links) < n:
        return False
    coverage_links.sort(key=lambda link: link.addr.digits)
    for cov_link in coverage_links[-n:]:
        if _review_filed_revise(session, cov_link.from_set[0]):
            return False
    return True


def is_confirmed_n(
    session: Session, addr: Address, n: int, *, exclude_cone: bool = False,
) -> bool:
    """Generalized confirmation: quiescent AND the most recent N
    reviews on its scope were all clean. Convergence-protocol gate
    with operator-tunable stochastic-quiescence depth.

    n=1 = "most recent review clean" (claim default).
    n=2 = "last two consecutive reviews clean" (note default; see
    stochastic-quiescence.md).

    `exclude_cone` (threaded to `last_n_reviews_were_clean`): count
    whole-ASN full reviews only, excluding the per-apex cone stream.
    `is_claim_confirmed` sets it so the global gate and the cone gate
    stay independent; factory.py's generic attribute gates keep the
    default (mixed) — they have no cone tier to separate.

    The final clause is `is_claim_cascade_fresh`: the latest review's
    foundation cascade-anchor must still point at head versions. This
    replaces the re-anchor-fooled `revised_after_latest_review` — the
    review-anchored signal can't be masked by re-running
    sync_claim_citations on the mutable claim head. Imported lazily to
    avoid the cascade↔quiescence import cycle (cascade imports from
    this module).
    """
    from lib.predicates.cascade import is_claim_cascade_fresh
    return (
        is_claim_quiescent(session, addr)
        and has_been_reviewed(session, addr)
        and last_n_reviews_were_clean(
            session, addr, n=n, exclude_cone=exclude_cone,
        )
        and is_claim_cascade_fresh(session, addr)
    )


CLAIM_CONFIRMATION_N = 2


def is_claim_confirmed(session: Session, addr: Address) -> bool:
    """Claim-side confirmation (n=2): quiescent AND the most recent TWO
    reviews on its scope were both clean, AND no revise landed after the
    latest review.

    Two-consecutive, not one: the claim reviewer is the same stochastic
    Opus/Sonnet as the note reviewer, so a single clean draw is just as
    unstable for a claim as for a note (see
    `docs/design-notes/stochastic-quiescence.md`). A lone CONVERGED can
    be a lucky draw; requiring two consecutive clean reviews is the
    empirical floor. Previously n=1 ("a clean review IS the
    confirmation"), which let a single fluke-clean review confirm a
    claim — raised to n=2 to match the note-side gate.

    `exclude_cone=True`: the global/full gate counts whole-ASN full
    reviews only; per-apex cone reviews converge on their own n=2 stream
    (`_clean_cone_review_streak`). This keeps the two phases independent
    so cone-phase REVISEs don't re-open `is_asn_confirmed`.
    """
    return is_confirmed_n(
        session, addr, n=CLAIM_CONFIRMATION_N, exclude_cone=True,
    )


def derived_claims(session: Session, note_addr: Address):
    """Yield substrate addresses of claims derived from a source note.

    Walks `provenance.derivation` forward from the note address.
    Emitted by transclude during claim derivation; the union of these
    targets is the note's claim cluster.

    NOTE: this is a DERIVATION-TIME view. It only sees claims the note
    transcluded; claims that claim-refinement created later (which carry
    no note→claim provenance — refinement never writes back to the note)
    are invisible to it. The refinement/convergence layer must enumerate
    via `asn_claim_addrs` instead, or it confirms prematurely over an
    incomplete set. The note is a derivation-time source only; once
    derived it is never read again.
    """
    for link in session.active_links(
        "provenance.derivation", from_set=[note_addr],
    ):
        for derived in link.to_set:
            yield derived


def asn_claim_addrs(session: Session, asn_label: str):
    """Yield substrate addresses of every claim in an ASN's claim region.

    Region-based enumeration: reads the claim region (1.3) via the
    ASN-scoped label index — the set of claim docs that physically exist
    for the ASN — NOT the note's `provenance.derivation` links. This is
    the post-derivation replacement for `derived_claims`: claim
    refinement may legitimately mint new claims (a definition or lemma a
    reviewer found missing), and those carry no note provenance, so a
    note walk misses them and reports false convergence. Keying off the
    region also means a refinement-created claim is seen even though only
    `claim_decompose` emits the `claim` classifier (refinement-minted
    claims lack it).

    The scoped index returns one address per claim label; it indexes
    claim main docs only (sidecars and the `_statements` aggregate are
    not labelled claim docs), so the values are exactly the ASN's claims.
    """
    from lib.lattice.labels import build_cross_asn_label_index
    index = build_cross_asn_label_index(
        session.store, allowed_asns={asn_label},
    )
    yield from index.values()


def asn_label_for_claim(
    session: Session, addr: Address,
) -> Optional[str]:
    """Derive the ASN label (e.g. 'ASN-0036') from a claim addr's path.

    Path-derived so it works for refinement-created claims that have no
    note provenance to reverse-walk. Returns None if the address has no
    parseable claim-doc path. This is how the refinement layer answers
    "which ASN does this claim belong to?" without touching the note.
    """
    from lib.lattice.labels import parse_claim_doc_path
    path = _safe_path_for_addr(session, addr)
    if path is None:
        return None
    parsed = parse_claim_doc_path(path)
    if parsed is None:
        return None
    asn_label, _basename, _asn_num = parsed
    return asn_label


def is_asn_quiescent(session: Session, asn_label: str) -> bool:
    """Conjunction of `is_claim_quiescent` over every claim in the ASN's
    claim region (region-based; see `asn_claim_addrs`). An ASN with no
    claims is not quiescent (False), so a mis-resolved label can't read
    as vacuously settled."""
    claims = list(asn_claim_addrs(session, asn_label))
    if not claims:
        return False
    return all(is_doc_quiescent(session, c) for c in claims)


def is_asn_confirmed(session: Session, asn_label: str) -> bool:
    """Conjunction of `is_claim_confirmed` over every claim in the ASN's
    claim region.

    ASN-level analog of `is_claim_confirmed`: each claim quiescent AND
    its most recent review was clean. Used as the full-review trigger's
    quiescence predicate — mirrors how cone-review uses
    `is_claim_confirmed`. Enumerates from the claim region (1.3), NOT the
    note, so claims created during refinement are included; a
    note-provenance walk would miss them and confirm prematurely. An ASN
    with no claims is not confirmed (False)."""
    claims = list(asn_claim_addrs(session, asn_label))
    if not claims:
        return False
    return all(is_claim_confirmed(session, c) for c in claims)
