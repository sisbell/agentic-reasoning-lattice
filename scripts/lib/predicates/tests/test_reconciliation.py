"""Tests for the reconciliation predicates.

Verifies orphan_sidecars, dangling_attribute_links, and the
claim/note finding orphan/dangling pairs detect the partial-failure
states described in docs/hypergraph-protocol/error-handling.md. The
predicates are detection-only; tests just check they correctly
identify which files/links are inconsistent.
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from lib.backend.emit import (
    emit_attribute_link, emit_claim, emit_comment, emit_finding, emit_note,
)
from lib.backend.store import Store
from lib.febe.session import Session
from lib.lattice.attributes import emit_attribute
from lib.predicates import (
    dangling_attribute_links,
    dangling_claim_finding_links,
    dangling_note_finding_links,
    orphan_claim_finding_docs,
    orphan_note_finding_docs,
    orphan_sidecars,
)


def _setup_lattice(tmp: Path) -> Path:
    """Create a minimal substrate-backed lattice in tmp."""
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


# ============================================================
#  Attribute reconciliation
# ============================================================


class OrphanSidecarsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        # macOS symlinks /var → /private/var; resolve up front so test
        # comparisons match the predicate's resolved paths.
        self.lattice = _setup_lattice(Path(self.tmp.name)).resolve()
        self.store = Store(self.lattice)
        self.session = Session(self.store)
        self.claim_dir = (
            self.lattice / "_docuverse" / "documents" / "claim" / "ASN-0099"
        )
        self.claim_dir.mkdir(parents=True)

    def test_no_orphans_when_clean(self):
        """A claim with a matching attribute link is not flagged."""
        claim_md = self.claim_dir / "T0.md"
        claim_md.write_text("# T0\n")
        emit_attribute(self.session, claim_md, "label", "T0")
        orphans = orphan_sidecars(self.session, self.claim_dir)
        self.assertEqual([], orphans)

    def test_orphan_file_no_link(self):
        """A sidecar file with no link is detected as orphan."""
        orphan = self.claim_dir / "Orphan.label.md"
        orphan.write_text("Orphan\n")
        orphans = orphan_sidecars(self.session, self.claim_dir)
        self.assertEqual([orphan], orphans)

    def test_orphan_after_retraction(self):
        """A sidecar whose link was retracted is flagged."""
        claim_md = self.claim_dir / "T1.md"
        claim_md.write_text("# T1\n")
        link, _ = emit_attribute(self.session, claim_md, "name", "T1Name")
        self.store.make_link(
            homedoc=link.homedoc,
            from_set=[],
            to_set=[link.addr],
            type_="retraction",
        )
        orphans = orphan_sidecars(self.session, self.claim_dir)
        sidecar = self.claim_dir / "T1.name.md"
        self.assertIn(sidecar, orphans)

    def test_non_sidecar_files_ignored(self):
        """Files not matching `<stem>.<kind>.md` aren't candidates."""
        (self.claim_dir / "T2.md").write_text("# T2\n")
        (self.claim_dir / "README.md").write_text("readme\n")
        self.assertEqual([], orphan_sidecars(self.session, self.claim_dir))


class DanglingAttributeLinksTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lattice = _setup_lattice(Path(self.tmp.name)).resolve()
        self.store = Store(self.lattice)
        self.session = Session(self.store)
        self.claim_dir = (
            self.lattice / "_docuverse" / "documents" / "claim" / "ASN-0099"
        )
        self.claim_dir.mkdir(parents=True)

    def test_no_dangling_when_clean(self):
        claim_md = self.claim_dir / "T0.md"
        claim_md.write_text("# T0\n")
        emit_attribute(self.session, claim_md, "label", "T0")
        self.assertEqual([], dangling_attribute_links(self.session))

    def test_dangling_when_file_deleted(self):
        """An attribute link whose target file is deleted is dangling."""
        claim_md = self.claim_dir / "T1.md"
        claim_md.write_text("# T1\n")
        link, _ = emit_attribute(self.session, claim_md, "label", "T1")
        sidecar = self.claim_dir / "T1.label.md"
        sidecar.unlink()
        dangling = dangling_attribute_links(self.session)
        addrs = [d.addr for d in dangling]
        self.assertIn(link.addr, addrs)

    def test_retracted_link_not_dangling(self):
        """Retracted links don't count — they're inactive."""
        claim_md = self.claim_dir / "T2.md"
        claim_md.write_text("# T2\n")
        link, _ = emit_attribute(self.session, claim_md, "name", "T2Name")
        self.store.make_link(
            homedoc=link.homedoc,
            from_set=[],
            to_set=[link.addr],
            type_="retraction",
        )
        sidecar = self.claim_dir / "T2.name.md"
        sidecar.unlink()
        self.assertEqual([], dangling_attribute_links(self.session))


