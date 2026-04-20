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
from lib.consult_common import invoke_claude as _invoke, get_total_usage

PROMPTS_DIR = DOMAIN_PROMPTS / "discovery" / "consultation"
TEST_HARNESS = CHANNELS_DIR / "evidence" / "udanax-test-harness"
KB_PATH = TEST_HARNESS / "knowledge-base" / "kb-formal.md"
KB_SYNTHESIS_PATH = TEST_HARNESS / "knowledge-base" / "kb-synthesis.md"
GENERATE_QUESTIONS_PROMPT = PROMPTS_DIR / "gregory" / "generate-questions.md"


def invoke_claude(prompt, model="sonnet", label="", allow_tools=False,
                  cwd=None, effort=None, output_file=None):
    """Wrapper around the shared invoke_claude that returns just the text
    (consult_common already tracks per-process totals)."""
    text, _ = _invoke(prompt, model=model, effort=effort,
                      allow_tools=allow_tools, cwd=cwd,
                      output_file=output_file,
                      skill=f"consult-gregory:{label}",
                      label=label)
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


def _parse_numbered(response):
    """Parse numbered questions (1. foo, 2. bar) into a list of strings.
    Strips any stray authority tags like [gregory] in case they appear."""
    questions = []
    for line in response.strip().split("\n"):
        line = line.strip()
        if not line or not (line[0].isdigit() and "." in line[:4]):
            continue
        q = line.split(".", 1)[1].strip()
        if q.startswith("[gregory]"):
            q = q[len("[gregory]"):].strip()
        questions.append(q)
    return questions


def generate_questions(inquiry_text, n=10, model="opus", out_of_scope=""):
    """Generate N evidence-side sub-questions for an inquiry.
    Injects the KB synthesis as context (Gregory's technical vocabulary).
    Returns a list of question strings."""
    template = read_file(GENERATE_QUESTIONS_PROMPT)
    if not template:
        print(f"  [ERROR] {GENERATE_QUESTIONS_PROMPT.name} not found",
              file=sys.stderr)
        sys.exit(1)

    kb = read_file(KB_SYNTHESIS_PATH)
    if not kb:
        print(f"  [WARN] KB synthesis not found at "
              f"{KB_SYNTHESIS_PATH.relative_to(WORKSPACE)}", file=sys.stderr)
        kb = ""

    out_of_scope_block = (
        f"\n## Scope Exclusions\n\nDO NOT generate questions about: {out_of_scope}\n"
        if out_of_scope else ""
    )
    prompt = template.format(
        inquiry=inquiry_text,
        kb=kb,
        num_questions=n,
        out_of_scope=out_of_scope_block,
    )

    print(f"  [DECOMPOSE:gregory] {n} questions, "
          f"{len(prompt) // 1024}KB prompt...", file=sys.stderr)
    text, _ = _invoke(prompt, model=model, skill="pre-consult:gregory",
                      label="gregory")
    return _parse_numbered(text)


def run_consultation(question, label="", model="sonnet", effort="max"):
    """Run a single evidence consultation (KB + code in parallel).
    Returns combined answer text. Used by the full-discovery orchestrator."""
    kb_result = [None]
    code_result = [None]

    def _kb():
        kb_result[0] = run_kb(question, model=model, effort=effort)

    def _code():
        code_result[0] = run_code(question, model=model, effort=effort)

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

    totals = get_total_usage()
    print(f"\n  [TOTAL] {elapsed:.0f}s | {totals['calls']} calls | "
          f"in:{totals['input_tokens']} out:{totals['output_tokens']} "
          f"${totals['cost_usd']:.4f}", file=sys.stderr)
    print(f"  [LOG] {consult_dir}", file=sys.stderr)


if __name__ == "__main__":
    main()
