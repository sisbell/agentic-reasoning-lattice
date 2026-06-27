"""Claim-findings agent — decompose a review doc into per-finding substrate.

Fires once per review doc that hasn't been decomposed yet (no
outbound `provenance.derivation` from the review). One fire = read
the review prose, extract each `### `-prefixed finding section, run
the classifier-override sub-routine to correct any reviewer
mis-classification, then emit the per-finding substrate (finding
docs + `comment.<kind>` links + `provenance.derivation` from review
→ finding).

For zero-findings cases (CONVERGED verdict, all findings filtered
out as unparseable), the agent emits a single empty-set derivation
(F=[review], G=∅) anchoring "decompose ran, produced no derivatives."
The predicate `is_review_decomposed` reads any outbound
`provenance.derivation`; this empty-G shape covers the zero-findings
disambiguation without a verb-flag classifier.

This agent owns the second stage of the review → findings → revise
chain. The first stage (review producer — cone_review / full_review)
runs the LLM and emits the review doc; the third stage
(claim_revise refiner) closes the per-finding comments. Override
moves here as a sub-routine because override is part of the
classification step that decides what `comment.<kind>` to emit on
each finding — it shapes the decomposer's substrate write, not the
reviewer's prose.
"""

from __future__ import annotations

import re
import sys
from typing import ClassVar

from lib.agents.base import Agent, AgentResult
from lib.agents.producers.claim_finding_override import apply_classifier_verdict
from lib.agents.producers.review_helpers import extract_findings
from lib.backend.addressing import Address
from lib.backend.emit import emit_empty_derivation
from lib.lattice.findings import record_findings
from lib.lattice.labels import (
    build_cross_asn_label_index,
    note_scoped_asns,
    parse_claim_doc_path,
)
from lib.protocols.febe.protocol import Session
from lib.shared.paths import CLAIM_FINDINGS_DIR


class ClaimFindingsAgent(Agent):
    """Decompose a review doc into per-finding substrate."""

    role: ClassVar[str] = "claim-findings"

    def run(self, session: Session, review_addr: Address) -> AgentResult:
        review_path = session.get_path_for_addr(review_addr)
        if review_path is None:
            return AgentResult(success=False, detail="no-review-path")

        full_review = session.store.lattice_dir / review_path
        if not full_review.exists():
            return AgentResult(success=False, detail="no-review-file")

        parsed = parse_claim_doc_path(review_path)
        if parsed is None:
            return AgentResult(success=False, detail="unparseable-review-path")
        asn_label, basename, asn_num = parsed
        # Full reviews are `review-N`, cone reviews `cone-N`; both
        # decompose identically. review_stem keys the per-finding subdir,
        # so keep the matched basename verbatim (cone-N stays distinct
        # from review-N under the shared finding tree).
        rev_match = re.match(r"(?:review|cone)-(\d+)$", basename)
        if rev_match is None:
            return AgentResult(success=False, detail="unparseable-review-path")
        review_stem = basename

        body = full_review.read_text()
        findings = extract_findings(body)
        apply_classifier_verdict(findings)

        # Scope to {this ASN} ∪ {note-cited ASNs}. record_findings does a
        # FORWARD lookup label_index[target_label] to mint the finding's
        # comment.revise; with a flat index a finding on a colliding label
        # (e.g. S5, shared by ASN-0036 and ASN-0053) binds to the WRONG
        # ASN's claim — the revise lands on a foreign claim, the real one
        # never gets it, and the "fix locus not an editable claim in THIS
        # ASN" path spuriously downgrades the REVISE to OBSERVE so the next
        # review re-flags it forever.
        label_index = build_cross_asn_label_index(
            session.store, allowed_asns=note_scoped_asns(asn_num),
        )
        emitted = record_findings(
            session, review_addr, findings,
            asn_label, review_stem, label_index,
            findings_dir=CLAIM_FINDINGS_DIR,
        )
        # Zero-findings case: emit one empty-set derivation
        # (F=[review], G=∅) to anchor "decompose ran, produced no
        # derivatives." Predicate `is_review_decomposed` checks for any
        # outbound provenance.derivation; this covers the
        # zero-findings disambiguation without a verb-flag classifier.
        if not emitted:
            emit_empty_derivation(session.store, review_addr)

        print(
            f"  [CLAIM-FINDINGS] {asn_label} {review_stem} "
            f"emitted={len(emitted)}/{len(findings)}",
            file=sys.stderr,
        )
        return AgentResult(
            success=True, detail=f"emitted={len(emitted)}",
        )
