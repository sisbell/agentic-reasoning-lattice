"""Unit tests for the substrate-attribute validator rules in
convergence-validate.py:

- check_attribute_link_shape (I4/I5/I6)
- check_attribute_doc_format (I7/I8/I9)
- load_pairs filtering of attribute docs

The validator script has a hyphen in its filename and isn't importable
as a normal module; we use importlib.util the same way other scripts do.
"""

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.store.attributes import emit_attribute
from lib.store.store import Store


def _load_validator():
    repo_root = Path(__file__).resolve().parents[4]
    spec = importlib.util.spec_from_file_location(
        "convergence_validate",
        repo_root / "scripts" / "convergence-validate.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


VAL = _load_validator()


class AttributeValidatorTestBase(unittest.TestCase):
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
        self.claim_yaml = self.claim_dir / "T0.yaml"
        self.claim_yaml.write_text("label: T0\nname: T\n")
        self.claim_rel = str(self.claim_md.relative_to(self.root))
        self.label_index = {"T0": self.claim_rel}
        # pairs as load_pairs would return for one claim
        self.pairs = {
            "T0": {
                "yaml": {"label": "T0", "name": "T"},
                "md": "# T0\n",
                "yaml_error": None,
            },
        }


class CheckAttributeLinkShapeTests(AttributeValidatorTestBase):
    def test_well_formed_link_no_findings(self):
        emit_attribute(self.store, self.claim_rel, "name",
                       "CarrierSetDefinition", lattice_root=self.root)
        findings = VAL.check_attribute_link_shape(
            self.pairs, self.store, self.label_index, "name",
        )
        self.assertEqual(findings, [])

    def test_wrong_to_set_flagged(self):
        # Manually file a link with wrong to_set (sibling pointing at the
        # wrong file, not <stem>.name.md).
        wrong_doc = "lattices/xanadu/claim-convergence/ASN-0001/elsewhere.md"
        self.store.make_link(
            from_set=[self.claim_rel],
            to_set=[wrong_doc],
            type_set=["name"],
        )
        findings = VAL.check_attribute_link_shape(
            self.pairs, self.store, self.label_index, "name",
        )
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["rule"], "name-link-shape")
        self.assertIn("to_set", findings[0]["detail"])

    def test_three_kinds_independent(self):
        emit_attribute(self.store, self.claim_rel, "label", "T0",
                       lattice_root=self.root)
        emit_attribute(self.store, self.claim_rel, "name", "Foo",
                       lattice_root=self.root)
        emit_attribute(self.store, self.claim_rel, "description", "Bar.",
                       lattice_root=self.root)
        for kind in ("label", "name", "description"):
            findings = VAL.check_attribute_link_shape(
                self.pairs, self.store, self.label_index, kind,
            )
            self.assertEqual(findings, [], f"{kind} should be clean")


class CheckAttributeDocFormatTests(AttributeValidatorTestBase):
    def _write_doc(self, kind, content):
        (self.claim_dir / f"T0.{kind}.md").write_text(content)

    def test_well_formed_label_no_findings(self):
        self._write_doc("label", "T0\n")
        findings = VAL.check_attribute_doc_format(self.claim_dir, "label")
        self.assertEqual(findings, [])

    def test_label_first_line_must_equal_stem(self):
        self._write_doc("label", "WrongLabel\n")
        findings = VAL.check_attribute_doc_format(self.claim_dir, "label")
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["rule"], "label-doc-format")
        self.assertIn("stem", findings[0]["detail"])

    def test_empty_label_doc_flagged(self):
        self._write_doc("label", "")
        findings = VAL.check_attribute_doc_format(self.claim_dir, "label")
        self.assertEqual(len(findings), 1)
        self.assertIn("empty", findings[0]["detail"])

    def test_empty_name_doc_flagged(self):
        self._write_doc("name", "   \n")
        findings = VAL.check_attribute_doc_format(self.claim_dir, "name")
        self.assertEqual(len(findings), 1)
        self.assertIn("empty", findings[0]["detail"])

    def test_empty_description_doc_flagged(self):
        self._write_doc("description", "")
        findings = VAL.check_attribute_doc_format(self.claim_dir, "description")
        self.assertEqual(len(findings), 1)
        self.assertIn("empty", findings[0]["detail"])

    def test_multiline_description_ok(self):
        self._write_doc("description", "First paragraph.\n\nSecond.\n")
        findings = VAL.check_attribute_doc_format(self.claim_dir, "description")
        self.assertEqual(findings, [])


class LoadPairsAttributeFilterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)
        # Real claim
        (self.dir / "T0.md").write_text("# T0\n")
        (self.dir / "T0.yaml").write_text("label: T0\nname: T\n")
        # Attribute docs (should be filtered out)
        (self.dir / "T0.label.md").write_text("T0\n")
        (self.dir / "T0.name.md").write_text("Foo\n")
        (self.dir / "T0.description.md").write_text("Prose.\n")

    def test_attribute_docs_not_treated_as_claims(self):
        pairs = VAL.load_pairs(self.dir)
        self.assertIn("T0", pairs)
        # No stems for the attribute doc filenames (T0.label, T0.name, T0.description).
        self.assertNotIn("T0.label", pairs)
        self.assertNotIn("T0.name", pairs)
        self.assertNotIn("T0.description", pairs)
        # Exactly one entry: T0.
        self.assertEqual(set(pairs.keys()), {"T0"})


if __name__ == "__main__":
    unittest.main()
