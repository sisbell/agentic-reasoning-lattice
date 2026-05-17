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
from typing import ClassVar, List, Optional

from pathlib import Path

from lib.backend.addressing import Address
from lib.backend.emit import emit_holding, emit_retraction
from lib.predicates.agents import agent_scope_for, resolve_to_scope
from lib.protocols.febe.protocol import Session
from lib.provenance import agent_context
from lib.shared.paths import LATTICE_NODE, LATTICE_USER, WORKSPACE, agent_doc_path


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

    # Emission region. Defaults to the lattice's primary (node, user)
    # — the standard place where this lattice's content lives. Agents
    # whose substrate output belongs in a different region override
    # these class attributes (e.g., claim-derivation agents set
    # `node = "1.3"` so claims emit at the claim region).
    #
    # The substrate auto-routes by path prefix; these attributes drive
    # the path strings the agent constructs, not the routing itself.
    # An agent that declared a node but wrote paths at the primary
    # region's prefix would still emit at the primary region — the
    # path is the source of truth. Use the `claim_dir` / `note_dir`
    # helper properties to keep these aligned.
    node: ClassVar[str] = LATTICE_NODE
    user: ClassVar[str] = LATTICE_USER

    @property
    def claim_dir(self) -> Path:
        """Lattice-rooted claim directory for this agent's region."""
        return (
            WORKSPACE / "_docuverse" / "documents"
            / self.node / self.user / "claim"
        )

    @property
    def note_dir(self) -> Path:
        """Lattice-rooted note directory for this agent's region."""
        return (
            WORKSPACE / "_docuverse" / "documents"
            / self.node / self.user / "note"
        )

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

    def resolve_holds(
        self, session: Session, addr: Address, scope_type: str,
    ) -> List[Address]:
        """Return every address the agent must hold during this fire.

        Default: a single resource resolved from `addr` to the agent's
        declared scope via `resolve_to_scope`. Subclasses override
        when the agent's work touches multiple resources (e.g., a
        full-ASN reviewer that reads every claim and must hold each
        for honest mutex against per-claim agents).

        Returning `[]` is treated as "could not resolve a hold" and
        causes `_hold_context` to raise — agents declaring a scope
        must hold *something*, otherwise they're firing under a
        broken mutex contract.
        """
        target = resolve_to_scope(session, addr, scope_type)
        return [target] if target is not None else []

    @contextlib.contextmanager
    def _hold_context(
        self, session: Session, addr: Address,
    ):
        """Acquire `holding` links on every address `resolve_holds`
        returns; retract them on exit.

        Reads the `agent.scope.<type>` classifier on the agent's doc;
        if present, calls `resolve_holds` to enumerate the resources
        the fire needs to lock, emits a `holding` link for each, and
        retracts on exit (LIFO). If absent, the agent runs without
        coordination (backward compatible).

        If a scope is declared but `resolve_holds` returns an empty
        list, raises `RuntimeError` — running without a hold would
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

        hold_addrs = self.resolve_holds(session, addr, scope_type)
        if not hold_addrs:
            raise RuntimeError(
                f"agent {self.role!r}: addr {addr} could not be resolved "
                f"to declared scope {scope_type!r}; "
                f"agent cannot fire without a hold target"
            )

        links: List = []
        try:
            for hold_addr in hold_addrs:
                links.append(
                    emit_holding(session.store, agent_doc, hold_addr)
                )
            yield
        finally:
            for link in reversed(links):
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
