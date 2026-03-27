#!/usr/bin/env python3
"""Draft — create a new ASN from an inquiry."""
import subprocess, sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "lib" / "discovery" / "draft.py"

if __name__ == "__main__":
    sys.exit(subprocess.run([sys.executable, str(SCRIPT)] + sys.argv[1:]).returncode)
