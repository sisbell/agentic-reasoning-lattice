"""Claim-structural-revise trigger — fires per claim with unresolved
structural-violation findings.

  scope:     each claim-classified derivation of the ASN's source note
             (CLI), or every claim (daemon)
  predicate: is_claim_structurally_clean (skip if every comment.violation
             targeting the claim has an active resolution)
  agent:     ClaimStructuralReviseAgent
"""

from __future__ import annotations

from lib.agents.refiners.claim_structural_revise import (
    ClaimStructuralReviseAgent,
)
from lib.predicates import is_claim_structurally_clean
from lib.runner import Trigger
from lib.triggers._commit_paths import per_claim_commit_paths
from lib.triggers.scope import per_claim_of_asn


claim_structural_revise = Trigger(
    name="claim-structural-revise",
    scope_query=per_claim_of_asn,
    predicate=is_claim_structurally_clean,
    agent=ClaimStructuralReviseAgent(),
    supports_claim_filter=True,
    commit_paths=per_claim_commit_paths,
)
