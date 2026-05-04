"""Stub-level tests for the BEBE dispatcher.

These verify the stub interface — methods are callable, return the
expected default-shaped values, peer registry is honored. Real
behavior tests arrive when the dispatcher gets a real implementation.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from lib.protocols.bebe import BEBEDispatcher, IndexSummary, NodeId, PeerStatus
from lib.backend.addressing import Address


class TestBEBEDispatcherStub(unittest.TestCase):
    """Verify the stub interface returns expected defaults."""

    def setUp(self):
        self.dispatcher = BEBEDispatcher()
        self.peer = "materials"
        self.addr = Address("1.1.0.1.0.1.2")

    def test_forward_read_returns_none(self):
        self.assertIsNone(
            self.dispatcher.forward_read(self.peer, self.addr)
        )

    def test_forward_find_links_returns_empty(self):
        self.assertEqual(
            [], self.dispatcher.forward_find_links(self.peer, type_="citation")
        )

    def test_forward_middleware_returns_none(self):
        self.assertIsNone(
            self.dispatcher.forward_middleware(
                self.peer, "probe_remote", query="test"
            )
        )

    def test_peer_status_unreachable_for_unknown_peer(self):
        self.assertEqual(
            PeerStatus.UNREACHABLE,
            self.dispatcher.peer_status("nonexistent"),
        )

    def test_peer_status_unreachable_for_configured_peer_in_stub(self):
        # Even configured peers are unreachable in the stub.
        d = BEBEDispatcher(peers={self.peer: "lattices/materials/"})
        self.assertEqual(PeerStatus.UNREACHABLE, d.peer_status(self.peer))

    def test_peer_index_summary_returns_none(self):
        self.assertIsNone(self.dispatcher.peer_index_summary(self.peer))

    def test_peer_for_address_returns_none(self):
        # Stub doesn't know any prefix-to-peer mapping.
        self.assertIsNone(self.dispatcher.peer_for_address(self.addr))

    def test_peers_registry_honored(self):
        d = BEBEDispatcher(peers={"materials": "lattices/materials/"})
        self.assertIn("materials", d.peers)


class TestIndexSummary(unittest.TestCase):
    """The IndexSummary dataclass."""

    def test_default_values(self):
        from datetime import datetime

        summary = IndexSummary(node="materials", captured_at=datetime.now())
        self.assertEqual(0, summary.doc_count)
        self.assertEqual({}, summary.link_counts)
        self.assertEqual("materials", summary.node)


if __name__ == "__main__":
    unittest.main()
