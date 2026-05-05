"""Store tests — lattice-bound facade over State + JSONL persistence."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from lib.backend.addressing import Address
from lib.backend.migrate import migrate
from lib.backend.store import Store


def _count_lines(path: Path) -> int:
    with open(path) as f:
        return sum(1 for _ in f)


def _seed_legacy_jsonl(path: Path) -> None:
    records = [
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
    ]
    with open(path, "w") as f:
        for r in records:
            f.write(json.dumps(r, sort_keys=True) + "\n")


class StoreLoadTests(unittest.TestCase):
    """Store loads a migrated substrate end-to-end."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lattice_dir = Path(self.tmp.name) / "test_lattice"
        self.docuverse = self.lattice_dir / "_docuverse"
        self.docuverse.mkdir(parents=True)
        legacy = self.docuverse / "legacy_links.jsonl"
        _seed_legacy_jsonl(legacy)
        # Migrate to produce links.jsonl + paths.json under _docuverse
        migrate(legacy, self.docuverse, lattice_name="test")

    def test_store_loads_meta(self):
        store = Store(self.lattice_dir)
        self.assertEqual(store.lattice_name, "test")
        self.assertEqual(str(store.registry_doc), "1.1.0.1.0.1")
        self.assertEqual(str(store.lattice_doc), "1.1.0.1.0.2")

    def test_path_to_addr_and_reverse(self):
        store = Store(self.lattice_dir)
        a = store.addr_for_path("claim/A.md")
        self.assertEqual(store.path_for_addr(a), "claim/A.md")

    def test_find_links_returns_loaded_links(self):
        store = Store(self.lattice_dir)
        # Total links: 2 lattice + 2 classifier + 1 citation = 5
        # (classifiers from legacy: claim a, claim b)
        self.assertEqual(len(store.find_links()), 5)
        a = store.addr_for_path("claim/A.md")
        b = store.addr_for_path("claim/B.md")
        citations = store.find_links(
            from_set=[a], to_set=[b], type_="citation",
        )
        self.assertEqual(len(citations), 1)

    def test_make_link_appends_to_jsonl(self):
        store = Store(self.lattice_dir)
        a = store.addr_for_path("claim/A.md")
        b = store.addr_for_path("claim/B.md")
        before = _count_lines(store.jsonl_path)
        store.make_link(
            homedoc=a, from_set=[a], to_set=[b],
            type_="citation.forward",
        )
        after = _count_lines(store.jsonl_path)
        self.assertEqual(after, before + 1)
        # And the new link is queryable
        results = store.find_links(
            from_set=[a], to_set=[b], type_="citation.forward",
        )
        self.assertEqual(len(results), 1)

    def test_register_path_allocates_fresh_tumbler(self):
        store = Store(self.lattice_dir)
        new_addr = store.register_path("new/doc.md")
        self.assertEqual(store.path_for_addr(new_addr), "new/doc.md")
        # Lattice link emitted
        from lib.backend.predicates import active_links
        lattice_links = active_links(store.state, "lattice", from_set=[new_addr])
        self.assertEqual(len(lattice_links), 1)
        self.assertEqual(lattice_links[0].to_set, (store.lattice_doc,))
        # Re-registering returns the same tumbler
        self.assertEqual(store.register_path("new/doc.md"), new_addr)

    def test_register_path_persists_to_disk(self):
        store = Store(self.lattice_dir)
        store.register_path("new/doc.md")
        # Reload Store and confirm the new path is mapped
        del store
        store2 = Store(self.lattice_dir)
        self.assertIn("new/doc.md", store2.path_to_addr)

    def test_make_link_doesnt_collide_with_existing(self):
        # The Store re-attaches doc owners after load. New links
        # in homedoc A should pick up at the next free slot, not
        # overwrite existing classifier link addresses.
        store = Store(self.lattice_dir)
        a = store.addr_for_path("claim/A.md")
        # Existing links homed in A: classifier (claim) + lattice link
        # + citation.depends (homedoc=a).
        existing = len(store.find_links(homedoc=a))
        new = store.make_link(
            homedoc=a, from_set=[a], to_set=[], type_="finding",
        )
        # New link should not equal any existing link's address
        all_links = store.find_links(homedoc=a)
        self.assertEqual(len(all_links), existing + 1)
        self.assertEqual(
            sum(1 for l in all_links if l.addr == new.addr), 1,
        )


class RegisterVersionTests(unittest.TestCase):
    """Store.register_version: tumbler-version + path reroute + supersession."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lattice_dir = Path(self.tmp.name) / "test_lattice"
        self.docuverse = self.lattice_dir / "_docuverse"
        self.docuverse.mkdir(parents=True)
        legacy = self.docuverse / "legacy_links.jsonl"
        _seed_legacy_jsonl(legacy)
        migrate(legacy, self.docuverse, lattice_name="test")

    def test_returns_new_address_distinct_from_prev(self):
        store = Store(self.lattice_dir)
        v1 = store.addr_for_path("claim/A.md")
        v2 = store.register_version(v1)
        self.assertNotEqual(v1, v2)

    def test_path_reroutes_to_head(self):
        store = Store(self.lattice_dir)
        v1 = store.addr_for_path("claim/A.md")
        v2 = store.register_version(v1)
        # Same path now resolves to the new version
        self.assertEqual(store.addr_for_path("claim/A.md"), v2)
        # Old addr still has its (former) path in addr_to_path for
        # historical lookups
        self.assertEqual(store.path_for_addr(v1), "claim/A.md")
        self.assertEqual(store.path_for_addr(v2), "claim/A.md")

    def test_emits_supersession_link(self):
        store = Store(self.lattice_dir)
        v1 = store.addr_for_path("claim/A.md")
        v2 = store.register_version(v1)
        links = store.find_links(
            from_set=[v1], to_set=[v2], type_="supersession",
        )
        self.assertEqual(len(links), 1)

    def test_inherits_classifier_on_new_version(self):
        store = Store(self.lattice_dir)
        v1 = store.addr_for_path("claim/A.md")
        v2 = store.register_version(v1)
        # New version has its own claim classifier link
        classifiers = store.find_links(to_set=[v2], type_="claim")
        self.assertEqual(len(classifiers), 1)

    def test_persists_across_reload(self):
        store = Store(self.lattice_dir)
        v1 = store.addr_for_path("claim/A.md")
        v2 = store.register_version(v1)
        del store
        store2 = Store(self.lattice_dir)
        # Path still routes to head version after reload
        self.assertEqual(store2.addr_for_path("claim/A.md"), v2)
        # Supersession link survives
        links = store2.find_links(
            from_set=[v1], to_set=[v2], type_="supersession",
        )
        self.assertEqual(len(links), 1)


if __name__ == "__main__":
    unittest.main()
