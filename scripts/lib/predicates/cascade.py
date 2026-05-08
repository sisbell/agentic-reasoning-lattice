"""Cascade-aware predicates for the cone-review trigger.

Two predicates compose into the cone-review's `_predicate` to make
cone-review respect upstream activity:

    is_upstream_settled_one_hop(session, claim_addr)
        — the *gate*. True iff every direct citation upstream of
        `claim_addr` is locally settled (no unresolved comment.revise,
        no unresolved comment.violation). Prevents the trigger from
        firing while any direct upstream is mid-update — the layered-
        convergence guarantee. Distribution-friendly: pure existence
        queries via depends + is_claim_quiescent +
        is_claim_structurally_clean.

    is_cascade_fresh_one_hop(session, claim_addr)
        — the *staleness detector*. True iff every direct citation
        upstream of `claim_addr`'s head version is itself a head
        version. Detects "claim was previously reviewed clean, but
        upstream has since been edited" — what makes the runner re-fire
        on cascade-stale claims even after they were once confirmed.

Both compose existing substrate primitives. No new substrate state, no
new tuple kinds, no emit-order comparison — the version chain itself
carries the cascade signal.

The mechanism:
- Body edits call `register_version(claim_addr)` (already in place at
  `resolution.py`, `claim_structural_revise.py`, `claim_formal_contract.py`).
- `register_version` allocates a tumbler-child of the doc and emits a
  supersession link.
- `is_head_version(addr)` is True iff the doc has no version-children.
- After upstream u is edited, `is_head_version(u-identity) = False`.
- A claim's citation pointing at u-identity (no longer head) marks the
  claim as cascade-stale.
- After the claim re-reviews (advancing its own chain), it emits new
  citations from its head version targeting upstream's current head.
- Predicate reads the head version's citations; all targets head → fresh.
"""

from __future__ import annotations

from lib.backend.addressing import Address
from lib.protocols.febe.protocol import Session

from .citations import depends
from .quiescence import is_claim_quiescent, is_claim_structurally_clean
from .versions import is_head_version, version_head


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


def is_cascade_fresh_one_hop(
    session: Session, claim_addr: Address,
) -> bool:
    """True iff every direct citation upstream of `claim_addr`'s head
    version is itself a head version.

    Reads citations from `version_head(claim_addr)` — the latest
    version of the claim. After `register_version` advances the claim's
    chain, the head version's outgoing citations are the post-edit ones
    (emitted by the next sync_claim_citations after re-review).

    For each cited address: `is_head_version` returns False iff that
    address has version-children, i.e., upstream has been edited since
    the citation was emitted. Any non-head target → cascade-stale.

    Vacuously fresh when the head version has no outgoing citations
    (e.g., a freshly created version-marker that hasn't yet been
    re-reviewed). The trigger predicate composition handles that path
    via `is_claim_confirmed` — a claim with no recent clean review is
    not confirmed, so the cascade-fresh skip branch is bypassed and
    cone-review fires regardless.
    """
    head = version_head(session, claim_addr)
    for upstream in depends(session, head):
        if not is_head_version(session, upstream):
            return False
    return True
