#!/usr/bin/env python3
"""Patch — apply a targeted fix to an ASN with scoped review/revise."""
import subprocess, sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "lib" / "manage" / "patch.py"

if __name__ == "__main__":
    sys.exit(subprocess.run([sys.executable, str(SCRIPT)] + sys.argv[1:]).returncode)
