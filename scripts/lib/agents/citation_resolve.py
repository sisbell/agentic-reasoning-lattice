"""Citation-resolve agent body.

One LLM invocation: render prompt, call Sonnet, parse the
CLASSIFICATIONS/RETRACTIONS YAML response. Returns a
`CitationClassifications` record with parsed edit lists, raw text
(for the orchestrator's resolve-doc persistence), and timing.

Public entry: `extract_citation_classifications(...)`. Everything
else is private agent-internal helpers.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, NamedTuple, Tuple

import yaml

from lib.shared.common import invoke_claude, read_file, strip_code_fence
from lib.shared.paths import prompt_path


PROMPT_TEMPLATE = prompt_path("claim-convergence/citation-resolve.md")


class CitationClassifications(NamedTuple):
    """Structured agent output."""
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
    """Run Sonnet against the citation-resolve prompt; return parsed output.

    Raises on malformed LLM output (missing CLASSIFICATIONS/RETRACTIONS
    headers, YAML parse errors, malformed entries, invalid direction
    values) — no graceful degradation; orchestrator decides how to
    surface a failure.
    """
    prompt = _render_prompt(
        claim_md_content, claim_dir, claims_root,
        existing_depends, existing_forwards,
    )
    raw_text, elapsed = _call_sonnet(prompt, model=model)
    classifications, retractions = _parse_response(raw_text)
    return CitationClassifications(
        classifications=classifications,
        retractions=retractions,
        raw_text=raw_text,
        elapsed_seconds=elapsed,
    )


# ---------------------------------------------------------------------------
# Prompt rendering


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


# ---------------------------------------------------------------------------
# Sonnet invocation


def _call_sonnet(prompt: str, *, model: str) -> Tuple[str, float]:
    text, elapsed = invoke_claude(
        prompt, model=model, effort="high", tools="Read",
    )
    if not text:
        raise RuntimeError(f"Sonnet returned empty after {elapsed:.0f}s")
    return text, elapsed


# ---------------------------------------------------------------------------
# Response parsing


def _parse_response(text: str) -> Tuple[list, list]:
    """Parse Sonnet's CLASSIFICATIONS/RETRACTIONS YAML output.

    Returns (classifications, retractions) — lists of dicts. Fails
    loudly on malformed output.
    """
    text = text.strip()
    cls_idx = text.find("CLASSIFICATIONS:")
    ret_idx = text.find("RETRACTIONS:")
    if cls_idx < 0:
        raise ValueError(f"missing CLASSIFICATIONS: header in response:\n{text}")
    if ret_idx < 0:
        raise ValueError(f"missing RETRACTIONS: header in response:\n{text}")
    if ret_idx < cls_idx:
        raise ValueError(
            "RETRACTIONS appears before CLASSIFICATIONS in response"
        )

    cls_yaml = strip_code_fence(
        text[cls_idx + len("CLASSIFICATIONS:"):ret_idx].strip()
    )
    ret_yaml = strip_code_fence(
        text[ret_idx + len("RETRACTIONS:"):].strip()
    )

    try:
        classifications = yaml.safe_load(cls_yaml) or []
        retractions = yaml.safe_load(ret_yaml) or []
    except yaml.YAMLError as e:
        raise ValueError(
            f"YAML parse error: {e}\n"
            f"--- CLASSIFICATIONS ---\n{cls_yaml}\n"
            f"--- RETRACTIONS ---\n{ret_yaml}"
        )

    if not isinstance(classifications, list):
        raise ValueError(
            f"CLASSIFICATIONS must be a list, got "
            f"{type(classifications).__name__}: {classifications!r}\n"
            f"--- raw block ---\n{cls_yaml}"
        )
    if not isinstance(retractions, list):
        raise ValueError(
            f"RETRACTIONS must be a list, got "
            f"{type(retractions).__name__}: {retractions!r}\n"
            f"--- raw block ---\n{ret_yaml}"
        )

    for c in classifications:
        if not isinstance(c, dict):
            raise ValueError(f"classification entry not a dict: {c}")
        for field in ("label", "direction", "bullet"):
            if field not in c:
                raise ValueError(f"classification missing {field!r}: {c}")
        if c["direction"] not in ("depends", "forward"):
            raise ValueError(f"invalid direction in classification: {c}")

    for r in retractions:
        if not isinstance(r, dict):
            raise ValueError(f"retraction entry not a dict: {r}")
        for field in ("label", "direction"):
            if field not in r:
                raise ValueError(f"retraction missing {field!r}: {r}")
        if r["direction"] not in ("depends", "forward"):
            raise ValueError(f"invalid direction in retraction: {r}")

    return classifications, retractions
