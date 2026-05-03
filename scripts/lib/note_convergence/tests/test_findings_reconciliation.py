"""Tests for note-layer finding reconciliation predicates.

Same shape as the claim-layer tests but for note-convergence
comment subtypes (revise, out-of-scope).
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from lib.backend.emit import emit_comment, emit_finding, emit_note
from lib.backend.store import Store
from lib.febe.session import Session
from lib.note_convergence.findings import (
    dangling_finding_links,
    orphan_finding_docs,
)


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


class NoteFindingReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lattice = _setup_lattice(Path(self.tmp.name)).resolve()
        self.store = Store(self.lattice)
        self.session = Session(self.store)
        self.findings_dir = (
            self.lattice / "_docuverse" / "documents" / "finding"
            / "notes" / "ASN-0099" / "review-1"
        )
        self.findings_dir.mkdir(parents=True)
        # A note doc as comment target
        self.note_path = (
            self.lattice / "_docuverse" / "documents" / "note" / "ASN-0099.md"
        )
        self.note_path.parent.mkdir(parents=True)
        self.note_path.write_text("# Note ASN-0099\n")
        self.note_addr = self.store.register_path(
            str(self.note_path.relative_to(self.lattice))
        )
        emit_note(self.store, self.note_addr)

    def test_no_orphans_when_clean(self):
        finding_path = self.findings_dir / "0.md"
        finding_path.write_text("finding body\n")
        finding_rel = str(finding_path.relative_to(self.lattice))
        finding_addr = self.store.register_path(finding_rel)
        emit_finding(self.store, finding_addr)
        emit_comment(
            self.store, finding_addr, self.note_addr, kind="revise",
        )
        self.assertEqual(
            [], orphan_finding_docs(self.session, self.findings_dir),
        )

    def test_orphan_finding_no_comment(self):
        orphan = self.findings_dir / "1.md"
        orphan.write_text("orphan\n")
        orphans = orphan_finding_docs(self.session, self.findings_dir)
        self.assertEqual([orphan], orphans)

    def test_observe_comment_satisfies_orphan_check(self):
        # observe comments also count as a valid finding-source link
        finding_path = self.findings_dir / "2.md"
        finding_path.write_text("observe finding\n")
        finding_rel = str(finding_path.relative_to(self.lattice))
        finding_addr = self.store.register_path(finding_rel)
        emit_comment(
            self.store, finding_addr, self.note_addr, kind="observe",
        )
        self.assertEqual(
            [], orphan_finding_docs(self.session, self.findings_dir),
        )

    def test_dangling_when_finding_deleted(self):
        finding_path = self.findings_dir / "3.md"
        finding_path.write_text("body\n")
        finding_rel = str(finding_path.relative_to(self.lattice))
        finding_addr = self.store.register_path(finding_rel)
        comment = emit_comment(
            self.store, finding_addr, self.note_addr, kind="revise",
        )
        finding_path.unlink()
        dangling = dangling_finding_links(self.session)
        addrs = [d.addr for d in dangling]
        self.assertIn(comment.addr, addrs)


if __name__ == "__main__":
    unittest.main()
