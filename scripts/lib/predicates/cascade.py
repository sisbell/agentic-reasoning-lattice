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

from typing import Optional

from lib.backend.addressing import Address
from lib.protocols.febe.protocol import Session

from .attributes import (
    description_sidecar_of, signature_sidecar_of, statements_sidecar_of,
)
from .citations import depends
from .quiescence import (
    derived_claims, is_asn_confirmed, is_claim_confirmed, is_claim_quiescent,
    is_claim_structurally_clean,
)
from .versions import (
    is_head_version, supersession_head, version_head,
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

    For citations whose target is a note that has been decomposed,
    the freshness check runs against the `claims.statements` aggregate
    reached via `note → statements → supersession`, not the note's own
    chain — claim-level edits advance the aggregate (via
    `ClaimsStatementsRefreshAgent`) while the note's chain stays
    static. See `_assembly_artifact_or_self`.
    """
    head = version_head(session, claim_addr)
    for upstream in depends(session, head):
        target = _assembly_artifact_or_self(session, upstream)
        if not is_head_version(session, target):
            return False
    return True


def _assembly_artifact_or_self(
    session: Session, addr: Address,
) -> Address:
    """Redirect cascade-freshness to the assembly artifact when one
    exists.

    For a note whose `statements` sidecar has been superseded by a
    `claims.statements` aggregate (the post-decompose state), the
    cascade signal lives on the aggregate's version chain. Walk
    `note → statements → supersession_head` and return the aggregate.

    Falls through to `addr` itself when:
      - `addr` has no `statements` sidecar (claims, foundation notes,
        un-decomposed notes).
      - The sidecar exists but has no outgoing supersession (decompose
        hasn't run yet).
    """
    sidecar = statements_sidecar_of(session, addr)
    if sidecar is None:
        return addr
    aggregate = supersession_head(session, sidecar)
    if aggregate == sidecar:
        return addr
    return aggregate


def description_is_fresh_after_asn_confirmation(
    session: Session, claim_addr: Address,
) -> bool:
    """Gate `claim_describe` to fire only after the whole ASN settles
    AND the claim has revised past the sidecar's last attestation.

    Each `attest_against_doc_head` fire emits a `citation.depends`
    from the new sidecar version to `version_head(claim)` at attest
    time. The predicate reads that citation: if the cited claim
    address is still head, the sidecar covers the current claim;
    if not, the claim has been revised past it.

    True (skip) when:
      - The claim's source note isn't `is_asn_confirmed` yet.
      - Sidecar exists AND its head version cites the claim's
        current head version.

    False (fire) when ASN is confirmed AND either:
      - No sidecar yet (initial attestation needed).
      - Sidecar's head version cites a non-head claim version
        (claim revised past last attestation).

    No chain-length comparison; chain advances by 1 per real
    attestation.
    """
    return _sidecar_against_doc_head_fresh(
        session, claim_addr, description_sidecar_of,
    )


def signature_is_fresh_after_asn_confirmation(
    session: Session, claim_addr: Address,
) -> bool:
    """Gate `claim_signature_resolve` to fire post-ASN-confirmation,
    once per claim that has revised past the signature sidecar's
    last attestation.

    Same shape as `description_is_fresh_after_asn_confirmation`:
    each fire emits a `citation.depends` from the new signature
    sidecar version to `version_head(claim)`; predicate flips False
    when the cited claim version is no longer head.
    """
    return _sidecar_against_doc_head_fresh(
        session, claim_addr, signature_sidecar_of,
    )


def _sidecar_against_doc_head_fresh(
    session: Session, claim_addr: Address, sidecar_lookup,
) -> bool:
    note_addr = _source_note_for_claim(session, claim_addr)
    if note_addr is None:
        return True
    if not is_asn_confirmed(session, note_addr):
        return True
    sidecar = sidecar_lookup(session, claim_addr)
    if sidecar is None:
        return False
    sidecar_head = version_head(session, sidecar)
    claim_head = version_head(session, claim_addr)
    citations = session.active_links(
        "citation.depends", from_set=[sidecar_head],
    )
    for link in citations:
        if claim_head in link.to_set:
            return True
    return False


def _source_note_for_claim(
    session: Session, claim_addr: Address,
) -> Optional[Address]:
    """Reverse-walk `provenance.derivation` to find the source note."""
    incoming = session.active_links(
        "provenance.derivation", to_set=[claim_addr],
    )
    if not incoming:
        return None
    return incoming[0].from_set[0]


def claims_statements_for_note(
    session: Session, note_addr: Address,
) -> Optional[Address]:
    """Resolve the `claims.statements` aggregate doc derived from a note.

    Walks `note → provenance.derivation → target` and returns the
    target carrying the `claims.statements` classifier. None if no
    such aggregate has been emitted yet (decompose hasn't run, or the
    note has no derived claims).
    """
    for link in session.active_links(
        "provenance.derivation", from_set=[note_addr],
    ):
        for target in link.to_set:
            if session.active_links("claims.statements", to_set=[target]):
                return target
    return None


def is_claims_statements_fresh(
    session: Session, note_addr: Address,
) -> bool:
    """True iff the note's `claims.statements` aggregate is up to date
    with its derived claims, gated on every claim being confirmed.

    Drives the two-mode `ClaimsStatementsRefreshAgent`:

      Quiescent (returns True) when:
        - No claim-classified derivations exist (degenerate ASN).
        - Any derived claim is not confirmed (gate closed — defer
          aggregate work until the cluster has settled).
        - Aggregate exists AND its head version emits a
          `citation.depends` to every derived claim's current head
          (caught up).

      Stale (returns False) when every claim is confirmed AND either:
        - No aggregate exists yet → fire creates it (the discovery
          → claim transition).
        - Aggregate exists but at least one derived claim's current
          head isn't cited by the aggregate's head → fire re-renders
          + register_version + re-emits citation anchors.

    The 1:N variant of the citation-anchor pattern. Each fire of
    `ClaimsStatementsRefreshAgent` emits N `citation.depends` links
    from the new aggregate version to `version_head(claim)` for each
    derived claim — the freshness anchors. Address-identity, not
    chain-length.

    The gate iterates claim-classified derivations only; the aggregate
    is itself a derivation target of the note but is never reviewed,
    so a raw `is_asn_confirmed` walk would never return True once the
    aggregate has been emitted.
    """
    classified_claims = {
        link.to_set[0]
        for link in session.active_links("claim")
        if link.to_set
    }
    claims = [
        d for d in derived_claims(session, note_addr)
        if d in classified_claims
    ]
    if not claims:
        return True
    if not all(is_claim_confirmed(session, c) for c in claims):
        return True
    doc = claims_statements_for_note(session, note_addr)
    if doc is None:
        return False

    aggregate_head = version_head(session, doc)
    cited = set()
    for link in session.active_links(
        "citation.depends", from_set=[aggregate_head],
    ):
        cited.update(link.to_set)
    for claim in claims:
        if version_head(session, claim) not in cited:
            return False
    return True
