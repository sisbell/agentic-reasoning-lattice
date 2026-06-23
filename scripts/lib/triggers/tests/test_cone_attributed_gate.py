"""Predicate-audit tests: cone_review converges on its OWN n=2 stream —
two consecutive clean, DECOMPOSED cone reviews — independent of the
whole-ASN full-review gate.

Cone reviews are distinguished from full-review coverage by PATH: cone
reviews live under `review/cone-claims/` (`is_cone_review_path`), full
reviews under `review/claims/`. Both land `review.coverage` on the apex,
so the coverage alone can't tell them apart — the path can. (This
replaces the earlier `manages`-attribution distinguisher, which the
in-process claim runner never emitted, so no cone review was ever counted
and the cone phase livelocked.)

The streak (`_clean_cone_review_streak`) counts only cone reviews, and
only once decomposed into findings — an undecomposed review's verdict is
unknown (no comment.revise yet), so it must not count as clean. The
predicate skips an apex only at streak >= CONE_CONFIRMATION_N (and
cascade-fresh) — so neither a clean full_review nor a single cone review
makes cone_review skip.
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


# Path stems for the two review streams. Cone reviews MUST carry the
# `/review/cone-claims/` segment so is_cone_review_path recognizes them.
_CONE_DIR = "_docuverse/documents/1.1/1/review/cone-claims/ASN-0099"
_FULL_DIR = "_docuverse/documents/1.1/1/review/claims/ASN-0099"


class CleanConeReviewStreak(unittest.TestCase):
    """The streak helper: counts trailing clean, decomposed cone reviews;
    full reviews (claims path) never count."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lattice = _setup_lattice(Path(self.tmp.name)).resolve()
        self.store = Store(self.lattice)
        self.session = Session(self.store)

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

    def _emit_review(self, claim_addr, *, cone, decomposed=True):
        """Emit a review covering claim_addr in the cone or full stream.
        decomposed=True marks it clean+processed via an empty derivation;
        decomposed=False leaves it pending (no provenance.derivation)."""
        self._n += 1
        if cone:
            rel = f"{_CONE_DIR}/cone-{self._n}.md"
        else:
            rel = f"{_FULL_DIR}/review-{self._n}.md"
        review = self.session.register_path(rel)
        emit_review_content(self.store, review)
        emit_review_coverage(self.store, review, claim_addr)
        if decomposed:
            emit_empty_derivation(self.store, review)  # 0 findings = clean
        return review

    def test_streak_zero_when_no_cone_reviews(self):
        self.assertEqual(_clean_cone_review_streak(self.session, self.claim), 0)

    def test_streak_counts_clean_decomposed_cone_reviews(self):
        self._emit_review(self.claim, cone=True)
        self.assertEqual(_clean_cone_review_streak(self.session, self.claim), 1)
        self._emit_review(self.claim, cone=True)
        self.assertEqual(_clean_cone_review_streak(self.session, self.claim), 2)

    def test_undecomposed_cone_review_not_counted(self):
        """A cone review not yet decomposed into findings has no
        comment.revise — verdict unknown — so it must not count clean."""
        self._emit_review(self.claim, cone=True, decomposed=False)
        self.assertEqual(_clean_cone_review_streak(self.session, self.claim), 0)

    def test_undecomposed_caps_streak_at_top(self):
        """One clean, then a pending cone review on top: the pending one
        caps the streak (most recent), so streak is 0 until decomposed."""
        self._emit_review(self.claim, cone=True)               # clean
        self._emit_review(self.claim, cone=True, decomposed=False)  # pending
        self.assertEqual(_clean_cone_review_streak(self.session, self.claim), 0)

    def test_full_review_not_counted_toward_cone_streak(self):
        """REGRESSION (the livelock): clean, decomposed FULL reviews on
        the claims path must NOT advance the cone streak. Before the fix,
        the manages-attribution distinguisher never matched real cone
        reviews, so the streak stuck at 0 and the cone phase re-reviewed
        the apex forever. Now full reviews are excluded by path and cone
        reviews counted by path — so many clean full reviews still leave
        the cone streak at 0."""
        for _ in range(5):
            self._emit_review(self.claim, cone=False)
        self.assertEqual(_clean_cone_review_streak(self.session, self.claim), 0)

    def test_full_reviews_dont_break_cone_streak(self):
        """Full reviews interleaved with cone reviews are simply ignored
        by the cone streak — they neither add to nor reset it."""
        self._emit_review(self.claim, cone=True)    # cone, clean
        self._emit_review(self.claim, cone=False)   # full (ignored)
        self._emit_review(self.claim, cone=True)    # cone, clean
        self.assertEqual(_clean_cone_review_streak(self.session, self.claim), 2)


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
            f"{_CONE_DIR}/cone-{self._n}.md",
        )
        emit_review_content(self.store, review)
        emit_review_coverage(self.store, review, self.apex)
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
