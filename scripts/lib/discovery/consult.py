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

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import WORKSPACE, EXPERTS_DIR, USAGE_LOG, load_manifest, load_excluded_covers

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "discovery" / "consultation"
TEST_HARNESS = WORKSPACE / "udanax-test-harness"
KB_SYNTHESIS = TEST_HARNESS / "knowledge-base" / "kb-synthesis.md"

# Nelson source paths
CONCEPTS_DIR = WORKSPACE / "nelson" / "xanadu-concepts"
INTENT_DIR = WORKSPACE / "nelson" / "nelson-intent"
LM_TOC = WORKSPACE / "nelson" / "literary-machines" / "table-of-contents.md"
LM_INVENTORY = WORKSPACE / "nelson" / "literary-machines" / "inventory.md"
NELSON_PROMPT_TEMPLATE = PROMPTS_DIR / "nelson" / "answer.md"

# Gregory source paths
KB_FORMAL = TEST_HARNESS / "knowledge-base" / "kb-formal.md"
GREGORY_KB_TEMPLATE = PROMPTS_DIR / "gregory" / "answer-from-kb.md"
GREGORY_CODE_TEMPLATE = PROMPTS_DIR / "gregory" / "answer-from-code.md"

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
    """Load inquiry from project model manifest."""
    manifest = load_manifest(inquiry_id)
    if not manifest:
        print(f"  [ERROR] Manifest not found for ASN-{inquiry_id:04d}", file=sys.stderr)
        sys.exit(1)
    inquiry = manifest.get("consultations", {})
    # Flatten for backward compatibility: callers expect top-level keys
    return {
        "id": inquiry_id,
        "title": manifest.get("title", ""),
        "question": inquiry.get("question", ""),
        "out_of_scope": manifest.get("out_of_scope", ""),
        "agents": inquiry.get("agents", {}),
    }




# ─── Step 1: Decompose ──────────────────────────────────────────

