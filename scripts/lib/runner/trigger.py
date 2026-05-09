"""Trigger — atomic unit of the trigger graph.

A trigger declares: which substrate addresses are in its scope, what
predicate decides whether the agent should fire on a given address,
and what agent runs when the predicate is unsatisfied.

Triggers carry no execution logic. The runner walks them.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable

from lib.backend.addressing import Address
from lib.protocols.febe.protocol import Session

from .scope import Scope


@dataclass(frozen=True)
class Trigger:
    """An atomic (scope, predicate, agent) record.

    name:        identifier for logs + provenance attribution
    scope_query: (session, scope) → addresses to consider this pass
    predicate:   (session, addr) → True iff the agent does NOT need to fire
                 (matches the convention of `is_*_quiescent` predicates:
                 True means "satisfied / done")
    agent:       (session, addr) → side effects on substrate. Return value
                 is ignored by the runner today; Agent subclasses returning
                 AgentResult slot in transparently. Future runner versions
                 may inspect the result for telemetry.
    supports_claim_filter:
                 True iff this trigger's `scope_query` honors
                 `scope.labels` (per-claim narrowing). Per-trigger CLIs
                 read this to decide whether `--claim LABEL` is a valid
                 flag for this trigger. False for note-scope, inquiry-
                 scope, and triggers whose scope_query yields non-claim
                 addresses (review docs, comments).
    """

    name: str
    scope_query: Callable[[Session, Scope], Iterable[Address]]
    predicate: Callable[[Session, Address], bool]
    agent: Callable[[Session, Address], Any]
    supports_claim_filter: bool = False
