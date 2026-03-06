#!/usr/bin/env python3
"""
Fix unverified Dafny files — agentic loop with baby-steps.

Finds .dfy files in the latest modeling directory that fail verification,
then launches a Claude agent for each to fix them incrementally.

Usage:
    python scripts/model.py fix 1
    python scripts/model.py fix 1 --property TA3
    python scripts/model.py fix 1 --modeling 2
    python scripts/model.py fix 1 --dry-run
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from paths import (WORKSPACE, STATEMENTS_DIR, PROOFS_DIR, DAFNY_DIR,
                   USAGE_LOG, find_latest_modeling_dir)
from lib.model_dafny import write_status_file, write_divergence_file, extract_divergences


def read_file(path):
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


def verify_dafny(path):
    """Run dafny verify. Returns (success, output)."""
    try:
        result = subprocess.run(
            ["dafny", "verify", str(path)],
            capture_output=True, text=True, timeout=120,
            cwd=str(WORKSPACE),
        )
        output = (result.stdout + result.stderr).strip()
        ok = result.returncode == 0 or re.search(r"\d+ verified, 0 errors", output)
        has_errors = bool(re.search(r"^.*Error:.*$", output, re.MULTILINE))
        return bool(ok) and not has_errors, output
    except subprocess.TimeoutExpired:
        return False, "verification timed out (120s)"


def find_modeling_dir(asn_id, modeling_num=None):
    """Find the modeling directory. Returns (dir_path, asn_label)."""
    num = re.sub(r"[^0-9]", "", str(asn_id))
    if not num:
        return None, None
    label = f"ASN-{int(num):04d}"

    if modeling_num is not None:
        d = DAFNY_DIR / label / f"modeling-{modeling_num}"
        return (d if d.exists() else None), label

    return find_latest_modeling_dir(label), label


def invoke_fix_agent(dfy_path, errors, model="opus", effort="max", max_turns=24):
    """Launch a Claude agent to fix an unverified .dfy file."""
    model_flag = {
        "opus": "claude-opus-4-6",
        "sonnet": "claude-sonnet-4-6",
    }.get(model, model)

    cmd = [
        "claude", "-p",
        "--model", model_flag,
        "--output-format", "json",
        "--max-turns", str(max_turns),
        "--tools", "Read,Write,Bash",
        "--allowedTools", "Read,Write,Bash",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    if effort:
        env["CLAUDE_CODE_EFFORT_LEVEL"] = effort

    dfy_source = read_file(dfy_path)

    prompt = f"""Fix this Dafny file that fails verification.

## Current file: {dfy_path}

```dafny
{dfy_source}
```

## Verification errors

```
{errors}
```

## Fix approach — baby steps

The file exists and is close to correct. Fix it incrementally:

1. Read the file and the errors above. Understand what the solver cannot prove.

2. Add the MINIMUM change to address the first error:
   - A single recursive call
   - One `assert` of an intermediate fact
   - One case split (`if ... {{{{ }}}} else {{{{ }}}}`)
   - A call to one existing lemma
   - A bridge lemma with its own signature

3. Write the updated file. Run `dafny verify {dfy_path}`.

4. If verification succeeds, you are done.

5. If it still fails, repeat from step 2. Never add more than one proof
   element between verifications.

6. If stuck after 3 failed attempts on the same error, try a different
   decomposition — a helper lemma, restructured cases, or a different
   encoding. Do not pile on assertions.

