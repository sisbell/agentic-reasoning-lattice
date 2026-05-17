"""Cone-review producer — focused regional review on an apex claim.

One cycle per fire. Fires on an apex claim that hasn't reached
quiescence. Performs:
  1. validate-gate precondition (halts on dirty structure)
  2. assemble cone content + cross-ASN foundation
  3. run review (LLM)
  4. emit review doc + per-finding docs + coverage links
  5. sync substrate citations to claim md
  6. step commit

The runner re-fires if `is_claim_quiescent(addr)` is still false after
this cycle. The cycle loop that used to live in run_cone_review now
lives in the runner: predicate true means quiescent.

Helpers inlined:
  - cone scope (assemble_cone, transitive_same_asn_deps,
    cross_asn_deps_in_cone) — substrate walks and content assembly
  - citation sync (sync_claim_citations) — bring substrate
    citation.depends/forward into agreement with the claim md's
    *Depends:* / *Forward References:* sections (safety net after
    agentic edits that didn't emit substrate calls)
  - run_cone_review legacy multi-cycle wrapper (operator-invoked
    via `scripts/run-trigger.py full_review <asn>`)
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import ClassVar, Dict, List, Optional, Set

from lib.agents.base import Agent, AgentResult
from lib.agents.producers.review_helpers import (
    previously_declined_findings, run_review,
)
from lib.backend.addressing import Address
from lib.backend.emit import emit_citation, emit_retraction
from lib.backend.predicates import active_links
from lib.backend.store import Store
from lib.lattice.context import claim_context_from_addr
from lib.lattice.findings import emit_review_doc
from lib.lattice.labels import build_cross_asn_label_index
from lib.predicates.versions import version_head
from lib.protocols.febe.protocol import Session
from lib.shared.claim_files import build_label_index
from lib.shared.paths import CLAIM_REVIEWS_DIR, next_review_number
from lib.shared.validate_gate import run_validate_gate


CONE_MODEL = "sonnet"
_DEPENDS_HEADER = "- *Depends:*"
_FORWARD_HEADER = "- *Forward References:*"


# ─── Cone scope: transitive deps + content assembly ─────────────────


def assemble_cone(asn_label, apex_label, dep_labels, claim_base_dir):
    """Assemble just the cone claims for focused review.

    Returns concatenated text of apex + same-ASN dependency claims.
    """
    claim_dir = claim_base_dir / asn_label
    label_index = build_label_index(claim_dir)
    parts = []

    for label in dep_labels + [apex_label]:
        stem = label_index.get(label)
        if stem is None:
            continue
        md_path = claim_dir / f"{stem}.md"
        if md_path.exists():
            parts.append(md_path.read_text().strip())

    return "\n\n---\n\n".join(parts)


def transitive_same_asn_deps(
    session: Session,
    apex_addr: Address,
    asn_labels: Set[str],
    rev_index: Dict[Address, str],
) -> List[str]:
    """BFS through citation.depends from `apex_addr`, returning the
    list of same-ASN labels reachable (excluding the apex itself).

    Walks only `citation.depends` (backward grounding); forward
    citations are deliberately not followed — the cone is the apex's
    grounding chain, not the downstream tree. Same-ASN only —
    cross-ASN deps are delivered separately via foundation_statements.
    """
    state = session.state

    def _base(addr: Address) -> Address:
        cur = addr
        while state.parent.get(cur) is not None:
            cur = state.parent[cur]
        return cur

    # Citations are emitted from version_head and target version_head.
    # Walk from each visited claim's head; resolve cited targets back
    # to base for rev_index lookup.
    apex_base = _base(apex_addr)
    visited = {apex_base}
    queue = [apex_base]
    deps: List[str] = []
    while queue:
        cur = queue.pop(0)
        cur_head = version_head(session, cur)
        for link in session.active_links(
            "citation.depends", from_set=[cur_head],
        ):
            for target in link.to_set:
                target_base = _base(target)
                if target_base in visited:
                    continue
                visited.add(target_base)
                label = rev_index.get(target_base)
                if label and label in asn_labels:
                    deps.append(label)
                    queue.append(target_base)
    return deps


def cross_asn_deps_in_cone(
    session: Session,
    cone_labels: List[str],
    label_index: Dict[str, Address],
    rev_index: Dict[Address, str],
    asn_labels: Set[str],
) -> List[str]:
    """Cross-ASN deps cited by anything in the cone.

    Used to narrow the foundation context loaded for the reviewer
    prompt: only deps that live outside this ASN need explicit
    foundation loading; same-ASN deps are already in `cone_labels`.
    """
    state = session.state

    def _base(addr: Address) -> Address:
        cur = addr
        while state.parent.get(cur) is not None:
            cur = state.parent[cur]
        return cur

    cross: List[str] = []
    for label in cone_labels:
        from_addr = label_index.get(label)
        if from_addr is None:
            continue
        # Walk from claim's head; resolve cited targets back to base
        # for rev_index lookup.
        for link in session.active_links(
            "citation.depends",
            from_set=[version_head(session, from_addr)],
        ):
            for cited in link.to_set:
                dep_label = rev_index.get(_base(cited))
                if (
                    dep_label
                    and dep_label not in asn_labels
                    and dep_label not in cross
                ):
                    cross.append(dep_label)
    return cross


# ─── Citation sync (md ↔ substrate) ─────────────────────────────────


def _md_labels_in_section(md_text: str, header: str) -> set[str]:
    """The set of bullet labels in a `*<Field>:*` section.

    Empty if the header is absent. The label is the first
    whitespace-delimited token after the `  - ` prefix.
    """
    in_section = False
    labels: set[str] = set()
    for line in md_text.split("\n"):
        if line.strip() == header.strip():
            in_section = True
            continue
        if not in_section:
            continue
        if line.startswith("  - "):
            labels.add(line[4:].split(None, 1)[0])
        elif line.startswith("    ") or line.strip() == "":
            continue
        else:
            break
    return labels


def _substrate_labels(
    session: Session,
    from_addr: Address,
    type_str: str,
    rev_index: Dict[Address, str],
) -> set[str]:
    """Labels currently active in substrate as `type_str` citations
    from `from_addr`. The cited target may be a version_head address;
    walk its parent chain back to the base identity for rev_index
    lookup.
    """
    out: set[str] = set()
    state = session.state
    for link in active_links(state, type_str, from_set=[from_addr]):
        for cited in link.to_set:
            base = _base_identity(state, cited)
            if base in rev_index:
                out.add(rev_index[base])
    return out


def _base_identity(state, addr: Address) -> Address:
    """Walk version-parent chain to the base identity (root of chain)."""
    cur = addr
    while state.parent.get(cur) is not None:
        cur = state.parent[cur]
    return cur


def sync_claim_citations(
    session: Session,
    claim_addr: Address,
    label_index: Dict[str, Address],
) -> Optional[dict]:
    """Bring substrate `citation.depends` / `citation.forward` into
    agreement with the claim md's `*Depends:*` / `*Forward References:*`
    sections.

    Citations are emitted from `version_head(claim_addr)` (the claim's
    current head version) targeting `version_head(target)` (each
    upstream's current head). After register_version on the claim, new
    citations land on the new version; old citations on the prior
    version stay in substrate as history but aren't queried for
    cascade-fresh purposes (the predicate reads from version_head).

    For each direction:
    - Labels in .md but not in active substrate-from-head → emit
      citation from claim's head to target's head
    - Labels in active substrate-from-head but not in .md → retract

    Labels in .md that don't resolve in `label_index` are skipped.
    Returns a changes dict, or None if the .md file isn't on disk.

    Safety net after agentic revise operations that may edit prose
    without emitting matching substrate calls. Drift detection is
    set-comparison, not history-based — distributed-safe.
    """
    store = session.store
    claim_path = store.path_for_addr(claim_addr)
    if claim_path is None:
        return None
    full_path = store.lattice_dir / claim_path
    if not full_path.exists():
        return None

    claim_head = version_head(session, claim_addr)
    rev_index: Dict[Address, str] = {
        addr: lbl for lbl, addr in label_index.items()
    }
    md_text = full_path.read_text()

    md_depends = _md_labels_in_section(md_text, _DEPENDS_HEADER)
    md_forwards = _md_labels_in_section(md_text, _FORWARD_HEADER)
    sub_depends = _substrate_labels(
        session, claim_head, "citation.depends", rev_index,
    )
    sub_forwards = _substrate_labels(
        session, claim_head, "citation.forward", rev_index,
    )

    changes = {
        "depends": {"added": [], "retracted": []},
        "forward": {"added": [], "retracted": []},
    }

    for label in sorted(md_depends - sub_depends):
        if label not in label_index:
            continue
        target_head = version_head(session, label_index[label])
        emit_citation(
            store, claim_head, target_head, direction="depends",
        )
        changes["depends"]["added"].append(label)

    for label in sorted(sub_depends - md_depends):
        if label not in label_index:
            continue
        # Retract any active citation from claim_head whose to_set
        # base-identity matches this label.
        for link in active_links(
            store.state, "citation.depends", from_set=[claim_head],
        ):
            for cited in link.to_set:
                if _base_identity(store.state, cited) == label_index[label]:
                    emit_retraction(store, claim_head, link.addr)
                    changes["depends"]["retracted"].append(label)
                    break
            else:
                continue
            break

    for label in sorted(md_forwards - sub_forwards):
        if label not in label_index:
            continue
        target_head = version_head(session, label_index[label])
        emit_citation(
            store, claim_head, target_head, direction="forward",
        )
        changes["forward"]["added"].append(label)

    for label in sorted(sub_forwards - md_forwards):
        if label not in label_index:
            continue
        for link in active_links(
            store.state, "citation.forward", from_set=[claim_head],
        ):
            for cited in link.to_set:
                if _base_identity(store.state, cited) == label_index[label]:
                    emit_retraction(store, claim_head, link.addr)
                    changes["forward"]["retracted"].append(label)
                    break
            else:
                continue
            break

    return changes


# ─── Agent class ────────────────────────────────────────────────────


class ConeReviewAgent(Agent):
    """One cycle of focused regional review on an apex claim.

    The runner replaces the multi-cycle loop. Each fire is independent;
    state lives in the substrate.
    """

    role: ClassVar[str] = "cone-review"
    node: ClassVar[str] = "1.3"

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

        # 1. Validate-gate precondition.
        gate_scope = {ctx.label} | set(dep_labels)
        gate_result = run_validate_gate(
            ctx.asn_label, scope_labels=gate_scope,
            claim_base_dir=self.claim_dir,
        )
        if gate_result != "clean":
            print(
                f"  [GATE] halted — structural violations remain in cone "
                f"({gate_result})", file=sys.stderr,
            )
            return AgentResult(
                success=False, detail=f"gate-failed:{gate_result}",
            )

        # 2. Declined-findings context (suppress re-raise of OBSERVE).
        cone_addrs = [ctx.addr] + [
            label_index[d] for d in dep_labels if d in label_index
        ]
        previous_findings = previously_declined_findings(session, cone_addrs)

        # 3. Assemble + review.
        cone_content = assemble_cone(
            ctx.asn_label, ctx.label, dep_labels, self.claim_dir,
        )
        verdict, findings_text, elapsed = run_review(
            ctx.asn_num, cone_content, ctx.asn_label, previous_findings,
            model=CONE_MODEL, foundation_labels=cross_asn_deps,
        )
        if verdict == "ERROR":
            return AgentResult(success=False, detail="review-error")

        # 4. Emit review doc + coverage links. The per-finding
        # decomposition (extract → override → record_findings) is the
        # claim-findings producer's job; the runner fires it on the
        # review_addr emitted here.
        review_num = next_review_number(
            ctx.asn_label, kind="claim",
            reviews_dir=CLAIM_REVIEWS_DIR / ctx.asn_label,
        )

        review_addr, _ = emit_review_doc(
            session, ctx.asn_label, review_num,
            body=findings_text,
            covered_addrs=cone_addrs,
        )

        # 5. Sync substrate citations against md as source of truth.
        for label in [ctx.label] + dep_labels:
            from_addr = label_index.get(label)
            if from_addr is None:
                continue
            sync_claim_citations(session, from_addr, label_index)

        # 6. Commit the review-doc emission as a cycle event.

        return AgentResult(success=True, detail=verdict)


