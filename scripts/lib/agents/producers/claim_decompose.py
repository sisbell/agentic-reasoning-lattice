"""Claim-decompose agent — first-pass derivation of a note into claims.

`ClaimDecomposeAgent` is the operator-gated entry point to the
claim-derivation arc. One fire = mechanically split the source note
at `## ` headers, run the decompose prompt in parallel on each
non-structural section, then for every extracted claim:

  - resolve the LLM-proposed body against the source note (byte-
    substring invariant — no fuzzy matching)
  - write the claim md file under `_docuverse/documents/claim/<asn>/`
  - emit substrate identity facts: `claim` classifier, `label` and
    `name` sidecars, `provenance.derivation` from source note
  - (after all claims) emit `transclusion.claim-statements` and
    supersede the note's statements sidecar (if any)

The per-section workspace yamls remain (annotate consumes them)
until annotate is also lifted to substrate-direct.

Caste: producer. Operator-gated trigger (not predicate-fired). The
agent grants new substrate identity to each claim doc — that's the
producer caste's defining role. Operator gating is independent of
caste; producers can be either runner-fired or manually invoked.
"""

from __future__ import annotations

import re
import sys
import time
from typing import ClassVar

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.backend.emit import (
    emit_claim, emit_derivation, emit_supersession, emit_transclusion,
)
from lib.lattice.attributes import attest_attribute
from lib.protocols.febe.protocol import Session
from lib.shared.git_ops import step_commit_asn
from lib.shared.invoke_claude import parallel_llm_calls
from lib.shared.paths import CLAIM_DIR, WORKSPACE, transclusion_path


# Sections that are structural — no LLM analysis needed.
SKIP_HEADERS = {
    "PREAMBLE",
    "Claims Introduced",
    "Open Questions",
    "Worked example",
}


def _is_structural(header: str) -> bool:
    return header in SKIP_HEADERS


def split_sections(text: str) -> list[tuple[str, str]]:
    """Mechanical split on `## ` headers. Returns [(header, content), ...]."""
    sections: list[tuple[str, str]] = []
    current_header = "PREAMBLE"
    current_lines: list[str] = []

    for line in text.split("\n"):
        if line.startswith("## "):
            sections.append((current_header, "\n".join(current_lines)))
            current_header = line.lstrip("#").strip()
            current_lines = [line]
        else:
            current_lines.append(line)

    sections.append((current_header, "\n".join(current_lines)))
    return sections


def _slugify(header: str) -> str:
    slug = header.lower().replace(" ", "-").replace("/", "-")
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


_WHITESPACE_RE = re.compile(r"\s+")


def find_in_source(source_note_text: str, llm_body_text: str) -> str | None:
    """Locate `llm_body_text` in `source_note_text` and return the
    matched source-bytes substring, or None on failure.

    The decompose-phase LLM returns a `body:` field that's its best
    attempt at copying a region of the source note verbatim. LLMs
    drift slightly in practice; this function treats the LLM body as
    a probe and returns the source's actual bytes so the caller
    writes a verbatim substring of the source note. Strict by design
    — no fuzzy matching, since fuzzy is silent acceptance of
    unexplained drift.

    Match strategy is two-stage:
    1. Exact byte-substring match.
    2. Whitespace-normalized match — collapse runs of whitespace to
       single spaces in both source and probe, locate, then map back
       to the source's original bytes.
    """
    if not source_note_text or not llm_body_text:
        return None

    if llm_body_text in source_note_text:
        return llm_body_text

    normalized_probe = _WHITESPACE_RE.sub(" ", llm_body_text).strip()
    if not normalized_probe:
        return None

    norm_source, norm_to_src = _normalize_with_offset_map(source_note_text)

    start_norm = norm_source.find(normalized_probe)
    if start_norm == -1:
        return None

    end_norm = start_norm + len(normalized_probe)
    src_start = norm_to_src[start_norm]
    src_end_inclusive = norm_to_src[end_norm - 1]
    src_end = src_end_inclusive + 1
    while (src_end < len(source_note_text)
           and source_note_text[src_end].isspace()
           and end_norm < len(norm_source)
           and norm_source[end_norm] == " "):
        src_end += 1

    return source_note_text[src_start:src_end]


