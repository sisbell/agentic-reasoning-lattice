#!/usr/bin/env python3
"""
Generate a proof index for a converged ASN.

Classifies each property by type (INV/PRE/POST/FRAME/LEMMA), assigns
proof labels, and produces an index table. Operates on ASNs that have
reached review maturity.

If a proof index already exists for the ASN, it is passed to the prompt so
the agent can preserve established proof labels and flag changes.

Usage:
    python scripts/model.py index 4
    python scripts/model.py index ASN-0004 --dry-run
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.shared.paths import WORKSPACE, ASNS_DIR, PROOF_INDEX_DIR, VOCABULARY, USAGE_LOG

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "formalization"
REFINE_TEMPLATE = PROMPTS_DIR / "refine.md"
COMMIT_SCRIPT = WORKSPACE / "scripts" / "commit.py"


def read_file(path):
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


def find_asn(asn_id):
    """Find ASN file by number. Accepts 9, 09, 0009, ASN-0009, or full path."""
    path = Path(asn_id)
    if path.exists():
        label = re.match(r"(ASN-\d+)", path.stem)
        return path, label.group(1) if label else path.stem

    num = re.sub(r"[^0-9]", "", str(asn_id))
    if not num:
        return None, None
    label = f"ASN-{int(num):04d}"
    matches = sorted(ASNS_DIR.glob(f"{label}-*.md"))
    if matches:
        return matches[0], label
    return None, label


def build_prompt(asn_content, vocabulary, existing_mapping):
    """Assemble refinement prompt from template + injected content."""
    template = read_file(REFINE_TEMPLATE)
    if not template:
        print("  Prompt template not found at scripts/prompts/refine.md",
              file=sys.stderr)
        sys.exit(1)

    if not existing_mapping:
        existing_mapping = "(No existing mapping — first run.)"

    return template.replace(
        "{{asn_content}}", asn_content
    ).replace(
        "{{vocabulary}}", vocabulary
    ).replace(
        "{{existing_mapping}}", existing_mapping
    )


def strip_preamble(text):
    """Strip any preamble before the proof index header."""
    marker = re.search(r"^# ASN-\d+", text, re.MULTILINE)
    if marker:
        return text[marker.start():]
    return text


def invoke_claude(prompt, model="opus", effort="max"):
    """Call claude --print with --tools "". Returns plain text response."""
    model_flag = {
        "opus": "claude-opus-4-6",
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


def log_usage(asn_label, elapsed):
    """Append a usage entry to the log."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "proof-index",
            "asn": asn_label,
            "elapsed_s": round(elapsed, 1),
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def main():
    parser = argparse.ArgumentParser(
        description="Generate proof index for a converged ASN")
    parser.add_argument("asn",
                        help="ASN number (e.g., 4, 0004, ASN-0004) or path")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"],
                        help="Model (default: opus)")
    parser.add_argument("--effort", default="max",
                        help="Thinking effort level (low/medium/high/max)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show prompt size without invoking Claude")
    args = parser.parse_args()

    # Find ASN
    asn_path, asn_label = find_asn(args.asn)
    if asn_path is None:
        print(f"  No ASN found for {args.asn} in vault/1-reasoning-docs/", file=sys.stderr)
        sys.exit(1)

    asn_content = asn_path.read_text()

    # Read vocabulary
    vocabulary = read_file(VOCABULARY)
    if not vocabulary:
        print("  Warning: vault/vocabulary.md not found", file=sys.stderr)

    # Read existing proof index (if any) for incremental update
    index_path = PROOF_INDEX_DIR / f"{asn_label}-proof-index.md"
    existing_mapping = read_file(index_path)
    if existing_mapping:
        # Check if proof index matches current ASN revision
        index_date = re.search(r"revised (\d{4}-\d{2}-\d{2})", existing_mapping)
        asn_dates = re.findall(r"\d{4}-\d{2}-\d{2}",
                               re.search(r"\*.*?\*", asn_content).group(0)
                               if re.search(r"\*.*?\*", asn_content) else "")
        asn_date = asn_dates[-1] if asn_dates else None
        if index_date and asn_date and index_date.group(1) == asn_date:
            print(f"  Existing proof index matches ASN revision ({asn_date})",
                  file=sys.stderr)
        elif index_date and asn_date:
            print(f"  ASN revised since last proof index ({index_date.group(1)} → {asn_date})",
                  file=sys.stderr)
        print(f"  Incremental update — preserving proof labels", file=sys.stderr)

    # Build prompt
    print(f"  [PROOF-INDEX] {asn_label}", file=sys.stderr)
    prompt = build_prompt(asn_content, vocabulary, existing_mapping)
    print(f"  Prompt: {len(prompt) // 1024}KB (~{len(prompt) // 4} tokens est.)",
          file=sys.stderr)

    if args.dry_run:
        print(f'  [DRY RUN] Would invoke {args.model} with --tools ""',
              file=sys.stderr)
        return

    # Invoke Claude
    text, elapsed = invoke_claude(prompt, model=args.model,
                                  effort=args.effort)

    if not text:
        print("  No proof index produced", file=sys.stderr)
        sys.exit(1)

    # Strip any preamble
    text = strip_preamble(text)

    # Extract ASN revision date from its header (e.g., "2026-02-23 (revised 2026-02-24)")
    date_match = re.search(r"\*.*?(\d{4}-\d{2}-\d{2}).*?\*", asn_content)
    # Find the last date mentioned in the header line (the most recent revision)
    all_dates = re.findall(r"\d{4}-\d{2}-\d{2}", date_match.group(0)) if date_match else []
    asn_date = all_dates[-1] if all_dates else "unknown"

    # Add source metadata line after the title
    source_line = f"\n*Source: {asn_path.name} (revised {asn_date}) — Index generated: {time.strftime('%Y-%m-%d')}*\n"
    # Insert after the first line (the title)
    lines = text.split("\n", 1)
    if len(lines) == 2:
        text = lines[0] + "\n" + source_line + lines[1]
    else:
        text = text + "\n" + source_line

    # Write output
    PROOF_INDEX_DIR.mkdir(parents=True, exist_ok=True)
    index_path.write_text(text + "\n")

    # Log usage
    log_usage(asn_label, elapsed)

    # Print output file path to stdout (for pipeline consumption)
    print(str(index_path))

    print(f"  [WROTE] {index_path.relative_to(WORKSPACE)}", file=sys.stderr)

    # Commit
    if not args.dry_run:
        print(f"\n  === COMMIT ===", file=sys.stderr)
        cmd = [sys.executable, str(COMMIT_SCRIPT),
               f"Proof index {asn_label}"]
        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=str(WORKSPACE),
        )
        if result.returncode != 0:
            print(f"  [COMMIT] FAILED", file=sys.stderr)
            if result.stderr:
                for line in result.stderr.strip().split("\n")[:3]:
                    print(f"    {line}", file=sys.stderr)
        else:
            if result.stderr:
                for line in result.stderr.strip().split("\n"):
                    print(f"  {line}", file=sys.stderr)


if __name__ == "__main__":
    main()
