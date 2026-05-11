"""Claim-contract producer — classify a claim's contract kind once.

Fires per claim missing a `contract.<kind>` classifier. One fire =
read claim md + label/name sidecars, dispatch the annotate-type
prompt, validate the kind against the contract.<kind> vocabulary,
emit the classifier link, persist the resolve-doc audit trail,
commit.

Lifted from the previous annotate-type pass (which wrote a
yaml.type field that transclude later read and turned into a
contract.<kind> emission). Predicate-fired by the runner; emits
substrate directly.

Caste: producer. Identity grant: the contract.<kind> classifier on
the claim doc — once classified, the agent does not re-fire
(predicate is a one-shot existence check, not a chain comparison).
"""

from __future__ import annotations

import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import ClassVar, NamedTuple

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.backend.emit import emit_contract
from lib.protocols.febe.protocol import Session
from lib.shared.common import read_file
from lib.shared.llm_response import invoke_text, parse_yaml_dict
from lib.lattice.labels import parse_claim_doc_path
from lib.shared.paths import CLAIM_CONTRACT_DIR, LATTICE, prompt_path
from lib.shared.prompts import read_prompt


CONTRACT_MODEL = "sonnet"
PROMPT_TEMPLATE = prompt_path("agents/producers/claim_contract.md")

# Mirrors the contract.<kind> vocabulary registered in lib/backend/types.py.
# "consequence" appears in the prompt's YAML tail but not in the type
# registry; the validator below rejects it (LLM must pick one of the
# six structurally-valid kinds).
VALID_KINDS = frozenset({
    "axiom", "definition", "design-requirement",
    "lemma", "theorem", "corollary",
})


class ContractClassification(NamedTuple):
    """Structured LLM output."""
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
    kind) — no graceful degradation.
    """
    template = read_prompt(PROMPT_TEMPLATE)
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


def _read_sidecar_text(claim_md_full: Path, kind: str) -> str:
    """Read `<claim>.<kind>.md` content, stripped. Empty string if missing."""
    sidecar = claim_md_full.parent / f"{claim_md_full.stem}.{kind}.md"
    if not sidecar.exists():
        return ""
    return sidecar.read_text().strip()


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


class ClaimContractAgent(Agent):
    """One claim's contract classification per fire.

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

        parsed = parse_claim_doc_path(claim_rel)
        if parsed is None:
            return AgentResult(success=False, detail="unparseable-claim-path")
        asn_label, claim_label, asn_num = parsed

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

        return AgentResult(success=True, detail=f"kind={result.kind}")