def _call_decompose(prompt, label, model="opus"):
    """Call claude --print for question generation. Returns response text."""
    model_flag = {
        "opus": "claude-opus-4-7",
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
        timeout=None,
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


def filter_questions(inquiry_text, out_of_scope, questions, covers_text=""):
    """Filter questions for scope using a cheap LLM call. Returns filtered list."""
    template = read_file(WORKSPACE / "scripts" / "prompts" / "discovery" / "consultation" / "filter-questions.md")
    if not template:
        print("  [WARN] filter-questions.md not found, skipping filter",
              file=sys.stderr)
        return questions

    questions_text = "\n".join(
        f"{i}. [{a}] {q}" for i, (a, q) in enumerate(questions, 1)
    )
    foundation_block = (
        f"## Already Established\n\n"
        f"The following topics are already covered by upstream ASNs. "
        f"Drop questions whose answers are already established:\n\n{covers_text}"
        if covers_text else ""
    )
    prompt = template.format(
        inquiry=inquiry_text,
        out_of_scope=out_of_scope,
        foundation_block=foundation_block,
        questions=questions_text,
    )

    print(f"  [FILTER] Checking {len(questions)} questions against exclusions...",
          file=sys.stderr)
    response = _call_decompose(prompt, "filter", model="opus")

    if not response:
        print("  [FILTER] No response, keeping all questions", file=sys.stderr)
        return questions

    # Parse KEEP/DROP lines
    keep_indices = set()
    for line in response.strip().split("\n"):
        line = line.strip()
        if line.startswith("KEEP"):
            try:
                idx = int(line.split()[1])
                keep_indices.add(idx)
            except (IndexError, ValueError):
                pass

    if not keep_indices:
        print("  [FILTER] No KEEP lines parsed, keeping all questions",
              file=sys.stderr)
        return questions

    filtered = [q for i, q in enumerate(questions, 1) if i in keep_indices]
    dropped = len(questions) - len(filtered)
    if dropped:
        print(f"  [FILTER] Dropped {dropped} out-of-scope questions, "
              f"keeping {len(filtered)}", file=sys.stderr)
    else:
        print(f"  [FILTER] All {len(filtered)} questions in scope",
              file=sys.stderr)

    return filtered


def decompose_inquiry(inquiry_text, num_nelson=10, num_gregory=10, model="opus",
                      out_of_scope="", asn_id=None):
    """Two-pass decompose: Nelson (design vocabulary) then Gregory (with KB context).

    Nelson questions use design vocabulary only — no implementation contamination.
    Gregory questions use KB vocabulary for precise technical questions.
    """
    # Pass 1: Nelson questions (inquiry only, no KB)
    nelson_template = read_file(PROMPTS_DIR / "nelson" / "generate-questions.md")
    if not nelson_template:
        print("  [ERROR] nelson/generate-questions.md not found",
              file=sys.stderr)
        sys.exit(1)

    covers_text = load_excluded_covers(asn_id) if asn_id else ""
    out_of_scope_block = (f"\n## Scope Exclusions\n\nDO NOT generate questions about: {out_of_scope}\n"
                     if out_of_scope else "")
    nelson_prompt = nelson_template.format(
        inquiry=inquiry_text,
        num_questions=num_nelson,
        out_of_scope=out_of_scope_block,
    )

    print(f"  [DECOMPOSE:nelson] {num_nelson} questions, "
          f"{len(nelson_prompt) // 1024}KB prompt...", file=sys.stderr)
    nelson_response = _call_decompose(nelson_prompt, "nelson", model=model)

    # Pass 2: Gregory questions (inquiry + KB synthesis)
    gregory_template = read_file(PROMPTS_DIR / "gregory" / "generate-questions.md")
    if not gregory_template:
        print("  [ERROR] gregory/generate-questions.md not found",
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
        out_of_scope=out_of_scope_block,
    )

    print(f"  [DECOMPOSE:gregory] {num_gregory} questions, "
          f"{len(gregory_prompt) // 1024}KB prompt...", file=sys.stderr)
    gregory_response = _call_decompose(gregory_prompt, "gregory", model=model)

    # Parse both
    nelson_qs = parse_questions(nelson_response, "nelson") if nelson_response else []
    gregory_qs = parse_questions(gregory_response, "gregory") if gregory_response else []

    all_qs = nelson_qs + gregory_qs

    # Filter for scope and upstream coverage (safety net)
    if (out_of_scope or covers_text) and all_qs:
        all_qs = filter_questions(inquiry_text, out_of_scope, all_qs,
                                  covers_text=covers_text)

    return all_qs


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


# ─── Step 2: Consult (inlined expert logic) ─────────────────────

def _invoke_claude(prompt, model="opus", effort=None, allow_tools=False,
                   cwd=None, label=""):
    """Call claude --print, parse JSON, track usage. Returns response text."""
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
        cwd=cwd, timeout=None,
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  [{label}] FAILED (exit {result.returncode}, {elapsed:.0f}s)",
              file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:3]:
                print(f"    {line}", file=sys.stderr)
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

        print(f"  [{label}] {elapsed:.0f}s | in:{inp} out:{out} ${cost:.4f}",
              file=sys.stderr)

        with _usage_lock:
            _total_usage["input_tokens"] += inp
            _total_usage["output_tokens"] += out
            _total_usage["cost_usd"] += cost
            _total_usage["calls"] += 1

        log_usage(f"consult:{label}", elapsed, inp, out, cost)

        return text
    except (json.JSONDecodeError, KeyError):
        print(f"  [{label}] {elapsed:.0f}s [parse error]", file=sys.stderr)
        return result.stdout


def _all_concepts():
    """Read all curated concept files."""
    files = sorted(CONCEPTS_DIR.glob("*.md"))
    parts = []
    for f in files:
        parts.append(f"### {f.stem}\n{f.read_text()}")
    return "\n\n".join(parts)


def _all_intent():
    """Read all design intent files."""
    files = sorted(INTENT_DIR.glob("*.md"))
    parts = []
    for f in files:
        parts.append(f"### {f.stem}\n{f.read_text()}")
    return "\n\n".join(parts)


def _build_nelson_prompt(question):
    """Build Nelson prompt from template + curated sources (no --with-png in batch)."""
    template = read_file(NELSON_PROMPT_TEMPLATE)
    if not template:
        print("  [ERROR] nelson-agent.md prompt template not found", file=sys.stderr)
        sys.exit(1)
    return template.replace(
        "{{concepts}}", _all_concepts()
    ).replace(
        "{{intent}}", _all_intent()
    ).replace(
        "{{toc}}", read_file(LM_TOC)
    ).replace(
        "{{inventory}}", read_file(LM_INVENTORY)
    ).replace(
        "{{raw_dir}}", ""
    ).replace(
        "{{question}}", question
    )


def _build_gregory_kb_prompt(question):
    """Build Gregory KB synthesis prompt from template + injected KB."""
    template = read_file(GREGORY_KB_TEMPLATE)
    kb = read_file(KB_FORMAL)
    if not template:
        print("  [ERROR] gregory-synthesis-agent.md prompt template not found",
              file=sys.stderr)
        sys.exit(1)
    if not kb:
        print("  [ERROR] kb-formal.md not found", file=sys.stderr)
        sys.exit(1)
    return template.replace("{{kb}}", kb).replace("{{question}}", question)


