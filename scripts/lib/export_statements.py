#!/usr/bin/env python3
"""
Export formal statements from a converged ASN.

Reads the reasoning document directly and extracts formal statements
using the ASN's own statement registry as the roster. Produces a
statements file in vault/project-model/ASN-NNNN/ for use as foundation by downstream
ASNs.

Does NOT depend on the proof index — operates purely on the reasoning doc.

Usage:
    python scripts/normalize.py 55
    python scripts/normalize.py ASN-0055 --dry-run
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
from paths import WORKSPACE, ASNS_DIR, USAGE_LOG, formal_stmts, dep_graph, asn_dir

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "discovery"
TEMPLATE = PROMPTS_DIR / "export.md"
COMMIT_SCRIPT = WORKSPACE / "scripts" / "commit.py"


def read_file(path):
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


def find_asn(asn_id):
    """Find ASN file by number. Accepts 9, 09, 0009, ASN-0009, or full path."""
    path = Path(asn_id)
    if path.exists():
        label = re.match(r"(ASN-\d+)", path.stem)
        return path, label.group(1) if label else path.stem

    num = re.sub(r"[^0-9]", "", str(asn_id))
    if not num:
        return None, None
    label = f"ASN-{int(num):04d}"
    matches = sorted(ASNS_DIR.glob(f"{label}-*.md"))
    if matches:
        return matches[0], label
    return None, label


def build_prompt(asn_content):
    """Assemble export prompt from template + ASN content."""
    template = read_file(TEMPLATE)
    if not template:
        print("  Prompt template not found at scripts/prompts/discovery/export.md",
              file=sys.stderr)
        sys.exit(1)

    return template.replace("{{asn_content}}", asn_content)


def strip_preamble(text):
    """Strip any preamble before the statements header."""
    marker = re.search(r"^# ASN-\d+", text, re.MULTILINE)
    if marker:
        return text[marker.start():]
    return text


def invoke_claude(prompt, model="sonnet", effort="high"):
    """Call claude --print with --tools "". Returns plain text response."""
    model_flag = {
        "opus": "claude-opus-4-6",
        "sonnet": "claude-sonnet-4-6",
    }.get(model, model)

    cmd = [
        "claude", "--print",
        "--model", model_flag,
        "--tools", "",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
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
            for line in result.stderr.strip().split("\n")[:3]:
                print(f"    {line}", file=sys.stderr)
        return "", elapsed

    print(f"  [{elapsed:.0f}s]", file=sys.stderr)
    return result.stdout.strip(), elapsed


def log_usage(asn_label, elapsed):
    """Append a usage entry to the log."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "export-statements",
            "asn": asn_label,
            "elapsed_s": round(elapsed, 1),
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def export_one(asn_id, model, effort, dry_run):
    """Export statements for a single ASN. Returns (asn_label, True) or (asn_id, False)."""
    asn_path, asn_label = find_asn(asn_id)
    if asn_path is None:
        print(f"  No ASN found for {asn_id} in vault/1-reasoning-docs/",
              file=sys.stderr)
        return asn_id, False

    asn_content = asn_path.read_text()

    # Build prompt
    print(f"  [EXPORT] {asn_label}", file=sys.stderr)
    prompt = build_prompt(asn_content)
    print(f"  Prompt: {len(prompt) // 1024}KB (~{len(prompt) // 4} tokens est.)",
          file=sys.stderr)

    if dry_run:
        print(f'  [DRY RUN] Would invoke {model} with --tools ""',
              file=sys.stderr)
        return asn_label, True

    # Invoke Claude
    text, elapsed = invoke_claude(prompt, model=model, effort=effort)

    if not text:
        print(f"  No statements extracted for {asn_label}", file=sys.stderr)
        return asn_label, False

    # Strip any preamble
    text = strip_preamble(text)

    # Add source metadata after the title
    date_match = re.search(r"\*.*?(\d{4}-\d{2}-\d{2}).*?\*", asn_content)
    all_dates = re.findall(r"\d{4}-\d{2}-\d{2}",
                           date_match.group(0)) if date_match else []
    asn_date = all_dates[-1] if all_dates else "unknown"

    source_line = (f"\n*Source: {asn_path.name} (revised {asn_date}) — "
                   f"Extracted: {time.strftime('%Y-%m-%d')}*\n")
    lines = text.split("\n", 1)
    if len(lines) == 2:
        text = lines[0] + "\n" + source_line + lines[1]
    else:
        text = text + "\n" + source_line

    # Write output
    asn_num = int(re.sub(r"[^0-9]", "", asn_label))
    asn_dir(asn_num).mkdir(parents=True, exist_ok=True)
    out_path = formal_stmts(asn_num)
    out_path.write_text(text + "\n")

    # Log usage
    log_usage(asn_label, elapsed)

    print(str(out_path))
    print(f"  [WROTE] {out_path.relative_to(WORKSPACE)}", file=sys.stderr)

    return asn_label, True


