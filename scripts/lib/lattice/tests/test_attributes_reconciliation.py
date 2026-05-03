"""Tests for the reconciliation predicates in lib.lattice.attributes.

Verifies orphan_sidecars and dangling_attribute_links detect the
partial-failure states described in
docs/hypergraph-protocol/error-handling.md. The predicates are
detection-only; tests just check they correctly identify which
files/links are inconsistent.
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from lib.backend.addressing import Address
from lib.backend.emit import emit_attribute_link
from lib.backend.store import Store
from lib.febe.session import Session
from lib.lattice.attributes import (
    dangling_attribute_links,
    emit_attribute,
    orphan_sidecars,
)


def _setup_lattice(tmp: Path) -> Path:
    """Create a minimal substrate-backed lattice in tmp."""
    docuverse = tmp / "_docuverse"
    docuverse.mkdir()
    # Minimal paths.json with the registry doc address pre-allocated
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


class OrphanSidecarsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        # macOS symlinks /var → /private/var; resolve up front so test
        # comparisons match the predicate's resolved paths.
        self.lattice = _setup_lattice(Path(self.tmp.name)).resolve()
        self.store = Store(self.lattice)
        self.session = Session(self.store)
        self.claim_dir = self.lattice / "_docuverse" / "documents" / "claim" / "ASN-0099"
        self.claim_dir.mkdir(parents=True)

    def test_no_orphans_when_clean(self):
        """A claim with a matching attribute link is not flagged."""
        claim_md = self.claim_dir / "T0.md"
        claim_md.write_text("# T0\n")
        emit_attribute(self.session, claim_md, "label", "T0")
        # Sidecar file exists; substrate link points at it
        orphans = orphan_sidecars(self.session, self.claim_dir)
        self.assertEqual([], orphans)

    def test_orphan_file_no_link(self):
        """A sidecar file with no link is detected as orphan."""
        # Manually create a sidecar without going through emit_attribute
        # (simulates partial-failure: doc write succeeded, link failed)
        orphan = self.claim_dir / "Orphan.label.md"
        orphan.write_text("Orphan\n")
        orphans = orphan_sidecars(self.session, self.claim_dir)
        self.assertEqual([orphan], orphans)

    def test_orphan_after_retraction(self):
        """A sidecar whose link was retracted is flagged.

        Different kind of orphan than the partial-failure case but
        still inconsistent: substrate cleared, file lingers.
        """
        claim_md = self.claim_dir / "T1.md"
        claim_md.write_text("# T1\n")
        link, _ = emit_attribute(self.session, claim_md, "name", "T1Name")
        # Now retract the attribute link by emitting a retraction
        self.store.make_link(
            homedoc=link.homedoc,
            from_set=[],
            to_set=[link.addr],
            type_="retraction",
        )
        # The sidecar file remains; its link is no longer active
        orphans = orphan_sidecars(self.session, self.claim_dir)
        sidecar = self.claim_dir / "T1.name.md"
        self.assertIn(sidecar, orphans)

    def test_non_sidecar_files_ignored(self):
        """Files not matching `<stem>.<kind>.md` aren't candidates."""
        (self.claim_dir / "T2.md").write_text("# T2\n")
        (self.claim_dir / "README.md").write_text("readme\n")
        # Neither is a sidecar — neither should appear
        self.assertEqual([], orphan_sidecars(self.session, self.claim_dir))


class DanglingAttributeLinksTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lattice = _setup_lattice(Path(self.tmp.name)).resolve()
        self.store = Store(self.lattice)
        self.session = Session(self.store)
        self.claim_dir = self.lattice / "_docuverse" / "documents" / "claim" / "ASN-0099"
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
        # Delete the sidecar without retracting the link
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
        # Retract the link
        self.store.make_link(
            homedoc=link.homedoc,
            from_set=[],
            to_set=[link.addr],
            type_="retraction",
        )
        # Now delete the file too
        sidecar = self.claim_dir / "T2.name.md"
        sidecar.unlink()
        # The link is retracted (inactive); shouldn't appear as dangling
        self.assertEqual([], dangling_attribute_links(self.session))


if __name__ == "__main__":
    unittest.main()
