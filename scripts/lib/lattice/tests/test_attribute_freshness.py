"""Tests for attest_attribute and freshness predicates.

Three sidecar kinds (description, signature, statements) have
chain-comparison freshness predicates: True iff sidecar's
supersession chain is at least as long as the claim/note's.

attest_attribute is the create-or-advance helper that all sidecar
emissions go through. First-time creates link + sidecar at chain
length 1; subsequent advances the chain by 1 via register_version
and writes the new content. The chain advance encodes "I checked
at this revision," which is meaningful even when the new content
matches the old (no-op LLM output still counts as an attestation).

These tests guard the create-or-advance contract. Skip the advance
and the freshness predicate stays False after any source edit; the
runner re-fires until max_iterations.
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from lib.backend.store import Store
from lib.protocols.febe.session import Session
from lib.lattice.attributes import attest_attribute
from lib.predicates.attributes import (
    signature_is_fresh, signature_sidecar_of,
)
from lib.predicates.versions import supersession_chain_length


def _setup_lattice(tmp):
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


class AttestAttributeTest(unittest.TestCase):
    """Verify attest_attribute's create-or-advance contract."""

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
        self.claim_md = self.claim_dir / "T0.md"
        self.claim_md.write_text("# T0\n\nFormal Contract: ...\n")

    def _claim_addr(self):
        return self.session.get_addr_for_path(
            str(self.claim_md.relative_to(self.lattice))
        )

    def test_first_emit_creates_link_at_chain_one(self):
        link, created = attest_attribute(
            self.session, self.claim_md, "signature", "- `nat`: ℕ",
        )
        self.assertTrue(created, "first call freshly emits the link")
        sidecar_addr = signature_sidecar_of(self.session, self._claim_addr())
        self.assertEqual(
            supersession_chain_length(self.session, sidecar_addr), 1,
        )
        self.assertTrue(signature_is_fresh(self.session, self._claim_addr()))

    def test_claim_edit_invalidates_predicate(self):
        attest_attribute(self.session, self.claim_md, "signature", "- `nat`: ℕ")
        self.session.register_version(self._claim_addr())
        self.assertFalse(
            signature_is_fresh(self.session, self._claim_addr()),
            "stale: claim edited, sidecar not yet re-attested",
        )

    def test_subsequent_emit_advances_chain_and_restores_freshness(self):
        # First fire.
        attest_attribute(self.session, self.claim_md, "signature", "- `nat`: ℕ")
        sidecar_addr = signature_sidecar_of(self.session, self._claim_addr())

        # Claim is edited (refiner accept): claim chain → 2.
        self.session.register_version(self._claim_addr())
        self.assertFalse(signature_is_fresh(self.session, self._claim_addr()))

        # Subsequent fire: attest_attribute advances the sidecar chain.
        link, created = attest_attribute(
            self.session, self.claim_md, "signature",
            "- `nat`: ℕ\n- `succ`: ℕ→ℕ",
        )
        self.assertFalse(created, "subsequent call returns existing link")

        self.assertEqual(
            supersession_chain_length(self.session, sidecar_addr), 2,
            "sidecar chain advanced via register_version",
        )
        self.assertTrue(
            signature_is_fresh(self.session, self._claim_addr()),
            "predicate True after subsequent fire — no re-fire loop",
        )

        # Side-effect: file content is updated.
        sidecar_file = self.claim_dir / "T0.signature.md"
        self.assertIn("succ", sidecar_file.read_text())

    def test_subsequent_emit_with_unchanged_content_still_advances(self):
        """Even when the LLM produces no delta, the chain ticks.

        The chain encodes "I checked at this revision," not "content
        changed." A no-op fire is still an attestation.
        """
        attest_attribute(self.session, self.claim_md, "signature", "- `nat`: ℕ")
        sidecar_addr = signature_sidecar_of(self.session, self._claim_addr())

        self.session.register_version(self._claim_addr())

        # Re-attest with identical content (no delta from LLM).
        attest_attribute(self.session, self.claim_md, "signature", "- `nat`: ℕ")

        self.assertEqual(
            supersession_chain_length(self.session, sidecar_addr), 2,
            "chain advanced even though sidecar content unchanged",
        )
        self.assertTrue(signature_is_fresh(self.session, self._claim_addr()))


if __name__ == "__main__":
    unittest.main()
