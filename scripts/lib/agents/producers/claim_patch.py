"""Claim-patch producer — apply a targeted fix to an ASN's claim files.

Operator-gated producer. One fire = promote a workspace patch md to a
substrate-citizen `patch` doc, apply the patch via LLM (editing claim
md files in place), run a one-shot patch-scoped review that emits
findings as substrate, commit. Standard claim convergence machinery
(claim_findings → claim_revise) picks up the open findings on the
next runner walk.

The agent does NOT drive convergence itself. The patch-scoped review
emits a `review.content`-classified review doc; `claim_findings`'s
predicate fires (review undecomposed) → emits per-finding docs +
`comment.revise` links to affected claims; `claim_revise`'s predicate
fires (open `comment.revise` findings) → addresses them.

Caste: producer. Identity grants per fire:

  - `patch.claim` classifier on the substrate patch doc
  - `provenance.derivation(F=[patch], G=[note])` audit edge
  - `review.content` classifier on the patch-scoped review doc
  - `review.coverage(review → each derived claim)` — same shape as
    standard claim review
  - `provenance.derivation(F=[patch], G=[review])` — review tied to
    patch fire

Operator workflow:

  1. Drop a patch md into `_workspace/patches/claim/<ASN-NNNN>/<filename>.md`.
  2. Run `python scripts/claim-patch.py <asn> --patch <filename>`.
  3. The runner walks afterward (operator invokes `full_review`,
     `claim_findings`, `claim_revise` via `scripts/run-trigger.py
     NAME <asn>`, or a daemon picks it up) and drives convergence
     on the findings the patch reviewer filed.

The patch-scoped review uses
`prompts/shared/claim-refinement/patch/review.md` (REVISE-only,
narrows scope to patched material). Its output format matches
`extract_findings` so `claim_findings` decomposes naturally into
per-finding substrate.
"""

from __future__ import annotations

import os
import re
import shutil
import sys
from pathlib import Path
from typing import ClassVar

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.backend.emit import emit_derivation, emit_patch_claim
from lib.lattice.findings import emit_review_doc
from lib.lattice.labels import extract_label_digits, format_label
from lib.predicates import derived_claims
from lib.protocols.febe.protocol import Session
from lib.shared.campaign import resolve_campaign
from lib.shared.common import assemble_readonly, find_asn, log_usage, read_file
from lib.shared.foundation import FoundationError, load_foundation
from lib.shared.invoke_claude import invoke_claude, invoke_claude_agent
from lib.shared.paths import (
    CLAIM_REVIEWS_DIR, LATTICE,
    PATCH_CLAIM_DIR, PATCH_INBOX_CLAIM,
    WORKSPACE, next_review_number, prompt_path,
)
from lib.shared.prompts import read_prompt


PATCH_MODEL = "opus"
PATCH_EFFORT = "max"

APPLY_TEMPLATE = prompt_path("agents/producers/claim_patch/apply.md")
REVIEW_TEMPLATE = prompt_path("agents/producers/claim_patch/review.md")


# ─── Patch promotion (workspace → substrate) ────────────────────────


def _promote_patch_to_substrate(
    session: Session,
    note_addr: Address,
    asn_label: str,
    patch_filename: str,
):
    """Copy the workspace patch md into the substrate doc tree, register
    its path, emit `patch` classifier + `provenance.derivation` from
    patch → note. Returns (substrate_path, patch_addr), or None if the
    workspace patch is missing.
    """
    workspace_path = PATCH_INBOX_CLAIM / asn_label / patch_filename
    if not workspace_path.exists():
        print(
            f"  [ERROR] Patch not found in workspace: "
            f"{workspace_path.relative_to(WORKSPACE)}",
            file=sys.stderr,
        )
        return None

    substrate_dir = PATCH_CLAIM_DIR / asn_label
    substrate_dir.mkdir(parents=True, exist_ok=True)
    substrate_path = substrate_dir / patch_filename
    shutil.copy2(workspace_path, substrate_path)

    substrate_rel = str(
        substrate_path.resolve().relative_to(WORKSPACE.resolve())
    )
    patch_addr = session.store.register_path(substrate_rel)

    emit_patch_claim(session.store, patch_addr)
    emit_derivation(session.store, patch_addr, note_addr)

    print(
        f"  [PROMOTE] {workspace_path.relative_to(WORKSPACE)} → "
        f"{substrate_path.relative_to(WORKSPACE)}",
        file=sys.stderr,
    )
    return substrate_path, patch_addr


# ─── LLM steps ──────────────────────────────────────────────────────


def _apply_patch(
    asn_path: Path, asn_label: str, patch_content: str,
    *, model: str, effort: str,
) -> bool:
    """Apply patch to claim files via LLM with Edit tools."""
    template = read_prompt(APPLY_TEMPLATE)
    if not template:
        print("  [ERROR] Apply prompt template not found", file=sys.stderr)
        return False

    prompt = (
        template
        .replace("{{patch_content}}", patch_content)
        .replace("{{asn_path}}", str(asn_path.relative_to(WORKSPACE)))
    )
    print(f"  [PATCH] Applying to {asn_label}...", file=sys.stderr)
    response = invoke_claude_agent(
        prompt, model=model, effort=effort,
        tools="Edit,Read,Glob,Grep", max_turns=15,
    )
    if response.data is None:
        print(f"  [ERROR] Patch application failed", file=sys.stderr)
        return False
    print(f"  [APPLIED] {asn_label}", file=sys.stderr)
    return True


