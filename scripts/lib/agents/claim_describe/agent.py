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
from lib.lattice.attributes import emit_attribute
from lib.predicates import description_sidecar_of
from lib.protocols.febe.protocol import Session
from lib.shared.invoke_claude import invoke_claude
from lib.shared.paths import prompt_path


DESCRIBE_MODEL = "sonnet"
DESCRIBE_TEMPLATE = prompt_path("claim-describe/describe.md")


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
            DESCRIBE_TEMPLATE.read_text()
            .replace("{{claim}}", claim_text)
            .replace("{{existing}}", existing_desc or "(none)")
        )
        text, elapsed = invoke_claude(
            prompt, model=DESCRIBE_MODEL, effort="high",
        )
        if not text:
            return AgentResult(success=False, detail="llm-failed")

        new_desc = text.strip()
        print(
            f"  [DESCRIBE] {full_claim.stem} ({elapsed:.0f}s)",
            file=sys.stderr,
        )

        # Emit. First-time: emit_attribute creates the link + sidecar.
        # Subsequent: register_version advances the description chain;
        # write the new content to the sidecar file.
        if sidecar_addr is None:
            emit_attribute(session, claim_path, "description", new_desc)
        else:
            session.register_version(sidecar_addr)
            sidecar_path = session.get_path_for_addr(sidecar_addr)
            full_sidecar = session.store.lattice_dir / sidecar_path
            body = new_desc if new_desc.endswith("\n") else new_desc + "\n"
            full_sidecar.write_text(body)

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
