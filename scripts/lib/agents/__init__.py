"""Agents — trigger-fired units of work with bound identity.

The Agent ABC (lib/agents/base.py) is the formal shape: subclasses
declare a `role` ClassVar and implement `run(session, addr) ->
AgentResult`. The base's `__call__` wraps each invocation in an
attribution context so substrate writes carry agent provenance
automatically.

Concrete agents either inherit Agent (new style) or live as free
functions (legacy — being migrated lazily).
"""

from .base import Agent, AgentResult

__all__ = ["Agent", "AgentResult"]
