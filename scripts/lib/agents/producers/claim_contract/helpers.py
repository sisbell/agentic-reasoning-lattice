"""LLM helper for claim-contract: classify a claim's contract kind.

One LLM invocation per call: render the annotate-type prompt with the
claim's body + label + name, dispatch Sonnet, parse the YAML response,
validate the kind against the contract.<kind> vocabulary, return a
structured result.

Public entry: `extract_contract_kind(...)`. Everything else is
private.
"""

from __future__ import annotations

from typing import NamedTuple, Tuple

import yaml

from lib.shared.common import read_file
from lib.shared.invoke_claude import invoke_claude, strip_code_fence
from lib.shared.paths import prompt_path


PROMPT_TEMPLATE = prompt_path("claim-derivation/annotate-type.md")

# Mirrors the contract.<kind> vocabulary registered in lib/backend/types.py.
# "consequence" appears in the prompt's YAML tail but not in the type
# registry; the validator below rejects it (LLM must pick one of the
# six structurally-valid kinds).
VALID_KINDS = frozenset({
    "axiom", "definition", "design-requirement",
    "lemma", "theorem", "corollary",
})


class ContractClassification(NamedTuple):
    """Structured agent output."""
    kind: str          # one of VALID_KINDS
    raw_text: str      # full LLM output for audit trail
    elapsed_seconds: float


def extract_contract_kind(
    claim_md_content: str,
    label: str,
    name: str,
    *,
    model: str = "sonnet",
) -> ContractClassification:
    """Run Sonnet against the annotate-type prompt; return parsed kind.

    Raises on malformed LLM output (missing `type` field, invalid
    kind) — no graceful degradation; agent surfaces the failure.
    """
    template = read_file(PROMPT_TEMPLATE)
    prompt = (
        template
        .replace("{{body}}", claim_md_content)
        .replace("{{label}}", label)
        .replace("{{name}}", name)
    )

    result = invoke_claude(prompt, model=model, effort="high")
    if not result.text:
        raise RuntimeError(
            f"contract-classify: LLM returned empty after "
            f"{result.elapsed:.0f}s",
        )

    text = strip_code_fence(result.text)
    try:
        parsed = yaml.safe_load(text)
    except yaml.YAMLError as e:
        raise ValueError(f"YAML parse error: {e}\n--- raw ---\n{text}")

    if not isinstance(parsed, dict) or "type" not in parsed:
        raise ValueError(
            f"contract-classify response missing 'type' field:\n{text}"
        )
    kind = str(parsed["type"]).strip()
    if kind not in VALID_KINDS:
        raise ValueError(
            f"invalid contract kind {kind!r}; must be one of "
            f"{sorted(VALID_KINDS)}\n--- raw ---\n{text}"
        )

    return ContractClassification(
        kind=kind,
        raw_text=result.text,
        elapsed_seconds=result.elapsed,
    )
