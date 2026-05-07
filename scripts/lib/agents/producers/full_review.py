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
  - context: `AsnContext` from a note address (vs claim address)
  - claims: all derivations of the note (vs apex + same-ASN deps)
  - foundation: full upstream (vs narrowed to cross-ASN deps)
  - validate-gate scope: whole ASN (vs cone subset)
  - model: opus (vs sonnet)
"""

from __future__ import annotations

import sys
from typing import ClassVar

from lib.agents.base import Agent, AgentResult
from lib.agents.producers.review_helpers import (
    previously_declined_findings, run_review,
)
from lib.agents.producers.cone_review import sync_claim_citations
from lib.backend.addressing import Address
from lib.lattice.findings import emit_review_doc
from lib.lattice.context import asn_context_from_note
from lib.lattice.labels import build_cross_asn_label_index
from lib.protocols.febe.protocol import Session
from lib.shared.common import assemble_readonly
from lib.shared.git_ops import step_commit_asn
from lib.shared.paths import CLAIM_REVIEWS_DIR, next_review_number
from lib.shared.validate_gate import run_validate_gate


FULL_MODEL = "opus"


class FullReviewAgent(Agent):
    """One cycle of whole-ASN deep review on a source note."""

    role: ClassVar[str] = "full-review"

    def run(self, session: Session, addr: Address) -> AgentResult:
        ctx = asn_context_from_note(session, addr)
        derived_addrs = list(ctx.derived_claim_addrs)

        label_index = build_cross_asn_label_index(session.store)

        print(
            f"\n  [FULL-REVIEW] {ctx.asn_label} "
            f"({len(derived_addrs)} derived claims)",
            file=sys.stderr,
        )

        # 1. Validate-gate (whole ASN).
        gate_result = run_validate_gate(ctx.asn_label, scope_labels=None)
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
        asn_content = assemble_readonly(ctx.asn_label)
        verdict, findings_text, _elapsed = run_review(
            ctx.asn_num, asn_content, ctx.asn_label, previous_findings,
            model=FULL_MODEL,
        )
        if verdict == "ERROR":
            return AgentResult(success=False, detail="review-error")

        # 4. Emit review doc + coverage links.
        review_num = next_review_number(
            ctx.asn_label, kind="claim",
            reviews_dir=CLAIM_REVIEWS_DIR / ctx.asn_label,
        )

        review_addr, _ = emit_review_doc(
            session, ctx.asn_label, review_num,
            body=findings_text,
            covered_addrs=derived_addrs,
        )

        # 5. Sync substrate citations against md across every derived claim.
        for claim_addr in ctx.derived_claim_addrs:
            sync_claim_citations(session.store, claim_addr, label_index)

        # 6. Commit the review-doc emission as a cycle event.
        step_commit_asn(
            ctx.asn_num,
            f"full-review(asn): {ctx.asn_label} review-{review_num}",
        )

        return AgentResult(success=True, detail=verdict)


def run_full_review(asn_num, *, max_cycles: int = 8) -> str:
    """Legacy multi-cycle wrapper: drive full_review + claim_revise
    triggers until quiescence. Returns "quiescent" / "not_quiescent" /
    "failed".

    Wraps the runner-driven path — the previous internal cycle loop
    inside this wrapper retired when claim_revise was lifted to a
    predicate-fired Agent class. The runner walks both triggers until
    every comment.revise on the ASN's claims is closed and the
    ASN's review coverage is current.
    """
    from lib.runner import asn, run_until_quiescent
    from lib.triggers import claim_findings, claim_revise, full_review

    result = run_until_quiescent(
        triggers=[full_review, claim_findings, claim_revise],
        scope=asn(asn_num),
        max_iterations=max_cycles,
    )
    if result.errors:
        return "failed"
    return "quiescent" if result.quiescent else "not_quiescent"
