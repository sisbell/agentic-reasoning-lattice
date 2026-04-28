"""Unit tests for the emit helpers (review classifier + finding documents)."""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.store.emit import (
    emit_campaign, emit_findings, emit_inquiry, emit_note,
    emit_note_findings, emit_review, emit_synthesis,
)
from lib.store.store import Store


class EmitTestBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.findings_dir = self.root / "_workspace" / "findings" / "claims"
        self.lattice_patcher = mock.patch(
            "lib.store.emit.LATTICE", self.root,
        )
        self.lattice_patcher.start()
        self.addCleanup(self.lattice_patcher.stop)

        self.store = Store(
            log_path=self.root / "_store" / "links.jsonl",
            index_path=self.root / "_store" / "index.db",
        )
        self.addCleanup(self.store.close)

    def _write_under_root(self, relpath, content=""):
        full = self.root / relpath
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(content)
        return full

    def _label_index(self, mapping):
        return {label: rel_path for label, rel_path in mapping.items()}


class EmitReviewTests(EmitTestBase):
    def test_emit_review_classifier(self):
        review_path = self._write_under_root(
            "claim-convergence/ASN-0001/reviews/review-1.md",
            "# Review\n",
        )
        link_id = emit_review(self.store, review_path)
        rec = self.store.get(link_id)
        self.assertEqual(rec["type_set"], ["review"])
        self.assertEqual(rec["from_set"], [])
        self.assertEqual(
            rec["to_set"],
            ["claim-convergence/ASN-0001/reviews/review-1.md"],
        )


class EmitInquiryTests(EmitTestBase):
    def test_first_call_creates_classifier(self):
        inq_path = self._write_under_root(
            "_store/documents/inquiry/ASN-0001.md",
            "---\ntitle: Foo\n---\n# Inquiry: Foo\n",
        )
        link_id, created = emit_inquiry(self.store, inq_path)
        self.assertTrue(created)
        rec = self.store.get(link_id)
        self.assertEqual(rec["type_set"], ["inquiry"])
        self.assertEqual(rec["from_set"], [])
        self.assertEqual(
            rec["to_set"],
            ["_store/documents/inquiry/ASN-0001.md"],
        )

    def test_repeated_call_is_idempotent(self):
        inq_path = self._write_under_root(
            "_store/documents/inquiry/ASN-0001.md", "x",
        )
        first_id, created1 = emit_inquiry(self.store, inq_path)
        second_id, created2 = emit_inquiry(self.store, inq_path)
        self.assertTrue(created1)
        self.assertFalse(created2)
        self.assertEqual(first_id, second_id)

    def test_distinct_inquiries_get_distinct_classifiers(self):
        a = self._write_under_root(
            "_store/documents/inquiry/ASN-0001.md", "a",
        )
        b = self._write_under_root(
            "_store/documents/inquiry/ASN-0002.md", "b",
        )
        a_id, _ = emit_inquiry(self.store, a)
        b_id, _ = emit_inquiry(self.store, b)
        self.assertNotEqual(a_id, b_id)


class EmitCampaignTests(EmitTestBase):
    def test_first_call_creates_classifier(self):
        camp_path = self._write_under_root(
            "_store/documents/campaign/foo/campaign.md",
            "---\nname: foo\ntheory: nelson\nevidence: gregory\n---\n",
        )
        link_id, created = emit_campaign(self.store, camp_path)
        self.assertTrue(created)
        rec = self.store.get(link_id)
        self.assertEqual(rec["type_set"], ["campaign"])
        self.assertEqual(rec["from_set"], [])
        self.assertEqual(
            rec["to_set"],
            ["_store/documents/campaign/foo/campaign.md"],
        )

    def test_repeated_call_is_idempotent(self):
        camp_path = self._write_under_root(
            "_store/documents/campaign/foo/campaign.md", "x",
        )
        first_id, created1 = emit_campaign(self.store, camp_path)
        second_id, created2 = emit_campaign(self.store, camp_path)
        self.assertTrue(created1)
        self.assertFalse(created2)
        self.assertEqual(first_id, second_id)


class EmitSynthesisTests(EmitTestBase):
    def setUp(self):
        super().setUp()
        self.inq_path = self._write_under_root(
            "_store/documents/inquiry/ASN-0001.md", "x",
        )
        self.note_path = self._write_under_root(
            "_store/documents/note/ASN-0001-foo.md", "# Foo\n",
        )

    def test_first_call_creates_link(self):
        link_id, created = emit_synthesis(
            self.store, self.inq_path, self.note_path,
        )
        self.assertTrue(created)
        rec = self.store.get(link_id)
        self.assertEqual(rec["type_set"], ["synthesis"])
        self.assertEqual(
            rec["from_set"],
            ["_store/documents/inquiry/ASN-0001.md"],
        )
        self.assertEqual(
            rec["to_set"],
            ["_store/documents/note/ASN-0001-foo.md"],
        )

    def test_repeated_call_is_idempotent(self):
        first_id, created1 = emit_synthesis(
            self.store, self.inq_path, self.note_path,
        )
        second_id, created2 = emit_synthesis(
            self.store, self.inq_path, self.note_path,
        )
        self.assertTrue(created1)
        self.assertFalse(created2)
        self.assertEqual(first_id, second_id)

    def test_distinct_pairs_get_distinct_links(self):
        other_inq = self._write_under_root(
            "_store/documents/inquiry/ASN-0002.md", "x",
        )
        other_note = self._write_under_root(
            "_store/documents/note/ASN-0002-bar.md", "y",
        )
        a_id, _ = emit_synthesis(self.store, self.inq_path, self.note_path)
        b_id, _ = emit_synthesis(self.store, other_inq, other_note)
        self.assertNotEqual(a_id, b_id)


