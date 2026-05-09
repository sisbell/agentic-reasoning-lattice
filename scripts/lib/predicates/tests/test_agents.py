"""Tests for agent-coordination predicates: holding and scope resolution.

Covers the substrate-side mechanism for the repellent-pheromone
coordination pattern: emit-and-retract holding lifecycle, scope
classifier reading, addr→scope resolution, and stale-holding
observability via the existing per-link `ts` field.
"""

from __future__ import annotations

import json
import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from lib.backend.addressing import Address
from lib.backend.emit import (
    emit_agent, emit_agent_scope, emit_claim, emit_derivation,
    emit_holding, emit_note, emit_retraction,
)
from lib.backend.store import Store
from lib.predicates.agents import (
    agent_scope_for, is_held, resolve_to_scope, stale_holdings,
)
from lib.protocols.febe.session import Session


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


class IsHeldTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lattice = _setup_lattice(Path(self.tmp.name)).resolve()
        self.store = Store(self.lattice)
        self.session = Session(self.store)
        self.agent = self.session.register_path(
            "_docuverse/documents/agent/test-agent.md",
        )
        emit_agent(self.store, self.agent)
        self.resource = self.session.register_path(
            "_docuverse/documents/note/ASN-0099/note.md",
        )
        emit_note(self.store, self.resource)

    def test_returns_false_when_no_holdings(self):
        self.assertFalse(is_held(self.session, self.resource))

    def test_returns_true_after_holding_emitted(self):
        emit_holding(self.store, self.agent, self.resource)
        self.assertTrue(is_held(self.session, self.resource))

    def test_returns_false_after_retraction(self):
        link = emit_holding(self.store, self.agent, self.resource)
        self.assertTrue(is_held(self.session, self.resource))
        emit_retraction(self.store, self.agent, link.addr)
        self.assertFalse(is_held(self.session, self.resource))

    def test_multiple_holdings_only_one_active_after_retract(self):
        link1 = emit_holding(self.store, self.agent, self.resource)
        emit_retraction(self.store, self.agent, link1.addr)
        # Second fire on same resource — fresh hold
        emit_holding(self.store, self.agent, self.resource)
        self.assertTrue(is_held(self.session, self.resource))


class AgentScopeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lattice = _setup_lattice(Path(self.tmp.name)).resolve()
        self.store = Store(self.lattice)
        self.session = Session(self.store)
        self.agent = self.session.register_path(
            "_docuverse/documents/agent/test-agent.md",
        )
        emit_agent(self.store, self.agent)

    def test_returns_none_when_no_scope_classifier(self):
        self.assertIsNone(agent_scope_for(self.session, self.agent))

    def test_returns_scope_type_when_note_classified(self):
        emit_agent_scope(self.store, self.agent, "note")
        self.assertEqual(agent_scope_for(self.session, self.agent), "note")

    def test_returns_scope_type_when_claim_classified(self):
        emit_agent_scope(self.store, self.agent, "claim")
        self.assertEqual(agent_scope_for(self.session, self.agent), "claim")

    def test_emit_agent_scope_rejects_unknown_type(self):
        with self.assertRaises(ValueError):
            emit_agent_scope(self.store, self.agent, "garbage")


class ResolveToScopeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lattice = _setup_lattice(Path(self.tmp.name)).resolve()
        self.store = Store(self.lattice)
        self.session = Session(self.store)
        self.note = self.session.register_path(
            "_docuverse/documents/note/ASN-0099/note.md",
        )
        emit_note(self.store, self.note)
        self.claim = self.session.register_path(
            "_docuverse/documents/claim/ASN-0099/T0.md",
        )
        emit_claim(self.store, self.claim)
        emit_derivation(self.store, self.note, self.claim)

    def test_note_scope_from_note_returns_note(self):
        self.assertEqual(
            resolve_to_scope(self.session, self.note, "note"), self.note,
        )

    def test_note_scope_from_claim_walks_to_note(self):
        self.assertEqual(
            resolve_to_scope(self.session, self.claim, "note"), self.note,
        )

    def test_claim_scope_from_claim_returns_claim(self):
        self.assertEqual(
            resolve_to_scope(self.session, self.claim, "claim"), self.claim,
        )

    def test_unknown_scope_returns_none(self):
        self.assertIsNone(
            resolve_to_scope(self.session, self.note, "nonexistent"),
        )

    def test_note_scope_from_unrelated_addr_returns_none(self):
        # Random address with no classifier — can't resolve
        random_addr = self.session.register_path(
            "_docuverse/documents/random/foo.md",
        )
        self.assertIsNone(
            resolve_to_scope(self.session, random_addr, "note"),
        )


class StaleHoldingsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lattice = _setup_lattice(Path(self.tmp.name)).resolve()
        self.store = Store(self.lattice)
        self.session = Session(self.store)
        self.agent = self.session.register_path(
            "_docuverse/documents/agent/test-agent.md",
        )
        emit_agent(self.store, self.agent)
        self.resource = self.session.register_path(
            "_docuverse/documents/note/ASN-0099/note.md",
        )
        emit_note(self.store, self.resource)

    def test_no_stale_holdings_when_none_emitted(self):
        self.assertEqual(stale_holdings(self.session, 0), [])

    def test_fresh_holding_not_stale_at_high_threshold(self):
        emit_holding(self.store, self.agent, self.resource)
        self.assertEqual(stale_holdings(self.session, 3600), [])

    def test_holding_stale_when_threshold_zero(self):
        emit_holding(self.store, self.agent, self.resource)
        # max_age=0 with a tiny sleep — even just-emitted is stale once
        # one second passes.
        time.sleep(1.1)
        result = stale_holdings(self.session, 0)
        self.assertEqual(len(result), 1)


if __name__ == "__main__":
    unittest.main()
