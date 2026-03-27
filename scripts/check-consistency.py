#!/usr/bin/env python3
"""
Semantic consistency check — audit ASNs against their foundation statements.

Runs a Claude prompt for each active ASN to detect stale labels, local
redefinitions, structural drift, missing dependencies, exhaustiveness gaps,
and registry mismatches.

Results are stored in vault/consistency-check/<timestamp>/ as a checkpoint.
Each checkpoint contains one file per ASN checked plus a report.md aggregate.
Re-running resumes from the last incomplete checkpoint.

Usage:
    python scripts/check-consistency.py              # all active ASNs
    python scripts/check-consistency.py 47 51 79     # specific ASNs
    python scripts/check-consistency.py --dry-run    # show what would run
    python scripts/check-consistency.py --force      # ignore existing checkpoint
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import (WORKSPACE, ASNS_DIR,
                   PROJECT_MODEL_DIR, load_manifest)
from lib.shared.common import find_asn
from lib.shared.foundation import load_foundation_statements

PROMPT_TEMPLATE = WORKSPACE / "scripts" / "prompts" / "discovery" / "consistency-check.md"
MODEL = "claude-sonnet-4-6"
CHECK_DIR = WORKSPACE / "vault" / "consistency-check"


def get_active_asns():
    """Get active ASN numbers from project model yamls. Yaml exists = active."""
    active = []
    for path in PROJECT_MODEL_DIR.glob("ASN-*/project.yaml"):
        m = re.match(r"ASN-(\d+)", path.parent.name)
        if m:
            active.append(int(m.group(1)))
    return sorted(active)


def find_or_create_checkpoint(asn_nums, force=False):
    """Find an existing incomplete checkpoint or create a new one.

    Returns (checkpoint_dir, already_done) where already_done is a set
    of ASN labels that have results in this checkpoint.
    """
    CHECK_DIR.mkdir(parents=True, exist_ok=True)

    if not force:
        # Find latest checkpoint directory
        checkpoints = sorted(CHECK_DIR.glob("20*"), reverse=True)
        for cp in checkpoints:
            if not cp.is_dir():
                continue
            # Check if this checkpoint has a report (completed) or is in progress
            done = {p.stem for p in cp.glob("ASN-*.md")}
            has_report = (cp / "report.md").exists()
            if not has_report and done:
                # Incomplete checkpoint — resume it
                print(f"  Resuming checkpoint: {cp.name}", file=sys.stderr)
                return cp, done

    # Create new checkpoint
    ts = time.strftime("%Y-%m-%d-%H%M")
    cp = CHECK_DIR / ts
    cp.mkdir(parents=True, exist_ok=True)
    print(f"  New checkpoint: {cp.name}", file=sys.stderr)
    return cp, set()


def check_asn(asn_num, dry_run=False):
    """Run consistency check on one ASN. Returns result dict or None."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return {"asn": asn_label, "skipped": "no reasoning doc"}

    manifest = load_manifest(asn_num)
    if not manifest:
        return {"asn": asn_label, "skipped": "no project model"}

    depends = manifest.get("depends", [])
    if not depends:
        return {"asn": asn_label, "skipped": "no dependencies"}

    foundation = load_foundation_statements(asn_num)
    if not foundation:
        return {"asn": asn_label, "skipped": "no foundation statements"}

    asn_content = asn_path.read_text()
    depends_str = ", ".join(f"ASN-{d:04d}" for d in depends)

    template = PROMPT_TEMPLATE.read_text()
    prompt = (template
              .replace("{{foundation_statements}}", foundation)
              .replace("{{asn_content}}", asn_content)
              .replace("{{asn_label}}", asn_label)
              .replace("{{depends}}", depends_str))

    prompt_kb = len(prompt) // 1024
    print(f"  [{asn_label}] {prompt_kb}KB prompt, deps: [{depends_str}]",
          end="", flush=True)

    if dry_run:
        print(" — dry run")
        return None

    cmd = [
        "claude", "-p",
        "--model", MODEL,
        "--output-format", "json",
        "--max-turns", "1",
        "--allowedTools", "",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE),
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f" — FAILED ({elapsed:.0f}s)")
        return None

    try:
        data = json.loads(result.stdout)
        text = data.get("result", "")
    except (json.JSONDecodeError, KeyError):
        print(f" — parse error ({elapsed:.0f}s)")
        return None

    clean = "RESULT: CLEAN" in text
    findings_match = re.search(r"RESULT: (\d+) FINDINGS?", text)
    count = 0 if clean else (int(findings_match.group(1)) if findings_match else "?")

    status = "CLEAN" if clean else f"{count} findings"
    print(f" — {status} ({elapsed:.0f}s)")

    return {
        "asn": asn_label,
        "status": status,
        "text": text,
        "clean": clean,
    }


