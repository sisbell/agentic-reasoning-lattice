#!/usr/bin/env python3
"""Disassemble — break a monolithic ASN into per-property files."""
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "lib" / "blueprinting" / "disassemble.py"

if __name__ == "__main__":
    sys.exit(subprocess.run(
        [sys.executable, str(SCRIPT)] + sys.argv[1:]).returncode)
