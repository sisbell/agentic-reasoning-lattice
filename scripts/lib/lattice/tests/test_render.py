"""Tests for the renderer registry + read_doc dispatch."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from lib.backend.addressing import Address
from lib.backend.state import State
from lib.lattice.render import _RENDERERS, read_doc, register_renderer
from lib.protocols.febe.session import Session


class RendererRegistryTests(unittest.TestCase):

    def setUp(self):
        self.state = State(account=Address("1.1.0.1"))
        self.session = Session(self.state)
        # Snapshot + clear the registry so tests don't leak.
        self._saved_registry = dict(_RENDERERS)
        _RENDERERS.clear()

    def tearDown(self):
        _RENDERERS.clear()
        _RENDERERS.update(self._saved_registry)

    def _emit_transclusion_tag(self, doc, kind):
        self.state.make_link(
            homedoc=doc, from_set=[], to_set=[doc],
            type_=f"transclusion.{kind}",
        )

    def test_registered_renderer_dispatches_on_tag(self):
        rendered = []

        def fake_render(session, addr):
            rendered.append(addr)
            return "rendered content"

        register_renderer("claim-statements", fake_render)

        doc = self.state.create_doc()
        self._emit_transclusion_tag(doc, "claim-statements")

        self.assertEqual(read_doc(self.session, doc), "rendered content")
        self.assertEqual(rendered, [doc])

    def test_doc_without_tag_falls_through_to_file_read(self):
        # A registered renderer exists but the doc has no tag — the
        # renderer must NOT run. read_doc should attempt the file-read
        # path instead.
        called = []
        register_renderer(
            "claim-statements", lambda s, a: called.append(a) or "ran",
        )
        doc = self.state.create_doc()
        # The fallthrough tries to read a file via store; with a
        # State-only session it raises NotImplementedError (no store)
        # or KeyError (no path). Either way, NOT the renderer.
        with self.assertRaises((KeyError, NotImplementedError)):
            read_doc(self.session, doc)
        self.assertEqual(called, [])

    def test_registry_dispatches_to_matching_kind(self):
        register_renderer("claim-statements", lambda s, a: "claim view")
        register_renderer("other-kind", lambda s, a: "other view")

        doc = self.state.create_doc()
        self._emit_transclusion_tag(doc, "claim-statements")

        self.assertEqual(read_doc(self.session, doc), "claim view")


if __name__ == "__main__":
    unittest.main()
