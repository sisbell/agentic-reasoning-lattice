"""Claim citation-resolve producer — per-claim references sidecars +
typed citation links.

Fires per-claim with a stale (or absent) references sidecar. One fire =
read the claim's prose, dispatch the LLM to type each label reference
(depends vs forward), apply changes to the claim md (insert/remove
bullets in *Depends:* / *Forward References:* sections), emit
substrate links (citation.depends/forward, retraction,
citation.resolve, provenance.derivation), attest the references
sidecar via attest_against_doc_head (chain advance + freshness-
anchor citation from sidecar head to claim head, which is what
references_is_fresh reads), persist the resolve-doc audit trail,
commit.

Caste: producer. Identity grant: references sidecar (created or
chain-advanced via attest_against_doc_head), plus per-fire
citation.depends/forward and retraction links.
"""

from __future__ import annotations

import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import ClassVar, List, NamedTuple

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.backend.emit import emit_citation, emit_retraction
from lib.lattice.attributes import attest_against_doc_head
from lib.lattice.labels import build_cross_asn_label_index
from lib.protocols.febe.protocol import Session
from lib.shared.common import read_file
from lib.shared.git_ops import step_commit_asn
from lib.shared.llm_response import invoke_text, parse_two_sections
from lib.shared.paths import CITATION_RESOLVE_DIR, LATTICE, prompt_path


CITATION_MODEL = "sonnet"
DEPENDS_HEADER = "- *Depends:*"
FORWARD_HEADER = "- *Forward References:*"
PROMPT_TEMPLATE = prompt_path("agents/producers/citation_resolve.md")


# ─── LLM helper ─────────────────────────────────────────────────────


class CitationClassifications(NamedTuple):
    classifications: list  # [{label, direction: depends|forward, bullet}, ...]
    retractions: list      # [{label, direction: depends|forward}, ...]
    raw_text: str
    elapsed_seconds: float


def extract_citation_classifications(
    claim_md_content: str,
    claim_dir: Path,
    claims_root: Path,
    existing_depends: List[str],
    existing_forwards: List[str],
    *,
    model: str = "sonnet",
) -> CitationClassifications:
    """Run Sonnet against the citation-resolve prompt; return parsed
    CLASSIFICATIONS / RETRACTIONS.

    Raises on malformed LLM output (missing headers, YAML parse errors,
    malformed entries, invalid direction values) — no graceful
    degradation.
    """
    prompt = _render_prompt(
        claim_md_content, claim_dir, claims_root,
        existing_depends, existing_forwards,
    )
    raw_text, elapsed = invoke_text(prompt, model=model, tools="Read")
    classifications, retractions = parse_two_sections(
        raw_text, "CLASSIFICATIONS", "RETRACTIONS",
    )
    _validate_classifications(classifications)
    _validate_retractions(retractions)
    return CitationClassifications(
        classifications=classifications,
        retractions=retractions,
        raw_text=raw_text,
        elapsed_seconds=elapsed,
    )


def _format_label_list(labels: List[str]) -> str:
    if not labels:
        return "(none)"
    return "\n".join(f"- {label}" for label in labels)


def _render_prompt(
    claim_md_content: str,
    claim_dir: Path,
    claims_root: Path,
    depends: List[str],
    forwards: List[str],
) -> str:
    template = read_file(PROMPT_TEMPLATE)
    return (
        template
        .replace("{{claim_md_content}}", claim_md_content)
        .replace("{{claim_dir}}", str(claim_dir))
        .replace("{{claims_root}}", str(claims_root))
        .replace("{{existing_depends}}", _format_label_list(depends))
        .replace("{{existing_forwards}}", _format_label_list(forwards))
    )


def _validate_classifications(classifications: list) -> None:
    for c in classifications:
        if not isinstance(c, dict):
            raise ValueError(f"classification entry not a dict: {c}")
        for field in ("label", "direction", "bullet"):
            if field not in c:
                raise ValueError(f"classification missing {field!r}: {c}")
        if c["direction"] not in ("depends", "forward"):
            raise ValueError(f"invalid direction in classification: {c}")


def _validate_retractions(retractions: list) -> None:
    for r in retractions:
        if not isinstance(r, dict):
            raise ValueError(f"retraction entry not a dict: {r}")
        for field in ("label", "direction"):
            if field not in r:
                raise ValueError(f"retraction missing {field!r}: {r}")
        if r["direction"] not in ("depends", "forward"):
            raise ValueError(f"invalid direction in retraction: {r}")


# ─── Substrate queries ──────────────────────────────────────────────