# ============================================================
#  Claim-layer finding reconciliation
# ============================================================


class ClaimFindingOrphansTests(unittest.TestCase):
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

    def test_no_orphans_when_clean(self):
        finding_path = self.findings_dir / "0.md"
        finding_path.write_text("**ASN**: T0\n\nFinding body\n")
        finding_rel = str(finding_path.relative_to(self.lattice))
        finding_addr = self.store.register_path(finding_rel)
        emit_finding(self.store, finding_addr)
        emit_comment(
            self.store, finding_addr, self.claim_addr, kind="revise",
        )
        self.assertEqual(
            [], orphan_claim_finding_docs(self.session, self.findings_dir),
        )

    def test_orphan_finding_with_no_comment(self):
        orphan = self.findings_dir / "1.md"
        orphan.write_text("orphan finding\n")
        orphans = orphan_claim_finding_docs(self.session, self.findings_dir)
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
        self.store.make_link(
            homedoc=comment.homedoc,
            from_set=[],
            to_set=[comment.addr],
            type_="retraction",
        )
        orphans = orphan_claim_finding_docs(self.session, self.findings_dir)
        self.assertIn(finding_path, orphans)


class ClaimFindingDanglingTests(unittest.TestCase):
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
        self.assertEqual([], dangling_claim_finding_links(self.session))

    def test_dangling_when_finding_deleted(self):
        finding_path = self.findings_dir / "1.md"
        finding_path.write_text("body\n")
        finding_rel = str(finding_path.relative_to(self.lattice))
        finding_addr = self.store.register_path(finding_rel)
        comment = emit_comment(
            self.store, finding_addr, self.claim_addr, kind="revise",
        )
        finding_path.unlink()
        dangling = dangling_claim_finding_links(self.session)
        addrs = [d.addr for d in dangling]
        self.assertIn(comment.addr, addrs)


# ============================================================
#  Note-layer finding reconciliation
# ============================================================


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
            [], orphan_note_finding_docs(self.session, self.findings_dir),
        )

    def test_orphan_finding_no_comment(self):
        orphan = self.findings_dir / "1.md"
        orphan.write_text("orphan\n")
        orphans = orphan_note_finding_docs(self.session, self.findings_dir)
        self.assertEqual([orphan], orphans)

    def test_observe_comment_satisfies_orphan_check(self):
        finding_path = self.findings_dir / "2.md"
        finding_path.write_text("observe finding\n")
        finding_rel = str(finding_path.relative_to(self.lattice))
        finding_addr = self.store.register_path(finding_rel)
        emit_comment(
            self.store, finding_addr, self.note_addr, kind="observe",
        )
        self.assertEqual(
            [], orphan_note_finding_docs(self.session, self.findings_dir),
        )

    def test_out_of_scope_comment_satisfies_orphan_check(self):
        finding_path = self.findings_dir / "4.md"
        finding_path.write_text("oos finding\n")
        finding_rel = str(finding_path.relative_to(self.lattice))
        finding_addr = self.store.register_path(finding_rel)
        emit_comment(
            self.store, finding_addr, self.note_addr, kind="out-of-scope",
        )
        self.assertEqual(
            [], orphan_note_finding_docs(self.session, self.findings_dir),
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
        dangling = dangling_note_finding_links(self.session)
        addrs = [d.addr for d in dangling]
        self.assertIn(comment.addr, addrs)


if __name__ == "__main__":
    unittest.main()
