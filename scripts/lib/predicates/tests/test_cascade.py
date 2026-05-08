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
    claims_statements_for_note,
    description_is_fresh_after_asn_confirmation,
    is_cascade_fresh_one_hop,
    is_claim_confirmed,
    is_claim_quiescent,
    is_claims_statements_fresh,
    is_upstream_settled_one_hop,
    signature_is_fresh_after_asn_confirmation,
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


def _advance_chain(state, addr):
    """Simulate Store.register_version on State-only tests: walk to chain
    head, allocate a child, emit supersession from head to it.

    Mirrors `Store.register_version`'s walk-to-head-then-allocate
    behavior — the chain stays linear, so `supersession_chain_length`
    grows monotonically with each call.
    """
    head = addr
    while True:
        children = sorted(
            (a for a, p in state.parent.items() if p == head),
            key=lambda a: a.digits,
        )
        if not children:
            break
        head = children[-1]
    new_addr = state.create_version(head)
    state.make_link(head, [head], [new_addr], "supersession")
    return new_addr


class ClaimsStatementsForNoteTests(unittest.TestCase):
    """Resolve the aggregate doc derived from a note via classifier walk."""

    def setUp(self):
        self.state = State(account=Address("1.1.0.1"))
        self.session = Session(self.state)
        self.lattice = self.state.create_doc()
        self.note = self.state.create_doc(kind="note", lattice=self.lattice)

    def test_no_aggregate_returns_none(self):
        self.assertIsNone(claims_statements_for_note(self.session, self.note))

    def test_finds_aggregate_via_derivation(self):
        agg = self.state.create_doc(
            kind="claims.statements", lattice=self.lattice,
        )
        self.state.make_link(
            self.note, [self.note], [agg], "provenance.derivation",
        )
        self.assertEqual(
            claims_statements_for_note(self.session, self.note), agg,
        )

    def test_skips_non_aggregate_derivations(self):
        # Note derives several docs; only the one with claims.statements
        # classifier is the aggregate.
        plain_claim = self.state.create_doc(
            kind="claim", lattice=self.lattice,
        )
        self.state.make_link(
            self.note, [self.note], [plain_claim], "provenance.derivation",
        )
        agg = self.state.create_doc(
            kind="claims.statements", lattice=self.lattice,
        )
        self.state.make_link(
            self.note, [self.note], [agg], "provenance.derivation",
        )
        self.assertEqual(
            claims_statements_for_note(self.session, self.note), agg,
        )


class ClaimsStatementsFreshTests(unittest.TestCase):
    """Aggregate freshness gates on is_asn_confirmed and chain trailing."""

    def setUp(self):
        self.state = State(account=Address("1.1.0.1"))
        self.session = Session(self.state)
        self.lattice = self.state.create_doc()
        self.note = self.state.create_doc(kind="note", lattice=self.lattice)
        self.c1 = self.state.create_doc(kind="claim", lattice=self.lattice)
        self.c2 = self.state.create_doc(kind="claim", lattice=self.lattice)
        self.state.make_link(
            self.note, [self.note], [self.c1], "provenance.derivation",
        )
        self.state.make_link(
            self.note, [self.note], [self.c2], "provenance.derivation",
        )
        self.agg = self.state.create_doc(
            kind="claims.statements", lattice=self.lattice,
        )
        self.state.make_link(
            self.note, [self.note], [self.agg], "provenance.derivation",
        )

    def _confirm_all_claims(self):
        """Make is_asn_confirmed True by emitting a clean review on each
        derived claim. Aggregate (kind=claims.statements) does not have
        a `claim` classifier so is_asn_confirmed iterates only c1, c2."""
        _emit_clean_review(self.state, self.c1, self.lattice)
        _emit_clean_review(self.state, self.c2, self.lattice)

    def test_unconfirmed_asn_is_vacuously_fresh(self):
        # Gate closed — predicate returns True regardless of chain state
        _advance_chain(self.state, self.c1)
        self.assertTrue(
            is_claims_statements_fresh(self.session, self.note),
        )

    def test_no_aggregate_with_confirmed_claims_fires_to_create(self):
        # Confirmed claims AND no aggregate → predicate returns False
        # (fire). The agent's first fire creates the aggregate. This is
        # the discovery → claim transition case.
        bare_note = self.state.create_doc(kind="note", lattice=self.lattice)
        bare_c = self.state.create_doc(kind="claim", lattice=self.lattice)
        self.state.make_link(
            bare_note, [bare_note], [bare_c], "provenance.derivation",
        )
        _emit_clean_review(self.state, bare_c, self.lattice)
        self.assertFalse(
            is_claims_statements_fresh(self.session, bare_note),
        )

    def test_no_claims_is_vacuously_fresh(self):
        # Note with no claim-classified derivations → True (no
        # aggregate to maintain)
        bare_note = self.state.create_doc(kind="note", lattice=self.lattice)
        self.assertTrue(
            is_claims_statements_fresh(self.session, bare_note),
        )

    def test_confirmed_with_matching_chain_is_fresh(self):
        # All claim chains length 1, aggregate chain length 1
        self._confirm_all_claims()
        self.assertTrue(
            is_claims_statements_fresh(self.session, self.note),
        )

    def test_confirmed_with_advanced_claim_is_stale(self):
        # c1 chain = 2, aggregate chain = 1 → stale
        self._confirm_all_claims()
        _advance_chain(self.state, self.c1)
        self.assertFalse(
            is_claims_statements_fresh(self.session, self.note),
        )

    def test_one_advance_catches_up(self):
        # After register_version on aggregate, predicate flips True
        self._confirm_all_claims()
        _advance_chain(self.state, self.c1)
        self.assertFalse(
            is_claims_statements_fresh(self.session, self.note),
        )
        _advance_chain(self.state, self.agg)
        self.assertTrue(
            is_claims_statements_fresh(self.session, self.note),
        )

    def test_aggregate_must_match_max_claim_chain(self):
        # c1 chain = 3, c2 chain = 1, aggregate chain = 2 → stale (still
        # below max). One more advance catches up.
        self._confirm_all_claims()
        _advance_chain(self.state, self.c1)
        _advance_chain(self.state, self.c1)
        _advance_chain(self.state, self.agg)
        self.assertFalse(
            is_claims_statements_fresh(self.session, self.note),
        )
        _advance_chain(self.state, self.agg)
        self.assertTrue(
            is_claims_statements_fresh(self.session, self.note),
        )


