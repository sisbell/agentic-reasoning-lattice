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
    python scripts/consult.py gregory "What happens to I-address allocation after DELETE?"
    python scripts/consult.py gregory --kb-only "question"
    python scripts/consult.py gregory --code-only "question"
    python scripts/consult.py gregory --effort max "question"
    echo "question" | python scripts/consult.py gregory --stdin
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import threading
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import WORKSPACE, CONSULTATIONS_DIR, USAGE_LOG, DOMAIN_PROMPTS
from lib.shared.common import read_file

PROMPTS_DIR = DOMAIN_PROMPTS / "discovery" / "consultation"
TEST_HARNESS = WORKSPACE / "udanax-test-harness"
KB_PATH = TEST_HARNESS / "knowledge-base" / "kb-formal.md"

_total_usage = {"input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0, "calls": 0}
_usage_lock = threading.Lock()


def invoke_claude(prompt, model="sonnet", label="", allow_tools=False,
                  cwd=None, effort=None, output_file=None):
    """Call claude --print. Write result to output_file. Returns response text."""
    model_flag = {
        "opus": "claude-opus-4-7",
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
        cwd=cwd, timeout=None
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  [{label}] FAILED (exit {result.returncode}, {elapsed:.0f}s)",
              file=sys.stderr)
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

        with _usage_lock:
            _total_usage["input_tokens"] += inp
            _total_usage["output_tokens"] += out
            _total_usage["cost_usd"] += cost
            _total_usage["calls"] += 1

        print(f"  [{label}] {elapsed:.0f}s | in:{inp} out:{out} ${cost:.4f}",
              file=sys.stderr)

        if output_file:
            output_file.write_text(text)

        try:
            entry = {
                "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "skill": f"consult-gregory:{label}",
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
        print(f"  [{label}] {elapsed:.0f}s [no token data]", file=sys.stderr)
        text = result.stdout
        if output_file:
            output_file.write_text(text)
        return text


def build_kb_prompt(question):
    """Assemble KB synthesis prompt from template + injected KB."""
    template = read_file(PROMPTS_DIR / "gregory" / "answer-from-kb.md")
    kb = read_file(KB_PATH)
    if not template:
        print("  KB prompt template not found", file=sys.stderr)
        sys.exit(1)
    if not kb:
        print("  KB file not found at udanax-test-harness/knowledge-base/kb-formal.md", file=sys.stderr)
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
