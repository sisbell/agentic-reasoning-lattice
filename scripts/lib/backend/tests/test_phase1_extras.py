"""Phase 1 extras: AgentStore, populate, sync."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from lib.backend.addressing import Address
from lib.backend.agent_store import AgentStore
from lib.backend.emit import emit_citation
from lib.backend.migrate import migrate
from lib.lattice.labels import (
    aggregate_asn_deps,
    build_cross_asn_label_index,
    build_note_label_index,
    note_dep_asn_ids,
    is_note_path,
)
from lib.backend.predicates import active_links
from lib.backend.store import Store
from lib.backend.sync import sync_claim_citations


def _seed_lattice_with_substrate(
    tmpdir: Path,
    legacy_records: list,
    *,
    sidecar_files: dict | None = None,
) -> Path:
    """Build a fresh lattice tree, seed legacy JSONL, migrate.

    `sidecar_files` maps relative paths to their content (one line each).
    Used to populate label sidecars whose first line is the canonical
    label string.
    """
    lattice_dir = tmpdir / "test_lattice"
    docuverse = lattice_dir / "_docuverse"
    docuverse.mkdir(parents=True)
    legacy = docuverse / "legacy_links.jsonl"
    with open(legacy, "w") as f:
        for r in legacy_records:
            f.write(json.dumps(r, sort_keys=True) + "\n")
    migrate(legacy, docuverse, lattice_name="test")
    if sidecar_files:
        for rel, content in sidecar_files.items():
            full = lattice_dir / rel
            full.parent.mkdir(parents=True, exist_ok=True)
            full.write_text(content)
    return lattice_dir


class AgentStoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        records = [
            {
                "op": "create", "id": f"l_{i}",
                "from_set": [], "to_set": [p], "type_set": ["claim"],
                "ts": "2026-01-01T00:00:00Z",
            }
            for i, p in enumerate([
                "agents/cone-review.md",
                "claim/A.md",
                "claim/B.md",
            ])
        ]
        self.lattice = _seed_lattice_with_substrate(Path(self.tmp.name), records)
        self.store = Store(self.lattice)
        self.agent = self.store.addr_for_path("agents/cone-review.md")

    def test_agent_store_files_agent_classifier_on_init(self):
        AgentStore(self.store, self.agent)
        agent_classifiers = active_links(
            self.store.state, "agent", to_set=[self.agent],
        )
        self.assertEqual(len(agent_classifiers), 1)

    def test_make_link_auto_emits_manages(self):
        agent_store = AgentStore(self.store, self.agent)
        a = self.store.addr_for_path("claim/A.md")
        b = self.store.addr_for_path("claim/B.md")
        before = len(self.store.find_links(type_="manages"))
        link = agent_store.make_link(a, [a], [b], "citation.depends")
        after = len(self.store.find_links(type_="manages"))
        self.assertEqual(after, before + 1)
        # The manages link points at the citation we just made
        manages = self.store.find_links(
            from_set=[self.agent], to_set=[link.addr], type_="manages",
        )
        self.assertEqual(len(manages), 1)

    def test_manages_skipped_for_manages_and_agent(self):
        agent_store = AgentStore(self.store, self.agent)
        a = self.store.addr_for_path("claim/A.md")
        before = len(self.store.find_links(type_="manages"))
        # Direct manages emission: shouldn't get auto-attributed (would recurse)
        agent_store.make_link(self.agent, [self.agent], [a], "manages")
        after = len(self.store.find_links(type_="manages"))
        self.assertEqual(after, before + 1)  # only the explicit one


class PopulateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        # Set up: claim T0 with a label sidecar carrying the string "T0"
        records = [
            {
                "op": "create", "id": "l_classify_t0",
                "from_set": [],
                "to_set": ["_docuverse/documents/claim/ASN-0034/T0.md"],
                "type_set": ["claim"], "ts": "ts",
            },
            {
                "op": "create", "id": "l_label_t0",
                "from_set": ["_docuverse/documents/claim/ASN-0034/T0.md"],
                "to_set": ["_docuverse/documents/claim/ASN-0034/T0.label.md"],
                "type_set": ["label"], "ts": "ts",
            },
            # Note doc
            {
                "op": "create", "id": "l_note_34",
                "from_set": [],
                "to_set": ["_docuverse/documents/note/ASN-0034.md"],
                "type_set": ["note"], "ts": "ts",
            },
            # Cross-ASN dependency: T0 depends on something in ASN-0036
            {
                "op": "create", "id": "l_classify_other",
                "from_set": [],
                "to_set": ["_docuverse/documents/claim/ASN-0036/Foo.md"],
                "type_set": ["claim"], "ts": "ts",
            },
            {
                "op": "create", "id": "l_dep",
                "from_set": ["_docuverse/documents/claim/ASN-0034/T0.md"],
                "to_set": ["_docuverse/documents/claim/ASN-0036/Foo.md"],
                "type_set": ["citation.depends"], "ts": "ts",
            },
        ]
        sidecars = {
            "_docuverse/documents/claim/ASN-0034/T0.label.md": "T0\n",
        }
        self.lattice = _seed_lattice_with_substrate(
            Path(self.tmp.name), records, sidecar_files=sidecars,
        )
        self.store = Store(self.lattice)

    def test_label_index_resolves_via_sidecar_content(self):
        index = build_cross_asn_label_index(self.store)
        self.assertIn("T0", index)
        # Should map to the claim doc itself, not the sidecar
        t0 = self.store.addr_for_path(
            "_docuverse/documents/claim/ASN-0034/T0.md",
        )
        self.assertEqual(index["T0"], t0)

    def test_note_label_index_extracts_asn(self):
        index = build_note_label_index(self.store)
        self.assertIn("ASN-0034", index)
        note = self.store.addr_for_path(
            "_docuverse/documents/note/ASN-0034.md",
        )
        self.assertEqual(index["ASN-0034"], note)

    def test_aggregate_asn_deps_excludes_self(self):
        deps = aggregate_asn_deps(self.store, "ASN-0034")
        # ASN-0034's claim T0 cites ASN-0036/Foo.md
        self.assertEqual(deps, [36])

    def test_is_note_path(self):
        self.assertTrue(is_note_path("_docuverse/documents/note/ASN-0034.md"))
        self.assertFalse(is_note_path("_docuverse/documents/claim/ASN-0034/T0.md"))


class SyncCitationsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        # T0 cites Foo currently in substrate. We'll set up md with Bar
        # in *Depends:*; sync should retract Foo and add Bar.
        records = [
            {
                "op": "create", "id": "l_classify_t0",
                "from_set": [],
                "to_set": ["claim/A.md"],
                "type_set": ["claim"], "ts": "ts",
            },
            {
                "op": "create", "id": "l_classify_foo",
                "from_set": [], "to_set": ["claim/Foo.md"],
                "type_set": ["claim"], "ts": "ts",
            },
            {
                "op": "create", "id": "l_classify_bar",
                "from_set": [], "to_set": ["claim/Bar.md"],
                "type_set": ["claim"], "ts": "ts",
            },
            {
                "op": "create", "id": "l_label_foo",
                "from_set": ["claim/Foo.md"],
                "to_set": ["claim/Foo.label.md"],
                "type_set": ["label"], "ts": "ts",
            },
            {
                "op": "create", "id": "l_label_bar",
                "from_set": ["claim/Bar.md"],
                "to_set": ["claim/Bar.label.md"],
                "type_set": ["label"], "ts": "ts",
            },
            {
                "op": "create", "id": "l_dep_foo",
                "from_set": ["claim/A.md"], "to_set": ["claim/Foo.md"],
                "type_set": ["citation.depends"], "ts": "ts",
            },
        ]
        sidecars = {
            "claim/Foo.label.md": "Foo\n",
            "claim/Bar.label.md": "Bar\n",
            "claim/A.md": (
                "# Claim A\n\n"
                "- *Depends:*\n"
                "  - Bar — for proof\n\n"
                "Body.\n"
            ),
        }
        self.lattice = _seed_lattice_with_substrate(
            Path(self.tmp.name), records, sidecar_files=sidecars,
        )
        self.store = Store(self.lattice)

    def test_sync_adds_md_only_and_retracts_substrate_only(self):
        label_index = build_cross_asn_label_index(self.store)
        a = self.store.addr_for_path("claim/A.md")
        changes = sync_claim_citations(self.store, a, label_index)
        self.assertIn("Bar", changes["depends"]["added"])
        self.assertIn("Foo", changes["depends"]["retracted"])

        # Verify substrate state
        active_deps = active_links(
            self.store.state, "citation.depends", from_set=[a],
        )
        # Should only have Bar now
        bar_addr = self.store.addr_for_path("claim/Bar.md")
        live_targets = {tgt for link in active_deps for tgt in link.to_set}
        self.assertEqual(live_targets, {bar_addr})


if __name__ == "__main__":
    unittest.main()