def _patch_scoped_review(
    asn_num: int, asn_path: Path, asn_label: str, patch_content: str,
    *, model: str, effort: str, claim_base_dir: Path | None = None,
) -> str | None:
    """One-shot patch-scoped review. Returns review text, or None on
    LLM failure."""
    asn_content = assemble_readonly(asn_label, claim_base_dir)
    vocabulary = read_file(resolve_campaign(asn_num).vocabulary_path)
    try:
        foundation = load_foundation(asn_num)
    except FoundationError as e:
        print(
            f"  [FOUNDATION] {asn_label}: {e}",
            file=sys.stderr,
        )
        return None

    template = read_prompt(REVIEW_TEMPLATE)
    if not template:
        print("  [ERROR] Review prompt template not found", file=sys.stderr)
        return None

    prompt = (
        template
        .replace("{{asn_label}}", asn_label)
        .replace("{{asn_content}}", asn_content)
        .replace("{{patch_content}}", patch_content)
        .replace("{{vocabulary}}", vocabulary)
        .replace("{{foundation_statements}}", foundation)
    )

    print(f"  [REVIEW] Patch-scoped claim review of {asn_label}...", file=sys.stderr)
    result = invoke_claude(prompt, model=model, effort=effort)
    if not result.text:
        print(f"  [WARN] Patch review produced no output", file=sys.stderr)
        return None
    log_usage("claim-patch-review", result.elapsed, asn=asn_num)
    return result.text


# ─── Agent class ────────────────────────────────────────────────────


class ClaimPatchAgent(Agent):
    """One claim patch application per fire.

    Pure producer (operator-gated). Promotes the workspace patch to
    substrate, applies it to the claim files, emits a patch-scoped
    review (with `review.content` classifier + coverage), and stops.
    `claim_findings` decomposes the review next runner pass; then
    `claim_revise` picks up the comment.revise findings.
    """

    role: ClassVar[str] = "claim-patch"
    node: ClassVar[str] = "1.3"

    def __init__(
        self, *,
        model: str = PATCH_MODEL,
        effort: str = PATCH_EFFORT,
    ):
        self.model = model
        self.effort = effort

    def run(
        self, session: Session, note_addr: Address,
        *, patch_filename: str,
    ) -> AgentResult:
        # 1. Resolve note + ASN identity
        note_rel = session.get_path_for_addr(note_addr)
        if note_rel is None:
            return AgentResult(success=False, detail="no-note-path")

        digits = extract_label_digits(note_rel)
        if digits is None:
            return AgentResult(success=False, detail="unparseable-note-path")
        asn_num = int(digits)
        asn_label = format_label(asn_num)
        asn_path, _ = find_asn(str(asn_num))
        if asn_path is None:
            return AgentResult(success=False, detail="find_asn-failed")

        os.environ.setdefault("PROTOCOL_ASN_LABEL", asn_label)

        # 2. Promote workspace patch → substrate
        promotion = _promote_patch_to_substrate(
            session, note_addr, asn_label, patch_filename,
        )
        if promotion is None:
            return AgentResult(success=False, detail="patch-not-in-workspace")
        substrate_path, patch_addr = promotion
        patch_content = substrate_path.read_text()

        # 3. Apply the patch
        ok = _apply_patch(
            asn_path, asn_label, patch_content,
            model=self.model, effort=self.effort,
        )
        if not ok:
            return AgentResult(success=False, detail="apply-failed")
        # The patch may have edited any subset of derived claims;
        # advance the supersession chain on each so cascade-fresh
        # detects the edit on whichever claims were actually touched.
        # Conservative: includes claims that weren't edited (their
        # downstream just re-fires once and finds nothing).
        for derived in derived_claims(session, note_addr):
            session.register_version(derived)
        log_usage("claim-patch-apply", 0, asn=asn_num)

        # 4. Patch-scoped review
        review_text = _patch_scoped_review(
            asn_num, asn_path, asn_label, patch_content,
            model=self.model, effort=self.effort,
            claim_base_dir=self.claim_dir,
        )
        if review_text is None:
            return AgentResult(success=False, detail="review-failed")

        # 5. Emit review doc + classifier + coverage to all derived claims
        review_num = next_review_number(
            asn_label, kind="claim",
            reviews_dir=CLAIM_REVIEWS_DIR / asn_label,
        )
        derived = list(derived_claims(session, note_addr))
        review_addr, _ = emit_review_doc(
            session, asn_label, review_num,
            body=review_text,
            covered_addrs=derived,
        )
        emit_derivation(session.store, patch_addr, review_addr)

        # 6. Final commit
        log_usage("claim-patch-complete", 0, asn=asn_num)

        print(
            f"  [REVIEW] Emitted review-{review_num} covering "
            f"{len(derived)} claim(s); claim_findings will decompose, "
            f"claim_revise will pick up the comment.revise findings.",
            file=sys.stderr,
        )

        return AgentResult(
            success=True,
            detail=f"patch={patch_filename} review={review_addr}",
        )
