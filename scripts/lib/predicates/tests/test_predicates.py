"""Predicate tests over the tumbler-keyed link store.

Verifies the convergence and alignment predicates, plus the alignment
helpers enabled by version-bearing addresses.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from lib.backend.addressing import Address
from lib.backend.predicates import active_links, retracted_link_addrs
from lib.backend.state import State
from lib.protocols.febe.session import Session
from lib.predicates import (
    all_claim_addrs,
    all_classified,
    dependents,
    depends,
    description_sidecar_of,
    has_been_reviewed,
    has_description,
    has_label,
    has_name,
    has_resolution,
    has_signature,
    is_claim_confirmed,
    is_converged,
    is_doc_converged,
    is_head_version,
    latest_review_for_addr,
    latest_review_was_clean,
    unresolved_revise_comments,
    version_children,
    version_head,
)


class ConvergencePredicateTests(unittest.TestCase):
    """The protocol predicate over comment.revise + resolution + retraction."""

    def setUp(self):
        self.state = State(account=Address("1.1.0.1"))
        self.session = Session(self.state)
        self.lattice = self.state.create_doc()
        self.claim = self.state.create_doc(kind="claim", lattice=self.lattice)
        self.review = self.state.create_doc(kind="review", lattice=self.lattice)

    def test_empty_substrate_is_converged(self):
        # No comment.revise links → vacuously converged
        self.assertTrue(is_converged(self.session))
        self.assertTrue(is_doc_converged(self.session, self.claim))

    def test_unresolved_revise_blocks_convergence(self):
        comment = self.state.make_link(
            self.review, [self.review], [self.claim], "comment.revise",
        )
        self.assertFalse(is_doc_converged(self.session, self.claim))
        unresolved = unresolved_revise_comments(self.session, self.claim)
        self.assertEqual([c.addr for c in unresolved], [comment.addr])

    def test_resolution_satisfies_convergence(self):
        comment = self.state.make_link(
            self.review, [self.review], [self.claim], "comment.revise",
        )
        # Substrate convention: F=claim (revised doc), G=comment_addr
        self.state.make_link(
            self.claim, [self.claim], [comment.addr], "resolution.edit",
        )
        self.assertTrue(is_doc_converged(self.session, self.claim))
        self.assertTrue(has_resolution(self.session, comment.addr))

    def test_retracted_revise_drops_out(self):
        comment = self.state.make_link(
            self.review, [self.review], [self.claim], "comment.revise",
        )
        # Retract the comment — it no longer counts
        self.state.make_link(
            self.claim, [self.claim], [comment.addr], "retraction",
        )
        self.assertTrue(is_doc_converged(self.session, self.claim))

    def test_retracted_resolution_does_not_satisfy(self):
        comment = self.state.make_link(
            self.review, [self.review], [self.claim], "comment.revise",
        )
        resolution = self.state.make_link(
            self.claim, [self.claim], [comment.addr], "resolution.edit",
        )
        self.state.make_link(
            self.claim, [self.claim], [resolution.addr], "retraction",
        )
        # Without the resolution, the revise is unresolved again
        self.assertFalse(is_doc_converged(self.session, self.claim))

    def test_retracted_link_addrs_collects_targets(self):
        comment = self.state.make_link(
            self.review, [self.review], [self.claim], "comment.revise",
        )
        self.state.make_link(
            self.claim, [self.claim], [comment.addr], "retraction",
        )
        self.assertIn(comment.addr, retracted_link_addrs(self.state))

    def test_active_links_excludes_retracted(self):
        comment = self.state.make_link(
            self.review, [self.review], [self.claim], "comment.revise",
        )
        self.state.make_link(
            self.claim, [self.claim], [comment.addr], "retraction",
        )
        actives = active_links(self.state, "comment.revise", to_set=[self.claim])
        self.assertEqual(actives, [])


class ClassifierEnumerationTests(unittest.TestCase):
    def setUp(self):
        self.state = State(account=Address("1.1.0.1"))
        self.session = Session(self.state)
        self.lattice = self.state.create_doc()

    def test_all_claim_addrs(self):
        c1 = self.state.create_doc(kind="claim", lattice=self.lattice)
        c2 = self.state.create_doc(kind="claim", lattice=self.lattice)
        self.state.create_doc(kind="note", lattice=self.lattice)
        addrs = all_claim_addrs(self.session)
        self.assertEqual(set(addrs), {c1, c2})

    def test_all_classified_filters_by_kind(self):
        c = self.state.create_doc(kind="claim", lattice=self.lattice)
        n = self.state.create_doc(kind="note", lattice=self.lattice)
        self.assertEqual(all_classified(self.session, "claim"), [c])
        self.assertEqual(all_classified(self.session, "note"), [n])


class AlignmentPredicateTests(unittest.TestCase):
    """Description, signature, name, label — all attribute links."""

    def setUp(self):
        self.state = State(account=Address("1.1.0.1"))
        self.session = Session(self.state)
        self.lattice = self.state.create_doc()
        self.claim_v1 = self.state.create_doc(kind="claim", lattice=self.lattice)
        self.desc_sidecar = self.state.create_doc(lattice=self.lattice)
        self.state.make_link(
            self.claim_v1,
            [self.claim_v1],
            [self.desc_sidecar],
            "description",
        )

    def test_v1_has_description(self):
        self.assertTrue(has_description(self.session, self.claim_v1))
        self.assertEqual(
            description_sidecar_of(self.session, self.claim_v1),
            self.desc_sidecar,
        )

    def test_v2_lacks_description_until_authored(self):
        # Claim revises — VER3 child address; the description link from v1
        # still pins to v1, so v2 is not described.
        v2 = self.state.create_version(self.claim_v1)
        self.assertFalse(has_description(self.session, v2))
        self.assertIsNone(description_sidecar_of(self.session, v2))

    def test_re_authoring_restores_alignment(self):
        v2 = self.state.create_version(self.claim_v1)
        self.state.make_link(v2, [v2], [self.desc_sidecar], "description")
        self.assertTrue(has_description(self.session, v2))

    def test_retracting_description_clears_predicate(self):
        link = self.session.active_links(
            "description", from_set=[self.claim_v1]
        )[0]
        self.state.make_link(
            self.claim_v1, [self.claim_v1], [link.addr], "retraction",
        )
        self.assertFalse(has_description(self.session, self.claim_v1))

    def test_name_and_label_predicates(self):
        name_sidecar = self.state.create_doc(lattice=self.lattice)
        label_sidecar = self.state.create_doc(lattice=self.lattice)
        self.state.make_link(
            self.claim_v1, [self.claim_v1], [name_sidecar], "name",
        )
        self.state.make_link(
            self.claim_v1, [self.claim_v1], [label_sidecar], "label",
        )
        self.assertTrue(has_name(self.session, self.claim_v1))
        self.assertTrue(has_label(self.session, self.claim_v1))

    def test_has_signature_when_emitted(self):
        sig_sidecar = self.state.create_doc(lattice=self.lattice)
        self.state.make_link(
            self.claim_v1, [self.claim_v1], [sig_sidecar], "signature",
        )
        self.assertTrue(has_signature(self.session, self.claim_v1))


class VersionChainTests(unittest.TestCase):
    def setUp(self):
        self.state = State(account=Address("1.1.0.1"))
        self.session = Session(self.state)
        self.lattice = self.state.create_doc()
        self.claim = self.state.create_doc(kind="claim", lattice=self.lattice)

    def test_no_versions_means_self_is_head(self):
        self.assertTrue(is_head_version(self.session, self.claim))
        self.assertEqual(version_head(self.session, self.claim), self.claim)

    def test_version_chain_walks_forward(self):
        v1 = self.state.create_version(self.claim)
        v2 = self.state.create_version(self.claim)
        v3 = self.state.create_version(self.claim)
        # version_children returns sorted siblings of the canonical claim
        self.assertEqual(
            version_children(self.session, self.claim), [v1, v2, v3],
        )
        self.assertFalse(is_head_version(self.session, self.claim))
        self.assertEqual(version_head(self.session, self.claim), v3)
        self.assertTrue(is_head_version(self.session, v3))

    def test_nested_versions_walk_deepest_chain(self):
        v1 = self.state.create_version(self.claim)
        v1_v1 = self.state.create_version(v1)
        # head from canonical: v1's chain is now deeper than the (empty) chain
        # at the top level. version_head picks highest sibling at each level.
        # Top level has only v1, so descend into v1; v1's head is v1_v1.
        self.assertEqual(version_head(self.session, self.claim), v1_v1)


class RetiredLifecycleTests(unittest.TestCase):
    """Lifecycle marker via standalone `retired` link."""

    def setUp(self):
        self.state = State(account=Address("1.1.0.1"))
        self.session = Session(self.state)
        self.lattice = self.state.create_doc()
        self.note = self.state.create_doc(kind="note", lattice=self.lattice)

    def test_default_is_active(self):
        from lib.predicates import is_retired
        self.assertFalse(is_retired(self.session, self.note))

    def test_retired_link_marks_retired(self):
        from lib.predicates import is_retired
        self.state.make_link(
            self.note, [], [self.note], "retired",
        )
        self.assertTrue(is_retired(self.session, self.note))

    def test_retracting_retired_revives(self):
        from lib.predicates import is_retired
        retired_link = self.state.make_link(
            self.note, [], [self.note], "retired",
        )
        # Retracting the retired link revives — predicate goes False.
        self.state.make_link(
            self.note, [self.note], [retired_link.addr], "retraction",
        )
        self.assertFalse(is_retired(self.session, self.note))


class SupersessionChainTests(unittest.TestCase):
    """Walk supersession links to find a doc's head version."""

    def setUp(self):
        self.state = State(account=Address("1.1.0.1"))
        self.session = Session(self.state)
        self.lattice = self.state.create_doc()
        self.v1 = self.state.create_doc(kind="claim", lattice=self.lattice)
        self.v2 = self.state.create_doc(kind="claim", lattice=self.lattice)
        self.v3 = self.state.create_doc(kind="claim", lattice=self.lattice)

    def _supersede(self, old, new):
        return self.state.make_link(
            new, [old], [new], "supersession",
        )

    def test_no_supersession_means_self_is_head(self):
        from lib.predicates import supersession_head
        self.assertEqual(supersession_head(self.session, self.v1), self.v1)

    def test_single_link_resolves_to_successor(self):
        from lib.predicates import supersession_head
        self._supersede(self.v1, self.v2)
        self.assertEqual(supersession_head(self.session, self.v1), self.v2)
        self.assertEqual(supersession_head(self.session, self.v2), self.v2)

    def test_chain_walks_to_deepest(self):
        from lib.predicates import supersession_head
        self._supersede(self.v1, self.v2)
        self._supersede(self.v2, self.v3)
        self.assertEqual(supersession_head(self.session, self.v1), self.v3)
        self.assertEqual(supersession_head(self.session, self.v2), self.v3)

    def test_retracted_supersession_drops_from_walk(self):
        from lib.predicates import supersession_head
        link = self._supersede(self.v1, self.v2)
        self.state.make_link(
            self.v1, [self.v1], [link.addr], "retraction",
        )
        # Retracted: v1's outgoing supersession is gone, head is v1.
        self.assertEqual(supersession_head(self.session, self.v1), self.v1)


