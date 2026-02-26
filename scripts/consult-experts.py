#!/usr/bin/env python3
"""
Consult experts — decompose an inquiry into focused questions, then consult Nelson and Gregory.

Takes an inquiry, decomposes it into focused sub-questions (5 Nelson, 5 Gregory by default),
then fires all consultations in parallel. Produces a single combined results file for the
discovery agent to consume.

The key insight: the KB informs question generation (what subsystems to ask about)
but never reaches the discovery agent. This prevents implementation contamination
while ensuring comprehensive coverage.

Usage:
    python scripts/consult-experts.py --inquiry-id 4
    python scripts/consult-experts.py "What must INSERT preserve and establish?"
    python scripts/consult-experts.py --inquiry-id 4 --nelson 5 --gregory 5
    python scripts/consult-experts.py --inquiry-id 4 --dry-run  # show questions only
"""

import argparse
import json
import os
import subprocess
import sys
import time
import threading
import yaml
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
PROMPTS_DIR = WORKSPACE / "scripts" / "prompts"
INQUIRIES_PATH = WORKSPACE / "vault" / "inquiries.yaml"
CONSULT_DIR = WORKSPACE / "vault" / "consultations"
USAGE_LOG = WORKSPACE / "vault" / "usage-log.jsonl"
NELSON_SCRIPT = WORKSPACE / "scripts" / "consult-nelson.py"
GREGORY_SCRIPT = WORKSPACE / "scripts" / "consult-gregory.py"
TEST_HARNESS = WORKSPACE / "udanax-test-harness"
KB_SYNTHESIS = TEST_HARNESS / "knowledge-base" / "kb-synthesis.md"

