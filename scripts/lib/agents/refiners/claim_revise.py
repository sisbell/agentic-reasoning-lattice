"""Claim-revise agent — close a single open comment.revise on a claim.

Two layers in this file:

- `revise(asn_num, title, finding_text, *, claim_dir, comment_id,
   claim_path) -> bool` — the per-finding LLM worker. Builds a prompt
   from the revise template + finding text, invokes Claude with
   Edit/Write/Read tools, runs the resolution.py CLI to close the
   comment. Returns True if changes were applied.

- `ClaimReviseAgent` — substrate-aware shell. Fires once per
   unresolved comment.revise link, walks the comment to its finding
   and target claim, populates `revise()` args from substrate, and
   returns `AgentResult`. The runner picks each comment off via the
   claim-revise trigger (predicate: has_resolution skips resolved
   comments). One agent fire = one finding closed.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import ClassVar, Optional

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.protocols.febe.protocol import Session
from lib.lattice.labels import extract_label_digits, format_label
from lib.shared.common import find_asn, read_file
from lib.shared.paths import LATTICE, USAGE_LOG, WORKSPACE, prompt_path
from lib.shared.prompts import read_prompt


REVISE_TEMPLATE = prompt_path("agents/refiners/claim_revise.md")


def revise(
    asn_num: int,
    title: str,
    finding_text: str,
    claim_base_dir: Path,
    comment_id: Optional[str] = None,
    claim_path: Optional[str] = None,
) -> bool:
    """Apply fix for one finding. Returns True if changes made.

    `comment_id` is passed through to the reviser via
    PROTOCOL_COMMENT_ID so the agent can call
    `scripts/agent_tools/resolution.py` to close the comment.
    When None, the agent can still run but won't be able to invoke
    resolution.py — callers that care about
    resolution links should pass it.

    `claim_path` is retained for backwards compatibility with the
    call sites' wiring; it's no longer passed through to the reviser
    (the reviser-side CLIs now resolve doc addresses from labels via
    the claim path convention, never from ambient path strings).
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return False

    claim_dir = claim_base_dir / asn_label

    template = read_prompt(REVISE_TEMPLATE)
    rel_path = claim_dir.relative_to(WORKSPACE)

    prompt = (
        template
        .replace("{{claim_dir}}", str(rel_path))
        .replace("{{label}}", title)
        .replace("{{finding}}", finding_text)
    )

    cmd = [
        "claude", "-p",
        "--model", "claude-opus-4-8[1m]",
        "--output-format", "json",
        "--allowedTools", "Edit,Write,Read,Glob,Grep,Bash",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = "max"
    if comment_id:
        env["PROTOCOL_COMMENT_ID"] = comment_id
        env["PROTOCOL_ASN_LABEL"] = asn_label

    print(f"  [REVISE] {title}...", end="", file=sys.stderr, flush=True)

    start = time.time()
    try:
        result = subprocess.run(
            cmd, input=prompt, capture_output=True, text=True, env=env,
            cwd=str(WORKSPACE), timeout=None,
        )
    except subprocess.TimeoutExpired:
        print(" timeout", file=sys.stderr)
        return False

    elapsed = time.time() - start

    if result.returncode != 0:
        print(f" failed ({elapsed:.0f}s)", file=sys.stderr)
        return False

    cost = 0
    try:
        data = json.loads(result.stdout)
        cost = data.get("total_cost_usd", 0)
    except (json.JSONDecodeError, KeyError):
        pass

    print(f" done ({elapsed:.0f}s, ${cost:.2f})", file=sys.stderr)

    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "full-review-revise",
            "asn": asn_label,
            "finding": title,
            "elapsed_s": round(elapsed, 1),
            "cost_usd": cost,
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass

    return True


# ---------------------------------------------------------------------------
# Trigger-runner entry: class form


class ClaimReviseAgent(Agent):
    """One Claude-with-tools invocation that closes a single open
    `comment.revise` on a claim.

    Fires per unresolved comment.revise link. Walks the comment to
    find the finding doc (from_set) and the target claim (to_set),
    reads the finding body, populates `revise()` args from substrate,
    and dispatches the per-finding worker.
    """

    role: ClassVar[str] = "claim-revise"
    node: ClassVar[str] = "1.3"

    def run(self, session: Session, comment_addr: Address) -> AgentResult:
        try:
            comment = session.get_link(comment_addr)
        except KeyError:
            return AgentResult(success=False, detail="no-comment-link")

        if not comment.from_set or not comment.to_set:
            return AgentResult(success=False, detail="malformed-comment")

        finding_addr = comment.from_set[0]
        claim_addr = comment.to_set[0]

        finding_rel = session.get_path_for_addr(finding_addr)
        if finding_rel is None:
            return AgentResult(success=False, detail="no-finding-path")
        finding_full = LATTICE / finding_rel
        if not finding_full.exists():
            return AgentResult(success=False, detail="no-finding-file")
        finding_body = finding_full.read_text().strip()
        first_line = finding_body.splitlines()[0] if finding_body else ""
        title = re.sub(r"^#+\s*", "", first_line).strip() or "(untitled)"

        claim_rel = session.get_path_for_addr(claim_addr)
        if claim_rel is None:
            return AgentResult(success=False, detail="no-claim-path")
        digits = extract_label_digits(claim_rel)
        if digits is None:
            return AgentResult(success=False, detail="no-asn-in-claim-path")
        asn_num = int(digits)

        ok = revise(
            asn_num, title, finding_body, self.claim_dir,
            comment_id=str(comment_addr),
            claim_path=claim_rel,
        )
        if not ok:
            return AgentResult(
                success=False, detail=f"revise-failed comment={comment_addr}",
            )

        # Advance the claim's version chain iff the reviser accepted.
        # resolution.py used to do this per-accept; lifecycle now lives
        # in the refiner. claim_revise fires per-comment so accept is
        # binary (this comment is closed via resolution.edit or not),
        # but we keep the structural check for clarity and symmetry
        # with note_revise.
        if session.active_links("resolution.edit", to_set=[comment_addr]):
            session.register_version(claim_addr)

        return AgentResult(
            success=True, detail=f"closed comment={comment_addr}",
        )
