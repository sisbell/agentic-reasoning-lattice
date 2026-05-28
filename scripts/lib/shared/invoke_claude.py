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

import itertools
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
    "opus": "claude-opus-4-8[1m]",
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


# ─── Account rotation + quota failover ──────────────────────────


_rotation_lock = threading.Lock()
_rotation_cycle = None
_ACCOUNT_STATE_PATH = WORKSPACE / "_workspace" / "account-state.json"
_QUOTA_COOLDOWN_SECONDS = 3600  # 1h — matches Anthropic 5-hour rolling window cadence
_SUBPROCESS_TIMEOUT_SECONDS = 7200  # 120min hard cap per LLM call

# After exponential backoff exhausts on overload (4 attempts, max ~15min
# total wait), enter polling phase: sleep + retry every interval until
# success or max polls. Overload is transient global state — server
# eventually catches up. Total max overload wait = backoff + polling.
_OVERLOAD_POLL_INTERVAL_SECONDS = 300  # 5min between polls
_OVERLOAD_POLL_MAX_ATTEMPTS = 12       # 1h total polling phase

# Per-process cumulative cost per config_dir. The load-balanced
# rotation reads this to pick the less-burdened account on each call.
# Starts empty; fresh process tie-breaks on dir order until enough
# calls have accumulated to differentiate. Reset on process restart.
_per_account_cost: dict = {}


def _record_call_cost(config_dir: str, cost_usd: float) -> None:
    """Accumulate cost against the config_dir that handled the call.

    Threadsafe via `_rotation_lock` (same lock that protects rotation
    state — load-balancing reads happen under the same lock).
    """
    if not config_dir or not cost_usd:
        return
    with _rotation_lock:
        _per_account_cost[config_dir] = (
            _per_account_cost.get(config_dir, 0.0) + cost_usd
        )


def _configured_dirs():
    """Parse CLAUDE_CONFIG_DIRS into a list of expanded paths, or [] if unset."""
    dirs_env = os.environ.get("CLAUDE_CONFIG_DIRS", "").strip()
    if not dirs_env:
        return []
    return [os.path.expanduser(d.strip()) for d in dirs_env.split(",") if d.strip()]


