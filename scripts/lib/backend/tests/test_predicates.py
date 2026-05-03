"""Substrate-predicate tests over the tumbler-keyed link store.

Verifies the convergence and alignment predicates ported from the
legacy queries.py, plus the new alignment helpers enabled by
version-bearing addresses.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from lib.backend.addressing import Address
from lib.backend.predicates import (
    active_links,
    all_claim_addrs,
    all_classified,
    dependents,
    depends,
    description_sidecar_of,
    has_description,
    has_label,
    has_name,
    has_resolution,
    has_signature,
    is_converged,
    is_doc_converged,
    is_head_version,
    retracted_link_addrs,
    unresolved_revise_comments,
    version_children,
    version_head,
)
from lib.backend.state import State


class ConvergencePredicateTests(unittest.TestCase):
    """The protocol predicate over comment.revise + resolution + retraction."""

    def setUp(self):
        self.state = State(account=Address("1.1.0.1"))
        self.lattice = self.state.create_doc()
        self.claim = self.state.create_doc(kind="claim", lattice=self.lattice)
        self.review = self.state.create_doc(kind="review", lattice=self.lattice)

    def test_empty_substrate_is_converged(self):
        # No comment.revise links → vacuously converged
        self.assertTrue(is_converged(self.state))
        self.assertTrue(is_doc_converged(self.state, self.claim))

    def test_unresolved_revise_blocks_convergence(self):
        comment = self.state.make_link(
            self.review, [self.review], [self.claim], "comment.revise",
        )
        self.assertFalse(is_doc_converged(self.state, self.claim))
        unresolved = unresolved_revise_comments(self.state, self.claim)
        self.assertEqual([c.addr for c in unresolved], [comment.addr])

    def test_resolution_satisfies_convergence(self):
        comment = self.state.make_link(
            self.review, [self.review], [self.claim], "comment.revise",
        )
        # Substrate convention: F=claim (revised doc), G=comment_addr
        self.state.make_link(
            self.claim, [self.claim], [comment.addr], "resolution.edit",
        )
        self.assertTrue(is_doc_converged(self.state, self.claim))
        self.assertTrue(has_resolution(self.state, comment.addr))

    def test_retracted_revise_drops_out(self):
        comment = self.state.make_link(
            self.review, [self.review], [self.claim], "comment.revise",
        )
        # Retract the comment — it no longer counts
        self.state.make_link(
            self.claim, [self.claim], [comment.addr], "retraction",
        )
        self.assertTrue(is_doc_converged(self.state, self.claim))

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
        self.assertFalse(is_doc_converged(self.state, self.claim))

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
        self.lattice = self.state.create_doc()

    def test_all_claim_addrs(self):
        c1 = self.state.create_doc(kind="claim", lattice=self.lattice)
        c2 = self.state.create_doc(kind="claim", lattice=self.lattice)
        self.state.create_doc(kind="note", lattice=self.lattice)
        addrs = all_claim_addrs(self.state)
        self.assertEqual(set(addrs), {c1, c2})

    def test_all_classified_filters_by_kind(self):
        c = self.state.create_doc(kind="claim", lattice=self.lattice)
        n = self.state.create_doc(kind="note", lattice=self.lattice)
        self.assertEqual(all_classified(self.state, "claim"), [c])
        self.assertEqual(all_classified(self.state, "note"), [n])


class AlignmentPredicateTests(unittest.TestCase):
    """Description, signature, name, label — all attribute links."""

    def setUp(self):
        self.state = State(account=Address("1.1.0.1"))
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
        self.assertTrue(has_description(self.state, self.claim_v1))
        self.assertEqual(
            description_sidecar_of(self.state, self.claim_v1),
            self.desc_sidecar,
        )

    def test_v2_lacks_description_until_authored(self):
        # Claim revises — VER3 child address; the description link from v1
        # still pins to v1, so v2 is not described.
        v2 = self.state.create_version(self.claim_v1)
        self.assertFalse(has_description(self.state, v2))
        self.assertIsNone(description_sidecar_of(self.state, v2))

    def test_re_authoring_restores_alignment(self):
        v2 = self.state.create_version(self.claim_v1)
        self.state.make_link(v2, [v2], [self.desc_sidecar], "description")
        self.assertTrue(has_description(self.state, v2))

    def test_retracting_description_clears_predicate(self):
        link = active_links(
            self.state, "description", from_set=[self.claim_v1]
        )[0]
        self.state.make_link(
            self.claim_v1, [self.claim_v1], [link.addr], "retraction",
        )
        self.assertFalse(has_description(self.state, self.claim_v1))

    def test_name_and_label_predicates(self):
        name_sidecar = self.state.create_doc(lattice=self.lattice)
        label_sidecar = self.state.create_doc(lattice=self.lattice)
        self.state.make_link(
            self.claim_v1, [self.claim_v1], [name_sidecar], "name",
        )
        self.state.make_link(
            self.claim_v1, [self.claim_v1], [label_sidecar], "label",
        )
        self.assertTrue(has_name(self.state, self.claim_v1))
        self.assertTrue(has_label(self.state, self.claim_v1))

    def test_has_signature_when_emitted(self):
        sig_sidecar = self.state.create_doc(lattice=self.lattice)
        self.state.make_link(
            self.claim_v1, [self.claim_v1], [sig_sidecar], "signature",
        )
        self.assertTrue(has_signature(self.state, self.claim_v1))


class VersionChainTests(unittest.TestCase):
    def setUp(self):
        self.state = State(account=Address("1.1.0.1"))
        self.lattice = self.state.create_doc()
        self.claim = self.state.create_doc(kind="claim", lattice=self.lattice)

    def test_no_versions_means_self_is_head(self):
        self.assertTrue(is_head_version(self.state, self.claim))
        self.assertEqual(version_head(self.state, self.claim), self.claim)

    def test_version_chain_walks_forward(self):
        v1 = self.state.create_version(self.claim)
        v2 = self.state.create_version(self.claim)
        v3 = self.state.create_version(self.claim)
        # version_children returns sorted siblings of the canonical claim
        self.assertEqual(version_children(self.state, self.claim), [v1, v2, v3])
        self.assertFalse(is_head_version(self.state, self.claim))
        self.assertEqual(version_head(self.state, self.claim), v3)
        self.assertTrue(is_head_version(self.state, v3))

    def test_nested_versions_walk_deepest_chain(self):
        v1 = self.state.create_version(self.claim)
        v1_v1 = self.state.create_version(v1)
        # head from canonical: v1's chain is now deeper than the (empty) chain
        # at the top level. version_head picks highest sibling at each level.
        # Top level has only v1, so descend into v1; v1's head is v1_v1.
        self.assertEqual(version_head(self.state, self.claim), v1_v1)


class CitationGraphTests(unittest.TestCase):
    def setUp(self):
        self.state = State(account=Address("1.1.0.1"))
        self.lattice = self.state.create_doc()
        self.a = self.state.create_doc(kind="claim", lattice=self.lattice)
        self.b = self.state.create_doc(kind="claim", lattice=self.lattice)
        self.c = self.state.create_doc(kind="claim", lattice=self.lattice)

    def test_depends_recovers_outgoing_dependencies(self):
        self.state.make_link(self.a, [self.a], [self.b], "citation.depends")
        self.state.make_link(self.a, [self.a], [self.c], "citation.depends")
        self.assertEqual(set(depends(self.state, self.a)), {self.b, self.c})
        self.assertEqual(depends(self.state, self.b), [])

    def test_dependents_recovers_incoming(self):
        self.state.make_link(self.a, [self.a], [self.b], "citation.depends")
        self.state.make_link(self.c, [self.c], [self.b], "citation.depends")
        self.assertEqual(set(dependents(self.state, self.b)), {self.a, self.c})

    def test_retracted_citation_drops_from_graph(self):
        link = self.state.make_link(
            self.a, [self.a], [self.b], "citation.depends",
        )
        self.state.make_link(
            self.a, [self.a], [link.addr], "retraction",
        )
        self.assertEqual(depends(self.state, self.a), [])
        self.assertEqual(dependents(self.state, self.b), [])


if __name__ == "__main__":
    unittest.main()
