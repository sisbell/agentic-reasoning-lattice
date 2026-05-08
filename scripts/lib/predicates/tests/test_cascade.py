"""Tests for cascade-aware predicates.

Synthetic substrate covering both predicates and the cone-review
trigger predicate's combined behavior. The cascade-fresh predicate
uses version chains: a claim's citations target the upstream's
head version at emit time; if upstream is later edited (creating a
new version via register_version), the cited address is no longer
the head, and cascade-fresh returns False.

The gate (is_upstream_settled_one_hop) uses pure existence queries
(no version primitives) — distribution-friendly via direct
predicate composition.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from lib.backend.addressing import Address
from lib.backend.state import State
from lib.protocols.febe.session import Session
from lib.predicates import (
    is_cascade_fresh_one_hop,
    is_claim_confirmed,
    is_claim_quiescent,
    is_upstream_settled_one_hop,
)


def _emit_clean_review(state, addr, lattice_addr):
    """Emit a review.content classifier + review.coverage targeting addr.
    Used to satisfy is_claim_confirmed (which needs latest_review_was_clean).
    Returns the review doc addr.
    """
    review_doc = state.create_doc(
        kind="review.content", lattice=lattice_addr,
    )
    state.make_link(
        review_doc, [review_doc], [addr], "review.coverage",
    )
    return review_doc


class UpstreamSettledTests(unittest.TestCase):
    """The chaining gate: don't fire downstream while upstream is
    mid-update."""

    def setUp(self):
        self.state = State(account=Address("1.1.0.1"))
        self.session = Session(self.state)
        self.lattice = self.state.create_doc()
        self.claim = self.state.create_doc(
            kind="claim", lattice=self.lattice,
        )
        self.upstream = self.state.create_doc(
            kind="claim", lattice=self.lattice,
        )

    def test_no_upstream_is_vacuously_settled(self):
        # Foundation claim with no citation upstream → trivially True
        self.assertTrue(
            is_upstream_settled_one_hop(self.session, self.claim)
        )

    def test_clean_upstream_is_settled(self):
        # claim cites upstream; no comments anywhere
        self.state.make_link(
            self.claim, [self.claim], [self.upstream], "citation.depends",
        )
        self.assertTrue(
            is_upstream_settled_one_hop(self.session, self.claim)
        )

    def test_unresolved_revise_on_upstream_blocks(self):
        self.state.make_link(
            self.claim, [self.claim], [self.upstream], "citation.depends",
        )
        review = self.state.create_doc(
            kind="review.content", lattice=self.lattice,
        )
        self.state.make_link(
            review, [review], [self.upstream], "comment.revise",
        )
        self.assertFalse(
            is_upstream_settled_one_hop(self.session, self.claim)
        )

    def test_resolved_revise_on_upstream_passes(self):
        self.state.make_link(
            self.claim, [self.claim], [self.upstream], "citation.depends",
        )
        review = self.state.create_doc(
            kind="review.content", lattice=self.lattice,
        )
        comment = self.state.make_link(
            review, [review], [self.upstream], "comment.revise",
        )
        self.state.make_link(
            self.upstream, [self.upstream], [comment.addr],
            "resolution.edit",
        )
        self.assertTrue(
            is_upstream_settled_one_hop(self.session, self.claim)
        )

    def test_unresolved_violation_on_upstream_blocks(self):
        self.state.make_link(
            self.claim, [self.claim], [self.upstream], "citation.depends",
        )
        finding = self.state.create_doc(
            kind="finding", lattice=self.lattice,
        )
        self.state.make_link(
            finding, [finding], [self.upstream],
            "comment.violation",
        )
        self.assertFalse(
            is_upstream_settled_one_hop(self.session, self.claim)
        )

    def test_two_upstream_one_dirty_blocks(self):
        upstream_b = self.state.create_doc(
            kind="claim", lattice=self.lattice,
        )
        self.state.make_link(
            self.claim, [self.claim], [self.upstream, upstream_b],
            "citation.depends",
        )
        review = self.state.create_doc(
            kind="review.content", lattice=self.lattice,
        )
        self.state.make_link(
            review, [review], [upstream_b], "comment.revise",
        )
        self.assertFalse(
            is_upstream_settled_one_hop(self.session, self.claim)
        )


class CascadeFreshTests(unittest.TestCase):
    """The staleness detector: did upstream's version chain advance
    past where this claim's citations point?"""

    def setUp(self):
        # state.create_version sets the parent map (which is_head_version
        # / version_children read), so we don't need a Store-backed
        # session for these tests — Session(state) suffices.
        self.state = State(account=Address("1.1.0.1"))
        self.session = Session(self.state)
        self.lattice = self.state.create_doc()
        self.claim = self.state.create_doc(
            kind="claim", lattice=self.lattice,
        )
        self.upstream = self.state.create_doc(
            kind="claim", lattice=self.lattice,
        )

    def test_no_upstream_is_vacuously_fresh(self):
        # Foundation claim with no citation upstream → trivially True
        self.assertTrue(
            is_cascade_fresh_one_hop(self.session, self.claim)
        )

    def test_unedited_upstream_is_fresh(self):
        # Claim cites upstream; upstream has not been edited
        # (no version-children); is_head_version(upstream) = True
        self.state.make_link(
            self.claim, [self.claim], [self.upstream],
            "citation.depends",
        )
        self.assertTrue(
            is_cascade_fresh_one_hop(self.session, self.claim)
        )

    def test_edited_upstream_is_stale(self):
        # Claim cites upstream-identity; upstream is edited via
        # register_version; the cited address is no longer head
        self.state.make_link(
            self.claim, [self.claim], [self.upstream],
            "citation.depends",
        )
        # Upstream is edited — register_version creates a child
        self.state.create_version(self.upstream)
        # Now upstream-identity has version-children; not head
        self.assertFalse(
            is_cascade_fresh_one_hop(self.session, self.claim)
        )

    def test_re_review_at_new_head_is_fresh(self):
        # Realistic re-review flow:
        # 1. claim cites upstream-identity originally
        # 2. upstream is edited (create_version)
        # 3. claim is edited via re-review (create_version on claim)
        # 4. New citation emitted from claim's head to upstream's head
        # 5. Predicate walks depends(version_head(claim)) — only the
        #    new citation; old citations from claim-identity are not
        #    queried.
        self.state.make_link(
            self.claim, [self.claim], [self.upstream],
            "citation.depends",
        )
        # Upstream is edited
        upstream_v1 = self.state.create_version(self.upstream)
        # Claim is also re-reviewed (create_version advances chain)
        claim_v1 = self.state.create_version(self.claim)
        # Re-review's sync emits new citation from claim's head to
        # upstream's head
        self.state.make_link(
            claim_v1, [claim_v1], [upstream_v1],
            "citation.depends",
        )
        # Predicate reads from claim_v1; sees citation to upstream_v1;
        # is_head_version(upstream_v1) = True; fresh.
        self.assertTrue(
            is_cascade_fresh_one_hop(self.session, self.claim)
        )

    def test_two_upstream_one_edited_is_stale(self):
        upstream_b = self.state.create_doc(
            kind="claim", lattice=self.lattice,
        )
        self.state.make_link(
            self.claim, [self.claim], [self.upstream, upstream_b],
            "citation.depends",
        )
        # Edit only upstream_b
        self.state.create_version(upstream_b)
        # Predicate detects upstream_b is no longer head
        self.assertFalse(
            is_cascade_fresh_one_hop(self.session, self.claim)
        )

    def test_claim_edit_alone_does_not_make_stale(self):
        # If claim itself versions but no upstream changes, claim is
        # still fresh. (After claim's register_version, its head is
        # the new version; that head has no citations yet, so the
        # predicate is vacuously True.)
        self.state.make_link(
            self.claim, [self.claim], [self.upstream],
            "citation.depends",
        )
        self.state.create_version(self.claim)
        # Claim's new head has no outgoing citations → vacuously fresh
        self.assertTrue(
            is_cascade_fresh_one_hop(self.session, self.claim)
        )


