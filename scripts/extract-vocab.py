#!/usr/bin/env python3
"""
Extract vocabulary from ASNs and detect notation conflicts.

Reads one or more ASNs, compares notation against current vocabulary,
reports conflicts, and updates vault/vocabulary.md.

Usage:
    python scripts/extract-vocab.py 4              # single ASN
    python scripts/extract-vocab.py 4 5 6          # multiple
    python scripts/extract-vocab.py --all          # all ASNs
    python scripts/extract-vocab.py 5 --dry-run    # show without writing
"""

import argparse
import os
import re
import subprocess
import sys
import time
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
PROMPTS_DIR = WORKSPACE / "scripts" / "prompts"
EXTRACT_TEMPLATE = PROMPTS_DIR / "extract-vocab.md"
ASNS_DIR = WORKSPACE / "vault" / "asns"
VOCAB_PATH = WORKSPACE / "vault" / "vocabulary.md"


def read_file(path):
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


def find_asn(asn_id):
    """Find ASN file by number. Accepts 4, 04, 0004, ASN-0004, or full path."""
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


def find_all_asns():
    """Find all ASN files in vault/asns/."""
    return sorted(ASNS_DIR.glob("ASN-*.md"))


def build_prompt(asn_content, vocabulary):
    """Assemble extraction prompt from template + injected content."""
    template = read_file(EXTRACT_TEMPLATE)
    if not template:
        print("  Prompt template not found at scripts/prompts/extract-vocab.md",
              file=sys.stderr)
        sys.exit(1)

    return template.replace(
        "{{vocabulary}}", vocabulary
    ).replace(
        "{{asn_content}}", asn_content
    )


def parse_output(text):
    """Split output into conflicts and vocabulary sections.

    Returns (conflicts, vocabulary) where conflicts is everything
    before the --- separator and vocabulary is everything after.
    """
    # Strip markdown fences if the model wrapped output
    if text.startswith("```"):
        lines = text.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines)

    # Split on --- separator (line containing only ---)
    parts = re.split(r"\n---\n", text, maxsplit=1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip() + "\n"
    # Fallback: treat entire output as vocabulary
    return "", text.strip() + "\n"


def invoke_claude(prompt, model="sonnet", effort="high"):
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


def main():
    parser = argparse.ArgumentParser(
        description="Extract vocabulary from ASNs and detect conflicts")
    parser.add_argument("asns", nargs="*",
                        help="ASN numbers (e.g., 4 5 6) or paths")
    parser.add_argument("--all", action="store_true",
                        help="Process all ASNs in vault/asns/")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show conflicts and proposed vocab, don't write")
    parser.add_argument("--model", "-m", default="sonnet",
                        choices=["opus", "sonnet"],
                        help="Model (default: sonnet)")
    parser.add_argument("--effort", default="high",
                        help="Thinking effort level (low/medium/high/max)")
    args = parser.parse_args()

    # Resolve ASN files
    if args.all:
        asn_files = find_all_asns()
        if not asn_files:
            print("  No ASNs found in vault/asns/", file=sys.stderr)
            sys.exit(1)
    elif not args.asns:
        parser.error("provide ASN numbers or use --all")
    else:
        asn_files = []
        for asn_id in args.asns:
            path, label = find_asn(asn_id)
            if path is None:
                print(f"  No ASN found for {asn_id} in vault/asns/",
                      file=sys.stderr)
                sys.exit(1)
            asn_files.append(path)

    # Read current vocabulary
    vocabulary = read_file(VOCAB_PATH)

    # Read ASN content
    asn_parts = []
    for path in asn_files:
        asn_parts.append(f"### {path.name}\n\n{path.read_text()}")

    asn_content = "\n\n".join(asn_parts)

    # Build prompt
    labels = [re.match(r"(ASN-\d+)", p.stem).group(1) for p in asn_files]
    print(f"  [EXTRACT] {', '.join(labels)}", file=sys.stderr)
    prompt = build_prompt(asn_content, vocabulary or "(empty)")
    print(f"  Prompt: {len(prompt) // 1024}KB (~{len(prompt) // 4} tokens est.)",
          file=sys.stderr)

    # Invoke Claude
    text, elapsed = invoke_claude(prompt, model=args.model, effort=args.effort)

    if not text:
        print("  No output produced", file=sys.stderr)
        sys.exit(1)

    # Parse into conflicts + vocabulary
    conflicts, new_vocab = parse_output(text)

    # Print conflicts to stderr
    if conflicts:
        print("\n" + conflicts, file=sys.stderr)

    if args.dry_run:
        # Print vocabulary to stdout for inspection
        print(new_vocab)
        print(f"\n  [DRY RUN] Would write to {VOCAB_PATH.relative_to(WORKSPACE)}",
              file=sys.stderr)
    else:
        VOCAB_PATH.write_text(new_vocab)
        print(f"  Written to {VOCAB_PATH.relative_to(WORKSPACE)} "
              f"({len(new_vocab)} bytes)", file=sys.stderr)
        # Print path to stdout (for pipeline consumption)
        print(str(VOCAB_PATH))


if __name__ == "__main__":
    main()
