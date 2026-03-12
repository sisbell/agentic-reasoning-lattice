"""Shared utilities for pipeline scripts — extracted from duplicated definitions."""

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from paths import WORKSPACE, ASNS_DIR, USAGE_LOG


def read_file(path):
    """Read file, return '' on FileNotFoundError."""
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


def find_asn(asn_id, asns_dir=None):
    """Find ASN by number. Accepts 9, 09, 0009, ASN-0009, or full path.

    Returns (path, label).
    """
    path = Path(asn_id)
    if path.exists():
        label = re.match(r"(ASN-\d+)", path.stem)
        return path, label.group(1) if label else path.stem

    num = re.sub(r"[^0-9]", "", str(asn_id))
    if not num:
        return None, None
    label = f"ASN-{int(num):04d}"
    d = asns_dir or ASNS_DIR
    matches = sorted(d.glob(f"{label}-*.md"))
    if matches:
        return matches[0], label
    return None, label


def invoke_claude(prompt, *, model="opus", effort="max", tools=None):
    """Call claude --print (single-turn, no tools by default). Returns (text, elapsed)."""
    model_flag = {
        "opus": "claude-opus-4-6",
        "sonnet": "claude-sonnet-4-6",
    }.get(model, model)

    cmd = ["claude", "--print", "--model", model_flag, "--output-format", "json"]
    if tools is not None:
        cmd.extend(["--tools", tools])
    else:
        cmd.extend(["--tools", ""])

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env.setdefault("CLAUDE_CODE_MAX_OUTPUT_TOKENS", "128000")
    if effort:
        env["CLAUDE_CODE_EFFORT_LEVEL"] = effort

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        timeout=None,
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  FAILED (exit {result.returncode}, {elapsed:.0f}s)",
              file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:3]:
                print(f"    {line}", file=sys.stderr)
        return "", elapsed

    try:
        data = json.loads(result.stdout)
        text = data.get("result", "")
        print(f"  [{elapsed:.0f}s]", file=sys.stderr)
        return text, elapsed
    except (json.JSONDecodeError, KeyError):
        print(f"  [{elapsed:.0f}s]", file=sys.stderr)
        return result.stdout.strip(), elapsed


def invoke_claude_agent(prompt, *, model="opus", effort="max",
                        tools="Read,Write,Bash", max_turns=12, cwd=None):
    """Call claude -p (agent mode). Returns (json_data, elapsed)."""
    model_flag = {
        "opus": "claude-opus-4-6",
        "sonnet": "claude-sonnet-4-6",
    }.get(model, model)

    cmd = [
        "claude", "-p",
        "--model", model_flag,
        "--output-format", "json",
        "--max-turns", str(max_turns),
        "--allowedTools", tools,
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env.setdefault("CLAUDE_CODE_MAX_OUTPUT_TOKENS", "128000")
    if effort:
        env["CLAUDE_CODE_EFFORT_LEVEL"] = effort

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        cwd=str(cwd or WORKSPACE), timeout=None,
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  FAILED (exit {result.returncode}, {elapsed:.0f}s)",
              file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:5]:
                print(f"    {line}", file=sys.stderr)
        return None, elapsed

    try:
        data = json.loads(result.stdout)
        return data, elapsed
    except (json.JSONDecodeError, KeyError):
        print(f"  [{elapsed:.0f}s] [parse error]", file=sys.stderr)
        return None, elapsed


def log_usage(skill, elapsed, **extra):
    """Append JSONL usage entry to USAGE_LOG."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": skill,
            "elapsed_s": round(elapsed, 1),
        }
        entry.update(extra)
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def step_commit(hint=""):
    """Run commit.py via subprocess. Returns True if committed."""
    commit_script = WORKSPACE / "scripts" / "commit.py"
    cmd = [sys.executable, str(commit_script)]
    if hint:
        cmd.append(hint)

    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=str(WORKSPACE),
    )
    if result.returncode != 0:
        print(f"  [COMMIT] FAILED", file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:3]:
                print(f"    {line}", file=sys.stderr)
        return False

    if result.stderr:
        for line in result.stderr.strip().split("\n"):
            print(f"  {line}", file=sys.stderr)

    if result.stdout.strip():
        print(f"  {result.stdout.strip()}", file=sys.stderr)
    return True


def step_consult(asn_id, review_path):
    """Run review_consult.py via subprocess. Returns consultation path or None."""
    consult_script = WORKSPACE / "scripts" / "lib" / "review_consult.py"
    cmd = [sys.executable, str(consult_script), str(asn_id)]

    import re as _re
    review_name = Path(review_path).stem
    m = _re.search(r"(review-\d+)", review_name)
    if m:
        cmd.append(m.group(1))

    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=str(WORKSPACE),
    )
    if result.returncode != 0:
        print(f"  [CONSULT] FAILED", file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:5]:
                print(f"    {line}", file=sys.stderr)
        return None

    if result.stderr:
        for line in result.stderr.strip().split("\n"):
            print(f"  {line}", file=sys.stderr)

    consultation_path = result.stdout.strip()
    if consultation_path and Path(consultation_path).exists():
        return consultation_path
    return None


def step_revise(asn_id, consultation_path=None):
    """Run review_revise.py via subprocess. Returns (asn_path, converged)."""
    revise_script = WORKSPACE / "scripts" / "lib" / "review_revise.py"
    cmd = [sys.executable, str(revise_script), str(asn_id)]
    if consultation_path:
        cmd.extend(["--consultation", consultation_path])

    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=str(WORKSPACE),
    )

    converged = result.returncode == 2

    if result.returncode not in (0, 2):
        print(f"  [REVISE] FAILED", file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:5]:
                print(f"    {line}", file=sys.stderr)
        return None, False

    if result.stderr:
        for line in result.stderr.strip().split("\n"):
            print(f"  {line}", file=sys.stderr)

    asn_path = result.stdout.strip()
    if asn_path and Path(asn_path).exists():
        return asn_path, converged
    return None, False
