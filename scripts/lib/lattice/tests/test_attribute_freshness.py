"""Tests for attest_against_doc_head and freshness predicates.

Three sidecar kinds (description, signature, statements) have
citation-anchor freshness predicates: True iff the sidecar's head
version emits a `citation.depends` to `version_head(doc)`.

`attest_against_doc_head` takes an explicit `content_changed` flag.
The producer signals from its own knowledge (LLM verdict, byte
compare, etc.) whether this fire produced a real edit:

  - content_changed=True  → register_version on existing sidecar +
                            attest + anchor citation
  - content_changed=False → no chain advance + attest (idempotent
                            file write) + anchor citation

The freshness predicate walks the citation anchor. The chain tracks
real edits; attestation events are the citation re-emission.

These tests guard the contract: predicate True after a fire (chain
advance or not); predicate False after the doc advances; predicate
True after re-firing against the new head; chain advances only when
content_changed is True.
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from lib.backend.store import Store
from lib.protocols.febe.session import Session
from lib.lattice.attributes import attest_against_doc_head
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


class AttestAgainstDocHeadTest(unittest.TestCase):
    """Verify attest_against_doc_head's contract: chain advance plus
    freshness-anchor citation, predicate flipping address-identity-
    wise."""

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
        # Register the claim md so claim_addr is available before
        # any attest call. attest_against_doc_head needs claim_addr
        # at call-time to emit the freshness anchor.
        self.session.register_path(
            str(self.claim_md.relative_to(self.lattice))
        )

    def _claim_addr(self):
        return self.session.get_addr_for_path(
            str(self.claim_md.relative_to(self.lattice))
        )

    def test_first_emit_creates_link_with_anchor(self):
        link, created = attest_against_doc_head(
            self.session, self.claim_md, "signature", "- `nat`: ℕ",
            self._claim_addr(),
            content_changed=True,
        )
        self.assertTrue(created, "first call freshly emits the link")
        sidecar_addr = signature_sidecar_of(self.session, self._claim_addr())
        self.assertEqual(
            supersession_chain_length(self.session, sidecar_addr), 1,
            "first emission creates chain at length 1; "
            "content_changed=True does not advance further on first emit",
        )
        self.assertTrue(signature_is_fresh(self.session, self._claim_addr()))

    def test_claim_edit_invalidates_predicate(self):
        attest_against_doc_head(
            self.session, self.claim_md, "signature", "- `nat`: ℕ",
            self._claim_addr(),
            content_changed=True,
        )
        self.session.register_version(self._claim_addr())
        self.assertFalse(
            signature_is_fresh(self.session, self._claim_addr()),
            "stale: claim advanced, sidecar's anchor cites old head",
        )

    def test_subsequent_with_content_changed_advances_chain(self):
        # First fire — anchor cites claim's identity (which is head).
        attest_against_doc_head(
            self.session, self.claim_md, "signature", "- `nat`: ℕ",
            self._claim_addr(),
            content_changed=True,
        )
        sidecar_addr = signature_sidecar_of(self.session, self._claim_addr())

        # Claim advances; old anchor now points at non-head.
        self.session.register_version(self._claim_addr())
        self.assertFalse(signature_is_fresh(self.session, self._claim_addr()))

        # Subsequent fire with content_changed=True: chain advance +
        # new anchor citing new head.
        link, created = attest_against_doc_head(
            self.session, self.claim_md, "signature",
            "- `nat`: ℕ\n- `succ`: ℕ→ℕ",
            self._claim_addr(),
            content_changed=True,
        )
        self.assertFalse(created, "subsequent call returns existing link")

        self.assertEqual(
            supersession_chain_length(self.session, sidecar_addr), 2,
            "sidecar chain advanced via register_version",
        )
        self.assertTrue(
            signature_is_fresh(self.session, self._claim_addr()),
            "predicate True after re-anchored fire",
        )

        # Side-effect: file content is updated.
        sidecar_file = self.claim_dir / "T0.signature.md"
        self.assertIn("succ", sidecar_file.read_text())

    def test_subsequent_with_content_unchanged_re_anchors_only(self):
        """Re-attesting with content_changed=False emits a new
        anchor citation but does NOT advance the sidecar chain.

        The producer signals via the flag whether its fire produced
        a real edit. False means no edit — the existing sidecar
        version stays head, the freshness anchor re-emits to point
        at the doc's new head, and the predicate flips True without
        chain churn.
        """
        attest_against_doc_head(
            self.session, self.claim_md, "signature", "- `nat`: ℕ",
            self._claim_addr(),
            content_changed=True,
        )
        sidecar_addr = signature_sidecar_of(self.session, self._claim_addr())

        # Doc advances; the sidecar's anchor now points at non-head.
        self.session.register_version(self._claim_addr())
        self.assertFalse(signature_is_fresh(self.session, self._claim_addr()))

        # Re-attest with content_changed=False (LLM verdict said no edit).
        attest_against_doc_head(
            self.session, self.claim_md, "signature", "- `nat`: ℕ",
            self._claim_addr(),
            content_changed=False,
        )

        # Chain unchanged — producer signaled no real edit.
        self.assertEqual(
            supersession_chain_length(self.session, sidecar_addr), 1,
            "chain stays at 1 — content_changed=False, no edit",
        )
        # Predicate True — a new citation anchor was emitted from the
        # existing sidecar version to the doc's new head version.
        self.assertTrue(signature_is_fresh(self.session, self._claim_addr()))


if __name__ == "__main__":
    unittest.main()
