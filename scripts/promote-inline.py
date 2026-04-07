#!/usr/bin/env python3
"""
Promote Inline — extract embedded results to standalone properties.

Operates on per-property blueprint files. For each flagged property:
1. Promote: rewrite narrative, create new property section in the file
2. Format: review/revise fixes labels, headers on the new section
3. Disassemble: split the file into separate property files

Run `python scripts/lint.py inline 34` first to identify candidates.

Usage:
    python scripts/promote-inline.py 34              # promote all flagged
    python scripts/promote-inline.py 34 --label T10a # single property
    python scripts/promote-inline.py 34 --dry-run    # show what would be promoted
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import (
    WORKSPACE, USAGE_LOG,
    blueprint_properties_dir,
)
from lib.shared.common import find_asn, invoke_claude, step_commit_asn
from lib.blueprinting.lint import _extract_post_contract, _scan_property_file

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "blueprinting" / "promote-inline"
PROMOTE_TEMPLATE = PROMPTS_DIR / "promote.md"
DISASSEMBLE_TEMPLATE = WORKSPACE / "scripts" / "prompts" / "blueprinting" / "disassemble.md"


def _promote_one(prop_file, label, findings, vocabulary, table):
    """Promote inline results in one property file. Returns rewritten content."""
    template = PROMOTE_TEMPLATE.read_text()
    content = prop_file.read_text()

    results_text = "\n".join(
        f"- {r['kind']} | {r['label']} | {r['name']} | {r['description']}"
        for r in findings
    )

    prompt = (template
              .replace("{{content}}", content)
              .replace("{{vocabulary}}", vocabulary)
              .replace("{{table}}", table)
              .replace("{{results}}", results_text))

    print(f"  [PROMOTE] {label} — {len([r for r in findings if r['kind'] == 'derived'])} results...",
          file=sys.stderr)

    cmd = [
        "claude", "--print", "--model", "claude-opus-4-6",
        "--tools", "",
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
        print(f"    FAILED ({elapsed:.0f}s)", file=sys.stderr)
        return None, elapsed

    new_content = result.stdout.strip()
    if len(new_content) < len(content) * 0.5:
        print(f"    REJECTED (output too short)", file=sys.stderr)
        return None, elapsed

    print(f"    Done ({elapsed:.0f}s)", file=sys.stderr)
    return new_content, elapsed


def _format_one(prop_file):
    """Run format review/revise on a single property file. Returns True if clean."""
    from lib.blueprinting.format import step_format_review, step_format_revise

    content = prop_file.read_text()

    # Use format review prompt with file content (print mode)
    review_template = (WORKSPACE / "scripts" / "prompts" / "blueprinting"
                       / "format" / "review.md").read_text()
    prompt = review_template.replace("{{asn_content}}", content)

    cmd = ["claude", "--print", "--model", "claude-sonnet-4-6"]
    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = "high"

    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
    )

    if result.returncode != 0:
        return True  # skip format on failure

    text = result.stdout.strip()
    if "RESULT: CLEAN" in text:
        print(f"    [FORMAT] Clean", file=sys.stderr)
        return True

    # Has findings — run revise with agent tools
    revise_template = (WORKSPACE / "scripts" / "prompts" / "blueprinting"
                       / "format" / "revise.md").read_text()
    rel_path = prop_file.relative_to(WORKSPACE)
    revise_prompt = (revise_template
                     .replace("{{asn_path}}", str(rel_path))
                     .replace("{{findings}}", text))

    cmd = [
        "claude", "-p",
        "--model", "claude-sonnet-4-6",
        "--output-format", "json",
        "--allowedTools", "Edit,Read,Glob,Grep",
    ]
    env["CLAUDE_CODE_EFFORT_LEVEL"] = "high"

    result = subprocess.run(
        cmd, input=revise_prompt, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE),
    )

    if result.returncode == 0:
        print(f"    [FORMAT] Revised", file=sys.stderr)
    else:
        print(f"    [FORMAT] Revise failed", file=sys.stderr)

    return True


def _disassemble_one(prop_file, blueprint_dir):
    """Disassemble a property file that contains multiple properties into separate files."""
    content = prop_file.read_text()

    # Check if file actually has multiple property headers
    headers = re.findall(r'^\*\*\S+.*?\.\*\*', content, re.MULTILINE)
    if len(headers) <= 1:
        print(f"    [DISASSEMBLE] Single property — no split needed", file=sys.stderr)
        return []

    template = DISASSEMBLE_TEMPLATE.read_text()
    rel_dir = blueprint_dir.relative_to(WORKSPACE)

    prompt = (template
              .replace("{{asn_path}}", str(prop_file.relative_to(WORKSPACE)))
              .replace("{{output_dir}}", str(rel_dir)))

    print(f"    [DISASSEMBLE] {len(headers)} properties in file...",
          file=sys.stderr)

    cmd = [
        "claude", "-p",
        "--model", "claude-sonnet-4-6",
        "--output-format", "json",
        "--allowedTools", "Read,Write,Glob",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = "max"

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE),
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"    [DISASSEMBLE] FAILED ({elapsed:.0f}s)", file=sys.stderr)
        return []

    # Find new files created (files in blueprint_dir that weren't there before)
    new_files = []
    for f in blueprint_dir.glob("*.md"):
        if f != prop_file and not f.name.startswith("_"):
            new_files.append(f.name)

    print(f"    [DISASSEMBLE] Done ({elapsed:.0f}s)", file=sys.stderr)
    return new_files


def _update_table(blueprint_dir, findings):
    """Append new property entries to _table.md."""
    table_path = blueprint_dir / "_table.md"
    if not table_path.exists():
        return

    derived = [f for f in findings if f["kind"] == "derived"]
    if not derived:
        return

    lines = table_path.read_text().rstrip().split("\n")
    for f in derived:
        label = f["label"]
        name = f["name"]
        desc = f["description"]
        lines.append(f"| {label} | {name} | {desc} | introduced |")

    table_path.write_text("\n".join(lines) + "\n")
    print(f"    [TABLE] Added {len(derived)} entries", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Promote Inline — extract embedded results to standalone properties")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument("--label", help="Promote for a single property only")
    parser.add_argument("--dry-run", action="store_true",
                        help="Scan only, show findings without promoting")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        sys.exit(1)

    blueprint_dir = blueprint_properties_dir(asn_label)
    if not blueprint_dir.exists():
        print(f"  No blueprint directory for {asn_label}", file=sys.stderr)
        sys.exit(1)

    print(f"\n  [PROMOTE-INLINE] {asn_label}", file=sys.stderr)
    print(f"  Blueprint: {blueprint_dir.relative_to(WORKSPACE)}", file=sys.stderr)

    # Load vocabulary and table
    vocab_path = blueprint_dir / "_vocabulary.md"
    vocabulary = vocab_path.read_text() if vocab_path.exists() else "(no vocabulary file)"

    table_path = blueprint_dir / "_table.md"
    table = table_path.read_text() if table_path.exists() else "(no table file)"

    # Collect property files
    prop_files = sorted(
        f for f in blueprint_dir.glob("*.md")
        if not f.name.startswith("_")
    )

    if args.label:
        prop_files = [f for f in prop_files if f.name.replace(".md", "") == args.label]

    # Scan for candidates (mechanical pre-filter + LLM scan)
    candidates = []
    for f in prop_files:
        content = f.read_text()
        if len(content) < 500:
            continue
        post = _extract_post_contract(content)
        if not post:
            continue

        label = f.name.replace(".md", "")
        print(f"  Scanning {label}...", end="", file=sys.stderr, flush=True)
        findings, elapsed = _scan_property_file(label, content)
        derived = [fd for fd in findings if fd["kind"] == "derived"]

        if derived:
            print(f" {len(derived)} derived ({elapsed:.0f}s)", file=sys.stderr)
            candidates.append((label, f, findings))
        else:
            print(f" clean ({elapsed:.0f}s)", file=sys.stderr)

    if not candidates:
        print(f"\n  Nothing to promote.", file=sys.stderr)
        return

    print(f"\n  {len(candidates)} properties with results to promote.",
          file=sys.stderr)

    if args.dry_run:
        for label, f, findings in candidates:
            derived = [fd for fd in findings if fd["kind"] == "derived"]
            for fd in derived:
                print(f"    {label} → {fd['label']} ({fd['name']}): {fd['description']}",
                      file=sys.stderr)
        return

    # Promote each property: promote → format → disassemble
    for label, prop_file, findings in candidates:
        print(f"\n  --- {label} ---", file=sys.stderr)

        # Step 1: Promote (rewrite narrative, create new section in file)
        new_content, elapsed = _promote_one(
            prop_file, label, findings, vocabulary, table)
        if new_content is None:
            continue
        prop_file.write_text(new_content + "\n")

        # Step 2: Format (fix labels, headers)
        _format_one(prop_file)

        # Step 3: Disassemble (split file into separate property files)
        new_files = _disassemble_one(prop_file, blueprint_dir)

        # Step 4: Update table
        _update_table(blueprint_dir, findings)

        # Reload table for next iteration
        if table_path.exists():
            table = table_path.read_text()

    print(f"\n  [PROMOTE-INLINE] Done", file=sys.stderr)


if __name__ == "__main__":
    main()
