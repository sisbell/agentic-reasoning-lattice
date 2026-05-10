"""Stale-holdings check.

Wraps `lib.predicates.agents.stale_holdings` so the doctor surfaces
stuck-fire holdings alongside its other checks. The standalone
`scripts/diagnostics/stale_holdings.py` CLI continues to work — both
share the same predicate.

A holding is "stale" when its emit timestamp is older than a threshold
the caller picks. Default 600s (10 min) matches the standalone
diagnostic. WARNING severity — a stale holding doesn't necessarily
indicate broken state (a long-running fire is fine), but is worth
surfacing.
"""

from __future__ import annotations

import time
from typing import Iterable

from lib.predicates.agents import stale_holdings
from lib.protocols.febe.protocol import Session

from . import Issue, Severity


CHECK_NAME = "stale-holdings"
CHECK_DESCRIPTION = (
    "Holding pheromones open beyond the age threshold. A long-running "
    "fire is normal; a holding that never closes likely means an agent "
    "crashed mid-fire and the retraction never landed."
)
DEFAULT_THRESHOLD_SECONDS = 600


def check_stale_holdings(
    session: Session,
    max_age_seconds: int = DEFAULT_THRESHOLD_SECONDS,
) -> Iterable[Issue]:
    """Yield one Issue per holding link open longer than the threshold."""
    now = int(time.time())
    for link in stale_holdings(session, max_age_seconds):
        agent = link.from_set[0] if link.from_set else "(none)"
        resource = link.to_set[0] if link.to_set else "(none)"
        age = now - link.ts if link.ts is not None else None
        yield Issue(
            severity=Severity.WARNING,
            check=CHECK_NAME,
            message=(
                f"link={link.addr}  agent={agent}  resource={resource}  "
                f"age={age}s"
            ),
        )
