"""Agent base class — opt-in formal shape for trigger-fired work units.

An Agent has identity (a `role` matching its agent doc under
`_docuverse/documents/agent/<role>.md`), a result type, and an
attribution-bound `__call__`. Concrete agents subclass and implement
`run`.

This is opt-in. Existing free-function agents under `lib/agents/`
(citation_resolve, claim_review, etc.) keep working unchanged. New
agents can adopt the class form when they benefit from automatic
attribution wiring or a structured result.
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar

from lib.backend.addressing import Address
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
    """

    role: ClassVar[str]

    def __call__(self, session: Session, addr: Address) -> AgentResult:
        with agent_context(str(agent_doc_path(self.role))):
            start = time.time()
            result = self.run(session, addr)
            if result.elapsed == 0.0:
                result.elapsed = time.time() - start
            return result

    @abstractmethod
    def run(self, session: Session, addr: Address) -> AgentResult:
        """Do the work. Return an AgentResult."""
