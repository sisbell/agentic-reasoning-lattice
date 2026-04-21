#!/usr/bin/env python3
"""
Extract Nelson design features from ASNs into a requirements file.

Sends the ASN content to an LLM which identifies all Nelson quotes,
references, and design intent — then deduplicates, categorizes by
feature area, assigns feature numbers, and maps features to ASNs.

Output: lattices/xanadu/requirements/features.md

Usage:
    python scripts/requirements.py 4 6 9        # specific ASNs
    python scripts/requirements.py               # all ASNs
    python scripts/requirements.py 11 --dry-run
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import WORKSPACE, NOTES_DIR, REQUIREMENTS_DIR, USAGE_LOG, DOMAIN_PROMPTS
from lib.shared.common import find_asn, read_file

PROMPTS_DIR = DOMAIN_PROMPTS / "requirements"
TEMPLATE = PROMPTS_DIR / "extract-features.md"


def asn_label(path):
    """Extract ASN-NNNN from a path."""
    m = re.match(r"(ASN-\d+)", path.stem)
    return m.group(1) if m else path.stem


def build_prompt(asn_contents, existing_features):
    """Assemble prompt from template + ASN content."""
    template = read_file(TEMPLATE)
    if not template:
        print(f"  Prompt template not found: {TEMPLATE.relative_to(WORKSPACE)}",
              file=sys.stderr)
        sys.exit(1)

    return template.replace(
        "{{asn_content}}", asn_contents
    ).replace(
        "{{existing_features}}",
        existing_features or "(No existing features file — first run.)"
    )


def strip_preamble(text):
    """Strip any preamble before the features header."""
    marker = re.search(r"^# Nelson Design Features", text, re.MULTILINE)
    if marker:
        return text[marker.start():]
    return text


def invoke_claude(prompt, model="opus", effort="high"):
    """Call claude --print with --tools "". Returns plain text response."""
    model_flag = {
        "opus": "claude-opus-4-7",
        "sonnet": "claude-sonnet-4-6",
    }.get(model, model)

    cmd = [
        "claude", "--print",
        "--model", model_flag,
        "--tools", "",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
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

    print(f"  [{elapsed:.0f}s]", file=sys.stderr)
    return result.stdout.strip(), elapsed


def log_usage(n_asns, elapsed):
    """Append a usage entry to the log."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "extract-features",
            "asns": n_asns,
            "elapsed_s": round(elapsed, 1),
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def main():
    parser = argparse.ArgumentParser(
        description="Extract Nelson design features from ASN quotes")
    parser.add_argument("asns", nargs="*",
                        help="ASN numbers (e.g., 4 6 9). "
                             "Omit for all ASNs.")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"],
                        help="Model (default: opus)")
    parser.add_argument("--effort", default="high",
                        help="Thinking effort level (low/medium/high/max)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show prompt size without invoking Claude")
    args = parser.parse_args()

    # Find ASNs
    if args.asns:
        asn_files = []
        for a in args.asns:
            path, _ = find_asn(a)
            if path:
                asn_files.append(path)
            else:
                print(f"  No ASN found for {a}", file=sys.stderr)
        if not asn_files:
            sys.exit(1)
    else:
        asn_files = sorted(NOTES_DIR.glob("ASN-*.md"))

    if not asn_files:
        print(f"  No ASN files found in {NOTES_DIR.relative_to(WORKSPACE)}/", file=sys.stderr)
        sys.exit(1)

    labels = [asn_label(p) for p in asn_files]
    print(f"  [FEATURES] {len(asn_files)} ASNs: "
          f"{', '.join(labels)}", file=sys.stderr)

    # Concatenate ASN content
    asn_contents = ""
    for p in asn_files:
        label = asn_label(p)
        content = p.read_text()
        asn_contents += f"\n---\n\n## {label}\n\n{content}\n"

    # Read existing features (for incremental update)
    features_path = REQUIREMENTS_DIR / "features.md"
    existing = read_file(features_path)

    # Build prompt
    prompt = build_prompt(asn_contents, existing)
    print(f"  Prompt: {len(prompt) // 1024}KB (~{len(prompt) // 4} tokens est.)",
          file=sys.stderr)

    if args.dry_run:
        print(f'  [DRY RUN] Would invoke {args.model} with --tools ""',
              file=sys.stderr)
        return

    # Invoke Claude
    text, elapsed = invoke_claude(prompt, model=args.model, effort=args.effort)

    if not text:
        print("  No features produced", file=sys.stderr)
        sys.exit(1)

    # Strip preamble
    text = strip_preamble(text)

    # Strip any existing Generated metadata line (LLM may echo it back)
    text = re.sub(r"\n\*Generated:.*?\*\n", "\n", text)

    # Add generation metadata
    meta_line = (f"\n*Generated: {time.strftime('%Y-%m-%d')} — "
                 f"from {', '.join(labels)}*\n")
    lines = text.split("\n", 1)
    if len(lines) == 2:
        text = lines[0] + "\n" + meta_line + lines[1]
    else:
        text = text + "\n" + meta_line

    # Write output
    REQUIREMENTS_DIR.mkdir(parents=True, exist_ok=True)
    features_path.write_text(text + "\n")

    # Log usage
    log_usage(len(asn_files), elapsed)

    # Print output path to stdout
    print(str(features_path))

    print(f"  [WROTE] {features_path.relative_to(WORKSPACE)}", file=sys.stderr)


if __name__ == "__main__":
    main()
