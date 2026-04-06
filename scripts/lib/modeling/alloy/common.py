"""Shared utilities for Alloy modeling pipeline."""

import json
import os
import re
import shutil
import subprocess
import sys
import time

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.shared.paths import WORKSPACE, ALLOY_DIR, USAGE_LOG, sanitize_filename

ALLOY_JAR_DEFAULT = (
    "/Applications/Alloy.app/Contents/Resources/org.alloytools.alloy.dist.jar"
)
COMMIT_SCRIPT = WORKSPACE / "scripts" / "commit.py"


def read_file(path):
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


def invoke_claude(prompt, out_path, model="opus", effort=None,
                  max_turns=12, write_instruction=None,
                  tools="Read,Write,Bash"):
    """Call claude -p in agent mode to generate a file.

    Default tools include Bash so the agent can self-check Alloy models.
    Returns (success, elapsed, cost).
    """
    model_flag = {
        "opus": "claude-opus-4-6",
        "sonnet": "claude-sonnet-4-6",
    }.get(model, model)

    cmd = [
        "claude", "-p",
        "--model", model_flag,
        "--output-format", "json",
        "--max-turns", str(max_turns),
        "--tools", tools,
        "--allowedTools", tools,
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = effort or "high"

    if write_instruction:
        full_prompt = f"""{prompt}

{write_instruction}: {out_path}
"""
    else:
        full_prompt = f"""{prompt}

Write the complete Alloy model to: {out_path}
"""

    start = time.time()
    result = subprocess.run(
        cmd, input=full_prompt, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE), timeout=None,
    )
    elapsed = time.time() - start

    cost = 0.0
    if result.returncode != 0:
        print(f"  FAILED (exit {result.returncode}, {elapsed:.0f}s)",
              file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:3]:
                print(f"    {line}", file=sys.stderr)
        return False, elapsed, cost

    # Parse JSON for usage stats
    try:
        data = json.loads(result.stdout)
        usage = data.get("usage", {})
        cost = data.get("total_cost_usd", 0) or 0.0
        inp = (usage.get("input_tokens", 0) +
               usage.get("cache_read_input_tokens", 0) +
               usage.get("cache_creation_input_tokens", 0))
        out = usage.get("output_tokens", 0)
        print(f"  [{elapsed:.0f}s] in:{inp} out:{out} ${cost:.4f}",
              file=sys.stderr)
        # Log subtype on failure (e.g., error_max_turns)
        subtype = data.get("subtype", "")
        if subtype and subtype != "success":
            print(f"  [WARN] stop: {subtype}", file=sys.stderr)
    except (json.JSONDecodeError, KeyError):
        print(f"  [{elapsed:.0f}s]", file=sys.stderr)

    return True, elapsed, cost


def log_usage(asn_label, llm_elapsed, alloy_elapsed, has_counterexample,
              prop_label=None, cost=0.0, model=None):
    """Append a usage entry to the log."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "check-alloy",
            "asn": asn_label,
            "llm_elapsed_s": round(llm_elapsed, 1),
            "alloy_elapsed_s": round(alloy_elapsed, 1),
            "counterexample": has_counterexample,
        }
        if prop_label:
            entry["property"] = prop_label
        if cost:
            entry["cost_usd"] = round(cost, 4)
        if model:
            entry["model"] = model
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def step_commit(hint=""):
    """Run commit.py."""
    print(f"\n  === COMMIT ===", file=sys.stderr)
    cmd = [sys.executable, str(COMMIT_SCRIPT)]
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


def cleanup_property_artifacts(als_path):
    """Remove Alloy build artifacts for a single property.

    Alloy creates a subdirectory named after the .als file (without extension)
    for counterexample output. Remove it after each property check.
    """
    artifact_dir = als_path.parent / als_path.stem
    if artifact_dir.is_dir():
        shutil.rmtree(artifact_dir)
        print(f"    [CLEANUP] {artifact_dir.name}/", file=sys.stderr)


def derive_output_name(asn_path):
    """ASN-0004-content-insertion.md -> ContentInsertion"""
    stem = Path(asn_path).stem
    name = re.sub(r"^ASN-\d+-", "", stem)
    return "".join(w.capitalize() for w in name.split("-"))


def next_run_number(asn_label):
    """Find the next Alloy modeling number for this ASN (independent of review numbers)."""
    existing = sorted((ALLOY_DIR / asn_label).glob("modeling-*"))
    if not existing:
        return 1
    nums = []
    for p in existing:
        m = re.search(r"modeling-(\d+)$", p.name)
        if m:
            nums.append(int(m.group(1)))
    return max(nums, default=0) + 1


def make_result(prop, out_dir):
    """Create a result dict for a property."""
    filename = sanitize_filename(prop["label"], prop["name"])
    return {
        "label": prop["label"],
        "name": prop["name"],
        "status": None,
        "model": None,
        "checks": 0,
        "llm_elapsed": 0.0,
        "alloy_elapsed": 0.0,
        "cost": 0.0,
        "als_path": out_dir / f"{filename}.als",
    }


def print_summary(asn_label, results):
    """Print a summary table to stderr."""
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"  {asn_label} Alloy Check ({len(results)} properties)",
          file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)

    STATUS_DISPLAY = {
        "pass": "pass",
        "counterexample": "COUNTEREXAMPLE",
        "syntax-error": "SYNTAX ERROR",
        "gen-fail": "GEN FAIL",
        "no-alloy": "no-alloy",
        "generated": "generated",
        "dry-run": "dry-run",
    }

    for r in results:
        status = STATUS_DISPLAY.get(r["status"], r["status"])
        checks_str = (f"{r['checks']} checks" if r["checks"]
                      else "")
        total = r["llm_elapsed"] + r["alloy_elapsed"]
        elapsed_str = f"{total:.0f}s" if total else ""
        cost = r.get("cost", 0)
        cost_str = f"${cost:.4f}" if cost else ""
        model_str = r.get("model", "") or ""
        detail = ", ".join(filter(None, [checks_str, elapsed_str, cost_str,
                                         model_str]))
        detail_str = f"  ({detail})" if detail else ""
        print(f"  {r['label']:<14s} {r['name']:<30s} {status}{detail_str}",
              file=sys.stderr)

    # Totals
    counts = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1

    total_cost = sum(r.get("cost", 0) for r in results)

    parts = []
    for status in ["pass", "syntax-error", "counterexample", "gen-fail",
                    "generated", "dry-run"]:
        if status in counts:
            parts.append(f"{STATUS_DISPLAY[status]}: {counts[status]}")
    parts.append(f"Total: {len(results)}")
    if total_cost:
        parts.append(f"${total_cost:.4f}")

    print(f"\n  {' | '.join(parts)}", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)
