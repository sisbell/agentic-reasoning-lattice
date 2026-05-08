"""Cascade-aware predicates — the chaining model's first instance.

Two predicates that together let a content-review trigger respect
upstream activity:

    is_upstream_settled_one_hop(session, claim_addr)
        — the *gate*. True iff every direct citation upstream of
        `claim_addr` is locally settled (no unresolved comment.revise,
        no unresolved comment.violation). Prevents the trigger from
        firing while any direct upstream is mid-update — the layered-
        convergence guarantee.

    is_cascade_fresh_one_hop(session, claim_addr)
        — the *staleness detector*. True iff no direct citation
        upstream has activity newer than this claim's latest content
        review. Detects "claim was previously reviewed clean, but
        upstream has since advanced" — what makes the runner re-fire
        on cascade-stale claims even after they were once confirmed.

Both compose existing predicates (`depends`, `is_claim_quiescent`,
`is_claim_structurally_clean`) plus emit-order comparison via
LinkStore position. No new substrate state, no new tuple kinds.

Note on emit-order: tumbler addresses are allocated *per homedoc*
(per ASN-0043 link addressing), so digit-by-digit comparison across
links from different homedocs doesn't reflect global emit-order.
Global emit-order is the LinkStore's iteration order — the append-
only log (R3 monotonicity) is the canonical record of "what came
after what." We build a position map once per evaluation and use it
for comparison.
"""

from __future__ import annotations

from typing import Optional

from lib.backend.addressing import Address
from lib.protocols.febe.protocol import Session

from .citations import depends
from .quiescence import is_claim_quiescent, is_claim_structurally_clean


# Direct-target tuple kinds: tuples whose `to_set` contains the
# upstream itself. Their existence with addr > anchor means upstream
# is in flight or its state moved.
DIRECT_KINDS_FOR_CONTENT = (
    "comment.revise",
    "comment.violation",
    "retraction",
)

# Two-hop tuple kinds: tuples that target a *comment* on the upstream,
# not the upstream directly. A resolution with addr > anchor implies
# upstream's body was edited as part of closing the comment, so the
# upstream's reasoning content shifted post-anchor.
TWO_HOP_KINDS_FOR_CONTENT = (
    "resolution.edit",
    "resolution.reject",
)


def is_upstream_settled_one_hop(
    session: Session, claim_addr: Address,
) -> bool:
    """True iff every direct citation upstream of `claim_addr` is
    locally settled.

    "Settled" means no unresolved `comment.revise` and no unresolved
    `comment.violation` targeting the upstream. The chaining gate that
    blocks a downstream agent from firing while any direct upstream is
    mid-update — closing comments, applying body edits, etc.

    Foundation claims (no citation upstream) are vacuously settled.
    The bottom-up cascade emerges: foundation's gate is trivially
    open; layer-1's gate clears when foundation settles; layer-2's
    gate clears when layer-1 settles.
    """
    for upstream in depends(session, claim_addr):
        if not is_claim_quiescent(session, upstream):
            return False
        if not is_claim_structurally_clean(session, upstream):
            return False
    return True


def _emit_position_map(session: Session) -> dict:
    """Build a (link addr → linkstore position) map for the session.

    LinkStore iteration order is global emit-order (R3 append-only).
    Tumbler addresses are per-homedoc, so this is the canonical way
    to compare "did A get emitted before B" across homedocs. Built
    once per predicate call; O(N) walk.
    """
    return {
        link.addr: i for i, link in enumerate(session.state.links)
    }


def _latest_review_coverage_addr(
    session: Session, claim_addr: Address, positions: dict,
) -> Optional[Address]:
    """Return the address of the latest-emitted `review.coverage` link
    covering `claim_addr` whose source carries a `review.content`
    classifier. None if no such coverage exists.

    "Latest" is measured by linkstore position — the canonical emit
    order — not by digit comparison (which doesn't work across
    homedocs).
    """
    coverage_links = [
        link for link in session.active_links(
            "review.coverage", to_set=[claim_addr],
        )
        if link.from_set
        and session.active_links(
            "review.content", to_set=[link.from_set[0]],
        )
    ]
    if not coverage_links:
        return None
    return max(
        coverage_links, key=lambda link: positions[link.addr],
    ).addr


def is_cascade_fresh_one_hop(
    session: Session, claim_addr: Address,
) -> bool:
    """True iff no direct citation upstream of `claim_addr` has tuples
    emitted after the anchor (claim's latest review.coverage).

    Returns False if `claim_addr` has never been content-reviewed
    (no anchor → not fresh, definitely needs a first review).

    Composes only existing substrate primitives. Does not introduce
    any cached or per-agent state — each evaluation is a pure read of
    current substrate state. Emit-order via LinkStore position.
    """
    positions = _emit_position_map(session)
    anchor = _latest_review_coverage_addr(session, claim_addr, positions)
    if anchor is None:
        return False  # never reviewed → not fresh

    anchor_pos = positions[anchor]
    for upstream in depends(session, claim_addr):
        # Direct-target check: tuples whose to_set contains upstream.
        for kind in DIRECT_KINDS_FOR_CONTENT:
            for link in session.active_links(kind, to_set=[upstream]):
                if positions[link.addr] > anchor_pos:
                    return False
        # Two-hop check: resolutions targeting comments on upstream.
        # Resolution.edit's to_set is the comment, not the upstream;
        # but its existence post-anchor implies upstream's body was
        # edited as part of the close.
        comments_on_upstream = (
            session.active_links("comment.revise", to_set=[upstream])
            + session.active_links("comment.violation", to_set=[upstream])
        )
        for comment in comments_on_upstream:
            for kind in TWO_HOP_KINDS_FOR_CONTENT:
                for resolution in session.active_links(
                    kind, to_set=[comment.addr],
                ):
                    if positions[resolution.addr] > anchor_pos:
                        return False
    return True
