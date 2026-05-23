"""Motif dispatch agent — operational phase, one fire per motif.

Predicate-fired producer. One fire reads a motif + its attribution
sidecar, determines the case (1 vs 2 vs STANDALONE), and emits the
appropriate operational spec docs into substrate. Subsequent agents
(note-patch, note-extract) consume those specs to do the actual work.

Currently implements only Case 1 (patch path). Case 2 / STANDALONE
return a no-op result; their emissions land when those paths are
implemented.

Case 1 logic:
  1. Determine base ASN from the attribution sidecar.
  2. Identify rederiving notes (cited notes minus base).
  3. For each rederiving note, LLM call decides PATCH or NONE.
  4. For each PATCH, write a `patch.note` spec to substrate.
  5. If at least one patch emitted: per-spec
     `provenance.derivation(motif → patch)`.
  6. If zero patches emitted (all NONE): empty-G
     `provenance.derivation(motif → ∅)` — the "ran, nothing to do"
     marker that flips the predicate.

Caste: producer. Operator triggers MotifAgent; the runner picks up
the materialized motif and fires this agent automatically.

TODO — audit gap: NONE decisions per rederiving note (the LLM
verdict "this note already cites the canonical") are not captured
in substrate. Only PATCH decisions land (as the patch spec itself).
A future revision should emit a dispatch-decision summary doc per
fire, recording per-note verdicts with their rationale, so the
audit trail of "we considered ASN-X and judged no patch needed"
is preserved. See _workspace/motif-agentic-plan.md for context.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import ClassVar, Dict, List, Optional, Tuple

import yaml

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.backend.emit import (
    emit_citation, emit_classifier, emit_derivation, emit_empty_derivation,
    emit_patch_note,
)
from lib.lattice.labels import format_label
from lib.predicates.versions import version_head
from lib.protocols.febe.protocol import Session
from lib.shared.common import find_asn, read_file
from lib.shared.frontmatter import read_doc_with_frontmatter
from lib.shared.invoke_claude import invoke_claude
from lib.shared.paths import (
    LATTICE, PATCH_NOTE_DIR, WORKSPACE, prompt_path,
)


DISPATCH_MODEL = "opus"
DISPATCH_EFFORT = "high"

PATCH_PROMPT = prompt_path("agents/producers/motif_dispatch_patch.md")


_FENCE_RE = re.compile(r"^```[^\n]*\n", re.MULTILINE)


def _strip_code_fence(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = _FENCE_RE.sub("", text, count=1)
        end_match = re.search(r"(?<=\n)```[^\n]*\n?", text)
        if end_match:
            text = text[:end_match.start()] + text[end_match.end():]
    return text


def _parse_yaml(text: str):
    return yaml.safe_load(_strip_code_fence(text))


# ─── Substrate readers ─────────────────────────────────────────────


def _read_motif_cited_labels(motif_path: Path) -> List[str]:
    """Parse `cited_claims` keys from the motif doc's frontmatter."""
    fm, _ = read_doc_with_frontmatter(motif_path)
    return list((fm or {}).get("cited_claims") or {})


def _read_attribution(motif_path: Path) -> Tuple[Optional[str], str]:
    """Read the attribution sidecar adjacent to the motif. Returns
    (base_label, rationale_prose). base_label is None for STANDALONE.
    """
    sidecar_path = motif_path.with_name(
        f"{motif_path.stem}.motif.attribution.md",
    )
    if not sidecar_path.exists():
        return None, ""
    text = sidecar_path.read_text()
    m = re.search(r"\*\*Base:\*\*\s*([A-Za-z0-9_\-]+)", text)
    base_label = (
        None if not m or m.group(1).upper() == "STANDALONE"
        else m.group(1)
    )
    # Rationale is everything after the **Base:** line
    after_base = text.split("**Base:**", 1)
    rationale = ""
    if len(after_base) == 2:
        rest = after_base[1]
        rest_lines = rest.split("\n", 1)
        rationale = rest_lines[1].strip() if len(rest_lines) > 1 else ""
    return base_label, rationale


# ─── Patch-spec writer ─────────────────────────────────────────────


def _next_patch_filename(asn_label: str, motif_label: str) -> str:
    """Sequential `<motif>-patch-NNNN.md` per ASN.

    Allows multiple motifs to land patches against the same note without
    collision; numbering is per-(asn, motif) prefix.
    """
    asn_dir = PATCH_NOTE_DIR / asn_label
    nums = []
    if asn_dir.exists():
        pat = re.compile(
            rf"{re.escape(motif_label)}-patch-(\d+)\.md$"
        )
        for p in asn_dir.glob(f"{motif_label}-patch-*.md"):
            mm = pat.match(p.name)
            if mm:
                nums.append(int(mm.group(1)))
    n = max(nums, default=0) + 1
    return f"{motif_label}-patch-{n:04d}.md"


# ─── Agent ─────────────────────────────────────────────────────────


