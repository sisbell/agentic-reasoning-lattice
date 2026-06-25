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
from lib.lattice.labels import build_cross_asn_label_index, note_scoped_asns
from lib.predicates import (
    has_formal_contract,
    is_claim_cascade_fresh,
    is_claim_quiescent,
    is_held,
    is_review_decomposed,
    is_upstream_settled_one_hop,
)
from lib.predicates.quiescence import _review_filed_revise
from lib.predicates.versions import version_head
from lib.protocols.febe.protocol import Session
from lib.runner import Scope, Trigger
from lib.shared.claim_files import build_label_index
from lib.shared.paths import is_cone_review_path
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

    # Scope to this ASN + its note-cited deps — labels aren't globally
    # unique (S0 in both ASN-0036 and ASN-0053). Lossless forward (apex
    # lookup) AND reverse (rev_index for cited siblings); the flat index
    # would drop a cited same-ASN sibling whose label collides.
    own_index = build_cross_asn_label_index(
        session.store, allowed_asns=note_scoped_asns(asn_num),
    )
    rev_index = {addr: label for label, addr in own_index.items()}
    state = session.state

    def _base(addr: Address) -> Address:
        cur = addr
        while state.parent.get(cur) is not None:
            cur = state.parent[cur]
        return cur

    apexes: list[str] = []
    for level_labels in topological_levels(deps_data):
        for label in level_labels:
            apex_addr = own_index.get(label)
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
    """Yield the FIRST apex (topological order) that still needs work,
    then stop — the cone phase advances ONE apex at a time.

    Cone reviews interact: a revise on one apex edits a shared dependency
    (e.g. WF) that other apexes' cones include, so a later apex must be
    reviewed against the EARLIER apex's post-revise content. Yielding all
    apexes at once made the runner batch-review every apex against stale
    content before any revise ran. Yielding a single apex lets the runner
    drive its full chain this pass — cone_review, then claim_findings,
    then claim_revise (in that trigger order) — so the apex is
    reviewed→revised→re-reviewed to convergence before the next apex is
    touched. Skipped/converged apexes (per `_predicate`) are passed over.
    """
    if scope.asn_label is None:
        return
    label_index = build_cross_asn_label_index(
        session.store, allowed_asns={scope.asn_label},
    )
    for label in apex_labels_in_topological_order(session, scope.asn_label):
        if scope.labels is not None and label not in scope.labels:
            continue
        addr = label_index.get(label)
        if addr is None:
            continue
        if not _predicate(session, addr):
            yield addr
            return


# An apex is cone-converged at two consecutive clean cone reviews — the
# same n=2 rule the global phase uses (quiescence.CLAIM_CONFIRMATION_N),
# but counted over the apex's OWN cone reviews, not whole-ASN full reviews.
CONE_CONFIRMATION_N = 2


def _clean_cone_review_streak(
    session: Session, claim_addr: Address,
) -> int:
    """Number of trailing consecutive CLEAN cone reviews of `claim_addr`.
    The apex is cone-converged once this reaches CONE_CONFIRMATION_N.

    Cone reviews are distinguished from whole-ASN full reviews by PATH:
    cone reviews live under `review/cone-claims/` (`is_cone_review_path`),
    full reviews under `review/claims/`. Both land `review.coverage` on
    the apex, so the coverage alone can't separate them — the path can.
    This replaces the prior `manages`-edge distinguisher, which relied on
    AttributingStore tagging that the in-process claim runner never emits
    (the session is built before the agent's attribution context opens),
    so NO cone review was ever counted and the streak stuck at 0 → the
    cone phase livelocked (re-reviewing the apex forever).

    Ordered by emission (link address); a REVISE-filing or not-yet-
    decomposed cone review resets the streak (same emit-time-verdict rule
    as global, see quiescence._review_filed_revise).
    """
    covs = [
        cov for cov in session.active_links(
            "review.coverage", to_set=[claim_addr],
        )
        if cov.from_set
        and is_cone_review_path(session.get_path_for_addr(cov.from_set[0]))
    ]
    covs.sort(key=lambda cov: cov.addr.digits)
    streak = 0
    for cov in reversed(covs):
        r = cov.from_set[0]
        # A cone review not yet decomposed into findings has no
        # comment.revise, so _review_filed_revise reads it as clean — but
        # its verdict is unknown until claim_findings runs. Treat pending
        # (undecomposed) as NOT clean so an apex can't be marked converged
        # on reviews whose findings haven't been processed yet.
        if not is_review_decomposed(session, r) or _review_filed_revise(
            session, r
        ):
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
         reviews AND is cascade-fresh — its own n=2 convergence with no
         stale upstream. Two converged cone reviews and a still-current
         cascade anchor and it's done; if an upstream advanced since the
         streak was earned (`is_claim_cascade_fresh` False), the apex is
         not skipped so the cone re-fires. (The old skip used
         is_claim_confirmed — the GLOBAL n=2 — plus "≥1 cone review
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
    if (
        _clean_cone_review_streak(session, addr) >= CONE_CONFIRMATION_N
        and is_claim_cascade_fresh(session, addr)
    ):
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
