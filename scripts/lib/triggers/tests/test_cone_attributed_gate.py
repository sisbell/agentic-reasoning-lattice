"""Predicate-audit tests: cone_review converges on its OWN n=2 stream —
two consecutive clean, DECOMPOSED, cone-attributed reviews — independent
of the whole-ASN full-review gate.

Cone reviews are distinguished from full-review coverage via the
`manages` link auto-emitted by `AttributingStore` (walk the graph from
the cone-review agent doc). The streak (`_clean_cone_review_streak`)
counts only cone-attributed coverage, and only once the review has been
decomposed into findings — an undecomposed review's verdict is unknown
(no comment.revise yet), so it must not be counted as clean. The
predicate skips an apex only at streak >= CONE_CONFIRMATION_N (and
cascade-fresh) — so a single clean full_review can't make cone_review
skip, and a single cone review isn't enough either.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from lib.backend.emit import (
    emit_claim, emit_empty_derivation, emit_review_content,
    emit_review_coverage,
)
from lib.backend.store import Store
from lib.protocols.febe.session import Session
from lib.triggers.cone_review import (
    CONE_CONFIRMATION_N,
    _clean_cone_review_streak,
    _predicate as cone_review_predicate,
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


class CleanConeReviewStreak(unittest.TestCase):
    """The streak helper: counts trailing clean, decomposed,
    cone-attributed reviews."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lattice = _setup_lattice(Path(self.tmp.name)).resolve()
        self.store = Store(self.lattice)
        self.session = Session(self.store)

        agent_dir = self.lattice / "_docuverse" / "documents" / "agent"
        agent_dir.mkdir(parents=True)
        (agent_dir / "cone-review.md").write_text("# cone-review agent\n")
        self.cone_agent = self.session.register_path(
            "_docuverse/documents/1.1/1/agent/cone-review.md",
        )
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
        self._n = 0

    def _emit_cone_review(self, claim_addr, *, decomposed=True, agent=None):
        """Emit a cone-attributed (default) review covering claim_addr.
        decomposed=True marks it clean+processed via an empty derivation;
        decomposed=False leaves it pending (no provenance.derivation)."""
        self._n += 1
        agent = agent if agent is not None else self.cone_agent
        review = self.session.register_path(
            f"_docuverse/documents/review/claims/ASN-0099/r-{self._n}.md",
        )
        emit_review_content(self.store, review)
        cov, _ = emit_review_coverage(self.store, review, claim_addr)
        self.store.make_link(
            homedoc=agent, from_set=[agent], to_set=[cov.addr],
            type_="manages",
        )
        if decomposed:
            emit_empty_derivation(self.store, review)  # 0 findings = clean
        return review

    def test_streak_zero_when_no_cone_reviews(self):
        self.assertEqual(_clean_cone_review_streak(self.session, self.claim), 0)

    def test_streak_counts_clean_decomposed_reviews(self):
        self._emit_cone_review(self.claim)
        self.assertEqual(_clean_cone_review_streak(self.session, self.claim), 1)
        self._emit_cone_review(self.claim)
        self.assertEqual(_clean_cone_review_streak(self.session, self.claim), 2)

    def test_undecomposed_review_not_counted(self):
        """A cone review not yet decomposed into findings has no
        comment.revise — verdict unknown — so it must not count clean."""
        self._emit_cone_review(self.claim, decomposed=False)
        self.assertEqual(_clean_cone_review_streak(self.session, self.claim), 0)

    def test_undecomposed_caps_streak_at_top(self):
        """One clean, then a pending review on top: the pending one caps
        the streak (it's the most recent), so streak is 0 until it's
        decomposed — an apex can't converge with a pending review."""
        self._emit_cone_review(self.claim)               # clean, decomposed
        self._emit_cone_review(self.claim, decomposed=False)  # pending
        self.assertEqual(_clean_cone_review_streak(self.session, self.claim), 0)

    def test_full_review_coverage_not_counted(self):
        agent_dir = self.lattice / "_docuverse" / "documents" / "agent"
        (agent_dir / "full-review.md").write_text("# full-review agent\n")
        full_agent = self.session.register_path(
            "_docuverse/documents/1.1/1/agent/full-review.md",
        )
        self._emit_cone_review(self.claim, agent=full_agent)
        self.assertEqual(_clean_cone_review_streak(self.session, self.claim), 0)

    def test_streak_zero_when_agent_doc_unregistered(self):
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
            claim = session2.register_path(str(cp.relative_to(lattice2)))
            emit_claim(store2, claim)
            self.assertEqual(_clean_cone_review_streak(session2, claim), 0)


class ConeReviewPredicateGate(unittest.TestCase):
    """The cone_review predicate's convergence skip: streak >=
    CONE_CONFIRMATION_N AND cascade-fresh. One cone review is not enough;
    two consecutive clean cone reviews are."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lattice = _setup_lattice(Path(self.tmp.name)).resolve()
        self.store = Store(self.lattice)
        self.session = Session(self.store)
        agent_dir = self.lattice / "_docuverse" / "documents" / "agent"
        agent_dir.mkdir(parents=True)
        (agent_dir / "cone-review.md").write_text("# cone-review agent\n")
        self.cone_agent = self.session.register_path(
            "_docuverse/documents/1.1/1/agent/cone-review.md",
        )
        claim_dir = (
            self.lattice / "_docuverse" / "documents" / "claim" / "ASN-0099"
        )
        claim_dir.mkdir(parents=True)
        cp = claim_dir / "T0.md"
        cp.write_text("# T0\n\n*Formal Contract:*\n- *Postconditions:* x\n")
        self.apex = self.session.register_path(
            str(cp.relative_to(self.lattice)),
        )
        emit_claim(self.store, self.apex)
        self._n = 0

    def _clean_cone_review(self):
        self._n += 1
        review = self.session.register_path(
            f"_docuverse/documents/review/claims/ASN-0099/c-{self._n}.md",
        )
        emit_review_content(self.store, review)
        cov, _ = emit_review_coverage(self.store, review, self.apex)
        self.store.make_link(
            homedoc=self.cone_agent, from_set=[self.cone_agent],
            to_set=[cov.addr], type_="manages",
        )
        emit_empty_derivation(self.store, review)
        return review

    def test_fires_with_fewer_than_n_cone_reviews(self):
        """One clean cone review (streak 1 < N) → predicate fires."""
        for _ in range(CONE_CONFIRMATION_N - 1):
            self._clean_cone_review()
        self.assertFalse(cone_review_predicate(self.session, self.apex))

    def test_skips_at_n_clean_cone_reviews(self):
        """N clean cone reviews (streak >= N) and cascade-fresh →
        predicate skips."""
        for _ in range(CONE_CONFIRMATION_N):
            self._clean_cone_review()
        self.assertTrue(cone_review_predicate(self.session, self.apex))


if __name__ == "__main__":
    unittest.main()
