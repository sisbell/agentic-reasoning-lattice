"""Allocator and state-creation tests.

Reference: T10a (allocator discipline), T4 (address structure),
ASN-0009 (version semantics, VER-P parentage). Note: State auto-bootstraps
a type-registry doc as the first emission (Gregory's LINK_TYPES_DOC
convention), so user-created docs start at the second slot.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from lib.backend.addressing import Address, inc
from lib.backend.allocator import Allocator
from lib.backend.state import State


class IncTests(unittest.TestCase):
    def test_inc_zero_increments_last_position(self):
        self.assertEqual(inc(Address("1.1.0.1.0.5"), 0), Address("1.1.0.1.0.6"))

    def test_inc_one_appends_single_digit(self):
        self.assertEqual(inc(Address("1.1.0.1.0.5"), 1), Address("1.1.0.1.0.5.1"))

    def test_inc_two_crosses_separator(self):
        self.assertEqual(inc(Address("1.1.0.1"), 2), Address("1.1.0.1.0.1"))

    def test_inc_preserves_length_invariant(self):
        t = Address("1.1.0.1.0.5")
        for k in (0, 1, 2):
            self.assertEqual(len(inc(t, k)), len(t) + k)


class AllocatorTests(unittest.TestCase):
    def test_dense_sibling_stream(self):
        a = Allocator(Address("1.1.0.1.0.1"))
        emitted = [a.emit_sibling() for _ in range(4)]
        self.assertEqual(
            [str(x) for x in emitted],
            ["1.1.0.1.0.1", "1.1.0.1.0.2", "1.1.0.1.0.3", "1.1.0.1.0.4"],
        )

    def test_spawn_child_is_idempotent_per_pair(self):
        a = Allocator(Address("1.1.0.1.0.1"))
        c1 = a.get_or_spawn_child(Address("1.1.0.1.0.1"), 1)
        c2 = a.get_or_spawn_child(Address("1.1.0.1.0.1"), 1)
        self.assertIs(c1, c2)

    def test_distinct_k_prime_yields_distinct_children(self):
        a = Allocator(Address("1.1.0.1"))
        c_one = a.get_or_spawn_child(Address("1.1.0.1"), 1)
        c_two = a.get_or_spawn_child(Address("1.1.0.1"), 2)
        self.assertIsNot(c_one, c_two)
        self.assertEqual(str(c_one.base), "1.1.0.1.1")
        self.assertEqual(str(c_two.base), "1.1.0.1.0.1")

    def test_k_prime_two_rejected_when_zeros_exceeds_two(self):
        a = Allocator(Address("1.1.0.1.0.1.0.1"))
        with self.assertRaises(ValueError):
            a.get_or_spawn_child(Address("1.1.0.1.0.1.0.1"), 2)


class StateCreationTests(unittest.TestCase):
    """Doc creation: shared global allocator; lattice membership is
    a substrate link; version-ancestry is structural per VER3."""

    def setUp(self):
        self.state = State(account=Address("1.1.0.1"))

    def test_registry_doc_takes_first_position(self):
        self.assertEqual(str(self.state.registry_doc), "1.1.0.1.0.1")
        self.assertEqual(self.state.kind[self.state.registry_doc], "type-registry")

    def test_global_allocator_emits_dense_doc_addresses(self):
        # Lattices are docs. Members of a lattice are docs. All share
        # the same allocator stream.
        xanadu = self.state.create_doc()
        materials = self.state.create_doc()
        claim = self.state.create_doc(kind="claim", lattice=xanadu)
        note = self.state.create_doc(kind="note", lattice=xanadu)
        inquiry = self.state.create_doc(kind="inquiry", lattice=materials)

        self.assertEqual(str(xanadu), "1.1.0.1.0.2")
        self.assertEqual(str(materials), "1.1.0.1.0.3")
        self.assertEqual(str(claim), "1.1.0.1.0.4")
        self.assertEqual(str(note), "1.1.0.1.0.5")
        self.assertEqual(str(inquiry), "1.1.0.1.0.6")

    def test_lattice_membership_recovered_via_substrate_link(self):
        xanadu = self.state.create_doc()
        claim = self.state.create_doc(kind="claim", lattice=xanadu)
        # Claim's address does NOT extend xanadu's — flat allocation
        self.assertFalse(claim.has_prefix(xanadu))
        # Membership is in the substrate link, recovered via query
        self.assertEqual(self.state.lattice_of(claim), xanadu)
        self.assertEqual(self.state.lattices_of(claim), [xanadu])
        # The lattice itself isn't a member of anything
        self.assertIsNone(self.state.lattice_of(xanadu))

    def test_multi_lattice_membership(self):
        xanadu = self.state.create_doc()
        foundations = self.state.create_doc()
        shared_claim = self.state.create_doc(kind="claim", lattice=xanadu)
        # Add to a second lattice via direct link emission
        self.state._emit_lattice_link(shared_claim, foundations)
        self.assertEqual(
            set(self.state.lattices_of(shared_claim)),
            {xanadu, foundations},
        )

    def test_versions_extend_source_address_per_ver3(self):
        xanadu = self.state.create_doc()
        claim = self.state.create_doc(kind="claim", lattice=xanadu)
        v1 = self.state.create_version(claim)
        v2 = self.state.create_version(claim)
        v_of_v = self.state.create_version(v1)

        self.assertEqual(str(v1), str(claim) + ".1")
        self.assertEqual(str(v2), str(claim) + ".2")
        self.assertEqual(str(v_of_v), str(v1) + ".1")
        self.assertTrue(v1.has_prefix(claim))
        self.assertTrue(v_of_v.has_prefix(v1))

    def test_version_inherits_lattice_membership(self):
        xanadu = self.state.create_doc()
        claim = self.state.create_doc(kind="claim", lattice=xanadu)
        v1 = self.state.create_version(claim)
        self.assertEqual(self.state.lattice_of(v1), xanadu)
        self.assertEqual(self.state.kind[v1], "claim")

    def test_version_copies_content_per_ver1(self):
        xanadu = self.state.create_doc()
        claim = self.state.create_doc(kind="claim", lattice=xanadu)
        self.state.content[claim] = "original text"
        v1 = self.state.create_version(claim)
        self.assertEqual(self.state.content[v1], "original text")

    def test_classifier_link_emitted_for_catalog_kinds(self):
        xanadu = self.state.create_doc()
        claim = self.state.create_doc(kind="claim", lattice=xanadu)
        # Querying for claim classifier should find it
        results = self.state.find_links(to_set=[claim], type_="claim")
        self.assertEqual(len(results), 1)
        # F=∅ for classifier shape
        self.assertEqual(results[0].from_set, ())

    def test_no_classifier_for_non_catalog_kinds(self):
        # "doc" isn't a catalog classifier kind — no link emitted, just
        # the kind dict cache
        d = self.state.create_doc()  # default kind="doc"
        results = self.state.find_links(to_set=[d])
        # Only links that exist would be lattice links, but we didn't
        # specify a lattice
        self.assertEqual(len(results), 0)
        self.assertEqual(self.state.kind[d], "doc")

    def test_docs_in_lattice_query(self):
        xanadu = self.state.create_doc()
        materials = self.state.create_doc()
        c1 = self.state.create_doc(kind="claim", lattice=xanadu)
        c2 = self.state.create_doc(kind="claim", lattice=xanadu)
        i1 = self.state.create_doc(kind="inquiry", lattice=materials)
        v_of_c1 = self.state.create_version(c1)
        # versions inherit lattice membership (re-emitted lattice link)
        self.assertEqual(set(self.state.docs_in(xanadu)), {c1, c2, v_of_c1})
        self.assertEqual(set(self.state.docs_in(materials)), {i1})

    def test_version_chain_traces_to_canonical_source(self):
        xanadu = self.state.create_doc()
        claim = self.state.create_doc(kind="claim", lattice=xanadu)
        v1 = self.state.create_version(claim)
        v2 = self.state.create_version(v1)
        self.assertEqual(self.state.version_chain(v2), [v1, claim])
        self.assertEqual(self.state.version_chain(claim), [])

    def test_all_emitted_doc_addresses_are_document_kind(self):
        xanadu = self.state.create_doc()
        claim = self.state.create_doc(kind="claim", lattice=xanadu)
        ver = self.state.create_version(claim)
        for addr in (xanadu, claim, ver):
            self.assertEqual(addr.zeros(), 2, f"{addr} should be a document address")

    def test_unknown_doc_address_rejected_for_create_version(self):
        with self.assertRaises(ValueError):
            self.state.create_version(Address("9.9.0.9.0.9"))


if __name__ == "__main__":
    unittest.main()
