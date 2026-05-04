"""Claude CLI invocation — single-turn, agent-mode, and parallel batches.

Wraps `claude --print` and `claude -p` subprocess calls with consistent
env-var setup (max output tokens, effort level, dropping CLAUDECODE),
JSON parsing, and timing. `parallel_llm_calls` runs many `invoke_*`
calls concurrently with progress logging.
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import WORKSPACE


MODEL_FLAGS = {
    "opus": "claude-opus-4-7",
    "sonnet": "claude-sonnet-4-6",
}


def invoke_claude(prompt, *, model="opus", effort="max", tools=None):
    """Call claude --print (single-turn, no tools by default). Returns (text, elapsed)."""
    model_flag = MODEL_FLAGS.get(model, model)

    cmd = ["claude", "--print", "--model", model_flag, "--output-format", "json"]
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
        timeout=None,
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
        return "", elapsed

    try:
        data = json.loads(result.stdout)
        if data.get("is_error"):
            print(f"  FAILED (is_error in JSON, {elapsed:.0f}s)", file=sys.stderr)
            print(f"    api_error_status: {data.get('api_error_status')}", file=sys.stderr)
            print(f"    result: {str(data.get('result', ''))[:300]}", file=sys.stderr)
            return "", elapsed
        text = data.get("result", "")
        return text, elapsed
    except (json.JSONDecodeError, KeyError):
        return result.stdout.strip(), elapsed


def invoke_claude_agent(prompt, *, model="opus", effort="max",
                        tools="Read,Write,Bash", max_turns=12, cwd=None):
    """Call claude -p (agent mode). Returns (json_data, elapsed)."""
    model_flag = MODEL_FLAGS.get(model, model)

    cmd = [
        "claude", "-p",
        "--model", model_flag,
        "--output-format", "json",
        "--max-turns", str(max_turns),
        "--allowedTools", tools,
    ]

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
        return None, elapsed

    try:
        data = json.loads(result.stdout)
        return data, elapsed
    except (json.JSONDecodeError, KeyError):
        print(f"  [{elapsed:.0f}s] [parse error]", file=sys.stderr)
        return None, elapsed


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
