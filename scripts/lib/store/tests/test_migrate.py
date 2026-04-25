"""Unit tests for the substrate-paths migration helper."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.shared.migrate_substrate_paths import (
    transform_string, transform_link, migrate_paths,
)


class TransformStringTests(unittest.TestCase):
    def test_no_match_passthrough(self):
        self.assertEqual(transform_string("foo/bar.md", {"baz/": "qux/"}), "foo/bar.md")

    def test_first_matching_prefix_wins(self):
        # When both prefixes match, dict iteration order picks the first.
        subs = {"foo/": "X/", "foo/bar/": "Y/"}
        # `foo/` is iterated first; `foo/bar/file.md` matches `foo/` and is rewritten
        # to `X/bar/file.md` rather than `Y/file.md`.
        out = transform_string("foo/bar/file.md", subs)
        self.assertEqual(out, "X/bar/file.md")

    def test_prefix_replaced(self):
        out = transform_string(
            "lattices/xanadu/formalization/ASN-0034/T0.md",
            {"lattices/xanadu/formalization/": "lattices/xanadu/claim-convergence/"},
        )
        self.assertEqual(out, "lattices/xanadu/claim-convergence/ASN-0034/T0.md")

    def test_only_prefix_match(self):
        # mid-string occurrence does not trigger
        out = transform_string(
            "other/lattices/xanadu/formalization/ASN-0034/T0.md",
            {"lattices/xanadu/formalization/": "lattices/xanadu/claim-convergence/"},
        )
        self.assertEqual(out, "other/lattices/xanadu/formalization/ASN-0034/T0.md")


class TransformLinkTests(unittest.TestCase):
    def test_transforms_both_sets(self):
        link = {
            "id": "l_123",
            "from_set": ["lattices/xanadu/formalization/ASN-0034/T1.md"],
            "to_set": ["lattices/xanadu/formalization/ASN-0034/T0.md"],
            "type_set": ["citation"],
            "ts": "2026-04-25T05:00:00Z",
            "op": "create",
        }
        subs = {"lattices/xanadu/formalization/": "lattices/xanadu/claim-convergence/"}
        out = transform_link(link, subs)
        self.assertEqual(
            out["from_set"],
            ["lattices/xanadu/claim-convergence/ASN-0034/T1.md"],
        )
        self.assertEqual(
            out["to_set"],
            ["lattices/xanadu/claim-convergence/ASN-0034/T0.md"],
        )
        # Other fields unchanged
        self.assertEqual(out["id"], "l_123")
        self.assertEqual(out["type_set"], ["citation"])
        self.assertEqual(out["ts"], "2026-04-25T05:00:00Z")
        self.assertEqual(out["op"], "create")

    def test_empty_sets(self):
        link = {
            "id": "l_x",
            "from_set": [],
            "to_set": ["lattices/xanadu/formalization/ASN-0034/T0.md"],
            "type_set": ["claim"],
            "ts": "2026-04-25T05:00:00Z",
            "op": "create",
        }
        subs = {"lattices/xanadu/formalization/": "lattices/xanadu/claim-convergence/"}
        out = transform_link(link, subs)
        self.assertEqual(out["from_set"], [])
        self.assertEqual(out["to_set"], ["lattices/xanadu/claim-convergence/ASN-0034/T0.md"])


class MigratePathsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.jsonl = self.root / "links.jsonl"

    def _write_lines(self, links):
        with open(self.jsonl, "w") as f:
            for link in links:
                f.write(json.dumps(link, sort_keys=True) + "\n")

    def _read_lines(self):
        with open(self.jsonl) as f:
            return [json.loads(line) for line in f if line.strip()]

    def test_migration_rewrites_paths(self):
        self._write_lines([
            {
                "id": "l_1", "op": "create",
                "from_set": [],
                "to_set": ["lattices/xanadu/formalization/ASN-0034/T0.md"],
                "type_set": ["claim"], "ts": "t1",
            },
            {
                "id": "l_2", "op": "create",
                "from_set": ["lattices/xanadu/formalization/ASN-0034/T1.md"],
                "to_set": ["lattices/xanadu/formalization/ASN-0034/T0.md"],
                "type_set": ["citation"], "ts": "t2",
            },
        ])

        changed = migrate_paths(
            self.jsonl,
            {"lattices/xanadu/formalization/": "lattices/xanadu/claim-convergence/"},
        )
        self.assertEqual(changed, 2)

        out = self._read_lines()
        self.assertEqual(
            out[0]["to_set"],
            ["lattices/xanadu/claim-convergence/ASN-0034/T0.md"],
        )
        self.assertEqual(
            out[1]["from_set"],
            ["lattices/xanadu/claim-convergence/ASN-0034/T1.md"],
        )
        self.assertEqual(
            out[1]["to_set"],
            ["lattices/xanadu/claim-convergence/ASN-0034/T0.md"],
        )

    def test_idempotent_second_pass(self):
        self._write_lines([
            {
                "id": "l_1", "op": "create",
                "from_set": [],
                "to_set": ["lattices/xanadu/formalization/ASN-0034/T0.md"],
                "type_set": ["claim"], "ts": "t1",
            },
        ])
        subs = {"lattices/xanadu/formalization/": "lattices/xanadu/claim-convergence/"}
        first = migrate_paths(self.jsonl, subs)
        self.assertEqual(first, 1)
        second = migrate_paths(self.jsonl, subs)
        self.assertEqual(second, 0)

    def test_dry_run_no_write(self):
        self._write_lines([
            {
                "id": "l_1", "op": "create",
                "from_set": [],
                "to_set": ["lattices/xanadu/formalization/ASN-0034/T0.md"],
                "type_set": ["claim"], "ts": "t1",
            },
        ])
        subs = {"lattices/xanadu/formalization/": "lattices/xanadu/claim-convergence/"}
        changed = migrate_paths(self.jsonl, subs, dry_run=True)
        self.assertEqual(changed, 1)
        # File still has old paths
        out = self._read_lines()
        self.assertEqual(
            out[0]["to_set"],
            ["lattices/xanadu/formalization/ASN-0034/T0.md"],
        )

    def test_unmatched_paths_unchanged(self):
        self._write_lines([
            {
                "id": "l_1", "op": "create",
                "from_set": [],
                "to_set": ["lattices/xanadu/blueprinting/ASN-0034/T0.md"],
                "type_set": ["claim"], "ts": "t1",
            },
        ])
        subs = {"lattices/xanadu/formalization/": "lattices/xanadu/claim-convergence/"}
        changed = migrate_paths(self.jsonl, subs)
        self.assertEqual(changed, 0)
        out = self._read_lines()
        self.assertEqual(
            out[0]["to_set"],
            ["lattices/xanadu/blueprinting/ASN-0034/T0.md"],
        )

    def test_multiple_substitutions(self):
        self._write_lines([
            {
                "id": "l_1", "op": "create",
                "from_set": ["old1/foo.md"],
                "to_set": ["old2/bar.md"],
                "type_set": ["citation"], "ts": "t1",
            },
        ])
        subs = {"old1/": "new1/", "old2/": "new2/"}
        changed = migrate_paths(self.jsonl, subs)
        self.assertEqual(changed, 1)
        out = self._read_lines()
        self.assertEqual(out[0]["from_set"], ["new1/foo.md"])
        self.assertEqual(out[0]["to_set"], ["new2/bar.md"])

    def test_preserves_other_fields_exactly(self):
        original = {
            "id": "l_1", "op": "create",
            "from_set": ["lattices/xanadu/formalization/ASN-0034/T1.md"],
            "to_set": ["lattices/xanadu/formalization/ASN-0034/T0.md"],
            "type_set": ["citation"],
            "ts": "2026-04-25T05:00:00Z",
        }
        self._write_lines([original])
        subs = {"lattices/xanadu/formalization/": "lattices/xanadu/claim-convergence/"}
        migrate_paths(self.jsonl, subs)
        out = self._read_lines()
        self.assertEqual(out[0]["id"], original["id"])
        self.assertEqual(out[0]["op"], original["op"])
        self.assertEqual(out[0]["type_set"], original["type_set"])
        self.assertEqual(out[0]["ts"], original["ts"])


if __name__ == "__main__":
    unittest.main()
