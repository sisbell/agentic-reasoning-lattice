"""Structural-rule-fix agent body.

Two entry points:

- `fix_structural_rule(rule, file_path, findings, metadata_bundle, *, tools)`:
  apply mode. Invokes Claude with Edit tools on `file_path` (a
  scratch copy the orchestrator owns). Claude edits the file in
  place; the agent returns transcript + timing. The orchestrator is
  responsible for the scratch/diff/apply dance.

- `propose_structural_fix(rule, findings, claim_dir, *, tools)`:
  propose mode. Invokes Claude with Read-only tools; returns a
  proposal document. Used for rules where automatic fixes aren't
  safe (acyclic-depends).

Both take a pre-built `metadata_bundle` from the orchestrator (the
substrate queries that produce it live in the orchestrator, not in
the agent — the agent just renders the bundle into its prompt).
"""

from __future__ import annotations

from pathlib import Path
from typing import List, NamedTuple, Optional

from lib.shared.common import invoke_claude_agent


REPO_ROOT = Path(__file__).resolve().parents[4]
PROMPT_DIR = (
    REPO_ROOT / "prompts" / "shared" / "claim-convergence" / "validate-revise"
)


class StructuralRuleFixResult(NamedTuple):
    """Apply-mode agent output."""
    transcript: str
    elapsed_seconds: float
    agent_failed: bool


def fix_structural_rule(
    rule: str,
    file_path: Path,
    findings: list,
    metadata_bundle: str,
    *,
    tools: str,
    model: str = "opus",
    effort: str = "max",
    max_turns: int = 20,
) -> StructuralRuleFixResult:
    """Apply mode: invoke Claude with Edit tools to fix a per-rule violation.

    Claude reads `findings` + `metadata_bundle` and edits `file_path`
    in place. The caller (orchestrator) is responsible for copying
    the real file to a scratch path before this call and diffing
    after.

    For depends-agreement specifically, Claude also writes a
    `__decisions.json` sidecar in `file_path.parent` describing
    ADD/RETRACT/SKIP decisions per label; that contract is checked
    by the orchestrator's `parse_decisions`.
    """
    prompt = _render_prompt(
        rule, file_path, findings, metadata_bundle,
    )
    data, elapsed = invoke_claude_agent(
        prompt, model=model, effort=effort, tools=tools,
        max_turns=max_turns, cwd=file_path.parent,
    )
    if data is None:
        return StructuralRuleFixResult(
            transcript="", elapsed_seconds=elapsed, agent_failed=True,
        )
    return StructuralRuleFixResult(
        transcript=data.get("result", "") or "",
        elapsed_seconds=elapsed,
        agent_failed=False,
    )


def propose_structural_fix(
    rule: str,
    findings: list,
    claim_dir: Path,
    *,
    tools: str = "Read",
    model: str = "opus",
    effort: str = "max",
    max_turns: int = 10,
) -> Optional[str]:
    """Propose mode: invoke Claude Read-only; return a proposal document.

    Used for rules where automatic fixes aren't safe — the agent
    suggests, the operator decides. Returns the agent's text output
    (the proposal), or None on invocation failure.
    """
    template = _read_template(rule)
    prompt = (
        template
        .replace("{findings_list}", _format_findings(findings))
        .replace("{claim_dir}", str(claim_dir))
        .replace("{metadata_bundle}", "")
    )
    data, elapsed = invoke_claude_agent(
        prompt, model=model, effort=effort, tools=tools,
        max_turns=max_turns, cwd=claim_dir,
    )
    if data is None:
        return None
    return data.get("result", "")


# ---------------------------------------------------------------------------
# Prompt rendering


def _read_template(rule: str) -> str:
    template_path = PROMPT_DIR / f"{rule}.md"
    if not template_path.exists():
        raise FileNotFoundError(f"missing prompt template: {template_path}")
    return template_path.read_text()


def _format_findings(findings: List[dict]) -> str:
    lines = []
    for f in findings:
        loc = f" (line {f['line']})" if f["line"] else ""
        src = f" [{f['file']}]" if f.get("file") else ""
        lines.append(f"- {f['detail']}{src}{loc}")
    return "\n".join(lines)


def _render_prompt(
    rule: str, file_path: Path, findings: list, metadata_bundle: str,
) -> str:
    template = _read_template(rule)
    return (
        template
        .replace("{file_path}", str(file_path))
        .replace("{findings_list}", _format_findings(findings))
        .replace("{metadata_bundle}", metadata_bundle)
    )
