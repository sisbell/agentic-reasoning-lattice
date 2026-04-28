"""Unit tests for the notation library.

Notation = lattice-wide language-provided primitive symbols. One doc,
one classifier link with empty `from_set`, parsed by `read_notation`
to support invariant #7.
"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.store.notation import (
    NOTATION_DOC_REL, emit_notation, read_notation,
)
from lib.store.store import Store


class NotationTestBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.store = Store(
            log_path=self.root / "_store" / "links.jsonl",
            index_path=self.root / "_store" / "index.db",
        )
        self.addCleanup(self.store.close)
        self.doc_abs = self.root / NOTATION_DOC_REL


class EmitNotationTests(NotationTestBase):
    def test_creates_link_and_doc(self):
        link_id, created = emit_notation(
            self.store, ["=", "≠", "∀"], lattice_root=self.root,
        )
        self.assertTrue(created)
        rec = self.store.get(link_id)
        self.assertEqual(rec["type_set"], ["notation"])
        self.assertEqual(rec["from_set"], [])
        self.assertEqual(rec["to_set"], [NOTATION_DOC_REL])
        self.assertEqual(
            self.doc_abs.read_text(),
            "- `=`\n- `≠`\n- `∀`\n",
        )

    def test_empty_primitives_writes_blank_doc(self):
        link_id, created = emit_notation(
            self.store, [], lattice_root=self.root,
        )
        self.assertTrue(created)
        self.assertEqual(self.doc_abs.read_text(), "\n")

    def test_strips_whitespace_and_skips_blanks(self):
        emit_notation(
            self.store, ["  =  ", "", "   ", "≠"],
            lattice_root=self.root,
        )
        self.assertEqual(self.doc_abs.read_text(), "- `=`\n- `≠`\n")


class IdempotencyTests(NotationTestBase):
    def test_second_call_same_primitives_returns_existing(self):
        id1, c1 = emit_notation(
            self.store, ["=", "∈"], lattice_root=self.root,
        )
        id2, c2 = emit_notation(
            self.store, ["=", "∈"], lattice_root=self.root,
        )
        self.assertEqual(id1, id2)
        self.assertTrue(c1)
        self.assertFalse(c2)

    def test_overwrites_doc_on_value_change_link_stays(self):
        id1, _ = emit_notation(
            self.store, ["="], lattice_root=self.root,
        )
        id2, c2 = emit_notation(
            self.store, ["=", "≠", "∀"], lattice_root=self.root,
        )
        self.assertEqual(id1, id2)
        self.assertFalse(c2)
        self.assertEqual(
            self.doc_abs.read_text(),
            "- `=`\n- `≠`\n- `∀`\n",
        )
        all_links = self.store.find_links(type_set=["notation"])
        self.assertEqual(len(all_links), 1)


class ReadNotationTests(NotationTestBase):
    def test_returns_empty_set_when_no_link(self):
        self.assertEqual(read_notation(self.store, lattice_root=self.root), set())

    def test_returns_empty_set_when_doc_missing(self):
        emit_notation(self.store, ["="], lattice_root=self.root)
        self.doc_abs.unlink()
        self.assertEqual(read_notation(self.store, lattice_root=self.root), set())

    def test_round_trips_symbol_set(self):
        primitives = ["=", "≠", "∈", "∀", "⇒"]
        emit_notation(self.store, primitives, lattice_root=self.root)
        self.assertEqual(
            read_notation(self.store, lattice_root=self.root),
            set(primitives),
        )

    def test_ignores_non_bullet_lines(self):
        emit_notation(self.store, ["="], lattice_root=self.root)
        self.doc_abs.write_text(
            "# Notation\n\nSome prose.\n\n- `=`\n- `≠`\n\nMore prose.\n"
        )
        self.assertEqual(
            read_notation(self.store, lattice_root=self.root),
            {"=", "≠"},
        )


if __name__ == "__main__":
    unittest.main()
