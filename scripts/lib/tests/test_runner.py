"""Runner unit tests with fake triggers.

The runner is pure modulo a session factory. These tests inject a
trivial fake session that holds dict-shaped state; predicates and
agents read/write that state. No filesystem or substrate touched.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.runner import (
    Scope, Trigger, run_force_pass, run_until_quiescent,
)


class _FakeSession:
    """Minimal stand-in for Session — just a state dict the test owns."""

    def __init__(self, state: dict):
        self.state = state


def _factory_for(state: dict):
    return lambda: _FakeSession(state)


class QuiescenceTests(unittest.TestCase):
    def test_no_addrs_in_scope_is_immediately_quiescent(self):
        trigger = Trigger(
            name="t",
            scope_query=lambda session, scope: iter([]),
            predicate=lambda session, addr: True,
            agent=lambda session, addr: None,
        )
        result = run_until_quiescent(
            [trigger], Scope(),
            session_factory=_factory_for({}),
        )
        self.assertTrue(result.quiescent)
        self.assertEqual(result.iterations, 0)
        self.assertEqual(result.fires, [])

    def test_predicate_already_true_no_fires(self):
        trigger = Trigger(
            name="t",
            scope_query=lambda session, scope: iter(["a", "b", "c"]),
            predicate=lambda session, addr: True,
            agent=lambda session, addr: self.fail("should not fire"),
        )
        result = run_until_quiescent(
            [trigger], Scope(),
            session_factory=_factory_for({}),
        )
        self.assertTrue(result.quiescent)
        self.assertEqual(result.fires, [])

    def test_agent_satisfies_predicate(self):
        state = {"a": False, "b": False}
        trigger = Trigger(
            name="t",
            scope_query=lambda session, scope: iter(state.keys()),
            predicate=lambda session, addr: session.state[addr],
            agent=lambda session, addr: state.update({addr: True}),
        )
        result = run_until_quiescent(
            [trigger], Scope(),
            session_factory=_factory_for(state),
        )
        self.assertTrue(result.quiescent)
        self.assertEqual(set(result.fires), {("t", "a"), ("t", "b")})


class CascadeTests(unittest.TestCase):
    def test_pair_can_refire_across_passes_when_predicate_flips(self):
        # b's predicate becomes false after a's first fire.
        # Models cascade: revising a invalidates b.
        state = {"a": False, "b": True}
        a_fired = [0]
        b_fired = [0]

        def agent_a(session, addr):
            a_fired[0] += 1
            state["a"] = True
            state["b"] = False  # cascade: revising a invalidates b

        def agent_b(session, addr):
            b_fired[0] += 1
            state["b"] = True

        trigger_a = Trigger(
            name="ta",
            scope_query=lambda s, sc: iter(["a"]),
            predicate=lambda s, addr: state["a"],
            agent=agent_a,
        )
        trigger_b = Trigger(
            name="tb",
            scope_query=lambda s, sc: iter(["b"]),
            predicate=lambda s, addr: state["b"],
            agent=agent_b,
        )

        result = run_until_quiescent(
            [trigger_a, trigger_b], Scope(),
            session_factory=_factory_for(state),
        )

        self.assertTrue(result.quiescent)
        self.assertEqual(a_fired[0], 1, "a should fire once")
        self.assertEqual(b_fired[0], 1, "b should fire once after cascade")


class PerPassCapTests(unittest.TestCase):
    def test_pair_does_not_pingpong_within_a_single_pass(self):
        # Agent fails to flip its own predicate. Without per-pass cap
        # the runner would ping-pong forever within one pass.
        state = {"x": False}
        fires = [0]

        def agent_x(session, addr):
            fires[0] += 1
            # Intentionally do not flip state["x"]

        trigger = Trigger(
            name="t",
            scope_query=lambda s, sc: iter(["x"]),
            predicate=lambda s, addr: state["x"],
            agent=agent_x,
        )
        result = run_until_quiescent(
            [trigger], Scope(),
            session_factory=_factory_for(state),
            max_iterations=5,
        )
        self.assertFalse(result.quiescent)
        self.assertEqual(result.iterations, 5)
        self.assertEqual(fires[0], 5)


class ForcePassTests(unittest.TestCase):
    def test_force_fires_regardless_of_predicate(self):
        state = {"a": True, "b": True, "c": True}
        fires = []

        def agent(session, addr):
            fires.append(addr)

        trigger = Trigger(
            name="t",
            scope_query=lambda s, sc: iter(state.keys()),
            predicate=lambda s, addr: state[addr],
            agent=agent,
        )

        result = run_force_pass(
            [trigger], Scope(),
            session_factory=_factory_for(state),
        )
        self.assertEqual(set(fires), {"a", "b", "c"})
        self.assertEqual(len(result.fires), 3)
        self.assertEqual(result.errors, [])

    def test_force_respects_scope_labels(self):
        state = {"a": True, "b": True, "c": True}
        fires = []

        def agent(session, addr):
            fires.append(addr)

        def scope_query(session, scope):
            for k in state.keys():
                if scope.labels is None or k in scope.labels:
                    yield k

        trigger = Trigger(
            name="t",
            scope_query=scope_query,
            predicate=lambda s, addr: state[addr],
            agent=agent,
        )

        result = run_force_pass(
            [trigger], Scope(labels=frozenset({"a", "c"})),
            session_factory=_factory_for(state),
        )
        self.assertEqual(set(fires), {"a", "c"})
        self.assertEqual(len(result.fires), 2)


class ErrorHandlingTests(unittest.TestCase):
    def test_agent_exception_logged_and_skipped(self):
        state = {"a": False, "b": False}

        def agent(session, addr):
            if addr == "a":
                raise RuntimeError("boom")
            state[addr] = True

        trigger = Trigger(
            name="t",
            scope_query=lambda s, sc: iter(["a", "b"]),
            predicate=lambda s, addr: state[addr],
            agent=agent,
        )
        result = run_until_quiescent(
            [trigger], Scope(),
            session_factory=_factory_for(state),
            max_iterations=3,
        )
        self.assertFalse(result.quiescent)
        self.assertTrue(any(addr == "a" for _, addr, _ in result.errors))


if __name__ == "__main__":
    unittest.main()
