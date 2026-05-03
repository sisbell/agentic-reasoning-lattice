"""Stub-level tests for lib/middle_end/.

These verify the architectural skeleton — package imports clean,
Protocol is satisfied by the stub implementation, stubs return
expected default-shaped values. Real behavior tests arrive when
actual implementations land.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from lib.backend.addressing import Address
from lib.backend.state import State
from lib.febe.session import Session
from lib.middle_end import (
    CandidateMatch,
    LLMJudgeSimilarity,
    SimilarityScore,
    SimilarityService,
)
from lib.middle_end.bridge import (
    BridgeReport,
    analyze_bridge,
    suggest_probe_targets,
)
from lib.middle_end.probe import (
    ProbeResult,
    confirm_connection,
    mark_saturated,
    probe_remote,
)


class SimilarityProtocolTests(unittest.TestCase):
    """LLMJudgeSimilarity satisfies SimilarityService at runtime."""

    def test_llm_judge_satisfies_protocol(self):
        judge = LLMJudgeSimilarity()
        self.assertIsInstance(judge, SimilarityService)

    def test_llm_judge_stub_returns_zero_score(self):
        judge = LLMJudgeSimilarity()
        backend = State(account=Address("1.1.0.1"))
        session = Session(backend)
        result = judge.score(
            session, Address("1.1.0.1.0.1.2"), Address("1.1.0.1.0.1.3"),
            "materials",
        )
        self.assertEqual(0.0, result.score)
        self.assertEqual("stub", result.rationale)

    def test_default_model_is_haiku(self):
        judge = LLMJudgeSimilarity()
        self.assertEqual("claude-haiku-4-5", judge.model)

    def test_model_is_configurable(self):
        judge = LLMJudgeSimilarity(model="claude-sonnet-4-6")
        self.assertEqual("claude-sonnet-4-6", judge.model)


class ProbeStubTests(unittest.TestCase):
    """Probe primitives are stubbed but return correct-shaped values."""

    def setUp(self):
        backend = State(account=Address("1.1.0.1"))
        self.session = Session(backend)
        self.judge = LLMJudgeSimilarity()

    def test_probe_remote_returns_empty_result(self):
        result = probe_remote(
            self.session, Address("1.1.0.1.0.1.2"),
            "materials", self.judge,
        )
        self.assertIsInstance(result, ProbeResult)
        self.assertEqual([], result.matches)

    def test_confirm_connection_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            confirm_connection(
                self.session,
                Address("1.1.0.1.0.1.2"), Address("2.1.0.1.0.1.2"),
                "materials",
            )

    def test_mark_saturated_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            mark_saturated(self.session, Address("1.1.0.1.0.1.5"))


class BridgeStubTests(unittest.TestCase):
    """Bridge analysis primitives are stubbed."""

    def setUp(self):
        backend = State(account=Address("1.1.0.1"))
        self.session = Session(backend)

    def test_analyze_bridge_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            analyze_bridge(self.session, Address("1.1.0.1.0.1.5"))

    def test_suggest_probe_targets_returns_empty(self):
        targets = suggest_probe_targets(
            self.session, Address("1.1.0.1.0.1.5"),
        )
        self.assertEqual([], targets)


class DataclassesTests(unittest.TestCase):
    """The dataclasses have the expected shape."""

    def test_similarity_score_fields(self):
        s = SimilarityScore(score=42.0, rationale="test")
        self.assertEqual(42.0, s.score)
        self.assertEqual("test", s.rationale)

    def test_candidate_match_fields(self):
        m = CandidateMatch(
            local=Address("1.1.0.1.0.1.2"),
            remote=Address("2.1.0.1.0.1.2"),
            remote_lattice="materials",
            similarity=SimilarityScore(score=80.0, rationale="ok"),
        )
        self.assertEqual("materials", m.remote_lattice)

    def test_bridge_report_default_gap_regions(self):
        from typing import Tuple
        r = BridgeReport(
            bridge_id=Address("1.1.0.1.0.1.5"),
            endpoints=(Address("1.1.0.1.0.1.2"),
                       Address("2.1.0.1.0.1.3")),
            density=0.0, saturation_score=0.0,
        )
        self.assertEqual([], r.gap_regions)


if __name__ == "__main__":
    unittest.main()
