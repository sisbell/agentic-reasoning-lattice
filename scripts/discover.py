#!/usr/bin/env python3
"""Discover — review/revise cycle for an ASN.

Replaces review.py and revise.py with a single entry point.

Usage:
    python scripts/discover.py 34                # 1 cycle: review -> consult -> revise -> commit
    python scripts/discover.py 34 --cycles 2     # 2 fixed cycles
    python scripts/discover.py 34 --refine       # loop until QUIESCENT (max 15)
    python scripts/discover.py 34 --refine 8     # loop until QUIESCENT (max 8)
    python scripts/discover.py 34 --cycles 3     # force 3 rounds, ignore quiescence
    python scripts/discover.py 34 --review-only  # just review, no consult or revise
"""
import subprocess, sys
from pathlib import Path

REVIEW = Path(__file__).resolve().parent / "note-review.py"
REVISE = Path(__file__).resolve().parent / "note-revise.py"

if __name__ == "__main__":
    args = sys.argv[1:]
    if "--refine" in args or "--cycles" in args or any(a == "--resume" for a in args):
        sys.exit(subprocess.run([sys.executable, str(REVISE)] + args).returncode)
    else:
        sys.exit(subprocess.run([sys.executable, str(REVIEW)] + args).returncode)
