"""Claim-decompose agent — first-pass structural analysis of a note.

`ClaimDecomposeAgent` is the operator-gated entry point to the
claim-derivation pipeline. One fire = mechanically split the source
note at `## ` headers, write each section's md to workspace, run the
decompose prompt in parallel on each non-structural section, write
the per-section yaml hypotheses alongside, commit.

Emits no substrate links — downstream phases consume the workspace
yamls. The agent does not auto-fire from a predicate; it is invoked
by the orchestrator (or the CLI) when the operator decides a note is
ready for derivation.
"""

from __future__ import annotations

import re
import sys
import time
from pathlib import Path
from typing import ClassVar

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.protocols.febe.protocol import Session
from lib.shared.git_ops import step_commit_asn
from lib.shared.invoke_claude import parallel_llm_calls
from lib.shared.paths import CLAIM_DERIVATION_DIR, WORKSPACE


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
    """First-pass structural analysis of a note.

    Operator-gated: invoked explicitly by the orchestrator or CLI. Does
    not auto-fire from a runner predicate. Emits no substrate links.
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

        step_commit_asn(asn_number, hint="decompose")
        return AgentResult(
            success=True,
            detail=(
                f"sections={len(sections)} yamls={yaml_count} "
                f"claims={total_props}"
            ),
        )