def _generate_deps(asn_id, label):
    """Generate deps YAML alongside the statements export.

    Two phases:
    1. Mechanical extract from property table Status column (fast, no LLM)
    2. LLM scan of derivation sections for undeclared dependencies (sonnet)
    """
    asn_num = int(re.sub(r"[^0-9]", "", str(asn_id)))

    # Phase 1: Mechanical extract
    try:
        from lib.rebase_deps import generate_deps, write_deps_yaml
        deps = generate_deps(asn_num)
        if deps:
            path = write_deps_yaml(asn_num, deps)
            print(f"  [DEPS] mechanical: {path.relative_to(WORKSPACE)} "
                  f"({len(deps['properties'])} properties)", file=sys.stderr)
        else:
            print(f"  [DEPS] WARNING: mechanical extract failed for {label}",
                  file=sys.stderr)
            return
    except Exception as e:
        print(f"  [DEPS] WARNING: mechanical extract failed for {label}: {e}",
              file=sys.stderr)
        return

    # Phase 2: LLM scan for undeclared dependencies
    try:
        from lib.rebase_dep_scan import scan_asn
        scan_asn(asn_num, model="sonnet", effort="high")
    except Exception as e:
        print(f"  [DEPS] WARNING: LLM dep scan failed for {label}: {e}",
              file=sys.stderr)


def main():
    from concurrent.futures import ThreadPoolExecutor, as_completed

    parser = argparse.ArgumentParser(
        description="Export formal statements from converged ASNs")
    parser.add_argument("asns", nargs="+",
                        help="ASN numbers (e.g., 55 56 34) or paths")
    parser.add_argument("--model", "-m", default="sonnet",
                        choices=["opus", "sonnet"],
                        help="Model (default: sonnet)")
    parser.add_argument("--effort", default="high",
                        help="Thinking effort level (low/medium/high/max)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show prompt size without invoking Claude")
    parser.add_argument("--normalize", action="store_true",
                        help="Run format normalization gate before export")
    parser.add_argument("--max-format-cycles", type=int, default=5,
                        help="Max format review/revise cycles (default: 5)")
    args = parser.parse_args()

    if len(args.asns) == 1:
        # Format normalization gate (if requested)
        if args.normalize and not args.dry_run:
            from lib.normalize_format import normalize_format
            asn_num = int(re.sub(r"[^0-9]", "", str(args.asns[0])))
            ok = normalize_format(asn_num, max_cycles=args.max_format_cycles)
            if not ok:
                print(f"  [ERROR] Format normalization failed — fix manually",
                      file=sys.stderr)
                sys.exit(1)

        # Single ASN — run directly, commit immediately
        label, ok = export_one(args.asns[0], args.model, args.effort,
                               args.dry_run)
        if ok and not args.dry_run:
            # Generate deps YAML (mechanical, no LLM)
            _generate_deps(args.asns[0], label)

            print(f"\n  === COMMIT ===", file=sys.stderr)
            asn_num = int(re.sub(r"[^0-9]", "", str(args.asns[0])))
            export_file = formal_stmts(asn_num)
            deps_file = dep_graph(asn_num)
            subprocess.run(
                ["git", "add", str(export_file), str(deps_file)],
                capture_output=True, text=True, cwd=str(WORKSPACE))
            cmd = [sys.executable, str(COMMIT_SCRIPT),
                   f"Export statements {label}"]
            subprocess.run(cmd, capture_output=True, text=True,
                           cwd=str(WORKSPACE))
            # Hint: check if this is an extension
            from paths import load_manifest
            asn_num = int(re.sub(r"[^0-9]", "", str(args.asns[0])))
            manifest = load_manifest(asn_num)
            if manifest.get("extends"):
                print(f"\n  [NEXT] Absorb into base: "
                      f"python scripts/absorb.py {asn_num}",
                      file=sys.stderr)
        if not ok:
            sys.exit(1)
        return

    # Multiple ASNs — run in parallel, commit once at end
    succeeded = []
    failed = []

    with ThreadPoolExecutor(max_workers=len(args.asns)) as pool:
        futures = {
            pool.submit(export_one, asn_id, args.model, args.effort,
                        args.dry_run): asn_id
            for asn_id in args.asns
        }
        for future in as_completed(futures):
            label, ok = future.result()
            if ok:
                succeeded.append(label)
            else:
                failed.append(label)

    if succeeded and not args.dry_run:
        # Generate deps YAML for each succeeded ASN
        for asn_id in args.asns:
            asn_num = int(re.sub(r"[^0-9]", "", str(asn_id)))
            lbl = f"ASN-{asn_num:04d}"
            if lbl in succeeded:
                _generate_deps(asn_id, lbl)

        labels = ", ".join(sorted(succeeded))
        print(f"\n  === COMMIT ({labels}) ===", file=sys.stderr)
        # Stage export files + deps YAML
        for lbl in sorted(succeeded):
            lbl_num = int(re.sub(r"[^0-9]", "", lbl))
            export_file = formal_stmts(lbl_num)
            deps_file = dep_graph(lbl_num)
            subprocess.run(
                ["git", "add", str(export_file), str(deps_file)],
                capture_output=True, text=True, cwd=str(WORKSPACE))
        cmd = [sys.executable, str(COMMIT_SCRIPT),
               f"Export statements {labels}"]
        result = subprocess.run(cmd, capture_output=True, text=True,
                                cwd=str(WORKSPACE))
        if result.returncode != 0:
            print(f"  [COMMIT] FAILED", file=sys.stderr)
            if result.stderr:
                for line in result.stderr.strip().split("\n")[:3]:
                    print(f"    {line}", file=sys.stderr)
        else:
            if result.stderr:
                for line in result.stderr.strip().split("\n"):
                    print(f"  {line}", file=sys.stderr)

    if failed:
        print(f"\n  FAILED: {', '.join(failed)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
