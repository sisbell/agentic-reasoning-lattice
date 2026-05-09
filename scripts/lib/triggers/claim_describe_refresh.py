"""Claim-describe refresh trigger — fires once per claim after the ASN
reaches full convergence and before assembly.

  scope:     each claim-classified derivation of the ASN's source note
  predicate: description_is_fresh_after_asn_confirmation
  agent:     ClaimDescribeAgent

Distinct from the existing `claim_describe` trigger (which uses the
ungated `description_is_fresh` and runs in `derive-claims.py` phase 2
to drive version 1 of every description sidecar). This trigger is
the post-confirmation refresh: gated on `is_asn_confirmed(note)`, so
descriptions don't churn during refinement cycles. Fires per stale
claim once the whole cluster settles, immediately before
`claims_statements_refresh` fires the assembly.
"""

from __future__ import annotations

from lib.agents.producers.claim_describe import ClaimDescribeAgent
from lib.predicates import description_is_fresh_after_asn_confirmation
from lib.runner import Trigger
from lib.triggers.scope import per_claim_of_asn


claim_describe_refresh = Trigger(
    name="claim-describe-refresh",
    scope_query=per_claim_of_asn,
    predicate=description_is_fresh_after_asn_confirmation,
    agent=ClaimDescribeAgent(),
    supports_claim_filter=True,
)
