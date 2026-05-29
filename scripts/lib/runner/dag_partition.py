"""DAG-honoring partition helpers — shared by `note-scheduler.py` and
the `dag_status.py` diagnostic.

The note runner partitions ASNs across workers via a two-clause filter
that respects the dependency DAG:

  active = {a : has_fireable_trigger(a)}
  ready  = {a in active : declared_deps(a) ∩ active == ∅}
  partition = round-robin(ready, worker_idx, worker_total)

A downstream ASN whose declared dep is currently active is excluded
from `ready` so the dep settles first. The per-outer-pass re-eval in
the scheduler lets dependents pick up automatically on the next pass
after the foundation drops out of `active`.

The diagnostic uses the same helpers so the partition preview matches
what the runner will actually do.
"""

from __future__ import annotations

import re
from typing import Iterable, List

from lib.backend.addressing import Address
from lib.protocols.febe.protocol import Session

from .scope import Scope
from .trigger import Trigger


_ASN_PAT = re.compile(r"(ASN-\d{4})")


def has_fireable_trigger(
    session: Session, asn_label: str, triggers: Iterable[Trigger],
) -> bool:
    """True iff at least one (trigger, addr) pair in this ASN's scope has
    an unsatisfied predicate — i.e., the runner would fire something on
    this ASN. Early-exits on the first fire-able pair to keep the check
    cheap.
    """
    scope = Scope(asn_label=asn_label)
    for trig in triggers:
        for addr in trig.scope_query(session, scope):
            if not trig.predicate(session, addr):
                return True
    return False


def build_dep_map(
    session: Session, asn_labels: List[str],
) -> dict[str, set[str]]:
    """Walk substrate `citation.depends` links and return a map from each
    ASN to the set of ASNs it directly depends on, restricted to the
    given asn_labels set.

    Self-loops are excluded. Targets that map to ASNs outside the given
    set are excluded (they don't block partition readiness).
    """
    from lib.backend.predicates import active_links
    state = session.store
    asn_set = set(asn_labels)
    deps: dict[str, set[str]] = {a: set() for a in asn_labels}
    for link in active_links(state, "citation.depends"):
        from_asns: set[str] = set()
        to_asns: set[str] = set()
        for a in link.from_set:
            p = state.path_for_addr(a)
            if p:
                m = _ASN_PAT.search(p)
                if m and m.group(1) in asn_set:
                    from_asns.add(m.group(1))
        for a in link.to_set:
            p = state.path_for_addr(a)
            if p:
                m = _ASN_PAT.search(p)
                if m and m.group(1) in asn_set:
                    to_asns.add(m.group(1))
        for f in from_asns:
            for t in to_asns:
                if f != t:
                    deps[f].add(t)
    return deps


def compute_active_ready_partition(
    session: Session, all_asn_labels: List[str], triggers: List[Trigger],
    partition_index: int, partition_total: int,
) -> tuple[set[str], List[str], List[str]]:
    """Two-pass filter for partition-time DAG-honoring scheduling.

    Returns (active_set, ready_topo, partition_for_this_worker):
      active_set       — every ASN that has at least one fire-able trigger
      ready_topo       — active ASNs whose declared deps are all NOT in
                         active_set (deps are stable), preserving the
                         input topo order
      partition_for_this_worker — round-robin slice of ready_topo

    The two-clause filter is what makes the partition DAG-safe: a
    downstream note enters ready only when every dep has settled.
    Foundations therefore process first; dependents pick up on the
    outer pass after their foundations drop out of the active set.
    """
    active_set = {
        label for label in all_asn_labels
        if has_fireable_trigger(session, label, triggers)
    }
    if not active_set:
        return active_set, [], []
    deps = build_dep_map(session, all_asn_labels)
    ready_topo = [
        a for a in all_asn_labels
        if a in active_set and not (deps[a] & active_set)
    ]
    partition_slice = [
        ready_topo[i] for i in range(len(ready_topo))
        if i % partition_total == partition_index
    ]
    return active_set, ready_topo, partition_slice
