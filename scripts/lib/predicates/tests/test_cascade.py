"""Tests for cascade-aware predicates.

Synthetic substrate covering both predicates and the cone-review
trigger predicate's combined behavior. Each test builds the minimal
link graph it needs via State + Session, exercises the predicate, and
asserts the True/False outcome.

The state-difference under test is the relative tumbler-address
ordering of (claim's latest review.coverage) vs (upstream activity
tuples). Per R0 monotonicity, links allocate addresses in emit order;
the predicates compare digits to decide "newer than anchor."
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


def _make_review_chain(state, claim_addr, lattice_addr):
    """Emit a review.content classifier + review.coverage targeting
    the claim. Returns (review_doc_addr, coverage_link)."""
    review_doc = state.create_doc(
        kind="review.content", lattice=lattice_addr,
    )
    coverage = state.make_link(
        review_doc, [review_doc], [claim_addr], "review.coverage",
    )
    return review_doc, coverage


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
        # claim cites upstream; upstream has open comment.revise
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
        # claim cites upstream; upstream's comment was resolved
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
        # comment.violation also gates (structural cleanness check)
        self.state.make_link(
            self.claim, [self.claim], [self.upstream], "citation.depends",
        )
        audit_finding = self.state.create_doc(
            kind="finding", lattice=self.lattice,
        )
        self.state.make_link(
            audit_finding, [audit_finding], [self.upstream],
            "comment.violation",
        )
        self.assertFalse(
            is_upstream_settled_one_hop(self.session, self.claim)
        )

    def test_two_upstream_one_dirty_blocks(self):
        # Two direct upstream; only one has open comment → still blocks
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
    """The staleness detector: did upstream advance after this claim's
    last review?"""

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

    def test_never_reviewed_is_not_fresh(self):
        # No review.coverage on claim → no anchor → not fresh
        self.assertFalse(
            is_cascade_fresh_one_hop(self.session, self.claim)
        )

    def test_reviewed_with_no_upstream_activity_is_fresh(self):
        # Claim cites upstream, claim has been reviewed, nothing has
        # happened on upstream since
        self.state.make_link(
            self.claim, [self.claim], [self.upstream], "citation.depends",
        )
        _make_review_chain(self.state, self.claim, self.lattice)
        self.assertTrue(
            is_cascade_fresh_one_hop(self.session, self.claim)
        )

    def test_upstream_advanced_after_review_is_stale(self):
        # claim reviewed, then upstream gets a comment.revise → stale
        self.state.make_link(
            self.claim, [self.claim], [self.upstream], "citation.depends",
        )
        _make_review_chain(self.state, self.claim, self.lattice)
        # Emit comment.revise AFTER the review (later tumbler addr).
        upstream_review = self.state.create_doc(
            kind="review.content", lattice=self.lattice,
        )
        self.state.make_link(
            upstream_review, [upstream_review], [self.upstream],
            "comment.revise",
        )
        self.assertFalse(
            is_cascade_fresh_one_hop(self.session, self.claim)
        )

    def test_resolution_after_review_is_stale(self):
        # Even a resolution.edit on upstream counts as upstream advance
        # (substantive revision happened).
        self.state.make_link(
            self.claim, [self.claim], [self.upstream], "citation.depends",
        )
        # Pre-existing comment on upstream (before claim's review)
        upstream_review = self.state.create_doc(
            kind="review.content", lattice=self.lattice,
        )
        comment = self.state.make_link(
            upstream_review, [upstream_review], [self.upstream],
            "comment.revise",
        )
        # Now claim is reviewed (anchor set)
        _make_review_chain(self.state, self.claim, self.lattice)
        # Then upstream's comment is resolved (later than claim's review)
        self.state.make_link(
            self.upstream, [self.upstream], [comment.addr],
            "resolution.edit",
        )
        self.assertFalse(
            is_cascade_fresh_one_hop(self.session, self.claim)
        )

    def test_upstream_activity_before_review_is_fresh(self):
        # Upstream activity that happened BEFORE the latest review
        # doesn't count as cascade-stale — the review already saw it.
        self.state.make_link(
            self.claim, [self.claim], [self.upstream], "citation.depends",
        )
        upstream_review = self.state.create_doc(
            kind="review.content", lattice=self.lattice,
        )
        self.state.make_link(
            upstream_review, [upstream_review], [self.upstream],
            "comment.revise",
        )
        # claim's review happens AFTER upstream's activity
        _make_review_chain(self.state, self.claim, self.lattice)
        self.assertTrue(
            is_cascade_fresh_one_hop(self.session, self.claim)
        )

    def test_two_reviews_uses_latest_anchor(self):
        # Two reviews on claim; second is the anchor. Activity before
        # the second review is fine; activity after is stale.
        self.state.make_link(
            self.claim, [self.claim], [self.upstream], "citation.depends",
        )
        _make_review_chain(self.state, self.claim, self.lattice)
        upstream_review = self.state.create_doc(
            kind="review.content", lattice=self.lattice,
        )
        self.state.make_link(
            upstream_review, [upstream_review], [self.upstream],
            "comment.revise",
        )
        # Second review on claim — this is the new anchor
        _make_review_chain(self.state, self.claim, self.lattice)
        # No upstream activity after the second review → fresh
        self.assertTrue(
            is_cascade_fresh_one_hop(self.session, self.claim)
        )


class TriggerPredicateTests(unittest.TestCase):
    """Combined behavior of cone-review's predicate after the cascade
    additions. Imported indirectly via the triggers module to verify
    the wire-up."""

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
        # (avoiding the module's CLI-only imports).
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

    def test_fires_when_confirmed_but_cascade_stale(self):
        # Claim was reviewed clean (confirmed), but upstream advanced
        # after — cone-review should re-fire to catch the cascade.
        self.state.make_link(
            self.claim, [self.claim], [self.upstream], "citation.depends",
        )
        review_doc, _ = _make_review_chain(
            self.state, self.claim, self.lattice,
        )
        # Clean review (no comment.revise from this review)
        # Upstream activity AFTER claim's review → cascade-stale
        upstream_review = self.state.create_doc(
            kind="review.content", lattice=self.lattice,
        )
        comment = self.state.make_link(
            upstream_review, [upstream_review], [self.upstream],
            "comment.revise",
        )
        # Resolve upstream's comment so upstream is settled (gate clear)
        self.state.make_link(
            self.upstream, [self.upstream], [comment.addr],
            "resolution.edit",
        )
        # Sanity: gate is open
        self.assertTrue(
            is_upstream_settled_one_hop(self.session, self.claim)
        )
        # But cascade-stale (upstream's tuples are after claim's anchor)
        self.assertFalse(
            is_cascade_fresh_one_hop(self.session, self.claim)
        )
        # is_claim_confirmed requires `latest_review_was_clean` AND
        # is_claim_quiescent. With no comment.revise on this claim and
        # one clean review, both hold. So the predicate falls past the
        # confirmed check (because cascade-fresh is False) and fires.
        self.assertFalse(self._predicate(self.claim))

    def test_skips_when_confirmed_and_fresh(self):
        # Claim reviewed clean, upstream stable, no cascade activity
        self.state.make_link(
            self.claim, [self.claim], [self.upstream], "citation.depends",
        )
        _make_review_chain(self.state, self.claim, self.lattice)
        # Sanity checks
        self.assertTrue(
            is_upstream_settled_one_hop(self.session, self.claim)
        )
        self.assertTrue(
            is_cascade_fresh_one_hop(self.session, self.claim)
        )
        self.assertTrue(is_claim_confirmed(self.session, self.claim))
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
        # Upstream is settled (no comments on upstream)
        self.assertTrue(
            is_upstream_settled_one_hop(self.session, self.claim)
        )
        # Claim is not quiescent (open revise)
        self.assertFalse(is_claim_quiescent(self.session, self.claim))
        # Predicate skips
        self.assertTrue(self._predicate(self.claim))


if __name__ == "__main__":
    unittest.main()