def _existing_classifications(
    session: Session, claim_md_rel: str, label_index: dict,
):
    """Return (depends_labels, forwards_labels) sourced from substrate."""
    from lib.predicates.versions import version_head

    rev_index = {addr: label for label, addr in label_index.items()}
    claim_addr = session.get_addr_for_path(claim_md_rel)
    if claim_addr is None:
        return [], []
    state = session.state

    def _base(addr):
        cur = addr
        while state.parent.get(cur) is not None:
            cur = state.parent[cur]
        return cur

    # Walk from claim's head; resolve each cited target to base for
    # rev_index lookup.
    claim_head = version_head(session, claim_addr)
    depends = []
    forwards = []
    for link in session.active_links(
        "citation.depends", from_set=[claim_head],
    ):
        for cited in link.to_set:
            base = _base(cited)
            if base in rev_index:
                depends.append(rev_index[base])
    for link in session.active_links(
        "citation.forward", from_set=[claim_head],
    ):
        for cited in link.to_set:
            base = _base(cited)
            if base in rev_index:
                forwards.append(rev_index[base])
    return sorted(depends), sorted(forwards)


def _validate_labels(classifications, retractions, label_index):
    """Every emitted label must resolve in the cross-ASN label index."""
    for c in classifications:
        if c["label"] not in label_index:
            raise ValueError(f"unknown label in classification: {c['label']!r}")
    for r in retractions:
        if r["label"] not in label_index:
            raise ValueError(f"unknown label in retraction: {r['label']!r}")


# ─── Claim md section editing ───────────────────────────────────────


def _find_section(lines, header):
    """Locate a `- *<Field>:*` section.

    Returns (start_idx, last_bullet_idx). Returns None if not present.
    """
    for i, line in enumerate(lines):
        if line.strip() == header.strip():
            last_bullet_idx = i
            for j in range(i + 1, len(lines)):
                ln = lines[j]
                if ln.startswith("  - "):
                    last_bullet_idx = j
                elif ln.startswith("    ") or ln.strip() == "":
                    continue
                else:
                    break
            return (i, last_bullet_idx)
    return None


def _bullet_label(bullet_line):
    return bullet_line[4:].split(None, 1)[0]


def _existing_section_labels(lines, header):
    section = _find_section(lines, header)
    if section is None:
        return set()
    start_idx, last_bullet_idx = section
    labels = set()
    for j in range(start_idx + 1, last_bullet_idx + 1):
        line = lines[j]
        if line.startswith("  - "):
            labels.add(_bullet_label(line))
    return labels


def _apply_changes(claim_md_path, classifications, retractions):
    """Apply classifications (insert bullets) and retractions (remove
    bullets). Retractions first (so a reclassify works: retract old
    direction, insert new). Bullet inserts dedup against labels
    already in the target section.
    """
    lines = claim_md_path.read_text().split("\n")

    for r in retractions:
        header = (
            DEPENDS_HEADER if r["direction"] == "depends" else FORWARD_HEADER
        )
        section = _find_section(lines, header)
        if section is None:
            raise ValueError(
                f"retraction target section {header!r} not in {claim_md_path}"
            )
        start_idx, last_bullet_idx = section
        removed = False
        for j in range(start_idx + 1, last_bullet_idx + 1):
            line = lines[j]
            if line.startswith("  - ") and _bullet_label(line) == r["label"]:
                del lines[j]
                removed = True
                break
        if not removed:
            raise ValueError(
                f"no bullet for {r['label']!r} in {header!r} of {claim_md_path}"
            )

    depends_to_add = [
        c for c in classifications if c["direction"] == "depends"
    ]
    forwards_to_add = [
        c for c in classifications if c["direction"] == "forward"
    ]

    if depends_to_add:
        section = _find_section(lines, DEPENDS_HEADER)
        if section is None:
            raise ValueError(
                f"no {DEPENDS_HEADER!r} section in {claim_md_path}; "
                f"cannot add depends bullets"
            )
        existing = _existing_section_labels(lines, DEPENDS_HEADER)
        depends_to_add = [
            c for c in depends_to_add if c["label"] not in existing
        ]
        if depends_to_add:
            _, last_bullet_idx = _find_section(lines, DEPENDS_HEADER)
            for c in reversed(depends_to_add):
                lines.insert(last_bullet_idx + 1, "  " + c["bullet"].lstrip())

    if forwards_to_add:
        existing = _existing_section_labels(lines, FORWARD_HEADER)
        forwards_to_add = [
            c for c in forwards_to_add if c["label"] not in existing
        ]
        if forwards_to_add:
            section = _find_section(lines, FORWARD_HEADER)
            if section is None:
                depends_section = _find_section(lines, DEPENDS_HEADER)
                if depends_section is None:
                    raise ValueError(
                        f"cannot create {FORWARD_HEADER!r}: no "
                        f"{DEPENDS_HEADER!r} to anchor it after in "
                        f"{claim_md_path}"
                    )
                _, depends_last = depends_section
                new_block = [FORWARD_HEADER]
                for c in forwards_to_add:
                    new_block.append("  " + c["bullet"].lstrip())
                for ln in reversed(new_block):
                    lines.insert(depends_last + 1, ln)
            else:
                _, last_bullet_idx = section
                for c in reversed(forwards_to_add):
                    lines.insert(
                        last_bullet_idx + 1, "  " + c["bullet"].lstrip()
                    )

    claim_md_path.write_text("\n".join(lines))


