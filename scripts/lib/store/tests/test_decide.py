"""Unit tests for the decide library (resolution.edit / resolution.reject)."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.store.decide import emit_decision
from lib.store.store import Store


class DecideTestBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.store = Store(
            log_path=self.root / "_store" / "links.jsonl",
            index_path=self.root / "_store" / "index.db",
        )
        self.addCleanup(self.store.close)
        self.claim_path = "lattices/xanadu/claim-convergence/ASN-0001/T0.md"
        self.comment_id = self.store.make_link(
            from_set=["_store/documents/findings/ASN-0001/review-1/0.md"],
            to_set=[self.claim_path],
            type_set=["comment.revise"],
        )


class AcceptTests(DecideTestBase):
    def test_accept_writes_resolution_edit(self):
        link_id = emit_decision(
            self.store, "accept", self.comment_id, self.claim_path, "ASN-0001",
        )
        rec = self.store.get(link_id)
        self.assertEqual(rec["type_set"], ["resolution.edit"])
        self.assertEqual(rec["to_set"], [self.comment_id])
        self.assertEqual(rec["from_set"], [self.claim_path])


class RejectTests(DecideTestBase):
    def test_reject_materializes_rationale_and_link(self):
        rationales = self.root / "_store" / "rationales"
        link_id = emit_decision(
            self.store, "reject", self.comment_id, self.claim_path, "ASN-0001",
            rationale="The reviewer misread the contract; T0 already handles this.",
            rationales_dir=rationales,
            workspace=self.root,
        )
        rationale_path = rationales / "ASN-0001" / f"{self.comment_id}.md"
        self.assertTrue(rationale_path.exists())
        self.assertIn("misread", rationale_path.read_text())
        rec = self.store.get(link_id)
        self.assertEqual(rec["type_set"], ["resolution.reject"])
        self.assertIn(self.comment_id, rec["to_set"])
        self.assertEqual(len(rec["to_set"]), 2)

    def test_reject_without_rationale_raises(self):
        with self.assertRaises(ValueError):
            emit_decision(
                self.store, "reject", self.comment_id, self.claim_path,
                "ASN-0001",
            )


class ErrorTests(DecideTestBase):
    def test_unknown_comment_raises(self):
        with self.assertRaises(KeyError):
            emit_decision(
                self.store, "accept", "l_nonexistent",
                self.claim_path, "ASN-0001",
            )

    def test_unknown_action_raises(self):
        with self.assertRaises(ValueError):
            emit_decision(
                self.store, "frobnicate", self.comment_id,
                self.claim_path, "ASN-0001",
            )


if __name__ == "__main__":
    unittest.main()
