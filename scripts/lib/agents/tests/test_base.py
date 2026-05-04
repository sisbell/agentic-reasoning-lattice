"""Agent ABC unit tests.

Verify the contract:
- subclasses must set `role` and implement `run`
- __call__ wraps run in agent_context (env var bound during call)
- elapsed time auto-populated when run() didn't set it
- AgentResult passes through faithfully
"""

import os
import sys
import unittest
from pathlib import Path
from typing import ClassVar

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.agents import Agent, AgentResult
from lib.provenance.context import AGENT_DOC_ENV_VAR


class _NoopAgent(Agent):
    role: ClassVar[str] = "noop"

    def __init__(self):
        self.captured_env = None

    def run(self, session, addr):
        self.captured_env = os.environ.get(AGENT_DOC_ENV_VAR)
        return AgentResult(success=True, detail="ok")


class _SlowAgent(Agent):
    role: ClassVar[str] = "noop"

    def run(self, session, addr):
        import time
        time.sleep(0.01)
        return AgentResult(success=True)


class _CustomElapsedAgent(Agent):
    role: ClassVar[str] = "noop"

    def run(self, session, addr):
        return AgentResult(success=True, elapsed=42.0)


class AgentContractTests(unittest.TestCase):
    def test_call_passes_through_run_result(self):
        agent = _NoopAgent()
        result = agent(session=None, addr=None)
        self.assertTrue(result.success)
        self.assertEqual(result.detail, "ok")

    def test_call_binds_agent_doc_env_var_during_run(self):
        agent = _NoopAgent()
        # Confirm clean before
        self.assertIsNone(os.environ.get(AGENT_DOC_ENV_VAR))
        agent(session=None, addr=None)
        # During run() the env var was bound
        self.assertEqual(
            agent.captured_env,
            "_docuverse/documents/agent/noop.md",
        )
        # After call returns it's cleaned up
        self.assertIsNone(os.environ.get(AGENT_DOC_ENV_VAR))

    def test_elapsed_auto_filled(self):
        result = _SlowAgent()(session=None, addr=None)
        self.assertGreater(result.elapsed, 0.0)

    def test_elapsed_preserved_when_run_sets_it(self):
        result = _CustomElapsedAgent()(session=None, addr=None)
        self.assertEqual(result.elapsed, 42.0)


class AbstractnessTests(unittest.TestCase):
    def test_cannot_instantiate_without_run(self):
        class Missing(Agent):
            role: ClassVar[str] = "missing"

        with self.assertRaises(TypeError):
            Missing()


if __name__ == "__main__":
    unittest.main()