def write_report(checkpoint_dir, results, requested_asns, all_active):
    """Write the aggregate report."""
    lines = [
        f"# Consistency Check — {checkpoint_dir.name}\n",
        f"**Scope**: {len(requested_asns)} ASNs requested"
        f" (of {len(all_active)} active)\n",
    ]

    if set(requested_asns) != set(all_active):
        labels = ", ".join(f"ASN-{n:04d}" for n in requested_asns)
        lines.append(f"**Checked**: {labels}\n")

    checked = [r for r in results if "skipped" not in r]
    skipped = [r for r in results if "skipped" in r]
    clean = [r for r in checked if r.get("clean")]
    dirty = [r for r in checked if not r.get("clean")]

    lines.append(f"\n**Results**: {len(clean)} clean, {len(dirty)} with findings"
                 f", {len(skipped)} skipped\n")

    if skipped:
        lines.append("\n## Skipped\n")
        for r in skipped:
            lines.append(f"- {r['asn']}: {r['skipped']}")

    if dirty:
        lines.append("\n## Findings\n")
        for r in dirty:
            lines.append(f"\n### {r['asn']} — {r['status']}\n")
            lines.append(f"See {r['asn']}.md for details.\n")

    if clean:
        lines.append("\n## Clean\n")
        for r in clean:
            lines.append(f"- {r['asn']}")

    report_path = checkpoint_dir / "report.md"
    report_path.write_text("\n".join(lines) + "\n")
    print(f"\n  Report: {report_path.relative_to(WORKSPACE)}")


def main():
    parser = argparse.ArgumentParser(
        description="Semantic consistency check for ASNs")
    parser.add_argument("asns", nargs="*", type=int,
                        help="ASN numbers to check (default: all active)")
    parser.add_argument("--exclude", "-x", nargs="+", type=int, default=[],
                        help="ASN numbers to exclude (e.g., --exclude 40 42 45)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true",
                        help="Start a new checkpoint, ignore incomplete ones")
    args = parser.parse_args()

    all_active = get_active_asns()
    asn_nums = args.asns if args.asns else all_active
    if args.exclude:
        asn_nums = [n for n in asn_nums if n not in args.exclude]

    print(f"\n  Consistency check: {len(asn_nums)} ASNs\n")

    if args.dry_run:
        for num in asn_nums:
            check_asn(num, dry_run=True)
        return

    checkpoint_dir, already_done = find_or_create_checkpoint(asn_nums,
                                                              force=args.force)

    results = []
    for num in asn_nums:
        label = f"ASN-{num:04d}"
        if label in already_done:
            print(f"  [{label}] already in checkpoint — skipped")
            continue

        r = check_asn(num)
        if r is None:
            continue

        results.append(r)

        # Write immediately
        if "skipped" not in r:
            asn_path = checkpoint_dir / f"{label}.md"
            content = r["text"] if not r["clean"] else "RESULT: CLEAN\n"
            asn_path.write_text(content + "\n")

    if not results:
        print("\n  No new results.\n")
        return

    # Summary to stdout
    checked = [r for r in results if "skipped" not in r]
    clean = sum(1 for r in checked if r.get("clean"))
    dirty = len(checked) - clean

    print(f"\n  Summary: {clean} clean, {dirty} with findings")

    for r in results:
        if "skipped" not in r and not r["clean"]:
            print(f"\n  === {r['asn']} ===\n")
            print(r["text"])

    # Write aggregate report
    write_report(checkpoint_dir, results, asn_nums, all_active)
    print("")


if __name__ == "__main__":
    main()
