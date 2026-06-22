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

import os

from typing import Iterator

from lib.agents.producers.cone_review import ConeReviewAgent
from lib.backend.addressing import Address
from lib.lattice.deps import build_deps_for_asn
from lib.lattice.labels import build_cross_asn_label_index
from lib.predicates import (
    has_formal_contract,
    is_claim_quiescent,
    is_held,
    is_upstream_settled_one_hop,
)
from lib.predicates.quiescence import _review_filed_revise
from lib.predicates.versions import version_head
from lib.protocols.febe.protocol import Session
from lib.runner import Scope, Trigger
from lib.shared.claim_files import build_label_index
from lib.shared.paths import agent_doc_path
from lib.shared.topological_sort import topological_levels

_AGENT = ConeReviewAgent()


# Minimum direct same-ASN dependencies for a claim to be an apex (and so
# get its own focused cone review). Read at module load from the
# CONE_MIN_DEPS env var (default 4) so run-claims-continuous.sh can set
# it via runner.env; claim-scheduler.py's --cone-min-deps overrides this
# module global directly at runtime. Lower → more apexes → more focused
# per-cone reviews (higher coverage, higher cost). The apex-selection
# code reads this global at call time, so a runtime override takes effect.
CONE_MIN_DEPS = int(os.environ.get("CONE_MIN_DEPS", "4"))


def apex_labels_in_topological_order(
    session: Session, asn_label: str,
) -> list[str]:
    """Yield apex labels (claims with >= CONE_MIN_DEPS same-ASN deps)
    in topological order (foundations first).

    Public helper for CLI discovery (`--apexes`) and `--force-from`
    expansion. Pure read; no side effects.
    """
    asn_num = int(asn_label[4:])
    claim_dir = _AGENT.claim_dir / asn_label
    if not claim_dir.exists():
        return []

    asn_labels_in_asn = set(build_label_index(claim_dir).keys())
    deps_data = build_deps_for_asn(asn_num, _AGENT.claim_dir)
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


# An apex is cone-converged at two consecutive clean cone reviews — the
# same n=2 rule the global phase uses (quiescence.CLAIM_CONFIRMATION_N),
# but counted over the apex's OWN cone reviews, not whole-ASN full reviews.
CONE_CONFIRMATION_N = 2


def _clean_cone_review_streak(
    session: Session, claim_addr: Address,
) -> int:
    """Number of trailing consecutive CLEAN cone-attributed reviews of
    `claim_addr`. The apex is cone-converged once this reaches
    CONE_CONFIRMATION_N.

    Cone reviews are distinguished from whole-ASN full reviews via the
    `manages` graph: every substrate write the cone-review agent emits is
    auto-tagged `manages(cone-review-agent → link)` by AttributingStore,
    so a `review.coverage` with such an edge is a cone review. Ordered by
    emission (link address); a REVISE-filing cone review resets the
    streak (same emit-time-verdict rule as global, see
    quiescence._review_filed_revise).

    This replaces the old boolean `_has_been_cone_reviewed` (≥1 ever),
    which let the skip predicate mark an apex done after a SINGLE cone
    review — the "two" in the old skip came from is_claim_confirmed, the
    GLOBAL n=2, so the cone phase never actually converged on its own.
    """
    cone_agent = session.get_addr_for_path(agent_doc_path("cone-review"))
    if cone_agent is None:
        return 0
    covs = [
        cov for cov in session.active_links(
            "review.coverage", to_set=[claim_addr],
        )
        if cov.from_set
        and session.active_links(
            "manages", from_set=[cone_agent], to_set=[cov.addr],
        )
    ]
    covs.sort(key=lambda cov: cov.addr.digits)
    streak = 0
    for cov in reversed(covs):
        if _review_filed_revise(session, cov.from_set[0]):
            break
        streak += 1
    return streak


def _predicate(session: Session, addr: Address) -> bool:
    """True (skip) iff cone-review should not fire on this claim.

    Five skip conditions:
      1. Claim has no Formal Contract section yet — wait for
         `claim_formal_contract` to land before reviewing. Without
         a Formal Contract there's nothing substantive to review.
      2. The apex claim is currently held by another agent (the
         repellent-pheromone mutex at claim granularity). Full-review
         multi-holds every claim of the ASN; if it's running, the
         apex is among them and we skip. This is the cone-vs-full
         exclusion.
      3. Upstream is mid-update — `is_upstream_settled_one_hop` is
         False. Wait for direct citation upstream to be locally
         settled before reviewing this claim. Implements the chaining
         model's layered-convergence gate.
      4. The apex has CONE_CONFIRMATION_N (=2) consecutive clean cone
         reviews — its own n=2 convergence. Two converged cone reviews
         and it's done; otherwise it still needs one. (The old skip
         used is_claim_confirmed — the GLOBAL n=2 — plus "≥1 cone review
         ever", so it declared an apex done after a SINGLE cone review.)
      5. Open revises pending on this claim — let the refiner close
         them before re-reviewing.
    """
    if not has_formal_contract(session, addr):
        return True
    if is_held(session, addr):
        return True
    if not is_upstream_settled_one_hop(session, addr):
        return True
    if _clean_cone_review_streak(session, addr) >= CONE_CONFIRMATION_N:
        return True
    if not is_claim_quiescent(session, addr):
        return True
    return False


from lib.triggers._commit_paths import per_asn_claim_review_paths


cone_review = Trigger(
    name="cone-review",
    scope_query=_scope_query,
    predicate=_predicate,
    agent=_AGENT,
    supports_claim_filter=True,
    commit_paths=per_asn_claim_review_paths,
)
