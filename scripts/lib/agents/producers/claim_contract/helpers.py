"""LLM helper for claim-contract: classify a claim's contract kind.

One LLM invocation per call: render the annotate-type prompt with the
claim's body + label + name, dispatch Sonnet, parse the YAML response,
validate the kind against the contract.<kind> vocabulary, return a
structured result.

Public entry: `extract_contract_kind(...)`.
"""

from __future__ import annotations

from typing import NamedTuple

from lib.shared.common import read_file
from lib.shared.llm_response import invoke_text, parse_yaml_dict
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

    raw_text, elapsed = invoke_text(prompt, model=model)
    parsed = parse_yaml_dict(raw_text)

    if "type" not in parsed:
        raise ValueError(
            f"contract-classify response missing 'type' field:\n{raw_text}"
        )
    kind = str(parsed["type"]).strip()
    if kind not in VALID_KINDS:
        raise ValueError(
            f"invalid contract kind {kind!r}; must be one of "
            f"{sorted(VALID_KINDS)}\n--- raw ---\n{raw_text}"
        )

    return ContractClassification(
        kind=kind, raw_text=raw_text, elapsed_seconds=elapsed,
    )