class TriggerPredicateTests(unittest.TestCase):
    """Combined behavior of cone-review's predicate after the cascade
    additions."""

    def setUp(self):
        self.state = State(account=Address("1.1.0.1"))
        self.session = Session(self.state)
        self.lattice = self.state.create_doc()
        self.claim = self.state.create_doc(
            kind="claim", lattice=self.lattice,
        )
        self.upstream = self.state.create_doc(
            kind="claim", lattice=self.lattice,
        )

    def _predicate(self, addr):
        # Inline replica of triggers/cone_review.py::_predicate
        if not is_upstream_settled_one_hop(self.session, addr):
            return True
        if (
            is_claim_confirmed(self.session, addr)
            and is_cascade_fresh_one_hop(self.session, addr)
        ):
            return True
        if not is_claim_quiescent(self.session, addr):
            return True
        return False

    def test_skips_when_upstream_in_flight(self):
        # Open comment on upstream → predicate returns True (skip)
        self.state.make_link(
            self.claim, [self.claim], [self.upstream], "citation.depends",
        )
        review = self.state.create_doc(
            kind="review.content", lattice=self.lattice,
        )
        self.state.make_link(
            review, [review], [self.upstream], "comment.revise",
        )
        self.assertTrue(self._predicate(self.claim))

    def test_fires_when_upstream_settled_and_never_reviewed(self):
        # Upstream clean, claim never reviewed → fires
        self.state.make_link(
            self.claim, [self.claim], [self.upstream], "citation.depends",
        )
        self.assertFalse(self._predicate(self.claim))

    def test_fires_when_confirmed_but_upstream_edited(self):
        # Claim was reviewed clean (confirmed), but upstream was edited
        # after — cone-review should re-fire to catch the cascade
        self.state.make_link(
            self.claim, [self.claim], [self.upstream], "citation.depends",
        )
        _emit_clean_review(self.state, self.claim, self.lattice)
        # Upstream is edited
        self.state.create_version(self.upstream)
        # Sanity checks
        self.assertTrue(
            is_upstream_settled_one_hop(self.session, self.claim)
        )
        self.assertFalse(
            is_cascade_fresh_one_hop(self.session, self.claim)
        )
        # Predicate returns False (fire) because confirmed-and-fresh
        # is not satisfied (cascade-fresh is False)
        self.assertFalse(self._predicate(self.claim))

    def test_skips_when_confirmed_and_fresh(self):
        # Claim reviewed clean, upstream stable (no edits)
        self.state.make_link(
            self.claim, [self.claim], [self.upstream], "citation.depends",
        )
        _emit_clean_review(self.state, self.claim, self.lattice)
        # Sanity
        self.assertTrue(
            is_upstream_settled_one_hop(self.session, self.claim)
        )
        self.assertTrue(
            is_cascade_fresh_one_hop(self.session, self.claim)
        )
        self.assertTrue(is_claim_confirmed(self.session, self.claim))
        # Skip
        self.assertTrue(self._predicate(self.claim))

    def test_skips_when_open_revise_on_claim(self):
        # Open revise on claim itself → wait for refiner to close it
        self.state.make_link(
            self.claim, [self.claim], [self.upstream], "citation.depends",
        )
        review = self.state.create_doc(
            kind="review.content", lattice=self.lattice,
        )
        self.state.make_link(
            review, [review], [self.claim], "comment.revise",
        )
        # Upstream is settled
        self.assertTrue(
            is_upstream_settled_one_hop(self.session, self.claim)
        )
        # Claim is not quiescent (open revise)
        self.assertFalse(is_claim_quiescent(self.session, self.claim))
        # Predicate skips (will let refiner close first)
        self.assertTrue(self._predicate(self.claim))


if __name__ == "__main__":
    unittest.main()
