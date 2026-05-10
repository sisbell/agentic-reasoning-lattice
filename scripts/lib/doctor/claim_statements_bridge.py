"""Claim-statements-bridge check.

For every `claims.statements` aggregate, there must be an active
`supersession` link from the source note's `statements` sidecar to
the aggregate. Readers walking the supersession chain from the
sidecar address must land on the live aggregate; without the bridge
they stop at the orphaned sidecar.

The bridge is emitted by `ClaimsStatementsRefreshAgent._create` on
the first fire. A missing bridge means either the first fire
errored after minting the aggregate but before the supersession
emit, or the aggregate was minted outside the agent.
"""

from __future__ import annotations

from typing import Iterable, Optional

from lib.backend.addressing import Address
from lib.protocols.febe.protocol import Session

from . import Issue, Severity


CHECK_NAME = "claim-statements-bridge"
CHECK_DESCRIPTION = (
    "Every claims.statements aggregate must be reachable from the "
    "source note's statements sidecar via an active supersession "
    "link. Otherwise readers walking from the sidecar land on a "
    "dead end."
)


def _source_note(
    session: Session, aggregate: Address,
) -> Optional[Address]:
    """Walk reverse `provenance.derivation` from the aggregate to find
    the note that derived it."""
    for link in session.active_links(
        "provenance.derivation", to_set=[aggregate],
    ):
        if link.from_set:
            return link.from_set[0]
    return None


def _note_statements_sidecar(
    session: Session, note: Address,
) -> Optional[Address]:
    """Walk the note's outgoing `statements` link to its sidecar."""
    for link in session.active_links("statements", from_set=[note]):
        if link.to_set:
            return link.to_set[0]
    return None


def check_claim_statements_bridge(session: Session) -> Iterable[Issue]:
    """Yield one Issue per aggregate whose supersession bridge from
    the source note's statements sidecar is missing."""
    for link in session.active_links("claims.statements"):
        if not link.to_set:
            continue
        aggregate = link.to_set[0]
        agg_path = session.get_path_for_addr(aggregate) or "(no path)"

        note = _source_note(session, aggregate)
        if note is None:
            yield Issue(
                severity=Severity.ERROR,
                check=CHECK_NAME,
                message=(
                    f"aggregate={aggregate} ({agg_path})  "
                    f"missing provenance.derivation from any note"
                ),
            )
            continue

        sidecar = _note_statements_sidecar(session, note)
        if sidecar is None:
            yield Issue(
                severity=Severity.WARNING,
                check=CHECK_NAME,
                message=(
                    f"aggregate={aggregate} ({agg_path})  "
                    f"note={note} has no statements sidecar"
                ),
            )
            continue

        has_bridge = any(
            aggregate in sup.to_set
            for sup in session.active_links(
                "supersession", from_set=[sidecar],
            )
        )
        if not has_bridge:
            sidecar_path = session.get_path_for_addr(sidecar) or "(no path)"
            yield Issue(
                severity=Severity.ERROR,
                check=CHECK_NAME,
                message=(
                    f"sidecar={sidecar} ({sidecar_path}) -> "
                    f"aggregate={aggregate}  missing supersession bridge"
                ),
            )
