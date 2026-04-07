#!/usr/bin/env python3
"""Proof structure — decompose proofs into explicit stages."""
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "lib" / "blueprinting" / "proof_structure.py"

if __name__ == "__main__":
    sys.exit(subprocess.run(
        [sys.executable, str(SCRIPT)] + sys.argv[1:]).returncode)
