"""Cone-review agent — one cycle per fire.

Fires on an apex claim that hasn't converged. Performs ONE cycle:
  1. retry unresolved revises from prior runs
  2. validate-gate precondition (halts on dirty structure)
  3. assemble cone content + cross-ASN foundation
  4. run review (LLM, claim_review agent)
  5. extract findings + apply finding-override classifier (LLM)
  6. emit review doc + per-finding docs + coverage/comment links
  7. dispatch revise per REVISE finding (LLM, claim_revise agent)
  8. sync substrate citations to claim md
  9. step commit

The runner re-fires if `is_claim_converged(addr)` is still false after
this cycle. The cycle loop that used to live in run_cone_review now
lives in the runner: predicate true means quiescent.
"""

from __future__ import annotations

import sys
from typing import ClassVar

from lib.agents.base import Agent, AgentResult
from lib.agents.claim_finding_override import apply_classifier_verdict
from lib.agents.claim_review import (
    extract_findings, filter_revise, run_review,
)
from lib.agents.claim_revise import revise
from lib.backend.addressing import Address
from lib.lattice.findings import emit_review_doc, record_findings
from lib.lattice.context import claim_context_from_addr
from lib.lattice.labels import build_cross_asn_label_index
from lib.orchestrators.retry import (
    _declined_findings_for_cone, _retry_unresolved_revises,
)
from lib.protocols.febe.protocol import Session
from lib.shared.claim_files import build_label_index
from lib.shared.git_ops import step_commit_asn
from lib.shared.paths import (
    CLAIM_FINDINGS_DIR, CLAIM_REVIEWS_DIR, next_review_number,
)
from lib.shared.validate_gate import run_validate_gate

from .scope import (
    assemble_cone, cross_asn_deps_in_cone, transitive_same_asn_deps,
)


CONE_MODEL = "sonnet"


class ConeReviewAgent(Agent):
    """One cycle of focused regional review on an apex claim.

    The runner replaces the multi-cycle loop. Each fire is independent;
    state lives in the substrate.
    """

    role: ClassVar[str] = "cone-review"

    def run(self, session: Session, addr: Address) -> AgentResult:
        ctx = claim_context_from_addr(session, addr)

        # Derive cone shape from substrate (transitive deps).
        label_index = build_cross_asn_label_index(session.store)
        rev_index = {a: lbl for lbl, a in label_index.items()}
        asn_labels = set(build_label_index(ctx.claim_dir).keys())
        dep_labels = transitive_same_asn_deps(
            session, ctx.addr, asn_labels, rev_index,
        )

        cross_asn_deps = cross_asn_deps_in_cone(
            session, [ctx.label] + dep_labels,
            label_index, rev_index, asn_labels,
        )

        print(
            f"\n  [REGIONAL-REVIEW] {ctx.label} + {len(dep_labels)} deps; "
            f"foundation: {len(cross_asn_deps)} cross-ASN",
            file=sys.stderr,
        )

        # 1. Close any lingering revises so this cycle starts clean.
        _retry_unresolved_revises(
            session, ctx.asn_num, ctx.claim_dir, [ctx.addr],
        )

        # 2. Validate-gate precondition.
        gate_scope = {ctx.label} | set(dep_labels)
        gate_result = run_validate_gate(
            ctx.asn_label, scope_labels=gate_scope,
        )
        if gate_result != "clean":
            print(
                f"  [GATE] halted — structural violations remain in cone "
                f"({gate_result})", file=sys.stderr,
            )
            return AgentResult(
                success=False, detail=f"gate-failed:{gate_result}",
            )

        # 3. Declined-findings context (suppress re-raise of OBSERVE).
        cone_addrs = [ctx.addr] + [
            label_index[d] for d in dep_labels if d in label_index
        ]
        previous_findings = _declined_findings_for_cone(session, cone_addrs)

        # 4. Assemble + review.
        cone_content = assemble_cone(ctx.asn_label, ctx.label, dep_labels)
        verdict, findings_text, elapsed = run_review(
            ctx.asn_num, cone_content, ctx.asn_label, previous_findings,
            model=CONE_MODEL, foundation_labels=cross_asn_deps,
        )
        if verdict == "ERROR":
            return AgentResult(success=False, detail="review-error")

        # 5. Extract findings + apply override classifier.
        findings = extract_findings(findings_text)
        apply_classifier_verdict(findings)

        # 6. Emit review doc + per-finding docs + coverage links.
        review_num = next_review_number(
            ctx.asn_label, kind="claim",
            reviews_dir=CLAIM_REVIEWS_DIR / ctx.asn_label,
        )
        review_stem = f"review-{review_num}"

        review_addr, _ = emit_review_doc(
            session, ctx.asn_label, review_num,
            body=findings_text,
            covered_addrs=cone_addrs,
        )
        emitted_findings = record_findings(
            session, review_addr, findings,
            ctx.asn_label, review_stem, label_index,
            findings_dir=CLAIM_FINDINGS_DIR,
        )
        emitted_by_title = {e["title"]: e for e in emitted_findings}
        emitted_titles = set(emitted_by_title.keys())
        emitted_for_filter = [f for f in findings if f[0] in emitted_titles]
        revise_findings = filter_revise(emitted_for_filter)

        for title_text, cls, _ in findings:
            print(f"  [{cls}] {title_text}", file=sys.stderr)

        # 7. Per-finding revise.
        any_changed = False
        for title_text, _cls, finding_text in revise_findings:
            emitted = emitted_by_title.get(title_text)
            if emitted is None:
                print(
                    f"  [WARN] orphan revise — finding {title_text[:60]!r}",
                    file=sys.stderr,
                )
                continue
            ok = revise(
                ctx.asn_num, title_text, finding_text,
                claim_dir=ctx.claim_dir,
                comment_id=str(emitted["comment_id"]),
                claim_path=emitted["claim_path"],
            )
            if ok:
                any_changed = True

        # 8. Sync substrate citations against md as source of truth.
        from .sync import sync_claim_citations
        for label in [ctx.label] + dep_labels:
            from_addr = label_index.get(label)
            if from_addr is None:
                continue
            sync_claim_citations(session.store, from_addr, label_index)

        # 9. Commit if anything changed this cycle.
        if revise_findings or any_changed:
            step_commit_asn(
                ctx.asn_num,
                f"cone-review(asn): {ctx.asn_label}/{ctx.label}",
            )

        return AgentResult(success=True, detail=verdict)
