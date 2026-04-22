#!/usr/bin/env python3
"""
Evidence consultation for the xanadu domain.

Runs two independent claude --print processes with the same question:
  1. KB agent: prompt template + injected KB (no tools, fast)
  2. Code agent: prompt template + tool access (tools, thorough)

Both run in parallel. Transcripts written to
lattices/xanadu/discovery/consultations/.../sessions/ for traceability.
Prints the combined output file path to stdout.

The channel is chosen per call (typically from the ASN's campaign binding).

For batch consultations (discovery decompose pipeline), evidence logic is
imported directly — this script is NOT called as a subprocess.

Usage:
    python scripts/consult.py evidence "What happens after DELETE?" --asn 34
    python scripts/consult.py evidence --kb-only "..." --asn 34
    python scripts/consult.py evidence --code-only "..." --asn 34
    echo "question" | python scripts/consult.py evidence --stdin --asn 34
"""

import argparse
import re
import sys
import time
import threading
from pathlib import Path

# Reach up from domains/xanadu/scripts/ to workspace root, then add scripts/ to path.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
from lib.shared.paths import WORKSPACE, CONSULTATIONS_DIR, CHANNELS_DIR, prompt_path
from lib.shared.common import read_file
from lib.shared.campaign import resolve_campaign
from lib.consult import (
    invoke_claude as _invoke,
    get_total_usage,
    parse_numbered,
    format_out_of_scope_block,
)


def _test_harness(channel):
    return CHANNELS_DIR / channel / "udanax-test-harness"


def _kb_path(channel):
    return _test_harness(channel) / "knowledge-base" / "kb-formal.md"


def _kb_synthesis_path(channel):
    return _test_harness(channel) / "knowledge-base" / "kb-synthesis.md"


def invoke_claude(prompt, channel, model="sonnet", label="", allow_tools=False,
                  cwd=None, effort=None, output_file=None):
    """Wrapper around the shared invoke_claude that returns just the text."""
    text, _ = _invoke(prompt, model=model, effort=effort,
                      allow_tools=allow_tools, cwd=cwd,
                      output_file=output_file,
                      skill=f"consult-{channel}:{label}",
                      label=label)
    return text


def build_kb_prompt(question, channel):
    """Assemble KB synthesis prompt from template + injected KB."""
    template = read_file(prompt_path("discovery/consultation/evidence/answer-from-kb.md"))
    kb = read_file(_kb_path(channel))
    if not template:
        print("  KB prompt template not found", file=sys.stderr)
        sys.exit(1)
    if not kb:
        print(f"  KB file not found at {_kb_path(channel).relative_to(WORKSPACE)}",
              file=sys.stderr)
        sys.exit(1)
    return template.replace("{{kb}}", kb).replace("{{question}}", question)


def build_code_prompt(question, channel):
    """Assemble code exploration prompt from template."""
    template = read_file(prompt_path("discovery/consultation/evidence/answer-from-code.md"))
    if not template:
        print("  Code prompt template not found", file=sys.stderr)
        sys.exit(1)
    return template.replace("{{question}}", question)


def run_kb(question, channel, model="sonnet", effort=None, output_file=None):
    """Run the KB synthesis agent. No tools — pure synthesis from injected KB."""
    print("  [KB]", file=sys.stderr)
    prompt = build_kb_prompt(question, channel)
    print(f"  Prompt: {len(prompt) // 1024}KB (~{len(prompt) // 4} tokens)",
          file=sys.stderr)
    return invoke_claude(prompt, channel, model=model, label="kb",
                         allow_tools=False, effort=effort,
                         output_file=output_file)


def run_code(question, channel, model="sonnet", effort=None, output_file=None):
    """Run the code exploration agent with tool access, cwd=test harness."""
    print("  [CODE]", file=sys.stderr)
    prompt = build_code_prompt(question, channel)
    print(f"  Prompt: {len(prompt) // 1024}KB (~{len(prompt) // 4} tokens)",
          file=sys.stderr)
    return invoke_claude(prompt, channel, model=model, label="code",
                         allow_tools=True, cwd=str(_test_harness(channel)),
                         effort=effort, output_file=output_file)


def generate_questions(inquiry_text, channel, n=10, model="opus", out_of_scope=""):
    """Generate N evidence-side sub-questions for an inquiry.
    Injects the KB synthesis as context (technical vocabulary).
    Returns a list of question strings."""
    template_path = prompt_path("discovery/consultation/evidence/generate-questions.md")
    template = read_file(template_path)
    if not template:
        print(f"  [ERROR] {template_path.name} not found", file=sys.stderr)
        sys.exit(1)

    kb = read_file(_kb_synthesis_path(channel))
    if not kb:
        print(f"  [WARN] KB synthesis not found at "
              f"{_kb_synthesis_path(channel).relative_to(WORKSPACE)}", file=sys.stderr)
        kb = ""

    prompt = template.format(
        inquiry=inquiry_text,
        kb=kb,
        num_questions=n,
        out_of_scope=format_out_of_scope_block(out_of_scope),
    )

    print(f"  [DECOMPOSE:{channel}] {n} questions, "
          f"{len(prompt) // 1024}KB prompt...", file=sys.stderr)
    text, _ = _invoke(prompt, model=model, skill=f"pre-consult:{channel}",
                      label=channel)
    return parse_numbered(text, tags_to_strip=(f"[{channel}]",))


