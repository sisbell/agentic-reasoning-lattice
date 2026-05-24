"""Reconcile substrate `citation.depends` to match inquiry frontmatter.

Target end state for every ASN:
  - ONE fan-out `citation.depends` link from the inquiry address to
    the dep notes (to_set holds every declared dep)
  - ZERO `citation.depends` links from the note address (legacy
    convention retired)

This module computes what reconciliation would do (`plan_reconciliation`)
and applies it (`apply_plan`). The CLI wrapper in
`scripts/asn-sync-deps.py` is a thin entry point.

Hard-fail contract: if any declared dep can't resolve to a substrate
note address, the plan refuses to emit a partial fan-out and raises
`SyncDepsError`. The operator must fix the spec (add the missing
note or correct the dep list) before reconciliation can proceed.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from lib.backend.addressing import Address
from lib.backend.emit import emit_citation_bundle, emit_retraction
from lib.backend.predicates import active_links
from lib.backend.store import Link
from lib.lattice.labels import format_label
from lib.shared.foundation import _read_inquiry_depends
from lib.shared.paths import NOTE_DIR, WORKSPACE, inquiry_doc_path


class SyncDepsError(Exception):
    """Reconciliation cannot proceed. Always raised with a precise
    message naming the ASN and the obstacle."""


@dataclass
class SyncPlan:
    """What reconciliation will do, computed without any writes."""

    asn_num: int
    declared_deps: List[int]
    inquiry_addr: Optional[Address]
    note_addr: Optional[Address]
    dep_addrs: List[Address] = field(default_factory=list)
    # The single existing fan-out link from inquiry_addr whose to_set
    # matches the declared set as a SET; None if no such link exists.
    keep_link: Optional[Link] = None
    # Inquiry-side links that must be retracted (don't match desired).
    retract_inquiry: List[Link] = field(default_factory=list)
    # All note-side citation.depends links (legacy convention).
    retract_note: List[Link] = field(default_factory=list)

    @property
    def needs_emit(self) -> bool:
        """True iff we need to emit a new fan-out link (no match exists)."""
        return self.keep_link is None and bool(self.dep_addrs)

    @property
    def is_noop(self) -> bool:
        """True iff the substrate is already in the target end state."""
        nothing_to_retract = not self.retract_inquiry and not self.retract_note
        if not self.dep_addrs:
            return nothing_to_retract
        return self.keep_link is not None and nothing_to_retract


def _resolve_inquiry_addr(store, asn_num: int) -> Address:
    """Find the path-registered inquiry address. Raises if absent."""
    inq_path = inquiry_doc_path(asn_num)
    inq_rel = str(inq_path.resolve().relative_to(Path(WORKSPACE).resolve()))
    addr = store.path_to_addr.get(inq_rel)
    if addr is None:
        raise SyncDepsError(
            f"ASN-{asn_num:04d}: inquiry {inq_rel} is not "
            f"path-registered in substrate",
        )
    return addr


def _resolve_note_addr(store, asn_num: int) -> Optional[Address]:
    """Find the path-registered note address. Returns None if no note
    exists yet (legitimate for inquiry-only ASNs, e.g., pre-draft)."""
    label = format_label(asn_num)
    prefix = str(NOTE_DIR.relative_to(WORKSPACE)) + f"/{label}-"
    for path, addr in store.path_to_addr.items():
        if path.startswith(prefix) and not path.endswith(".statements.md"):
            return addr
    return None


def _resolve_dep_addrs(store, asn_num: int, dep_ids: List[int]) -> List[Address]:
    """Resolve each dep ASN id to its note address.

    Returns the addresses in id-sorted order (caller's input is
    already sorted by `_read_inquiry_depends`). Raises SyncDepsError
    if any dep has no note in substrate — the caller must not get a
    partial fan-out.
    """
    out: List[Address] = []
    for dep_id in dep_ids:
        addr = _resolve_note_addr(store, dep_id)
        if addr is None:
            raise SyncDepsError(
                f"ASN-{asn_num:04d} declares dep ASN-{dep_id:04d} but "
                f"its note is not in substrate. Either draft the note "
                f"first or remove this dep from the inquiry frontmatter.",
            )
        out.append(addr)
    return out


def plan_reconciliation(session, asn_num: int) -> SyncPlan:
    """Compute what reconciliation would do — no writes.

    Raises SyncDepsError if the inquiry is malformed or any declared
    dep can't be resolved. A returned plan is always actionable.
    """
    store = session.store
    declared_deps = _read_inquiry_depends(asn_num)

    inquiry_addr = _resolve_inquiry_addr(store, asn_num)
    note_addr = _resolve_note_addr(store, asn_num)

    plan = SyncPlan(
        asn_num=asn_num,
        declared_deps=declared_deps,
        inquiry_addr=inquiry_addr,
        note_addr=note_addr,
    )

    if not declared_deps:
        existing_inq = list(active_links(
            store.state, "citation.depends", from_set=[inquiry_addr],
        ))
        plan.retract_inquiry = existing_inq
        if note_addr is not None:
            plan.retract_note = list(active_links(
                store.state, "citation.depends", from_set=[note_addr],
            ))
        return plan

    plan.dep_addrs = _resolve_dep_addrs(store, asn_num, declared_deps)
    desired_set = set(plan.dep_addrs)

    existing_inq = list(active_links(
        store.state, "citation.depends", from_set=[inquiry_addr],
    ))
    for link in existing_inq:
        if (
            plan.keep_link is None
            and set(link.to_set) == desired_set
            and len(link.to_set) == len(plan.dep_addrs)
        ):
            plan.keep_link = link
        else:
            plan.retract_inquiry.append(link)

    if note_addr is not None:
        plan.retract_note = list(active_links(
            store.state, "citation.depends", from_set=[note_addr],
        ))

    return plan


@dataclass
class ApplyResult:
    asn_num: int
    retracted_inquiry: int = 0
    retracted_note: int = 0
    emitted: bool = False
    kept_existing: bool = False


def apply_plan(session, plan: SyncPlan) -> ApplyResult:
    """Execute the plan: retract inconsistent links, emit the fan-out.

    `by_doc` on retractions is the inquiry address (the doc on whose
    behalf the retraction is filed — the inquiry is the source of the
    declarative spec).
    """
    store = session.store
    result = ApplyResult(asn_num=plan.asn_num)

    if plan.inquiry_addr is None:
        raise SyncDepsError(
            f"ASN-{plan.asn_num:04d}: cannot apply plan with no "
            f"inquiry_addr (this should have been caught at plan-time)",
        )

    for link in plan.retract_inquiry:
        emit_retraction(store, plan.inquiry_addr, link.addr)
        result.retracted_inquiry += 1

    for link in plan.retract_note:
        emit_retraction(store, plan.inquiry_addr, link.addr)
        result.retracted_note += 1

    if plan.keep_link is not None:
        result.kept_existing = True

    if plan.needs_emit:
        emit_citation_bundle(
            store, plan.inquiry_addr, plan.dep_addrs,
            direction="depends",
        )
        result.emitted = True

    return result
