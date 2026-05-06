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
from pathlib import Path
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
from lib.shared.paths import (
    CLAIM_DERIVATION_DIR, CLAIM_DIR, WORKSPACE, transclusion_path,
)


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


def analyze_section(section_content: str) -> str | None:
    """Call the decompose LLM on one section. Returns YAML text, or None
    if the LLM failed or found no claims."""
    from lib.shared.invoke_claude import invoke_claude, strip_code_fence
    from lib.shared.paths import prompt_path

    prompt_template = prompt_path("claim-derivation/decompose.md").read_text()
    prompt = prompt_template.replace("{{section_content}}", section_content)

    response = invoke_claude(prompt, model="sonnet", effort="high")
    if not response.text:
        return None

    text = strip_code_fence(response.text)
    if "- label:" not in text:
        return None
    return text


def _make_worker(sections_dir: Path):
    def _worker(item):
        idx, header, content = item
        slug = _slugify(header)
        label = f"{idx:02d}-{slug}"
        yaml_text = analyze_section(content)
        if yaml_text:
            (sections_dir / f"{label}.yaml").write_text(yaml_text + "\n")
        return label, yaml_text

    return _worker


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

        sections_dir = CLAIM_DERIVATION_DIR / asn_label / "sections"
        sections_dir.mkdir(parents=True, exist_ok=True)
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
            (sections_dir / f"{filename}.md").write_text(
                content.strip() + "\n",
            )
            lines = len(content.strip().split("\n"))
            if _is_structural(header):
                print(
                    f"    {filename}.md  ({lines} lines) [structural, skip]",
                    file=sys.stderr,
                )
                skipped += 1
            else:
                print(
                    f"    {filename}.md  ({lines} lines)",
                    file=sys.stderr,
                )
                items.append((i, header, content.strip()))

        print(
            f"\n  Analyzing {len(items)} sections in parallel "
            f"({skipped} structural skipped)...",
            file=sys.stderr,
        )
        start = time.time()
        results = parallel_llm_calls(items, _make_worker(sections_dir),
                                     max_workers=5)
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
        # substrate.
        emitted, failed = self._emit_substrate(
            session, note_addr, asn_label, sections_dir, asn_text,
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
        sections_dir: Path,
        source_note_text: str,
    ):
        """Resolve bodies + emit per-claim identity + ASN-level transclusion.

        Returns (emitted_count, failed_list).
        """
        from .helpers import clean_label, find_in_source, load_claims_from_yamls

        store = session.store
        lattice_root = store.lattice_dir.resolve()
        claims_dir = CLAIM_DIR / asn_label
        claims_dir.mkdir(parents=True, exist_ok=True)

        seen_labels: set[str] = set()
        failed: list[tuple[str, str, str]] = []
        emitted = 0

        for yaml_basename, prop in load_claims_from_yamls(sections_dir):
            raw_label = prop.get("label", "")
            if not raw_label:
                print(
                    f"    WARNING: claim without label in {yaml_basename}",
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
                    f"    WARNING: duplicate label {label!r} in {yaml_basename}",
                    file=sys.stderr,
                )
                continue
            seen_labels.add(label)

            llm_body = (prop.get("body") or "").strip()
            resolved = find_in_source(source_note_text, llm_body)
            if resolved is None:
                failed.append((label, yaml_basename, llm_body[:120]))
                continue

            body_md = claims_dir / f"{label}.md"
            body_md.write_text(resolved.rstrip() + "\n")

            body_rel = str(body_md.resolve().relative_to(lattice_root))
            body_addr = store.register_path(body_rel)
            emit_claim(store, body_addr)
            attest_attribute(session, body_md, "label", label)
            attest_attribute(
                session, body_md, "name", (prop.get("name") or label).strip(),
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
