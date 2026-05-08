"""Claims-statements refresh trigger — fires on the source note when
its `claims.statements` aggregate's chain trails its derived claims.

  scope:     the source note for the requested ASN
  predicate: is_claims_statements_fresh
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
from lib.predicates import is_claims_statements_fresh
from lib.runner import Trigger
from lib.triggers.scope import per_asn_note


claims_statements_refresh = Trigger(
    name="claims-statements-refresh",
    scope_query=per_asn_note,
    predicate=is_claims_statements_fresh,
    agent=ClaimsStatementsRefreshAgent(),
)
