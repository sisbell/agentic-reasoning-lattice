#!/usr/bin/env python3
"""Discover — review/revise cycle for an ASN.

Replaces review.py and revise.py with a single entry point.

Usage:
    python scripts/discover.py 34                # 1 cycle: review -> consult -> revise -> commit
    python scripts/discover.py 34 --cycles 2     # 2 fixed cycles
    python scripts/discover.py 34 --converge     # loop until CONVERGED (max 15)
    python scripts/discover.py 34 --converge 8   # loop until CONVERGED (max 8)
    python scripts/discover.py 34 --cycles 3     # force 3 rounds, ignore convergence
    python scripts/discover.py 34 --review-only  # just review, no consult or revise
"""
import subprocess, sys
from pathlib import Path

REVIEW = Path(__file__).resolve().parent / "lib" / "discovery" / "review.py"
REVISE = Path(__file__).resolve().parent / "lib" / "discovery" / "revise.py"

if __name__ == "__main__":
    args = sys.argv[1:]
    if "--converge" in args or "--cycles" in args or any(a == "--resume" for a in args):
        sys.exit(subprocess.run([sys.executable, str(REVISE)] + args).returncode)
    else:
        sys.exit(subprocess.run([sys.executable, str(REVIEW)] + args).returncode)
