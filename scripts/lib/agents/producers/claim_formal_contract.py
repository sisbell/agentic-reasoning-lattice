"""Claim formal-contract producer — synthesize the Formal Contract
section in a claim's md body.

Fires per claim where the contract.<kind> is set AND the kind requires
a Formal Contract (theorem / lemma / corollary) AND the claim md does
not yet have a `*Formal Contract:*` section. One fire = build dep
context, dispatch the synthesis LLM (with up to N internal cycles for
transient failure), review the rewrite for damage, write the new
section to disk, advance the claim's supersession chain, persist the
resolve-doc audit trail, commit.

Caste: producer. The Formal Contract section IS the producer's output
(lives in the claim md body, not a separate sidecar). The agent edits
the body and advances the claim's chain so downstream sidecar
predicates flip False and re-attest.
"""

from __future__ import annotations

import re
import sys
from datetime import datetime, timezone
from typing import ClassVar, Tuple

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.lattice.deps import build_deps_for_asn
from lib.lattice.labels import format_label, parse_claim_doc_path
from lib.predicates import current_contract_kind
from lib.protocols.febe.protocol import Session
from lib.shared.claim_files import build_label_index
from lib.shared.common import find_asn
from lib.shared.foundation import _extract_formal_contract
from lib.shared.git_ops import step_commit_asn
from lib.shared.invoke_claude import invoke_claude
from lib.shared.paths import (
    CLAIM_DIR, FORMAL_CONTRACT_DIR, LATTICE, claim_statements, prompt_path,
)


SYNTHESIS_MODEL = "opus"
MAX_CYCLES = 3
KINDS_REQUIRING_CONTRACT = frozenset({"theorem", "lemma", "corollary"})

SYNTHESIS_TEMPLATE = prompt_path(
    "agents/producers/claim_formal_contract/produce-contract.md",
)
REVIEW_REWRITE_TEMPLATE = prompt_path(
    "agents/producers/claim_formal_contract/review-rewrite.md",
)
VALIDATE_CONTRACT_TEMPLATE = prompt_path(
    "agents/producers/claim_formal_contract/validate-contracts.md",
)


# ─── LLM helpers ────────────────────────────────────────────────────


def has_formal_contract(section_text: str) -> bool:
    """True iff the claim body has a Formal Contract section."""
    return "*Formal Contract:*" in section_text


def synthesize_contract(
    label: str, section: str, dep_text: str, *, model: str = "opus",
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
                            f"### {dep_label} ({format_label(dep_asn)})\n\n"
                            f"{m.group(0).strip()}"
                        )
                        break

    return "\n\n".join(dep_parts) if dep_parts else "(none)"


# ─── Resolve-doc persistence (audit trail) ──────────────────────────


def _next_run_num(asn_label: str, claim_label: str) -> int:
    asn_dir = FORMAL_CONTRACT_DIR / asn_label
    if not asn_dir.exists():
        return 1
    pat = re.compile(rf"^{re.escape(claim_label)}-(\d+)\.md$")
    nums = []
    for p in asn_dir.iterdir():
        m = pat.match(p.name)
        if m:
            nums.append(int(m.group(1)))
    return (max(nums) if nums else 0) + 1


def _persist_resolve_doc(
    asn_label: str,
    claim_label: str,
    cycles: int,
    final_response: str,
    review_detail: str,
    validation_match: bool,
    validation_detail: str,
    model: str,
):
    run_num = _next_run_num(asn_label, claim_label)
    asn_dir = FORMAL_CONTRACT_DIR / asn_label
    asn_dir.mkdir(parents=True, exist_ok=True)
    path = asn_dir / f"{claim_label}-{run_num}.md"
    timestamp = (
        datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z")
    )
    parts = [
        f"# Claim Formal Contract — {asn_label}/{claim_label} — run {run_num}\n",
        f"*{timestamp}*",
        f"*Model: {model}*",
        f"*Cycles: {cycles}*",
        f"*Validation: {'MATCH' if validation_match else 'MISMATCH'}*",
        "",
        "## Validation detail",
        "",
        validation_detail or "(no detail)",
        "",
        "## Review-rewrite detail",
        "",
        review_detail or "(passed)",
        "",
        "## Final LLM response",
        "",
        final_response.strip(),
    ]
    path.write_text("\n".join(parts) + "\n")
    return path, run_num


# ─── Agent class ────────────────────────────────────────────────────


