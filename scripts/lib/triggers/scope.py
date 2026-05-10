"""Reusable scope-query helpers for triggers.

Trigger `scope_query` functions yield the addresses a trigger should
evaluate this pass. Most triggers fit one of four standard shapes:

  per_claim_of_asn   — every claim-classified derivation of an ASN
  per_active_note    — every active non-retired note
  per_inquiry_of_asn — every inquiry doc
  per_asn_note       — the single note for the requested ASN (CLI only)

Each helper handles both CLI mode (scope.asn_label set) and daemon
mode (asn_label is None), where applicable. Triggers with custom
shapes (e.g., per-comment, per-review, per-apex) keep bespoke
scope_query implementations.

The shared `_claim_set_for_scope` builds the set of in-scope claim
addresses; `per_claim_of_asn` yields from it directly, and
trigger-specific filters (e.g., claim_revise's per-comment query)
can use it to scope their own walks.
"""

from __future__ import annotations

from typing import Iterator, Set

from lib.backend.addressing import Address
from lib.predicates import derived_claims, is_retired
from lib.protocols.febe.protocol import Session
from lib.runner import Scope, asn_note_addr
from lib.shared.paths import WORKSPACE, inquiry_doc_path


def _claim_set_for_scope(session: Session, scope: Scope) -> Set[Address]:
    """Return the set of claim-classified addresses in scope.

    CLI mode: claim-classified derivations of the ASN's source note,
    optionally narrowed to `scope.labels` if the scope carries any.
    Daemon mode: every claim-classified address (labels ignored;
    daemon scopes are not label-filtered).

    Used by `per_claim_of_asn` directly and by triggers that need
    the in-scope claim set as a filter (e.g., claim_revise scoping
    its comment.revise query to claims of the current ASN).
    """
    classified_claims = {
        link.to_set[0]
        for link in session.active_links("claim")
        if link.to_set
    }
    if scope.asn_label is None:
        return classified_claims

    note_addr = asn_note_addr(session, scope)
    if note_addr is None:
        return set()
    in_asn = {
        d for d in derived_claims(session, note_addr)
        if d in classified_claims
    }
    if scope.labels is None:
        return in_asn

    from lib.lattice.labels import build_cross_asn_label_index
    label_index = build_cross_asn_label_index(session.store)
    wanted = {
        addr for label, addr in label_index.items()
        if label in scope.labels
    }
    return in_asn & wanted


def per_claim_of_asn(
    session: Session, scope: Scope,
) -> Iterator[Address]:
    """Yield each claim-classified derivation of the ASN's source note.

    CLI mode: derivations of the ASN's note, filtered to claim-
    classified addresses (skips non-claim derivations like the
    claim-statements transclusion). Daemon mode: every claim-
    classified address.

    Used by claim_contract, claim_describe, claim_signature_resolve,
    claim_citation_resolve, claim_formal_contract,
    claim_structural_audit, claim_structural_revise.
    """
    yield from _claim_set_for_scope(session, scope)


def per_active_note(
    session: Session, scope: Scope,
) -> Iterator[Address]:
    """Yield active non-retired notes in scope.

    CLI mode: the single ASN's note. Daemon mode: every active
    non-retired note.

    Used by note_review, note_revise, note_consult.
    """
    if scope.asn_label is not None:
        addr = asn_note_addr(session, scope)
        if addr is not None:
            yield addr
        return
    for link in session.active_links("note"):
        if not link.to_set:
            continue
        addr = link.to_set[0]
        if not is_retired(session, addr):
            yield addr


def per_inquiry_of_asn(
    session: Session, scope: Scope,
) -> Iterator[Address]:
    """Yield inquiry-doc addresses in scope.

    CLI mode: the single ASN's inquiry doc. Daemon mode: every
    active inquiry.

    Used by note_draft, inquiry_consult.
    """
    if scope.asn_label is not None:
        asn_num = int(scope.asn_label[4:])
        path = inquiry_doc_path(asn_num)
        if not path.exists():
            return
        rel = str(path.resolve().relative_to(WORKSPACE.resolve()))
        addr = session.get_addr_for_path(rel)
        if addr is not None:
            yield addr
        return
    for link in session.active_links("inquiry"):
        if link.to_set:
            yield link.to_set[0]


def per_asn_note(
    session: Session, scope: Scope,
) -> Iterator[Address]:
    """Yield the source note address for the requested ASN.

    CLI-only: returns nothing in daemon mode (no asn_label). Used
    by triggers whose semantics require a specific ASN (note_statements,
    full_review).
    """
    addr = asn_note_addr(session, scope)
    if addr is not None:
        yield addr