class CitationGraphTests(unittest.TestCase):
    def setUp(self):
        self.state = State(account=Address("1.1.0.1"))
        self.session = Session(self.state)
        self.lattice = self.state.create_doc()
        self.a = self.state.create_doc(kind="claim", lattice=self.lattice)
        self.b = self.state.create_doc(kind="claim", lattice=self.lattice)
        self.c = self.state.create_doc(kind="claim", lattice=self.lattice)

    def test_depends_recovers_outgoing_dependencies(self):
        self.state.make_link(self.a, [self.a], [self.b], "citation.depends")
        self.state.make_link(self.a, [self.a], [self.c], "citation.depends")
        self.assertEqual(set(depends(self.session, self.a)), {self.b, self.c})
        self.assertEqual(depends(self.session, self.b), [])

    def test_dependents_recovers_incoming(self):
        self.state.make_link(self.a, [self.a], [self.b], "citation.depends")
        self.state.make_link(self.c, [self.c], [self.b], "citation.depends")
        self.assertEqual(
            set(dependents(self.session, self.b)), {self.a, self.c},
        )

    def test_retracted_citation_drops_from_graph(self):
        link = self.state.make_link(
            self.a, [self.a], [self.b], "citation.depends",
        )
        self.state.make_link(
            self.a, [self.a], [link.addr], "retraction",
        )
        self.assertEqual(depends(self.session, self.a), [])
        self.assertEqual(dependents(self.session, self.b), [])