def _normalize_with_offset_map(text: str) -> Tuple[str, List[int]]:
    """Collapse whitespace runs to single spaces; return (normalized,
    offset_map) where offset_map[i] is the source byte offset for
    position i in the normalized text. Leading/trailing whitespace
    preserved positionally.
    """
    out_chars = []
    offset_map = []
    in_ws_run = False
    for i, ch in enumerate(text):
        if ch.isspace():
            if in_ws_run:
                continue
            out_chars.append(" ")
            offset_map.append(i)
            in_ws_run = True
        else:
            out_chars.append(ch)
            offset_map.append(i)
            in_ws_run = False
    return "".join(out_chars), offset_map


def clean_label(raw_label: str) -> Tuple[str, bool]:
    """Strip trailing dots and replace spaces with dashes. Return the
    cleaned label and a bool indicating whether anything changed."""
    cleaned = raw_label.rstrip(".").replace(" ", "-")
    return cleaned, cleaned != raw_label


# ─── Body resolution + label cleaning helpers ─────────────────────


def analyze_section(section_content: str) -> str | None:
    """Call the decompose LLM on one section. Returns YAML text, or None
    if the LLM failed or found no claims."""
    from lib.shared.invoke_claude import invoke_claude, strip_code_fence
    from lib.shared.paths import prompt_path

    prompt_template = prompt_path("agents/producers/claim_decompose.md").read_text()
    prompt = prompt_template.replace("{{section_content}}", section_content)

    response = invoke_claude(prompt, model="sonnet", effort="high")
    if not response.text:
        return None

    text = strip_code_fence(response.text)
    if "- label:" not in text:
        return None
    return text


def _worker(item):
    idx, header, content = item
    slug = _slugify(header)
    label = f"{idx:02d}-{slug}"
    yaml_text = analyze_section(content)
    return label, yaml_text


