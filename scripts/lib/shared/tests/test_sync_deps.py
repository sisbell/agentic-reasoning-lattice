"""Tests for lib.shared.sync_deps — reconciliation logic.

Unit tests cover the SyncPlan dataclass behavior (needs_emit, is_noop)
against synthesized plans. Integration test runs the planner against
the live substrate to ensure it produces actionable plans for known
ASN states (NEW_ONLY, HEALTHY, etc.) without ever silently misclassifying.
"""

from __future__ import annotations

import pytest

from lib.shared.sync_deps import (
    SyncDepsError,
    SyncPlan,
    apply_plan,
    plan_reconciliation,
)


# ─── SyncPlan helper-property semantics ────────────────────────────


def test_plan_is_noop_when_matching_link_exists_and_nothing_to_retract() -> None:
    plan = SyncPlan(
        asn_num=97,
        declared_deps=[34, 36],
        inquiry_addr="dummy_inq",
        note_addr="dummy_note",
        keep_link="dummy_link",
    )
    assert plan.is_noop is True
    assert plan.needs_emit is False


def test_plan_needs_emit_when_no_match_and_deps_declared() -> None:
    plan = SyncPlan(
        asn_num=97,
        declared_deps=[34, 36],
        inquiry_addr="dummy_inq",
        note_addr="dummy_note",
        dep_addrs=["a", "b"],
    )
    assert plan.needs_emit is True
    assert plan.is_noop is False


def test_plan_no_emit_when_empty_deps_declared() -> None:
    # depends: [] — foundation ASN case. Nothing to emit even if no
    # keep_link exists.
    plan = SyncPlan(
        asn_num=34,
        declared_deps=[],
        inquiry_addr="dummy_inq",
        note_addr="dummy_note",
    )
    assert plan.needs_emit is False
    assert plan.is_noop is True  # nothing to do, no retracts pending


def test_plan_not_noop_when_retracts_pending() -> None:
    plan = SyncPlan(
        asn_num=97,
        declared_deps=[34, 36],
        inquiry_addr="dummy_inq",
        note_addr="dummy_note",
        keep_link="dummy_link",
        retract_inquiry=["link_to_retract"],
    )
    assert plan.is_noop is False


def test_plan_not_noop_when_note_side_retracts_pending() -> None:
    plan = SyncPlan(
        asn_num=97,
        declared_deps=[34, 36],
        inquiry_addr="dummy_inq",
        note_addr="dummy_note",
        keep_link="dummy_link",
        retract_note=["legacy_link"],
    )
    assert plan.is_noop is False


# ─── plan_reconciliation against live substrate ────────────────────


def _open_session():
    from lib.protocols.febe.session import open_session
    from lib.shared.paths import LATTICE
    return open_session(LATTICE)


def test_plan_for_asn_with_no_inquiry_raises() -> None:
    # ASN 99999 has no inquiry file
    with _open_session() as session:
        with pytest.raises(Exception):  # SyncDepsError or FoundationError
            plan_reconciliation(session, 99999)


def test_plan_for_asn_0097_is_actionable() -> None:
    """ASN-0097 should be in NEW_ONLY state per the audit: 7 one-per-target
    inquiry-side, 0 note-side. Reconciliation should retract all 7 and
    emit one fan-out (or, if step-4 has already run, be a no-op)."""
    with _open_session() as session:
        plan = plan_reconciliation(session, 97)
    assert plan.declared_deps == [34, 36, 40, 43, 47, 53, 58]
    assert plan.inquiry_addr is not None
    # Either: pre-fix state (7 one-per-target to retract, needs emit),
    # or: post-fix state (1 fan-out kept, nothing to retract).
    if plan.is_noop:
        assert plan.keep_link is not None
        assert len(plan.keep_link.to_set) == 7
        assert not plan.retract_inquiry
        assert not plan.retract_note
    else:
        # Pre-fix: 7 one-per-target on inquiry side, all need retract,
        # fan-out needs emit.
        assert plan.needs_emit
        assert len(plan.retract_inquiry) == 7
        assert all(
            len(L.to_set) == 1 for L in plan.retract_inquiry
        )
        assert len(plan.dep_addrs) == 7


def test_plan_for_asn_0088_raises_when_dep_unresolvable() -> None:
    """ASN-0088 declares ASN-0097 as a dep. If 0097's note isn't
    in substrate (or any other dep isn't), planner should raise rather
    than emit a partial fan-out. (Today 0097's note IS in substrate, so
    this should produce a plan.)"""
    with _open_session() as session:
        try:
            plan = plan_reconciliation(session, 88)
        except SyncDepsError as e:
            # Acceptable outcome if a dep has no note yet
            assert "not in substrate" in str(e)
            return
    # If it didn't raise, the plan must be actionable
    assert plan.declared_deps
    assert plan.inquiry_addr is not None


def test_plan_for_asn_with_missing_depends_field_raises() -> None:
    """ASN-0036 has no `depends:` field in frontmatter. The planner
    (via _read_inquiry_depends) should raise FoundationError."""
    with _open_session() as session:
        with pytest.raises(Exception) as exc_info:
            plan_reconciliation(session, 36)
        assert "depends" in str(exc_info.value).lower()
