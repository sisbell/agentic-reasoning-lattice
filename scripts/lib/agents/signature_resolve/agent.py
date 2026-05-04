"""Signature-resolve agent body.

One LLM invocation: render prompt, call Sonnet, parse the
INTRODUCES/REMOVES YAML response. Returns a `SignatureChanges`
record with the parsed edit lists, the raw text (for the
orchestrator's resolve-doc persistence), and timing.

Public entry: `extract_signature_changes(...)`. Everything else is
private agent-internal helpers.
"""

from __future__ import annotations

import re
from typing import List, NamedTuple, Tuple

import yaml

from lib.shared.common import invoke_claude, read_file, strip_code_fence
from lib.shared.paths import prompt_path


PROMPT_TEMPLATE = prompt_path("claim-convergence/signature-resolve.md")


class SignatureChanges(NamedTuple):
    """Structured agent output."""
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
    """Run Sonnet against the signature-resolve prompt; return parsed changes.

    `upstream_signatures` is `[(label, signature_text), ...]` for each
    upstream claim with a populated signature sidecar.

    Raises on malformed LLM output (missing INTRODUCES/REMOVES headers,
    YAML parse errors, malformed entries) — no graceful degradation;
    the orchestrator decides how to surface a failure.
    """
    prompt = _render_prompt(
        claim_md_content, notation_primitives, upstream_signatures,
        existing_signature,
    )
    raw_text, elapsed = _call_sonnet(prompt, model=model)
    introduces, removes = _parse_response(raw_text)
    return SignatureChanges(
        introduces=introduces,
        removes=removes,
        raw_text=raw_text,
        elapsed_seconds=elapsed,
    )


# ---------------------------------------------------------------------------
# Prompt rendering


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
    """Parse Sonnet's INTRODUCES / REMOVES YAML output.

    Returns (introduces, removes) — lists of dicts. Each INTRODUCES
    entry gains a `symbol` field parsed from its bullet. Fails loudly
    on malformed output.
    """
    text = text.strip()
    intro_idx = text.find("INTRODUCES:")
    rem_idx = text.find("REMOVES:")
    if intro_idx < 0:
        raise ValueError(f"missing INTRODUCES: header:\n{text}")
    if rem_idx < 0:
        raise ValueError(f"missing REMOVES: header:\n{text}")
    if rem_idx < intro_idx:
        raise ValueError("REMOVES appears before INTRODUCES")

    intro_yaml = strip_code_fence(
        text[intro_idx + len("INTRODUCES:"):rem_idx].strip()
    )
    rem_yaml = strip_code_fence(
        text[rem_idx + len("REMOVES:"):].strip()
    )

    try:
        introduces = yaml.safe_load(intro_yaml) or []
        removes = yaml.safe_load(rem_yaml) or []
    except yaml.YAMLError as e:
        raise ValueError(
            f"YAML parse error: {e}\n"
            f"--- INTRODUCES ---\n{intro_yaml}\n"
            f"--- REMOVES ---\n{rem_yaml}"
        )

    if not isinstance(introduces, list):
        raise ValueError(
            f"INTRODUCES must be a list, got "
            f"{type(introduces).__name__}: {introduces!r}\n"
            f"--- raw block ---\n{intro_yaml}"
        )
    if not isinstance(removes, list):
        raise ValueError(
            f"REMOVES must be a list, got "
            f"{type(removes).__name__}: {removes!r}\n"
            f"--- raw block ---\n{rem_yaml}"
        )

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

    for entry in removes:
        if not isinstance(entry, dict):
            raise ValueError(f"REMOVES entry not a dict: {entry}")
        for field in ("symbol", "reason"):
            if field not in entry:
                raise ValueError(f"REMOVES entry missing {field!r}: {entry}")

    return introduces, removes
