"""Unit tests for the classify library (contract.<kind> link emission)."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.store.classify import emit_classifier
from lib.store.schema import VALID_SUBTYPES
from lib.store.store import Store


class ClassifyTestBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.store = Store(
            log_path=self.root / "_store" / "links.jsonl",
            index_path=self.root / "_store" / "index.db",
        )
        self.addCleanup(self.store.close)
        self.claim_path = "claim-convergence/ASN-0001/T0.md"


class EmitClassifierTests(ClassifyTestBase):
    def test_each_valid_kind(self):
        for kind in sorted(VALID_SUBTYPES["contract"]):
            with self.subTest(kind=kind):
                claim = f"claim-convergence/ASN-0001/{kind}.md"
                link_id, created = emit_classifier(self.store, claim, kind)
                self.assertTrue(created)
                rec = self.store.get(link_id)
                self.assertEqual(rec["type_set"], [f"contract.{kind}"])
                self.assertEqual(rec["from_set"], [])
                self.assertEqual(rec["to_set"], [claim])

    def test_idempotent(self):
        link_id_1, c1 = emit_classifier(self.store, self.claim_path, "axiom")
        link_id_2, c2 = emit_classifier(self.store, self.claim_path, "axiom")
        self.assertEqual(link_id_1, link_id_2)
        self.assertTrue(c1)
        self.assertFalse(c2)

    def test_invalid_kind_raises(self):
        with self.assertRaises(ValueError):
            emit_classifier(self.store, self.claim_path, "not-a-real-kind")

    def test_different_kinds_create_separate_links(self):
        # A claim could in principle accumulate multiple classifier links over
        # time (Xanadu permanence); they're distinct because type_set differs.
        link_id_1, c1 = emit_classifier(self.store, self.claim_path, "axiom")
        link_id_2, c2 = emit_classifier(self.store, self.claim_path, "theorem")
        self.assertNotEqual(link_id_1, link_id_2)
        self.assertTrue(c1)
        self.assertTrue(c2)

    def test_no_from_set(self):
        link_id, _ = emit_classifier(self.store, self.claim_path, "axiom")
        rec = self.store.get(link_id)
        self.assertEqual(rec["from_set"], [])


if __name__ == "__main__":
    unittest.main()
