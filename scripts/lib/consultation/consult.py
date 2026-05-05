#!/usr/bin/env python3
"""Consult-specific operation primitives.

`invoke_claude` is a thin wrapper around lib.shared.invoke_claude that
adds consult-side effects (output_file write, USAGE_LOG append,
process-local usage accumulator update). `parse_numbered` and
`format_out_of_scope_block` are small helpers used by channel plugins
and plugin.build_channel_plugin to assemble consult-style prompts and parse
the responses.

Plugin loading lives next door in lib.consultation.plugin.
"""

import sys

from lib.shared.common import log_usage
from lib.shared.invoke_claude import (
    _accumulate_usage,
    invoke_claude as _shared_invoke_claude,
)


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


