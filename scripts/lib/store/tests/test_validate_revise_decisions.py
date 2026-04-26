"""Unit tests for the validate-revise decisions sidecar handling.

Covers parse_decisions (corruption-or-validated) and apply_retract_decisions
(emits one retraction per RETRACT entry).

The orchestrator script has a hyphen in its name and isn't importable as
a normal module; we use importlib.util the same way the orchestrator
imports the validator.
"""

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.store.cite import emit_citation
from lib.store.queries import active_links
from lib.store.store import Store


def _load_orchestrator():
    repo_root = Path(__file__).resolve().parents[4]
    spec = importlib.util.spec_from_file_location(
        "cvr", repo_root / "scripts" / "convergence-validate-revise.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CVR = _load_orchestrator()


class DecisionsTestBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.scratch = Path(self.tmp.name)
        self.label_index = {
            "T0":      "lattices/xanadu/claim-convergence/ASN-0001/T0.md",
            "T1":      "lattices/xanadu/claim-convergence/ASN-0001/T1.md",
            "T-stale": "lattices/xanadu/claim-convergence/ASN-0001/T-stale.md",
            "T-new":   "lattices/xanadu/claim-convergence/ASN-0001/T-new.md",
        }
        self.findings_labels = {"T0", "T-stale", "T-new"}

    def _write_decisions(self, decisions):
        (self.scratch / "__decisions.json").write_text(json.dumps(decisions))

    def _write_raw(self, text):
        (self.scratch / "__decisions.json").write_text(text)


class ParseDecisionsHappyTests(DecisionsTestBase):
    def test_valid_all_skip(self):
        self._write_decisions([
            {"label": "T0",      "action": "SKIP", "rationale": "deferred"},
            {"label": "T-stale", "action": "SKIP", "rationale": "uncertain"},
        ])
        out = CVR.parse_decisions(
            self.scratch, self.findings_labels, self.label_index, "",
        )
        self.assertEqual([d["action"] for d in out], ["SKIP", "SKIP"])

    def test_valid_mixed_actions(self):
        diff = (
            "--- a/T2.md\n+++ b/T2.md\n@@ -1 +1,2 @@\n"
            "+  - T-new (Name) — used at line 47\n"
        )
        self._write_decisions([
            {"label": "T-new",   "action": "ADD",     "rationale": "use-site at line 47"},
            {"label": "T-stale", "action": "RETRACT", "rationale": "no use-site"},
            {"label": "T0",      "action": "SKIP",    "rationale": "deferred"},
        ])
        out = CVR.parse_decisions(
            self.scratch, self.findings_labels, self.label_index, diff,
        )
        self.assertEqual(
            [(d["label"], d["action"]) for d in out],
            [("T-new", "ADD"), ("T-stale", "RETRACT"), ("T0", "SKIP")],
        )


class ParseDecisionsCorruptionTests(DecisionsTestBase):
    def test_missing_file_raises(self):
        with self.assertRaises(CVR.DecisionsCorruption) as cm:
            CVR.parse_decisions(
                self.scratch, self.findings_labels, self.label_index, "",
            )
        self.assertIn("not written", str(cm.exception))

    def test_invalid_json_raises(self):
        self._write_raw("{not json")
        with self.assertRaises(CVR.DecisionsCorruption) as cm:
            CVR.parse_decisions(
                self.scratch, self.findings_labels, self.label_index, "",
            )
        self.assertIn("not valid JSON", str(cm.exception))

    def test_not_an_array_raises(self):
        self._write_raw('{"label": "T0"}')
        with self.assertRaises(CVR.DecisionsCorruption) as cm:
            CVR.parse_decisions(
                self.scratch, self.findings_labels, self.label_index, "",
            )
        self.assertIn("must be a JSON array", str(cm.exception))

    def test_unknown_action_raises(self):
        self._write_decisions([
            {"label": "T0", "action": "MAYBE", "rationale": ""},
        ])
        with self.assertRaises(CVR.DecisionsCorruption) as cm:
            CVR.parse_decisions(
                self.scratch, self.findings_labels, self.label_index, "",
            )
        self.assertIn("MAYBE", str(cm.exception))

    def test_label_not_in_findings_raises(self):
        self._write_decisions([
            {"label": "T1", "action": "SKIP", "rationale": ""},
        ])
        with self.assertRaises(CVR.DecisionsCorruption) as cm:
            CVR.parse_decisions(
                self.scratch, self.findings_labels, self.label_index, "",
            )
        self.assertIn("not in findings", str(cm.exception))

    def test_label_not_in_index_raises(self):
        # A label in findings list but not in the lattice's label_index.
        findings_labels = {"T-ghost"}
        self._write_decisions([
            {"label": "T-ghost", "action": "SKIP", "rationale": ""},
        ])
        with self.assertRaises(CVR.DecisionsCorruption) as cm:
            CVR.parse_decisions(
                self.scratch, findings_labels, self.label_index, "",
            )
        self.assertIn("label_index", str(cm.exception))

    def test_add_without_diff_entry_raises(self):
        self._write_decisions([
            {"label": "T-new", "action": "ADD", "rationale": "use-site"},
        ])
        # Diff doesn't contain a +  - T-new bullet line.
        with self.assertRaises(CVR.DecisionsCorruption) as cm:
            CVR.parse_decisions(
                self.scratch, self.findings_labels, self.label_index, "",
            )
        self.assertIn("no matching bullet", str(cm.exception))


class ApplyRetractDecisionsTests(unittest.TestCase):
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
            "T0":      "lattices/xanadu/claim-convergence/ASN-0001/T0.md",
            "T1":      "lattices/xanadu/claim-convergence/ASN-0001/T1.md",
            "T-stale": "lattices/xanadu/claim-convergence/ASN-0001/T-stale.md",
        }
        self.from_claim = "lattices/xanadu/claim-convergence/ASN-0001/T2.md"
        emit_citation(self.store, self.from_claim, "T0", self.label_index)
        emit_citation(self.store, self.from_claim, "T1", self.label_index)
        emit_citation(
            self.store, self.from_claim, "T-stale", self.label_index,
        )

    def test_emits_one_per_retract(self):
        decisions = [
            {"label": "T-stale", "action": "RETRACT", "rationale": "stale"},
        ]
        n = CVR.apply_retract_decisions(
            self.store, decisions, self.from_claim, self.label_index,
        )
        self.assertEqual(n, 1)
        active = active_links(
            self.store, "citation", from_set=[self.from_claim],
        )
        self.assertEqual(len(active), 2)

    def test_idempotent(self):
        decisions = [
            {"label": "T-stale", "action": "RETRACT", "rationale": "stale"},
        ]
        CVR.apply_retract_decisions(
            self.store, decisions, self.from_claim, self.label_index,
        )
        # Re-apply: emit_retraction returns existing id, no new link created.
        before = len(self.store.find_links(type_set=["retraction"]))
        CVR.apply_retract_decisions(
            self.store, decisions, self.from_claim, self.label_index,
        )
        after = len(self.store.find_links(type_set=["retraction"]))
        self.assertEqual(before, after)

    def test_skips_non_retract(self):
        decisions = [
            {"label": "T0",      "action": "ADD",  "rationale": ""},
            {"label": "T-stale", "action": "SKIP", "rationale": ""},
        ]
        n = CVR.apply_retract_decisions(
            self.store, decisions, self.from_claim, self.label_index,
        )
        self.assertEqual(n, 0)
        self.assertEqual(
            len(self.store.find_links(type_set=["retraction"])), 0,
        )

    def test_missing_citation_raises_corruption(self):
        # T-stale citation already retracted by a prior pass; this
        # decision references a citation that emit_retraction can't
        # find as ACTIVE — wait, but emit_retraction looks up by
        # find_links which sees retracted citations too. Test the
        # actual failure mode: a label whose citation was never emitted.
        decisions = [
            {"label": "T-never", "action": "RETRACT", "rationale": ""},
        ]
        with self.assertRaises(CVR.DecisionsCorruption):
            CVR.apply_retract_decisions(
                self.store, decisions, self.from_claim,
                {"T-never": "lattices/xanadu/claim-convergence/ASN-0001/T-never.md"},
            )


class AddedBulletLabelsTests(unittest.TestCase):
    def test_extracts_added_bullets(self):
        diff = (
            "--- a/file\n+++ b/file\n@@\n"
            "   - T0 (Foo) — existing bullet\n"
            "+  - T-new (Bar) — newly added\n"
            "+  - NAT-other (Baz) — also new\n"
            "-  - T-old (Old) — removed\n"
        )
        self.assertEqual(
            CVR._added_bullet_labels(diff),
            {"T-new", "NAT-other"},
        )

    def test_ignores_removed_and_context(self):
        diff = (
            "   - T-context (X) — unchanged\n"
            "-  - T-removed (Y) — was here\n"
        )
        self.assertEqual(CVR._added_bullet_labels(diff), set())


if __name__ == "__main__":
    unittest.main()
