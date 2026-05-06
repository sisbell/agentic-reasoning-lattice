"""Claim-structural-revise trigger — fires per claim with unresolved
structural-violation findings.

  scope:     each claim derived from the requested ASN's source note
             (CLI mode), or every active claim (daemon mode)
  predicate: is_claim_structurally_clean (skip if every comment.violation
             targeting this claim has a resolution)
  agent:     ClaimStructuralReviseAgent

Per-claim granularity: the agent fires once per claim with unresolved
violations and walks all apply-mode rule passes internally. The runner
re-fires next pass if findings remain (some rules failed/declined, or
the audit re-fires and emits fresh violations from post-edit state).

Naming follows the *_revise refiner convention (note_revise,
claim_revise, claim_structural_revise) — refiners that close
comment.<kind> via resolution.<kind> share the verb regardless of
the input subtype.
"""

from __future__ import annotations

from typing import Iterator

from lib.agents.refiners.claim_structural_revise import (
    ClaimStructuralReviseAgent,
)
from lib.backend.addressing import Address
from lib.predicates import (
    derived_claims, is_claim_structurally_clean,
)
from lib.protocols.febe.protocol import Session
from lib.runner import Scope, Trigger, asn_note_addr


def _scope_query(session: Session, scope: Scope) -> Iterator[Address]:
    """Yield each claim-classified derivation of the ASN's source note.

    Mirrors the claim-describe / claim-revise scope shape: walk
    derived_claims, filter to claim-classified addresses.
    """
    if scope.asn_label is not None:
        note_addr = asn_note_addr(session, scope)
        if note_addr is None:
            return
        claim_addrs = {
            link.to_set[0]
            for link in session.active_links("claim")
            if link.to_set
        }
        for derived_addr in derived_claims(session, note_addr):
            if derived_addr in claim_addrs:
                yield derived_addr
        return

    for link in session.active_links("claim"):
        if link.to_set:
            yield link.to_set[0]


claim_structural_revise = Trigger(
    name="claim-structural-revise",
    scope_query=_scope_query,
    predicate=is_claim_structurally_clean,
    agent=ClaimStructuralReviseAgent(),
)
