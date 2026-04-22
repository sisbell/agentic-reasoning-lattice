"""
Local Review reviser — applies proof fixes from findings.

Takes a claim label and its finding text, builds a prompt from
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
from lib.shared.paths import WORKSPACE, USAGE_LOG, prompt_path
from lib.shared.common import find_asn

REVISE_TEMPLATE = prompt_path("formalization/local-review/revise.md")


def revise(asn_num, label, finding_text, claim_path=None):
    """Apply proof fix for a claim. Returns True if changes made."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"    [REVISE] ASN not found", file=sys.stderr)
        return False

    # Use claim file path if provided, otherwise fall back to ASN path
    if claim_path is None:
        from lib.shared.paths import FORMALIZATION_DIR
        claim_path = FORMALIZATION_DIR / asn_label / (label.replace("(", "").replace(")", "") + ".md")

    template = REVISE_TEMPLATE.read_text()
    rel_path = claim_path.relative_to(WORKSPACE)
    prompt = (template
        .replace("{{asn_path}}", str(rel_path))
        .replace("{{label}}", label)
        .replace("{{finding}}", finding_text))

    cmd = [
        "claude", "-p",
        "--model", "claude-opus-4-7",
        "--output-format", "json",
        "--allowedTools", "Edit,Write,Read,Glob,Grep",
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
            "skill": "local-review-revise",
            "asn": asn_label,
            "claim": label,
            "elapsed_s": round(elapsed, 1),
            "cost_usd": cost,
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass

    return True