Do NOT rewrite the file from scratch. Fix what's there.
"""

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE), timeout=None,
    )
    elapsed = time.time() - start

    cost = 0
    try:
        data = json.loads(result.stdout)
        usage = data.get("usage", {})
        cost = data.get("total_cost_usd", 0)
        inp = (usage.get("input_tokens", 0) +
               usage.get("cache_read_input_tokens", 0) +
               usage.get("cache_creation_input_tokens", 0))
        out = usage.get("output_tokens", 0)
        print(f" [{elapsed:.0f}s] in:{inp} out:{out} ${cost:.4f}",
              file=sys.stderr, end="", flush=True)
        subtype = data.get("subtype", "")
        if subtype and subtype != "success":
            print(f" [{subtype}]", file=sys.stderr, end="", flush=True)
    except (json.JSONDecodeError, KeyError):
        print(f" [{elapsed:.0f}s]", file=sys.stderr, end="", flush=True)

    return elapsed, cost


def log_usage(asn_label, name, elapsed, verified, cost):
    """Append a usage entry to the log."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "fix-dafny",
            "asn": asn_label,
            "property": name,
            "elapsed_s": round(elapsed, 1),
            "verified": verified,
            "cost_usd": round(cost, 4),
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def main():
    parser = argparse.ArgumentParser(
        description="Fix unverified Dafny files with agentic baby-steps")
    parser.add_argument("asn",
                        help="ASN number (e.g., 1, 0001, ASN-0001)")
    parser.add_argument("--property", "-p",
                        help="Fix specific properties, comma-separated (e.g., T5 or T1,T3,TA0)")
    parser.add_argument("--modeling", type=int, default=None,
                        help="Target specific modeling-N directory")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"],
                        help="Model (default: opus)")
    parser.add_argument("--effort", default="max",
                        help="Thinking effort level")
    parser.add_argument("--max-turns", type=int, default=24,
                        help="Max agent turns per property (default: 24)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be fixed without invoking Claude")
    args = parser.parse_args()

    # Find modeling directory
    gen_dir, asn_label = find_modeling_dir(args.asn, args.modeling)
    if gen_dir is None:
        print(f"  No modeling directory found for {args.asn}", file=sys.stderr)
        sys.exit(1)

    print(f"[FIX] {asn_label} — {gen_dir.relative_to(WORKSPACE)}",
          file=sys.stderr)

    # Find .dfy files
    dfy_files = sorted(gen_dir.glob("*.dfy"))
    if not dfy_files:
        print(f"  No .dfy files found in {gen_dir.relative_to(WORKSPACE)}",
              file=sys.stderr)
        sys.exit(1)

    # Filter to specific properties if requested
    if args.property:
        targets = [t.strip() for t in args.property.split(",")]
        matches = []
        for target in targets:
            found = [f for f in dfy_files
                     if target.lower() in f.stem.lower()]
            if not found:
                print(f"  No file matching '{target}' found",
                      file=sys.stderr)
                print(f"  Available: {', '.join(f.stem for f in dfy_files)}",
                      file=sys.stderr)
                sys.exit(1)
            matches.extend(found)
        dfy_files = matches

    # Verify each file, collect failures
    failures = []
    for dfy_path in dfy_files:
        ok, output = verify_dafny(dfy_path)
        if ok:
            print(f"  [OK] {dfy_path.stem}", file=sys.stderr)
        else:
            # Extract error lines
            error_lines = [line for line in output.split("\n")
                           if re.search(r"Error:", line)]
            errors = output
            failures.append((dfy_path, errors))
            print(f"  [FAIL] {dfy_path.stem}: {error_lines[0] if error_lines else 'unknown error'}",
                  file=sys.stderr)

    if not failures:
        print(f"\n  All files verify. Nothing to fix.", file=sys.stderr)
        return

    print(f"\n  {len(failures)} file(s) to fix", file=sys.stderr)

    if args.dry_run:
        for dfy_path, _ in failures:
            print(f"  [DRY RUN] Would fix {dfy_path.stem}", file=sys.stderr)
        return

    # Fix each failure
    total_cost = 0
    fixed = 0
    fix_results = []

    for dfy_path, errors in failures:
        print(f"\n  [{dfy_path.stem}]...", file=sys.stderr, end="", flush=True)

        elapsed, cost = invoke_fix_agent(
            dfy_path, errors,
            model=args.model, effort=args.effort, max_turns=args.max_turns,
        )
        total_cost += cost

        # Verify result
        ok, vout = verify_dafny(dfy_path)
        divergences = extract_divergences(dfy_path)
        if ok:
            m = re.search(r"(\d+) verified", vout)
            n = m.group(1) if m else "?"
            print(f" verified({n})", file=sys.stderr)
            fixed += 1
        else:
            print(f" STILL UNVERIFIED", file=sys.stderr)

        if divergences:
            write_divergence_file(gen_dir, dfy_path.stem, dfy_path.stem, divergences)

        fix_results.append({
            "proof_label": dfy_path.stem,
            "verified": ok,
            "divergences": divergences,
            "cost": cost,
        })
        log_usage(asn_label, dfy_path.stem, elapsed, ok, cost)

    # Update STATUS.md with fix results
    write_status_file(gen_dir, fix_results, source="fix")
    print(f"\n  Done: {fixed}/{len(failures)} fixed, ${total_cost:.2f}",
          file=sys.stderr)
    print(f"  Status: {gen_dir.name}/STATUS.md", file=sys.stderr)


if __name__ == "__main__":
    main()
