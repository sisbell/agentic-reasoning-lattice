#!/usr/bin/env python3
"""
Batch rebase — check and rebase all ASNs in dependency order.

Processes ASNs in topological order (foundations first). For each ASN:
  1. Check if rebase needed (dependency exports newer than last_rebase_check)
  2. If not needed → skip
  3. If needed, check consistency (or reuse cached CLEAN result)
  4. If CLEAN → update timestamps, skip
  5. If findings → rebase with findings, review/revise, post-check, re-export
  6. If post-check fails → retry once, then stop batch

State is tracked in each ASN's project model yaml:
  - last_rebase_check: timestamp of last rebase verification
  - last_consistency_check: timestamp of last consistency check
  - last_consistency_result: "CLEAN" or "FINDINGS"

Usage:
    python scripts/rebase-all.py                       # all active ASNs
    python scripts/rebase-all.py --exclude 40 42 45    # skip specific ASNs
    python scripts/rebase-all.py --dry-run             # show order + status
    python scripts/rebase-all.py --force               # ignore cached state
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import (WORKSPACE, ASNS_DIR, STATEMENTS_DIR, FOUNDATION_LIST,
                   PROJECT_MODEL_DIR, load_manifest)
from lib.common import find_asn
from lib.rebase_asn import (
    step_surface_check, step_find_extensions, step_verify_transfer,
    step_audit, step_export, update_rebase_timestamp, clear_open_issues,
    _append_open_issues, _load_open_issues,
)


def get_active_asns():
    """Get active ASN numbers from project model yamls. Yaml exists = active."""
    active = []
    for path in PROJECT_MODEL_DIR.glob("ASN-*.yaml"):
        m = re.match(r"ASN-(\d+)", path.stem)
        if m:
            active.append(int(m.group(1)))
    return sorted(active)


def build_dep_graph(asn_nums):
    """Build dependency graph from project models."""
    graph = {}
    for num in asn_nums:
        manifest = load_manifest(num)
        if manifest:
            deps = set(manifest.get("depends", []))
            graph[num] = deps & set(asn_nums)
        else:
            graph[num] = set()
    return graph


def topological_sort(graph):
    """Topological sort — returns list in dependency order (foundations first)."""
    result = []
    visited = set()
    visiting = set()

    def visit(node):
        if node in visited:
            return
        if node in visiting:
            print(f"  [WARN] Dependency cycle involving ASN-{node:04d}",
                  file=sys.stderr)
            return
        visiting.add(node)
        for dep in graph.get(node, set()):
            visit(dep)
        visiting.remove(node)
        visited.add(node)
        result.append(node)

    for node in sorted(graph.keys()):
        visit(node)

    return result


def get_dep_export_timestamps(asn_num):
    """Get the newest dependency export timestamp for an ASN."""
    manifest = load_manifest(asn_num)
    if not manifest:
        return 0

    newest = 0
    for dep in manifest.get("depends", []):
        dep_export = WORKSPACE / "vault" / "3-export" / f"ASN-{dep:04d}-statements.md"
        if dep_export.exists():
            ts = dep_export.stat().st_mtime
            if ts > newest:
                newest = ts
    return newest


def parse_iso_timestamp(ts_str):
    """Parse ISO timestamp string to unix timestamp. Returns None on failure."""
    if not ts_str:
        return None
    try:
        dt = datetime.fromisoformat(ts_str.strip('"'))
        return dt.timestamp()
    except (ValueError, TypeError):
        return None


def update_consistency_state(asn_num, result):
    """Write last_consistency_check and last_consistency_result to yaml."""
    yaml_path = PROJECT_MODEL_DIR / f"ASN-{asn_num:04d}.yaml"
    if not yaml_path.exists():
        return

    content = yaml_path.read_text()
    ts = time.strftime("%Y-%m-%dT%H:%M:%S")

    # Update or append last_consistency_check
    if "last_consistency_check:" in content:
        content = re.sub(r'^last_consistency_check:.*$',
                         f'last_consistency_check: "{ts}"', content,
                         flags=re.MULTILINE)
    else:
        content = content.rstrip() + f'\nlast_consistency_check: "{ts}"\n'

    # Update or append last_consistency_result
    if "last_consistency_result:" in content:
        content = re.sub(r'^last_consistency_result:.*$',
                         f'last_consistency_result: "{result}"', content,
                         flags=re.MULTILINE)
    else:
        content = content.rstrip() + f'\nlast_consistency_result: "{result}"\n'

    yaml_path.write_text(content)


def needs_rebase(asn_num, force=False):
    """Check if an ASN needs rebasing based on yaml state.

    Returns:
      "skip" — no rebase needed
      "check" — needs consistency check to determine
      "rebase" — known to need rebase (force mode)
    """
    manifest = load_manifest(asn_num)
    if not manifest or not manifest.get("depends"):
        return "skip"

    # No reasoning doc — nothing to rebase
    asn_path, _ = find_asn(str(asn_num))
    if asn_path is None:
        return "skip"

    if force:
        return "rebase"

    newest_dep = get_dep_export_timestamps(asn_num)
    if newest_dep == 0:
        return "skip"

    # Check last_rebase_check
    rebase_ts = parse_iso_timestamp(manifest.get("last_rebase_check", ""))
    if rebase_ts is not None and rebase_ts > newest_dep:
        return "skip"  # Rebase is newer than all deps

    return "rebase"


def run_convergence(asn_num, max_cycles):
    """Run revise.py --converge. Returns True on success, False on failure."""
    cmd = [sys.executable,
           str(WORKSPACE / "scripts" / "revise.py"),
           str(asn_num),
           "--converge", str(max_cycles)]
    result = subprocess.run(cmd, capture_output=False, text=True,
                            cwd=str(WORKSPACE))
    return result.returncode == 0


def step_commit_asn(asn_num, message):
    """Commit ASN-scoped changes (reasoning doc + review artifacts)."""
    asn_label = f"ASN-{asn_num:04d}"

    # Stage reasoning doc
    asn_path, _ = find_asn(str(asn_num))
    if asn_path:
        subprocess.run(["git", "add", str(asn_path)],
                       capture_output=True, cwd=str(WORKSPACE))

    # Stage review artifacts
    review_dir = WORKSPACE / "vault" / "2-review" / asn_label
    if review_dir.exists():
        subprocess.run(["git", "add", str(review_dir)],
                       capture_output=True, cwd=str(WORKSPACE))

    # Stage consultation artifacts
    consult_dir = WORKSPACE / "vault" / "0-consultations" / asn_label
    if consult_dir.exists():
        subprocess.run(["git", "add", str(consult_dir)],
                       capture_output=True, cwd=str(WORKSPACE))

    # Stage project model
    yaml_path = PROJECT_MODEL_DIR / f"{asn_label}.yaml"
    if yaml_path.exists():
        subprocess.run(["git", "add", str(yaml_path)],
                       capture_output=True, cwd=str(WORKSPACE))

    # Stage export
    export_path = WORKSPACE / "vault" / "3-export" / f"{asn_label}-statements.md"
    if export_path.exists():
        subprocess.run(["git", "add", str(export_path)],
                       capture_output=True, cwd=str(WORKSPACE))

    # Check if there's anything to commit
    diff = subprocess.run(["git", "diff", "--cached", "--quiet"],
                          capture_output=True, cwd=str(WORKSPACE))
    if diff.returncode == 0:
        return  # nothing staged

    subprocess.run(["git", "commit", "-m", message],
                   capture_output=True, cwd=str(WORKSPACE))


def has_open_issues(asn_num):
    """Check if an ASN has open issues."""
    path = PROJECT_MODEL_DIR / f"ASN-{asn_num:04d}-open-issues.md"
    return path.exists() and path.read_text().strip()


def process_asn_hybrid(asn_num, model, effort, max_cycles, force=False):
    """Hybrid rebase: mechanical + focused LLM + surface check + opus."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return "skipped"

    manifest = load_manifest(asn_num)
    if not manifest or not manifest.get("depends"):
        return "skipped"

    print(f"\n  {'='*50}", file=sys.stderr)
    print(f"  {asn_label} (hybrid)", file=sys.stderr)
    print(f"  {'='*50}", file=sys.stderr)

    # ── Check if work needed ──
    status = needs_rebase(asn_num, force=force)
    if status == "skip":
        print(f"  [SKIP] {asn_label} — up to date", file=sys.stderr)
        return "skipped"

    # ── Step 0: Export (if needed — ensures deps YAML exists) ──
    deps_path = STATEMENTS_DIR / f"ASN-{asn_num:04d}-deps.yaml"
    if not deps_path.exists():
        print(f"  [EXPORT] Generating deps YAML (first time)...", file=sys.stderr)
        step_export(asn_num)
        step_commit_asn(asn_num, f"export(asn): {asn_label} — deps YAML generated")

    # ── Do NOT clear open issues — accumulate across runs ──

    # ── Step 1: Mechanical checker (no LLM) ──
    print(f"  [AUDIT 1/4] Mechanical checker...", file=sys.stderr)
    try:
        from lib.rebase_mechanical import check_asn, format_findings
        findings = check_asn(asn_num)
        if findings:
            _append_open_issues(asn_num, format_findings(findings))
            print(f"  [MECHANICAL] {len(findings)} findings", file=sys.stderr)
        else:
            print(f"  [MECHANICAL] Clean", file=sys.stderr)
    except Exception as e:
        print(f"  [MECHANICAL] WARNING: {e}", file=sys.stderr)

    # ── Step 2: Extension extractor + focused LLM (sonnet) ──
    print(f"  [AUDIT 2/4] Extension verification...", file=sys.stderr)
    try:
        from lib.rebase_extensions import extract_claims, verify_claims, format_findings as fmt_ext
        claims = extract_claims(asn_num)
        if claims:
            results = verify_claims(claims, model="sonnet", effort="high")
            ext_findings = fmt_ext(results)
            if ext_findings:
                _append_open_issues(asn_num, ext_findings)
                print(f"  [EXTENSIONS] Gaps found", file=sys.stderr)
            else:
                print(f"  [EXTENSIONS] All verified", file=sys.stderr)
        else:
            print(f"  [EXTENSIONS] No claims", file=sys.stderr)
    except Exception as e:
        print(f"  [EXTENSIONS] WARNING: {e}", file=sys.stderr)

    # ── Step 3: Surface check (sonnet) ──
    print(f"  [AUDIT 3/4] Surface check...", file=sys.stderr)
    step_surface_check(asn_num, asn_path, asn_label)

    # ── Step 4: Open-ended audit (opus) ──
    print(f"  [AUDIT 4/4] Open-ended audit...", file=sys.stderr)
    step_audit(asn_num, asn_path, asn_label)

    # ── Commit audit artifacts ──
    # Create 2a-audit directory
    audit_dir = WORKSPACE / "vault" / "2a-audit" / asn_label
    audit_dir.mkdir(parents=True, exist_ok=True)
    step_commit_asn(asn_num, f"audit(asn): {asn_label} hybrid audit")

    # ── Check if any open issues exist ──
    if not has_open_issues(asn_num):
        print(f"  [AUDIT] No open issues — updating timestamps",
              file=sys.stderr)
        update_rebase_timestamp(asn_num)
        update_consistency_state(asn_num, "CLEAN")
        step_commit_asn(asn_num, f"rebase(asn): {asn_label} — clean, timestamps updated")
        step_export(asn_num)
        step_commit_asn(asn_num, f"export(asn): {asn_label}")
        print(f"  [DONE] {asn_label}", file=sys.stderr)
        return "completed"

    print(f"  [AUDIT] Open issues found — starting review/revise convergence",
          file=sys.stderr)

    # ── REVIEW/REVISE CONVERGENCE ──
    print(f"  [REVIEW] Running fresh review...", file=sys.stderr)
    review_cmd = [sys.executable,
                  str(WORKSPACE / "scripts" / "review.py"),
                  str(asn_num)]
    review_result = subprocess.run(review_cmd, capture_output=False, text=True,
                                   cwd=str(WORKSPACE))

    if review_result.returncode == 2:
        print(f"  [REVIEW] CONVERGED — skipping convergence", file=sys.stderr)
    elif review_result.returncode == 1:
        print(f"  [FAILED] {asn_label} review failed", file=sys.stderr)
        return "failed"
    else:
        print(f"  [CONVERGE] Running standard convergence...", file=sys.stderr)
        if not run_convergence(asn_num, max_cycles):
            print(f"  [FAILED] {asn_label} convergence failed", file=sys.stderr)
            return "failed"

    update_consistency_state(asn_num, "CLEAN")

    # ── RE-EXPORT (if ASN changed) ──
    step_export(asn_num)
    step_commit_asn(asn_num, f"export(asn): {asn_label}")

    # ── Check if re-export found new dep issues (stop, don't loop) ──
    # The export runs the dep scan which may find new issues.
    # If open-issues grew, flag it but don't re-enter review/revise.
    if has_open_issues(asn_num):
        current_issues = _load_open_issues(asn_num)
        if current_issues:
            print(f"  [WARN] Re-export found additional issues — flagged in open-issues.md",
                  file=sys.stderr)

    # ── UPDATE TIMESTAMPS ──
    update_rebase_timestamp(asn_num)
    step_commit_asn(asn_num, f"rebase(asn): {asn_label} timestamps updated")

    print(f"  [DONE] {asn_label}", file=sys.stderr)
    return "completed"