class EmitNoteTests(EmitTestBase):
    def test_first_call_creates_classifier(self):
        note_path = self._write_under_root(
            "_store/documents/note/ASN-0001-foo.md", "# Note\n",
        )
        link_id, created = emit_note(self.store, note_path)
        self.assertTrue(created)
        rec = self.store.get(link_id)
        self.assertEqual(rec["type_set"], ["note"])
        self.assertEqual(rec["from_set"], [])
        self.assertEqual(
            rec["to_set"],
            ["_store/documents/note/ASN-0001-foo.md"],
        )

    def test_repeated_call_is_idempotent(self):
        note_path = self._write_under_root(
            "_store/documents/note/ASN-0001-foo.md", "# Note\n",
        )
        first_id, created1 = emit_note(self.store, note_path)
        second_id, created2 = emit_note(self.store, note_path)
        self.assertTrue(created1)
        self.assertFalse(created2)
        self.assertEqual(first_id, second_id)

    def test_distinct_notes_get_distinct_classifiers(self):
        a = self._write_under_root(
            "_store/documents/note/ASN-0001-a.md", "a",
        )
        b = self._write_under_root(
            "_store/documents/note/ASN-0002-b.md", "b",
        )
        a_id, _ = emit_note(self.store, a)
        b_id, _ = emit_note(self.store, b)
        self.assertNotEqual(a_id, b_id)


class EmitFindingsTests(EmitTestBase):
    def _findings(self, *items):
        # items: each is dict with title, cls, target_label or override body
        out = []
        for item in items:
            body = item.get("body") or (
                f"### {item['title']}\n"
                f"**Class**: {item['cls']}\n"
                f"**ASN**: {item['target_label']} — context\n"
                f"**Issue**: example issue\n"
                f"**What needs resolving**: fix it\n"
            )
            out.append((item["title"], item["cls"], body))
        return out

    def test_one_revise(self):
        review_path = self._write_under_root(
            "claim-convergence/ASN-0001/reviews/review-1.md", "x",
        )
        index = {"T0": "claim-convergence/ASN-0001/T0.md"}
        findings = self._findings(
            {"title": "missing precondition", "cls": "REVISE", "target_label": "T0"},
        )
        results = emit_findings(
            self.store, review_path, findings,
            asn_label="ASN-0001", review_stem="review-1",
            label_index=index, findings_dir=self.findings_dir,
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["claim_path"], index["T0"])
        rec = self.store.get(results[0]["comment_id"])
        self.assertEqual(rec["type_set"], ["comment.revise"])
        self.assertEqual(rec["from_set"], [results[0]["finding_path"]])
        self.assertEqual(rec["to_set"], [index["T0"]])

    def test_observe_classified_correctly(self):
        review_path = self._write_under_root(
            "claim-convergence/ASN-0001/reviews/review-1.md", "x",
        )
        index = {"T0": "claim-convergence/ASN-0001/T0.md"}
        findings = self._findings(
            {"title": "naming nit", "cls": "OBSERVE", "target_label": "T0"},
        )
        results = emit_findings(
            self.store, review_path, findings,
            asn_label="ASN-0001", review_stem="review-1",
            label_index=index, findings_dir=self.findings_dir,
        )
        rec = self.store.get(results[0]["comment_id"])
        self.assertEqual(rec["type_set"], ["comment.observe"])

    def test_skips_unresolvable_target(self):
        review_path = self._write_under_root(
            "claim-convergence/ASN-0001/reviews/review-1.md", "x",
        )
        index = {"T0": "claim-convergence/ASN-0001/T0.md"}
        findings = self._findings(
            {"title": "good", "cls": "REVISE", "target_label": "T0"},
            {"title": "bad", "cls": "REVISE", "target_label": "DoesNotExist"},
        )
        results = emit_findings(
            self.store, review_path, findings,
            asn_label="ASN-0001", review_stem="review-1",
            label_index=index, findings_dir=self.findings_dir,
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "good")

    def test_returns_input_order(self):
        review_path = self._write_under_root(
            "claim-convergence/ASN-0001/reviews/review-1.md", "x",
        )
        index = {
            "T0": "claim-convergence/ASN-0001/T0.md",
            "T1": "claim-convergence/ASN-0001/T1.md",
            "T2": "claim-convergence/ASN-0001/T2.md",
        }
        findings = self._findings(
            {"title": "one", "cls": "REVISE", "target_label": "T2"},
            {"title": "two", "cls": "OBSERVE", "target_label": "T0"},
            {"title": "three", "cls": "REVISE", "target_label": "T1"},
        )
        results = emit_findings(
            self.store, review_path, findings,
            asn_label="ASN-0001", review_stem="review-1",
            label_index=index, findings_dir=self.findings_dir,
        )
        self.assertEqual([r["title"] for r in results], ["one", "two", "three"])

    def test_materializes_at_expected_path(self):
        review_path = self._write_under_root(
            "claim-convergence/ASN-0034/reviews/review-46.md", "x",
        )
        index = {"S7": "claim-convergence/ASN-0034/S7.md"}
        findings = self._findings(
            {"title": "issue A", "cls": "REVISE", "target_label": "S7"},
        )
        results = emit_findings(
            self.store, review_path, findings,
            asn_label="ASN-0034", review_stem="review-46",
            label_index=index, findings_dir=self.findings_dir,
        )
        finding_full = self.root / results[0]["finding_path"]
        self.assertTrue(finding_full.exists())
        self.assertIn(
            "_workspace/findings/claims/ASN-0034/review-46/0.md",
            results[0]["finding_path"],
        )
        self.assertIn("**Class**: REVISE", finding_full.read_text())

    def test_falls_back_to_foundation_when_asn_missing(self):
        review_path = self._write_under_root(
            "claim-convergence/ASN-0001/reviews/review-1.md", "x",
        )
        index = {"NAT-zero": "claim-convergence/ASN-0034/NAT-zero.md"}
        body = (
            "### Cross-cone observation\n"
            "**Class**: REVISE\n"
            "**Foundation**: NAT-zero — base case\n"
            "**Issue**: ...\n"
        )
        findings = [("Cross-cone observation", "REVISE", body)]
        results = emit_findings(
            self.store, review_path, findings,
            asn_label="ASN-0001", review_stem="review-1",
            label_index=index, findings_dir=self.findings_dir,
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["claim_path"], index["NAT-zero"])


