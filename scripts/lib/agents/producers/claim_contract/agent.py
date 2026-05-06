"""Claim-contract agent — classify a claim's contract kind once.

Fires per claim missing a `contract.<kind>` classifier. One fire =
read claim md + label/name sidecars, dispatch the LLM helper to
classify the contract kind (axiom / definition / design-requirement /
lemma / theorem / corollary), emit the contract.<kind> link, persist
the resolve-doc audit trail, commit.

This is the lifted form of the previous annotate-type pass (which
wrote a yaml.type field that transclude later read and turned into a
contract.<kind> emission). Predicate-fired by the runner; emits
substrate directly.

Caste: producer. Working surface: claim md prose + label/name
sidecars. Identity grant: the contract.<kind> classifier on the
claim doc — once classified, the agent does not re-fire (predicate
is a one-shot existence check, not a chain comparison).
"""

from __future__ import annotations

import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import ClassVar

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.backend.emit import emit_contract
from lib.protocols.febe.protocol import Session
from lib.shared.git_ops import step_commit_asn
from lib.shared.paths import CLAIM_CONTRACT_DIR, LATTICE

from .helpers import extract_contract_kind


CONTRACT_MODEL = "sonnet"


# ─── Sidecar helpers ────────────────────────────────────────────────


def _read_sidecar_text(claim_md_full: Path, kind: str) -> str:
    """Read `<claim>.<kind>.md` content, stripped. Empty string if missing."""
    sidecar = claim_md_full.parent / f"{claim_md_full.stem}.{kind}.md"
    if not sidecar.exists():
        return ""
    return sidecar.read_text().strip()


# ─── Resolve-doc persistence (audit trail) ──────────────────────────


def _next_run_num(asn_label: str, claim_label: str) -> int:
    asn_dir = CLAIM_CONTRACT_DIR / asn_label
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
    asn_label: str, claim_label: str, sonnet_output: str, model: str,
):
    run_num = _next_run_num(asn_label, claim_label)
    asn_dir = CLAIM_CONTRACT_DIR / asn_label
    asn_dir.mkdir(parents=True, exist_ok=True)
    path = asn_dir / f"{claim_label}-{run_num}.md"
    timestamp = (
        datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z")
    )
    content = (
        f"# Claim Contract — {asn_label}/{claim_label} — run {run_num}\n"
        f"\n"
        f"*{timestamp}*\n"
        f"*Model: {model}*\n"
        f"\n"
        f"## Output\n"
        f"\n"
        f"{sonnet_output.strip()}\n"
    )
    path.write_text(content)
    return path, run_num


# ─── Agent class ────────────────────────────────────────────────────


class ClaimContractAgent(Agent):
    """One claim's contract classification per fire.

    Reads claim md + label/name sidecars, dispatches the LLM helper,
    emits the contract.<kind> classifier, persists the resolve-doc
    audit trail, commits per fire.

    Producer caste, predicate-fired (skip if claim already has a
    contract.<kind> classifier).
    """

    role: ClassVar[str] = "claim-contract"

    def __init__(self, *, model: str = CONTRACT_MODEL):
        self.model = model

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

        claim_md_content = claim_md_full.read_text()
        label = _read_sidecar_text(claim_md_full, "label") or claim_label
        name = _read_sidecar_text(claim_md_full, "name") or claim_label

        print(
            f"  [CLAIM-CONTRACT] {asn_label}/{claim_label} ({self.model})...",
            end="", file=sys.stderr, flush=True,
        )
        try:
            result = extract_contract_kind(
                claim_md_content, label, name, model=self.model,
            )
        except (RuntimeError, ValueError) as e:
            print(f" FAILED: {e}", file=sys.stderr)
            return AgentResult(success=False, detail=f"llm-failed:{e}")
        print(
            f" kind={result.kind} ({result.elapsed_seconds:.0f}s)",
            file=sys.stderr,
        )

        emit_contract(session.store, claim_addr, result.kind)

        _, run_num = _persist_resolve_doc(
            asn_label, claim_label, result.raw_text, self.model,
        )

        step_commit_asn(
            asn_num,
            hint=(
                f"claim-contract(asn): {asn_label}/{claim_label} — "
                f"{result.kind}, run {run_num}"
            ),
        )

        return AgentResult(
            success=True, detail=f"kind={result.kind}",
        )
