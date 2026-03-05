#!/usr/bin/env python3
"""
Generate a Dafny specification module from an ASN's extracted properties.

Takes the extract (formal properties + definitions with Dafny metadata)
and vocabulary, then produces a verified Dafny module.

Requires: extract file in vault/formalization/extracts/ (run extract-properties.py first)

Usage:
    python scripts/generate-dafny.py 4
    python scripts/generate-dafny.py ASN-0001 --dry-run
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time

from pathlib import Path

from paths import WORKSPACE, EXTRACTS_DIR, DAFNY_DIR, ALLOY_DIR, VOCABULARY, USAGE_LOG

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "formalization"
TEMPLATE = PROMPTS_DIR / "generate-dafny.md"


def read_file(path):
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


def find_extract(asn_id):
    """Find extract file by ASN number."""
    num = re.sub(r"[^0-9]", "", str(asn_id))
    if not num:
        return None, None
    label = f"ASN-{int(num):04d}"
    extract_path = EXTRACTS_DIR / f"{label}-extract.md"
    if extract_path.exists():
        return extract_path, label
    return None, label


def find_alloy_models(asn_label):
    """Find Alloy .als files from the latest run directory for an ASN."""
    asn_dir = ALLOY_DIR / asn_label
    if not asn_dir.exists():
        return []

    # Find highest-numbered modeling-* directory
    run_dirs = sorted(asn_dir.glob("modeling-*"), key=lambda p: int(p.name.split("-")[1]))
    if not run_dirs:
        return []

    latest = run_dirs[-1]
    print(f"  Alloy models: {latest.relative_to(WORKSPACE)}", file=sys.stderr)

    models = []
    for als in sorted(latest.glob("*.als")):
        models.append((als.name, als.read_text()))
    return models


def format_alloy_section(models):
    """Format Alloy models as markdown for prompt injection."""
    parts = []
    for filename, content in models:
        parts.append(f"### {filename}\n\n```alloy\n{content}\n```")
    return "\n\n---\n\n".join(parts)


def build_prompt(extract, vocabulary, alloy_content=""):
    """Assemble Dafny generation prompt from template + injected content."""
    template = read_file(TEMPLATE)
    if not template:
        print("  Prompt template not found at scripts/prompts/generate-dafny.md",
              file=sys.stderr)
        sys.exit(1)

    # Handle {{#if alloy_models}} conditional
    if alloy_content:
        template = re.sub(r"\{\{#if alloy_models\}\}", "", template)
        template = re.sub(r"\{\{/if\}\}", "", template, count=1)
    else:
        template = re.sub(
            r"\{\{#if alloy_models\}\}.*?\{\{/if\}\}", "", template,
            flags=re.DOTALL, count=1)

    return template.replace(
        "{{alloy_models}}", alloy_content
    ).replace(
        "{{extract}}", extract
    ).replace(
        "{{vocabulary}}", vocabulary
    )



def invoke_claude(prompt, out_path, model="opus", effort="max"):
    """Call claude -p with Write tool to generate the .dfy file directly."""
    model_flag = {
        "opus": "claude-opus-4-6",
        "sonnet": "claude-sonnet-4-6",
    }.get(model, model)

    cmd = [
        "claude", "-p",
        "--model", model_flag,
        "--output-format", "json",
        "--max-turns", "8",
        "--tools", "Read,Write",
        "--allowedTools", "Read,Write",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    if effort:
        env["CLAUDE_CODE_EFFORT_LEVEL"] = effort

    full_prompt = f"""{prompt}

Write the complete Dafny module to: {out_path}
"""

    start = time.time()
    result = subprocess.run(
        cmd, input=full_prompt, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE), timeout=None,
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  FAILED (exit {result.returncode}, {elapsed:.0f}s)",
              file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:3]:
                print(f"    {line}", file=sys.stderr)
        return False, elapsed

    # Parse JSON for usage stats
    try:
        data = json.loads(result.stdout)
        usage = data.get("usage", {})
        cost = data.get("total_cost_usd", 0)
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

    return True, elapsed


def log_usage(asn_label, elapsed):
    """Append a usage entry to the log."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "generate-dafny",
            "asn": asn_label,
            "elapsed_s": round(elapsed, 1),
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def main():
    parser = argparse.ArgumentParser(
        description="Generate Dafny specification from ASN extract")
    parser.add_argument("asn",
                        help="ASN number (e.g., 4, 0004, ASN-0004)")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"],
                        help="Model (default: opus)")
    parser.add_argument("--effort", default="max",
                        help="Thinking effort level (low/medium/high/max)")
    parser.add_argument("--with-alloy", action="store_true",
                        help="Inject Alloy models as conceptual reference")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show prompt size without invoking Claude")
    args = parser.parse_args()

    # Find extract
    extract_path, asn_label = find_extract(args.asn)
    if extract_path is None:
        print(f"  No extract found for {args.asn} in vault/formalization/extracts/",
              file=sys.stderr)
        print(f"  Run: python scripts/extract-properties.py {args.asn}",
              file=sys.stderr)
        sys.exit(1)

    extract = extract_path.read_text()

    # Read vocabulary
    vocabulary = read_file(VOCABULARY)
    if not vocabulary:
        print("  Warning: vault/modeling/vocabulary.md not found", file=sys.stderr)

    # Alloy reference models (optional)
    alloy_content = ""
    if args.with_alloy:
        models = find_alloy_models(asn_label)
        if models:
            alloy_content = format_alloy_section(models)
            print(f"  Alloy: {len(models)} models ({len(alloy_content) // 1024}KB)",
                  file=sys.stderr)
        else:
            print(f"  Warning: --with-alloy but no models found for {asn_label}",
                  file=sys.stderr)

    # Build prompt
    print(f"  [DAFNY] {asn_label}", file=sys.stderr)
    prompt = build_prompt(extract, vocabulary, alloy_content)
    print(f"  Prompt: {len(prompt) // 1024}KB (~{len(prompt) // 4} tokens est.)",
          file=sys.stderr)

    # Output path
    DAFNY_DIR.mkdir(parents=True, exist_ok=True)
    out_path = DAFNY_DIR / f"{asn_label}.dfy"

    if args.dry_run:
        print(f"  [DRY RUN] Would invoke {args.model} with -p --allowedTools Write",
              file=sys.stderr)
        print(f"  [DRY RUN] Output: {out_path}", file=sys.stderr)
        return

    # Invoke Claude — writes the .dfy file directly
    success, elapsed = invoke_claude(prompt, out_path,
                                     model=args.model, effort=args.effort)

    if not success or not out_path.exists():
        print("  No Dafny code generated", file=sys.stderr)
        sys.exit(1)

    # Log usage
    log_usage(asn_label, elapsed)

    # Print output file path to stdout (for pipeline consumption)
    print(str(out_path))

    print(f"  [WROTE] {out_path.relative_to(WORKSPACE)}", file=sys.stderr)


if __name__ == "__main__":
    main()
