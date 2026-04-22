"""Nelson theory channel — multi-section corpus consultation plugin.

Nelson's consultation assembles a 5-slot prompt from structured sources:
xanadu-concepts/ and nelson-intent/ (flat .md dirs, concatenated), plus
Literary Machines table-of-contents.md, inventory.md, and an optional
page-image directory pointer (when --with-png is passed through).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
from lib.shared.common import read_file
from lib.consult import (
    invoke_claude as _invoke,
    parse_numbered,
    format_out_of_scope_block,
)

HERE = Path(__file__).parent
CHANNEL = HERE.parent
RESOURCES = CHANNEL / "resources"

ANSWER_PROMPT = HERE / "answer.md"
GEN_QUESTIONS_PROMPT = HERE / "generate-questions.md"

CONCEPTS_DIR = RESOURCES / "xanadu-concepts"
INTENT_DIR = RESOURCES / "nelson-intent"
LM_TOC = RESOURCES / "literary-machines" / "table-of-contents.md"
LM_INVENTORY = RESOURCES / "literary-machines" / "inventory.md"
LM_RAW_DIR = RESOURCES / "literary-machines" / "raw"

CHANNEL_NAME = "nelson"
ROLE_LABEL = "theory"

_cache = {}


def _concat_md_files(directory):
    """Flat-only concat. Distinct from lib.shared.common.concat_md_files
    (which recurses) — Nelson's concept/intent dirs assume flat layout."""
    return "\n\n".join(
        f"### {f.stem}\n{f.read_text()}"
        for f in sorted(directory.glob("*.md"))
    )


def _cached(key, loader):
    if key not in _cache:
        _cache[key] = loader()
    return _cache[key]


def _build_answer_prompt(question, with_png=False):
    template = _cached("tmpl-answer", lambda: read_file(ANSWER_PROMPT))
    if not template:
        print(f"  prompt template not found: {ANSWER_PROMPT}", file=sys.stderr)
        sys.exit(1)
    raw_dir = str(LM_RAW_DIR) if with_png else ""
    return (template
            .replace("{{concepts}}",
                     _cached("concepts", lambda: _concat_md_files(CONCEPTS_DIR)))
            .replace("{{intent}}",
                     _cached("intent", lambda: _concat_md_files(INTENT_DIR)))
            .replace("{{toc}}",
                     _cached("toc", lambda: read_file(LM_TOC)))
            .replace("{{inventory}}",
                     _cached("inventory", lambda: read_file(LM_INVENTORY)))
            .replace("{{raw_dir}}", raw_dir)
            .replace("{{question}}", question))


def generate_questions(inquiry, n=10, model="opus", out_of_scope=""):
    template = _cached("tmpl-gq", lambda: read_file(GEN_QUESTIONS_PROMPT))
    if not template:
        print(f"  [ERROR] {GEN_QUESTIONS_PROMPT.name} not found",
              file=sys.stderr)
        sys.exit(1)

    prompt = template.format(
        inquiry=inquiry,
        num_questions=n,
        out_of_scope=format_out_of_scope_block(out_of_scope),
    )

    print(f"  [DECOMPOSE:{ROLE_LABEL}:{CHANNEL_NAME}] {n} questions, "
          f"{len(prompt) // 1024}KB prompt...", file=sys.stderr)
    text, _ = _invoke(
        prompt, model=model,
        skill=f"pre-consult:{CHANNEL_NAME}", label=CHANNEL_NAME)
    return parse_numbered(text, tags_to_strip=(f"[{CHANNEL_NAME}]",))


def consult(question, label="", model="opus", effort="max",
            with_png=False, **_):
    prompt = _build_answer_prompt(question, with_png=with_png)
    print(f"  [{label}] Prompt: {len(prompt) // 1024}KB", file=sys.stderr)
    skill = f"consult:{label}" if label else f"consult:{CHANNEL_NAME}"
    text, _ = _invoke(
        prompt, model=model, effort=effort, allow_tools=with_png,
        skill=skill, label=label)
    return text
