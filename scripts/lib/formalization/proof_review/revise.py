"""
Proof Review reviser — applies proof fixes from findings.

Takes a property label and its finding text, builds a prompt from
revise.md, and runs claude -p with Edit tools to apply the fix.
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

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "formalization" / "proof-review"
REVISE_TEMPLATE = PROMPTS_DIR / "revise.md"


def revise(asn_num, label, finding_text):
    """Apply proof fix for a property. Returns True if changes made."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"    [REVISE] ASN not found", file=sys.stderr)
        return False

    template = REVISE_TEMPLATE.read_text()
    rel_path = asn_path.relative_to(WORKSPACE)
    prompt = (template
        .replace("{{asn_path}}", str(rel_path))
        .replace("{{label}}", label)
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

    print(f"  [REVISE] {label}...", end="", file=sys.stderr, flush=True)

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
            "skill": "proof-review-revise",
            "asn": asn_label,
            "property": label,
            "elapsed_s": round(elapsed, 1),
            "cost_usd": cost,
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass

    return True
