"""Cone-review trigger — fires on non-quiescent claims with enough deps.

Wires the ConeReviewAgent (lib/agents/producers/cone_review/) to the
substrate predicate `is_claim_quiescent` over a topologically-ordered
apex scope.

  scope:     claims in the requested ASN with >= MIN_DEPS same-ASN deps,
             walked in topological order (foundations first)
  predicate: is_claim_quiescent
  agent:     ConeReviewAgent
"""

from __future__ import annotations

from typing import Iterator

from lib.agents.producers.cone_review import ConeReviewAgent
from lib.backend.addressing import Address
from lib.lattice.deps import build_deps_for_asn
from lib.lattice.labels import build_cross_asn_label_index
from lib.predicates import (
    has_formal_contract,
    is_cascade_fresh_one_hop,
    is_claim_confirmed,
    is_claim_quiescent,
    is_held,
    is_upstream_settled_one_hop,
    resolve_to_scope,
)
from lib.predicates.versions import version_head
from lib.protocols.febe.protocol import Session
from lib.runner import Scope, Trigger
from lib.shared.claim_files import build_label_index
from lib.shared.paths import CLAIM_DIR
from lib.shared.topological_sort import topological_levels


CONE_MIN_DEPS = 4


def apex_labels_in_topological_order(
    session: Session, asn_label: str,
) -> list[str]:
    """Yield apex labels (claims with >= CONE_MIN_DEPS same-ASN deps)
    in topological order (foundations first).

    Public helper for CLI discovery (`--apexes`) and `--force-from`
    expansion. Pure read; no side effects.
    """
    asn_num = int(asn_label[4:])
    claim_dir = CLAIM_DIR / asn_label
    if not claim_dir.exists():
        return []

    asn_labels_in_asn = set(build_label_index(claim_dir).keys())
    deps_data = build_deps_for_asn(asn_num)
    if not deps_data:
        return []

    label_index = build_cross_asn_label_index(session.store)
    rev_index = {addr: label for label, addr in label_index.items()}
    state = session.state

    def _base(addr: Address) -> Address:
        cur = addr
        while state.parent.get(cur) is not None:
            cur = state.parent[cur]
        return cur

    apexes: list[str] = []
    for level_labels in topological_levels(deps_data):
        for label in level_labels:
            apex_addr = label_index.get(label)
            if apex_addr is None:
                continue
            # Citations are emitted from version_head; walk to head
            # before querying so post-edit citations are visible.
            apex_head = version_head(session, apex_addr)
            same_deps = []
            for link in session.active_links(
                "citation.depends", from_set=[apex_head],
            ):
                if not link.to_set:
                    continue
                # Cited target may be a version address; walk to base
                # for label lookup.
                base = _base(link.to_set[0])
                dep_label = rev_index.get(base)
                if dep_label in asn_labels_in_asn:
                    same_deps.append(dep_label)
            if len(same_deps) >= CONE_MIN_DEPS:
                apexes.append(label)
    return apexes


def _scope_query(session: Session, scope: Scope) -> Iterator[Address]:
    """Yield apex claim addresses, optionally filtered by scope.labels."""
    if scope.asn_label is None:
        return
    label_index = build_cross_asn_label_index(session.store)
    for label in apex_labels_in_topological_order(session, scope.asn_label):
        if scope.labels is not None and label not in scope.labels:
            continue
        addr = label_index.get(label)
        if addr is not None:
            yield addr


def _has_been_cone_reviewed(
    session: Session, claim_addr: Address,
) -> bool:
    """True iff some `review.coverage` link targeting `claim_addr`
    was emitted by the cone-review agent.

    Walks the `manages` graph: every substrate write the cone-review
    agent emits is auto-tagged with `manages(cone-review-agent → link)`
    via `AttributingStore`. The query reads that record — find every
    review.coverage covering the claim, check if any has a `manages`
    edge from the cone-review agent doc.

    Distinguishes "this apex has had its own focused cone review" from
    "this apex was touched by a whole-ASN full review" — both emit
    `review.coverage` to the claim, but only the cone-review-attributed
    one means the apex has received its focused per-cone treatment.
    """
    cone_agent = session.get_addr_for_path(
        "_docuverse/documents/agent/cone-review.md",
    )
    if cone_agent is None:
        return False
    for cov in session.active_links(
        "review.coverage", to_set=[claim_addr],
    ):
        if session.active_links(
            "manages", from_set=[cone_agent], to_set=[cov.addr],
        ):
            return True
    return False


def _predicate(session: Session, addr: Address) -> bool:
    """True (skip) iff cone-review should not fire on this claim.

    Six skip conditions:
      1. Claim has no Formal Contract section yet — wait for
         `claim_formal_contract` to land before reviewing. Without
         a Formal Contract there's nothing substantive to review.
      2. Parent ASN's note is currently held by another agent (the
         repellent-pheromone mutex). cone-review and full-review are
         in conflict at the note-scope; one fires at a time. Wait for
         the holder to retract before firing.
      3. Upstream is mid-update — `is_upstream_settled_one_hop` is
         False. Wait for direct citation upstream to be locally
         settled before reviewing this claim. Implements the chaining
         model's layered-convergence gate.
      4. Claim is confirmed AND cascade-fresh AND has already had a
         cone-attributed review — no further cone review needed
         until upstream advances or confirmation breaks. The
         agent-attributed check distinguishes "covered by full
         review only" from "had its own cone review."
      5. Open revises pending on this claim — let the refiner close
         them before re-reviewing.
    """
    if not has_formal_contract(session, addr):
        return True
    note_addr = resolve_to_scope(session, addr, "note")
    if note_addr is not None and is_held(session, note_addr):
        return True
    if not is_upstream_settled_one_hop(session, addr):
        return True
    if (
        is_claim_confirmed(session, addr)
        and is_cascade_fresh_one_hop(session, addr)
        and _has_been_cone_reviewed(session, addr)
    ):
        return True
    if not is_claim_quiescent(session, addr):
        return True
    return False


cone_review = Trigger(
    name="cone-review",
    scope_query=_scope_query,
    predicate=_predicate,
    agent=ConeReviewAgent(),
    supports_claim_filter=True,
)
