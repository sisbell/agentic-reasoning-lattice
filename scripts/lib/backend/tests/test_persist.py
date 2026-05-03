"""JSONL persistence — round-trip the link store."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from lib.backend.addressing import Address
from lib.backend.links import LinkStore
from lib.backend.persist import load_jsonl, persist_jsonl
from lib.backend.state import State


class PersistRoundTripTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.path = Path(self.tmpdir.name) / "links.jsonl"

    def test_round_trip_empty_substrate(self):
        state = State(account=Address("1.1.0.1"))
        # Only the bootstrap registry exists; no links emitted yet
        n = persist_jsonl(state.links, self.path)
        self.assertEqual(n, 0)
        loaded = load_jsonl(self.path)
        self.assertEqual(len(loaded), 0)

    def test_round_trip_single_link(self):
        state = State(account=Address("1.1.0.1"))
        xanadu = state.create_doc()
        claim = state.create_doc(kind="claim", lattice=xanadu)
        original_link_count = len(state.links)
        persist_jsonl(state.links, self.path)
        loaded = load_jsonl(self.path)
        self.assertEqual(len(loaded), original_link_count)
        # Compare link addresses + value tuples (order should match)
        for orig, restored in zip(state.links, loaded):
            self.assertEqual(orig.addr, restored.addr)
            self.assertEqual(orig.from_set, restored.from_set)
            self.assertEqual(orig.to_set, restored.to_set)
            self.assertEqual(orig.type_set, restored.type_set)

    def test_round_trip_recovers_lattice_membership(self):
        state = State(account=Address("1.1.0.1"))
        xanadu = state.create_doc()
        claim_a = state.create_doc(kind="claim", lattice=xanadu)
        claim_b = state.create_doc(kind="claim", lattice=xanadu)
        state.make_link(
            homedoc=claim_a,
            from_set=[claim_a],
            to_set=[claim_b],
            type_="citation.depends",
        )

        persist_jsonl(state.links, self.path)
        # Build a fresh state and replay the link log
        fresh = State(account=Address("1.1.0.1"))
        fresh.links = load_jsonl(self.path)
        # Lattice membership recoverable by querying the link store
        self.assertEqual(fresh.lattice_of(claim_a), xanadu)
        self.assertEqual(fresh.lattice_of(claim_b), xanadu)
        self.assertEqual(set(fresh.docs_in(xanadu)), {claim_a, claim_b})
        # Citation recovered too
        citations = fresh.find_links(
            from_set=[claim_a], type_="citation.depends"
        )
        self.assertEqual(len(citations), 1)
        self.assertEqual(citations[0].to_set, (claim_b,))

    def test_round_trip_recovers_classifier_links(self):
        state = State(account=Address("1.1.0.1"))
        xanadu = state.create_doc()
        claim = state.create_doc(kind="claim", lattice=xanadu)
        persist_jsonl(state.links, self.path)
        fresh = State(account=Address("1.1.0.1"))
        fresh.links = load_jsonl(self.path)
        # Querying for the claim classifier on the persisted link store
        # should return the link emitted at create_doc time
        results = fresh.find_links(to_set=[claim], type_="claim")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].from_set, ())  # classifier shape: F=∅

    def test_round_trip_format_matches_legacy_schema(self):
        # The persisted JSONL records carry the same field shape as
        # lib.store.Store's records (op, id, from_set, to_set, type_set, ts).
        state = State(account=Address("1.1.0.1"))
        xanadu = state.create_doc()
        state.create_doc(kind="claim", lattice=xanadu)
        persist_jsonl(state.links, self.path)
        with open(self.path) as f:
            for line in f:
                record = json.loads(line)
                self.assertEqual(record["op"], "create")
                self.assertIn("id", record)
                self.assertIn("from_set", record)
                self.assertIn("to_set", record)
                self.assertIn("type_set", record)
                self.assertIn("ts", record)


if __name__ == "__main__":
    unittest.main()
