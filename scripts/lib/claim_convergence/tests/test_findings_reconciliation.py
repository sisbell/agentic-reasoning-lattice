"""Tests for claim-layer finding reconciliation predicates.

Verifies orphan_finding_docs and dangling_finding_links detect
partial-failure states in the claim-convergence finding pipeline
(per docs/hypergraph-protocol/error-handling.md).
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from lib.backend.addressing import Address
from lib.backend.emit import emit_claim, emit_comment, emit_finding
from lib.backend.store import Store
from lib.claim_convergence.findings import (
    dangling_finding_links,
    orphan_finding_docs,
)
from lib.febe.session import Session


def _setup_lattice(tmp: Path) -> Path:
    docuverse = tmp / "_docuverse"
    docuverse.mkdir()
    paths = {
        "_meta": {
            "registry_doc": "1.1.0.1.0.1",
            "lattice_doc": "1.1.0.1.0.1.1",
            "lattice_name": "test",
        },
        "paths": {},
    }
    (docuverse / "paths.json").write_text(json.dumps(paths, indent=2))
    (docuverse / "links.jsonl").write_text("")
    return tmp


class OrphanFindingDocsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lattice = _setup_lattice(Path(self.tmp.name)).resolve()
        self.store = Store(self.lattice)
        self.session = Session(self.store)
        self.findings_dir = (
            self.lattice / "_docuverse" / "documents" / "finding"
            / "claims" / "ASN-0099" / "review-1"
        )
        self.findings_dir.mkdir(parents=True)
        # A claim doc to be the comment target
        self.claim_path = (
            self.lattice / "_docuverse" / "documents" / "claim"
            / "ASN-0099" / "T0.md"
        )
        self.claim_path.parent.mkdir(parents=True)
        self.claim_path.write_text("# T0\n")
        self.claim_addr = self.store.register_path(
            str(self.claim_path.relative_to(self.lattice))
        )
        emit_claim(self.store, self.claim_addr)

    def test_no_orphans_when_clean(self):
        # Finding doc with comment link → not orphan
        finding_path = self.findings_dir / "0.md"
        finding_path.write_text("**ASN**: T0\n\nFinding body\n")
        finding_rel = str(finding_path.relative_to(self.lattice))
        finding_addr = self.store.register_path(finding_rel)
        emit_finding(self.store, finding_addr)
        emit_comment(
            self.store, finding_addr, self.claim_addr, kind="revise",
        )
        self.assertEqual(
            [], orphan_finding_docs(self.session, self.findings_dir),
        )

    def test_orphan_finding_with_no_comment(self):
        # Finding doc on disk; never registered, no comment link
        orphan = self.findings_dir / "1.md"
        orphan.write_text("orphan finding\n")
        orphans = orphan_finding_docs(self.session, self.findings_dir)
        self.assertEqual([orphan], orphans)

    def test_orphan_after_comment_retraction(self):
        finding_path = self.findings_dir / "2.md"
        finding_path.write_text("**ASN**: T0\n\nbody\n")
        finding_rel = str(finding_path.relative_to(self.lattice))
        finding_addr = self.store.register_path(finding_rel)
        emit_finding(self.store, finding_addr)
        comment = emit_comment(
            self.store, finding_addr, self.claim_addr, kind="revise",
        )
        # Retract the comment
        self.store.make_link(
            homedoc=comment.homedoc,
            from_set=[],
            to_set=[comment.addr],
            type_="retraction",
        )
        # Finding doc still on disk; substrate has no active comment from it
        orphans = orphan_finding_docs(self.session, self.findings_dir)
        self.assertIn(finding_path, orphans)


class DanglingFindingLinksTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lattice = _setup_lattice(Path(self.tmp.name)).resolve()
        self.store = Store(self.lattice)
        self.session = Session(self.store)
        self.findings_dir = (
            self.lattice / "_docuverse" / "documents" / "finding"
            / "claims" / "ASN-0099" / "review-1"
        )
        self.findings_dir.mkdir(parents=True)
        self.claim_path = (
            self.lattice / "_docuverse" / "documents" / "claim"
            / "ASN-0099" / "T0.md"
        )
        self.claim_path.parent.mkdir(parents=True)
        self.claim_path.write_text("# T0\n")
        self.claim_addr = self.store.register_path(
            str(self.claim_path.relative_to(self.lattice))
        )
        emit_claim(self.store, self.claim_addr)

    def test_no_dangling_when_clean(self):
        finding_path = self.findings_dir / "0.md"
        finding_path.write_text("body\n")
        finding_rel = str(finding_path.relative_to(self.lattice))
        finding_addr = self.store.register_path(finding_rel)
        emit_comment(
            self.store, finding_addr, self.claim_addr, kind="revise",
        )
        self.assertEqual([], dangling_finding_links(self.session))

    def test_dangling_when_finding_deleted(self):
        finding_path = self.findings_dir / "1.md"
        finding_path.write_text("body\n")
        finding_rel = str(finding_path.relative_to(self.lattice))
        finding_addr = self.store.register_path(finding_rel)
        comment = emit_comment(
            self.store, finding_addr, self.claim_addr, kind="revise",
        )
        # Delete the finding file without retracting the comment
        finding_path.unlink()
        dangling = dangling_finding_links(self.session)
        addrs = [d.addr for d in dangling]
        self.assertIn(comment.addr, addrs)


if __name__ == "__main__":
    unittest.main()
