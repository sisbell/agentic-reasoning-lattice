"""Trigger runner — predicate-driven and force dispatch.

Two functions:

  run_until_quiescent — convergence loop. Fire only where predicate is
    false. Re-evaluate after each fire so cascades propagate. Stop
    when a full pass fires nothing.

  run_force_pass — one pass that fires every (trigger, addr) returned
    by scope_query, regardless of predicate. Used for "I don't trust
    the predicate" cases (LLM noise, crash recovery on a named subset).

Per-pass fire cap (run_until_quiescent only): within one pass, each
(trigger, addr) pair fires at most once — prevents ping-pong inside a
single sweep. Across passes, a pair re-fires whenever its predicate is
false (this is what makes downstream invalidation work).

Known limitation — cascade invalidation: substrate-local predicates
(`is_claim_converged`, `unresolved_revise_comments`) read only the
target's own state. They do not catch invalidation from upstream
revisions. Until cascade-aware predicates exist, callers mitigate via
`run_force_pass` on a user-named subset.
"""

from __future__ import annotations

import sys
import time
from dataclasses import dataclass, field
from typing import Callable

from lib.protocols.febe.protocol import Session
from lib.protocols.febe.session import open_session
from lib.shared.paths import LATTICE

from .scope import Scope
from .trigger import Trigger


SessionFactory = Callable[[], Session]


def _default_session_factory() -> Session:
    return open_session(LATTICE)


@dataclass
class RunResult:
    quiescent: bool
    iterations: int
    fires: list[tuple[str, str]] = field(default_factory=list)
    errors: list[tuple[str, str, str]] = field(default_factory=list)


def run_until_quiescent(
    triggers: list[Trigger],
    scope: Scope,
    *,
    session_factory: SessionFactory = _default_session_factory,
    max_iterations: int = 100,
) -> RunResult:
    """Convergence loop. Returns RunResult.

    - Each pass walks every trigger over its scope.
    - For each (trigger, addr) where predicate is false, fire the agent.
    - Within one pass, a pair fires at most once.
    - Across passes, a pair can re-fire if its predicate has flipped
      back to false (cascade case).
    - Quiescent iff a full pass fires nothing.
    - max_iterations is a safety net.
    """
    fires: list[tuple[str, str]] = []
    errors: list[tuple[str, str, str]] = []

    for iteration in range(max_iterations):
        fired_this_pass: set[tuple[str, str]] = set()
        session = session_factory()
        for trigger in triggers:
            for addr in trigger.scope_query(session, scope):
                key = (trigger.name, str(addr))
                if key in fired_this_pass:
                    continue
                if trigger.predicate(session, addr):
                    continue
                fired_this_pass.add(key)
                start = time.time()
                try:
                    trigger.agent(session, addr)
                except Exception as exc:
                    errors.append((trigger.name, str(addr), repr(exc)))
                    print(
                        f"  [RUNNER] {trigger.name} on {addr} failed: {exc!r}",
                        file=sys.stderr,
                    )
                    continue
                fires.append((trigger.name, str(addr)))
                print(
                    f"  [RUNNER] fired {trigger.name} on {addr} "
                    f"({time.time() - start:.0f}s)",
                    file=sys.stderr,
                )
                session = session_factory()
        if not fired_this_pass:
            return RunResult(
                quiescent=True, iterations=iteration,
                fires=fires, errors=errors,
            )
    return RunResult(
        quiescent=False, iterations=max_iterations,
        fires=fires, errors=errors,
    )


def run_force_pass(
    triggers: list[Trigger],
    scope: Scope,
    *,
    session_factory: SessionFactory = _default_session_factory,
) -> RunResult:
    """Single pass; fire every (trigger, addr) in scope, ignoring predicate.

    For "I don't trust the predicate" use cases:
    - LLM-noise: a clean run might still have missed something
    - Crash recovery: substrate state may not reflect actual completion
    - Targeted re-run: user named a subset they want re-processed

    Returns RunResult with quiescent=False (we did not check). Caller
    should distinguish success via the errors list.
    """
    fires: list[tuple[str, str]] = []
    errors: list[tuple[str, str, str]] = []
    session = session_factory()
    for trigger in triggers:
        for addr in trigger.scope_query(session, scope):
            start = time.time()
            try:
                trigger.agent(session, addr)
            except Exception as exc:
                errors.append((trigger.name, str(addr), repr(exc)))
                print(
                    f"  [RUNNER] {trigger.name} on {addr} failed: {exc!r}",
                    file=sys.stderr,
                )
                continue
            fires.append((trigger.name, str(addr)))
            print(
                f"  [RUNNER] forced {trigger.name} on {addr} "
                f"({time.time() - start:.0f}s)",
                file=sys.stderr,
            )
            session = session_factory()
    return RunResult(
        quiescent=False, iterations=1, fires=fires, errors=errors,
    )
