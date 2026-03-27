#!/usr/bin/env python3
"""Review — review-revise cycle for an ASN."""
import subprocess, sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "lib" / "discovery" / "review.py"

if __name__ == "__main__":
    sys.exit(subprocess.run([sys.executable, str(SCRIPT)] + sys.argv[1:]).returncode)
