#!/usr/bin/env python3
"""
Commit vault changes with descriptive messages.

Checks for changes in vault/, invokes claude -p with the commit prompt
template so it can read diffs and generate a meaningful commit message.

Prints the commit hash to stdout.

Usage:
    python scripts/commit.py
    python scripts/commit.py "ASN-0009 revised to address review 1"
    python scripts/commit.py --proofs-only "promote LessThanIntro bridge lemma"
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

from paths import WORKSPACE, USAGE_LOG

COMMIT_PROMPT = WORKSPACE / "scripts" / "prompts" / "commit.md"
PROOFS_COMMIT_PROMPT = WORKSPACE / "scripts" / "prompts" / "commit-proofs.md"

MODEL = "claude-sonnet-4-6"


def read_file(path):
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


def main():
    # Parse --proofs-only flag from args
    args = sys.argv[1:]
    proofs_mode = "--proofs-only" in args
    if proofs_mode:
        args.remove("--proofs-only")
    hint = " ".join(args)

    # Check for changes in the appropriate directory
    check_path = "vault/proofs/" if proofs_mode else "vault/"
    result = subprocess.run(
        ["git", "status", "--porcelain", check_path],
        capture_output=True, text=True, cwd=str(WORKSPACE),
    )
    if not result.stdout.strip():
        label = "vault/proofs/" if proofs_mode else "vault/"
        print(f"  nothing to commit in {label}", file=sys.stderr)
        sys.exit(0)

    prompt_path = PROOFS_COMMIT_PROMPT if proofs_mode else COMMIT_PROMPT
    skill_body = read_file(prompt_path)
    if not skill_body:
        print(f"  Commit prompt not found at {prompt_path.relative_to(WORKSPACE)}",
              file=sys.stderr)
        sys.exit(1)

    prompt = f"""{skill_body}

## Context

{hint}

Check for changes in {"vault/proofs/" if proofs_mode else "vault/"}, read the diffs, and commit with a descriptive message.
"""

    cmd = [
        "claude", "-p",
        "--model", MODEL,
        "--output-format", "json",
        "--max-turns", "8",
        "--allowedTools", "Bash,Read",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = "high"

    print("  [COMMIT] reading diff, generating message...", file=sys.stderr)
    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE),
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  [COMMIT] failed ({elapsed:.0f}s) — changes left unstaged",
              file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:3]:
                print(f"    {line}", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(result.stdout)
        usage = data.get("usage", {})
        cost = data.get("total_cost_usd", 0)
        inp = (usage.get("input_tokens", 0) +
               usage.get("cache_read_input_tokens", 0) +
               usage.get("cache_creation_input_tokens", 0))
        out = usage.get("output_tokens", 0)

        print(f"  [COMMIT] done ({elapsed:.0f}s) | in:{inp} out:{out} ${cost:.4f}",
              file=sys.stderr)

        try:
            entry = {
                "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "skill": "commit",
                "elapsed_s": round(elapsed, 1),
                "input_tokens": inp, "output_tokens": out,
                "cost_usd": cost,
            }
            with open(USAGE_LOG, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except OSError:
            pass

    except (json.JSONDecodeError, KeyError):
        print(f"  [COMMIT] done ({elapsed:.0f}s)", file=sys.stderr)

    # Print the latest commit hash
    hash_result = subprocess.run(
        ["git", "log", "--oneline", "-1"],
        capture_output=True, text=True, cwd=str(WORKSPACE),
    )
    if hash_result.stdout.strip():
        print(hash_result.stdout.strip())


if __name__ == "__main__":
    main()
