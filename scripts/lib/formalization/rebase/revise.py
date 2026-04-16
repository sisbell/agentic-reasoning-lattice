"""
Dependency Rebase reviser — applies fixes from findings.

Takes a property label and its findings, builds a prompt from the
revise template, and runs claude -p with Edit tools to apply the fix.
"""

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import WORKSPACE, USAGE_LOG
from lib.shared.common import find_asn
from lib.formalization.core.finding import Finding

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "rebase"
REVISE_TEMPLATE = PROMPTS_DIR / "revise.md"


def format_finding_for_reviser(findings):
    """Format one or more findings into text for the reviser prompt."""
    parts = []
    for f in findings:
        parts.append(
            f"**[{f.category}]** (location: {f.location})\n\n"
            f"**Problem**: {f.detail}\n\n"
            f"**Required**: Fix the {f.category} issue — "
            f"{'update the reference to use the canonical upstream label' if f.category == 'stale-label' else ''}"
            f"{'add the missing dependency to the property table' if f.category == 'missing-dep' else ''}"
            f"{'add the ASN to the depends list in project.yaml' if f.category == 'undeclared-asn' else ''}"
            f"{'add the label to the follows_from list in the property table' if f.category == 'prose-only' else ''}"
            f"{f.detail if f.category in ('cross-ref', 'extension-gap') else ''}"
        )
    return "\n\n---\n\n".join(parts)


def revise(asn_num, label, findings):
    """Apply fixes for a property's findings. Returns True if changes made."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"    [REVISE] ASN not found", file=sys.stderr)
        return False

    finding_text = format_finding_for_reviser(findings)

    template = REVISE_TEMPLATE.read_text()
    rel_path = asn_path.relative_to(WORKSPACE)
    prompt = (template
        .replace("{{asn_path}}", str(rel_path))
        .replace("{{report}}", finding_text))

    cmd = [
        "claude", "-p",
        "--model", "claude-opus-4-7",
        "--output-format", "json",
        "--allowedTools", "Edit,Read,Glob,Grep",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = "max"

    print(f"    [{label}]", end="", file=sys.stderr, flush=True)

    start = time.time()
    try:
        result = subprocess.run(
            cmd, input=prompt, capture_output=True, text=True, env=env,
            cwd=str(WORKSPACE), timeout=None,
        )
    except subprocess.TimeoutExpired:
        print(f" timeout", file=sys.stderr)
        return False

    elapsed = time.time() - start

    if result.returncode != 0:
        print(f" failed ({elapsed:.0f}s)", file=sys.stderr)
        return False

    # Parse cost
    cost = 0
    try:
        data = json.loads(result.stdout)
        cost = data.get("total_cost_usd", 0)
    except (json.JSONDecodeError, KeyError):
        pass

    print(f" done ({elapsed:.0f}s, ${cost:.2f})", file=sys.stderr)

    # Log usage
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "rebase-revise",
            "asn": asn_label,
            "property": label,
            "findings": len(findings),
            "elapsed_s": round(elapsed, 1),
            "cost_usd": cost,
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass

    return True