class MotifDispatchAgent(Agent):
    """One fire per motif: case detection + appropriate operational
    spec emission.

    Predicate gates re-fire via the standard "no outbound
    provenance.derivation on the motif" check.
    """

    role: ClassVar[str] = "motif-dispatch"

    def __init__(
        self, *,
        model: str = DISPATCH_MODEL,
        effort: str = DISPATCH_EFFORT,
    ):
        self.model = model
        self.effort = effort

    def run(
        self, session: Session, motif_addr: Address,
    ) -> AgentResult:
        motif_rel = session.get_path_for_addr(motif_addr)
        if motif_rel is None:
            return AgentResult(success=False, detail="motif-path-not-found")
        motif_path = WORKSPACE / motif_rel

        cited_labels = _read_motif_cited_labels(motif_path)
        if not cited_labels:
            return AgentResult(
                success=False, detail="motif-cited-claims-empty",
            )

        base_label, attribution_rationale = _read_attribution(motif_path)
        if base_label is None:
            # STANDALONE — Case 2 / STANDALONE path. Not yet implemented.
            return AgentResult(
                success=True,
                detail="case-standalone-not-impl; no emissions",
            )

        # Case determination: is base among cited notes?
        cited_label_set = {self._canonicalize(c) for c in cited_labels}
        if self._canonicalize(base_label) not in cited_label_set:
            # Case 2 — base is a transitive dep. Not yet implemented.
            return AgentResult(
                success=True,
                detail="case-2-not-impl; no emissions",
            )

        # Case 1: emit patches for each rederiving note.
        rederiving = [
            c for c in cited_labels
            if self._canonicalize(c) != self._canonicalize(base_label)
        ]
        if not rederiving:
            emit_empty_derivation(session.store, motif_addr)
            return AgentResult(
                success=True,
                detail="case-1: no rederiving notes (motif singleton)",
            )

        motif_text = motif_path.read_text()
        emitted_specs: List[Address] = []
        skipped: List[str] = []

        for rederiving_label in rederiving:
            decision = self._dispatch_one_note(
                motif_text=motif_text,
                base_label=base_label,
                attribution_rationale=attribution_rationale,
                rederiving_label=rederiving_label,
            )
            if decision is None or decision.get("action") == "NONE":
                skipped.append(rederiving_label)
                continue
            if decision.get("action") != "PATCH":
                skipped.append(rederiving_label)
                continue
            patch_addr = self._emit_patch_spec(
                session, motif_addr, motif_path, rederiving_label,
                decision.get("patch_body") or "",
                decision.get("rationale") or "",
            )
            if patch_addr is not None:
                emitted_specs.append(patch_addr)

        if not emitted_specs:
            emit_empty_derivation(session.store, motif_addr)
            return AgentResult(
                success=True,
                detail=(
                    f"case-1: no patches needed; "
                    f"all {len(rederiving)} rederiving notes already cite"
                ),
            )

        return AgentResult(
            success=True,
            detail=(
                f"case-1: emitted {len(emitted_specs)} patch spec(s); "
                f"skipped {len(skipped)}"
            ),
        )

    # ── LLM dispatch per rederiving note ───────────────────────────

    def _dispatch_one_note(
        self, *, motif_text: str, base_label: str,
        attribution_rationale: str, rederiving_label: str,
    ) -> Optional[dict]:
        path, label = find_asn(self._asn_num_from_label(rederiving_label))
        if path is None:
            return None
        rederiving_body = path.read_text()
        template = read_file(PATCH_PROMPT)
        if not template:
            return None
        prompt = (
            template
            .replace("{{motif}}", motif_text)
            .replace("{{base_label}}", base_label)
            .replace("{{attribution_rationale}}", attribution_rationale)
            .replace("{{rederiving_label}}", label)
            .replace("{{rederiving_note}}", rederiving_body)
        )
        result = invoke_claude(
            prompt, model=self.model, effort=self.effort,
            tools="", output_format=None,
        )
        if not result.text:
            return None
        return _parse_yaml(result.text)

    # ── Patch-spec emission ────────────────────────────────────────

    def _emit_patch_spec(
        self, session: Session, motif_addr: Address,
        motif_path: Path, rederiving_label: str,
        patch_body: str, rationale: str,
    ) -> Optional[Address]:
        """Write the patch md directly to the substrate path, register
        it, emit `patch.note` classifier + `provenance.derivation` from
        motif. Skips the workspace inbox — pre-promoted into substrate.
        """
        asn_num = self._asn_num_from_label(rederiving_label)
        if asn_num is None:
            return None
        asn_label = format_label(int(asn_num))
        motif_stem = motif_path.stem  # e.g. "motif-0001"
        filename = _next_patch_filename(asn_label, motif_stem)
        target_dir = PATCH_NOTE_DIR / asn_label
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / filename

        body = (
            f"# Patch — {motif_stem} → {asn_label}\n\n"
            f"_Generated by motif-dispatch._\n\n"
            f"**Rationale.** {rationale.strip()}\n\n"
            f"{patch_body.strip()}\n"
        )
        target_path.write_text(body)

        rel = str(target_path.relative_to(WORKSPACE))
        patch_addr = session.store.register_path(rel)
        emit_patch_note(session.store, patch_addr)
        emit_derivation(session.store, motif_addr, patch_addr)

        return patch_addr

    # ── Label helpers ──────────────────────────────────────────────

    def _canonicalize(self, label: str) -> str:
        """Reduce `ASN-0034` or `ASN-34` to a canonical form for set
        comparison. Returns the zero-padded label."""
        num = self._asn_num_from_label(label)
        return format_label(int(num)) if num else label

    def _asn_num_from_label(self, label: str) -> Optional[str]:
        m = re.search(r"(\d+)", label or "")
        return m.group(1) if m else None
