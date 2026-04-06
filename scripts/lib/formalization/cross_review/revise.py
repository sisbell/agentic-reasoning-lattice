"""
Cross-cutting Review reviser — applies fixes from findings.

Takes a finding title and text, builds a prompt from the revise template,
and runs claude -p with Edit tools to apply the fix.
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
from lib.shared.common import find_asn, read_file

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "formalization" / "cross-review"
REVISE_TEMPLATE = PROMPTS_DIR / "revise.md"


def revise(asn_num, title, finding_text):
    """Apply fix for one finding. Returns True if changes made."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return False

    template = read_file(REVISE_TEMPLATE)
    rel_path = asn_path.relative_to(WORKSPACE)

    # The finding may not have a single label — use the title
    prompt = (template
        .replace("{{asn_path}}", str(rel_path))
        .replace("{{label}}", title)
        .replace("{{finding}}", finding_text))

    cmd = [
        "claude", "-p",
        "--model", "claude-opus-4-6",
        "--output-format", "json",
        "--allowedTools", "Edit,Read,Glob,Grep",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = "max"

    print(f"  [REVISE] {title}...", end="", file=sys.stderr, flush=True)

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
            "skill": "cross-review-revise",
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