def run_consultation(question, channel, label="", model="sonnet", effort="max"):
    """Run a single evidence consultation (KB + code in parallel).
    Returns combined answer text. Used by the full-discovery orchestrator."""
    kb_result = [None]
    code_result = [None]

    def _kb():
        kb_result[0] = run_kb(question, channel, model=model, effort=effort)

    def _code():
        code_result[0] = run_code(question, channel, model=model, effort=effort)

    print(f"  [{label}] Starting KB + code in parallel...", file=sys.stderr)
    kb_thread = threading.Thread(target=_kb)
    code_thread = threading.Thread(target=_code)
    kb_thread.start()
    code_thread.start()
    kb_thread.join()
    code_thread.join()

    parts = []
    if kb_result[0]:
        parts.append(f"## KB Synthesis\n\n{kb_result[0]}")
    if code_result[0]:
        parts.append(f"## Code Exploration\n\n{code_result[0]}")

    combined = "\n\n---\n\n".join(parts) if parts else "[No answer]"
    print(f"  [{label}] Done", file=sys.stderr)
    return combined


def main():
    parser = argparse.ArgumentParser(description="Evidence consultation (xanadu)")
    parser.add_argument("question", nargs="?", help="The question to ask")
    parser.add_argument("--stdin", action="store_true",
                        help="Read question from stdin")
    parser.add_argument("--model", "-m", default="sonnet",
                        help="Model (default: sonnet)")
    parser.add_argument("--effort", default="max",
                        help="Thinking effort level (low/medium/high/max)")
    parser.add_argument("--kb-only", action="store_true",
                        help="Run KB synthesis agent only")
    parser.add_argument("--code-only", action="store_true",
                        help="Run code exploration agent only")
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

    if args.channel:
        channel = args.channel
    elif args.asn:
        channel = resolve_campaign(args.asn).evidence_channel
    else:
        parser.error("Provide --asn (to resolve via campaign) or --channel (explicit)")

    # Create consultation log directory
    prefix = f"ASN-{args.asn}" if args.asn else "adhoc"
    prefix_dir = CONSULTATIONS_DIR / prefix / "sessions"
    prefix_dir.mkdir(parents=True, exist_ok=True)
    existing = sorted(prefix_dir.glob(f"{channel}-*/"))
    next_num = 1
    pat = re.compile(rf"{re.escape(channel)}-(\d+)$")
    for d in existing:
        m = pat.search(d.name)
        if m:
            next_num = max(next_num, int(m.group(1)) + 1)
    consult_dir = prefix_dir / f"{channel}-{next_num}"
    consult_dir.mkdir(parents=True, exist_ok=True)

    (consult_dir / "question.md").write_text(question + "\n")

    start = time.time()

    kb_file = consult_dir / "kb-answer.md"
    code_file = consult_dir / "code-answer.md"

    if args.kb_only:
        run_kb(question, channel, model=args.model, effort=args.effort,
               output_file=kb_file)
    elif args.code_only:
        run_code(question, channel, model=args.model, effort=args.effort,
                 output_file=code_file)
    else:
        kb_thread = threading.Thread(
            target=run_kb,
            args=(question, channel),
            kwargs={"model": args.model, "effort": args.effort,
                    "output_file": kb_file}
        )
        code_thread = threading.Thread(
            target=run_code,
            args=(question, channel),
            kwargs={"model": args.model, "effort": args.effort,
                    "output_file": code_file}
        )

        kb_thread.start()
        code_thread.start()
        kb_thread.join()
        code_thread.join()

    elapsed = time.time() - start

    combined = consult_dir / "combined.md"
    parts = [f"# {channel.capitalize()} Consultation\n\n**Question:** {question}\n"]

    if kb_file.exists() and kb_file.stat().st_size > 0:
        parts.append(f"\n## KB Synthesis\n\n{kb_file.read_text()}")
    if code_file.exists() and code_file.stat().st_size > 0:
        parts.append(f"\n---\n\n## Code Exploration\n\n{code_file.read_text()}")

    combined.write_text("\n".join(parts))

    print(str(combined))

    totals = get_total_usage()
    print(f"\n  [TOTAL] {elapsed:.0f}s | {totals['calls']} calls | "
          f"in:{totals['input_tokens']} out:{totals['output_tokens']} "
          f"${totals['cost_usd']:.4f}", file=sys.stderr)
    print(f"  [LOG] {consult_dir}", file=sys.stderr)


if __name__ == "__main__":
    main()
