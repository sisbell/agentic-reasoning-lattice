"""Stuck-revises check — surfaces open `comment.revise` links that have
sat without resolution longer than a threshold.

A healthy review→consult→revise loop closes each `comment.revise`
within minutes of its emission. Revises that sit open for hours
indicate the runner isn't making progress — either revise isn't
firing (predicate gating, missing consultation coverage), or it's
firing but failing silently, or the agent's edits aren't producing
the resolution emissions readers expect.

Pair with `stale-holdings` as the "is the runner making forward
progress?" observability layer. Holding age tracks mid-fire stuck
state; revise age tracks between-fire stuck state.

Severity: WARNING. A briefly-stuck revise is normal between fires;
the threshold is conservative enough that exceeding it is
signal-worthy without being alarmist.
"""

from __future__ import annotations

import time
from typing import Iterable

from lib.predicates import unresolved_revise_comments
from lib.protocols.febe.protocol import Session

from . import Issue, Severity


CHECK_NAME = "stuck-revises"
CHECK_DESCRIPTION = (
    "Open `comment.revise` links older than the threshold. A healthy "
    "review → consult → revise loop closes each revise within minutes; "
    "long-standing open revises mean revise isn't making progress."
)
DEFAULT_THRESHOLD_SECONDS = 600


def check_stuck_revises(
    session: Session,
    max_age_seconds: int = DEFAULT_THRESHOLD_SECONDS,
) -> Iterable[Issue]:
    """Yield one Issue per stuck revise link past the threshold."""
    now = int(time.time())
    threshold = now - max_age_seconds
    # unresolved_revise_comments(session) without a doc filter returns
    # every open revise across the substrate (per quiescence.py's
    # factory pattern: doc-arg-less call walks all).
    stuck = [
        link for link in unresolved_revise_comments(session)
        if link.ts is not None and link.ts < threshold
    ]
    for link in stuck:
        finding = link.from_set[0] if link.from_set else "(none)"
        target = link.to_set[0] if link.to_set else "(none)"
        age = now - link.ts
        yield Issue(
            severity=Severity.WARNING,
            check=CHECK_NAME,
            message=(
                f"link={link.addr}  finding={finding}  target={target}  "
                f"age={age}s"
            ),
        )
