"""Contract validation — review Alloy model against formal contract."""

import os
import re
import subprocess
import sys
import time

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.shared.paths import WORKSPACE

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "modeling" / "alloy"
CONTRACT_REVIEW_TEMPLATE = PROMPTS_DIR / "validate-contract.md"


def validate(alloy_source, formal_contract, label):
    """Review a single Alloy property against its formal contract.

    Returns (result, reason, elapsed) where result is 'clean' or 'flag'.
    """
    template = CONTRACT_REVIEW_TEMPLATE.read_text()
    prompt = (template
              .replace("{{alloy_source}}", alloy_source)
              .replace("{{formal_contract}}", formal_contract))

    cmd = [
        "claude", "--print", "--model", "claude-opus-4-7",
    ]
    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = "high"

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        return "error", f"opus failed ({elapsed:.0f}s)", elapsed

    text = result.stdout.strip()
    text = re.sub(r'```\s*', '', text).strip()

    # Find the CLEAN or FLAG line anywhere in output
    lines = text.split("\n")
    for i, line in enumerate(lines):
        line = line.strip()
        m = re.match(r'^(CLEAN|FLAG)\s*\|\s*(.*)', line, re.IGNORECASE)
        if m:
            rec = m.group(1).lower()
            # For FLAG: capture summary + everything after as detail
            summary = m.group(2).strip()
            detail = "\n".join(lines[i + 1:]).strip()
            reason = f"{summary}\n\n{detail}".strip() if detail else summary
            return rec, reason, elapsed

    # Fallback
    if "|" in text:
        parts = text.split("|", 1)
        return parts[0].strip().lower(), parts[1].strip(), elapsed

    return text.strip().lower(), "", elapsed