# ─── Resolve-doc persistence (audit trail) ──────────────────────────


def _next_run_num(asn_label, claim_label):
    asn_dir = CITATION_RESOLVE_DIR / asn_label
    if not asn_dir.exists():
        return 1
    pat = re.compile(rf"^{re.escape(claim_label)}-(\d+)\.md$")
    nums = []
    for p in asn_dir.iterdir():
        m = pat.match(p.name)
        if m:
            nums.append(int(m.group(1)))
    return (max(nums) if nums else 0) + 1


def _persist_resolve_doc(asn_label, claim_label, sonnet_output, model):
    """Write the resolve doc with a small header + raw Sonnet output."""
    run_num = _next_run_num(asn_label, claim_label)
    asn_dir = CITATION_RESOLVE_DIR / asn_label
    asn_dir.mkdir(parents=True, exist_ok=True)
    path = asn_dir / f"{claim_label}-{run_num}.md"
    timestamp = (
        datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z")
    )
    content = (
        f"# Citation Resolve — {asn_label}/{claim_label} — run {run_num}\n"
        f"\n"
        f"*{timestamp}*\n"
        f"*Model: {model}*\n"
        f"\n"
        f"## Output\n"
        f"\n"
        f"{sonnet_output.strip()}\n"
    )
    path.write_text(content)
    return path, run_num


# ─── Substrate emission ─────────────────────────────────────────────


def _walk_to_base(state, addr: Address) -> Address:
    """Walk version-parent chain to the base identity (root)."""
    cur = addr
    while state.parent.get(cur) is not None:
        cur = state.parent[cur]
    return cur


def _emit_citation_substrate(
    session: Session,
    claim_md_rel: str,
    classifications: list,
    retractions: list,
    resolve_doc_rel: str,
    label_index: dict,
):
    """Emit substrate links for one resolve operation.

    Order:
    1. citation.resolve classifier on the resolve doc
    2. citation.depends / citation.forward for each classification
    3. retraction for each retraction
    4. provenance.derivation from the resolve doc to each emitted link
    """
    from lib.predicates.versions import version_head

    store = session.store
    resolve_doc_addr = store.register_path(resolve_doc_rel)
    claim_addr = store.register_path(claim_md_rel)
    claim_head = version_head(session, claim_addr)

    store.make_link(
        homedoc=resolve_doc_addr,
        from_set=[],
        to_set=[resolve_doc_addr],
        type_="citation.resolve",
    )

    derivation_targets = []
    for c in classifications:
        cited_addr = label_index.get(c["label"])
        if cited_addr is None:
            continue
        cited_head = version_head(session, cited_addr)
        link, _ = emit_citation(
            store, claim_head, cited_head, direction=c["direction"],
        )
        derivation_targets.append(link.addr)
    for r in retractions:
        cited_addr = label_index.get(r["label"])
        if cited_addr is None:
            continue
        type_str = f"citation.{r['direction']}"
        # Citations may target version-head addresses (not identity);
        # walk each candidate's to_set back to base before matching.
        for cand in session.active_links(
            type_str, from_set=[claim_head],
        ):
            if not any(
                _walk_to_base(store.state, t) == cited_addr
                for t in cand.to_set
            ):
                continue
            retraction = emit_retraction(store, claim_head, cand.addr)
            derivation_targets.append(retraction.addr)
            break  # retract one matching link per (claim, target, direction)

    for target_addr in derivation_targets:
        store.make_link(
            homedoc=resolve_doc_addr,
            from_set=[resolve_doc_addr],
            to_set=[target_addr],
            type_="provenance.derivation",
        )


# ─── References sidecar rendering ───────────────────────────────────


