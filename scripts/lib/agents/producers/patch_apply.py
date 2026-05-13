"""Patch-apply agent — predicate-fired on substrate-resident patch.note docs.

Bridge from operationally-emitted patches (e.g., from MotifDispatchAgent)
to the existing apply machinery. The MotifDispatchAgent writes patch
specs directly to substrate and emits the `patch.note` classifier;
this agent fires on any patch.note doc that hasn't yet been applied
(no outbound `provenance.derivation` to a review doc) and runs the
LLM apply + post-apply review.

Reuses `note_patch._apply_patch`, `note_patch._patch_scoped_review`,
and `note_patch._emit_review_with_findings` — the substantive work
is one shared implementation; this module just provides a different
entry point that works on substrate addresses rather than workspace
filenames.

Caste: producer. Identity grants per fire: review doc + per-finding
decomposition + `provenance.derivation(patch → review)`.

Operator-authored workspace patches still go through `note-patch.py`
CLI — its promote+apply lifecycle is unchanged. This agent fires
only on patches that were pre-promoted (e.g., by motif-dispatch).
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import ClassVar, Optional

from lib.agents.base import Agent, AgentResult
from lib.agents.producers.note_patch import (
    _apply_patch, _emit_review_with_findings, _patch_scoped_review,
)
from lib.backend.addressing import Address
from lib.lattice.labels import format_label
from lib.protocols.febe.protocol import Session
from lib.shared.common import find_asn, read_file
from lib.shared.paths import WORKSPACE


APPLY_MODEL = "opus"
APPLY_EFFORT = "max"


class PatchApplyAgent(Agent):
    """Fires on substrate-resident patch.note docs that haven't been
    applied yet. Derives target ASN from the patch's substrate path,
    runs the LLM apply, runs the post-apply review.
    """

    role: ClassVar[str] = "patch-apply"

    def __init__(
        self, *,
        model: str = APPLY_MODEL,
        effort: str = APPLY_EFFORT,
    ):
        self.model = model
        self.effort = effort

    def run(
        self, session: Session, patch_addr: Address,
    ) -> AgentResult:
        # 1. Resolve patch path + content
        patch_rel = session.get_path_for_addr(patch_addr)
        if patch_rel is None:
            return AgentResult(success=False, detail="no-patch-path")
        patch_path = WORKSPACE / patch_rel
        if not patch_path.exists():
            return AgentResult(success=False, detail="no-patch-file")
        patch_content = patch_path.read_text()

        # 2. Derive target ASN from patch path:
        #    `_docuverse/.../patch/note/ASN-NNNN/<filename>.md`
        m = re.search(r"/patch/note/(ASN-\d+)/", patch_rel)
        if not m:
            return AgentResult(
                success=False,
                detail=f"cant-derive-asn-from-path: {patch_rel}",
            )
        asn_label = m.group(1)
        asn_num_match = re.search(r"(\d+)", asn_label)
        if not asn_num_match:
            return AgentResult(
                success=False, detail="cant-parse-asn-number",
            )
        asn_num = int(asn_num_match.group(1))
        asn_path, _ = find_asn(str(asn_num))
        if asn_path is None:
            return AgentResult(
                success=False, detail=f"find_asn-failed: {asn_label}",
            )

        # 3. Substrate-side: target note's address
        note_rel = str(
            asn_path.resolve().relative_to(WORKSPACE.resolve()),
        )
        note_addr = session.store.path_to_addr.get(note_rel)
        if note_addr is None:
            return AgentResult(
                success=False, detail=f"note-not-registered: {note_rel}",
            )

        # 4. Apply via shared helper
        os.environ.setdefault("PROTOCOL_ASN_LABEL", asn_label)
        applied = _apply_patch(
            asn_path, asn_label, patch_content,
            model=self.model, effort=self.effort,
        )
        if not applied:
            return AgentResult(success=False, detail="apply-failed")

        # 5. Post-apply review via shared helper
        review_text = _patch_scoped_review(
            asn_num, asn_path, asn_label, patch_content,
            model=self.model, effort=self.effort,
        )
        if review_text is None:
            return AgentResult(
                success=False, detail="apply-ok-review-failed",
            )
        review_addr, n_findings = _emit_review_with_findings(
            session, asn_label, note_addr, patch_addr, review_text,
        )

        return AgentResult(
            success=True,
            detail=f"applied; review-{review_addr} emitted with {n_findings} finding(s)",
        )
