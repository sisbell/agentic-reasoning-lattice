#!/usr/bin/env python3
"""
Theory consultation for the xanadu domain.

Pre-loads a named channel's structured corpus (xanadu-concepts, nelson-intent,
Literary Machines table-of-contents and inventory, plus optional page-image
access) and answers questions grounded in it. The channel is chosen per call
(typically from the ASN's campaign binding).

Transcripts are written to lattices/xanadu/discovery/consultations/.../sessions/
for traceability. Prints the output file path to stdout.

For batch consultations (discovery decompose pipeline), theory logic is imported
directly — this script is NOT called as a subprocess.

Usage:
    python scripts/consult.py theory "What is Nelson's intent for withdrawal?" --asn 34
    python scripts/consult.py theory --with-png "..." --asn 34
    echo "question" | python scripts/consult.py theory --stdin --asn 34
"""

import argparse
import sys
from pathlib import Path

# Reach up from domains/xanadu/scripts/ to workspace root, then add scripts/ to path.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
from lib.shared.paths import CONSULTATIONS_DIR, CHANNELS_DIR, prompt_path
from lib.shared.common import read_file
from lib.consult import (
    invoke_claude as _invoke,
    parse_numbered,
    format_out_of_scope_block,
    next_session_dir,
    resolve_channel_from_args,
)

PROMPT_TEMPLATE = prompt_path("discovery/consultation/theory/answer.md")
GENERATE_QUESTIONS_PROMPT = prompt_path("discovery/consultation/theory/generate-questions.md")

_CACHED_TEMPLATE = None


def _channel_dir(channel):
    return CHANNELS_DIR / channel


def _concat_md_files(directory):
    """Flat-only concatenation of .md files in a directory, each headed by its
    filename stem. Distinct from shared concat_md_files, which recurses —
    xanadu's xanadu-concepts/ and nelson-intent/ sources rely on flat-only."""
    return "\n\n".join(
        f"### {f.stem}\n{f.read_text()}"
        for f in sorted(directory.glob("*.md"))
    )


_CACHED_CONCEPTS_BY_CHANNEL = {}
_CACHED_INTENT_BY_CHANNEL = {}
_CACHED_TOC_BY_CHANNEL = {}
_CACHED_INVENTORY_BY_CHANNEL = {}


def all_concepts(channel):
    if channel not in _CACHED_CONCEPTS_BY_CHANNEL:
        _CACHED_CONCEPTS_BY_CHANNEL[channel] = _concat_md_files(
            _channel_dir(channel) / "xanadu-concepts")
    return _CACHED_CONCEPTS_BY_CHANNEL[channel]


def all_intent(channel):
    if channel not in _CACHED_INTENT_BY_CHANNEL:
        _CACHED_INTENT_BY_CHANNEL[channel] = _concat_md_files(
            _channel_dir(channel) / "nelson-intent")
    return _CACHED_INTENT_BY_CHANNEL[channel]


def _lm_toc(channel):
    if channel not in _CACHED_TOC_BY_CHANNEL:
        _CACHED_TOC_BY_CHANNEL[channel] = read_file(
            _channel_dir(channel) / "literary-machines" / "table-of-contents.md")
    return _CACHED_TOC_BY_CHANNEL[channel]


def _lm_inventory(channel):
    if channel not in _CACHED_INVENTORY_BY_CHANNEL:
        _CACHED_INVENTORY_BY_CHANNEL[channel] = read_file(
            _channel_dir(channel) / "literary-machines" / "inventory.md")
    return _CACHED_INVENTORY_BY_CHANNEL[channel]


def _lm_raw_dir(channel):
    return _channel_dir(channel) / "literary-machines" / "raw"


def generate_questions(inquiry_text, channel, n=10, model="opus", out_of_scope=""):
    """Generate N theory-side sub-questions for an inquiry.
    Returns a list of question strings."""
    template = read_file(GENERATE_QUESTIONS_PROMPT)
    if not template:
        print(f"  [ERROR] {GENERATE_QUESTIONS_PROMPT.name} not found",
              file=sys.stderr)
        sys.exit(1)

    prompt = template.format(
        inquiry=inquiry_text,
        num_questions=n,
        out_of_scope=format_out_of_scope_block(out_of_scope),
    )

    print(f"  [DECOMPOSE:theory:{channel}] {n} questions, "
          f"{len(prompt) // 1024}KB prompt...", file=sys.stderr)
    text, _ = _invoke(prompt, model=model, skill=f"pre-consult:{channel}",
                      label=channel)
    return parse_numbered(text, tags_to_strip=(f"[{channel}]",))


def run_consultation(question, channel, label="", model="opus", effort="max"):
    """Run a single theory consultation. Returns answer text.
    Used by the full-discovery orchestrator; no tool access, no image loading."""
    prompt = build_prompt(question, channel, with_png=False)
    print(f"  [{label}] Prompt: {len(prompt) // 1024}KB", file=sys.stderr)
    skill = f"consult:{label}" if label else f"consult:{channel}"
    text, _ = _invoke(prompt, model=model, effort=effort, allow_tools=False,
                      skill=skill, label=label)
    return text


def build_prompt(question, channel, with_png=False):
    global _CACHED_TEMPLATE
    if _CACHED_TEMPLATE is None:
        _CACHED_TEMPLATE = read_file(PROMPT_TEMPLATE)
        if not _CACHED_TEMPLATE:
            print("  prompt template not found", file=sys.stderr)
            sys.exit(1)
    template = _CACHED_TEMPLATE

    raw_dir = str(_lm_raw_dir(channel)) if with_png else ""

    return template.replace(
        "{{concepts}}", all_concepts(channel)
    ).replace(
        "{{intent}}", all_intent(channel)
    ).replace(
        "{{toc}}", _lm_toc(channel)
    ).replace(
        "{{inventory}}", _lm_inventory(channel)
    ).replace(
        "{{raw_dir}}", raw_dir
    ).replace(
        "{{question}}", question
    )


def main():
    parser = argparse.ArgumentParser(description="Theory consultation (xanadu)")
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
                        help="ASN number — resolves campaign to pick the theory channel")
    parser.add_argument("--channel", default=None,
                        help="Explicit theory channel name (overrides --asn resolution)")
    args = parser.parse_args()

    if args.stdin:
        question = sys.stdin.read().strip()
    elif args.question:
        question = args.question
    else:
        parser.error("Provide a question or use --stdin")

    if not question:
        parser.error("Empty question")

    channel = resolve_channel_from_args(args, "theory")

    prefix = f"ASN-{args.asn}" if args.asn else "adhoc"
    consult_dir = next_session_dir(CONSULTATIONS_DIR / prefix / "sessions", channel)
    (consult_dir / "question.md").write_text(question + "\n")
    answer_file = consult_dir / "answer.md"

    label = f"[{channel.upper()}+PNG]" if args.with_png else f"[{channel.upper()}]"
    print(f"  {label} pre-loading all sources...", file=sys.stderr)
    prompt = build_prompt(question, channel, with_png=args.with_png)
    prompt_size = len(prompt)
    print(f"  Prompt: {prompt_size / 1024:.0f}KB ({prompt_size // 4:.0f} tokens est.)",
          file=sys.stderr)

    _invoke(prompt, model=args.model, effort=args.effort,
            allow_tools=args.with_png, output_file=answer_file,
            skill=f"{channel}-consult")

    print(str(answer_file))
    print(f"  [LOG] {consult_dir}", file=sys.stderr)


if __name__ == "__main__":
    main()
