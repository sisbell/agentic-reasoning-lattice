"""Claims-statements refresh trigger — fires on the source note when
its `claims.statements` aggregate's chain trails its derived claims.

  scope:     one canonical claim of the ASN (first by tumbler) —
             the agent multi-holds every classified claim, so the
             initial address just needs to anchor the fire.
  predicate: is_claims_statements_fresh (note-side check; we resolve
             claim → note before delegating).
  agent:     ClaimsStatementsRefreshAgent

Fires after `is_asn_confirmed` opens the gate and at least one claim
edit has advanced a claim's chain past the aggregate's chain. Each
fire calls `register_version` on the aggregate, advancing its chain
by one. The runner re-evaluates and refires until the aggregate
catches up to the maximum claim chain length, then quiesces.

The aggregate's content is rendered live by `render_claim_statements`
on read; the agent only advances the version chain so downstream
cascade detectors (citing the aggregate) see the change via
`is_head_version`.
"""

from __future__ import annotations

from lib.agents.producers.claims_statements_refresh import (
    ClaimsStatementsRefreshAgent,
)
from lib.backend.addressing import Address
from lib.predicates import is_claims_statements_fresh, resolve_to_scope
from lib.protocols.febe.protocol import Session
from lib.runner import Trigger
from lib.triggers._commit_paths import claims_aggregate_paths
from lib.triggers.scope import asn_first_claim


def _predicate(session: Session, addr: Address) -> bool:
    """Resolve the canonical claim back to its source note, then
    delegate to the note-keyed freshness predicate."""
    note_addr = resolve_to_scope(session, addr, "note")
    if note_addr is None:
        return True
    return is_claims_statements_fresh(session, note_addr)


def _commit_paths(session: Session, addr: Address) -> list[str]:
    """Resolve the canonical claim back to its source note, then
    return the aggregate path under that note's ASN."""
    note_addr = resolve_to_scope(session, addr, "note")
    if note_addr is None:
        return []
    return claims_aggregate_paths(session, note_addr)


claims_statements_refresh = Trigger(
    name="claims-statements-refresh",
    scope_query=asn_first_claim,
    predicate=_predicate,
    agent=ClaimsStatementsRefreshAgent(),
    commit_paths=_commit_paths,
)