class EmitNoteFindingsTests(EmitTestBase):
    def setUp(self):
        super().setUp()
        self.note_findings_dir = (
            self.root / "_workspace" / "findings" / "notes"
        )
        self.note_path = self._write_under_root(
            "_store/documents/note/ASN-0001-foo.md", "# Note\n",
        )
        self.note_rel = "_store/documents/note/ASN-0001-foo.md"

    def test_revise_finding_emits_comment_revise(self):
        findings = [("Issue 1: bad", "REVISE", "### Issue 1: bad\nbody\n")]
        results = emit_note_findings(
            self.store, self.note_path, findings,
            asn_label="ASN-0001", review_stem="review-1",
            findings_dir=self.note_findings_dir,
        )
        self.assertEqual(len(results), 1)
        rec = self.store.get(results[0]["comment_id"])
        self.assertEqual(rec["type_set"], ["comment.revise"])
        self.assertEqual(rec["from_set"], [results[0]["finding_path"]])
        self.assertEqual(rec["to_set"], [self.note_rel])

    def test_oos_finding_emits_comment_out_of_scope(self):
        findings = [("Issue 2: scope", "OUT_OF_SCOPE", "body\n")]
        results = emit_note_findings(
            self.store, self.note_path, findings,
            asn_label="ASN-0001", review_stem="review-1",
            findings_dir=self.note_findings_dir,
        )
        rec = self.store.get(results[0]["comment_id"])
        self.assertEqual(rec["type_set"], ["comment.out-of-scope"])

    def test_materializes_at_expected_path(self):
        findings = [("X", "REVISE", "### X\nbody\n")]
        results = emit_note_findings(
            self.store, self.note_path, findings,
            asn_label="ASN-0001", review_stem="review-1",
            findings_dir=self.note_findings_dir,
        )
        self.assertIn(
            "_workspace/findings/notes/ASN-0001/review-1/0.md",
            results[0]["finding_path"],
        )
        full = self.root / results[0]["finding_path"]
        self.assertTrue(full.exists())
        self.assertIn("body", full.read_text())

    def test_multiple_findings_preserve_order_and_classify(self):
        findings = [
            ("a", "REVISE", "### a\n"),
            ("b", "OUT_OF_SCOPE", "### b\n"),
            ("c", "REVISE", "### c\n"),
        ]
        results = emit_note_findings(
            self.store, self.note_path, findings,
            asn_label="ASN-0001", review_stem="review-1",
            findings_dir=self.note_findings_dir,
        )
        self.assertEqual([r["title"] for r in results], ["a", "b", "c"])
        self.assertEqual(
            [r["cls"] for r in results],
            ["REVISE", "OUT_OF_SCOPE", "REVISE"],
        )


if __name__ == "__main__":
    unittest.main()
