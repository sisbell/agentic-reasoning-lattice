"""Cone-review trigger — fires on unconverged claims with enough deps.

The cone-review agent runs a focused regional review on a claim and
its same-ASN dependency chain. This trigger declares when it should
fire:

  scope:     claims in the requested ASN with >= MIN_DEPS same-ASN deps,
             walked in topological order (foundations first)
  predicate: is_claim_converged
  agent:     run_cone_review (the existing orchestrator function)
"""

from __future__ import annotations

from typing import Iterator

from lib.backend.addressing import Address
from lib.lattice.deps import build_deps_for_asn
from lib.lattice.labels import build_cross_asn_label_index
from lib.orchestrators.cone_review import run_cone_review
from lib.predicates import is_claim_converged
from lib.protocols.febe.protocol import Session
from lib.runner import Scope, Trigger
from lib.shared.claim_files import build_label_index
from lib.shared.paths import CLAIM_DIR
from lib.shared.topological_sort import topological_levels


CONE_MIN_DEPS = 4
CONE_MAX_CYCLES = 8
CONE_MODEL = "sonnet"


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

    apexes: list[str] = []
    for level_labels in topological_levels(deps_data):
        for label in level_labels:
            apex_addr = label_index.get(label)
            if apex_addr is None:
                continue
            same_deps = [
                rev_index[link.to_set[0]]
                for link in session.active_links(
                    "citation.depends", from_set=[apex_addr],
                )
                if link.to_set
                and rev_index.get(link.to_set[0]) in asn_labels_in_asn
            ]
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


def _agent(session: Session, addr: Address) -> None:
    """Resolve apex context and dispatch the cone-review orchestrator."""
    label_index = build_cross_asn_label_index(session.store)
    rev_index = {a: lbl for lbl, a in label_index.items()}

    apex_label = rev_index.get(addr)
    if apex_label is None:
        return

    asn_path = session.get_path_for_addr(addr)
    if asn_path is None:
        return
    asn_label_str = asn_path.split("/")[3]  # _docuverse/documents/claim/<ASN>/<label>.md
    asn_num = int(asn_label_str[4:])

    claim_dir = CLAIM_DIR / asn_label_str
    asn_labels = set(build_label_index(claim_dir).keys())
    same_deps = [
        rev_index[link.to_set[0]]
        for link in session.active_links(
            "citation.depends", from_set=[addr],
        )
        if link.to_set and rev_index.get(link.to_set[0]) in asn_labels
    ]

    run_cone_review(
        asn_num, apex_label, same_deps,
        max_cycles=CONE_MAX_CYCLES, model=CONE_MODEL,
    )


cone_review = Trigger(
    name="cone-review",
    scope_query=_scope_query,
    predicate=is_claim_converged,
    agent=_agent,
)