class ClaimFormalContractAgent(Agent):
    """Synthesize the Formal Contract section for one claim per fire.

    Multi-cycle within the fire (transient LLM failures retry; review-
    rewrite rejection fails). Edits the claim md directly and advances
    the claim's supersession chain so downstream sidecar predicates
    flip False and re-attest.
    """

    role: ClassVar[str] = "claim-formal-contract"

    def __init__(
        self, *, model: str = SYNTHESIS_MODEL, max_cycles: int = MAX_CYCLES,
    ):
        self.model = model
        self.max_cycles = max_cycles

    def run(self, session: Session, claim_addr: Address) -> AgentResult:
        claim_rel = session.get_path_for_addr(claim_addr)
        if claim_rel is None:
            return AgentResult(success=False, detail="no-claim-path")

        parsed = parse_claim_doc_path(claim_rel)
        if parsed is None:
            return AgentResult(success=False, detail="unparseable-claim-path")
        asn_label, claim_label, asn_num = parsed

        claim_md_full = LATTICE / claim_rel
        if not claim_md_full.exists():
            return AgentResult(success=False, detail="no-claim-file")

        section = claim_md_full.read_text()
        kind = current_contract_kind(session, claim_addr)
        if kind not in KINDS_REQUIRING_CONTRACT:
            return AgentResult(
                success=True,
                detail=f"skip:kind={kind}-doesnt-need-contract",
            )
        if has_formal_contract(section):
            return AgentResult(success=True, detail="skip:already-has-contract")

        dep_text = build_dep_context(asn_num, claim_label)

        final_response = ""
        review_detail = ""
        cycles_used = 0
        for cycle in range(1, self.max_cycles + 1):
            cycles_used = cycle
            print(
                f"  [FORMAL-CONTRACT] {asn_label}/{claim_label} "
                f"(cycle {cycle}, {self.model})...",
                file=sys.stderr,
            )
            new_section, elapsed = synthesize_contract(
                claim_label, section, dep_text, model=self.model,
            )
            if new_section is None:
                print(
                    f"  [FORMAL-CONTRACT] LLM returned empty after "
                    f"{elapsed:.0f}s",
                    file=sys.stderr,
                )
                return AgentResult(success=False, detail="llm-empty")
            final_response = new_section
            if "<tool_call>" in new_section:
                print(
                    f"  [FORMAL-CONTRACT] REJECTED (tool_call leak); retrying",
                    file=sys.stderr,
                )
                continue
            if new_section == section.strip():
                print(
                    f"  [FORMAL-CONTRACT] no changes from LLM",
                    file=sys.stderr,
                )
                return AgentResult(
                    success=True, detail="no-changes-from-llm",
                )

            ok, review_detail = review_rewrite(
                claim_label, section, new_section, model="sonnet",
            )
            if not ok:
                print(
                    f"  [FORMAL-CONTRACT] REJECTED by review-rewrite — "
                    f"{review_detail[:120]}...",
                    file=sys.stderr,
                )
                return AgentResult(
                    success=False,
                    detail=f"review-rejected:{review_detail[:120]}",
                )

            claim_md_full.write_text(new_section + "\n")
            print(
                f"  [FORMAL-CONTRACT] wrote {claim_label}.md ({elapsed:.0f}s)",
                file=sys.stderr,
            )

            if has_formal_contract(new_section):
                break

            section = new_section
            print(
                f"  [FORMAL-CONTRACT] missing Formal Contract still; retrying",
                file=sys.stderr,
            )
        else:
            print(
                f"  [FORMAL-CONTRACT] failed after {self.max_cycles} cycles",
                file=sys.stderr,
            )
            return AgentResult(
                success=False,
                detail=f"failed-after-{self.max_cycles}-cycles",
            )

        # Advance the claim's supersession chain — body changed, so
        # downstream sidecar predicates flip False and the corresponding
        # producers re-attest on the next runner pass.
        session.register_version(claim_addr)

        # Validate the new contract against the proof. Informational —
        # mismatch doesn't fail the fire (the structural validator is
        # the authority on contract correctness).
        match, validation_detail = validate_contract(
            claim_label, claim_md_full.read_text(), model="sonnet",
        )

        _, run_num = _persist_resolve_doc(
            asn_label, claim_label, cycles_used, final_response,
            review_detail, match, validation_detail, self.model,
        )

        step_commit_asn(
            asn_num,
            hint=(
                f"claim-formal-contract(asn): {asn_label}/{claim_label} — "
                f"{'MATCH' if match else 'MISMATCH'}, run {run_num}"
            ),
        )

        return AgentResult(success=True, detail=f"emitted match={match}")
