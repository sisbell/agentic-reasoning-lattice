"""Unit tests for the protocol substrate store."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.store.schema import (
    VALID_SUBTYPES, VALID_TYPES, make_link_id, validate_type,
)
from lib.store.store import Store


class StoreTestBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.log = Path(self.tmp.name) / "links.jsonl"
        self.idx = Path(self.tmp.name) / "index.db"
        self.store = Store(log_path=self.log, index_path=self.idx)
        self.addCleanup(self.store.close)


class MakeLinkTests(StoreTestBase):
    def test_make_link_and_get_roundtrip(self):
        link_id = self.store.make_link(
            from_set=["_workspace/findings/review-1/0.md"],
            to_set=["claim-convergence/ASN-0034/T3.md"],
            type_set=["comment.revise"],
            ts="2026-04-24T00:00:00Z",
        )
        rec = self.store.get(link_id)
        self.assertEqual(rec["id"], link_id)
        self.assertEqual(rec["type_set"], ["comment.revise"])
        self.assertEqual(rec["from_set"], ["_workspace/findings/review-1/0.md"])
        self.assertEqual(rec["to_set"], ["claim-convergence/ASN-0034/T3.md"])
        self.assertEqual(rec["ts"], "2026-04-24T00:00:00Z")

    def test_one_sided_classifier(self):
        link_id = self.store.make_link(
            from_set=[], to_set=["T3.md"], type_set=["claim"], ts="t1",
        )
        rec = self.store.get(link_id)
        self.assertEqual(rec["from_set"], [])
        self.assertEqual(rec["to_set"], ["T3.md"])

    def test_link_to_link_endpoint(self):
        comment_id = self.store.make_link(
            from_set=["f.md"], to_set=["c.md"], type_set=["comment.revise"], ts="t1",
        )
        resolution_id = self.store.make_link(
            from_set=["c.md"], to_set=[comment_id],
            type_set=["resolution.edit"], ts="t2",
        )
        rec = self.store.get(resolution_id)
        self.assertEqual(rec["to_set"], [comment_id])
        found = self.store.find_links(to_set=[comment_id])
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]["id"], resolution_id)

    def test_multi_target(self):
        comment_id = self.store.make_link(
            from_set=["f.md"], to_set=["c.md"], type_set=["comment.revise"], ts="t1",
        )
        rej_id = self.store.make_link(
            from_set=[], to_set=[comment_id, "_store/documents/rationale/r1.md"],
            type_set=["resolution.reject"], ts="t2",
        )
        self.assertEqual(len(self.store.find_links(to_set=[comment_id])), 1)
        self.assertEqual(
            len(self.store.find_links(to_set=["_store/documents/rationale/r1.md"])), 1,
        )
        self.assertEqual(self.store.find_links(to_set=[comment_id])[0]["id"], rej_id)

    def test_duplicate_raises(self):
        kwargs = dict(
            from_set=[], to_set=["c.md"], type_set=["claim"], ts="t1",
        )
        self.store.make_link(**kwargs)
        with self.assertRaises(ValueError):
            self.store.make_link(**kwargs)

    def test_type_set_must_be_length_one(self):
        with self.assertRaises(ValueError):
            self.store.make_link(from_set=[], to_set=["x"], type_set=[])
        with self.assertRaises(ValueError):
            self.store.make_link(
                from_set=[], to_set=["x"], type_set=["claim", "review"],
            )
        with self.assertRaises(ValueError):
            self.store.make_link(from_set=[], to_set=["x"], type_set="claim")


class FindLinksTests(StoreTestBase):
    def setUp(self):
        super().setUp()
        self.a = self.store.make_link(
            from_set=["f1.md"], to_set=["c.md"],
            type_set=["comment.revise"], ts="t1",
        )
        self.b = self.store.make_link(
            from_set=["f2.md"], to_set=["c.md"],
            type_set=["comment.observe"], ts="t2",
        )
        self.cite = self.store.make_link(
            from_set=["claim-a.md"], to_set=["claim-b.md"],
            type_set=["citation"], ts="t3",
        )

    def test_find_by_type_exact(self):
        result = self.store.find_links(type_set=["comment.revise"])
        self.assertEqual([r["id"] for r in result], [self.a])

    def test_find_by_type_prefix(self):
        result = self.store.find_links(type_set=["comment"])
        self.assertEqual(sorted(r["id"] for r in result), sorted([self.a, self.b]))

    def test_find_from(self):
        result = self.store.find_links(from_set=["claim-a.md"])
        self.assertEqual([r["id"] for r in result], [self.cite])

    def test_find_to(self):
        result = self.store.find_links(to_set=["c.md"])
        self.assertEqual(sorted(r["id"] for r in result), sorted([self.a, self.b]))

    def test_find_combined(self):
        result = self.store.find_links(
            to_set=["c.md"], type_set=["comment.revise"],
        )
        self.assertEqual([r["id"] for r in result], [self.a])

    def test_find_with_no_constraints_returns_all(self):
        result = self.store.find_links()
        self.assertEqual(len(result), 3)

    def test_find_unknown_returns_empty(self):
        self.assertEqual(self.store.find_links(to_set=["unknown.md"]), [])
        self.assertEqual(self.store.find_links(type_set=["nonexistent"]), [])

    def test_find_empty_constraint_returns_empty(self):
        self.assertEqual(self.store.find_links(to_set=[]), [])
        self.assertEqual(self.store.find_links(from_set=[]), [])
        self.assertEqual(self.store.find_links(type_set=[]), [])


class FindNumLinksTests(StoreTestBase):
    def setUp(self):
        super().setUp()
        self.store.make_link(
            from_set=["f1.md"], to_set=["c.md"],
            type_set=["comment.revise"], ts="t1",
        )
        self.store.make_link(
            from_set=["f2.md"], to_set=["c.md"],
            type_set=["comment.observe"], ts="t2",
        )

    def test_count_by_type_exact(self):
        self.assertEqual(self.store.find_num_links(type_set=["comment.revise"]), 1)

    def test_count_by_type_prefix(self):
        self.assertEqual(self.store.find_num_links(type_set=["comment"]), 2)

    def test_count_to(self):
        self.assertEqual(self.store.find_num_links(to_set=["c.md"]), 2)

    def test_count_zero(self):
        self.assertEqual(self.store.find_num_links(to_set=["unknown.md"]), 0)

    def test_count_all(self):
        self.assertEqual(self.store.find_num_links(), 2)


class ValidationTests(unittest.TestCase):
    def test_validate_type_accepts_known(self):
        for t in VALID_TYPES:
            validate_type(t)
        for parent, subs in VALID_SUBTYPES.items():
            for sub in subs:
                validate_type(f"{parent}.{sub}")

    def test_validate_type_rejects_unknown(self):
        with self.assertRaises(ValueError):
            validate_type("bogus")
        with self.assertRaises(ValueError):
            validate_type("comment.unknown")
        with self.assertRaises(ValueError):
            validate_type("unknownparent.sub")


class LinkIdTests(unittest.TestCase):
    def test_link_id_format(self):
        lid = make_link_id("claim", [], ["a.md"], "t1")
        self.assertRegex(lid, r"^l_[0-9a-f]{12}$")

    def test_link_id_is_deterministic(self):
        args = ("claim", [], ["a.md"], "t1")
        self.assertEqual(make_link_id(*args), make_link_id(*args))


class RebuildTests(StoreTestBase):
    def test_rebuild_index_roundtrip(self):
        self.store.make_link(from_set=[], to_set=["T3.md"], type_set=["claim"], ts="t1")
        b = self.store.make_link(
            from_set=["f.md"], to_set=["T3.md"],
            type_set=["comment.revise"], ts="t2",
        )
        self.store.make_link(
            from_set=["T3.md"], to_set=[b],
            type_set=["resolution.edit"], ts="t3",
        )

        def snapshot():
            return sorted(
                (r["id"], r["type_set"][0])
                for r in self.store.find_links()
            )

        before = snapshot()
        self.store.rebuild_index()
        after = snapshot()
        self.assertEqual(before, after)


class EmptyGraphTests(StoreTestBase):
    def test_get_missing_returns_none(self):
        self.assertIsNone(self.store.get("l_nonexistent"))

    def test_find_on_empty_graph(self):
        self.assertEqual(self.store.find_links(), [])
        self.assertEqual(self.store.find_links(type_set=["claim"]), [])
        self.assertEqual(self.store.find_num_links(), 0)
        self.assertEqual(self.store.find_num_links(type_set=["claim"]), 0)


if __name__ == "__main__":
    unittest.main()
