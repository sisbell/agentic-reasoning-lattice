#!/usr/bin/env python3
"""
Fast nelson consultation — pre-loads all curated sources, answers in one call.

Pre-loads ~70K tokens of curated content. With --with-png, also enables
tool access so the model can read individual Literary Machines page images
for diagrams and details not in the curated text.

Results written to vault/transcripts/ for traceability.
Prints the output file path to stdout (avoids Bash capture bug in CC 2.1.45+).

Usage:
    python scripts/consult-nelson.py "What is Nelson's intent for withdrawal?"
    python scripts/consult-nelson.py --with-png "What is Nelson's intent for withdrawal?"
    echo "question" | python scripts/consult-nelson.py --stdin
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
CONCEPTS_DIR = WORKSPACE / "resources" / "xanadu-concepts"
INTENT_DIR = WORKSPACE / "resources" / "nelson-intent"
LM_TOC = WORKSPACE / "resources" / "literary-machines" / "table-of-contents.md"
LM_INVENTORY = WORKSPACE / "resources" / "literary-machines" / "inventory.md"
LM_RAW_DIR = WORKSPACE / "resources" / "literary-machines" / "raw"
PROMPT_TEMPLATE = WORKSPACE / "scripts" / "prompts" / "nelson-agent.md"
TRANSCRIPTS_DIR = WORKSPACE / "vault" / "transcripts"
USAGE_LOG = WORKSPACE / "vault" / "usage-log.jsonl"


def read_file(path):
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


def invoke_claude(prompt, model="opus", effort=None, allow_tools=False,
                  output_file=None):
    """Call claude --print with pre-assembled prompt via stdin."""
    model_flag = {
        "opus": "claude-opus-4-6",
        "sonnet": "claude-sonnet-4-6",
    }.get(model, model)

    cmd = ["claude", "--print", "--model", model_flag, "--output-format", "json"]
    if not allow_tools:
        cmd.extend(["--tools", ""])

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    if effort:
        env["CLAUDE_CODE_EFFORT_LEVEL"] = effort

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        timeout=None
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  FAILED (exit {result.returncode}, {elapsed:.0f}s)", file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:3]:
                print(f"    {line}", file=sys.stderr)
        if output_file:
            output_file.write_text(f"[FAILED: exit {result.returncode}]\n")
        return ""

    try:
        data = json.loads(result.stdout)
        text = data.get("result", "")
        usage = data.get("usage", {})
        cost = data.get("total_cost_usd", 0)
        inp = (usage.get("input_tokens", 0) +
               usage.get("cache_read_input_tokens", 0) +
               usage.get("cache_creation_input_tokens", 0))
        out = usage.get("output_tokens", 0)
        print(f"  [{elapsed:.0f}s] in:{inp} out:{out} ${cost:.4f}", file=sys.stderr)

        if output_file:
            output_file.write_text(text)

        try:
            entry = {
                "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "skill": "nelson-consult",
                "elapsed_s": round(elapsed, 1),
                "input_tokens": inp, "output_tokens": out,
                "cost_usd": cost,
            }
            with open(USAGE_LOG, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except OSError:
            pass

        return text
    except (json.JSONDecodeError, KeyError):
        print(f"  [{elapsed:.0f}s] [no token data]", file=sys.stderr)
        text = result.stdout
        if output_file:
            output_file.write_text(text)
        return text


def all_concepts():
    """Read all curated concept files."""
    files = sorted(CONCEPTS_DIR.glob("*.md"))
    parts = []
    for f in files:
        parts.append(f"### {f.stem}\n{f.read_text()}")
    return "\n\n".join(parts)


def all_intent():
    """Read all design intent files."""
    files = sorted(INTENT_DIR.glob("*.md"))
    parts = []
    for f in files:
        parts.append(f"### {f.stem}\n{f.read_text()}")
    return "\n\n".join(parts)


def build_prompt(question, with_png=False):
    template = read_file(PROMPT_TEMPLATE)
    if not template:
        print("  prompt template not found", file=sys.stderr)
        sys.exit(1)

    raw_dir = str(LM_RAW_DIR) if with_png else ""

    return template.replace(
        "{{concepts}}", all_concepts()
    ).replace(
        "{{intent}}", all_intent()
    ).replace(
        "{{toc}}", read_file(LM_TOC)
    ).replace(
        "{{inventory}}", read_file(LM_INVENTORY)
    ).replace(
        "{{raw_dir}}", raw_dir
    ).replace(
        "{{question}}", question
    )


def main():
    parser = argparse.ArgumentParser(description="Fast nelson consultation")
    parser.add_argument("question", nargs="?", help="The question to ask")
    parser.add_argument("--stdin", action="store_true",
                        help="Read question from stdin")
    parser.add_argument("--model", "-m", default="opus",
                        help="Model (default: opus)")
    parser.add_argument("--effort", default="max",
                        help="Thinking effort level (low/medium/high/max)")
    parser.add_argument("--with-png", action="store_true",
                        help="Enable tool access to read Literary Machines page images")
    parser.add_argument("--asn", default=None,
                        help="ASN number for consultation log naming")
    parser.add_argument("--no-transcript", action="store_true",
                        help="Skip saving to vault/transcripts/ (used by pipeline)")
    args = parser.parse_args()

    if args.stdin:
        question = sys.stdin.read().strip()
    elif args.question:
        question = args.question
    else:
        parser.error("Provide a question or use --stdin")

    if not question:
        parser.error("Empty question")

    # Create transcript directory (unless suppressed by pipeline)
    consult_dir = None
    answer_file = None
    if not args.no_transcript:
        prefix = f"ASN-{args.asn}" if args.asn else "adhoc"
        existing = sorted(TRANSCRIPTS_DIR.glob(f"{prefix}-nelson-*/"))
        next_num = 1
        for d in existing:
            m = re.search(r"-nelson-(\d+)$", d.name)
            if m:
                next_num = max(next_num, int(m.group(1)) + 1)
        consult_dir = TRANSCRIPTS_DIR / f"{prefix}-nelson-{next_num}"
        consult_dir.mkdir(parents=True, exist_ok=True)
        (consult_dir / "question.md").write_text(question + "\n")
        answer_file = consult_dir / "answer.md"

    label = "[NELSON+PNG]" if args.with_png else "[NELSON]"
    print(f"  {label} pre-loading all sources...", file=sys.stderr)
    prompt = build_prompt(question, with_png=args.with_png)
    prompt_size = len(prompt)
    print(f"  Prompt: {prompt_size / 1024:.0f}KB ({prompt_size // 4:.0f} tokens est.)",
          file=sys.stderr)

    answer = invoke_claude(prompt, args.model, args.effort,
                           allow_tools=args.with_png,
                           output_file=answer_file)

    # Print the answer to stdout (when no transcript, pipeline reads this)
    if answer_file:
        print(str(answer_file))
        print(f"  [LOG] {consult_dir}", file=sys.stderr)
    else:
        print(answer)


if __name__ == "__main__":
    main()
