"""Predicate-audit tests: cone_review and full_review skip when
Formal Contract sections are missing.

Both triggers gate the LLM-driven content review on every in-scope
claim having a `*Formal Contract:*` section in its body. Without
that, there's nothing substantive to review — the agent would burn
tokens producing reviews of a contract-less stub.

The predicates read the file directly via `has_formal_contract`,
so these tests use a tempfile-backed lattice with real claim files.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from lib.backend.store import Store
from lib.protocols.febe.session import Session
from lib.triggers.cone_review import _predicate as cone_review_predicate
from lib.triggers.full_review import _predicate as full_review_predicate


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


class ConeReviewFormalContractGate(unittest.TestCase):
    """cone_review must skip a claim whose body lacks a Formal Contract."""

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

    def _register_claim(self, name: str, body: str) -> "Address":
        from lib.backend.emit import emit_claim
        path = self.claim_dir / f"{name}.md"
        path.write_text(body)
        rel = str(path.relative_to(self.lattice))
        addr = self.session.register_path(rel)
        emit_claim(self.store, addr)
        return addr

    def test_skips_when_no_formal_contract_section(self):
        """Claim body without `*Formal Contract:*` → predicate True (skip)."""
        addr = self._register_claim(
            "T0", "# T0\n\nSome prose, no Formal Contract.\n",
        )
        self.assertTrue(cone_review_predicate(self.session, addr))

    def test_skips_when_no_path_registered(self):
        """No claim file at all → predicate True (skip)."""
        # Create an unregistered address by storing a doc without a path.
        from lib.backend.emit import emit_claim
        unregistered = self.session.register_path(
            "_docuverse/documents/claim/ASN-0099/missing.md",
        )
        emit_claim(self.store, unregistered)
        # The path is registered but the file doesn't exist on disk.
        self.assertTrue(cone_review_predicate(self.session, unregistered))

    def test_does_not_skip_on_fc_alone_falls_through_to_other_gates(self):
        """When a Formal Contract IS present but other skip conditions
        also apply, the FC gate doesn't blanket-skip — the predicate
        evaluates the rest of the chain. With no upstream and no
        review yet, the predicate fires (returns False)."""
        addr = self._register_claim(
            "T0",
            "# T0\n\n*Formal Contract:*\n- *Postconditions:* something\n",
        )
        # No upstream (vacuously settled), not confirmed, quiescent
        # (no comments) → predicate False (fire).
        self.assertFalse(cone_review_predicate(self.session, addr))


class FullReviewFormalContractGate(unittest.TestCase):
    """full_review must skip when any derived claim lacks a Formal
    Contract."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lattice = _setup_lattice(Path(self.tmp.name)).resolve()
        self.store = Store(self.lattice)
        self.session = Session(self.store)
        self.claim_dir = (
            self.lattice / "_docuverse" / "documents" / "claim" / "ASN-0099"
        )
        self.note_dir = (
            self.lattice / "_docuverse" / "documents" / "note" / "ASN-0099"
        )
        self.claim_dir.mkdir(parents=True)
        self.note_dir.mkdir(parents=True)
        # Register a note doc.
        note_path = self.note_dir / "ASN-0099-note.md"
        note_path.write_text("# Note\n")
        from lib.backend.emit import emit_note
        rel = str(note_path.relative_to(self.lattice))
        self.note_addr = self.session.register_path(rel)
        emit_note(self.store, self.note_addr)

    def _register_claim(self, name: str, body: str) -> "Address":
        from lib.backend.emit import emit_claim, emit_derivation
        path = self.claim_dir / f"{name}.md"
        path.write_text(body)
        rel = str(path.relative_to(self.lattice))
        addr = self.session.register_path(rel)
        emit_claim(self.store, addr)
        emit_derivation(self.store, self.note_addr, addr)
        return addr

    def test_skips_when_one_derived_claim_lacks_fc(self):
        """Two claims derived; one has FC, the other doesn't →
        predicate True (skip).
        """
        self._register_claim(
            "T0",
            "# T0\n\n*Formal Contract:*\n- *Postconditions:* x\n",
        )
        self._register_claim("T1", "# T1\n\nNo formal contract here.\n")
        self.assertTrue(full_review_predicate(self.session, self.note_addr))

    def test_does_not_skip_on_fc_alone_when_all_claims_have_fc(self):
        """All derived claims have FC; ASN quiescent (no comments);
        not yet confirmed → predicate False (fire)."""
        self._register_claim(
            "T0",
            "# T0\n\n*Formal Contract:*\n- *Postconditions:* x\n",
        )
        self._register_claim(
            "T1",
            "# T1\n\n*Formal Contract:*\n- *Postconditions:* y\n",
        )
        self.assertFalse(full_review_predicate(self.session, self.note_addr))

    def test_no_derived_claims_skips_via_vacuous_confirmation(self):
        """Note with no claim-classified derivations → `is_asn_confirmed`
        returns True vacuously (`all` over empty), predicate skips
        before reaching the FC gate."""
        self.assertTrue(full_review_predicate(self.session, self.note_addr))


if __name__ == "__main__":
    unittest.main()
