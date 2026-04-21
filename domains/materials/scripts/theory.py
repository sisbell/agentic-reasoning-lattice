#!/usr/bin/env python3
"""
Theory ad-hoc consultation for the materials domain.

Pre-loads the full theory corpus (e.g., Maxwell's *Theory of Heat*) and
answers questions grounded in it. No tool access.

Transcripts are written to lattices/materials/discovery/consultations/.../sessions/
for traceability. Prints the output file path to stdout.

For batch consultations (discovery decompose pipeline), theory logic is
imported directly — this script is NOT called as a subprocess.

Usage:
    python scripts/consult.py theory "What does equipartition imply for heat?"
    echo "question" | python scripts/consult.py theory --stdin
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
from lib.shared.paths import CONSULTATIONS_DIR, DOMAIN_PROMPTS, CHANNELS_DIR
from lib.shared.common import read_file
from lib.consult import (
    invoke_claude as _invoke,
    parse_numbered,
    format_out_of_scope_block,
)

CORPUS_DIR = CHANNELS_DIR / "theory"
PROMPT_TEMPLATE = DOMAIN_PROMPTS / "discovery" / "consultation" / "theory" / "answer.md"
GENERATE_QUESTIONS_PROMPT = DOMAIN_PROMPTS / "discovery" / "consultation" / "theory" / "generate-questions.md"


_CACHED_CORPUS = None


def _concat_md_files(directory):
    """Concatenate all .md files under a directory (recursive), each headed by filename stem."""
    return "\n\n".join(
        f"### {f.stem}\n{f.read_text()}"
        for f in sorted(directory.rglob("*.md"))
    )


def all_corpus():
    """Return the concatenated theory corpus (cached at module scope)."""
    global _CACHED_CORPUS
    if _CACHED_CORPUS is None:
        _CACHED_CORPUS = _concat_md_files(CORPUS_DIR)
    return _CACHED_CORPUS


def build_prompt(question):
    template = read_file(PROMPT_TEMPLATE)
    if not template:
        print(f"  prompt template not found: {PROMPT_TEMPLATE}", file=sys.stderr)
        sys.exit(1)
    return template.replace("{{corpus}}", all_corpus()).replace("{{question}}", question)


def generate_questions(inquiry_text, n=10, model="opus", out_of_scope=""):
    """Generate N theory-side sub-questions for an inquiry. Returns list of strings."""
    template = read_file(GENERATE_QUESTIONS_PROMPT)
    if not template:
        print(f"  [ERROR] {GENERATE_QUESTIONS_PROMPT.name} not found", file=sys.stderr)
        sys.exit(1)

    prompt = template.format(
        inquiry=inquiry_text,
        num_questions=n,
        out_of_scope=format_out_of_scope_block(out_of_scope),
    )

    print(f"  [DECOMPOSE:theory] {n} questions, {len(prompt) // 1024}KB prompt...",
          file=sys.stderr)
    text, _ = _invoke(prompt, model=model, skill="pre-consult:theory", label="theory")
    return parse_numbered(text)


def run_consultation(question, label="", model="opus", effort="max"):
    """Single theory consultation. Returns answer text. No tool access."""
    prompt = build_prompt(question)
    print(f"  [{label}] Prompt: {len(prompt) // 1024}KB", file=sys.stderr)
    skill = f"consult:{label}" if label else "consult:theory"
    text, _ = _invoke(prompt, model=model, effort=effort, allow_tools=False,
                      skill=skill, label=label)
    return text


def main():
    parser = argparse.ArgumentParser(
        description="Ad-hoc theory consultation (materials domain)")
    parser.add_argument("question", nargs="?", help="The question to ask")
    parser.add_argument("--stdin", action="store_true", help="Read question from stdin")
    parser.add_argument("--model", "-m", default="opus", help="Model (default: opus)")
    parser.add_argument("--effort", default="max", help="Thinking effort (low/medium/high/max)")
    parser.add_argument("--asn", default=None, help="ASN number for consultation log naming")
    args = parser.parse_args()

    if args.stdin:
        question = sys.stdin.read().strip()
    elif args.question:
        question = args.question
    else:
        parser.error("Provide a question or use --stdin")

    if not question:
        parser.error("Empty question")

    prefix = f"ASN-{args.asn}" if args.asn else "adhoc"
    prefix_dir = CONSULTATIONS_DIR / prefix / "sessions"
    prefix_dir.mkdir(parents=True, exist_ok=True)
    existing = sorted(prefix_dir.glob("theory-*/"))
    next_num = 1
    for d in existing:
        m = re.search(r"theory-(\d+)$", d.name)
        if m:
            next_num = max(next_num, int(m.group(1)) + 1)
    consult_dir = prefix_dir / f"theory-{next_num}"
    consult_dir.mkdir(parents=True, exist_ok=True)
    (consult_dir / "question.md").write_text(question + "\n")
    answer_file = consult_dir / "answer.md"

    print(f"  [THEORY] pre-loading corpus...", file=sys.stderr)
    prompt = build_prompt(question)
    prompt_size = len(prompt)
    print(f"  Prompt: {prompt_size / 1024:.0f}KB ({prompt_size // 4:.0f} tokens est.)",
          file=sys.stderr)

    _invoke(prompt, model=args.model, effort=args.effort,
            allow_tools=False, output_file=answer_file,
            skill="theory-consult")
    print(str(answer_file))
    print(f"  [LOG] {consult_dir}", file=sys.stderr)


if __name__ == "__main__":
    main()
