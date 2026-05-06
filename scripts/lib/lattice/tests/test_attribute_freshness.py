"""Tests for attribute-emission patterns vs freshness predicates.

Three sidecar kinds (description, signature, statements) have
chain-comparison freshness predicates: predicate is True iff
sidecar's supersession chain is at least as long as the claim/note's.

The relaxed-model rule: chains advance only where a predicate
consumes them, and the caller is responsible for opting in.
emit_attribute does NOT advance the chain on subsequent calls — it
just writes the file and emits/looks-up the link. Callers whose
attribute kind has a freshness predicate must therefore branch:
first-time → emit_attribute; subsequent → register_version + write.

This test guards the pattern at the substrate level. If a future
caller skips register_version on subsequent emissions, the agent's
predicate will stay False forever and the runner will re-fire the
trigger until max_iterations. That's the bug shape this regression
test catches at the primitive level.
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from lib.backend.store import Store
from lib.protocols.febe.session import Session
from lib.lattice.attributes import emit_attribute
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


class AttributeChainAdvanceTest(unittest.TestCase):
    """Verify the create-or-advance dance keeps chain-based predicates
    convergent.

    The agent pattern (used by claim_describe, note_statements,
    signature_resolve, substrate/description.py CLI):

        sidecar_addr = <kind>_sidecar_of(session, claim_addr)
        if sidecar_addr is None:
            emit_attribute(session, claim_path, kind, body)
        else:
            session.register_version(sidecar_addr)
            <write the new body to the sidecar's path>

    Without the register_version branch, signature_is_fresh stays
    False after any claim edit because the sidecar's chain stays at 1.
    """

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

    def _emit_or_advance_signature(self, body):
        """Mirror the agent's emission pattern."""
        claim_addr = self._claim_addr()
        sidecar_addr = signature_sidecar_of(self.session, claim_addr)
        if sidecar_addr is None:
            emit_attribute(self.session, self.claim_md, "signature", body)
        else:
            self.session.register_version(sidecar_addr)
            sidecar_path = self.session.get_path_for_addr(sidecar_addr)
            full = self.session.store.lattice_dir / sidecar_path
            full.write_text(body.rstrip() + "\n")

    def test_first_emit_creates_at_chain_one(self):
        self._emit_or_advance_signature("- `nat`: ℕ")
        sidecar_addr = signature_sidecar_of(self.session, self._claim_addr())
        self.assertEqual(
            supersession_chain_length(self.session, sidecar_addr), 1,
        )
        self.assertTrue(signature_is_fresh(self.session, self._claim_addr()))

    def test_claim_edit_invalidates_predicate(self):
        self._emit_or_advance_signature("- `nat`: ℕ")
        self.session.register_version(self._claim_addr())
        self.assertFalse(
            signature_is_fresh(self.session, self._claim_addr()),
            "stale: claim edited, sidecar not yet re-attested",
        )

    def test_subsequent_emit_advances_chain_and_restores_freshness(self):
        # First fire.
        self._emit_or_advance_signature("- `nat`: ℕ")
        sidecar_addr = signature_sidecar_of(self.session, self._claim_addr())

        # Claim is edited (refiner accept): claim chain → 2.
        self.session.register_version(self._claim_addr())
        self.assertFalse(signature_is_fresh(self.session, self._claim_addr()))

        # Subsequent fire: agent uses the register_version path.
        self._emit_or_advance_signature("- `nat`: ℕ\n- `succ`: ℕ→ℕ")

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


if __name__ == "__main__":
    unittest.main()
