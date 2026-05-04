"""Tests for the renderer registry + read_doc dispatch."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from lib.backend.addressing import Address
from lib.backend.state import State
from lib.lattice.render import (
    _RENDERERS, read_doc, register_renderer, view_kind_for,
)
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

    def _emit_view_classifier(self, doc, kind):
        self.state.make_link(
            homedoc=doc, from_set=[], to_set=[doc],
            type_=f"view.{kind}",
        )

    def test_unregistered_kind_returns_none(self):
        doc = self.state.create_doc()
        self.assertIsNone(view_kind_for(self.session, doc))

    def test_registered_renderer_dispatches_on_classifier(self):
        rendered = []

        def fake_render(session, addr):
            rendered.append(addr)
            return "rendered content"

        register_renderer("claim-statements", fake_render)

        doc = self.state.create_doc()
        self._emit_view_classifier(doc, "claim-statements")

        self.assertEqual(view_kind_for(self.session, doc), "claim-statements")
        self.assertEqual(read_doc(self.session, doc), "rendered content")
        self.assertEqual(rendered, [doc])

    def test_doc_without_view_classifier_falls_through(self):
        # A registered renderer exists but the doc has no classifier.
        register_renderer("claim-statements", lambda s, a: "should not run")
        doc = self.state.create_doc()
        self.assertIsNone(view_kind_for(self.session, doc))

    def test_registry_dispatches_to_matching_kind(self):
        register_renderer("claim-statements", lambda s, a: "claim view")
        register_renderer("other-view", lambda s, a: "other view")

        doc = self.state.create_doc()
        self._emit_view_classifier(doc, "claim-statements")

        self.assertEqual(read_doc(self.session, doc), "claim view")


if __name__ == "__main__":
    unittest.main()
