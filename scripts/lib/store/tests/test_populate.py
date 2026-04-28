"""Unit tests for the structural populate script."""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.store.populate import (
    build_cross_asn_label_index,
    populate_structural,
)
from lib.store.store import Store


def _make_fixture_asn(claim_convergence_dir, asn, claims):
    """Create yaml + md pairs for each claim in the named ASN dir.

    `claims` is a list of dicts with keys label, name, type, depends.
    """
    asn_dir = claim_convergence_dir / asn
    asn_dir.mkdir(parents=True, exist_ok=True)
    for c in claims:
        yaml_path = asn_dir / f"{c['label']}.yaml"
        md_path = asn_dir / f"{c['label']}.md"
        yaml_path.write_text(yaml.dump({
            "label": c["label"],
            "name": c["name"],
            "type": c["type"],
            "depends": c.get("depends", []),
        }))
        md_path.write_text(f"# {c['label']}\n\n{c['name']}\n")


class PopulateTestBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        # _lattice_relative() computes paths relative to LATTICE. We patch
        # LATTICE to point at self.root so claim_convergence_dir/<asn>/<label>.md
        # resolves to a clean lattice-relative key like
        # "claim-convergence/<asn>/<label>.md".
        self.claim_convergence_dir = self.root / "claim-convergence"
        self.claim_convergence_dir.mkdir(parents=True)
        self.lattice_patcher = mock.patch(
            "lib.store.populate.LATTICE", self.root,
        )
        self.lattice_patcher.start()
        self.addCleanup(self.lattice_patcher.stop)

        self.store = Store(
            log_path=self.root / "_store" / "links.jsonl",
            index_path=self.root / "_store" / "index.db",
        )
        self.addCleanup(self.store.close)

    def _path_to(self, asn, label):
        full = self.claim_convergence_dir / asn / f"{label}.md"
        return str(full.relative_to(self.root))


