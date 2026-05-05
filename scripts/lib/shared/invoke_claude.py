"""Claude CLI invocation — single-turn, agent-mode, and parallel batches.

Wraps `claude --print` and `claude -p` subprocess calls with consistent
env-var setup (max output tokens, effort level, dropping CLAUDECODE),
JSON parsing, and timing. `parallel_llm_calls` runs many `invoke_*`
calls concurrently with progress logging.

Also exposes a process-local usage accumulator that callers can read
between invocations (`get_total_usage`, `reset_total_usage`). Modules
that have their own invoke_claude wrappers can update this accumulator
to keep the process-wide totals correct.
"""

import json
import os
import subprocess
import sys
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import WORKSPACE


MODEL_FLAGS = {
    "opus": "claude-opus-4-7",
    "sonnet": "claude-sonnet-4-6",
}


@dataclass
class Result:
    """Return value of every invoke_claude variant.

    Callers pick whichever fields they need:
      text     — the model's response text (data.result for json output,
                 raw stdout otherwise)
      data     — parsed JSON dict, or None when --output-format is omitted
                 or parsing failed
      elapsed  — wall time in seconds
      usage    — {"input_tokens", "output_tokens"} (zeros if no json)
      cost     — total_cost_usd from the response (0.0 if no json)
      ok       — returncode == 0 AND not data.is_error
    """
    text: str = ""
    data: dict | None = None
    elapsed: float = 0.0
    usage: dict = field(default_factory=lambda: {
        "input_tokens": 0, "output_tokens": 0,
    })
    cost: float = 0.0
    ok: bool = False


# ─── Process-local usage accumulator ────────────────────────────


# Updated by invoke_claude wrappers that opt in to tracking. Readers
# (orchestrator-level summaries) can snapshot this dict at any point
# to print a cross-call total. Thread-safe via _usage_lock.
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


def _accumulate_usage(input_tokens, output_tokens, cost_usd):
    """Update the process-local accumulator. Used by invoke_claude
    wrappers in this module + the consult-side wrapper."""
    with _usage_lock:
        _total_usage["input_tokens"] += input_tokens
        _total_usage["output_tokens"] += output_tokens
        _total_usage["cost_usd"] += cost_usd
        _total_usage["calls"] += 1


def invoke_claude(prompt, *, model="opus", effort="max", tools=None,
                  output_format="json", cwd=None, omit_tools=False):
    """Call claude --print (single-turn, no tools by default). Returns Result.

    output_format="json" wraps the response in a JSON envelope (default).
    output_format=None omits the flag — claude emits plain text and
    Result.data is None.

    `tools` controls --tools (default None → --tools "", no tools
    available). `omit_tools=True` skips the --tools flag entirely
    (claude defaults to all tools).

    `cwd` sets the subprocess cwd; None inherits from the parent.
    """
    model_flag = MODEL_FLAGS.get(model, model)

    cmd = ["claude", "--print", "--model", model_flag]
    if output_format:
        cmd.extend(["--output-format", output_format])
    if not omit_tools:
        if tools is not None:
            cmd.extend(["--tools", tools])
        else:
            cmd.extend(["--tools", ""])

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env.setdefault("CLAUDE_CODE_MAX_OUTPUT_TOKENS", "128000")
    if effort:
        env["CLAUDE_CODE_EFFORT_LEVEL"] = effort

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        cwd=cwd, timeout=None,
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  FAILED (exit {result.returncode}, {elapsed:.0f}s)",
              file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:5]:
                print(f"    stderr: {line}", file=sys.stderr)
        if result.stdout:
            for line in result.stdout.strip().split("\n")[:5]:
                print(f"    stdout: {line[:300]}", file=sys.stderr)
        return Result(elapsed=elapsed)

    if output_format != "json":
        return Result(text=result.stdout.strip(), elapsed=elapsed, ok=True)

    try:
        data = json.loads(result.stdout)
        if data.get("is_error"):
            print(f"  FAILED (is_error in JSON, {elapsed:.0f}s)", file=sys.stderr)
            print(f"    api_error_status: {data.get('api_error_status')}", file=sys.stderr)
            print(f"    result: {str(data.get('result', ''))[:300]}", file=sys.stderr)
            return Result(data=data, elapsed=elapsed)
        return _result_from_json(data, elapsed)
    except (json.JSONDecodeError, KeyError):
        return Result(text=result.stdout.strip(), elapsed=elapsed, ok=True)


