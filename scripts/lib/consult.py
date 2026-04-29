#!/usr/bin/env python3
"""Shared consultation operation primitives.

The atomic verb: consult one channel with one question. Channel plugins
under channels/<name>/consultations/consult.py use the primitives here
(invoke_claude, parse_numbered, format_out_of_scope_block) to build their
own generate_questions and consult functions. Pipeline orchestrators use
load_channel_plugin to resolve a channel name to its plugin module and
dispatch_* to route calls through it.

This module holds only engine-level primitives that don't vary by channel:
Claude CLI invocation, token/cost extraction, usage-log append, session-
dir numbering, channel-arg resolution.
"""

import importlib.util
import json
import os
import re
import subprocess
import sys
import threading
import time
from pathlib import Path

from lib.shared.common import MODEL_FLAGS, log_usage
from lib.shared.campaign import resolve_campaign
from lib.shared.paths import WORKSPACE, CHANNELS_DIR, load_channel_meta


# Process-local usage accumulator. Every invoke_claude call updates it
# under _usage_lock. Readers (e.g. the full-discovery orchestrator) can
# read the dict at any point to print a cross-call total.
_total_usage = {"input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0, "calls": 0}
_usage_lock = threading.Lock()


def reset_total_usage():
    """Zero the process-local usage accumulator."""
    with _usage_lock:
        _total_usage["input_tokens"] = 0
        _total_usage["output_tokens"] = 0
        _total_usage["cost_usd"] = 0.0
        _total_usage["calls"] = 0


def get_total_usage():
    """Snapshot the current process-local usage totals."""
    with _usage_lock:
        return dict(_total_usage)


def invoke_claude(prompt, model="opus", effort=None, allow_tools=False,
                  cwd=None, output_file=None, skill="consult", label=""):
    """Call claude --print with pre-assembled prompt via stdin.

    Returns (text, usage) where usage is a dict with input_tokens,
    output_tokens, cost_usd, elapsed_s. On failure returns ("", zeroed-usage).

    Writes the answer to output_file if given; appends a usage entry to
    USAGE_LOG under the given skill label.
    """
    model_flag = MODEL_FLAGS.get(model, model)

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

    prefix = f"[{label}] " if label else ""

    if result.returncode != 0:
        print(f"  {prefix}FAILED (exit {result.returncode}, {elapsed:.0f}s)",
              file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:3]:
                print(f"    {line}", file=sys.stderr)
        if output_file:
            output_file.write_text(f"[FAILED: exit {result.returncode}]\n")
        return "", _zero_usage(elapsed)

    try:
        data = json.loads(result.stdout)
        text = data.get("result", "")
        usage_data = data.get("usage", {})
        cost = data.get("total_cost_usd", 0)
        inp = (usage_data.get("input_tokens", 0) +
               usage_data.get("cache_read_input_tokens", 0) +
               usage_data.get("cache_creation_input_tokens", 0))
        out = usage_data.get("output_tokens", 0)

        print(f"  {prefix}[{elapsed:.0f}s] in:{inp} out:{out} ${cost:.4f}",
              file=sys.stderr)

        if output_file:
            output_file.write_text(text)

        log_usage(skill, elapsed,
                  input_tokens=inp, output_tokens=out, cost_usd=cost)

        with _usage_lock:
            _total_usage["input_tokens"] += inp
            _total_usage["output_tokens"] += out
            _total_usage["cost_usd"] += cost
            _total_usage["calls"] += 1

        return text, {
            "input_tokens": inp,
            "output_tokens": out,
            "cost_usd": cost,
            "elapsed_s": elapsed,
        }
    except (json.JSONDecodeError, KeyError):
        print(f"  {prefix}[{elapsed:.0f}s] [no token data]", file=sys.stderr)
        text = result.stdout
        if output_file:
            output_file.write_text(text)
        return text, _zero_usage(elapsed)


def _zero_usage(elapsed):
    return {"input_tokens": 0, "output_tokens": 0, "cost_usd": 0, "elapsed_s": elapsed}


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


def next_session_dir(parent, prefix):
    """Create and return the next numbered session dir under `parent`.

    Scans for existing `{prefix}-N/` dirs, picks max(N)+1, mkdirs the result
    (and its parents). Used by consultation scripts to number per-call
    transcript dirs under lattices/<L>/discovery/consultations/. The prefix
    is typically a channel name (xanadu) or a role name (materials).
    """
    parent.mkdir(parents=True, exist_ok=True)
    pat = re.compile(rf"{re.escape(prefix)}-(\d+)$")
    next_num = 1
    for d in parent.glob(f"{prefix}-*/"):
        m = pat.search(d.name)
        if m:
            next_num = max(next_num, int(m.group(1)) + 1)
    consult_dir = parent / f"{prefix}-{next_num}"
    consult_dir.mkdir(parents=True, exist_ok=True)
    return consult_dir


def resolve_channel_from_args(args, role):
    """Pick the channel name from CLI args for a consultation script.

    `role` is 'theory' or 'evidence'. Prefers an explicit --channel, falls
    back to resolving via --asn's campaign. Exits via argparse error if
    neither is provided.
    """
    if args.channel:
        return args.channel
    if args.asn:
        return getattr(resolve_campaign(args.asn), f"{role}_channel")
    raise SystemExit(
        "error: provide --asn (to resolve via campaign) or --channel (explicit)")


_plugin_cache = {}


def dispatch_generate_questions(channel, inquiry, n, model, out_of_scope):
    """Load the channel plugin and call its generate_questions."""
    plugin = load_channel_plugin(channel)
    return plugin.generate_questions(
        inquiry, n=n, model=model, out_of_scope=out_of_scope)


def dispatch_run_consultation(channel, question, label, model, effort, **extra):
    """Load the channel plugin and call its consult."""
    plugin = load_channel_plugin(channel)
    return plugin.consult(
        question, label=label, model=model, effort=effort, **extra)


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
        from lib.consult_patterns import build_plugin
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
