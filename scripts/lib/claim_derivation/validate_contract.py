"""Validate one claim's formal contract against its proof prose.

Single-claim validator used by produce_contract during contract
generation: after producing or revising a claim's section with a
*Formal Contract:* block, this checks that the contract correctly
reflects the prose proof.
"""

from lib.shared.common import invoke_claude
from lib.shared.paths import prompt_path


VALIDATE_TEMPLATE = prompt_path("claim-convergence/assembly/validate-contracts.md")


def _extract_formal_contract(section_text):
    """Extract the formal contract block from a claim section."""
    marker = "*Formal Contract:*"
    idx = section_text.find(marker)
    if idx == -1:
        return None
    return section_text[idx:].strip()


def validate_contract(label, section, signature="", dependencies="", model="sonnet"):
    """Validate one claim's contract against its proof section.

    Returns (match: bool, detail: str).
    """
    contract = _extract_formal_contract(section)
    if contract is None:
        return True, ""

    marker = "*Formal Contract:*"
    idx = section.find(marker)
    proof_section = section[:idx].strip() if idx != -1 else section

    template = VALIDATE_TEMPLATE.read_text()
    prompt = (template
              .replace("{{label}}", label)
              .replace("{{proof_section}}", proof_section)
              .replace("{{formal_contract}}", contract)
              .replace("{{signature}}", signature or "(none)")
              .replace("{{dependencies}}", dependencies or "(none)"))

    result, _elapsed = invoke_claude(prompt, model=model, effort="high")

    if result is None:
        return True, ""

    if "RESULT: MATCH" in result:
        return True, ""

    if "RESULT: MISMATCH" in result:
        idx = result.find("RESULT: MISMATCH")
        detail = result[idx + len("RESULT: MISMATCH"):].strip()
        return False, detail

    return True, ""
