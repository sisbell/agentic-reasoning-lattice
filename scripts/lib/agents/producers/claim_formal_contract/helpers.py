"""LLM helpers for the claim-formal-contract producer.

Three LLM-driven operations:

- `synthesize_contract(label, section, dep_text, *, model)` — runs the
  produce-contract prompt against a claim's body + dependency context.
  Returns the rewritten section text, or None on transient failure.
- `review_rewrite(label, before, after, *, model)` — runs the
  review-rewrite prompt to detect damaging rewrites. Returns
  (ok, detail) — ok=True means safe to keep the rewrite.
- `validate_contract(label, section, *, model)` — runs the validate-
  contracts prompt to confirm the Formal Contract matches the proof.
  Returns (match, detail) — match=True means contract matches.
- `build_dep_context(asn_num, label)` — assembles same-ASN dependency
  bodies + cross-ASN foundation excerpts for the synthesis prompt.

Side-effect-free helpers; the agent owns substrate writes and file IO.
"""

from __future__ import annotations

import re
import sys
from typing import Tuple

from lib.lattice.deps import build_deps_for_asn
from lib.shared.claim_files import build_label_index
from lib.shared.common import find_asn
from lib.shared.foundation import _extract_formal_contract
from lib.shared.invoke_claude import invoke_claude
from lib.shared.paths import CLAIM_DIR, claim_statements, prompt_path


SYNTHESIS_TEMPLATE = prompt_path("claim-derivation/produce-contract.md")
REVIEW_REWRITE_TEMPLATE = prompt_path("claim-derivation/review-rewrite.md")
VALIDATE_CONTRACT_TEMPLATE = prompt_path(
    "claim-refinement/assembly/validate-contracts.md",
)


def has_formal_contract(section_text: str) -> bool:
    """True iff the claim body has a Formal Contract section."""
    return "*Formal Contract:*" in section_text


def is_definition_section(section_text: str) -> bool:
    """True iff the claim body opens with a `**Definition (...).**` marker.

    Definitions don't get Formal Contract sections; they assign meaning
    rather than asserting truth.
    """
    return bool(re.search(r'^\*\*Definition\s*\(', section_text, re.MULTILINE))


def synthesize_contract(
    label: str,
    section: str,
    dep_text: str,
    *,
    model: str = "opus",
) -> Tuple[str | None, float]:
    """Run the produce-contract prompt; return (rewritten_section, elapsed).

    rewritten_section is None on transient LLM failure (empty response).
    """
    template = SYNTHESIS_TEMPLATE.read_text()
    prompt = (
        template
        .replace("{{label}}", label)
        .replace("{{section}}", section)
        .replace("{{dependency_sections}}", dep_text)
    )
    response = invoke_claude(prompt, model=model, effort="high")
    if not response.text:
        return None, response.elapsed
    return response.text.strip(), response.elapsed


def review_rewrite(
    label: str, before: str, after: str, *, model: str = "sonnet",
) -> Tuple[bool, str]:
    """Review a rewrite for damage. Returns (ok, detail).

    ok=True iff the rewrite is safe to keep. ok=False means rejection.
    On unclear/empty LLM output, defaults to ok=True (don't block).
    """
    template = REVIEW_REWRITE_TEMPLATE.read_text()
    prompt = (
        template
        .replace("{{label}}", label)
        .replace("{{before}}", before)
        .replace("{{after}}", after)
    )
    response = invoke_claude(prompt, model=model, effort="high")
    text = response.text or ""
    if "RESULT: PASS" in text:
        return True, ""
    if "RESULT: FAIL" in text:
        idx = text.find("RESULT: FAIL")
        return False, text[idx + len("RESULT: FAIL"):].strip()
    return True, ""


def validate_contract(
    label: str,
    section: str,
    signature: str = "",
    dependencies: str = "",
    *,
    model: str = "sonnet",
) -> Tuple[bool, str]:
    """Validate a claim's Formal Contract against its proof section.

    Returns (match, detail). match=True iff contract matches; on no
    contract or empty LLM output, returns (True, "").
    """
    contract = _extract_formal_contract(section)
    if not contract:
        return True, ""

    marker = "*Formal Contract:*"
    idx = section.find(marker)
    proof_section = section[:idx].strip() if idx != -1 else section

    template = VALIDATE_CONTRACT_TEMPLATE.read_text()
    prompt = (
        template
        .replace("{{label}}", label)
        .replace("{{proof_section}}", proof_section)
        .replace("{{formal_contract}}", contract)
        .replace("{{signature}}", signature or "(none)")
        .replace("{{dependencies}}", dependencies or "(none)")
    )
    response = invoke_claude(prompt, model=model, effort="high")
    text = response.text or ""
    if "RESULT: MATCH" in text:
        return True, ""
    if "RESULT: MISMATCH" in text:
        idx = text.find("RESULT: MISMATCH")
        return False, text[idx + len("RESULT: MISMATCH"):].strip()
    return True, ""


def build_dep_context(asn_num: int, label: str) -> str:
    """Assemble dependency context for the synthesis prompt.

    Returns markdown text with same-ASN dependency bodies + cross-ASN
    foundation excerpts (from claim-statements transclusion files).
    Returns "(none)" when no deps resolve.
    """
    deps_data = build_deps_for_asn(asn_num)
    if not deps_data:
        return "(none)"

    claim_data = deps_data.get("claims", {}).get(label, {})
    follows_from = claim_data.get("follows_from", [])
    all_labels = set(deps_data.get("claims", {}).keys())

    _, asn_label = find_asn(str(asn_num))
    claim_dir = CLAIM_DIR / asn_label
    label_index = build_label_index(claim_dir)

    dep_parts = []
    for dep_label in follows_from:
        if dep_label in all_labels:
            dep_stem = label_index.get(
                dep_label,
                dep_label.replace("(", "").replace(")", ""),
            )
            dep_file = claim_dir / f"{dep_stem}.md"
            if dep_file.exists():
                dep_parts.append(
                    f"### {dep_label}\n\n{dep_file.read_text().strip()}"
                )

    depends = deps_data.get("depends", [])
    for dep_label in follows_from:
        if dep_label not in all_labels:
            for dep_asn in depends:
                stmt_path = claim_statements(dep_asn)
                if stmt_path.exists():
                    ftext = stmt_path.read_text()
                    pattern = re.compile(
                        r'^## ' + re.escape(dep_label) + r'\s*—.*?\n'
                        r'(.*?)(?=^## |\Z)',
                        re.MULTILINE | re.DOTALL,
                    )
                    m = pattern.search(ftext)
                    if m:
                        dep_parts.append(
                            f"### {dep_label} (ASN-{dep_asn:04d})\n\n"
                            f"{m.group(0).strip()}"
                        )
                        break

    return "\n\n".join(dep_parts) if dep_parts else "(none)"
