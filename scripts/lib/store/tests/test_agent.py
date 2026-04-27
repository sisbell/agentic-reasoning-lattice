"""Unit tests for the agent module library (emit_agent, emit_manages).

Per docs/protocols/agent.md:
- emit_agent classifies a doc as an agent. Idempotent on active classifiers.
- emit_manages declares an agent manages an operation. Idempotent on
  active (agent, operation) pairs.
- After retraction, re-emitting creates a fresh link with a new id.
- A6 (classifier retraction is well-defined): retracting the classifier
  removes the doc from agent-discovery queries while preserving manages
  links and their resolution.
"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.store.agent import emit_agent, emit_manages
from lib.store.queries import active_links
from lib.store.store import Store


class AgentLibTestBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.store = Store(
            log_path=self.root / "_store" / "links.jsonl",
            index_path=self.root / "_store" / "index.db",
        )
        self.addCleanup(self.store.close)
        self.agent_doc = "lattices/xanadu/_store/agents/cone-review.md"
        self.other_agent_doc = "lattices/xanadu/_store/agents/full-review.md"
        # A throwaway operation link to manage. Use a simple claim link.
        self.op_id = self.store.make_link(
            from_set=[], to_set=["lattices/xanadu/claim-convergence/ASN-0001/T0.md"],
            type_set=["claim"],
        )

    def _retract(self, link_id):
        """File a substrate retraction nullifying link_id."""
        return self.store.make_link(
            from_set=[], to_set=[link_id], type_set=["retraction"],
        )


class EmitAgentTests(AgentLibTestBase):
    def test_first_call_creates_classifier(self):
        link_id, created = emit_agent(self.store, self.agent_doc)
        self.assertTrue(created)
        rec = self.store.get(link_id)
        self.assertEqual(rec["type_set"], ["agent"])
        self.assertEqual(rec["from_set"], [])
        self.assertEqual(rec["to_set"], [self.agent_doc])

    def test_repeated_call_is_idempotent(self):
        first_id, created1 = emit_agent(self.store, self.agent_doc)
        second_id, created2 = emit_agent(self.store, self.agent_doc)
        self.assertTrue(created1)
        self.assertFalse(created2)
        self.assertEqual(first_id, second_id)

    def test_retraction_then_emit_creates_fresh_classifier(self):
        # Set up the prior classifier with an explicit past ts so the fresh
        # emit (which uses utcnow_iso) gets a different content hash. The
        # substrate's link id is content+ts derived; without distinct ts
        # values, identical content produces identical ids.
        first_id = self.store.make_link(
            from_set=[], to_set=[self.agent_doc], type_set=["agent"],
            ts="2025-01-01T00:00:00Z",
        )
        self._retract(first_id)
        second_id, created = emit_agent(self.store, self.agent_doc)
        self.assertTrue(created)
        self.assertNotEqual(first_id, second_id)
        # Active set contains only the new classifier.
        active = active_links(self.store, "agent", to_set=[self.agent_doc])
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0]["id"], second_id)

    def test_distinct_agent_docs_get_distinct_classifiers(self):
        a_id, _ = emit_agent(self.store, self.agent_doc)
        b_id, _ = emit_agent(self.store, self.other_agent_doc)
        self.assertNotEqual(a_id, b_id)


class EmitManagesTests(AgentLibTestBase):
    def setUp(self):
        super().setUp()
        emit_agent(self.store, self.agent_doc)
        emit_agent(self.store, self.other_agent_doc)

    def test_first_call_creates_manages(self):
        link_id, created = emit_manages(self.store, self.agent_doc, self.op_id)
        self.assertTrue(created)
        rec = self.store.get(link_id)
        self.assertEqual(rec["type_set"], ["manages"])
        self.assertEqual(rec["from_set"], [self.agent_doc])
        self.assertEqual(rec["to_set"], [self.op_id])

    def test_repeated_call_is_idempotent(self):
        first_id, created1 = emit_manages(self.store, self.agent_doc, self.op_id)
        second_id, created2 = emit_manages(self.store, self.agent_doc, self.op_id)
        self.assertTrue(created1)
        self.assertFalse(created2)
        self.assertEqual(first_id, second_id)

    def test_retraction_then_emit_creates_fresh_manages(self):
        # Same pattern as the classifier test: explicit past ts on the prior
        # link so the fresh emit's auto-generated ts differs.
        first_id = self.store.make_link(
            from_set=[self.agent_doc], to_set=[self.op_id],
            type_set=["manages"], ts="2025-01-01T00:00:00Z",
        )
        self._retract(first_id)
        second_id, created = emit_manages(self.store, self.agent_doc, self.op_id)
        self.assertTrue(created)
        self.assertNotEqual(first_id, second_id)
        # Active set contains only the new manages link.
        active = active_links(
            self.store, "manages",
            from_set=[self.agent_doc], to_set=[self.op_id],
        )
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0]["id"], second_id)

    def test_two_agents_can_both_manage_same_operation(self):
        """A4: cross-asserter non-resolution. Two agents file manages on the
        same operation; both are active; substrate stores both without
        conflict."""
        a_id, _ = emit_manages(self.store, self.agent_doc, self.op_id)
        b_id, _ = emit_manages(self.store, self.other_agent_doc, self.op_id)
        self.assertNotEqual(a_id, b_id)
        active = active_links(self.store, "manages", to_set=[self.op_id])
        active_ids = {link["id"] for link in active}
        self.assertEqual(active_ids, {a_id, b_id})


class A6ClassifierRetractionTests(AgentLibTestBase):
    """Property A6: retracting the agent classifier removes the doc from
    agent-discovery queries while preserving all manages relationships."""

    def test_retracted_classifier_removed_from_agent_queries(self):
        agent_id, _ = emit_agent(self.store, self.agent_doc)
        emit_manages(self.store, self.agent_doc, self.op_id)
        self._retract(agent_id)
        # Agent discovery query no longer returns the classifier.
        active_agents = active_links(self.store, "agent", to_set=[self.agent_doc])
        self.assertEqual(active_agents, [])

    def test_retracted_classifier_preserves_manages(self):
        agent_id, _ = emit_agent(self.store, self.agent_doc)
        manages_id, _ = emit_manages(self.store, self.agent_doc, self.op_id)
        self._retract(agent_id)
        # Manages link still active despite classifier retraction.
        active_manages = active_links(
            self.store, "manages",
            from_set=[self.agent_doc], to_set=[self.op_id],
        )
        self.assertEqual(len(active_manages), 1)
        self.assertEqual(active_manages[0]["id"], manages_id)


if __name__ == "__main__":
    unittest.main()
