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
    is_cascade_fresh_one_hop,
    is_claim_confirmed,
    is_claim_quiescent,
    is_upstream_settled_one_hop,
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


def _predicate(session: Session, addr: Address) -> bool:
    """True (skip) iff cone-review should not fire on this claim.

    Three skip conditions:
      1. Upstream is mid-update — `is_upstream_settled_one_hop` is
         False. Wait for direct citation upstream to be locally
         settled before reviewing this claim. Implements the chaining
         model's layered-convergence gate.
      2. Claim is confirmed AND cascade-fresh — already done; nothing
         has advanced upstream since the last review.
      3. Open revises pending on this claim — let the refiner close
         them before re-reviewing.
    """
    if not is_upstream_settled_one_hop(session, addr):
        return True
    if (
        is_claim_confirmed(session, addr)
        and is_cascade_fresh_one_hop(session, addr)
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
)
