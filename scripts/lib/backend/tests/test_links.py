"""Link store + canonical type registry: MAKELINK + FINDLINKS.

Per ASN-0043 L8 (TypeByAddress): every link's type_set holds tumbler
addresses pointing into the type-registry doc. L10
(TypeHierarchyByContainment): subtype hierarchies are recovered by
prefix-matching on type addresses — query at parent matches all
subtypes.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from lib.backend.addressing import Address
from lib.backend.links import LinkStore
from lib.backend.state import State, link_subspace_base
from lib.backend.types import CANONICAL_POSITIONS, PARENT_TYPES, TypeRegistry


class TypeRegistryTests(unittest.TestCase):
    def setUp(self):
        # registry doc convention from link-types.md §4: <doc>.1.0.2.<position>
        self.registry_doc = Address("1.1.0.1.0.1")
        self.types = TypeRegistry(self.registry_doc)

    def test_canonical_positions_loaded(self):
        # spot-check coverage of every family
        self.assertTrue(self.types.is_known("claim"))
        self.assertTrue(self.types.is_known("contract.axiom"))
        self.assertTrue(self.types.is_known("citation.depends"))
        self.assertTrue(self.types.is_known("comment.observe"))
        self.assertTrue(self.types.is_known("provenance.derivation"))
        self.assertTrue(self.types.is_known("manages"))
        self.assertTrue(self.types.is_known("lattice"))

    def test_lattice_address_at_position_21(self):
        self.assertEqual(
            self.types.address_for("lattice"),
            Address("1.1.0.1.0.1.1.0.2.21"),
        )

    def test_address_for_leaf_type(self):
        # claim is at position 1 → address is <registry>.1.0.2.1
        self.assertEqual(
            self.types.address_for("claim"),
            Address("1.1.0.1.0.1.1.0.2.1"),
        )

    def test_address_for_subtype(self):
        # citation.depends is at position 15.1 → <registry>.1.0.2.15.1
        self.assertEqual(
            self.types.address_for("citation.depends"),
            Address("1.1.0.1.0.1.1.0.2.15.1"),
        )

    def test_address_for_parent_type(self):
        # parent type "citation" at position 15 → <registry>.1.0.2.15
        self.assertEqual(
            self.types.address_for("citation"),
            Address("1.1.0.1.0.1.1.0.2.15"),
        )

    def test_subtype_extends_parent_address_per_l10(self):
        parent = self.types.address_for("citation")
        for kind in ("citation.depends", "citation.forward", "citation.resolve"):
            child = self.types.address_for(kind)
            self.assertTrue(
                child.has_prefix(parent),
                f"{kind} address should extend the parent type address",
            )

    def test_unknown_type_raises(self):
        with self.assertRaises(KeyError):
            self.types.address_for("not-a-real-type")

    def test_name_for_addr_roundtrip(self):
        for name in CANONICAL_POSITIONS:
            self.assertEqual(self.types.name_for(self.types.address_for(name)), name)
        for name in PARENT_TYPES:
            self.assertEqual(self.types.name_for(self.types.address_for(name)), name)


class LinkSubspaceAddressingTests(unittest.TestCase):
    def test_link_subspace_base_for_doc(self):
        self.assertEqual(
            link_subspace_base(Address("1.1.0.1.0.5")),
            Address("1.1.0.1.0.5.0.2.1"),
        )

    def test_link_addresses_are_element_kind(self):
        base = link_subspace_base(Address("1.1.0.1.0.5"))
        self.assertEqual(base.zeros(), 3)

    def test_address_split_recovers_homedoc(self):
        link_addr = Address("1.1.0.1.0.5.0.2.7")
        homedoc, local = link_addr.split()
        self.assertEqual(homedoc, Address("1.1.0.1.0.5"))
        self.assertEqual(local, Address("2.7"))


class LinkStoreLowLevelTests(unittest.TestCase):
    """LinkStore taken directly with synthetic addresses — no State."""

    def test_emit_and_iterate(self):
        store = LinkStore()
        store.emit(
            addr=Address("1.1.0.1.0.5.0.2.1"),
            from_set=[Address("1.1.0.1.0.3")],
            to_set=[Address("1.1.0.1.0.4")],
            type_set=[Address("1.1.0.1.0.1.1.0.2.15.1")],
        )
        self.assertEqual(len(store), 1)
        link = list(store)[0]
        self.assertEqual(link.type_set, (Address("1.1.0.1.0.1.1.0.2.15.1"),))
        self.assertEqual(link.homedoc, Address("1.1.0.1.0.5"))


class StateMakeLinkTests(unittest.TestCase):
    def setUp(self):
        self.state = State(account=Address("1.1.0.1"))
        # description_doc is the homedoc under test, kept lattice-less
        # so its link subspace is empty before the test's make_link call.
        self.claim = self.state.create_doc()
        self.description_doc = self.state.create_doc()

    def test_link_address_in_homedoc_link_subspace(self):
        link = self.state.make_link(
            homedoc=self.description_doc,
            from_set=[self.description_doc],
            to_set=[self.claim],
            type_="description",
        )
        self.assertEqual(str(link.addr), f"{self.description_doc}.0.2.1")
        self.assertEqual(link.addr.zeros(), 3)

    def test_string_type_resolves_to_registry_address(self):
        link = self.state.make_link(
            self.description_doc, [self.description_doc], [self.claim], "description"
        )
        self.assertEqual(
            link.type_set, (self.state.types.address_for("description"),)
        )

    def test_link_addresses_are_dense_within_homedoc(self):
        l1 = self.state.make_link(
            self.description_doc, [self.description_doc], [self.claim], "description"
        )
        l2 = self.state.make_link(
            self.description_doc, [self.description_doc], [self.claim], "description"
        )
        self.assertEqual(str(l2.addr), f"{self.description_doc}.0.2.2")
        self.assertNotEqual(l1.addr, l2.addr)

    def test_unknown_type_string_raises(self):
        with self.assertRaises(KeyError):
            self.state.make_link(
                self.claim, [self.claim], [self.claim], "not-a-real-type"
            )

    def test_unknown_homedoc_rejected(self):
        with self.assertRaises(ValueError):
            self.state.make_link(
                Address("9.9.0.9.0.9"), [self.claim], [self.claim], "description"
            )


class HierarchicalTypeQueryTests(unittest.TestCase):
    """Per L10: query at a parent type address matches every subtype."""

    def setUp(self):
        self.state = State(account=Address("1.1.0.1"))
        self.xanadu = self.state.create_doc()
        self.claim_a = self.state.create_doc(kind="claim", lattice=self.xanadu)
        self.claim_b = self.state.create_doc(kind="claim", lattice=self.xanadu)
        self.claim_c = self.state.create_doc(kind="claim", lattice=self.xanadu)
        # Three citations from claim_a, varied by subtype
        self.depends = self.state.make_link(
            self.claim_a, [self.claim_a], [self.claim_b], "citation.depends"
        )
        self.forward = self.state.make_link(
            self.claim_a, [self.claim_a], [self.claim_c], "citation.forward"
        )
        # An unrelated description link
        self.desc = self.state.make_link(
            self.claim_a, [self.claim_a], [self.claim_b], "description"
        )

    def test_parent_type_query_matches_all_subtypes(self):
        results = self.state.find_links(type_="citation")
        self.assertEqual(set(results), {self.depends, self.forward})

    def test_leaf_type_query_matches_only_that_subtype(self):
        results = self.state.find_links(type_="citation.depends")
        self.assertEqual(results, [self.depends])

    def test_distinct_family_doesnt_match(self):
        results = self.state.find_links(type_="description")
        self.assertEqual(results, [self.desc])

    def test_filter_combines_with_to_set(self):
        results = self.state.find_links(
            to_set=[self.claim_b], type_="citation"
        )
        self.assertEqual(results, [self.depends])


class LinkVersioningTests(unittest.TestCase):
    """Editable links via VER3-style child allocators (D.0.2.N → D.0.2.N.M)."""

    def setUp(self):
        self.state = State(account=Address("1.1.0.1"))
        self.xanadu = self.state.create_doc()
        self.claim = self.state.create_doc(kind="claim", lattice=self.xanadu)
        self.other = self.state.create_doc(kind="claim", lattice=self.xanadu)
        self.link = self.state.make_link(
            homedoc=self.claim,
            from_set=[self.claim],
            to_set=[self.other],
            type_="citation.depends",
        )

    def test_first_edit_lands_at_child_address(self):
        edit = self.state.make_link_version(self.link.addr)
        self.assertEqual(str(edit.addr), str(self.link.addr) + ".1")

    def test_second_edit_is_sibling_of_first(self):
        e1 = self.state.make_link_version(self.link.addr)
        e2 = self.state.make_link_version(self.link.addr)
        self.assertEqual(str(e2.addr), str(self.link.addr) + ".2")
        self.assertEqual(self.state.parent[e1.addr], self.link.addr)
        self.assertEqual(self.state.parent[e2.addr], self.link.addr)

    def test_edit_of_edit_is_grandchild(self):
        e1 = self.state.make_link_version(self.link.addr)
        e1_v1 = self.state.make_link_version(e1.addr)
        self.assertEqual(str(e1_v1.addr), str(e1.addr) + ".1")
        self.assertEqual(self.state.parent[e1_v1.addr], e1.addr)

    def test_unspecified_fields_inherited_from_original(self):
        new_target = self.state.create_doc(kind="claim", lattice=self.xanadu)
        edit = self.state.make_link_version(self.link.addr, to_set=[new_target])
        self.assertEqual(edit.from_set, self.link.from_set)
        self.assertEqual(edit.to_set, (new_target,))
        self.assertEqual(edit.type_set, self.link.type_set)

    def test_edit_can_change_type(self):
        edit = self.state.make_link_version(
            self.link.addr, type_="citation.forward"
        )
        self.assertEqual(
            edit.type_set, (self.state.types.address_for("citation.forward"),)
        )

    def test_original_link_value_unchanged_after_edit(self):
        self.state.make_link_version(self.link.addr, to_set=[self.claim])
        original_after = self.state.links.get(self.link.addr)
        self.assertEqual(original_after.to_set, self.link.to_set)

    def test_link_homedoc_recovery_works_for_versioned_link(self):
        edit = self.state.make_link_version(self.link.addr)
        self.assertEqual(edit.homedoc, self.claim)

    def test_unknown_link_address_rejected(self):
        with self.assertRaises(ValueError):
            self.state.make_link_version(Address("9.9.0.9.0.9.0.2.1"))


class DescriptionAlignmentExampleTests(unittest.TestCase):
    """The substrate-predicate query that detects whether a head claim
    version has an active description-link — the original motivation
    for this whole simulation track."""

    def setUp(self):
        self.state = State(account=Address("1.1.0.1"))
        self.xanadu = self.state.create_doc()
        self.claim_v1 = self.state.create_doc(kind="claim", lattice=self.xanadu)
        self.description_doc = self.state.create_doc(lattice=self.xanadu)
        self.state.make_link(
            homedoc=self.description_doc,
            from_set=[self.description_doc],
            to_set=[self.claim_v1],
            type_="description",
        )

    def test_v1_has_description(self):
        results = self.state.find_links(
            to_set=[self.claim_v1], type_="description"
        )
        self.assertEqual(len(results), 1)

    def test_v2_does_not_have_description(self):
        claim_v2 = self.state.create_version(self.claim_v1)
        results = self.state.find_links(
            to_set=[claim_v2], type_="description"
        )
        self.assertEqual(len(results), 0)

    def test_alignment_predicate(self):
        def has_description(claim_version):
            return bool(
                self.state.find_links(
                    to_set=[claim_version], type_="description"
                )
            )

        self.assertTrue(has_description(self.claim_v1))
        claim_v2 = self.state.create_version(self.claim_v1)
        self.assertFalse(has_description(claim_v2))
        self.state.make_link(
            homedoc=self.description_doc,
            from_set=[self.description_doc],
            to_set=[claim_v2],
            type_="description",
        )
        self.assertTrue(has_description(claim_v2))


if __name__ == "__main__":
    unittest.main()
