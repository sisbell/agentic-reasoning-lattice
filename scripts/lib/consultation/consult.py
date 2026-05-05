#!/usr/bin/env python3
"""Shared consultation operation primitives.

Channel plugins under channels/<name>/consultations/consult.py use
`invoke_claude`, `parse_numbered`, and `format_out_of_scope_block` to
build their own generate_questions and consult functions. Pipeline
orchestrators use `load_channel_plugin` to resolve a channel name to
its plugin module and call its methods directly.

`invoke_claude` here is a thin wrapper around lib.shared.invoke_claude
that adds consult-specific side effects (output_file write, USAGE_LOG
append, process-local usage accumulator update).
"""

import importlib.util
import sys
from pathlib import Path

from lib.shared.common import log_usage
from lib.shared.invoke_claude import (
    _accumulate_usage,
    invoke_claude as _shared_invoke_claude,
)
from lib.shared.paths import CHANNELS_DIR, load_channel_meta


def invoke_claude(prompt, model="opus", effort=None, allow_tools=False,
                  cwd=None, output_file=None, skill="consult", label=""):
    """Call claude --print with consult-specific side effects.

    Thin wrapper around lib.shared.invoke_claude.invoke_claude that also:
      - writes the answer (or [FAILED]) to `output_file` if given
      - appends a usage entry to USAGE_LOG under `skill`
      - updates the process-local usage accumulator

    Returns the same Result that shared.invoke_claude returns. Callers
    typically read .text.
    """
    response = _shared_invoke_claude(
        prompt,
        model=model,
        effort=effort,
        cwd=cwd,
        omit_tools=allow_tools,
    )

    prefix = f"[{label}] " if label else ""

    if not response.ok:
        if output_file:
            output_file.write_text("[FAILED]\n")
        return response

    inp = response.usage["input_tokens"]
    out = response.usage["output_tokens"]
    cost = response.cost

    print(
        f"  {prefix}[{response.elapsed:.0f}s] in:{inp} out:{out} ${cost:.4f}",
        file=sys.stderr,
    )

    if output_file:
        output_file.write_text(response.text)

    log_usage(skill, response.elapsed,
              input_tokens=inp, output_tokens=out, cost_usd=cost)
    _accumulate_usage(inp, out, cost)

    return response


def parse_numbered(response, tags_to_strip=()):
    """Parse numbered lines (`1. foo`, `2. bar`) into a list of strings.
    Optionally strips leading authority tags like `[nelson]` or `[gregory]`
    if they appear. Returns the trimmed question strings."""
    questions = []
    for line in response.strip().split("\n"):
        line = line.strip()
        if not line or not (line[0].isdigit() and "." in line[:4]):
            continue
        q = line.split(".", 1)[1].strip()
        for tag in tags_to_strip:
            if q.startswith(tag):
                q = q[len(tag):].strip()
                break
        questions.append(q)
    return questions


def format_out_of_scope_block(out_of_scope):
    """Format the scope-exclusion block injected into generate-questions prompts."""
    if not out_of_scope:
        return ""
    return f"\n## Scope Exclusions\n\nDO NOT generate questions about: {out_of_scope}\n"


_plugin_cache = {}


def load_channel_plugin(channel_name):
    """Construct or load the channel plugin, dispatching on `meta.yaml.shape`.

    Returns an object exposing:
      generate_questions(inquiry, n=10, model="opus", out_of_scope="") -> list[str]
      consult(question, label="", model="opus", effort="max") -> str

    For `shape: flat-corpus` (and any other registered shape) the plugin
    is constructed directly from `meta.yaml` + the channel's standard
    paths — no per-channel Python required. For `shape: custom` the
    runtime loads `consultations/consult.py` as a module.

    Cached per process so the corpus and prompt-template caches are
    shared across calls within a decompose run.
    """
    if channel_name in _plugin_cache:
        return _plugin_cache[channel_name]

    channel_dir = CHANNELS_DIR / channel_name
    meta = load_channel_meta(channel_name)
    shape = meta.get("shape")

    if shape != "custom":
        from lib.consultation.patterns import build_plugin
        plugin = build_plugin(meta, channel_dir)
        _plugin_cache[channel_name] = plugin
        return plugin

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
    _plugin_cache[channel_name] = mod
    return mod