def _result_from_json(data, elapsed):
    """Build a Result from a successfully parsed JSON response."""
    usage_data = data.get("usage", {}) or {}
    inp = (usage_data.get("input_tokens", 0) +
           usage_data.get("cache_read_input_tokens", 0) +
           usage_data.get("cache_creation_input_tokens", 0))
    out = usage_data.get("output_tokens", 0)
    return Result(
        text=data.get("result", ""),
        data=data,
        elapsed=elapsed,
        usage={"input_tokens": inp, "output_tokens": out},
        cost=data.get("total_cost_usd", 0) or 0.0,
        ok=True,
    )


def invoke_claude_agent(prompt, *, model="opus", effort="max",
                        tools="Read,Write,Bash", max_turns=12, cwd=None,
                        enabled_tools=None):
    """Call claude -p (agent mode). Returns Result.

    `tools` is passed via --allowedTools (bypass permission prompts).
    `enabled_tools=None` (default) omits --tools so all built-in tools
    are available. When set, --tools restricts the enabled surface to
    just those tools.
    `max_turns=None` omits the --max-turns flag (server default applies).
    """
    model_flag = MODEL_FLAGS.get(model, model)

    cmd = [
        "claude", "-p",
        "--model", model_flag,
        "--output-format", "json",
    ]
    if max_turns is not None:
        cmd.extend(["--max-turns", str(max_turns)])
    if enabled_tools is not None:
        cmd.extend(["--tools", enabled_tools])
    cmd.extend(["--allowedTools", tools])

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env.setdefault("CLAUDE_CODE_MAX_OUTPUT_TOKENS", "128000")
    if effort:
        env["CLAUDE_CODE_EFFORT_LEVEL"] = effort

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        cwd=str(cwd or WORKSPACE), timeout=None,
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  FAILED (exit {result.returncode}, {elapsed:.0f}s)",
              file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:5]:
                print(f"    {line}", file=sys.stderr)
        return Result(elapsed=elapsed)

    try:
        data = json.loads(result.stdout)
        return _result_from_json(data, elapsed)
    except (json.JSONDecodeError, KeyError):
        print(f"  [{elapsed:.0f}s] [parse error]", file=sys.stderr)
        return Result(elapsed=elapsed)


def strip_code_fence(text):
    """Strip leading/trailing ``` code fences from an LLM response.

    Handles opening ``` on its own line (with optional language tag) and
    closing ``` either on its own line or appended to the last line.
    """
    text = text.strip()
    if text.startswith("```"):
        nl = text.find("\n")
        if nl == -1:
            return ""
        text = text[nl + 1:]
    if text.endswith("```"):
        text = text[:-3].rstrip()
    return text


def parallel_llm_calls(items, worker_fn, max_workers=10):
    """Run LLM calls in parallel over a list of items.

    worker_fn(item) → (label, result) — called in thread pool.
    Returns list of (label, result) in original item order.
    Prints progress with thread-safe locking.
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import threading

    print_lock = threading.Lock()
    results = {}

    def _wrapped(idx, item):
        label, result = worker_fn(item)
        with print_lock:
            print(f"    {label}...", file=sys.stderr)
        return idx, label, result

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(_wrapped, i, item): i
            for i, item in enumerate(items)
        }
        for future in as_completed(futures):
            try:
                idx, label, result = future.result()
                results[idx] = (label, result)
            except Exception as e:
                idx = futures[future]
                print(f"    [ERROR] item {idx}: {e}", file=sys.stderr)
                results[idx] = ("?", None)

    return [results[i] for i in sorted(results.keys())]