def _build_gregory_code_prompt(question):
    """Build Gregory code exploration prompt from template."""
    template = read_file(GREGORY_CODE_TEMPLATE)
    if not template:
        print("  [ERROR] gregory-code-agent.md prompt template not found",
              file=sys.stderr)
        sys.exit(1)
    return template.replace("{{question}}", question)


def _run_nelson(question, question_num, model="opus", effort="max"):
    """Build prompt, call claude. Returns answer text."""
    label = f"Q{question_num}:nelson"

    print(f"  [{label}] Building prompt...", file=sys.stderr)
    prompt = _build_nelson_prompt(question)
    print(f"  [{label}] Prompt: {len(prompt) // 1024}KB", file=sys.stderr)

    return _invoke_claude(
        prompt, model=model, effort=effort, allow_tools=False, label=label,
    )


def _run_gregory_kb(question, label, model="sonnet", effort="max"):
    """KB synthesis call — no tools, pure synthesis from injected KB."""
    prompt = _build_gregory_kb_prompt(question)
    print(f"  [{label}:kb] Prompt: {len(prompt) // 1024}KB", file=sys.stderr)
    return _invoke_claude(
        prompt, model=model, effort=effort, allow_tools=False,
        label=f"{label}:kb",
    )


def _run_gregory_code(question, label, model="sonnet", effort="max"):
    """Code exploration call — tools enabled, cwd=test harness."""
    prompt = _build_gregory_code_prompt(question)
    print(f"  [{label}:code] Prompt: {len(prompt) // 1024}KB", file=sys.stderr)
    return _invoke_claude(
        prompt, model=model, effort=effort, allow_tools=True,
        cwd=str(TEST_HARNESS), label=f"{label}:code",
    )


def _run_gregory(question, question_num, model="sonnet", effort="max"):
    """Run KB + code in parallel. Returns combined text."""
    label = f"Q{question_num}:gregory"

    print(f"  [{label}] Starting KB + code in parallel...", file=sys.stderr)

    kb_result = [None]
    code_result = [None]

    def run_kb():
        kb_result[0] = _run_gregory_kb(question, label, model=model, effort=effort)

    def run_code():
        code_result[0] = _run_gregory_code(question, label, model=model, effort=effort)

    kb_thread = threading.Thread(target=run_kb)
    code_thread = threading.Thread(target=run_code)

    kb_thread.start()
    code_thread.start()
    kb_thread.join()
    code_thread.join()

    # Combine KB + code answers
    parts = []
    if kb_result[0]:
        parts.append(f"## KB Synthesis\n\n{kb_result[0]}")
    if code_result[0]:
        parts.append(f"## Code Exploration\n\n{code_result[0]}")

    combined = "\n\n---\n\n".join(parts) if parts else "[No answer]"
    print(f"  [{label}] Done", file=sys.stderr)
    return combined


def _answer_path(consult_dir, index, authority):
    """Path for an individual answer file: answer-01-nelson.md"""
    return consult_dir / f"answer-{index + 1:02d}-{authority}.md"


def _save_answer(consult_dir, index, authority, question, answer):
    """Save a single answer to disk immediately."""
    path = _answer_path(consult_dir, index, authority)
    content = (f"## Question {index + 1} [{authority}]\n\n"
               f"> {question}\n\n"
               f"{answer.strip() if answer else '[No answer]'}\n")
    path.write_text(content)
    print(f"  [SAVED] {path.name}", file=sys.stderr)


def _load_existing_answers(consult_dir, questions):
    """Load answers already on disk. Returns dict of index → (authority, question, answer).

    Extracts the answer body (after the question header) to avoid
    double-wrapping when build_combined_output adds its own headers.
    """
    existing = {}
    for i, (authority, question) in enumerate(questions):
        path = _answer_path(consult_dir, i, authority)
        if path.exists():
            raw = path.read_text()
            # Strip the header we added (## Question N, > question, blank lines)
            # Answer body starts after the first blank line following ">"
            lines = raw.split("\n")
            body_start = 0
            found_quote = False
            for j, line in enumerate(lines):
                if line.startswith(">"):
                    found_quote = True
                elif found_quote and line.strip() == "":
                    body_start = j + 1
                    break
            answer = "\n".join(lines[body_start:]).strip()
            existing[i] = (authority, question, answer)
            print(f"  [CACHED] answer-{i + 1:02d}-{authority}.md", file=sys.stderr)
    return existing


