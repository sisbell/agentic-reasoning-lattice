"""LLM helper for citation-resolve: type each label reference in a
claim's prose as depends or forward.

Public entry: `extract_citation_classifications(...)`.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, NamedTuple

from lib.shared.common import read_file
from lib.shared.llm_response import invoke_text, parse_two_sections
from lib.shared.paths import prompt_path


PROMPT_TEMPLATE = prompt_path("claim-refinement/citation-resolve.md")


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
