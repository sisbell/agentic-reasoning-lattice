"""Unit tests for the cite library (citation link emission)."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.store.cite import emit_citation
from lib.store.store import Store


class CiteTestBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.store = Store(
            log_path=self.root / "_store" / "links.jsonl",
            index_path=self.root / "_store" / "index.db",
        )
        self.addCleanup(self.store.close)
        self.label_index = {
            "T0": "claim-convergence/ASN-0001/T0.md",
            "T1": "claim-convergence/ASN-0001/T1.md",
        }
        self.from_claim = "claim-convergence/ASN-0001/T2.md"


class EmitCitationTests(CiteTestBase):
    def test_resolves_label_to_path(self):
        link_id, _ = emit_citation(
            self.store, self.from_claim, "T0", self.label_index,
        )
        rec = self.store.get(link_id)
        self.assertEqual(
            rec["to_set"],
            ["claim-convergence/ASN-0001/T0.md"],
        )

    def test_returns_created_true_first_time(self):
        _, created = emit_citation(
            self.store, self.from_claim, "T0", self.label_index,
        )
        self.assertTrue(created)

    def test_idempotent(self):
        link_id_1, c1 = emit_citation(
            self.store, self.from_claim, "T0", self.label_index,
        )
        link_id_2, c2 = emit_citation(
            self.store, self.from_claim, "T0", self.label_index,
        )
        self.assertEqual(link_id_1, link_id_2)
        self.assertTrue(c1)
        self.assertFalse(c2)

    def test_unknown_label_raises(self):
        with self.assertRaises(KeyError):
            emit_citation(
                self.store, self.from_claim, "DoesNotExist", self.label_index,
            )

    def test_creates_link_with_correct_endsets(self):
        link_id, _ = emit_citation(
            self.store, self.from_claim, "T0", self.label_index,
        )
        rec = self.store.get(link_id)
        self.assertEqual(rec["from_set"], [self.from_claim])
        self.assertEqual(
            rec["to_set"],
            ["claim-convergence/ASN-0001/T0.md"],
        )
        self.assertEqual(rec["type_set"], ["citation"])


if __name__ == "__main__":
    unittest.main()
