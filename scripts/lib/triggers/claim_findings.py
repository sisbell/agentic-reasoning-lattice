"""Claim-findings trigger — fires on review docs whose findings have
not yet been decomposed into per-finding substrate.

  scope:     each `review` classifier targeting a review doc in
             the requested ASN (CLI mode), or every active review
             (daemon mode)
  predicate: is_decomposed (skip if the review already carries a
             `decomposed` marker)
  agent:     ClaimFindingsAgent

The agent reads the review prose, extracts findings, applies the
classifier-override sub-routine, emits the per-finding substrate
(finding docs + comment.<kind> links + provenance.derivation),
and stamps the review with the `decomposed` marker. After fire,
the predicate flips True and the runner stops walking this review.
"""

from __future__ import annotations

import re
from typing import Iterator

from lib.agents.producers.claim_findings import ClaimFindingsAgent
from lib.backend.addressing import Address
from lib.predicates import is_decomposed
from lib.protocols.febe.protocol import Session
from lib.runner import Scope, Trigger


def _scope_query(session: Session, scope: Scope) -> Iterator[Address]:
    """Yield review-doc addresses to consider this pass.

    CLI mode: review docs whose path contains the requested ASN
    label. Daemon mode: every active review doc.

    Path-based filtering matches how the review docs are organized
    (`_docuverse/documents/review/claims/<asn_label>/review-N.md`).
    """
    asn_filter = scope.asn_label
    for link in session.active_links("review"):
        if not link.to_set:
            continue
        review_addr = link.to_set[0]
        review_path = session.get_path_for_addr(review_addr)
        if review_path is None:
            continue
        if asn_filter is not None and asn_filter not in review_path:
            continue
        # Only the per-ASN claim review docs (not note reviews) — they
        # live under review/claims/<asn>/. Note reviews use a different
        # decomposition path.
        if "/review/claims/" not in review_path:
            continue
        yield review_addr


claim_findings = Trigger(
    name="claim-findings",
    scope_query=_scope_query,
    predicate=is_decomposed,
    agent=ClaimFindingsAgent(),
)
