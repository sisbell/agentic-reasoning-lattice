#!/usr/bin/env python3
"""Shared utilities for per-domain consultation scripts.

Each domain's consult_theory.py and consult_evidence.py import from here.
This module holds only the engine-level primitives that don't vary by
domain: Claude CLI invocation, token/cost extraction, usage-log append.

Domain-specific logic (source loading, prompt composition, role identity)
lives in the per-domain scripts, not here.
"""

import json
import os
import subprocess
import sys
import threading
import time

from lib.shared.common import MODEL_FLAGS, log_usage


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
