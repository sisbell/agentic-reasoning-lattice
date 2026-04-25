"""Unit tests for the convergence query helpers."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.store.queries import (
    all_claim_paths, has_resolution, is_claim_converged,
    is_converged, unresolved_revise_comments,
)
from lib.store.store import Store


def _make_resolved_revise(store, claim_path, finding_path, ts_seed):
    """Create a comment.revise + resolution.edit closing it.

    Returns (comment_id, resolution_id).
    """
    comment_id = store.make_link(
        from_set=[finding_path], to_set=[claim_path],
        type_set=["comment.revise"], ts=f"t{ts_seed}",
    )
    res_id = store.make_link(
        from_set=[claim_path], to_set=[comment_id],
        type_set=["resolution.edit"], ts=f"t{ts_seed + 1}",
    )
    return comment_id, res_id


class QueriesTestBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = Store(
            log_path=Path(self.tmp.name) / "links.jsonl",
            index_path=Path(self.tmp.name) / "index.db",
        )
        self.addCleanup(self.store.close)


class ConvergenceTests(QueriesTestBase):
    def test_empty_graph_converges(self):
        # Coverage is the choreography's responsibility — the predicate is
        # vacuously true on an empty graph. See protocol-v2.md.
        self.assertTrue(is_converged(self.store))

    def test_claim_with_no_comments_converges(self):
        self.store.make_link(
            from_set=[], to_set=["T3.md"], type_set=["claim"], ts="t1",
        )
        self.assertTrue(is_claim_converged(self.store, "T3.md"))
        self.assertTrue(is_converged(self.store))

    def test_observe_only_converges(self):
        self.store.make_link(
            from_set=[], to_set=["T3.md"], type_set=["claim"], ts="t1",
        )
        self.store.make_link(
            from_set=["f.md"], to_set=["T3.md"],
            type_set=["comment.observe"], ts="t2",
        )
        self.assertTrue(is_claim_converged(self.store, "T3.md"))
        self.assertTrue(is_converged(self.store))

    def test_unresolved_revise_blocks(self):
        self.store.make_link(
            from_set=[], to_set=["T3.md"], type_set=["claim"], ts="t1",
        )
        self.store.make_link(
            from_set=["f.md"], to_set=["T3.md"],
            type_set=["comment.revise"], ts="t2",
        )
        self.assertFalse(is_claim_converged(self.store, "T3.md"))
        self.assertFalse(is_converged(self.store))

    def test_revise_resolved_by_edit(self):
        self.store.make_link(
            from_set=[], to_set=["T3.md"], type_set=["claim"], ts="t1",
        )
        _make_resolved_revise(self.store, "T3.md", "f.md", ts_seed=2)
        self.assertTrue(is_claim_converged(self.store, "T3.md"))
        self.assertTrue(is_converged(self.store))

    def test_revise_resolved_by_reject(self):
        self.store.make_link(
            from_set=[], to_set=["T3.md"], type_set=["claim"], ts="t1",
        )
        comment_id = self.store.make_link(
            from_set=["f.md"], to_set=["T3.md"],
            type_set=["comment.revise"], ts="t2",
        )
        self.store.make_link(
            from_set=[],
            to_set=[comment_id, "_store/rationales/r1.md"],
            type_set=["resolution.reject"], ts="t3",
        )
        self.assertTrue(is_claim_converged(self.store, "T3.md"))
        self.assertTrue(is_converged(self.store))

    def test_mix_edit_and_reject_resolutions_all_resolved(self):
        self.store.make_link(
            from_set=[], to_set=["T3.md"], type_set=["claim"], ts="t1",
        )
        _make_resolved_revise(self.store, "T3.md", "f1.md", ts_seed=2)
        comment_b = self.store.make_link(
            from_set=["f2.md"], to_set=["T3.md"],
            type_set=["comment.revise"], ts="t10",
        )
        self.store.make_link(
            from_set=[], to_set=[comment_b, "_store/rationales/r.md"],
            type_set=["resolution.reject"], ts="t11",
        )
        self.assertTrue(is_claim_converged(self.store, "T3.md"))

    def test_mix_resolved_and_unresolved(self):
        self.store.make_link(
            from_set=[], to_set=["T3.md"], type_set=["claim"], ts="t1",
        )
        _make_resolved_revise(self.store, "T3.md", "f1.md", ts_seed=2)
        self.store.make_link(
            from_set=["f2.md"], to_set=["T3.md"],
            type_set=["comment.revise"], ts="t10",
        )
        self.assertFalse(is_claim_converged(self.store, "T3.md"))
        self.assertFalse(is_converged(self.store))

    def test_per_claim_isolation(self):
        self.store.make_link(
            from_set=[], to_set=["T3.md"], type_set=["claim"], ts="t1",
        )
        self.store.make_link(
            from_set=[], to_set=["T4.md"], type_set=["claim"], ts="t2",
        )
        # T3 has a resolved revise; T4 has an unresolved revise
        _make_resolved_revise(self.store, "T3.md", "f1.md", ts_seed=3)
        self.store.make_link(
            from_set=["f2.md"], to_set=["T4.md"],
            type_set=["comment.revise"], ts="t20",
        )

        self.assertTrue(is_claim_converged(self.store, "T3.md"))
        self.assertFalse(is_claim_converged(self.store, "T4.md"))
        self.assertFalse(is_converged(self.store))


class HelperTests(QueriesTestBase):
    def test_has_resolution_true_when_resolved(self):
        comment_id, _ = _make_resolved_revise(
            self.store, "T3.md", "f.md", ts_seed=1,
        )
        self.assertTrue(has_resolution(self.store, comment_id))

    def test_has_resolution_false_when_unresolved(self):
        comment_id = self.store.make_link(
            from_set=["f.md"], to_set=["T3.md"],
            type_set=["comment.revise"], ts="t1",
        )
        self.assertFalse(has_resolution(self.store, comment_id))

    def test_unresolved_revise_comments_returns_only_unresolved(self):
        resolved_id, _ = _make_resolved_revise(
            self.store, "T3.md", "f1.md", ts_seed=1,
        )
        unresolved_id = self.store.make_link(
            from_set=["f2.md"], to_set=["T3.md"],
            type_set=["comment.revise"], ts="t10",
        )
        # An OBSERVE comment never blocks and never appears in this list.
        self.store.make_link(
            from_set=["f3.md"], to_set=["T3.md"],
            type_set=["comment.observe"], ts="t20",
        )
        result = unresolved_revise_comments(self.store)
        self.assertEqual([c["id"] for c in result], [unresolved_id])

    def test_unresolved_revise_comments_scoped_to_claim(self):
        unresolved_t3 = self.store.make_link(
            from_set=["f1.md"], to_set=["T3.md"],
            type_set=["comment.revise"], ts="t1",
        )
        self.store.make_link(
            from_set=["f2.md"], to_set=["T4.md"],
            type_set=["comment.revise"], ts="t2",
        )
        result = unresolved_revise_comments(self.store, claim_path="T3.md")
        self.assertEqual([c["id"] for c in result], [unresolved_t3])

    def test_all_claim_paths_collects_classifiers(self):
        self.store.make_link(
            from_set=[], to_set=["T3.md"], type_set=["claim"], ts="t1",
        )
        self.store.make_link(
            from_set=[], to_set=["T0.md"], type_set=["claim"], ts="t2",
        )
        self.store.make_link(
            from_set=[], to_set=["S7.md"], type_set=["claim"], ts="t3",
        )
        self.assertEqual(
            all_claim_paths(self.store), ["S7.md", "T0.md", "T3.md"],
        )


if __name__ == "__main__":
    unittest.main()