class ClaimDecomposeAgent(Agent):
    """Operator-gated derivation entry point. One fire per source note.

    Mechanical-split + per-section LLM extraction, then for each claim
    found: resolve body against source note, write claim md, emit
    identity facts to substrate. After all claims, emit
    `transclusion.claim-statements` and supersede the note's
    statements sidecar (if any).

    Producer caste: grants new substrate identity to each claim doc.
    """

    role: ClassVar[str] = "claim-decompose"

    def run(self, session: Session, note_addr: Address) -> AgentResult:
        note_path_rel = session.get_path_for_addr(note_addr)
        if note_path_rel is None:
            return AgentResult(success=False, detail="no-note-path")

        asn_path = session.store.lattice_dir / note_path_rel
        if not asn_path.exists():
            return AgentResult(success=False, detail="no-note-file")

        m = re.search(r"(ASN-\d{4})", note_path_rel)
        if m is None:
            return AgentResult(success=False, detail="no-asn-label")
        asn_label = m.group(1)
        asn_number = int(asn_label[4:])

        asn_text = asn_path.read_text()

        print(f"\n  [DECOMPOSE] {asn_label}", file=sys.stderr)
        print(
            f"  Source: {asn_path.relative_to(WORKSPACE)}",
            file=sys.stderr,
        )

        sections = split_sections(asn_text)
        print(f"  {len(sections)} sections found", file=sys.stderr)

        items = []
        skipped = 0
        for i, (header, content) in enumerate(sections):
            slug = "preamble" if header == "PREAMBLE" else _slugify(header)
            filename = f"{i:02d}-{slug}"
            lines = len(content.strip().split("\n"))
            if _is_structural(header):
                print(
                    f"    {filename}  ({lines} lines) [structural, skip]",
                    file=sys.stderr,
                )
                skipped += 1
            else:
                print(
                    f"    {filename}  ({lines} lines)",
                    file=sys.stderr,
                )
                items.append((i, header, content.strip()))

        print(
            f"\n  Analyzing {len(items)} sections in parallel "
            f"({skipped} structural skipped)...",
            file=sys.stderr,
        )
        start = time.time()
        results = parallel_llm_calls(items, _worker, max_workers=5)
        elapsed = time.time() - start

        total_props = 0
        yaml_count = 0
        for _label, yaml_text in results:
            if yaml_text:
                total_props += yaml_text.count("- label:")
                yaml_count += 1

        print(
            f"\n  [DECOMPOSE] {len(sections)} sections, {yaml_count} with "
            f"claims, {total_props} total claims, {elapsed:.0f}s",
            file=sys.stderr,
        )

        # Per-claim: resolve body against source note + emit identity to
        # substrate. Claims come from the parallel-LLM results
        # (in-memory yaml strings); no disk round-trip through workspace.
        emitted, failed = self._emit_substrate(
            session, note_addr, asn_label, results, asn_text,
        )

        if failed:
            print(
                f"\n  [DECOMPOSE] {len(failed)} claim(s) failed body "
                f"resolution against source note:", file=sys.stderr,
            )
            for label, yaml_basename, snippet in failed:
                print(
                    f"    {label} (in {yaml_basename}): "
                    f"no exact / whitespace-normalized match. "
                    f"LLM body started: {snippet!r}", file=sys.stderr,
                )

        print(
            f"  [DECOMPOSE] emitted {emitted} claim(s) to substrate",
            file=sys.stderr,
        )

        step_commit_asn(asn_number, hint="decompose")
        return AgentResult(
            success=not failed,
            detail=(
                f"sections={len(sections)} yamls={yaml_count} "
                f"claims={total_props} emitted={emitted} failed={len(failed)}"
            ),
        )

    def _emit_substrate(
        self,
        session: Session,
        note_addr: Address,
        asn_label: str,
        results: list,
        source_note_text: str,
    ):
        """Resolve bodies + emit per-claim identity + ASN-level transclusion.

        `results` is the list of (section_label, yaml_text) tuples
        returned by the parallel LLM workers. Yaml strings are parsed
        in memory; no workspace round-trip.

        Returns (emitted_count, failed_list).
        """
        import yaml

        store = session.store
        lattice_root = store.lattice_dir.resolve()
        claims_dir = CLAIM_DIR / asn_label
        claims_dir.mkdir(parents=True, exist_ok=True)

        seen_labels: set[str] = set()
        failed: list[tuple[str, str, str]] = []
        emitted = 0

        for section_label, yaml_text in results:
            if not yaml_text:
                continue
            try:
                data = yaml.safe_load(yaml_text)
            except yaml.YAMLError as e:
                print(
                    f"    WARNING: yaml parse error for section "
                    f"{section_label!r}: {e}",
                    file=sys.stderr,
                )
                continue
            if not data:
                continue
            for prop in data.get("claims") or []:
                raw_label = prop.get("label", "")
                if not raw_label:
                    print(
                        f"    WARNING: claim without label in "
                        f"section {section_label!r}",
                        file=sys.stderr,
                    )
                    continue
                label, label_was_cleaned = clean_label(raw_label)
                if label_was_cleaned:
                    print(
                        f"    FIX label: {raw_label!r} → {label!r}",
                        file=sys.stderr,
                    )
                if label in seen_labels:
                    print(
                        f"    WARNING: duplicate label {label!r} "
                        f"(section {section_label!r})",
                        file=sys.stderr,
                    )
                    continue
                seen_labels.add(label)

                llm_body = (prop.get("body") or "").strip()
                resolved = find_in_source(source_note_text, llm_body)
                if resolved is None:
                    failed.append((label, section_label, llm_body[:120]))
                    continue

                body_md = claims_dir / f"{label}.md"
                body_md.write_text(resolved.rstrip() + "\n")

                body_rel = str(body_md.resolve().relative_to(lattice_root))
                body_addr = store.register_path(body_rel)
                emit_claim(store, body_addr)
                attest_attribute(session, body_md, "label", label)
                attest_attribute(
                    session, body_md, "name",
                    (prop.get("name") or label).strip(),
                )
                emit_derivation(store, note_addr, body_addr)

                emitted += 1

        # ASN-level transclusion view + supersession of statements sidecar.
        if emitted > 0:
            transclusion_rel = str(
                transclusion_path(asn_label, "claim-statements").resolve()
                .relative_to(lattice_root)
            )
            transclusion_addr = store.register_path(transclusion_rel)
            emit_transclusion(store, transclusion_addr, "claim-statements")
            emit_derivation(store, note_addr, transclusion_addr)

            for link in session.active_links("statements", from_set=[note_addr]):
                if link.to_set:
                    emit_supersession(store, link.to_set[0], transclusion_addr)
                    break

        return emitted, failed
