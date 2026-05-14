"""Claim-signature refresh trigger — fires once per claim after the ASN
reaches full convergence and the claim has revised past the sidecar's
last attestation.

  scope:     each claim-classified derivation of the ASN's source note
  predicate: signature_is_fresh_after_asn_confirmation
  agent:     ClaimSignatureResolveAgent

Mirrors `claim_describe_refresh`. Distinct from the existing
`claim_signature_resolve` trigger (which uses the ungated
`signature_is_fresh` and runs in `derive-claims.py` phase 2 to drive
version 1 of every signature sidecar). Each fire emits a
`citation.depends` anchor from the new sidecar version to
`version_head(claim)`; the predicate reads that anchor — if the
cited claim version is still head, fresh; otherwise stale.
"""

from __future__ import annotations

from lib.agents.producers.claim_signature_resolve import (
    ClaimSignatureResolveAgent,
)
from lib.predicates import signature_is_fresh_after_asn_confirmation
from lib.runner import Trigger
from lib.triggers._commit_paths import per_claim_commit_paths
from lib.triggers.scope import per_claim_of_asn


claim_signature_refresh = Trigger(
    name="claim-signature-refresh",
    scope_query=per_claim_of_asn,
    predicate=signature_is_fresh_after_asn_confirmation,
    agent=ClaimSignatureResolveAgent(),
    supports_claim_filter=True,
    commit_paths=per_claim_commit_paths,
)