class StructuralImportTests(PopulateTestBase):
    def test_imports_claim_classifier_per_yaml(self):
        _make_fixture_asn(self.claim_convergence_dir, "ASN-0001", [
            {"label": "T0", "name": "FoundA", "type": "axiom"},
            {"label": "T1", "name": "FoundB", "type": "axiom"},
            {"label": "T2", "name": "Result", "type": "theorem", "depends": ["T0", "T1"]},
        ])
        stats = populate_structural(self.store, self.claim_convergence_dir)
        self.assertEqual(stats["claims_seen"], 3)
        self.assertEqual(stats["claims_added"], 3)
        claim_links = self.store.find_links(type_set=["claim"])
        targets = sorted(l["to_set"][0] for l in claim_links)
        self.assertEqual(targets, [
            self._path_to("ASN-0001", "T0"),
            self._path_to("ASN-0001", "T1"),
            self._path_to("ASN-0001", "T2"),
        ])

    def test_imports_contract_classifier_per_yaml(self):
        _make_fixture_asn(self.claim_convergence_dir, "ASN-0001", [
            {"label": "T0", "name": "FoundA", "type": "axiom"},
            {"label": "T2", "name": "Result", "type": "theorem", "depends": ["T0"]},
        ])
        populate_structural(self.store, self.claim_convergence_dir)
        axioms = self.store.find_links(type_set=["contract.axiom"])
        theorems = self.store.find_links(type_set=["contract.theorem"])
        self.assertEqual(len(axioms), 1)
        self.assertEqual(len(theorems), 1)
        self.assertEqual(axioms[0]["to_set"], [self._path_to("ASN-0001", "T0")])
        self.assertEqual(theorems[0]["to_set"], [self._path_to("ASN-0001", "T2")])

    def test_imports_citation_links_from_depends(self):
        _make_fixture_asn(self.claim_convergence_dir, "ASN-0001", [
            {"label": "T0", "name": "A", "type": "axiom"},
            {"label": "T1", "name": "B", "type": "axiom"},
            {"label": "T2", "name": "C", "type": "theorem", "depends": ["T0", "T1"]},
        ])
        populate_structural(self.store, self.claim_convergence_dir)
        cites = self.store.find_links(
            from_set=[self._path_to("ASN-0001", "T2")],
            type_set=["citation"],
        )
        targets = sorted(l["to_set"][0] for l in cites)
        self.assertEqual(targets, [
            self._path_to("ASN-0001", "T0"),
            self._path_to("ASN-0001", "T1"),
        ])

    def test_cross_asn_citation_resolved(self):
        _make_fixture_asn(self.claim_convergence_dir, "ASN-0001", [
            {"label": "GlobalUniqueness", "name": "GU", "type": "axiom"},
        ])
        _make_fixture_asn(self.claim_convergence_dir, "ASN-0002", [
            {"label": "AX-3", "name": "Ax3", "type": "axiom",
             "depends": ["GlobalUniqueness"]},
        ])
        populate_structural(self.store, self.claim_convergence_dir)
        cites = self.store.find_links(
            from_set=[self._path_to("ASN-0002", "AX-3")],
            type_set=["citation"],
        )
        self.assertEqual(len(cites), 1)
        self.assertEqual(
            cites[0]["to_set"], [self._path_to("ASN-0001", "GlobalUniqueness")],
        )

    def test_unresolved_label_recorded_not_fatal(self):
        _make_fixture_asn(self.claim_convergence_dir, "ASN-0001", [
            {"label": "T2", "name": "C", "type": "theorem",
             "depends": ["DoesNotExist"]},
        ])
        stats = populate_structural(self.store, self.claim_convergence_dir)
        self.assertEqual(stats["citations_seen"], 1)
        self.assertEqual(stats["citations_added"], 0)
        self.assertEqual(stats["unresolved_labels"], [("T2", "DoesNotExist")])

    def test_idempotent(self):
        _make_fixture_asn(self.claim_convergence_dir, "ASN-0001", [
            {"label": "T0", "name": "A", "type": "axiom"},
            {"label": "T2", "name": "C", "type": "theorem", "depends": ["T0"]},
        ])
        first = populate_structural(self.store, self.claim_convergence_dir)
        second = populate_structural(self.store, self.claim_convergence_dir)
        self.assertEqual(first["claims_added"], 2)
        self.assertEqual(first["citations_added"], 1)
        self.assertEqual(second["claims_added"], 0)
        self.assertEqual(second["contracts_added"], 0)
        self.assertEqual(second["citations_added"], 0)

    def test_skips_underscore_files(self):
        _make_fixture_asn(self.claim_convergence_dir, "ASN-0001", [
            {"label": "T0", "name": "A", "type": "axiom"},
        ])
        # Add cache files that should be ignored
        (self.claim_convergence_dir / "ASN-0001" / "_contract-cache.json").write_text("{}")
        (self.claim_convergence_dir / "ASN-0001" / "_signature.md").write_text("# sig")
        stats = populate_structural(self.store, self.claim_convergence_dir)
        self.assertEqual(stats["claims_seen"], 1)

    def test_design_requirement_imported_as_contract_subtype(self):
        _make_fixture_asn(self.claim_convergence_dir, "ASN-0001", [
            {"label": "DR-1", "name": "Req", "type": "design-requirement"},
        ])
        populate_structural(self.store, self.claim_convergence_dir)
        reqs = self.store.find_links(type_set=["contract.design-requirement"])
        self.assertEqual(len(reqs), 1)

    def test_unknown_type_raises(self):
        _make_fixture_asn(self.claim_convergence_dir, "ASN-0001", [
            {"label": "X", "name": "X", "type": "bogus"},
        ])
        with self.assertRaises(ValueError):
            populate_structural(self.store, self.claim_convergence_dir)


class LabelIndexTests(PopulateTestBase):
    def test_index_spans_multiple_asns(self):
        _make_fixture_asn(self.claim_convergence_dir, "ASN-0001", [
            {"label": "GlobalUniqueness", "name": "GU", "type": "axiom"},
        ])
        _make_fixture_asn(self.claim_convergence_dir, "ASN-0002", [
            {"label": "AX-3", "name": "Ax3", "type": "axiom"},
        ])
        idx = build_cross_asn_label_index(self.claim_convergence_dir)
        self.assertEqual(idx["GlobalUniqueness"],
                         self._path_to("ASN-0001", "GlobalUniqueness"))
        self.assertEqual(idx["AX-3"], self._path_to("ASN-0002", "AX-3"))

    def test_index_skips_underscore_files(self):
        asn_dir = self.claim_convergence_dir / "ASN-0001"
        asn_dir.mkdir(parents=True)
        (asn_dir / "_contract-cache.json").write_text("{}")
        idx = build_cross_asn_label_index(self.claim_convergence_dir)
        self.assertEqual(idx, {})


if __name__ == "__main__":
    unittest.main()
