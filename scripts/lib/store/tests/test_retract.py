"""Unit tests for the retract library (citation retraction emission)."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.store.cite import emit_citation
from lib.store.retract import emit_retraction
from lib.store.store import Store


class RetractTestBase(unittest.TestCase):
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
            "T0": "lattices/xanadu/claim-convergence/ASN-0001/T0.md",
            "T1": "lattices/xanadu/claim-convergence/ASN-0001/T1.md",
        }
        self.from_claim = "lattices/xanadu/claim-convergence/ASN-0001/T2.md"

    def _emit_citation(self, to_label="T0"):
        return emit_citation(
            self.store, self.from_claim, to_label, self.label_index,
        )


class EmitRetractionTests(RetractTestBase):
    def test_retracts_existing_citation(self):
        cite_id, _ = self._emit_citation("T0")
        retract_id, created = emit_retraction(
            self.store, self.from_claim, "T0", self.label_index,
        )
        self.assertTrue(created)
        rec = self.store.get(retract_id)
        self.assertEqual(rec["type_set"], ["retraction"])
        self.assertEqual(rec["from_set"], [self.from_claim])
        self.assertEqual(rec["to_set"], [cite_id])

    def test_retraction_to_set_is_link_id_not_doc_path(self):
        cite_id, _ = self._emit_citation("T0")
        retract_id, _ = emit_retraction(
            self.store, self.from_claim, "T0", self.label_index,
        )
        rec = self.store.get(retract_id)
        # to_set is the citation's link id, not the dep's doc path
        self.assertEqual(rec["to_set"], [cite_id])
        self.assertNotIn(
            "lattices/xanadu/claim-convergence/ASN-0001/T0.md",
            rec["to_set"],
        )

    def test_idempotent(self):
        self._emit_citation("T0")
        link_id_1, c1 = emit_retraction(
            self.store, self.from_claim, "T0", self.label_index,
        )
        link_id_2, c2 = emit_retraction(
            self.store, self.from_claim, "T0", self.label_index,
        )
        self.assertEqual(link_id_1, link_id_2)
        self.assertTrue(c1)
        self.assertFalse(c2)

    def test_no_citation_raises(self):
        # No citation emitted; retraction has nothing to point at
        with self.assertRaises(ValueError):
            emit_retraction(
                self.store, self.from_claim, "T0", self.label_index,
            )

    def test_unknown_label_raises(self):
        with self.assertRaises(KeyError):
            emit_retraction(
                self.store, self.from_claim, "DoesNotExist",
                self.label_index,
            )

    def test_distinct_targets_get_distinct_retractions(self):
        cite_id_T0, _ = self._emit_citation("T0")
        cite_id_T1, _ = self._emit_citation("T1")
        retract_T0, _ = emit_retraction(
            self.store, self.from_claim, "T0", self.label_index,
        )
        retract_T1, _ = emit_retraction(
            self.store, self.from_claim, "T1", self.label_index,
        )
        self.assertNotEqual(retract_T0, retract_T1)
        self.assertEqual(self.store.get(retract_T0)["to_set"], [cite_id_T0])
        self.assertEqual(self.store.get(retract_T1)["to_set"], [cite_id_T1])


if __name__ == "__main__":
    unittest.main()
