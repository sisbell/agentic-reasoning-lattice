"""Unit tests for the channel-shape dispatcher in lib.consultation.plugin.

Verifies that build_channel_plugin dispatches correctly on `meta['shape']`,
that flat-corpus channels construct without a consult.py, and that
unknown or missing shapes are rejected with helpful messages.
"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.consultation.plugin import build_channel_plugin


class BuildPluginTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.channel_dir = Path(self.tmp.name) / "demo"
        (self.channel_dir / "resources").mkdir(parents=True)
        (self.channel_dir / "consultations").mkdir()
        (self.channel_dir / "resources" / "corpus.md").write_text(
            "# Corpus\n\nA tiny test corpus.\n"
        )
        (self.channel_dir / "consultations" / "answer.md").write_text(
            "ANSWER: {{question}} CORPUS: {{corpus}}\n"
        )
        (self.channel_dir / "consultations" / "generate-questions.md").write_text(
            "GEN: {inquiry} N={num_questions} {out_of_scope}\n"
        )

    def _meta(self, shape):
        return {
            "name": "demo",
            "role_hint": "theory",
            "description": "test channel",
            "shape": shape,
        }

    def test_flat_corpus_returns_plugin_with_callables(self):
        plugin = build_channel_plugin(self._meta("flat-corpus"), self.channel_dir)
        self.assertTrue(callable(plugin.generate_questions))
        self.assertTrue(callable(plugin.consult))

    def test_missing_shape_raises_with_helpful_message(self):
        meta = {"name": "demo", "role_hint": "theory", "description": "x"}
        with self.assertRaises(ValueError) as cm:
            build_channel_plugin(meta, self.channel_dir)
        msg = str(cm.exception)
        self.assertIn("shape", msg)
        self.assertIn("demo", msg)
        self.assertIn("flat-corpus", msg)
        self.assertIn("custom", msg)

    def test_unknown_shape_raises_with_valid_options(self):
        with self.assertRaises(ValueError) as cm:
            build_channel_plugin(self._meta("invented-shape"), self.channel_dir)
        msg = str(cm.exception)
        self.assertIn("invented-shape", msg)
        self.assertIn("flat-corpus", msg)

    def test_custom_shape_without_consult_py_raises(self):
        # `custom` shape importlib-loads the channel's consult.py; if
        # the file is missing, surface a clear FileNotFoundError.
        with self.assertRaises(FileNotFoundError) as cm:
            build_channel_plugin(self._meta("custom"), self.channel_dir)
        self.assertIn("consult.py", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
