"""Full-review agent — one cycle per fire over a derived ASN.

Fires on a source note that is quiescent but not confirmed. Performs
ONE cycle:
  1. validate-gate precondition (full ASN; halts on dirty structure)
  2. assemble whole-ASN content
  3. run review (LLM, claim_review agent)
  4. emit review doc + coverage links
  5. sync substrate citations to md across every derived claim
  6. step commit

The per-finding decomposition (extract → override → record_findings)
is the claim-findings producer's job; the runner fires it on the
review_addr emitted in step 4. Open `comment.revise` links those
emit are closed by the claim-revise refiner. The producer's job is
review-and-emit; everything downstream is the runner's.

Structurally identical to cone-review; differences are scope-level:
  - context: ASN label PATH-derived from the canonical claim addr; the
    note is never read post-derivation
  - claims: every claim in the ASN's claim region (asn_claim_addrs) —
    including claims refinement created (vs apex + same-ASN deps)
  - foundation: full upstream (vs narrowed to cross-ASN deps)
  - validate-gate scope: whole ASN (vs cone subset)
  - model: opus (vs sonnet)
"""

from __future__ import annotations

import os
import sys
from typing import ClassVar, List

from lib.agents.base import Agent, AgentResult
from lib.agents.producers.review_helpers import (
    previously_declined_findings, run_review,
)
from lib.agents.producers.cone_review import sync_claim_citations
from lib.backend.addressing import Address
from lib.lattice.findings import emit_review_doc
from lib.lattice.labels import build_cross_asn_label_index, note_scoped_asns
from lib.predicates import (
    asn_claim_addrs, asn_label_for_claim, version_head,
)
from lib.protocols.febe.protocol import Session
from lib.shared.common import assemble_readonly
from lib.shared.foundation import FoundationError, foundation_dep_addrs
from lib.shared.paths import CLAIM_REVIEWS_DIR, next_review_number
from lib.shared.validate_gate import run_validate_gate


FULL_MODEL = "opus"


class FullReviewAgent(Agent):
    """One cycle of whole-ASN deep review.

    The trigger feeds the agent one canonical claim of the ASN; the
    agent path-derives the ASN label from it and multi-holds every
    claim in the ASN's claim region. The note is not consulted.
    """

    role: ClassVar[str] = "full-review"
    node: ClassVar[str] = "1.3"

    def resolve_holds(
        self, session: Session, addr: Address, scope_type: str,
    ) -> List[Address]:
        """Hold every claim of the ASN (region-based — includes claims
        refinement created). Mutex against cone-review (which holds its
        apex) and per-claim refiners."""
        asn_label = asn_label_for_claim(session, addr)
        if asn_label is None:
            return []
        return list(asn_claim_addrs(session, asn_label))

    def run(self, session: Session, addr: Address) -> AgentResult:
        # ASN identity is PATH-derived; the note is never read post-
        # derivation. Claims are enumerated from the claim region so
        # refinement-created claims are reviewed too.
        asn_label = asn_label_for_claim(session, addr)
        if asn_label is None:
            return AgentResult(
                success=False, detail="no-asn-for-canonical-claim",
            )
        asn_num = int(asn_label[4:])
        derived_addrs = list(asn_claim_addrs(session, asn_label))

        # Scope to {this ASN} ∪ {note-cited ASNs}. sync_claim_citations
        # (below) does forward AND reverse label lookups to reconcile each
        # claim's citation graph; a flat index is last-writer-wins, so for
        # a colliding label (S0–S8 are shared by ASN-0036 and ASN-0053) it
        # would sync citations against the WRONG ASN's address — corrupting
        # the depends graph every pass so depends-agreement never converges
        # (a full-review livelock).
        label_index = build_cross_asn_label_index(
            session.store, allowed_asns=note_scoped_asns(asn_num),
        )

        print(
            f"\n  [FULL-REVIEW] {asn_label} "
            f"({len(derived_addrs)} derived claims)",
            file=sys.stderr,
        )

        # 1. Validate-gate (whole ASN).
        gate_result = run_validate_gate(
            asn_label, scope_labels=None, claim_base_dir=self.claim_dir,
        )
        if gate_result != "clean":
            print(
                f"  [GATE] halted — structural violations remain "
                f"({gate_result})", file=sys.stderr,
            )
            return AgentResult(
                success=False, detail=f"gate-failed:{gate_result}",
            )

        # 2. Declined-findings context (suppress re-raise of OBSERVE).
        previous_findings = previously_declined_findings(session, derived_addrs)

        # 3. Assemble + review (full upstream foundation, no narrowing).
        # Claims ONLY — the note is a frozen discovery artifact and must
        # not reach the reviewer (feeding it caused note-drift findings and
        # contaminated correctness judgments). Claims + cited foundation
        # statements are the authoritative review inputs.
        asn_content = assemble_readonly(
            asn_label, self.claim_dir, include_note=False,
        )
        # Effort for the whole-ASN review. Defaults to "max" — the global
        # review is the ASN-wide quality gate (a non-clean draw re-opens
        # every claim's confirmation), so it runs at the top tier, matching
        # claim_revise. Operator-tunable down via FULL_REVIEW_EFFORT
        # (ladder: low/medium/high/xhigh/max) for cheaper test passes.
        # cone_review is unaffected (it keeps run_review's "high" default).
        full_effort = os.environ.get("FULL_REVIEW_EFFORT", "max")
        verdict, findings_text, _elapsed = run_review(
            asn_num, asn_content, asn_label, previous_findings,
            model=FULL_MODEL, effort=full_effort,
        )
        if verdict == "ERROR":
            return AgentResult(success=False, detail="review-error")

        # 4. Emit review doc + coverage links.
        review_num = next_review_number(
            asn_label, kind="claim",
            reviews_dir=CLAIM_REVIEWS_DIR / asn_label,
        )

        # Cascade anchor: snapshot the foundation version each upstream
        # was at when this review read the ASN — exactly the note-side
        # mechanism (see note_review). is_claim_cascade_fresh walks this
        # bundled link and re-fires review if any upstream advanced.
        # Defensive try/except mirrors note_review: skip the anchor
        # rather than leave the review partial if deps go unresolvable
        # between load and emit. Missing anchor → vacuously fresh.
        try:
            cascade_anchor_heads = [
                version_head(session, dep)
                for dep in foundation_dep_addrs(session, asn_num)
            ]
        except FoundationError as e:
            print(
                f"  [FOUNDATION] {asn_label}: cascade-anchor emission "
                f"skipped — deps unresolvable post-load ({e})",
                file=sys.stderr,
            )
            cascade_anchor_heads = []

        review_addr, _ = emit_review_doc(
            session, asn_label, review_num,
            body=findings_text,
            covered_addrs=derived_addrs,
            cascade_anchor_heads=cascade_anchor_heads,
        )

        # 5. Sync substrate citations against md across every derived claim.
        #    sync_claim_citations takes a Session (it does session.store
        #    internally) — pass `session`, not `session.store`.
        for claim_addr in derived_addrs:
            sync_claim_citations(session, claim_addr, label_index)

        # 6. Commit the review-doc emission as a cycle event.

        return AgentResult(success=True, detail=verdict)
