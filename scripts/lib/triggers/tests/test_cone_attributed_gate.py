"""Predicate-audit tests: cone_review skips when an apex has already
received its own cone-attributed review (and is otherwise settled).

The substrate already records which agent emitted each operation
via the `manages` link auto-emitted by `AttributingStore`. Cone-
attributed reviews are distinguishable from full-review-attributed
ones by walking the `manages` graph from the cone-review agent
doc.

Without this gate, a clean full_review (zero findings) would
confirm the ASN, set every claim cascade-fresh, and the cone_review
predicate would skip forever — losing cone_review's focused
per-apex coverage. The gate uses agent attribution to recognize
"this apex hasn't had a cone-attributed review yet" and fires
cone_review even when the ASN is fully confirmed.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from lib.backend.emit import emit_claim, emit_review_coverage
from lib.backend.store import Store
from lib.protocols.febe.session import Session
from lib.triggers.cone_review import (
    _has_been_cone_reviewed, _predicate as cone_review_predicate,
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


class HasBeenConeReviewed(unittest.TestCase):
    """The predicate-helper that walks the `manages` graph."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lattice = _setup_lattice(Path(self.tmp.name)).resolve()
        self.store = Store(self.lattice)
        self.session = Session(self.store)

        # Register the cone-review agent doc.
        agent_dir = self.lattice / "_docuverse" / "documents" / "agent"
        agent_dir.mkdir(parents=True)
        (agent_dir / "cone-review.md").write_text("# cone-review agent\n")
        self.cone_agent = self.session.register_path(
            "_docuverse/documents/agent/cone-review.md",
        )
        # Register a claim.
        claim_dir = (
            self.lattice / "_docuverse" / "documents" / "claim" / "ASN-0099"
        )
        claim_dir.mkdir(parents=True)
        claim_path = claim_dir / "T0.md"
        claim_path.write_text(
            "# T0\n\n*Formal Contract:*\n- *Postconditions:* x\n",
        )
        self.claim = self.session.register_path(
            str(claim_path.relative_to(self.lattice)),
        )
        emit_claim(self.store, self.claim)

    def _emit_review_with_attribution(
        self, agent_addr, review_addr, claim_addr,
    ):
        """Emit review.coverage(review → claim) and manages(agent → cov)."""
        cov, _ = emit_review_coverage(self.store, review_addr, claim_addr)
        self.store.make_link(
            homedoc=agent_addr,
            from_set=[agent_addr],
            to_set=[cov.addr],
            type_="manages",
        )
        return cov

    def test_returns_false_when_no_cone_reviews(self):
        self.assertFalse(_has_been_cone_reviewed(self.session, self.claim))

    def test_returns_true_after_cone_attributed_coverage(self):
        review = self.session.register_path(
            "_docuverse/documents/review/claims/ASN-0099/cone-1.md",
        )
        self._emit_review_with_attribution(
            self.cone_agent, review, self.claim,
        )
        self.assertTrue(_has_been_cone_reviewed(self.session, self.claim))

    def test_full_review_coverage_alone_does_not_count(self):
        """Coverage emitted by a different agent (e.g., full-review)
        doesn't satisfy the cone-attributed predicate."""
        # Register full-review agent doc.
        agent_dir = self.lattice / "_docuverse" / "documents" / "agent"
        (agent_dir / "full-review.md").write_text("# full-review agent\n")
        full_agent = self.session.register_path(
            "_docuverse/documents/agent/full-review.md",
        )
        # Emit a review.coverage attributed to full-review only.
        review = self.session.register_path(
            "_docuverse/documents/review/claims/ASN-0099/full-1.md",
        )
        self._emit_review_with_attribution(full_agent, review, self.claim)
        # Predicate: still False (no cone-attributed coverage).
        self.assertFalse(_has_been_cone_reviewed(self.session, self.claim))

    def test_returns_false_when_agent_doc_unregistered(self):
        # Fresh lattice without an agent doc registered.
        with tempfile.TemporaryDirectory() as tmp2:
            lattice2 = _setup_lattice(Path(tmp2)).resolve()
            store2 = Store(lattice2)
            session2 = Session(store2)
            claim_dir = (
                lattice2 / "_docuverse" / "documents" / "claim" / "ASN-0099"
            )
            claim_dir.mkdir(parents=True)
            cp = claim_dir / "T0.md"
            cp.write_text("# T0\n*Formal Contract:*\n- *Postconditions:* x\n")
            claim = session2.register_path(
                str(cp.relative_to(lattice2)),
            )
            emit_claim(store2, claim)
            self.assertFalse(_has_been_cone_reviewed(session2, claim))


class ConeReviewPredicateGate(unittest.TestCase):
    """The cone_review predicate's third skip condition: confirmed AND
    cascade-fresh AND cone-attributed-review-exists. The
    cone-attributed clause is what keeps cone_review firing on a
    fresh apex even after a clean full_review confirmed the ASN."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lattice = _setup_lattice(Path(self.tmp.name)).resolve()
        self.store = Store(self.lattice)
        self.session = Session(self.store)
        # Agent docs.
        agent_dir = self.lattice / "_docuverse" / "documents" / "agent"
        agent_dir.mkdir(parents=True)
        (agent_dir / "cone-review.md").write_text("# cone-review agent\n")
        self.cone_agent = self.session.register_path(
            "_docuverse/documents/agent/cone-review.md",
        )
        # Apex claim with FC.
        claim_dir = (
            self.lattice / "_docuverse" / "documents" / "claim" / "ASN-0099"
        )
        claim_dir.mkdir(parents=True)
        cp = claim_dir / "T0.md"
        cp.write_text(
            "# T0\n\n*Formal Contract:*\n- *Postconditions:* x\n",
        )
        self.apex = self.session.register_path(
            str(cp.relative_to(self.lattice)),
        )
        emit_claim(self.store, self.apex)

    def _confirm(self):
        """Emit a clean review covering self.apex; advances
        is_claim_confirmed True."""
        from lib.backend.emit import emit_review_content
        rev_path = (
            "_docuverse/documents/review/claims/ASN-0099/r-1.md"
        )
        review = self.session.register_path(rev_path)
        emit_review_content(self.store, review)
        emit_review_coverage(self.store, review, self.apex)
        return review

    def test_fires_when_confirmed_clean_but_no_cone_review_yet(self):
        """Apex has FC, was reviewed clean (full-review-style), no cone
        review attributed to it → predicate fires (False)."""
        self._confirm()
        # The clean review confirms the apex; without the cone-
        # attributed gate the predicate would skip. With the gate,
        # cone-review's focused coverage is still pending.
        self.assertFalse(cone_review_predicate(self.session, self.apex))

    def test_skips_when_confirmed_clean_and_cone_attributed_exists(self):
        """Apex has FC, confirmed, AND cone-review-attributed coverage
        exists → predicate skips (True)."""
        cone_review = self._confirm()
        # Attribute that review to cone-review by emitting manages.
        cov_links = list(
            self.session.active_links(
                "review.coverage", from_set=[cone_review],
            ),
        )
        self.assertEqual(len(cov_links), 1)
        self.store.make_link(
            homedoc=self.cone_agent,
            from_set=[self.cone_agent],
            to_set=[cov_links[0].addr],
            type_="manages",
        )
        self.assertTrue(cone_review_predicate(self.session, self.apex))


if __name__ == "__main__":
    unittest.main()
