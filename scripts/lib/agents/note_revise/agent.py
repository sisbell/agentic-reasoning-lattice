"""Note-revise agent body.

One LLM invocation: assemble a discovery-methodology prompt with
per-finding instructions, invoke Claude with Edit/Read/Bash/etc.
tools, return the parsed JSON result.

Public entry: `run_revise_pass(asn_path, asn_label, findings, *,
model, effort, consultation_content) -> (data, elapsed)`. Returns
None on invocation failure.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

from lib.shared.campaign import resolve_campaign
from lib.shared.common import read_file
from lib.shared.foundation import load_foundation_for_note
from lib.shared.paths import LATTICE, LATTICE_PROMPTS, WORKSPACE


PROMPTS_DIR = LATTICE_PROMPTS / "discovery"
DISCOVERY_PROMPT = PROMPTS_DIR / "instructions.md"

MODEL = "claude-opus-4-7"


def run_revise_pass(
    asn_path: Path,
    asn_label: str,
    findings: list,
    *,
    model: str = "opus",
    effort: str = "max",
    consultation_content=None,
):
    """Run one reviser invocation that addresses `findings`.

    Sets PROTOCOL_ASN_LABEL env var. The agent closes each comment via
    `convergence-link-resolution.py --comment-id <id>` per the prompt.
    Returns (data, elapsed) from the underlying Claude call — caller
    logs usage and re-queries the substrate for remaining open revises.
    """
    asn_num = int(re.sub(r"[^0-9]", "", asn_label))
    vocab = read_file(resolve_campaign(asn_label).vocabulary_path)

    prompt = build_prompt(
        asn_path, findings, vocab, consultation_content,
        asn_number=asn_num,
    )
    print(
        f"  Prompt: {len(prompt) // 1024}KB (~{len(prompt) // 4} tokens)",
        file=sys.stderr,
    )

    model_flag = {
        "opus": "claude-opus-4-7",
        "sonnet": "claude-sonnet-4-6",
    }.get(model, model)

    os.environ["PROTOCOL_ASN_LABEL"] = asn_label

    return _invoke_claude(prompt, model=model_flag, effort=effort)


def build_prompt(
    asn_path: Path,
    findings: list,
    vocab: str,
    consultation_content=None,
    asn_number=None,
) -> str:
    """Build revise prompt: discovery methodology + per-finding instructions.

    `findings` is a list of (comment_id, title, body) tuples — one per
    open `comment.revise` link on the note. The agent is instructed to
    address each in the note md and call convergence-link-resolution.py
    per finding to close the comment in the substrate.
    """
    skill_body = read_file(DISCOVERY_PROMPT)
    if not skill_body:
        print(
            f"  Discovery prompt not found at "
            f"{DISCOVERY_PROMPT.relative_to(WORKSPACE)}",
            file=sys.stderr,
        )
        sys.exit(1)

    parts = [skill_body]

    if vocab:
        parts.append(f"## Shared Vocabulary\n\n{vocab}")

    foundation = load_foundation_for_note(asn_path, asn_number)
    if foundation:
        parts.append(foundation)

    rel_path = asn_path.relative_to(WORKSPACE)
    asn_label = re.match(r"(ASN-\d+)", asn_path.stem).group(1)

    assignment = f"""## Your Assignment: REVISE {asn_label}

You are revising an existing ASN based on per-finding review feedback.
Read the ASN at `{rel_path}`, then address each finding below.

**Do not rewrite the ASN from scratch.** Make targeted fixes per finding.
Preserve the existing structure, notation, and reasoning where it is not
affected by the finding.

Write the revised ASN back to `{rel_path}`.

For each finding below, after you have addressed it (either by editing
the note or by deciding the finding is incorrect), close the
corresponding comment in the link store:

  python scripts/convergence-link-resolution.py accept --comment-id <id>
  python scripts/convergence-link-resolution.py reject --comment-id <id> --rationale "<one or two sentences>"

`accept` means you applied the fix; `reject` means the finding is
incorrect and you wrote a rationale instead. Do this once per finding."""

    if consultation_content:
        assignment += f"""

## Consultation Results

The following expert consultations were conducted based on the review.
Use these answers as evidence when addressing the corresponding findings.

{consultation_content}"""

    assignment += "\n\n## Findings\n"
    for n, (comment_id, title, body) in enumerate(findings, 1):
        assignment += (
            f"\n### Finding {n}: {title}\n"
            f"**Comment ID:** `{comment_id}`\n\n"
            f"{body}\n"
        )

    parts.append(assignment)
    return "\n\n".join(parts)


def _invoke_claude(prompt: str, *, model: str, effort: str):
    """Run claude -p with tools. Returns (data, elapsed) — data is
    the parsed JSON dict, or None on failure."""
    cmd = [
        "claude", "-p",
        "--model", model,
        "--output-format", "json",
        "--allowedTools", "Edit,Bash,Write,Read,Glob,Grep",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = effort

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE),
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(
            f"  FAILED (exit {result.returncode}, {elapsed:.0f}s)",
            file=sys.stderr,
        )
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:5]:
                print(f"    {line}", file=sys.stderr)
        return None, elapsed

    try:
        data = json.loads(result.stdout)
        usage = data.get("usage", {})
        cost = data.get("total_cost_usd", 0)
        inp = (
            usage.get("input_tokens", 0)
            + usage.get("cache_read_input_tokens", 0)
            + usage.get("cache_creation_input_tokens", 0)
        )
        out = usage.get("output_tokens", 0)
        num_turns = data.get("num_turns", 0)

        print(
            f"  [{elapsed:.0f}s] in:{inp} out:{out} turns:{num_turns} "
            f"${cost:.4f}",
            file=sys.stderr,
        )

        return data, elapsed
    except (json.JSONDecodeError, KeyError):
        print(f"  [{elapsed:.0f}s] [parse error]", file=sys.stderr)
        return None, elapsed
