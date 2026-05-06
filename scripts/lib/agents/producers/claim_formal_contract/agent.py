"""Claim formal-contract agent — synthesize the Formal Contract section
of a claim's md body.

Fires per claim where the contract.<kind> is set AND the kind requires
a Formal Contract (theorem / lemma / corollary) AND the claim md does
not yet have a `*Formal Contract:*` section. One fire = build dep
context, dispatch the synthesis LLM (with up to N internal cycles for
transient failure), review the rewrite for damage, write the new
section to disk, advance the claim's supersession chain, persist the
resolve-doc audit trail, commit.

This is the lifted form of the previous produce_contract phase.
Earlier the orchestrator iterated over `find_claims_needing_quality`
and called `produce_contract` per claim; now the runner walks per-
claim via the predicate.

Caste: producer. The Formal Contract section IS the producer's
output (lives in the claim md body, not a separate sidecar). The
agent edits the body and advances the claim's chain so downstream
sidecar predicates flip False and re-attest.
"""

from __future__ import annotations

import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import ClassVar

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.predicates import current_contract_kind
from lib.protocols.febe.protocol import Session
from lib.shared.git_ops import step_commit_asn
from lib.shared.paths import LATTICE, FORMAL_CONTRACT_DIR

from .helpers import (
    build_dep_context, has_formal_contract, review_rewrite,
    synthesize_contract, validate_contract,
)


SYNTHESIS_MODEL = "opus"
MAX_CYCLES = 3
KINDS_REQUIRING_CONTRACT = frozenset({"theorem", "lemma", "corollary"})


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

    def __init__(self, *, model: str = SYNTHESIS_MODEL, max_cycles: int = MAX_CYCLES):
        self.model = model
        self.max_cycles = max_cycles

    def run(self, session: Session, claim_addr: Address) -> AgentResult:
        claim_rel = session.get_path_for_addr(claim_addr)
        if claim_rel is None:
            return AgentResult(success=False, detail="no-claim-path")

        m = re.search(r"(ASN-(\d{4}))/([^/]+)\.md$", claim_rel)
        if m is None:
            return AgentResult(success=False, detail="unparseable-claim-path")
        asn_label = m.group(1)
        asn_num = int(m.group(2))
        claim_label = m.group(3)

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
                    success=False, detail=f"review-rejected:{review_detail[:120]}",
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
                success=False, detail=f"failed-after-{self.max_cycles}-cycles",
            )

        # Advance the claim's supersession chain — body changed, so
        # downstream sidecar predicates (description_is_fresh,
        # signature_is_fresh, references_is_fresh) flip False and the
        # corresponding producers re-attest on the next runner pass.
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

        return AgentResult(
            success=True, detail=f"emitted match={match}",
        )