_total_usage = {"input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0, "calls": 0}
_usage_lock = threading.Lock()


def read_file(path):
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


def log_usage(skill, elapsed, inp=0, out=0, cost=0):
    """Append a usage entry to the log."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": skill,
            "elapsed_s": round(elapsed, 1),
            "input_tokens": inp, "output_tokens": out,
            "cost_usd": cost,
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def load_inquiry(inquiry_id):
    """Load a specific inquiry from inquiries.yaml."""
    with open(INQUIRIES_PATH) as f:
        data = yaml.safe_load(f)
    for inq in data["inquiries"]:
        if inq["id"] == inquiry_id:
            return inq
    print(f"  [ERROR] Inquiry {inquiry_id} not found", file=sys.stderr)
    sys.exit(1)


# ─── Step 1: Decompose ──────────────────────────────────────────

def _call_decompose(prompt, label, model="opus"):
    """Call claude --print for question generation. Returns response text."""
    model_flag = {
        "opus": "claude-opus-4-6",
        "sonnet": "claude-sonnet-4-6",
    }.get(model, model)

    cmd = [
        "claude", "--print",
        "--model", model_flag,
        "--tools", "",
        "--output-format", "json",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        timeout=180,
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  [{label}] FAILED (exit {result.returncode}, {elapsed:.0f}s)",
              file=sys.stderr)
        return None

    try:
        data = json.loads(result.stdout)
        text = data.get("result", "")
        usage = data.get("usage", {})
        cost = data.get("total_cost_usd", 0)
        inp = (usage.get("input_tokens", 0) +
               usage.get("cache_read_input_tokens", 0) +
               usage.get("cache_creation_input_tokens", 0))
        out = usage.get("output_tokens", 0)

        print(f"  [{label}] {elapsed:.0f}s | in:{inp} out:{out} ${cost:.4f}",
              file=sys.stderr)

        with _usage_lock:
            _total_usage["input_tokens"] += inp
            _total_usage["output_tokens"] += out
            _total_usage["cost_usd"] += cost
            _total_usage["calls"] += 1

        log_usage(f"pre-consult:{label}", elapsed, inp, out, cost)
        return text

    except (json.JSONDecodeError, KeyError):
        print(f"  [{label}] {elapsed:.0f}s [parse error]", file=sys.stderr)
        return result.stdout


def decompose_inquiry(inquiry_text, num_nelson=10, num_gregory=10, model="opus"):
    """Two-pass decompose: Nelson (design vocabulary) then Gregory (with KB context).

    Nelson questions use design vocabulary only — no implementation contamination.
    Gregory questions use KB vocabulary for precise technical questions.
    """
    # Pass 1: Nelson questions (inquiry only, no KB)
    nelson_template = read_file(PROMPTS_DIR / "nelson-questions.md")
    if not nelson_template:
        print("  [ERROR] scripts/prompts/nelson-questions.md not found",
              file=sys.stderr)
        sys.exit(1)

    nelson_prompt = nelson_template.format(
        inquiry=inquiry_text,
        num_questions=num_nelson,
    )

    print(f"  [DECOMPOSE:nelson] {num_nelson} questions, "
          f"{len(nelson_prompt) // 1024}KB prompt...", file=sys.stderr)
    nelson_response = _call_decompose(nelson_prompt, "nelson", model=model)

    # Pass 2: Gregory questions (inquiry + KB synthesis)
    gregory_template = read_file(PROMPTS_DIR / "gregory-questions.md")
    if not gregory_template:
        print("  [ERROR] scripts/prompts/gregory-questions.md not found",
              file=sys.stderr)
        sys.exit(1)

    kb = read_file(KB_SYNTHESIS)
    if not kb:
        print("  [WARN] KB synthesis not found at "
              "udanax-test-harness/knowledge-base/kb-synthesis.md", file=sys.stderr)

    gregory_prompt = gregory_template.format(
        inquiry=inquiry_text,
        kb=kb,
        num_questions=num_gregory,
    )

    print(f"  [DECOMPOSE:gregory] {num_gregory} questions, "
          f"{len(gregory_prompt) // 1024}KB prompt...", file=sys.stderr)
    gregory_response = _call_decompose(gregory_prompt, "gregory", model=model)

    # Parse both
    nelson_qs = parse_questions(nelson_response, "nelson") if nelson_response else []
    gregory_qs = parse_questions(gregory_response, "gregory") if gregory_response else []

    return nelson_qs + gregory_qs


def parse_questions(response, default_authority="gregory"):
    """Parse numbered questions from response.

    Returns list of (authority, question) tuples.
    """
    questions = []
    for line in response.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        if line[0].isdigit() and "." in line[:4]:
            q = line.split(".", 1)[1].strip()
            # Strip authority tag if present
            if q.startswith("[nelson]"):
                questions.append(("nelson", q[len("[nelson]"):].strip()))
            elif q.startswith("[gregory]"):
                questions.append(("gregory", q[len("[gregory]"):].strip()))
            else:
                questions.append((default_authority, q))
    return questions


# ─── Step 2: Consult ────────────────────────────────────────────

def _run_subprocess(script, question, question_num, asn_label, label_prefix):
    """Run a consultation script as subprocess. Returns answer text.

    Both consult-nelson.py and consult-gregory.py follow the same protocol:
    save transcript to vault/transcripts/, print file path to stdout.
    """
    label = f"Q{question_num}:{label_prefix}"
    print(f"  [{label}] Starting...", file=sys.stderr)

    cmd = [
        sys.executable, str(script),
        "--effort", "max",
        "--asn", asn_label,
        question,
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)

    start = time.time()
    result = subprocess.run(
        cmd, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE),
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  [{label}] FAILED ({elapsed:.0f}s)", file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[-3:]:
                print(f"    {line}", file=sys.stderr)
        return f"[FAILED: exit {result.returncode}]"

    # stderr has progress info
    for line in result.stderr.strip().split("\n"):
        if line.strip():
            print(f"  [{label}] {line.strip()}", file=sys.stderr)

    # stdout has the output file path
    answer_path = result.stdout.strip()
    if answer_path and Path(answer_path).exists():
        answer = Path(answer_path).read_text()
        print(f"  [{label}] Done ({elapsed:.0f}s, {len(answer)} chars)",
              file=sys.stderr)
        return answer

    print(f"  [{label}] No answer file ({elapsed:.0f}s)", file=sys.stderr)
    return "[No answer produced]"


def run_nelson(question, question_num, asn_label, output_dir):
    """Run nelson consultation via consult-nelson.py. Returns answer text."""
    return _run_subprocess(NELSON_SCRIPT, question, question_num,
                           asn_label, "nelson")


def run_gregory(question, question_num, asn_label, output_dir):
    """Run gregory consultation via consult-gregory.py. Returns answer text.

    consult-gregory.py manages KB + code calls internally and saves
    transcripts (kb-answer.md, code-answer.md, combined.md).
    """
    return _run_subprocess(GREGORY_SCRIPT, question, question_num,
                           asn_label, "gregory")


def run_consultations(questions, asn_label, output_dir):
    """Run all consultations. Nelson in parallel, Gregory sequentially.

    Nelson: no tools, safe to parallelize.
    Gregory: each call runs KB + code internally (consult-gregory.py
    parallelizes them). Run sequentially because code exploration has tools.
    """
    results = [None] * len(questions)

    # Split by authority
    nelson_indices = [i for i, (a, _) in enumerate(questions) if a == "nelson"]
    gregory_indices = [i for i, (a, _) in enumerate(questions) if a == "gregory"]

    # Nelson in parallel
    if nelson_indices:
        print(f"  [NELSON] Firing {len(nelson_indices)} calls in parallel...",
              file=sys.stderr)
        threads = []

        for i in nelson_indices:
            authority, question = questions[i]
            def run_n(idx=i, q=question, auth=authority):
                answer = run_nelson(q, idx + 1, asn_label, output_dir)
                results[idx] = (auth, q, answer)
            t = threading.Thread(target=run_n)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
        print(f"  [NELSON] All done", file=sys.stderr)

    # Gregory sequentially (each call runs KB + code in parallel internally)
    if gregory_indices:
        print(f"  [GREGORY] Running {len(gregory_indices)} calls sequentially...",
              file=sys.stderr)
        for i in gregory_indices:
            authority, question = questions[i]
            answer = run_gregory(question, i + 1, asn_label, output_dir)
            results[i] = (authority, question, answer)

        print(f"  [GREGORY] All done", file=sys.stderr)

    return results


# ─── Step 3: Combine ────────────────────────────────────────────

def build_combined_output(inquiry_text, inquiry_title, questions, results):
    """Build the combined consultation answers file."""
    parts = []

    parts.append(f"# Consultation Answers — {inquiry_title}")
    parts.append(f"")
    parts.append(f"**Inquiry:** {inquiry_text}")
    parts.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    nelson_count = sum(1 for a, _ in questions if a == "nelson")
    gregory_count = len(questions) - nelson_count
    parts.append(f"**Questions:** {len(questions)} ({nelson_count} nelson, {gregory_count} gregory)")
    parts.append(f"")

    for i, (authority, question, answer) in enumerate(results, 1):
        parts.append(f"---")
        parts.append(f"")
        parts.append(f"## Question {i} [{authority}]")
        parts.append(f"")
        parts.append(f"> {question}")
        parts.append(f"")

        if authority == "nelson":
            parts.append(f"### Nelson's Answer")
        else:
            parts.append(f"### Gregory's Answer")

        parts.append(f"")
        parts.append(answer.strip() if answer else "[No answer]")
        parts.append(f"")

    return "\n".join(parts)


# ─── Main ───────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Consult experts: decompose inquiry → run Nelson and Gregory consultations")
    parser.add_argument("question", nargs="?",
                        help="The inquiry question")
    parser.add_argument("--inquiry-id", type=int,
                        help="Load inquiry by ID from inquiries.yaml")
    parser.add_argument("--nelson", type=int, default=None,
                        help="Number of Nelson questions (overrides inquiries.yaml, default: 10)")
    parser.add_argument("--gregory", type=int, default=None,
                        help="Number of Gregory questions (overrides inquiries.yaml, default: 10)")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["sonnet", "opus"],
                        help="Model for question generation (default: opus)")
    parser.add_argument("--output", "-o",
                        help="Output file path (default: vault/consultations/ASN-NNNN/answers.md)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Generate questions only, don't run consultations")
    args = parser.parse_args()

    # Load inquiry
    inquiry_title = "Ad-hoc inquiry"
    asn_label = "adhoc"
    num_nelson = 10
    num_gregory = 10
    if args.inquiry_id:
        inquiry = load_inquiry(args.inquiry_id)
        inquiry_text = inquiry["question"]
        inquiry_title = inquiry["title"]
        asn_label = f"{args.inquiry_id:04d}"
        # Read per-inquiry agent counts from YAML (agents.nelson, agents.gregory)
        agents = inquiry.get("agents", {})
        num_nelson = agents.get("nelson", 10)
        num_gregory = agents.get("gregory", 10)
    elif args.question:
        inquiry_text = args.question
    else:
        parser.error("Provide a question or --inquiry-id")

    # CLI flags override YAML values
    if args.nelson is not None:
        num_nelson = args.nelson
    if args.gregory is not None:
        num_gregory = args.gregory

    total_start = time.time()

    # Step 1: Decompose (two-pass: Nelson design vocab, Gregory with KB)
    questions = decompose_inquiry(inquiry_text,
                                  num_nelson=num_nelson,
                                  num_gregory=num_gregory,
                                  model=args.model)

    if not questions:
        print("  [ERROR] No questions generated", file=sys.stderr)
        sys.exit(1)

    nelson_qs = sum(1 for a, _ in questions if a == "nelson")
    gregory_qs = len(questions) - nelson_qs
    print(f"  [OK] {len(questions)} questions ({nelson_qs} nelson, {gregory_qs} gregory)",
          file=sys.stderr)
    print(f"", file=sys.stderr)

    for i, (authority, q) in enumerate(questions, 1):
        print(f"  {i}. [{authority}] {q}", file=sys.stderr)

    print(f"", file=sys.stderr)

    if args.dry_run:
        # Print questions to stdout and exit
        for i, (authority, q) in enumerate(questions, 1):
            print(f"{i}. [{authority}] {q}")
        return

    # Step 2: Run all consultations in parallel
    output_dir = CONSULT_DIR / f"ASN-{asn_label}"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save questions for traceability
    questions_text = "\n".join(
        f"{i}. [{a}] {q}" for i, (a, q) in enumerate(questions, 1)
    )
    (output_dir / "questions.md").write_text(
        f"# Sub-Questions — {inquiry_title}\n\n"
        f"**Inquiry:** {inquiry_text}\n\n"
        f"{questions_text}\n"
    )

    print(f"  [CONSULT] Firing {len(questions)} consultations in parallel...",
          file=sys.stderr)
    consult_start = time.time()
    results = run_consultations(questions, asn_label, output_dir)
    consult_elapsed = time.time() - consult_start
    print(f"  [CONSULT] All done ({consult_elapsed:.0f}s)", file=sys.stderr)

    # Step 3: Build combined output
    combined = build_combined_output(inquiry_text, inquiry_title, questions, results)

    output_path = args.output or str(
        output_dir / "answers.md"
    )
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(combined)

    total_elapsed = time.time() - total_start

    # Summary
    print(f"", file=sys.stderr)
    print(f"  {'='*50}", file=sys.stderr)
    print(f"  EXPERT CONSULTATION COMPLETE", file=sys.stderr)
    print(f"  {'='*50}", file=sys.stderr)
    print(f"  Questions: {len(questions)} ({nelson_qs} nelson, {gregory_qs} gregory)",
          file=sys.stderr)
    print(f"  Decompose: {consult_start - total_start:.0f}s", file=sys.stderr)
    print(f"  Consultations: {consult_elapsed:.0f}s (parallel)", file=sys.stderr)
    print(f"  Total: {total_elapsed:.0f}s ({total_elapsed/60:.1f}min)", file=sys.stderr)

    with _usage_lock:
        if _total_usage["calls"] > 0:
            print(f"  Decompose cost: ${_total_usage['cost_usd']:.4f}",
                  file=sys.stderr)

    print(f"  Output: {output_path}", file=sys.stderr)
    print(f"  Log dir: {output_dir}", file=sys.stderr)

    # Print the output file path to stdout (for pipeline consumption)
    print(str(Path(output_path).resolve()))


if __name__ == "__main__":
    main()
