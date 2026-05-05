"""Shared utilities for Alloy verification pipeline."""

import json
import re
import shutil
import subprocess
import sys
import time

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.shared.invoke_claude import invoke_claude_agent
from lib.shared.paths import WORKSPACE, ALLOY_DIR, USAGE_LOG, sanitize_filename
from lib.shared.common import read_file

ALLOY_JAR_DEFAULT = (
    "/Applications/Alloy.app/Contents/Resources/org.alloytools.alloy.dist.jar"
)
COMMIT_SCRIPT = WORKSPACE / "scripts" / "commit.py"


def invoke_claude(prompt, out_path, model="opus", effort=None,
                  max_turns=12, write_instruction=None,
                  tools="Read,Write,Bash"):
    """Call claude -p in agent mode to generate a file.

    Default tools include Bash so the agent can self-check Alloy models.
    Returns (success, elapsed, cost).
    """
    if write_instruction:
        full_prompt = f"""{prompt}

{write_instruction}: {out_path}
"""
    else:
        full_prompt = f"""{prompt}

Write the complete Alloy model to: {out_path}
"""

    response = invoke_claude_agent(
        full_prompt,
        model=model,
        effort=effort or "high",
        tools=tools,
        enabled_tools=tools,
        max_turns=max_turns,
    )

    if response.ok:
        usage = response.usage
        print(
            f"  [{response.elapsed:.0f}s] "
            f"in:{usage['input_tokens']} out:{usage['output_tokens']} "
            f"${response.cost:.4f}",
            file=sys.stderr,
        )
        # Log subtype on failure (e.g., error_max_turns)
        subtype = (response.data or {}).get("subtype", "")
        if subtype and subtype != "success":
            print(f"  [WARN] stop: {subtype}", file=sys.stderr)

    return response.ok, response.elapsed, response.cost


def log_usage(asn_label, llm_elapsed, alloy_elapsed, has_counterexample,
              claim_label=None, cost=0.0, model=None):
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
        if claim_label:
            entry["claim"] = claim_label
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


def cleanup_claim_artifacts(als_path):
    """Remove Alloy build artifacts for a single claim.

    Alloy creates a subdirectory named after the .als file (without extension)
    for counterexample output. Remove it after each claim check.
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
    """Create a result dict for a claim."""
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
    print(f"  {asn_label} Alloy Check ({len(results)} claims)",
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