def run_consultations(questions, consult_dir, nelson_model="opus",
                      gregory_model="sonnet", effort="max"):
    """Run all consultations. Nelson in parallel, Gregory sequentially.

    Saves each answer to disk as it completes. Skips questions that
    already have answer files (resume support).

    Nelson: no tools, safe to parallelize.
    Gregory: each call runs KB + code in parallel internally.
    Run Gregory sequentially because code exploration uses tools.
    """
    results = [None] * len(questions)

    # Load existing answers (resume support)
    existing = _load_existing_answers(consult_dir, questions)
    for i, cached in existing.items():
        results[i] = cached

    skipped = len(existing)
    if skipped:
        print(f"  [RESUME] Skipping {skipped} already-completed questions",
              file=sys.stderr)

    # Split by authority, excluding already-completed
    nelson_indices = [i for i, (a, _) in enumerate(questions)
                      if a == "nelson" and i not in existing]
    gregory_indices = [i for i, (a, _) in enumerate(questions)
                       if a == "gregory" and i not in existing]

    # Nelson in parallel
    if nelson_indices:
        print(f"  [NELSON] Firing {len(nelson_indices)} calls in parallel...",
              file=sys.stderr)
        threads = []

        for i in nelson_indices:
            authority, question = questions[i]
            def run_n(idx=i, q=question, auth=authority):
                answer = _run_nelson(q, idx + 1,
                                     model=nelson_model, effort=effort)
                results[idx] = (auth, q, answer)
                _save_answer(consult_dir, idx, auth, q, answer)
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
            answer = _run_gregory(question, i + 1,
                                  model=gregory_model, effort=effort)
            results[i] = (authority, question, answer)
            _save_answer(consult_dir, i, authority, question, answer)

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
                        help="Output file path (default: vault/0-consultations/ASN-NNNN/consultation/answers.md)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Generate and save questions, don't run consultations")
    parser.add_argument("--regenerate", action="store_true",
                        help="Regenerate questions even if a saved questions file exists")
    args = parser.parse_args()

    # Load inquiry
    inquiry_title = "Ad-hoc inquiry"
    asn_label = "adhoc"
    num_nelson = 10
    num_gregory = 10
    out_of_scope = ""
    asn_id = None
    if args.inquiry_id:
        inquiry = load_inquiry(args.inquiry_id)
        inquiry_text = inquiry["question"]
        inquiry_title = inquiry["title"]
        asn_label = f"{args.inquiry_id:04d}"
        asn_id = args.inquiry_id
        out_of_scope = inquiry.get("out_of_scope", "")
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

    # Check for existing questions file (editable by user)
    existing_questions_path = EXPERTS_DIR / f"ASN-{asn_label}" / "consultation" / "questions.md"
    if not args.dry_run and existing_questions_path.exists() and not args.regenerate:
        print(f"  [LOAD] Using existing questions from {existing_questions_path.relative_to(WORKSPACE)}",
              file=sys.stderr)
        existing_text = existing_questions_path.read_text()
        questions = parse_questions(existing_text)
    else:
        # Step 1: Decompose (two-pass: Nelson design vocab, Gregory with KB)
        questions = decompose_inquiry(inquiry_text,
                                      num_nelson=num_nelson,
                                      num_gregory=num_gregory,
                                      model=args.model,
                                      out_of_scope=out_of_scope,
                                      asn_id=asn_id)

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

    # Save questions
    output_dir = EXPERTS_DIR / f"ASN-{asn_label}"
    init_dir = output_dir / "consultation"
    init_dir.mkdir(parents=True, exist_ok=True)
    questions_path = init_dir / "questions.md"
    questions_text = "\n".join(
        f"{i}. [{a}] {q}" for i, (a, q) in enumerate(questions, 1)
    )
    questions_path.write_text(
        f"# Sub-Questions — {inquiry_title}\n\n"
        f"**Inquiry:** {inquiry_text}\n\n"
        f"{questions_text}\n"
    )
    print(f"  [SAVED] {questions_path.relative_to(WORKSPACE)}", file=sys.stderr)

    if args.dry_run:
        for i, (authority, q) in enumerate(questions, 1):
            print(f"{i}. [{authority}] {q}")
        return

    print(f"  [CONSULT] Firing {len(questions)} consultations...",
          file=sys.stderr)
    consult_start = time.time()
    results = run_consultations(questions, init_dir)
    consult_elapsed = time.time() - consult_start
    print(f"  [CONSULT] All done ({consult_elapsed:.0f}s)", file=sys.stderr)

    # Step 3: Build combined output
    combined = build_combined_output(inquiry_text, inquiry_title, questions, results)

    output_path = args.output or str(
        init_dir / "answers.md"
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
            print(f"  Total cost: ${_total_usage['cost_usd']:.4f} "
                  f"({_total_usage['calls']} calls)",
                  file=sys.stderr)

    print(f"  Output: {output_path}", file=sys.stderr)
    print(f"  Log dir: {output_dir}", file=sys.stderr)

    # Print the output file path to stdout (for pipeline consumption)
    print(str(Path(output_path).resolve()))


if __name__ == "__main__":
    main()
