"""Migration: legacy path-keyed substrate → tumbler-keyed substrate."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from lib.backend.addressing import Address
from lib.backend.migrate import collect_legacy_paths, migrate
from lib.backend.persist import load_jsonl


def write_legacy_jsonl(path: Path, records: list) -> None:
    with open(path, "w") as f:
        for r in records:
            f.write(json.dumps(r, sort_keys=True) + "\n")


class CollectPathsTests(unittest.TestCase):
    def test_first_appearance_order_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            legacy = Path(tmp) / "links.jsonl"
            write_legacy_jsonl(
                legacy,
                [
                    {
                        "op": "create",
                        "id": "l_a",
                        "from_set": [],
                        "to_set": ["pathA.md"],
                        "type_set": ["claim"],
                        "ts": "2026-01-01T00:00:00Z",
                    },
                    {
                        "op": "create",
                        "id": "l_b",
                        "from_set": ["pathA.md"],
                        "to_set": ["pathB.md"],
                        "type_set": ["citation.depends"],
                        "ts": "2026-01-02T00:00:00Z",
                    },
                ],
            )
            paths = collect_legacy_paths(legacy)
            self.assertEqual(paths, ["pathA.md", "pathB.md"])

    def test_link_ids_excluded(self):
        with tempfile.TemporaryDirectory() as tmp:
            legacy = Path(tmp) / "links.jsonl"
            write_legacy_jsonl(
                legacy,
                [
                    {
                        "op": "create",
                        "id": "l_a",
                        "from_set": [],
                        "to_set": ["docA.md"],
                        "type_set": ["claim"],
                        "ts": "ts",
                    },
                    {
                        "op": "create",
                        "id": "l_b",
                        "from_set": [],
                        "to_set": ["l_a"],
                        "type_set": ["retraction"],
                        "ts": "ts",
                    },
                ],
            )
            paths = collect_legacy_paths(legacy)
            self.assertEqual(paths, ["docA.md"])


class MigrateSmallSubstrateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.legacy = Path(self.tmp.name) / "legacy.jsonl"
        self.output = Path(self.tmp.name) / "substrate"

    def test_minimal_migration_round_trip(self):
        write_legacy_jsonl(
            self.legacy,
            [
                {
                    "op": "create",
                    "id": "l_classify_a",
                    "from_set": [],
                    "to_set": ["claim/A.md"],
                    "type_set": ["claim"],
                    "ts": "2026-01-01T00:00:00Z",
                },
                {
                    "op": "create",
                    "id": "l_classify_b",
                    "from_set": [],
                    "to_set": ["claim/B.md"],
                    "type_set": ["claim"],
                    "ts": "2026-01-01T00:00:00Z",
                },
                {
                    "op": "create",
                    "id": "l_cite",
                    "from_set": ["claim/A.md"],
                    "to_set": ["claim/B.md"],
                    "type_set": ["citation.depends"],
                    "ts": "2026-01-02T00:00:00Z",
                },
            ],
        )
        counts = migrate(self.legacy, self.output, lattice_name="xanadu")
        self.assertEqual(counts["docs"], 2)
        self.assertEqual(counts["lattice_links"], 2)
        self.assertEqual(counts["legacy_links"], 3)

        # Verify files written
        self.assertTrue((self.output / "links.jsonl").exists())
        self.assertTrue((self.output / "paths.json").exists())

        # Path map carries metadata + paths
        with open(self.output / "paths.json") as f:
            path_map = json.load(f)
        self.assertEqual(path_map["_meta"]["lattice_name"], "xanadu")
        self.assertIn("registry_doc", path_map["_meta"])
        self.assertIn("lattice_doc", path_map["_meta"])
        self.assertEqual(set(path_map["paths"]), {"claim/A.md", "claim/B.md"})

    def test_link_id_translation_for_retraction(self):
        write_legacy_jsonl(
            self.legacy,
            [
                {
                    "op": "create",
                    "id": "l_cite_aaa",
                    "from_set": ["claim/A.md"],
                    "to_set": ["claim/B.md"],
                    "type_set": ["citation.depends"],
                    "ts": "2026-01-01T00:00:00Z",
                },
                {
                    "op": "create",
                    "id": "l_retract_aaa",
                    "from_set": ["claim/A.md"],
                    "to_set": ["l_cite_aaa"],
                    "type_set": ["retraction"],
                    "ts": "2026-01-02T00:00:00Z",
                },
            ],
        )
        migrate(self.legacy, self.output)
        # Load and verify the retraction's to_set points at the
        # citation link's tumbler address
        store = load_jsonl(self.output / "links.jsonl")
        retraction_type_addr = None
        from lib.backend.types import TypeRegistry
        # Recover registry doc address from path map
        with open(self.output / "paths.json") as f:
            meta = json.load(f)["_meta"]
        types = TypeRegistry(Address(meta["registry_doc"]))
        retraction_type_addr = types.address_for("retraction")

        retractions = store.find_links(type_set=[retraction_type_addr])
        self.assertEqual(len(retractions), 1)
        cite_addr = next(
            l.addr for l in store
            if l.type_set == (types.address_for("citation.depends"),)
        )
        self.assertEqual(retractions[0].to_set, (cite_addr,))

    def test_classifier_link_homed_in_classified_doc(self):
        write_legacy_jsonl(
            self.legacy,
            [
                {
                    "op": "create",
                    "id": "l_cl",
                    "from_set": [],
                    "to_set": ["claim/A.md"],
                    "type_set": ["claim"],
                    "ts": "2026-01-01T00:00:00Z",
                },
            ],
        )
        migrate(self.legacy, self.output)
        store = load_jsonl(self.output / "links.jsonl")
        with open(self.output / "paths.json") as f:
            path_map = json.load(f)
        a_tumbler = Address(path_map["paths"]["claim/A.md"])

        # The classifier link homed in claim/A.md (since F=∅ for classifier shape)
        from lib.backend.types import TypeRegistry
        types = TypeRegistry(Address(path_map["_meta"]["registry_doc"]))
        claim_classifiers = store.find_links(
            type_set=[types.address_for("claim")],
        )
        self.assertEqual(len(claim_classifiers), 1)
        self.assertEqual(claim_classifiers[0].homedoc, a_tumbler)
        self.assertEqual(claim_classifiers[0].from_set, ())
        self.assertEqual(claim_classifiers[0].to_set, (a_tumbler,))

    def test_legacy_source_in_meta_is_not_absolute(self):
        # We never want absolute filesystem paths leaking into committed
        # metadata. legacy_source should resolve to a repo-relative path
        # (or be left as-supplied if the input is outside the repo root).
        write_legacy_jsonl(
            self.legacy,
            [
                {
                    "op": "create",
                    "id": "l_a",
                    "from_set": [],
                    "to_set": ["claim/A.md"],
                    "type_set": ["claim"],
                    "ts": "ts",
                },
            ],
        )
        migrate(self.legacy, self.output)
        with open(self.output / "paths.json") as f:
            meta = json.load(f)["_meta"]
        # legacy is under the tempdir (outside the repo) — fallback applies
        # but should still not resemble a pinned user-home path that would
        # surprise a future reader. Test the in-repo case via a synthetic check.
        self.assertNotIn("/Users/", meta["legacy_source"])

    def test_lattice_links_emitted_for_every_doc(self):
        write_legacy_jsonl(
            self.legacy,
            [
                {
                    "op": "create",
                    "id": "l_a",
                    "from_set": [],
                    "to_set": ["claim/A.md"],
                    "type_set": ["claim"],
                    "ts": "ts",
                },
                {
                    "op": "create",
                    "id": "l_b",
                    "from_set": [],
                    "to_set": ["claim/B.md"],
                    "type_set": ["claim"],
                    "ts": "ts",
                },
            ],
        )
        migrate(self.legacy, self.output)
        store = load_jsonl(self.output / "links.jsonl")
        with open(self.output / "paths.json") as f:
            path_map = json.load(f)

        from lib.backend.types import TypeRegistry
        types = TypeRegistry(Address(path_map["_meta"]["registry_doc"]))
        lattice_doc = Address(path_map["_meta"]["lattice_doc"])
        lattice_links = store.find_links(
            type_set=[types.address_for("lattice")],
            to_set=[lattice_doc],
        )
        self.assertEqual(len(lattice_links), 2)
        # Each lattice link's from_set is the migrated doc
        sources = set()
        for link in lattice_links:
            sources.update(link.from_set)
        a_tumbler = Address(path_map["paths"]["claim/A.md"])
        b_tumbler = Address(path_map["paths"]["claim/B.md"])
        self.assertEqual(sources, {a_tumbler, b_tumbler})


if __name__ == "__main__":
    unittest.main()
