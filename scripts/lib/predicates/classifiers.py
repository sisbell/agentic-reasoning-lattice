"""Classifier-enumeration predicates.

Walk classifier link types and surface the docs they classify.
Includes the `contract.<kind>` reverse lookup for contract-kind
introspection.

Single-kind presence predicates are generated via
`lib/predicates/factory.py`'s `is_classifier(kind)` template.
"""

from __future__ import annotations

from typing import List, Optional, Set

from lib.backend.addressing import Address
from lib.protocols.febe.protocol import Session

from .factory import is_classifier


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


def has_contract_kind(session: Session, claim_addr: Address) -> bool:
    """True iff the claim has any `contract.<kind>` classifier.

    Used as the skip-predicate for the claim-contract producer:
    fires when False (no classifier yet); skips when True (already
    classified). Once-and-done — the agent does NOT re-fire on
    subsequent claim edits (contract kind is structural metadata,
    rarely changes after initial classification).
    """
    return current_contract_kind(session, claim_addr) is not None


# Kinds that don't get a Formal Contract section in the claim body —
# definitions assign meaning, axioms are foundational postulates,
# design-requirements are system constraints with informal justification.
# The remaining kinds (theorem, lemma, corollary) DO need a Formal
# Contract section synthesized from the proof.
_KINDS_WITHOUT_FORMAL_CONTRACT = frozenset({
    "definition", "axiom", "design-requirement",
})


def has_formal_contract(
    session: Session, claim_addr: Address,
) -> bool:
    """True iff the claim's doc body contains a `*Formal Contract:*`
    section.

    Reads the file directly. Returns False if the path can't be resolved
    or the file is missing.
    """
    rel = session.get_path_for_addr(claim_addr)
    if rel is None:
        return False
    full = session.store.lattice_dir / rel
    if not full.exists():
        return False
    return "*Formal Contract:*" in full.read_text()


def claim_formal_contract_is_fresh(
    session: Session, claim_addr: Address,
) -> bool:
    """Skip-predicate for the claim-formal-contract producer.

    True (skip) iff:
    - The claim's contract kind is not yet classified (wait for
      claim_contract producer), OR
    - The kind doesn't need a Formal Contract section (definition /
      axiom / design-requirement), OR
    - The claim md already has a Formal Contract section.

    False (fire) iff the claim is theorem/lemma/corollary AND the
    body still lacks the section.

    Existence-only — once synthesized, doesn't re-fire on subsequent
    body edits. Drift is caught by the structural validator (scout +
    refiner pair) if and when it surfaces.
    """
    kind = current_contract_kind(session, claim_addr)
    if kind is None:
        return True  # wait for claim_contract producer
    if kind in _KINDS_WITHOUT_FORMAL_CONTRACT:
        return True
    return has_formal_contract(session, claim_addr)


def all_classified(session: Session, kind: str) -> List[Address]:
    """Every doc with a classifier link of the given kind. Sorted."""
    out: Set[Address] = set()
    for link in session.find_links(type_=kind):
        # Classifier shape: F=∅, G=[doc]
        if not link.from_set:
            out.update(link.to_set)
    return sorted(out, key=lambda a: a.digits)


is_retired = is_classifier("retired")


def is_review_decomposed(session: Session, review_addr: Address) -> bool:
    """True iff the review has been decomposed into per-finding substrate.

    Substrate-driven: the claim_findings producer emits at least one
    `provenance.derivation` link from review_addr per fire. Non-zero
    findings → derivation(s) to per-finding doc(s). Zero findings →
    one derivation with G=∅ (the review derived nothing). Either
    shape, the predicate sees an outbound derivation and reports the
    review as decomposed.

    No verb-flag classifier. The empty-derivation pattern (F=[review],
    G=∅) is the structural fact "decompose ran, produced no
    derivatives" — semantically honest where a self-link wasn't.
    """
    return bool(session.active_links(
        "provenance.derivation", from_set=[review_addr],
    ))
