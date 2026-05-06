"""LLM-call helper for the structural-rule-fix refiner.

Single entry point:

- `fix_structural_rule(rule, file_path, findings, metadata_bundle, *, tools)`:
  apply mode. Invokes Claude with Edit tools on `file_path` (a
  scratch copy the Agent owns). Claude edits the file in place; the
  helper returns transcript + timing. The Agent class
  (`ClaimStructuralFixAgent`) handles the scratch/diff/apply dance
  around this call.

The `metadata_bundle` is built by the Agent class from substrate
(label · name pairs for the claim and its dependencies); this helper
just renders it into the prompt template.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, NamedTuple

from lib.shared.invoke_claude import invoke_claude_agent


REPO_ROOT = Path(__file__).resolve().parents[4]
PROMPT_DIR = (
    REPO_ROOT / "prompts" / "shared" / "claim-refinement" / "validate-revise"
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
    response = invoke_claude_agent(
        prompt, model=model, effort=effort, tools=tools,
        max_turns=max_turns, cwd=file_path.parent,
    )
    if response.data is None:
        return StructuralRuleFixResult(
            transcript="", elapsed_seconds=response.elapsed, agent_failed=True,
        )
    return StructuralRuleFixResult(
        transcript=response.text,
        elapsed_seconds=response.elapsed,
        agent_failed=False,
    )


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
