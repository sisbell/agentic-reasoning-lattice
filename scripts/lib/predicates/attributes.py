"""Attribute-link presence predicates.

Version-bearing addresses (VER3) make alignment questions like "does
the head version of claim D have an active description link?" reduce
to a single substrate query. When the claim revises (D → D.1), an
existing description link still points at D — the predicate returns
False for D.1 until claim-describe runs against it.
"""

from __future__ import annotations

from typing import Optional

from lib.backend.addressing import Address
from lib.protocols.febe.protocol import Session


def has_description(session: Session, doc_addr: Address) -> bool:
    """True iff the doc is the F of an active `description` attribute link.

    Per VER3, the description is pinned to a specific doc version. When
    the doc revises (D → D.1), this returns False for D.1 until
    claim-describe runs against it.
    """
    return bool(session.active_links("description", from_set=[doc_addr]))


def description_is_fresh(session: Session, claim_addr: Address) -> bool:
    """True iff the description's supersession chain is at least as
    long as the claim's chain.

    False when there's no description link at all (initial state).

    Each `register_version` advances the relevant chain by 1; chain
    length counts as "edit count" (claim) or "attestation count"
    (description). Equal counts mean every claim edit has a matching
    description attestation. Lower description count means at least
    one edit is unattested → stale.

    Pure structural counting — no cross-allocator tumbler compare.
    """
    from lib.predicates.versions import supersession_chain_length
    links = session.active_links("description", from_set=[claim_addr])
    if not links or not links[0].to_set:
        return False
    sidecar_addr = links[0].to_set[0]
    return (
        supersession_chain_length(session, sidecar_addr)
        >= supersession_chain_length(session, claim_addr)
    )


def description_sidecar_of(
    session: Session, doc_addr: Address,
) -> Optional[Address]:
    """The description sidecar's address for this doc, or None.

    If multiple active description links exist (rare — usually 1:1),
    returns the first by sibling order.
    """
    links = session.active_links("description", from_set=[doc_addr])
    for link in links:
        if link.to_set:
            return link.to_set[0]
    return None


def has_signature(session: Session, doc_addr: Address) -> bool:
    """True iff the doc has an active `signature` attribute link."""
    return bool(session.active_links("signature", from_set=[doc_addr]))


def signature_sidecar_of(
    session: Session, doc_addr: Address,
) -> Optional[Address]:
    links = session.active_links("signature", from_set=[doc_addr])
    for link in links:
        if link.to_set:
            return link.to_set[0]
    return None


def has_name(session: Session, doc_addr: Address) -> bool:
    return bool(session.active_links("name", from_set=[doc_addr]))


def has_label(session: Session, doc_addr: Address) -> bool:
    return bool(session.active_links("label", from_set=[doc_addr]))