class SidecarAgainstClaimHeadTests(unittest.TestCase):
    """description_is_fresh_after_asn_confirmation +
    signature_is_fresh_after_asn_confirmation walk a citation from
    sidecar head → claim head; predicate flips False when the claim
    revises past the cited version.
    """

    def setUp(self):
        self.state = State(account=Address("1.1.0.1"))
        self.session = Session(self.state)
        self.lattice = self.state.create_doc()
        self.note = self.state.create_doc(kind="note", lattice=self.lattice)
        self.claim = self.state.create_doc(kind="claim", lattice=self.lattice)
        self.state.make_link(
            self.note, [self.note], [self.claim], "provenance.derivation",
        )

    def _confirm_claim(self):
        _emit_clean_review(self.state, self.claim, self.lattice)

    def _attach_sidecar(self, kind, cite_target=None):
        """Create a sidecar via attribute link, optionally cite a claim
        version (the freshness anchor)."""
        sidecar = self.state.create_doc(lattice=self.lattice)
        self.state.make_link(
            self.claim, [self.claim], [sidecar], kind,
        )
        if cite_target is not None:
            self.state.make_link(
                sidecar, [sidecar], [cite_target], "citation.depends",
            )
        return sidecar

    def test_unconfirmed_asn_skips_description(self):
        # ASN not confirmed → predicate True (skip), regardless of
        # sidecar state
        self.assertTrue(
            description_is_fresh_after_asn_confirmation(
                self.session, self.claim,
            ),
        )

    def test_no_sidecar_fires_to_create(self):
        # Confirmed AND no sidecar yet → predicate False (fire)
        self._confirm_claim()
        self.assertFalse(
            description_is_fresh_after_asn_confirmation(
                self.session, self.claim,
            ),
        )

    def test_sidecar_cites_current_head_is_fresh(self):
        # Sidecar's citation targets claim head → predicate True (skip)
        self._confirm_claim()
        self._attach_sidecar("description", cite_target=self.claim)
        self.assertTrue(
            description_is_fresh_after_asn_confirmation(
                self.session, self.claim,
            ),
        )

    def test_claim_revised_past_cited_version_is_stale(self):
        # Sidecar cites claim_v0; claim revises (v1); cited address is
        # no longer head → predicate False (fire)
        self._confirm_claim()
        self._attach_sidecar("description", cite_target=self.claim)
        self.state.create_version(self.claim)
        self.assertFalse(
            description_is_fresh_after_asn_confirmation(
                self.session, self.claim,
            ),
        )

    def test_signature_uses_same_shape(self):
        # Same predicate logic for signature, keyed on the signature
        # attribute link
        self._confirm_claim()
        self._attach_sidecar("signature", cite_target=self.claim)
        self.assertTrue(
            signature_is_fresh_after_asn_confirmation(
                self.session, self.claim,
            ),
        )
        self.state.create_version(self.claim)
        self.assertFalse(
            signature_is_fresh_after_asn_confirmation(
                self.session, self.claim,
            ),
        )


if __name__ == "__main__":
    unittest.main()