def _render_references_sidecar(
    session: Session, claim_md_rel: str, label_index: dict,
) -> str:
    """Render the post-fire references sidecar from current substrate.

    Reads active citation.depends + citation.forward from the claim and
    emits a labels-only markdown view. The sidecar is the LLM's
    authoritative classification — labels only, no explanatory prose
    (those live in the claim md's bullet sections). Empty sections
    omitted.
    """
    depends, forwards = _existing_classifications(
        session, claim_md_rel, label_index,
    )
    parts = []
    if depends:
        parts.append("*Depends:*")
        for label in depends:
            parts.append(f"  - {label}")
    if forwards:
        if parts:
            parts.append("")
        parts.append("*Forward References:*")
        for label in forwards:
            parts.append(f"  - {label}")
    return "\n".join(parts) + "\n" if parts else ""


# ─── Agent class ────────────────────────────────────────────────────


class ClaimCitationResolveAgent(Agent):
    """One claim's citation-classification per fire.

    Reads the claim md, dispatches the LLM to type each label
    reference, applies the resulting changes to the claim md
    (insert/remove bullets in *Depends:* / *Forward References:*),
    emits substrate links, attests the references sidecar via
    attest_against_doc_head, persists the resolve-doc audit trail,
    commits.
    """

    role: ClassVar[str] = "claim-citation-resolve"

    def __init__(self, *, model: str = CITATION_MODEL):
        self.model = model

    def run(self, session: Session, claim_addr: Address) -> AgentResult:
        claim_rel = session.get_path_for_addr(claim_addr)
        if claim_rel is None:
            return AgentResult(success=False, detail="no-claim-path")

        m = re.search(r"(ASN-(\d{4}))/([^/]+)\.md$", claim_rel)
        if m is None:
            return AgentResult(success=False, detail="unparseable-claim-path")
        asn_label = m.group(1)
        asn_num = int(m.group(2))
        claim_label = m.group(3)

        os.environ.setdefault("PROTOCOL_ASN_LABEL", asn_label)

        claim_md_full = LATTICE / claim_rel
        if not claim_md_full.exists():
            return AgentResult(success=False, detail="no-claim-file")

        claim_md_content = claim_md_full.read_text()

        label_index = build_cross_asn_label_index(session.store)
        depends, forwards = _existing_classifications(
            session, claim_rel, label_index,
        )

        claim_dir = claim_md_full.parent
        claims_root = claim_dir.parent

        print(
            f"  [CITATION-RESOLVE] {asn_label}/{claim_label} ({self.model})...",
            end="", file=sys.stderr, flush=True,
        )
        result = extract_citation_classifications(
            claim_md_content, claim_dir, claims_root, depends, forwards,
            model=self.model,
        )
        print(f" ({result.elapsed_seconds:.0f}s)", file=sys.stderr)

        # Apply delta (claim md edits + substrate emissions). On no-op
        # delta these are skipped, but the attestation and audit trail
        # below still fire.
        if result.classifications or result.retractions:
            _validate_labels(
                result.classifications, result.retractions, label_index,
            )
            _apply_changes(
                claim_md_full, result.classifications, result.retractions,
            )

        # Persist the resolve doc as audit trail (never discard LLM
        # output). Same on no-op as on changes.
        resolve_path, run_num = _persist_resolve_doc(
            asn_label, claim_label, result.raw_text, self.model,
        )
        resolve_rel = str(resolve_path.relative_to(LATTICE))

        if result.classifications or result.retractions:
            _emit_citation_substrate(
                session, claim_rel,
                result.classifications, result.retractions,
                resolve_rel, label_index,
            )

        # attest_against_doc_head emits the freshness anchor citation
        # (sidecar's head → claim's head) alongside the attestation.
        # content_changed reflects the LLM verdict: empty
        # classifications AND empty retractions means the references
        # sidecar's content is unchanged this fire (re-anchor only,
        # no chain advance). Any non-empty list means real edit.
        sidecar_text = _render_references_sidecar(
            session, claim_rel, label_index,
        )
        content_changed = (
            bool(result.classifications) or bool(result.retractions)
        )
        attest_against_doc_head(
            session, claim_rel, "references", sidecar_text.rstrip(),
            claim_addr,
            content_changed=content_changed,
        )

        n_class = len(result.classifications)
        n_retr = len(result.retractions)
        if n_class == 0 and n_retr == 0:
            summary = "re-attested, no changes"
        else:
            summary = f"{n_class} classifications, {n_retr} retractions"
        print(
            f"  [CITATION-RESOLVE] {claim_label}: {summary}, run {run_num}",
            file=sys.stderr,
        )

        step_commit_asn(
            asn_num,
            hint=(
                f"citation-resolve(asn): {asn_label}/{claim_label} — "
                f"{summary}"
            ),
        )

        return AgentResult(
            success=True,
            detail=f"classifications={n_class} retractions={n_retr}",
        )
