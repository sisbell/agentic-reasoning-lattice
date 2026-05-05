"""Classifier-enumeration predicates.

Walk classifier link types and surface the docs they classify.
Includes the `contract.<kind>` reverse lookup for contract-kind
introspection.
"""

from __future__ import annotations

from typing import List, Optional, Set

from lib.backend.addressing import Address
from lib.protocols.febe.protocol import Session


def all_claim_addrs(session: Session) -> List[Address]:
    """Every doc classified as a claim. Sorted for determinism."""
    out: Set[Address] = set()
    for link in session.find_links(type_="claim"):
        out.update(link.to_set)
    return sorted(out, key=lambda a: a.digits)


def current_contract_kind(
    session: Session, claim_addr: Address,
) -> Optional[str]:
    """Most recent `contract.<kind>` classifier targeting the claim.

    Returns the bare subtype string ("axiom", "theorem", etc.) or None.
    Links are permanent; multiple classifiers may accumulate over time;
    the latest in emission order is the current kind.
    """
    links = session.find_links(to_set=[claim_addr], type_="contract")
    if not links:
        return None
    # Order in LinkStore preserves emission order; take the last
    latest = links[-1]
    if not latest.type_set:
        return None
    name = session.type_name_for(latest.type_set[0])
    if name and "." in name:
        return name.split(".", 1)[1]
    return None


def all_classified(session: Session, kind: str) -> List[Address]:
    """Every doc with a classifier link of the given kind. Sorted."""
    out: Set[Address] = set()
    for link in session.find_links(type_=kind):
        # Classifier shape: F=∅, G=[doc]
        if not link.from_set:
            out.update(link.to_set)
    return sorted(out, key=lambda a: a.digits)


def is_retired(session: Session, doc_addr: Address) -> bool:
    """True iff the doc has an active `retired` classifier link.

    Lifecycle marker per the standalone-link pattern: presence means
    out of the active lattice. Retracting the link revives the doc.
    """
    return bool(session.active_links("retired", to_set=[doc_addr]))
