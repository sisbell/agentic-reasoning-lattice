#!/usr/bin/env python3
"""
Evidence ad-hoc consultation for the materials domain.

Pre-loads a named channel's corpus (measurement data, historical experimental
papers) and answers questions grounded in it. Single-source read — no parallel
KB+code subcalls, no tool access. The channel is chosen per call (typically from
the ASN's campaign binding).

Transcripts are written to lattices/materials/discovery/consultations/.../sessions/
for traceability. Prints the output file path to stdout.

For batch consultations (discovery decompose pipeline), evidence logic is
imported directly — this script is NOT called as a subprocess.

Usage:
    python scripts/consult.py evidence "What values are reported for copper?" --asn 2
    echo "question" | python scripts/consult.py evidence --stdin --asn 2
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
from lib.shared.paths import CONSULTATIONS_DIR, CHANNELS_DIR, prompt_path
from lib.shared.common import read_file, concat_md_files
from lib.consult import (
    invoke_claude as _invoke,
    parse_numbered,
    format_out_of_scope_block,
    next_session_dir,
    resolve_channel_from_args,
)

PROMPT_TEMPLATE = prompt_path("discovery/consultation/evidence/answer.md")
GENERATE_QUESTIONS_PROMPT = prompt_path("discovery/consultation/evidence/generate-questions.md")

_CACHED_CORPUS_BY_CHANNEL = {}
_CACHED_TEMPLATES = {}


def _load_template(path):
    if path not in _CACHED_TEMPLATES:
        _CACHED_TEMPLATES[path] = read_file(path)
    return _CACHED_TEMPLATES[path]


def all_corpus(channel):
    """Return the concatenated corpus for the named channel, cached by channel name."""
    if channel in _CACHED_CORPUS_BY_CHANNEL:
        return _CACHED_CORPUS_BY_CHANNEL[channel]
    corpus_dir = CHANNELS_DIR / channel
    corpus = concat_md_files(corpus_dir)
    if not corpus:
        raise RuntimeError(
            f"evidence corpus is empty at {corpus_dir} — "
            f"add .md source files before running evidence consultations")
    _CACHED_CORPUS_BY_CHANNEL[channel] = corpus
    return corpus


def build_prompt(question, channel):
    template = _load_template(PROMPT_TEMPLATE)
    if not template:
        print(f"  prompt template not found: {PROMPT_TEMPLATE}", file=sys.stderr)
        sys.exit(1)
    return template.replace("{{corpus}}", all_corpus(channel)).replace("{{question}}", question)


def generate_questions(inquiry_text, channel, n=10, model="opus", out_of_scope=""):
    """Generate N evidence-side sub-questions for an inquiry. Returns list of strings.

    Injects the evidence corpus so the generator can target specific substances,
    measurements, and patterns that actually appear in the data — matching
    xanadu's Gregory generator which injects a KB synthesis for the same reason.
    See docs/design-notes/question-generator-context.md.
    """
    template = _load_template(GENERATE_QUESTIONS_PROMPT)
    if not template:
        print(f"  [ERROR] {GENERATE_QUESTIONS_PROMPT.name} not found", file=sys.stderr)
        sys.exit(1)

    prompt = template.format(
        inquiry=inquiry_text,
        corpus=all_corpus(channel),
        num_questions=n,
        out_of_scope=format_out_of_scope_block(out_of_scope),
    )

    print(f"  [DECOMPOSE:evidence:{channel}] {n} questions, {len(prompt) // 1024}KB prompt...",
          file=sys.stderr)
    text, _ = _invoke(prompt, model=model, skill="pre-consult:evidence", label="evidence")
    return parse_numbered(text)


def run_consultation(question, channel, label="", model="opus", effort="max"):
    """Single evidence consultation against the named channel. Returns answer text. No tool access, no parallel subcalls."""
    prompt = build_prompt(question, channel)
    print(f"  [{label}] Prompt: {len(prompt) // 1024}KB", file=sys.stderr)
    skill = f"consult:{label}" if label else "consult:evidence"
    text, _ = _invoke(prompt, model=model, effort=effort, allow_tools=False,
                      skill=skill, label=label)
    return text


def main():
    parser = argparse.ArgumentParser(
        description="Ad-hoc evidence consultation (materials domain)")
    parser.add_argument("question", nargs="?", help="The question to ask")
    parser.add_argument("--stdin", action="store_true", help="Read question from stdin")
    parser.add_argument("--model", "-m", default="opus", help="Model (default: opus)")
    parser.add_argument("--effort", default="max", help="Thinking effort (low/medium/high/max)")
    parser.add_argument("--asn", default=None,
                        help="ASN number — resolves campaign to pick the evidence channel")
    parser.add_argument("--channel", default=None,
                        help="Explicit evidence channel name (overrides --asn resolution)")
    args = parser.parse_args()

    if args.stdin:
        question = sys.stdin.read().strip()
    elif args.question:
        question = args.question
    else:
        parser.error("Provide a question or use --stdin")

    if not question:
        parser.error("Empty question")

    channel = resolve_channel_from_args(args, "evidence")

    asn_prefix = f"ASN-{args.asn}" if args.asn else "adhoc"
    consult_dir = next_session_dir(CONSULTATIONS_DIR / asn_prefix / "sessions", "evidence")
    (consult_dir / "question.md").write_text(question + "\n")
    answer_file = consult_dir / "answer.md"

    print(f"  [EVIDENCE:{channel}] pre-loading corpus...", file=sys.stderr)
    prompt = build_prompt(question, channel)
    prompt_size = len(prompt)
    print(f"  Prompt: {prompt_size / 1024:.0f}KB ({prompt_size // 4:.0f} tokens est.)",
          file=sys.stderr)

    _invoke(prompt, model=args.model, effort=args.effort,
            allow_tools=False, output_file=answer_file,
            skill="evidence-consult")
    print(str(answer_file))
    print(f"  [LOG] {consult_dir}", file=sys.stderr)


if __name__ == "__main__":
    main()
