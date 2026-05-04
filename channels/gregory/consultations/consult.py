"""Gregory evidence channel — parallel KB+code consultation plugin.

Gregory runs two independent Claude invocations in parallel per question:
  1. KB agent — prompt + injected knowledge-base synthesis, no tools
  2. Code agent — prompt with cwd set to the test harness, tool access

Answers are combined (## KB Synthesis / ## Code Exploration) into one string.

generate_questions injects the KB synthesis as context so decomposed
questions target vocabulary that actually appears in the implementation.
"""

import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
from lib.shared.paths import WORKSPACE
from lib.shared.common import read_file
from lib.consultation.consult import (
    invoke_claude as _invoke,
    parse_numbered,
    format_out_of_scope_block,
)

HERE = Path(__file__).parent
CHANNEL = HERE.parent
RESOURCES = CHANNEL / "resources"

KB_PROMPT = HERE / "answer-from-kb.md"
CODE_PROMPT = HERE / "answer-from-code.md"
GEN_QUESTIONS_PROMPT = HERE / "generate-questions.md"

TEST_HARNESS = RESOURCES / "udanax-test-harness"
KB_PATH = TEST_HARNESS / "knowledge-base" / "kb-formal.md"
KB_SYNTHESIS_PATH = TEST_HARNESS / "knowledge-base" / "kb-synthesis.md"

CHANNEL_NAME = "gregory"
ROLE_LABEL = "evidence"

_cache = {}


def _cached(key, loader):
    if key not in _cache:
        _cache[key] = loader()
    return _cache[key]


def _build_kb_prompt(question):
    template = _cached("tmpl-kb", lambda: read_file(KB_PROMPT))
    kb = read_file(KB_PATH)
    if not template:
        print("  KB prompt template not found", file=sys.stderr)
        sys.exit(1)
    if not kb:
        print(f"  KB file not found at {KB_PATH.relative_to(WORKSPACE)}",
              file=sys.stderr)
        sys.exit(1)
    return template.replace("{{kb}}", kb).replace("{{question}}", question)


def _build_code_prompt(question):
    template = _cached("tmpl-code", lambda: read_file(CODE_PROMPT))
    if not template:
        print("  Code prompt template not found", file=sys.stderr)
        sys.exit(1)
    return template.replace("{{question}}", question)


def _run_kb(question, label, model, effort):
    print("  [KB]", file=sys.stderr)
    prompt = _build_kb_prompt(question)
    print(f"  Prompt: {len(prompt) // 1024}KB (~{len(prompt) // 4} tokens)",
          file=sys.stderr)
    text, _ = _invoke(
        prompt, model=model, effort=effort, allow_tools=False,
        skill=f"consult-{CHANNEL_NAME}:kb", label="kb")
    return text


def _run_code(question, label, model, effort):
    print("  [CODE]", file=sys.stderr)
    prompt = _build_code_prompt(question)
    print(f"  Prompt: {len(prompt) // 1024}KB (~{len(prompt) // 4} tokens)",
          file=sys.stderr)
    text, _ = _invoke(
        prompt, model=model, effort=effort, allow_tools=True,
        cwd=str(TEST_HARNESS),
        skill=f"consult-{CHANNEL_NAME}:code", label="code")
    return text


def generate_questions(inquiry, n=10, model="opus", out_of_scope=""):
    template = _cached("tmpl-gq", lambda: read_file(GEN_QUESTIONS_PROMPT))
    if not template:
        print(f"  [ERROR] {GEN_QUESTIONS_PROMPT.name} not found",
              file=sys.stderr)
        sys.exit(1)

    kb = read_file(KB_SYNTHESIS_PATH)
    if not kb:
        print(f"  [WARN] KB synthesis not found at "
              f"{KB_SYNTHESIS_PATH.relative_to(WORKSPACE)}", file=sys.stderr)
        kb = ""

    prompt = template.format(
        inquiry=inquiry,
        kb=kb,
        num_questions=n,
        out_of_scope=format_out_of_scope_block(out_of_scope),
    )

    print(f"  [DECOMPOSE:{CHANNEL_NAME}] {n} questions, "
          f"{len(prompt) // 1024}KB prompt...", file=sys.stderr)
    text, _ = _invoke(
        prompt, model=model,
        skill=f"pre-consult:{CHANNEL_NAME}", label=CHANNEL_NAME)
    return parse_numbered(text, tags_to_strip=(f"[{CHANNEL_NAME}]",))


def consult(question, label="", model="sonnet", effort="max",
            kb_only=False, code_only=False, **_):
    """Run KB + code in parallel (default), or just one if kb_only/code_only."""
    if kb_only:
        return _run_kb(question, label, model, effort)
    if code_only:
        return _run_code(question, label, model, effort)

    kb_result = [None]
    code_result = [None]

    def _kb():
        kb_result[0] = _run_kb(question, label, model, effort)

    def _code():
        code_result[0] = _run_code(question, label, model, effort)

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
