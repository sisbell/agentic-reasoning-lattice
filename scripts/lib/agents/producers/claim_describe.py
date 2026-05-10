"""Claim-describe agent — one LLM call per fire to refresh a description.

Fires when the claim's supersession chain has advanced past the
description's chain (i.e., an edit happened, the description hasn't
been re-attested for the new revision). On each fire:

  1. Read the claim's md content + any existing description.
  2. LLM produces a 1-3 sentence description (may return existing
     verbatim if still accurate).
  3. Emit a new description-sidecar version via register_version,
     advancing the description's supersession chain. The sidecar's
     file content is overwritten with the LLM's output.

The new sidecar version's tumbler is later than the claim's latest
edit marker, so the predicate flips True until the next claim edit.
"""

from __future__ import annotations

import sys
from typing import ClassVar, Optional

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.lattice.attributes import attest_against_doc_head
from lib.predicates import description_sidecar_of
from lib.protocols.febe.protocol import Session
from lib.shared.invoke_claude import invoke_claude
from lib.shared.paths import prompt_path
from lib.shared.prompts import read_prompt


DESCRIBE_MODEL = "sonnet"
DESCRIBE_TEMPLATE = prompt_path("agents/producers/claim_describe.md")


class ClaimDescribeAgent(Agent):
    """One LLM call per fire to attest the claim's description against
    its current revision state."""

    role: ClassVar[str] = "claim-describe"

    def run(self, session: Session, claim_addr: Address) -> AgentResult:
        claim_path = session.get_path_for_addr(claim_addr)
        if claim_path is None:
            return AgentResult(success=False, detail="no-claim-path")

        full_claim = session.store.lattice_dir / claim_path
        if not full_claim.exists():
            return AgentResult(success=False, detail="no-claim-file")

        claim_text = full_claim.read_text()

        # Existing description, if any (the canonical sidecar address
        # the description link points at).
        sidecar_addr = description_sidecar_of(session, claim_addr)
        existing_desc = self._read_sidecar_text(session, sidecar_addr)

        # LLM call
        prompt = (
            read_prompt(DESCRIBE_TEMPLATE)
            .replace("{{claim}}", claim_text)
            .replace("{{existing}}", existing_desc or "(none)")
        )
        result = invoke_claude(
            prompt, model=DESCRIBE_MODEL, effort="high",
        )
        if not result.text:
            return AgentResult(success=False, detail="llm-failed")

        new_desc = result.text.strip()
        print(
            f"  [DESCRIBE] {full_claim.stem} ({result.elapsed:.0f}s)",
            file=sys.stderr,
        )

        # Attest + emit freshness-anchor citation. The LLM returns text
        # without an explicit "no change" verdict, so we determine
        # content_changed by comparing the new description to the
        # existing one (both stripped). True on first emission (no
        # existing) and on every real edit; False only when the LLM
        # produced byte-identical output.
        content_changed = (
            existing_desc is None or new_desc != existing_desc
        )
        attest_against_doc_head(
            session, claim_path, "description", new_desc, claim_addr,
            content_changed=content_changed,
        )

        return AgentResult(success=True, detail="emitted")

    def _read_sidecar_text(
        self, session: Session, sidecar_addr: Optional[Address],
    ) -> Optional[str]:
        """Read the sidecar's file content, or None if unresolvable."""
        if sidecar_addr is None:
            return None
        sidecar_path = session.get_path_for_addr(sidecar_addr)
        if sidecar_path is None:
            return None
        full = session.store.lattice_dir / sidecar_path
        if not full.exists():
            return None
        return full.read_text().strip() or None
