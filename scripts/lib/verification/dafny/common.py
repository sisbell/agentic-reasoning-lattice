#!/usr/bin/env python3
"""Shared utilities for Dafny verification scripts."""

import json
import subprocess
import sys
import time

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.shared.paths import WORKSPACE, USAGE_LOG


def read_file(path):
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


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
            "skill": "generate-dafny-claim",
            "asn": asn_label,
            "claim": proof_label,
            "elapsed_s": round(elapsed, 1),
            "verified": verified,
            "cost_usd": cost,
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass
