"""Agent base class — opt-in formal shape for trigger-fired work units.

An Agent has identity (a `role` matching its agent doc under
`_docuverse/documents/agent/<role>.md`), a result type, and an
attribution-bound `__call__`. Concrete agents subclass and implement
`run`.

This is opt-in. Existing free-function agents under `lib/agents/`
(citation_resolve, claim_review, etc.) keep working unchanged. New
agents can adopt the class form when they benefit from automatic
attribution wiring or a structured result.

Coordination: if the agent's doc carries an `agent.scope.<type>`
classifier, `__call__` wraps `run` in a holding context (per
docs/design-notes/stigmergic-coordination.md). The hold is acquired
at fire start and retracted at fire end (success or failure). Other
agents whose predicates check `is_held` on the same resource yield
while the hold is active. Agents without a scope classifier run
without coordination — backward-compatible default.
"""

from __future__ import annotations

import contextlib
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Optional

from lib.backend.addressing import Address
from lib.backend.emit import emit_holding, emit_retraction
from lib.predicates.agents import agent_scope_for, resolve_to_scope
from lib.protocols.febe.protocol import Session
from lib.provenance import agent_context
from lib.shared.paths import agent_doc_path


@dataclass
class AgentResult:
    """Outcome of an agent firing.

    success — did the agent complete the work it intended to.
    elapsed — wall-clock seconds for the run() body.
    detail  — short human-readable summary; agents are free to put
              richer info here.
    """

    success: bool
    elapsed: float = 0.0
    detail: str = ""


class Agent(ABC):
    """Trigger-fired unit of work with bound identity.

    Subclasses set `role` (a class variable) and implement `run`. The
    `__call__` wrapper opens an attribution context using `role`'s
    canonical agent doc path before delegating to `run`, so every
    substrate write the agent emits is provenance-tagged automatically.

    If the agent's doc has an `agent.scope.<type>` classifier, the
    wrapper additionally acquires a `holding` link on the resolved
    scope address before invoking `run`, and retracts on exit. See
    `_hold_context`.
    """

    role: ClassVar[str]

    def __call__(
        self, session: Session, addr: Address, **kwargs,
    ) -> AgentResult:
        """Open attribution context, optionally acquire holding, run.

        Forwards keyword arguments to `run`. Composite and operator-gated
        producers commonly take per-fire context (filenames, spec
        addresses, configuration) via kwargs that the predicate-fired
        path wouldn't supply — the base class is permissive about this
        so subclasses can extend `run`'s signature without overriding
        `__call__`.
        """
        agent_doc_str = str(agent_doc_path(self.role))
        with agent_context(agent_doc_str):
            with self._hold_context(session, addr):
                start = time.time()
                result = self.run(session, addr, **kwargs)
                if result.elapsed == 0.0:
                    result.elapsed = time.time() - start
                return result

    @contextlib.contextmanager
    def _hold_context(
        self, session: Session, addr: Address,
    ):
        """Acquire a `holding` on the agent's declared scope; retract
        on exit.

        Reads the `agent.scope.<type>` classifier on the agent's doc;
        if present, resolves `addr` to the corresponding scope-level
        resource and emits a `holding` link. If absent, the agent runs
        without coordination (backward compatible).

        If a scope is declared but `addr` cannot be resolved to that
        scope, raises `RuntimeError` — running without a hold would
        defeat the mutex guarantee. Failure is loud, not silent.

        If `session` is None (test harness, deliberate opt-out), skips
        the hold entirely.
        """
        if session is None:
            yield
            return

        agent_doc = self._agent_doc_addr(session)
        scope_type = (
            agent_scope_for(session, agent_doc)
            if agent_doc is not None else None
        )
        if scope_type is None:
            yield
            return

        hold_addr = resolve_to_scope(session, addr, scope_type)
        if hold_addr is None:
            raise RuntimeError(
                f"agent {self.role!r}: addr {addr} could not be resolved "
                f"to declared scope {scope_type!r}; "
                f"agent cannot fire without a hold target"
            )

        link = emit_holding(session.store, agent_doc, hold_addr)
        try:
            yield
        finally:
            emit_retraction(session.store, agent_doc, link.addr)

    def _agent_doc_addr(
        self, session: Session,
    ) -> Optional[Address]:
        """Resolve this agent's doc path to a substrate address."""
        return session.get_addr_for_path(str(agent_doc_path(self.role)))

    @abstractmethod
    def run(self, session: Session, addr: Address, **kwargs) -> AgentResult:
        """Do the work. Return an AgentResult.

        Subclasses may extend the signature with additional keyword
        arguments (e.g. `spec_filename` for operator-gated extract,
        `patch_filename` for note-patch). Predicate-fired agents
        ignore the kwargs hatch and accept only `(session, addr)`.
        """
