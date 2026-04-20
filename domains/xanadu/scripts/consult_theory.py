#!/usr/bin/env python3
"""
Nelson ad-hoc consultation — for the discovery agent's follow-up questions.

Pre-loads ~70K tokens of curated content (concepts, intent, Literary Machines).
With --with-png, also enables tool access for reading page images.

Transcripts written to lattices/xanadu/discovery/consultations/.../sessions/ for traceability.
Prints the output file path to stdout.

For batch consultations (consult-experts.py pipeline), Nelson logic is
inlined directly — this script is NOT called as a subprocess.

Usage:
    python scripts/consult.py theory "What is Nelson's intent for withdrawal?"
    python scripts/consult.py theory --with-png "What is Nelson's intent for withdrawal?"
    echo "question" | python scripts/consult.py theory --stdin
"""

import argparse
import re
import sys
from pathlib import Path

# Reach up from domains/xanadu/scripts/ to workspace root, then add scripts/ to path.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
from lib.shared.paths import CONSULTATIONS_DIR, DOMAIN_PROMPTS, CHANNELS_DIR
from lib.shared.common import read_file
from lib.consult_common import invoke_claude as _invoke

CONCEPTS_DIR = CHANNELS_DIR / "theory" / "xanadu-concepts"
INTENT_DIR = CHANNELS_DIR / "theory" / "nelson-intent"
LM_TOC = CHANNELS_DIR / "theory" / "literary-machines" / "table-of-contents.md"
LM_INVENTORY = CHANNELS_DIR / "theory" / "literary-machines" / "inventory.md"
LM_RAW_DIR = CHANNELS_DIR / "theory" / "literary-machines" / "raw"
PROMPT_TEMPLATE = DOMAIN_PROMPTS / "discovery" / "consultation" / "nelson" / "answer.md"


def invoke_claude(prompt, model="opus", effort=None, allow_tools=False,
                  output_file=None):
    """Wrapper around the shared invoke_claude with nelson-consult skill."""
    text, _ = _invoke(prompt, model=model, effort=effort,
                      allow_tools=allow_tools, output_file=output_file,
                      skill="nelson-consult")
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
    args = parser.parse_args()

    if args.stdin:
        question = sys.stdin.read().strip()
    elif args.question:
        question = args.question
    else:
        parser.error("Provide a question or use --stdin")

    if not question:
        parser.error("Empty question")

    # Create transcript directory
    prefix = f"ASN-{args.asn}" if args.asn else "adhoc"
    prefix_dir = CONSULTATIONS_DIR / prefix / "sessions"
    prefix_dir.mkdir(parents=True, exist_ok=True)
    existing = sorted(prefix_dir.glob("nelson-*/"))
    next_num = 1
    for d in existing:
        m = re.search(r"nelson-(\d+)$", d.name)
        if m:
            next_num = max(next_num, int(m.group(1)) + 1)
    consult_dir = prefix_dir / f"nelson-{next_num}"
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

    print(str(answer_file))
    print(f"  [LOG] {consult_dir}", file=sys.stderr)


if __name__ == "__main__":
    main()
