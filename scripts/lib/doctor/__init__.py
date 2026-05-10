"""Lattice doctor — substrate health checks.

A doctor check inspects substrate state for protocol-level inconsistency:
state that's structurally legal (won't crash a query) but semantically
wrong (two redundant representations disagree, an invariant the substrate
doesn't enforce has been violated, a quiescence assumption is stale).

The doctor is read-only. It reports; it doesn't repair. Repair is a
separate workflow because each kind of inconsistency has its own
remediation cost and risk profile.

Each check is a function `check(session) -> Iterable[Issue]`. The CLI
runs every registered check, prints issues by severity, exits non-zero
when any error-level issue is found.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Iterable, List

from lib.protocols.febe.protocol import Session


class Severity(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass(frozen=True)
class Issue:
    """One thing the doctor noticed.

    severity: ERROR (broken invariant), WARNING (recoverable drift),
              INFO (observability signal).
    check:    short identifier of the check that emitted this
              (e.g., "version-graph", "stale-holdings").
    message:  human-readable description, including the relevant address
              when applicable.
    """
    severity: Severity
    check: str
    message: str


CheckFn = Callable[[Session], Iterable[Issue]]


def run_checks(
    session: Session, checks: List[CheckFn],
) -> List[Issue]:
    """Run every check; return the flat issue list, deduplicated by
    (severity, check, message) so the same finding doesn't print twice
    if two checks happen to flag it.
    """
    seen: set = set()
    out: List[Issue] = []
    for check in checks:
        for issue in check(session):
            key = (issue.severity, issue.check, issue.message)
            if key in seen:
                continue
            seen.add(key)
            out.append(issue)
    return out
