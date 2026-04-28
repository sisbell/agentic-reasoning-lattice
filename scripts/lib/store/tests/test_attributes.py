"""Unit tests for the attributes library (label, name, description, vocabulary).

Substrate-owned attribute links emit a typed link from a claim md to a
sibling `<stem>.<kind>.md` doc. Edit-in-place mutability: re-emit with a
new value updates the doc, link stays.
"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.store.attributes import emit_attribute
from lib.store.store import Store


class AttributesTestBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.store = Store(
            log_path=self.root / "_store" / "links.jsonl",
            index_path=self.root / "_store" / "index.db",
        )
        self.addCleanup(self.store.close)
        self.claim_dir = self.root / "lattices" / "xanadu" / "claim-convergence" / "ASN-0001"
        self.claim_dir.mkdir(parents=True)
        self.claim_md = self.claim_dir / "T0.md"
        self.claim_md.write_text("# T0\n")
        self.claim_rel = str(self.claim_md.relative_to(self.root))

    def _attr_doc(self, kind, stem="T0"):
        return self.claim_dir / f"{stem}.{kind}.md"


class EmitLabelTests(AttributesTestBase):
    def test_creates_link_and_doc(self):
        link_id, created = emit_attribute(
            self.store, self.claim_rel, "label", "T0",
            lattice_root=self.root,
        )
        self.assertTrue(created)
        rec = self.store.get(link_id)
        self.assertEqual(rec["type_set"], ["label"])
        self.assertEqual(rec["from_set"], [self.claim_rel])
        expected_doc_rel = str(self._attr_doc("label").relative_to(self.root))
        self.assertEqual(rec["to_set"], [expected_doc_rel])
        self.assertEqual(self._attr_doc("label").read_text(), "T0\n")


class EmitNameTests(AttributesTestBase):
    def test_creates_link_and_doc(self):
        link_id, created = emit_attribute(
            self.store, self.claim_rel, "name", "CarrierSetDefinition",
            lattice_root=self.root,
        )
        self.assertTrue(created)
        rec = self.store.get(link_id)
        self.assertEqual(rec["type_set"], ["name"])
        self.assertEqual(self._attr_doc("name").read_text(),
                         "CarrierSetDefinition\n")


class EmitDescriptionTests(AttributesTestBase):
    def test_creates_link_and_doc_multiline(self):
        body = ("Defines the carrier set ℕ for tumbler addresses.\n\n"
                "Supplies the underlying numeric structure that all\n"
                "subsequent definitions build upon.")
        link_id, created = emit_attribute(
            self.store, self.claim_rel, "description", body,
            lattice_root=self.root,
        )
        self.assertTrue(created)
        rec = self.store.get(link_id)
        self.assertEqual(rec["type_set"], ["description"])
        self.assertEqual(self._attr_doc("description").read_text(), body + "\n")


class EmitVocabularyTests(AttributesTestBase):
    def test_creates_link_and_doc(self):
        body = ("- `Σ.C` — The content store: a partial function "
                "from tumblers to content values\n"
                "- `Val` — An unspecified set of content values")
        link_id, created = emit_attribute(
            self.store, self.claim_rel, "vocabulary", body,
            lattice_root=self.root,
        )
        self.assertTrue(created)
        rec = self.store.get(link_id)
        self.assertEqual(rec["type_set"], ["vocabulary"])
        self.assertEqual(rec["from_set"], [self.claim_rel])
        expected_doc_rel = str(
            self._attr_doc("vocabulary").relative_to(self.root)
        )
        self.assertEqual(rec["to_set"], [expected_doc_rel])
        self.assertEqual(self._attr_doc("vocabulary").read_text(), body + "\n")

    def test_idempotent_on_repeated_call(self):
        body = "- `T` — carrier set\n- `#a` — length operator"
        first_id, c1 = emit_attribute(
            self.store, self.claim_rel, "vocabulary", body,
            lattice_root=self.root,
        )
        second_id, c2 = emit_attribute(
            self.store, self.claim_rel, "vocabulary", body,
            lattice_root=self.root,
        )
        self.assertTrue(c1)
        self.assertFalse(c2)
        self.assertEqual(first_id, second_id)

    def test_preserves_trailing_newline_when_present(self):
        body = "Prose description.\n"
        emit_attribute(
            self.store, self.claim_rel, "description", body,
            lattice_root=self.root,
        )
        # No double-newline added when value already ended with one.
        self.assertEqual(self._attr_doc("description").read_text(),
                         "Prose description.\n")


class IdempotencyTests(AttributesTestBase):
    def test_second_call_same_value_returns_existing(self):
        id1, c1 = emit_attribute(
            self.store, self.claim_rel, "name", "Foo",
            lattice_root=self.root,
        )
        id2, c2 = emit_attribute(
            self.store, self.claim_rel, "name", "Foo",
            lattice_root=self.root,
        )
        self.assertEqual(id1, id2)
        self.assertTrue(c1)
        self.assertFalse(c2)

    def test_overwrites_doc_on_value_change_link_stays(self):
        id1, _ = emit_attribute(
            self.store, self.claim_rel, "name", "Foo",
            lattice_root=self.root,
        )
        id2, c2 = emit_attribute(
            self.store, self.claim_rel, "name", "Bar",
            lattice_root=self.root,
        )
        # Same link id (no new link emitted; doc was edited in place).
        self.assertEqual(id1, id2)
        self.assertFalse(c2)
        self.assertEqual(self._attr_doc("name").read_text(), "Bar\n")
        # And only one name link exists in the store.
        all_name_links = self.store.find_links(type_set=["name"])
        self.assertEqual(len(all_name_links), 1)


class UnknownKindTests(AttributesTestBase):
    def test_unknown_kind_raises(self):
        with self.assertRaises(ValueError) as cm:
            emit_attribute(
                self.store, self.claim_rel, "summary", "Foo",
                lattice_root=self.root,
            )
        self.assertIn("summary", str(cm.exception))


class CoexistenceTests(AttributesTestBase):
    def test_distinct_kinds_coexist_for_one_claim(self):
        emit_attribute(self.store, self.claim_rel, "label", "T0",
                       lattice_root=self.root)
        emit_attribute(self.store, self.claim_rel, "name",
                       "CarrierSetDefinition", lattice_root=self.root)
        emit_attribute(self.store, self.claim_rel, "description",
                       "Carrier set on ℕ.", lattice_root=self.root)
        # Three independent links.
        for kind in ("label", "name", "description"):
            links = self.store.find_links(
                from_set=[self.claim_rel], type_set=[kind],
            )
            self.assertEqual(len(links), 1, f"{kind} link missing or duplicated")
            self.assertTrue(self._attr_doc(kind).exists())

    def test_distinct_claims_get_distinct_attribute_docs(self):
        claim_md_t1 = self.claim_dir / "T1.md"
        claim_md_t1.write_text("# T1\n")
        rel_t1 = str(claim_md_t1.relative_to(self.root))

        emit_attribute(self.store, self.claim_rel, "name", "CarrierA",
                       lattice_root=self.root)
        emit_attribute(self.store, rel_t1, "name", "CarrierB",
                       lattice_root=self.root)

        self.assertEqual(self._attr_doc("name", "T0").read_text(),
                         "CarrierA\n")
        self.assertEqual(self._attr_doc("name", "T1").read_text(),
                         "CarrierB\n")
        all_name = self.store.find_links(type_set=["name"])
        self.assertEqual(len(all_name), 2)


if __name__ == "__main__":
    unittest.main()
