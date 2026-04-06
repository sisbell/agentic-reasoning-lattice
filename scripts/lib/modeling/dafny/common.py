#!/usr/bin/env python3
"""Shared utilities for Dafny modeling scripts."""

import json
import re
import subprocess
import sys
import time

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.shared.paths import WORKSPACE, USAGE_LOG, DAFNY_DIR, find_latest_modeling_dir


STATUS_DISPLAY = {
    "verified": "verified",
    "proof_failure": "**PROOF FAILURE**",
    "compile_failure": "**COMPILE FAILURE**",
    "timeout": "**TIMEOUT**",
}


def read_file(path):
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


def write_status_file(gen_dir, results, source="generate"):
    """Write or update STATUS.md in the modeling directory.

    Called by both translate.py (after generation) and align.py (after fixes).
    Appends fix attempts to an existing file; overwrites the table on generation.
    """
    status_path = gen_dir / "STATUS.md"
    now = time.strftime("%Y-%m-%d %H:%M")

    # Build the table from results
    verified_count = sum(1 for r in results if r.get("status") == "verified")
    total = len(results)

    lines = [
        f"# Verification Status — {gen_dir.name}",
        f"",
        f"Updated: {now}",
        f"Verified: {verified_count}/{total}",
        f"",
        f"| Property | Status | Contract |",
        f"|----------|--------|----------|",
    ]

    for r in results:
        status = STATUS_DISPLAY.get(r.get("status", ""), "**UNKNOWN**")
        contract = r.get("contract", "")
        lines.append(f"| {r['proof_label']} | {status} | {contract} |")

    lines.append("")

    if source == "generate":
        # Fresh write
        status_path.write_text("\n".join(lines))
    else:
        # Fix: preserve existing content, append fix log entry
        existing = ""
        if status_path.exists():
            existing = status_path.read_text()

        # Find or create Fix Attempts section
        if "## Fix Attempts" not in existing:
            existing = existing.rstrip() + "\n\n## Fix Attempts\n"

        fix_entries = []
        for r in results:
            status = STATUS_DISPLAY.get(r.get("status", ""), "STILL UNVERIFIED")
            cost = f"${r.get('cost', 0):.2f}" if r.get("cost") else ""
            fix_entries.append(f"- {now}: {r['proof_label']} — {status} {cost}")

        status_path.write_text(existing + "\n".join(fix_entries) + "\n")


def run_commit(hint=""):
    """Run commit.py to commit vault changes."""
    cmd = [sys.executable, str(WORKSPACE / "scripts" / "commit.py")]
    if hint:
        cmd.append(hint)
    result = subprocess.run(cmd, cwd=str(WORKSPACE))
    if result.returncode != 0:
        print("  [COMMIT] failed — changes left unstaged", file=sys.stderr)
    return result.returncode == 0


def log_usage(asn_label, proof_label, elapsed, verified, cost):
    """Append a usage entry to the log."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "generate-dafny-property",
            "asn": asn_label,
            "property": proof_label,
            "elapsed_s": round(elapsed, 1),
            "verified": verified,
            "cost_usd": cost,
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def find_modeling_dir(asn_label, modeling_num=None):
    """Find the modeling directory to review."""
    if modeling_num:
        d = DAFNY_DIR / asn_label / f"modeling-{modeling_num}"
        return d if d.exists() else None
    return find_latest_modeling_dir(asn_label)
