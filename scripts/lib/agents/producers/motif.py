"""Motif agent — one fire produces a motif (substrate citizen).

Operator-gated producer. One fire:

  1. Scout the input notes for like-claim correspondences (≥3 notes).
  2. Materialize a `motifs` snapshot doc with the scout's candidate list.
  3. Select the most worthwhile motif (or reject the batch).
  4. On select: materialize a `motif` doc with its citation anchors to
     the cited claims.
  5. Attribute the motif to a base (the deepest note whose vocabulary
     owns the construct's primitives); emit a `motif.attribution`
     sidecar with rationale + a `citation.depends` link to the base
     (omitted for STANDALONE).
  6. On reject: emit empty-G `provenance.derivation` on the motifs
     snapshot doc and stop.

Caste: producer (grants identity to new substrate docs). Operator-
triggered, not predicate-fired. The operational phase (extract /
patch dispatch) is separate and consumes the motif via downstream
agents.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import ClassVar, List, Optional, Tuple

import yaml

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.backend.emit import (
    emit_attribute_link, emit_citation, emit_classifier, emit_derivation,
    emit_empty_derivation,
)
from lib.lattice.labels import format_label, note_dep_asn_ids
from lib.predicates import latest_doc_head, statements_sidecar_of
from lib.predicates.versions import version_head
from lib.protocols.febe.protocol import Session
from lib.shared.common import find_asn, read_file
from lib.shared.invoke_claude import invoke_claude
from lib.shared.paths import (
    LATTICE, MOTIF_DIR, MOTIFS_DIR, WORKSPACE, prompt_path,
)


MOTIF_MODEL = "opus"
MOTIF_EFFORT = "high"

SCOUT_PROMPT = prompt_path("agents/scouts/cross_note_bridge.md")
SELECT_PROMPT = prompt_path("agents/producers/motif_select.md")
ATTRIBUTION_PROMPT = prompt_path("agents/producers/motif_attribution.md")


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


# ─── Path helpers ──────────────────────────────────────────────────


def _next_sequence_number(directory: Path, stem_prefix: str) -> int:
    """Return next sequential number for `<stem_prefix>-NNNN.md` files
    in `directory`. Matches the `audit-N`/`review-N`/`motif-NNNN`
    convention.
    """
    if not directory.exists():
        return 1
    nums = []
    pat = re.compile(rf"{re.escape(stem_prefix)}-(\d+)\.md$")
    for p in directory.glob(f"{stem_prefix}-*.md"):
        m = pat.match(p.name)
        if m:
            nums.append(int(m.group(1)))
    return max(nums, default=0) + 1


def _motifs_snapshot_path(num: int) -> Path:
    return MOTIFS_DIR / f"motifs-{num:04d}.md"


def _motif_doc_path(num: int) -> Path:
    return MOTIF_DIR / f"motif-{num:04d}.md"


def _attribution_sidecar_path(motif_path: Path) -> Path:
    """`<motif-stem>.motif.attribution.md` — two-dot suffix is awkward
    but follows the existing `<stem>.<kind>.md` sidecar convention."""
    return motif_path.with_name(f"{motif_path.stem}.motif.attribution.md")


# ─── Note loading + formatting ─────────────────────────────────────


def _load_input_notes(asn_nums: List[int]) -> List[Tuple[int, str, str]]:
    """Return [(asn_num, label, body), ...] for input notes."""
    out = []
    for n in asn_nums:
        path, label = find_asn(str(n))
        if path is None:
            continue
        out.append((n, label, path.read_text()))
    return out


def _format_notes_block(notes) -> str:
    """Concat input note bodies with separator headers."""
    parts = [f"### {label}\n\n{body}\n" for _, label, body in notes]
    return "\n---\n\n".join(parts)


def _all_transitive_deps(session: Session, asn_nums: List[int]) -> List[int]:
    """BFS over note-level citation.depends from the given ASNs."""
    visited = set()
    queue = list(asn_nums)
    while queue:
        n = queue.pop()
        if n in visited:
            continue
        visited.add(n)
        path, _ = find_asn(str(n))
        if path is None:
            continue
        rel = str(path.resolve().relative_to(Path(WORKSPACE).resolve()))
        addr = session.store.path_to_addr.get(rel)
        if addr is None:
            continue
        deps = note_dep_asn_ids(session.store, addr)
        queue.extend(d for d in deps if d not in visited)
    return sorted(visited - set(asn_nums))


def _format_candidate_notes(asn_nums: List[int]) -> str:
    """Format candidate notes (cited + transitive deps) as full bodies."""
    if not asn_nums:
        return "(none)"
    parts = []
    for n in asn_nums:
        path, label = find_asn(str(n))
        if path is None:
            parts.append(f"## {format_label(n)} — (note not found)\n")
            continue
        parts.append(f"## {label}\n\n{path.read_text().rstrip()}\n")
    return "\n\n---\n\n".join(parts)


# ─── Agent ─────────────────────────────────────────────────────────


class MotifAgent(Agent):
    """One fire = scout → select → attribute → emit substrate.

    Operator-gated CLI producer. Internal phases (scout, select,
    attribute) are LLM calls; the agent emits the resulting substrate
    citizens (motifs snapshot, motif doc, attribution sidecar) plus
    their linking edges.
    """

    role: ClassVar[str] = "motif"

    def __init__(
        self, *,
        model: str = MOTIF_MODEL,
        effort: str = MOTIF_EFFORT,
    ):
        self.model = model
        self.effort = effort

    def run(
        self, session: Session, addr: Optional[Address] = None,
        *, input_asns: List[int],
    ) -> AgentResult:
        del addr  # not used; this is an operator-gated producer

        if len(input_asns) < 2:
            return AgentResult(
                success=False,
                detail=f"need >=2 input ASNs, got {len(input_asns)}",
            )

        notes = _load_input_notes(input_asns)
        if len(notes) < 2:
            return AgentResult(
                success=False,
                detail="fewer than 2 input notes found in lattice",
            )
        notes_block = _format_notes_block(notes)

        # 1. Scout
        scout_text = self._call(
            "scout", SCOUT_PROMPT,
            {"{{notes_block}}": notes_block},
        )
        if scout_text is None:
            return AgentResult(success=False, detail="scout-llm-failed")
        scout_data = _parse_yaml(scout_text)
        if not isinstance(scout_data, dict) or "motifs" not in scout_data:
            return AgentResult(
                success=False, detail="scout-yaml-malformed",
            )

        # 2. Materialize motifs snapshot
        motifs_addr = self._emit_motifs_snapshot(
            session, scout_text, input_asns,
        )

        # 3. Selector
        sel_text = self._call(
            "select", SELECT_PROMPT,
            {
                "{{scout_report}}": scout_text,
                "{{notes_block}}": notes_block,
            },
        )
        if sel_text is None:
            return AgentResult(success=False, detail="select-llm-failed")
        sel_data = _parse_yaml(sel_text) or {}
        if sel_data.get("decision") != "SELECTED":
            emit_empty_derivation(session.store, motifs_addr)
            return AgentResult(
                success=True,
                detail=f"all-rejected: {sel_data.get('rationale', '')[:120]}",
            )

        motif_id = sel_data.get("motif_id")
        chosen = next(
            (m for m in scout_data["motifs"] if m.get("id") == motif_id),
            None,
        )
        if chosen is None:
            return AgentResult(
                success=False,
                detail=f"selector picked id={motif_id!r} not in scout output",
            )

        # 4. Materialize motif doc + cited-claim anchors + derivation
        motif_addr = self._emit_motif_doc(session, chosen, motifs_addr)

        # 5. Attribution
        attrib_text = self._call(
            "attribution", ATTRIBUTION_PROMPT,
            self._attribution_slots(session, chosen),
        )
        if attrib_text is None:
            return AgentResult(success=False, detail="attribution-llm-failed")
        attrib_data = _parse_yaml(attrib_text) or {}

        # 6. Materialize attribution sidecar
        self._emit_attribution_sidecar(
            session, motif_addr, attrib_data, attrib_text,
        )

        base = attrib_data.get("base") or "(unset)"
        return AgentResult(
            success=True,
            detail=f"motif emitted; base={base}",
        )

    # ── LLM helpers ────────────────────────────────────────────────

    def _call(self, label: str, prompt_path_obj, slots) -> Optional[str]:
        template = read_file(prompt_path_obj)
        if not template:
            return None
        prompt = template
        for placeholder, value in slots.items():
            prompt = prompt.replace(placeholder, value)
        result = invoke_claude(
            prompt, model=self.model, effort=self.effort,
            tools="", output_format=None,
        )
        if not result.text:
            return None
        return result.text

    def _attribution_slots(self, session: Session, chosen: dict) -> dict:
        """Build the attribution prompt's slot fillings from the chosen
        motif's cited_claims + transitive deps."""
        cited_nums = sorted({
            int(re.search(r"(\d+)", k).group(1))
            for k in (chosen.get("cited_claims") or {})
            if re.search(r"(\d+)", k)
        })
        dep_nums = _all_transitive_deps(session, cited_nums)
        candidate_nums = sorted(set(cited_nums) | set(dep_nums))
        finding_lines = [f"### Motif — {chosen.get('name', '')}"]
        for asn_label, claims in (chosen.get("cited_claims") or {}).items():
            cl = ", ".join(str(c) for c in claims) if isinstance(claims, list) else claims
            finding_lines.append(f"- **{asn_label}**: {cl}")
        if chosen.get("rationale"):
            finding_lines.extend(["", chosen["rationale"].rstrip()])
        return {
            "{{motif_finding}}": "\n".join(finding_lines),
            "{{candidate_notes}}": _format_candidate_notes(candidate_nums),
        }

    # ── Substrate emissions ────────────────────────────────────────

    def _emit_motifs_snapshot(
        self, session: Session, scout_text: str,
        input_asns: List[int],
    ) -> Address:
        """Materialize the scout's snapshot doc with `motifs` classifier."""
        del input_asns  # captured in provenance.derivation upstream
        MOTIFS_DIR.mkdir(parents=True, exist_ok=True)
        num = _next_sequence_number(MOTIFS_DIR, "motifs")
        path = _motifs_snapshot_path(num)
        path.write_text(_strip_code_fence(scout_text).rstrip() + "\n")
        rel = str(path.relative_to(WORKSPACE))
        addr = session.store.register_path(rel)
        emit_classifier(session.store, addr, "motifs")
        return addr

    def _emit_motif_doc(
        self, session: Session, chosen: dict, motifs_addr: Address,
    ) -> Address:
        """Materialize the motif doc + cited-claim citation anchors +
        provenance.derivation back to the motifs snapshot."""
        MOTIF_DIR.mkdir(parents=True, exist_ok=True)
        num = _next_sequence_number(MOTIF_DIR, "motif")
        path = _motif_doc_path(num)

        # Body: motif frontmatter + rationale prose.
        # Build via yaml.safe_dump to handle quoting + special chars.
        fm = {
            "name": chosen.get("name", ""),
            "cited_claims": dict(chosen.get("cited_claims") or {}),
        }
        fm_yaml = yaml.safe_dump(
            fm, default_flow_style=False, sort_keys=False, allow_unicode=True,
        )
        rationale = (chosen.get("rationale") or "").rstrip()
        body = (
            f"---\n{fm_yaml}---\n\n"
            f"# Motif — {chosen.get('name', '')}\n\n"
            f"{rationale}\n"
        )
        path.write_text(body)

        rel = str(path.relative_to(WORKSPACE))
        motif_addr = session.store.register_path(rel)

        emit_classifier(session.store, motif_addr, "motif")
        emit_derivation(session.store, motifs_addr, motif_addr)

        # One citation.depends per cited note, pointing at the note's
        # statements sidecar's supersession head. The chain head is the
        # claims.statements aggregate when the note's been through claim
        # derivation, otherwise the operator-drafted statements sidecar.
        for asn_label in (chosen.get("cited_claims") or {}):
            head = self._resolve_statements_head(session, asn_label)
            if head is not None:
                emit_citation(
                    session.store, motif_addr, head, direction="depends",
                )

        return motif_addr

    def _emit_attribution_sidecar(
        self, session: Session, motif_addr: Address,
        attrib_data: dict, attrib_text: str,
    ) -> Address:
        """Materialize the attribution sidecar with the two citation
        anchors (freshness against motif, structural against base)."""
        motif_path = WORKSPACE / session.get_path_for_addr(motif_addr)
        sidecar_path = _attribution_sidecar_path(motif_path)

        rationale = attrib_data.get("rationale") or ""
        body = (
            f"# Attribution\n\n"
            f"**Base:** {attrib_data.get('base', '(unset)')}\n\n"
            f"{rationale.rstrip()}\n"
        )
        sidecar_path.write_text(body)
        rel = str(sidecar_path.relative_to(WORKSPACE))
        sidecar_addr = session.store.register_path(rel)

        emit_attribute_link(
            session.store, motif_addr, "motif.attribution", sidecar_addr,
        )

        # Freshness anchor: sidecar → motif head
        emit_citation(
            session.store, sidecar_addr,
            version_head(session, motif_addr),
            direction="depends",
        )

        # Structural fact: sidecar → base note's statements head, omitted
        # for STANDALONE. Same `note → statements → supersession_head`
        # resolution the motif uses for its cited-claim anchors.
        base_label = (attrib_data.get("base") or "").strip()
        if base_label and base_label != "STANDALONE":
            head = self._resolve_statements_head(session, base_label)
            if head is not None:
                emit_citation(
                    session.store, sidecar_addr, head, direction="depends",
                )

        return sidecar_addr

    # ── Address resolution ─────────────────────────────────────────

    def _resolve_asn(
        self, session: Session, asn_label: str,
    ) -> Optional[Address]:
        """Resolve `ASN-NNNN` to its note's substrate address."""
        m = re.search(r"(\d+)", asn_label)
        if not m:
            return None
        path, _ = find_asn(m.group(1))
        if path is None:
            return None
        rel = str(path.resolve().relative_to(Path(WORKSPACE).resolve()))
        return session.store.path_to_addr.get(rel)

    def _resolve_statements_head(
        self, session: Session, asn_label: str,
    ) -> Optional[Address]:
        """Resolve `ASN-NNNN` to the latest doc-level head of its note's
        statements sidecar.

        Walks `note → statements → latest_doc_head`. The result is the
        `claims.statements` aggregate when the note's been through
        claim derivation, otherwise the operator-drafted statements
        sidecar — both are path-bearing identity addresses. Version
        markers in the supersession chain are normalized via
        `version_root` so the citation target always resolves to a
        readable doc.
        """
        note_addr = self._resolve_asn(session, asn_label)
        if note_addr is None:
            return None
        sidecar = statements_sidecar_of(session, note_addr)
        if sidecar is None:
            return None
        return latest_doc_head(session, sidecar)