def _load_account_state():
    if not _ACCOUNT_STATE_PATH.exists():
        return {}
    try:
        return json.loads(_ACCOUNT_STATE_PATH.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def _save_account_state(state):
    _ACCOUNT_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    _ACCOUNT_STATE_PATH.write_text(json.dumps(state, indent=2))


def _pause_account(config_dir, cooldown=_QUOTA_COOLDOWN_SECONDS):
    """Mark a config_dir as quota-paused for `cooldown` seconds.

    Persisted to `_workspace/account-state.json` (per-machine,
    gitignored) so scheduler restarts inherit the cooldown and don't
    immediately re-trigger the same quota.
    """
    with _rotation_lock:
        state = _load_account_state()
        state[config_dir] = time.time() + cooldown
        _save_account_state(state)
    print(
        f"  [QUOTA] paused {config_dir} until "
        f"{time.strftime('%H:%M:%S', time.localtime(time.time() + cooldown))} "
        f"(cooldown {cooldown // 60}min)",
        file=sys.stderr,
    )


def _is_overloaded_error(data):
    """True iff the JSON response indicates Anthropic API overload.

    Status 529 with `overloaded_error` type. Transient global capacity
    issue, NOT account-specific — switching accounts doesn't help;
    waiting does.
    """
    if not isinstance(data, dict) or not data.get("is_error"):
        return False
    if data.get("api_error_status") == 529:
        return True
    msg = (data.get("result") or "").lower()
    return "overloaded" in msg


def _is_overloaded_signal(text):
    """True iff raw subprocess output contains an overload signature.

    Used when claude -p exits non-zero and prefixes the error to stdout
    rather than returning a structured JSON envelope (e.g.,
    `API Error: 529 {"type":"error","error":{"type":"overloaded_error"...`).
    """
    if not text:
        return False
    text_lower = text.lower()
    return ("overloaded" in text_lower) or ("529" in text_lower)


def _is_quota_signal(text):
    """True iff raw subprocess output contains an account-quota signature.

    Fallback for when claude -p exits non-zero without emitting a parseable
    JSON envelope (e.g., output_format != "json", or truncated output).
    Mirrors `_is_overloaded_signal` for quota errors.
    """
    if not text:
        return False
    text_lower = text.lower()
    return any(
        s in text_lower for s in
        ("rate limit", "quota", "weekly", "5-hour", "5 hour",
         "hit your limit", "429")
    )


def _is_quota_error(data):
    """True iff the JSON response looks like an account-quota error.

    Detected via api_error_status == 429 OR substring match on the
    error message (rate limit, quota, weekly, 5-hour). False positives
    are recoverable (just pause-and-retry); false negatives leave a
    quota error unhandled and propagating, which is the existing
    behaviour.
    """
    if not isinstance(data, dict) or not data.get("is_error"):
        return False
    status = data.get("api_error_status")
    if status == 429:
        return True
    msg = (data.get("result") or "").lower()
    return any(
        s in msg for s in
        ("rate limit", "quota", "weekly", "5-hour", "5 hour")
    )


def _is_auth_error(data):
    """True iff the JSON response looks like an authentication failure.

    Detected via api_error_status == 401 OR substring match on the
    error message (authentication_error, invalid authentication, failed
    to authenticate). Treated the same as quota for rotation purposes:
    pause the account and try the next one. The cooldown is the same as
    quota's — the broken token won't fix itself, but pausing prevents
    the worker from hammering the broken account indefinitely and gives
    the operator time to re-login via CLAUDE_CONFIG_DIR=<dir> claude.
    """
    if not isinstance(data, dict) or not data.get("is_error"):
        return False
    status = data.get("api_error_status")
    if status == 401:
        return True
    msg = (data.get("result") or "").lower()
    return any(
        s in msg for s in
        ("authentication_error", "invalid authentication",
         "failed to authenticate")
    )


def _is_auth_signal(text):
    """True iff raw subprocess output contains an auth-error signature.

    Fallback for when claude -p exits non-zero without emitting a
    parseable JSON envelope. Mirrors `_is_quota_signal` for auth errors.
    """
    if not text:
        return False
    text_lower = text.lower()
    return any(
        s in text_lower for s in
        ("authentication_error", "invalid authentication",
         "failed to authenticate", " 401 ", "error: 401")
    )


def _overload_wait_and_continue(overload_attempts):
    """Decide whether to retry after an overload response, sleep
    accordingly, and return True if retry should proceed.

    Strategy:
      - First _OVERLOAD_BACKOFF_ATTEMPTS attempts (default 4): exponential
        backoff 60, 120, 240, 480s (capped at 600s).
      - Subsequent _OVERLOAD_POLL_MAX_ATTEMPTS attempts: fixed-interval
        polling (default 5min each, up to 1h total polling phase).
      - After both phases exhaust, return False (caller gives up).

    Overload is global API state, not account-specific. Switching
    accounts doesn't help — only waiting does. The polling phase keeps
    retrying long after the exponential backoff would have given up,
    matching the operator intuition that overload is transient and
    eventually clears.
    """
    BACKOFF_ATTEMPTS = 4
    if overload_attempts < BACKOFF_ATTEMPTS:
        delay = min(60 * (2 ** overload_attempts), 600)
        phase = f"backoff {overload_attempts + 1}/{BACKOFF_ATTEMPTS}"
    elif overload_attempts < BACKOFF_ATTEMPTS + _OVERLOAD_POLL_MAX_ATTEMPTS:
        delay = _OVERLOAD_POLL_INTERVAL_SECONDS
        poll_idx = overload_attempts - BACKOFF_ATTEMPTS
        phase = f"poll {poll_idx + 1}/{_OVERLOAD_POLL_MAX_ATTEMPTS}"
    else:
        print(
            f"  [OVERLOADED] giving up after "
            f"{BACKOFF_ATTEMPTS} backoff + "
            f"{_OVERLOAD_POLL_MAX_ATTEMPTS} poll attempts exhausted",
            file=sys.stderr,
        )
        return False
    print(
        f"  [OVERLOADED] {phase}; sleeping {delay}s before retry",
        file=sys.stderr,
    )
    time.sleep(delay)
    return True


def _wait_for_account_unpause(check_interval=300):
    """Block until at least one configured account is unpaused.

    No-op when CLAUDE_CONFIG_DIRS is unset (single-account inheritance
    has no rotation to wait on).
    """
    dirs = _configured_dirs()
    if not dirs:
        return
    while True:
        state = _load_account_state()
        now = time.time()
        if any(state.get(d, 0) <= now for d in dirs):
            return
        next_unpause = min(state[d] for d in dirs if state.get(d, 0) > now)
        wait = max(min(next_unpause - now + 1, check_interval), 5)
        print(
            f"  [QUOTA] all {len(dirs)} accounts paused; sleeping {int(wait)}s "
            f"(next unpause in {int(next_unpause - now)}s)",
            file=sys.stderr,
        )
        time.sleep(wait)


def _next_config_dir():
    """Return the available CLAUDE_CONFIG_DIR with the lowest
    cumulative cost so far this process, or None to inherit the
    parent shell's CLAUDE_CONFIG_DIR.

    Load-balanced rotation: each call routes to whichever configured
    account has accumulated less spend during this process. Replaces
    the prior round-robin (which produced systematic skew when
    certain expensive call types aligned to the same parity slot —
    e.g., note-revise consistently landing on the same account when
    interleaved with cheap commit-msg calls).

    Fresh-process tie-break: when all accounts are at $0, returns the
    first dir of the rotated `available` list (rotated by CLAUDE_WORKER_INDEX
    so parallel workers diverge on their first call instead of all picking
    the same account); subsequent calls naturally diverge as costs accumulate.

    Skips accounts paused by `_pause_account` (quota-exhausted).
    Returns None if all configured accounts are currently paused;
    callers should `_wait_for_account_unpause()` and retry.

    Unset CLAUDE_CONFIG_DIRS leaves the existing single-account
    behaviour untouched.
    """
    dirs = _configured_dirs()
    if not dirs:
        return None
    state = _load_account_state()
    now = time.time()
    available = [d for d in dirs if state.get(d, 0) <= now]
    if not available:
        return None
    with _rotation_lock:
        # Rotate `available` by CLAUDE_WORKER_INDEX so parallel workers
        # don't collide on the all-zero-cost tie-break (each worker's
        # process starts with an empty cost dict; without rotation,
        # every worker's first call piles onto the first listed dir).
        try:
            worker_index = int(os.environ.get("CLAUDE_WORKER_INDEX", "0"))
        except ValueError:
            worker_index = 0
        offset = worker_index % len(available)
        rotated = available[offset:] + available[:offset]
        # Pick the least-burdened of the available accounts. Cost dict
        # may be empty (fresh process) — .get(d, 0.0) tie-breaks on the
        # first dir of `rotated` via the stable min() iteration order.
        picked = min(rotated, key=lambda d: _per_account_cost.get(d, 0.0))
    cost_so_far = _per_account_cost.get(picked, 0.0)
    print(
        f"  [ROTATE] config_dir={os.path.basename(picked)} "
        f"(cumulative ${cost_so_far:.2f})",
        file=sys.stderr,
    )
    return picked


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

    Quota failover: when CLAUDE_CONFIG_DIRS is set and a call returns
    a quota error (api_error_status 429 or matching message), the
    current account is paused (2h cooldown) and the call retries on
    the next available account. Up to 4 attempts per logical call.
    """
    model_flag = MODEL_FLAGS.get(model, model)
    has_rotation = bool(_configured_dirs())
    max_attempts = 4 if has_rotation else 1
    last_elapsed = 0.0

    # `attempt` counts account-attempts (consumed by quota / rotation).
    # `overload_attempts` counts overload retries independently — overload
    # is global API state, doesn't burn account quota, retries via the
    # helper's backoff-then-poll strategy.
    attempt = 0
    overload_attempts = 0

    while attempt < max_attempts:
        cmd = ["claude", "--print", "--model", model_flag]
        if output_format:
            cmd.extend(["--output-format", output_format])
        if not omit_tools:
            cmd.extend(["--tools", tools if tools is not None else ""])

        env = os.environ.copy()
        env.pop("CLAUDECODE", None)
        env.setdefault("CLAUDE_CODE_MAX_OUTPUT_TOKENS", "128000")
        config_dir = None
        if has_rotation:
            config_dir = _next_config_dir()
            if config_dir is None:
                _wait_for_account_unpause()
                continue  # don't bump attempt; just retry routing
            env["CLAUDE_CONFIG_DIR"] = config_dir
        if effort:
            env["CLAUDE_CODE_EFFORT_LEVEL"] = effort

        start = time.time()
        try:
            result = subprocess.run(
                cmd, input=prompt, capture_output=True, text=True, env=env,
                cwd=cwd, timeout=_SUBPROCESS_TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired:
            elapsed = time.time() - start
            print(
                f"  TIMEOUT (killed after {elapsed:.0f}s; "
                f"cap = {_SUBPROCESS_TIMEOUT_SECONDS}s)",
                file=sys.stderr,
            )
            attempt += 1
            if has_rotation and attempt < max_attempts:
                continue  # retry on next account
            return Result(elapsed=elapsed)
        elapsed = time.time() - start
        last_elapsed = elapsed

        # claude -p emits structured JSON envelopes (api_error_status,
        # is_error) with exit=1 for quota/overload responses. Parse the
        # envelope before treating non-zero exit as fatal — the JSON is
        # the source of truth when --output-format json was requested.
        data = None
        if output_format == "json":
            try:
                data = json.loads(result.stdout)
            except (json.JSONDecodeError, ValueError):
                data = None

        if data is not None:
            if _is_overloaded_error(data):
                if _overload_wait_and_continue(overload_attempts):
                    overload_attempts += 1
                    continue  # don't bump account attempt
                return Result(data=data, elapsed=elapsed)

            if _is_quota_error(data):
                if config_dir:
                    _pause_account(config_dir)
                attempt += 1
                if has_rotation and attempt < max_attempts:
                    continue
                return Result(data=data, elapsed=elapsed)

            if _is_auth_error(data):
                if config_dir:
                    print(
                        f"  [AUTH-FAIL] {config_dir} — re-login with: "
                        f"CLAUDE_CONFIG_DIR={config_dir} claude /login",
                        file=sys.stderr,
                    )
                    _pause_account(config_dir)
                attempt += 1
                if has_rotation and attempt < max_attempts:
                    continue
                return Result(data=data, elapsed=elapsed)

            if data.get("is_error"):
                print(f"  FAILED (is_error in JSON, {elapsed:.0f}s)", file=sys.stderr)
                print(f"    api_error_status: {data.get('api_error_status')}", file=sys.stderr)
                print(f"    result: {str(data.get('result', ''))[:300]}", file=sys.stderr)
                return Result(data=data, elapsed=elapsed)

            result_obj = _result_from_json(data, elapsed)
            _record_call_cost(config_dir, result_obj.cost)
            return result_obj

        # No parseable JSON envelope. Fall back to exit-code + text-signal
        # handling (covers truly-broken subprocesses, non-JSON output_format,
        # and edge cases where claude emits plain text on failure).
        if result.returncode != 0:
            combined = (result.stderr or "") + " " + (result.stdout or "")
            if _is_overloaded_signal(combined):
                if _overload_wait_and_continue(overload_attempts):
                    overload_attempts += 1
                    continue  # don't bump account attempt
                return Result(elapsed=elapsed)
            if _is_quota_signal(combined):
                if config_dir:
                    _pause_account(config_dir)
                attempt += 1
                if has_rotation and attempt < max_attempts:
                    continue
                return Result(elapsed=elapsed)
            if _is_auth_signal(combined):
                if config_dir:
                    print(
                        f"  [AUTH-FAIL] {config_dir} — re-login with: "
                        f"CLAUDE_CONFIG_DIR={config_dir} claude /login",
                        file=sys.stderr,
                    )
                    _pause_account(config_dir)
                attempt += 1
                if has_rotation and attempt < max_attempts:
                    continue
                return Result(elapsed=elapsed)
            print(f"  FAILED (exit {result.returncode}, {elapsed:.0f}s)",
                  file=sys.stderr)
            if result.stderr:
                for line in result.stderr.strip().split("\n")[:5]:
                    print(f"    stderr: {line}", file=sys.stderr)
            if result.stdout:
                for line in result.stdout.strip().split("\n")[:5]:
                    print(f"    stdout: {line[:300]}", file=sys.stderr)
            return Result(elapsed=elapsed)

        # exit==0 + non-JSON output (output_format != "json").
        return Result(text=result.stdout.strip(), elapsed=elapsed, ok=True)

    print(f"  FAILED (quota exhausted on all accounts after {max_attempts} attempts)",
          file=sys.stderr)
    return Result(elapsed=last_elapsed)


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

    Quota failover: when CLAUDE_CONFIG_DIRS is set and a call returns
    a quota error, the current account is paused (2h cooldown) and
    the call retries on the next available account. Up to 4 attempts.
    """
    model_flag = MODEL_FLAGS.get(model, model)
    has_rotation = bool(_configured_dirs())
    max_attempts = 4 if has_rotation else 1
    last_elapsed = 0.0

    # `attempt` counts account-attempts (consumed by quota / rotation).
    # `overload_attempts` counts overload retries independently — overload
    # is global API state, doesn't burn account quota, retries via the
    # helper's backoff-then-poll strategy.
    attempt = 0
    overload_attempts = 0

    while attempt < max_attempts:
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
        config_dir = None
        if has_rotation:
            config_dir = _next_config_dir()
            if config_dir is None:
                _wait_for_account_unpause()
                continue  # don't bump attempt; just retry routing
            env["CLAUDE_CONFIG_DIR"] = config_dir
        if effort:
            env["CLAUDE_CODE_EFFORT_LEVEL"] = effort

        start = time.time()
        try:
            result = subprocess.run(
                cmd, input=prompt, capture_output=True, text=True, env=env,
                cwd=str(cwd or WORKSPACE),
                timeout=_SUBPROCESS_TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired:
            elapsed = time.time() - start
            print(
                f"  TIMEOUT (killed after {elapsed:.0f}s; "
                f"cap = {_SUBPROCESS_TIMEOUT_SECONDS}s)",
                file=sys.stderr,
            )
            attempt += 1
            if has_rotation and attempt < max_attempts:
                continue  # retry on next account
            return Result(elapsed=elapsed)
        elapsed = time.time() - start
        last_elapsed = elapsed

        # claude -p emits structured JSON envelopes (api_error_status,
        # is_error) with exit=1 for quota/overload responses. Parse the
        # envelope before treating non-zero exit as fatal — the JSON is
        # the source of truth.
        data = None
        try:
            data = json.loads(result.stdout)
        except (json.JSONDecodeError, ValueError):
            data = None

        if data is not None:
            if _is_overloaded_error(data):
                if _overload_wait_and_continue(overload_attempts):
                    overload_attempts += 1
                    continue  # don't bump account attempt
                return Result(data=data, elapsed=elapsed)

            if _is_quota_error(data):
                if config_dir:
                    _pause_account(config_dir)
                attempt += 1
                if has_rotation and attempt < max_attempts:
                    continue
                return Result(data=data, elapsed=elapsed)

            if _is_auth_error(data):
                if config_dir:
                    print(
                        f"  [AUTH-FAIL] {config_dir} — re-login with: "
                        f"CLAUDE_CONFIG_DIR={config_dir} claude /login",
                        file=sys.stderr,
                    )
                    _pause_account(config_dir)
                attempt += 1
                if has_rotation and attempt < max_attempts:
                    continue
                return Result(data=data, elapsed=elapsed)

            result_obj = _result_from_json(data, elapsed)
            _record_call_cost(config_dir, result_obj.cost)
            return result_obj

        # No parseable JSON envelope. Fall back to exit-code + text-signal
        # handling.
        if result.returncode != 0:
            combined = (result.stderr or "") + " " + (result.stdout or "")
            if _is_overloaded_signal(combined):
                if _overload_wait_and_continue(overload_attempts):
                    overload_attempts += 1
                    continue  # don't bump account attempt
                return Result(elapsed=elapsed)
            if _is_quota_signal(combined):
                if config_dir:
                    _pause_account(config_dir)
                attempt += 1
                if has_rotation and attempt < max_attempts:
                    continue
                return Result(elapsed=elapsed)
            if _is_auth_signal(combined):
                if config_dir:
                    print(
                        f"  [AUTH-FAIL] {config_dir} — re-login with: "
                        f"CLAUDE_CONFIG_DIR={config_dir} claude /login",
                        file=sys.stderr,
                    )
                    _pause_account(config_dir)
                attempt += 1
                if has_rotation and attempt < max_attempts:
                    continue
                return Result(elapsed=elapsed)
            print(f"  FAILED (exit {result.returncode}, {elapsed:.0f}s)",
                  file=sys.stderr)
            if result.stderr:
                for line in result.stderr.strip().split("\n")[:5]:
                    print(f"    {line}", file=sys.stderr)
            return Result(elapsed=elapsed)

        # exit==0 but stdout wasn't JSON — agent mode always expects JSON.
        print(f"  [{elapsed:.0f}s] [parse error]", file=sys.stderr)
        return Result(elapsed=elapsed)

    print(f"  FAILED (quota exhausted on all accounts after {max_attempts} attempts)",
          file=sys.stderr)
    return Result(elapsed=last_elapsed)


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
