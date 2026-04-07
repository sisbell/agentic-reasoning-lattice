#!/usr/bin/env python3
"""Blueprinting lint — status and dependency checks."""
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "lib" / "blueprinting" / "lint.py"

if __name__ == "__main__":
    sys.exit(subprocess.run(
        [sys.executable, str(SCRIPT)] + sys.argv[1:]).returncode)
