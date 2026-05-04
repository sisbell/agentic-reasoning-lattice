"""Trigger — atomic unit of the trigger graph.

A trigger declares: which substrate addresses are in its scope, what
predicate decides whether the agent should fire on a given address,
and what agent runs when the predicate is unsatisfied.

Triggers carry no execution logic. The runner walks them.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from lib.backend.addressing import Address
from lib.protocols.febe.protocol import Session

from .scope import Scope


@dataclass(frozen=True)
class Trigger:
    """An atomic (scope, predicate, agent) record.

    name:        identifier for logs + provenance attribution
    scope_query: (session, scope) → addresses to consider this pass
    predicate:   (session, addr) → True iff the agent does NOT need to fire
                 (matches the convention of `is_*_converged` predicates:
                 True means "satisfied / done")
    agent:       (session, addr) → side effects on substrate
    """

    name: str
    scope_query: Callable[[Session, Scope], Iterable[Address]]
    predicate: Callable[[Session, Address], bool]
    agent: Callable[[Session, Address], None]