def process_asn(asn_num, model, effort, max_cycles, force=False):
    """Process one ASN: audit → review/converge → post-check → export."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return "skipped"

    manifest = load_manifest(asn_num)
    if not manifest or not manifest.get("depends"):
        return "skipped"

    print(f"\n  {'='*50}", file=sys.stderr)
    print(f"  {asn_label}", file=sys.stderr)
    print(f"  {'='*50}", file=sys.stderr)

    # ── Check if work needed ──
    status = needs_rebase(asn_num, force=force)
    if status == "skip":
        print(f"  [SKIP] {asn_label} — up to date", file=sys.stderr)
        return "skipped"

    # ── Clear stale open issues from previous runs ──
    clear_open_issues(asn_num)

    # ── AUDIT: 4 focused passes ──
    # Pass 1-3: sonnet (prescriptive). Pass 4: opus (open-ended).
    # Each reads foundation + ASN directly. No dependency between passes.
    # All append raw findings to the same open issues file.
    audit_steps = [
        ("Surface check",        lambda: step_surface_check(asn_num, asn_path, asn_label)),
        ("Domain extensions",    lambda: step_find_extensions(asn_num, asn_path, asn_label)),
        ("Transfer verification", lambda: step_verify_transfer(asn_num, asn_path, asn_label)),
        ("Open-ended audit",     lambda: step_audit(asn_num, asn_path, asn_label)),
    ]

    for i, (desc, run_step) in enumerate(audit_steps, 1):
        print(f"  [AUDIT {i}/4] {desc}...", file=sys.stderr)
        ok = run_step()
        if ok is False and i == 4:
            print(f"  [WARN] {asn_label} audit pass {i} failed — continuing",
                  file=sys.stderr)

    # Commit audit artifacts (open issues file, review files)
    step_commit_asn(asn_num, f"audit(asn): {asn_label} foundation audit")

    # ── Check if any open issues exist ──
    if not has_open_issues(asn_num):
        print(f"  [AUDIT] No open issues — updating timestamps",
              file=sys.stderr)
        update_rebase_timestamp(asn_num)
        update_consistency_state(asn_num, "CLEAN")
        step_commit_asn(asn_num, f"rebase(asn): {asn_label} — clean, timestamps updated")
        step_export(asn_num)
        step_commit_asn(asn_num, f"export(asn): {asn_label}")
        print(f"  [DONE] {asn_label}", file=sys.stderr)
        return "completed"

    print(f"  [AUDIT] Open issues found — starting review/revise convergence",
          file=sys.stderr)

    # ── REVIEW/REVISE CONVERGENCE ──
    # review.py reads open issues and promotes them to REVISE items.
    # revise.py fixes them. The loop continues until converged.
    print(f"  [REVIEW] Running fresh review...", file=sys.stderr)
    review_cmd = [sys.executable,
                  str(WORKSPACE / "scripts" / "review.py"),
                  str(asn_num)]
    review_result = subprocess.run(review_cmd, capture_output=False, text=True,
                                   cwd=str(WORKSPACE))

    if review_result.returncode == 2:
        # CONVERGED — skip convergence
        print(f"  [REVIEW] CONVERGED — skipping convergence", file=sys.stderr)
    elif review_result.returncode == 1:
        # Failure — stop batch
        print(f"  [FAILED] {asn_label} review failed", file=sys.stderr)
        return "failed"
    else:
        # Exit 0 — findings exist, run convergence
        print(f"  [CONVERGE] Running standard convergence...", file=sys.stderr)
        if not run_convergence(asn_num, max_cycles):
            print(f"  [FAILED] {asn_label} convergence failed", file=sys.stderr)
            return "failed"

    update_consistency_state(asn_num, "CLEAN")

    # ── EXPORT ──
    step_export(asn_num)
    step_commit_asn(asn_num, f"export(asn): {asn_label}")

    # ── UPDATE TIMESTAMPS ──
    update_rebase_timestamp(asn_num)
    step_commit_asn(asn_num, f"rebase(asn): {asn_label} timestamps updated")

    print(f"  [DONE] {asn_label}", file=sys.stderr)
    return "completed"


def main():
    parser = argparse.ArgumentParser(
        description="Batch rebase — check and rebase all ASNs in dependency order")
    parser.add_argument("--only", nargs="+", type=int, default=[],
                        help="Only process these ASN numbers")
    parser.add_argument("--exclude", "-x", nargs="+", type=int, default=[],
                        help="ASN numbers to exclude")
    parser.add_argument("--topic", "-t",
                        help="Only process ASNs with this topic")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"])
    parser.add_argument("--effort", default="max")
    parser.add_argument("--max-cycles", type=int, default=30,
                        help="Max convergence cycles (default: 30)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true",
                        help="Re-check all, ignore cached state")
    parser.add_argument("--hybrid", action="store_true",
                        help="Use hybrid pipeline (mechanical + focused LLM)")
    parser.add_argument("--clear-issues", type=int, metavar="N",
                        help="Clear open-issues for ASN-N before processing")
    args = parser.parse_args()

    if args.clear_issues:
        clear_open_issues(args.clear_issues)
        print(f"  [CLEARED] ASN-{args.clear_issues:04d} open-issues",
              file=sys.stderr)

    all_active = get_active_asns()
    if args.only:
        asn_nums = [n for n in args.only if n in all_active]
    else:
        asn_nums = [n for n in all_active if n not in args.exclude]

    if args.topic:
        filtered = [n for n in asn_nums
                    if (load_manifest(n) or {}).get("topic") == args.topic]
        if not filtered:
            known = sorted(set((load_manifest(n) or {}).get("topic", "")
                               for n in asn_nums) - {""})
            print(f"  [ERROR] No ASNs with topic '{args.topic}'. "
                  f"Known topics: {', '.join(known)}", file=sys.stderr)
            sys.exit(1)
        asn_nums = filtered

    graph = build_dep_graph(asn_nums)
    ordered = topological_sort(graph)

    print(f"\n  Rebase-all: {len(ordered)} ASNs in dependency order\n",
          file=sys.stderr)

    if args.dry_run:
        for i, num in enumerate(ordered, 1):
            label = f"ASN-{num:04d}"
            deps = graph.get(num, set())
            deps_str = ", ".join(f"{d:04d}" for d in sorted(deps)) or "—"
            status = needs_rebase(num)
            print(f"  {i:2d}. {label}  deps: [{deps_str}]  {status}",
                  file=sys.stderr)
        print("", file=sys.stderr)
        return

    completed = 0
    skipped = 0
    failed = 0

    process_fn = process_asn_hybrid if args.hybrid else process_asn

    for num in ordered:
        result = process_fn(num, args.model, args.effort,
                            args.max_cycles, force=args.force)

        if result == "completed":
            completed += 1
        elif result == "skipped":
            skipped += 1
        elif result == "failed":
            failed += 1
            print(f"\n  Batch stopped due to failure.", file=sys.stderr)
            break

    print(f"\n  Done: {completed} rebased, {skipped} clean, {failed} failed\n",
          file=sys.stderr)


if __name__ == "__main__":
    main()
