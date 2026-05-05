"""Channel plugin loader + built-in factories.

`load_channel_plugin(name)` is the entry point: looks up the channel's
meta.yaml, builds (or importlib-loads) the plugin, caches the result.

`build_channel_plugin(meta, channel_dir)` dispatches on `meta['shape']`:
  - `custom`:      importlib-load `channel_dir/consultations/consult.py`
  - `flat-corpus`: build a plugin in-memory via the `flat_corpus` factory
                   (single resources/ dir + answer/generate-questions
                   prompts; used by maxwell-1867, dulong-petit-1819)
  - otherwise:     ValueError

Add a new shape only when a second channel needs the same one.
"""

import importlib.util
import sys
from types import SimpleNamespace

from lib.consultation.consult import (
    invoke_claude, parse_numbered, format_out_of_scope_block,
)
from lib.shared.common import concat_md_files, read_file
from lib.shared.paths import CHANNELS_DIR, load_channel_meta


_plugin_cache = {}


def load_channel_plugin(channel_name):
    """Return the plugin object for `channel_name`. Per-process cached."""
    if channel_name in _plugin_cache:
        return _plugin_cache[channel_name]
    channel_dir = CHANNELS_DIR / channel_name
    meta = load_channel_meta(channel_name)
    plugin = build_channel_plugin(meta, channel_dir)
    _plugin_cache[channel_name] = plugin
    return plugin


def build_channel_plugin(meta, channel_dir):
    """Construct a plugin from meta + channel_dir based on meta['shape'].

    Returns an object exposing
      generate_questions(inquiry, n=10, model="opus", out_of_scope="") -> list[str]
      consult(question, label="", model="opus", effort="max") -> str
    """
    shape = meta.get("shape")
    if shape is None:
        raise ValueError(
            f"channel {meta.get('name', '?')!r} meta.yaml is missing the "
            f"`shape:` field; expected one of ['flat-corpus', 'custom']"
        )
    if shape == "custom":
        return _load_custom(channel_dir, meta.get("name", "?"))
    if shape == "flat-corpus":
        return _build_flat_corpus(meta, channel_dir)
    raise ValueError(
        f"channel {meta.get('name', '?')!r} declares unknown shape "
        f"{shape!r}; expected one of ['flat-corpus', 'custom']"
    )


def _load_custom(channel_dir, channel_name):
    path = channel_dir / "consultations" / "consult.py"
    if not path.exists():
        raise FileNotFoundError(
            f"channel {channel_name!r} declares shape: custom but "
            f"{path} does not exist"
        )
    spec = importlib.util.spec_from_file_location(
        f"channels.{channel_name}.consult", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _build_flat_corpus(meta, channel_dir):
    consultations = channel_dir / "consultations"
    gen_q, consult_fn = flat_corpus(
        resources_dir=channel_dir / "resources",
        answer_prompt=consultations / "answer.md",
        gen_questions_prompt=consultations / "generate-questions.md",
        role_label=meta["role_hint"],
        channel_name=meta["name"],
    )
    return SimpleNamespace(generate_questions=gen_q, consult=consult_fn)


def flat_corpus(
    resources_dir,
    answer_prompt,
    gen_questions_prompt,
    role_label,
    channel_name,
):
    """Build a (generate_questions, consult) pair for a flat-corpus channel.

    Channel shape: a single directory of .md source files concatenated
    into a {{corpus}} slot in the answer prompt; generate-questions uses
    an {inquiry, num_questions, out_of_scope} slot set (optionally also
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
        response = invoke_claude(
            prompt, model=model,
            skill=f"pre-consult:{role_label}", label=role_label)
        return parse_numbered(response.text)

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
        return invoke_claude(
            prompt, model=model, effort=effort, allow_tools=False,
            skill=skill, label=label).text

    return generate_questions, consult