class ConfirmationPredicateTests(unittest.TestCase):
    """Confirmation predicate: is_converged AND latest review was clean.

    Requires `review.coverage` links to find the latest review on a doc's
    scope, and `provenance.derivation` walks to count revise findings.
    """

    def setUp(self):
        self.state = State(account=Address("1.1.0.1"))
        self.session = Session(self.state)
        self.lattice = self.state.create_doc()
        self.claim = self.state.create_doc(kind="claim", lattice=self.lattice)

    def _make_review(self, finding_kinds=()):
        """Create a review meta + review.coverage → claim, plus a finding
        per `finding_kinds` entry. Each kind is "revise" or "observe";
        emits provenance.derivation from review and comment.<kind> from
        finding to claim. Returns the review meta address.
        """
        review_meta = self.state.create_doc(
            kind="review", lattice=self.lattice,
        )
        self.state.make_link(
            review_meta, [review_meta], [self.claim], "review.coverage",
        )
        for kind in finding_kinds:
            finding = self.state.create_doc(
                kind="finding", lattice=self.lattice,
            )
            self.state.make_link(
                review_meta, [review_meta], [finding],
                "provenance.derivation",
            )
            self.state.make_link(
                finding, [finding], [self.claim], f"comment.{kind}",
            )
        return review_meta

    def test_unreviewed_claim_not_confirmed(self):
        self.assertFalse(has_been_reviewed(self.session, self.claim))
        self.assertIsNone(
            latest_review_for_addr(self.session, self.claim),
        )
        self.assertFalse(is_claim_confirmed(self.session, self.claim))

    def test_clean_review_confirms_claim(self):
        self._make_review(finding_kinds=())  # zero findings
        self.assertTrue(has_been_reviewed(self.session, self.claim))
        self.assertTrue(latest_review_was_clean(self.session, self.claim))
        self.assertTrue(is_claim_confirmed(self.session, self.claim))

    def test_observe_only_review_is_clean(self):
        # comment.observe doesn't block convergence or confirmation.
        self._make_review(finding_kinds=("observe",))
        self.assertTrue(latest_review_was_clean(self.session, self.claim))
        self.assertTrue(is_claim_confirmed(self.session, self.claim))

    def test_review_with_unresolved_revise_does_not_confirm(self):
        self._make_review(finding_kinds=("revise",))
        self.assertFalse(latest_review_was_clean(self.session, self.claim))
        self.assertFalse(is_claim_confirmed(self.session, self.claim))

    def test_latest_review_supersedes_older(self):
        # Older review had revises; newer review came up clean.
        # The older review's revise comment is resolved before the
        # new clean review fires, so is_converged is true again.
        old = self._make_review(finding_kinds=("revise",))
        # resolve the old revise so converged becomes true
        old_revise = self.session.active_links(
            "comment.revise", to_set=[self.claim],
        )[0]
        self.state.make_link(
            self.claim, [self.claim], [old_revise.addr], "resolution.edit",
        )
        # now a clean review covers the claim
        new = self._make_review(finding_kinds=())
        self.assertEqual(
            latest_review_for_addr(self.session, self.claim), new,
        )
        self.assertTrue(latest_review_was_clean(self.session, self.claim))
        self.assertTrue(is_claim_confirmed(self.session, self.claim))

    def test_clean_review_but_unresolved_revise_blocks_confirmation(self):
        # A different un-related revise comment exists on the claim;
        # the latest review was clean but converged is still false.
        self._make_review(finding_kinds=())  # clean
        # add a stray revise from something else (not derived from the
        # latest review) — this can't happen via our agents but the
        # predicate must compose correctly anyway.
        other_finding = self.state.create_doc(
            kind="finding", lattice=self.lattice,
        )
        self.state.make_link(
            other_finding, [other_finding], [self.claim], "comment.revise",
        )
        self.assertTrue(latest_review_was_clean(self.session, self.claim))
        self.assertFalse(is_doc_converged(self.session, self.claim))
        self.assertFalse(is_claim_confirmed(self.session, self.claim))


if __name__ == "__main__":
    unittest.main()
