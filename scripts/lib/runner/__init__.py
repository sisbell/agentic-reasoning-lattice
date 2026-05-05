"""Trigger runner — predicate-driven dispatch for agentic flows.

A trigger is a (scope, predicate, agent) record. The runner walks a
list of triggers across a scope, firing any whose predicate is
unsatisfied, until a full pass fires nothing (quiescent).

CLI scripts and a future daemon both invoke the runner; only the
scope and termination policy differ.
"""

from .run import RunResult, run_force_pass, run_until_quiescent
from .scope import Scope, asn, asn_note_addr, cone
from .trigger import Trigger

__all__ = [
    "RunResult",
    "Scope",
    "Trigger",
    "asn",
    "asn_note_addr",
    "cone",
    "run_force_pass",
    "run_until_quiescent",
]
