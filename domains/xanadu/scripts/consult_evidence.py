#!/usr/bin/env python3
"""
Gregory ad-hoc consultation — for the discovery agent's follow-up questions.

Runs two independent claude --print processes with the same question:
  1. KB agent: prompt template + injected KB (no tools, fast)
  2. Code agent: prompt template + tool access (tools, thorough)

Both run in parallel. Transcripts written to lattices/xanadu/discovery/consultations/.../sessions/ for traceability.
Prints the output file path to stdout.

For batch consultations (consult-experts.py pipeline), Gregory logic is
inlined directly — this script is NOT called as a subprocess.

Usage:
    python scripts/consult.py evidence "What happens to I-address allocation after DELETE?"
    python scripts/consult.py evidence --kb-only "question"
    python scripts/consult.py evidence --code-only "question"
    python scripts/consult.py evidence --effort max "question"
    echo "question" | python scripts/consult.py evidence --stdin
"""

import argparse
import re
import sys
import time
import threading
from pathlib import Path

# Reach up from domains/xanadu/scripts/ to workspace root, then add scripts/ to path.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
from lib.shared.paths import WORKSPACE, CONSULTATIONS_DIR, DOMAIN_PROMPTS, CHANNELS_DIR
from lib.shared.common import read_file
from lib.consult_common import invoke_claude as _invoke

PROMPTS_DIR = DOMAIN_PROMPTS / "discovery" / "consultation"
TEST_HARNESS = CHANNELS_DIR / "evidence" / "udanax-test-harness"
KB_PATH = TEST_HARNESS / "knowledge-base" / "kb-formal.md"

_total_usage = {"input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0, "calls": 0}
_usage_lock = threading.Lock()


def invoke_claude(prompt, model="sonnet", label="", allow_tools=False,
                  cwd=None, effort=None, output_file=None):
    """Wrapper around the shared invoke_claude that also accumulates
    per-process totals across parallel KB + code calls."""
    text, usage = _invoke(prompt, model=model, effort=effort,
                          allow_tools=allow_tools, cwd=cwd,
                          output_file=output_file,
                          skill=f"consult-gregory:{label}",
                          label=label)
    with _usage_lock:
        _total_usage["input_tokens"] += usage["input_tokens"]
        _total_usage["output_tokens"] += usage["output_tokens"]
        _total_usage["cost_usd"] += usage["cost_usd"]
        _total_usage["calls"] += 1
    return text


def build_kb_prompt(question):
    """Assemble KB synthesis prompt from template + injected KB."""
    template = read_file(PROMPTS_DIR / "gregory" / "answer-from-kb.md")
    kb = read_file(KB_PATH)
    if not template:
        print("  KB prompt template not found", file=sys.stderr)
        sys.exit(1)
    if not kb:
        print(f"  KB file not found at {KB_PATH.relative_to(WORKSPACE)}", file=sys.stderr)
        sys.exit(1)
    return template.replace("{{kb}}", kb).replace("{{question}}", question)


def build_code_prompt(question):
    """Assemble code exploration prompt from template."""
    template = read_file(PROMPTS_DIR / "gregory" / "answer-from-code.md")
    if not template:
        print("  Code prompt template not found", file=sys.stderr)
        sys.exit(1)
    return template.replace("{{question}}", question)


def run_kb(question, model="sonnet", effort=None, output_file=None):
    """Run the KB synthesis agent. No tools — pure synthesis from injected KB."""
    print("  [KB]", file=sys.stderr)
    prompt = build_kb_prompt(question)
    print(f"  Prompt: {len(prompt) // 1024}KB (~{len(prompt) // 4} tokens)",
          file=sys.stderr)
    return invoke_claude(prompt, model=model, label="kb",
                         allow_tools=False, effort=effort,
                         output_file=output_file)


def run_code(question, model="sonnet", effort=None, output_file=None):
    """Run the code exploration agent with tool access, cwd=test harness."""
    print("  [CODE]", file=sys.stderr)
    prompt = build_code_prompt(question)
    print(f"  Prompt: {len(prompt) // 1024}KB (~{len(prompt) // 4} tokens)",
          file=sys.stderr)
    return invoke_claude(prompt, model=model, label="code",
                         allow_tools=True, cwd=str(TEST_HARNESS),
                         effort=effort, output_file=output_file)


def main():
    parser = argparse.ArgumentParser(description="Gregory split consultation")
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

    # Create consultation log directory
    prefix = f"ASN-{args.asn}" if args.asn else "adhoc"
    prefix_dir = CONSULTATIONS_DIR / prefix / "sessions"
    prefix_dir.mkdir(parents=True, exist_ok=True)
    existing = sorted(prefix_dir.glob("gregory-*/"))
    next_num = 1
    for d in existing:
        m = re.search(r"gregory-(\d+)$", d.name)
        if m:
            next_num = max(next_num, int(m.group(1)) + 1)
    consult_dir = prefix_dir / f"gregory-{next_num}"
    consult_dir.mkdir(parents=True, exist_ok=True)

    # Save the question
    (consult_dir / "question.md").write_text(question + "\n")

    start = time.time()

    kb_file = consult_dir / "kb-answer.md"
    code_file = consult_dir / "code-answer.md"

    if args.kb_only:
        run_kb(question, model=args.model, effort=args.effort,
               output_file=kb_file)
    elif args.code_only:
        run_code(question, model=args.model, effort=args.effort,
                 output_file=code_file)
    else:
        # Run both in parallel
        kb_thread = threading.Thread(
            target=run_kb,
            args=(question,),
            kwargs={"model": args.model, "effort": args.effort,
                    "output_file": kb_file}
        )
        code_thread = threading.Thread(
            target=run_code,
            args=(question,),
            kwargs={"model": args.model, "effort": args.effort,
                    "output_file": code_file}
        )

        kb_thread.start()
        code_thread.start()
        kb_thread.join()
        code_thread.join()

    elapsed = time.time() - start

    # Build combined output file
    combined = consult_dir / "combined.md"
    parts = [f"# Gregory Consultation\n\n**Question:** {question}\n"]

    if kb_file.exists() and kb_file.stat().st_size > 0:
        parts.append(f"\n## KB Synthesis\n\n{kb_file.read_text()}")
    if code_file.exists() and code_file.stat().st_size > 0:
        parts.append(f"\n---\n\n## Code Exploration\n\n{code_file.read_text()}")

    combined.write_text("\n".join(parts))

    # Print the output file path (small stdout — avoids Bash capture bug)
    print(str(combined))

    print(f"\n  [TOTAL] {elapsed:.0f}s | {_total_usage['calls']} calls | "
          f"in:{_total_usage['input_tokens']} out:{_total_usage['output_tokens']} "
          f"${_total_usage['cost_usd']:.4f}", file=sys.stderr)
    print(f"  [LOG] {consult_dir}", file=sys.stderr)


if __name__ == "__main__":
    main()
