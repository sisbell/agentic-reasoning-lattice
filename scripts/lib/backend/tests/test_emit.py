"""Emit-helper tests — semantic substrate writes with idempotency."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from lib.backend.addressing import Address
from lib.backend.emit import (
    emit_attribute_link,
    emit_campaign,
    emit_citation,
    emit_claim,
    emit_classifier,
    emit_comment,
    emit_contract,
    emit_derivation,
    emit_inquiry,
    emit_label,
    emit_manages,
    emit_name,
    emit_note,
    emit_resolution,
    emit_retraction,
    emit_review,
    emit_synthesis,
)
from lib.lattice.attributes import emit_attribute
from lib.backend.migrate import migrate
from lib.predicates import is_doc_converged
from lib.backend.store import Store


def _setup_lattice(tmpdir: Path, paths: list[str]) -> Path:
    lattice_dir = tmpdir / "test_lattice"
    docuverse = lattice_dir / "_docuverse"
    docuverse.mkdir(parents=True)
    legacy = docuverse / "legacy_links.jsonl"
    records = []
    for i, p in enumerate(paths):
        records.append({
            "op": "create",
            "id": f"l_seed_{i}",
            "from_set": [],
            "to_set": [p],
            "type_set": ["claim"],
            "ts": "2026-01-01T00:00:00Z",
        })
    with open(legacy, "w") as f:
        for r in records:
            f.write(json.dumps(r, sort_keys=True) + "\n")
    migrate(legacy, docuverse, lattice_name="test")
    return lattice_dir


class ClassifierEmitTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        # Pre-seed two claims
        self.lattice = _setup_lattice(Path(self.tmp.name), ["claim/A.md", "claim/B.md"])
        self.store = Store(self.lattice)

    def test_emit_claim_idempotent_on_existing(self):
        a = self.store.addr_for_path("claim/A.md")
        # claim/A.md was migrated with a `claim` classifier already
        link, created = emit_claim(self.store, a)
        self.assertFalse(created)

    def test_emit_classifier_for_new_kind(self):
        a = self.store.addr_for_path("claim/A.md")
        link, created = emit_classifier(self.store, a, "review")
        self.assertTrue(created)
        # Re-emit returns the same link
        link2, created2 = emit_classifier(self.store, a, "review")
        self.assertFalse(created2)
        self.assertEqual(link.addr, link2.addr)

    def test_emit_contract_with_subtype(self):
        a = self.store.addr_for_path("claim/A.md")
        link, created = emit_contract(self.store, a, "axiom")
        self.assertTrue(created)

    def test_emit_contract_invalid_kind_raises(self):
        a = self.store.addr_for_path("claim/A.md")
        with self.assertRaises(ValueError):
            emit_contract(self.store, a, "not-a-kind")


class AttributeEmitTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lattice = _setup_lattice(Path(self.tmp.name), ["claim/A.md", "sidecar.md"])
        self.store = Store(self.lattice)
        self.a = self.store.addr_for_path("claim/A.md")
        self.sidecar = self.store.addr_for_path("sidecar.md")

    def test_emit_attribute_then_idempotent(self):
        link, created = emit_name(self.store, self.a, self.sidecar)
        self.assertTrue(created)
        link2, created2 = emit_name(self.store, self.a, self.sidecar)
        self.assertFalse(created2)
        self.assertEqual(link.addr, link2.addr)

    def test_emit_attribute_invalid_kind(self):
        with self.assertRaises(ValueError):
            emit_attribute_link(self.store, self.a, "not-real", self.sidecar)

    def test_label_description_signature(self):
        link_l, _ = emit_label(self.store, self.a, self.sidecar)
        link_d, _ = emit_attribute_link(
            self.store, self.a, "description", self.sidecar,
        )
        self.assertNotEqual(link_l.addr, link_d.addr)


class CitationEmitTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lattice = _setup_lattice(Path(self.tmp.name), ["claim/A.md", "claim/B.md"])
        self.store = Store(self.lattice)
        self.a = self.store.addr_for_path("claim/A.md")
        self.b = self.store.addr_for_path("claim/B.md")

    def test_emit_citation_default_depends(self):
        link, created = emit_citation(self.store, self.a, self.b)
        self.assertTrue(created)
        self.assertEqual(
            link.type_set,
            (self.store.state.types.address_for("citation.depends"),),
        )

    def test_emit_citation_idempotent(self):
        emit_citation(self.store, self.a, self.b)
        link2, created2 = emit_citation(self.store, self.a, self.b)
        self.assertFalse(created2)

    def test_emit_citation_forward_distinct_from_depends(self):
        d, _ = emit_citation(self.store, self.a, self.b, direction="depends")
        f, _ = emit_citation(self.store, self.a, self.b, direction="forward")
        self.assertNotEqual(d.addr, f.addr)

    def test_emit_citation_invalid_direction(self):
        with self.assertRaises(ValueError):
            emit_citation(self.store, self.a, self.b, direction="bogus")


class RetractionEmitTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lattice = _setup_lattice(Path(self.tmp.name), ["claim/A.md", "claim/B.md"])
        self.store = Store(self.lattice)
        self.a = self.store.addr_for_path("claim/A.md")
        self.b = self.store.addr_for_path("claim/B.md")

    def test_emit_retraction_targets_link(self):
        cite, _ = emit_citation(self.store, self.a, self.b)
        retract = emit_retraction(self.store, self.a, cite.addr)
        self.assertEqual(retract.to_set, (cite.addr,))


class CommentResolutionEmitTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lattice = _setup_lattice(Path(self.tmp.name), ["claim/A.md", "review.md"])
        self.store = Store(self.lattice)
        self.claim = self.store.addr_for_path("claim/A.md")
        self.review = self.store.addr_for_path("review.md")

    def test_review_revise_resolution_cycle(self):
        from lib.protocols.febe.session import Session
        session = Session(self.store)
        # Review files a revise comment
        comment = emit_comment(
            self.store, self.review, self.claim, kind="revise",
        )
        # Initially not converged
        self.assertFalse(is_doc_converged(session, self.claim))
        # File a resolution closing the comment
        emit_resolution(self.store, self.claim, comment.addr, kind="edit")
        # Now converged
        self.assertTrue(is_doc_converged(session, self.claim))


class ProvenanceEmitTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lattice = _setup_lattice(
            Path(self.tmp.name),
            ["note.md", "claim.md", "inquiry.md"],
        )
        self.store = Store(self.lattice)

    def test_emit_derivation_idempotent(self):
        note = self.store.addr_for_path("note.md")
        claim = self.store.addr_for_path("claim.md")
        link, created = emit_derivation(self.store, note, claim)
        self.assertTrue(created)
        link2, created2 = emit_derivation(self.store, note, claim)
        self.assertFalse(created2)
        self.assertEqual(link.addr, link2.addr)

    def test_emit_synthesis_idempotent(self):
        inquiry = self.store.addr_for_path("inquiry.md")
        note = self.store.addr_for_path("note.md")
        link, created = emit_synthesis(self.store, inquiry, note)
        self.assertTrue(created)
        link2, created2 = emit_synthesis(self.store, inquiry, note)
        self.assertFalse(created2)


class AgentEmitTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lattice = _setup_lattice(Path(self.tmp.name), ["agent.md", "claim.md"])
        self.store = Store(self.lattice)
        self.agent = self.store.addr_for_path("agent.md")
        self.claim = self.store.addr_for_path("claim.md")

    def test_emit_manages_not_idempotent(self):
        # Each operation gets its own manages link
        cite, _ = emit_citation(self.store, self.agent, self.claim)
        m1 = emit_manages(self.store, self.agent, cite.addr)
        m2 = emit_manages(self.store, self.agent, cite.addr)
        self.assertNotEqual(m1.addr, m2.addr)


if __name__ == "__main__":
    unittest.main()
