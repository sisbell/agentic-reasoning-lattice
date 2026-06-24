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
from pathlib import Path
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
from lib.shared.invoke_claude import invoke_claude
from lib.shared.paths import (
    CLAIM_DIR, DERIVED_CLAIM_DIR, FORMAL_CONTRACT_DIR, prompt_path,
)
from lib.shared.prompts import read_prompt


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
    template = read_prompt(SYNTHESIS_TEMPLATE)
    prompt = (
        template
        .replace("{{label}}", label)
        .replace("{{section}}", section)
        .replace("{{dependency_sections}}", dep_text)
    )
    response = invoke_claude(prompt, model=model, effort="xhigh")
    if not response.text:
        return None, response.elapsed
    return response.text.strip(), response.elapsed


def review_rewrite(
    label: str, before: str, after: str, *, model: str = "sonnet",
) -> Tuple[bool, str]:
    """Review a rewrite for damage. Returns (ok, detail).

    On unclear/empty LLM output, defaults to ok=True (don't block).
    """
    template = read_prompt(REVIEW_REWRITE_TEMPLATE)
    prompt = (
        template
        .replace("{{label}}", label)
        .replace("{{before}}", before)
        .replace("{{after}}", after)
    )
    response = invoke_claude(prompt, model=model, effort="xhigh")
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

    template = read_prompt(VALIDATE_CONTRACT_TEMPLATE)
    prompt = (
        template
        .replace("{{label}}", label)
        .replace("{{proof_section}}", proof_section)
        .replace("{{formal_contract}}", contract)
        .replace("{{signature}}", signature or "(none)")
        .replace("{{dependencies}}", dependencies or "(none)")
    )
    response = invoke_claude(prompt, model=model, effort="xhigh")
    text = response.text or ""
    if "RESULT: MATCH" in text:
        return True, ""
    if "RESULT: MISMATCH" in text:
        idx = text.find("RESULT: MISMATCH")
        return False, text[idx + len("RESULT: MISMATCH"):].strip()
    return True, ""


class DependencyResolutionError(RuntimeError):
    """A declared dependency's claim/statement could not be resolved.

    Raised rather than silently clipping the dep — synthesizing a contract
    against an incomplete dependency set produces ungrounded contracts that
    only surface much later (or never). Fail the build here instead.
    """


def build_dep_context(asn_num: int, label: str, claim_base_dir: Path) -> str:
    """Assemble dependency context for the synthesis prompt.

    Same-ASN deps → the dep's claim-file body. Cross-ASN deps → the dep's
    section from its ASN's claims.statements aggregate
    (`claim/<asn>/_statements.md`), looked up region 1.3 first then 1.1.

    EVERY declared dependency must resolve: a missing same-ASN claim file
    or an unfindable cross-ASN statement raises DependencyResolutionError
    (no silent clipping). Returns "(none)" only when the claim has no
    declared deps at all.
    """
    deps_data = build_deps_for_asn(asn_num, claim_base_dir)
    if not deps_data:
        return "(none)"

    claim_data = deps_data.get("claims", {}).get(label, {})
    follows_from = claim_data.get("follows_from", [])
    all_labels = set(deps_data.get("claims", {}).keys())

    _, asn_label = find_asn(str(asn_num))
    claim_dir = claim_base_dir / asn_label
    label_index = build_label_index(claim_dir)
    depends = deps_data.get("depends", [])

    dep_parts = []
    for dep_label in follows_from:
        if dep_label in all_labels:
            # Same-ASN dep: read its claim-file body.
            dep_stem = label_index.get(
                dep_label,
                dep_label.replace("(", "").replace(")", ""),
            )
            dep_file = claim_dir / f"{dep_stem}.md"
            if not dep_file.exists():
                raise DependencyResolutionError(
                    f"{asn_label} {label!r}: same-ASN dependency "
                    f"{dep_label!r} claim file not found at {dep_file}"
                )
            dep_parts.append(
                f"### {dep_label}\n\n{dep_file.read_text().strip()}"
            )
        else:
            # Cross-ASN dep: find its statement in a foundation ASN's
            # claims.statements aggregate (claim/<asn>/_statements.md),
            # region 1.3 first then 1.1.
            pattern = re.compile(
                r'^## ' + re.escape(dep_label) + r'\s*—.*?\n'
                r'(.*?)(?=^## |\Z)',
                re.MULTILINE | re.DOTALL,
            )
            section = None
            for dep_asn in depends:
                for region_dir in (DERIVED_CLAIM_DIR, CLAIM_DIR):  # 1.3, 1.1
                    agg = region_dir / format_label(dep_asn) / "_statements.md"
                    if agg.exists():
                        m = pattern.search(agg.read_text())
                        if m:
                            section = (m.group(0).strip(), dep_asn)
                            break
                if section:
                    break
            if section is None:
                raise DependencyResolutionError(
                    f"{asn_label} {label!r}: cross-ASN dependency "
                    f"{dep_label!r} not found in any foundation "
                    f"claims.statements aggregate (searched "
                    f"{[format_label(d) for d in depends]} in regions 1.3, 1.1)"
                )
            text, dep_asn = section
            dep_parts.append(
                f"### {dep_label} ({format_label(dep_asn)})\n\n{text}"
            )

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
    node: ClassVar[str] = "1.3"

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

        claim_md_full = session.store.lattice_dir / claim_rel
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

        dep_text = build_dep_context(asn_num, claim_label, self.claim_dir)

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

        return AgentResult(success=True, detail=f"emitted match={match}")
