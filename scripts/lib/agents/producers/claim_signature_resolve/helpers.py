"""LLM helper for claim-signature-resolve: extract per-claim signature
introductions and removals.

Public entry: `extract_signature_changes(...)`.
"""

from __future__ import annotations

import re
from typing import List, NamedTuple, Tuple

from lib.shared.common import read_file
from lib.shared.llm_response import invoke_text, parse_two_sections
from lib.shared.paths import prompt_path


PROMPT_TEMPLATE = prompt_path("claim-refinement/signature-resolve.md")


class SignatureChanges(NamedTuple):
    introduces: list
    removes: list
    raw_text: str
    elapsed_seconds: float


def extract_signature_changes(
    claim_md_content: str,
    notation_primitives: list,
    upstream_signatures: List[Tuple[str, str]],
    existing_signature: str,
    *,
    model: str = "sonnet",
) -> SignatureChanges:
    """Run Sonnet against the signature-resolve prompt; return parsed
    INTRODUCES / REMOVES.

    `upstream_signatures` is `[(label, signature_text), ...]` for each
    upstream claim with a populated signature sidecar.

    Raises on malformed LLM output (missing headers, YAML parse errors,
    malformed entries) — no graceful degradation.
    """
    prompt = _render_prompt(
        claim_md_content, notation_primitives, upstream_signatures,
        existing_signature,
    )
    raw_text, elapsed = invoke_text(prompt, model=model, tools="Read")
    introduces, removes = parse_two_sections(
        raw_text, "INTRODUCES", "REMOVES",
    )
    _validate_introduces(introduces)
    _validate_removes(removes)
    return SignatureChanges(
        introduces=introduces,
        removes=removes,
        raw_text=raw_text,
        elapsed_seconds=elapsed,
    )


def _format_upstream_sigs(upstream: List[Tuple[str, str]]) -> str:
    if not upstream:
        return (
            "(none — this is a foundation claim or has no upstream signatures)"
        )
    return "\n\n".join(f"### {label}\n{sig}" for label, sig in upstream)


def _format_notation_primitives(primitives: list) -> str:
    if not primitives:
        return "(none registered)"
    return "\n".join(f"- `{p}`" for p in primitives)


def _render_prompt(
    claim_md_content: str,
    notation_primitives: list,
    upstream_sigs: List[Tuple[str, str]],
    existing_signature: str,
) -> str:
    template = read_file(PROMPT_TEMPLATE)
    return (
        template
        .replace("{{claim_md_content}}", claim_md_content)
        .replace(
            "{{notation_primitives}}",
            _format_notation_primitives(notation_primitives),
        )
        .replace(
            "{{upstream_signatures}}",
            _format_upstream_sigs(upstream_sigs),
        )
        .replace("{{existing_signature}}", existing_signature or "(none)")
    )


def _validate_introduces(introduces: list) -> None:
    """Per-entry validation; mutates entries to add a parsed `symbol`."""
    for entry in introduces:
        if not isinstance(entry, dict):
            raise ValueError(f"INTRODUCES entry not a dict: {entry}")
        if "bullet" not in entry:
            raise ValueError(f"INTRODUCES entry missing 'bullet': {entry}")
        bullet = entry["bullet"]
        if not isinstance(bullet, str) or not bullet.startswith("- `"):
            raise ValueError(
                f"INTRODUCES bullet must start with '- `<symbol>`': {entry}"
            )
        m = re.match(r"^- `([^`]+)`", bullet)
        if not m:
            raise ValueError(
                f"INTRODUCES bullet has no parseable symbol: {bullet!r}"
            )
        entry["symbol"] = m.group(1)


def _validate_removes(removes: list) -> None:
    for entry in removes:
        if not isinstance(entry, dict):
            raise ValueError(f"REMOVES entry not a dict: {entry}")
        for field in ("symbol", "reason"):
            if field not in entry:
                raise ValueError(f"REMOVES entry missing {field!r}: {entry}")
