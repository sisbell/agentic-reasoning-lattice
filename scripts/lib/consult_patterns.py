"""Consultation-shape patterns — factories used by channel plugins.

Each factory returns a (generate_questions, consult) pair matching the
channel-plugin interface. Channels sharing a consultation shape (e.g.
flat-corpus single-invocation) opt in by importing and calling the
factory with their specific paths and metadata.

Channels whose shape is unique (Nelson's multi-section template, Gregory's
parallel KB+code workflow) write their own consult.py from scratch and do
not use any factory here.

Extract a new pattern only when a second channel needs the same shape.
"""

import sys

from lib.shared.common import read_file, concat_md_files
from lib.consult import (
    invoke_claude,
    parse_numbered,
    format_out_of_scope_block,
)


def flat_corpus(
    resources_dir,
    answer_prompt,
    gen_questions_prompt,
    role_label,
    channel_name,
):
    """Build a (generate_questions, consult) pair for a flat-corpus channel.

    Channel shape: a single directory of .md source files concatenated into
    a {{corpus}} slot in the answer prompt; generate-questions uses an
    {inquiry, num_questions, out_of_scope} slot set (optionally also
    {corpus} — injected harmlessly if the template doesn't reference it).

    Arguments:
      resources_dir: Path to the channel's resources/ directory
      answer_prompt: Path to the channel's consultations/answer.md template
      gen_questions_prompt: Path to consultations/generate-questions.md
      role_label: 'theory' or 'evidence' — used in skill tags and debug
      channel_name: the channel's identity string, for logs

    Returns (generate_questions, consult) — two pure functions.
    """
    # Process-local caches: the corpus and templates are static within a
    # process. Repeated calls (common in a decompose run with N questions)
    # reuse both.
    _corpus_cache = [None]
    _template_cache = {}

    def _corpus():
        if _corpus_cache[0] is None:
            corpus = concat_md_files(resources_dir)
            if not corpus:
                raise RuntimeError(
                    f"{role_label} corpus is empty at {resources_dir} — "
                    f"add .md source files before running consultations")
            _corpus_cache[0] = corpus
        return _corpus_cache[0]

    def _template(path):
        if path not in _template_cache:
            _template_cache[path] = read_file(path)
        return _template_cache[path]

    def generate_questions(inquiry, n=10, model="opus", out_of_scope=""):
        template = _template(gen_questions_prompt)
        if not template:
            print(f"  [ERROR] {gen_questions_prompt.name} not found",
                  file=sys.stderr)
            sys.exit(1)

        prompt = template.format(
            inquiry=inquiry,
            corpus=_corpus(),
            num_questions=n,
            out_of_scope=format_out_of_scope_block(out_of_scope),
        )

        print(f"  [DECOMPOSE:{role_label}:{channel_name}] {n} questions, "
              f"{len(prompt) // 1024}KB prompt...", file=sys.stderr)
        text, _ = invoke_claude(
            prompt, model=model,
            skill=f"pre-consult:{role_label}", label=role_label)
        return parse_numbered(text)

    def consult(question, label="", model="opus", effort="max"):
        template = _template(answer_prompt)
        if not template:
            print(f"  prompt template not found: {answer_prompt}",
                  file=sys.stderr)
            sys.exit(1)
        prompt = (template
                  .replace("{{corpus}}", _corpus())
                  .replace("{{question}}", question))

        print(f"  [{label}] Prompt: {len(prompt) // 1024}KB", file=sys.stderr)
        skill = f"consult:{label}" if label else f"consult:{role_label}"
        text, _ = invoke_claude(
            prompt, model=model, effort=effort, allow_tools=False,
            skill=skill, label=label)
        return text

    return generate_questions, consult
