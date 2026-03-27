#!/usr/bin/env python3
"""Rebase — update an ASN's local derivations to cite from its updated foundation."""
import subprocess, sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "lib" / "discovery" / "rebase.py"

if __name__ == "__main__":
    sys.exit(subprocess.run([sys.executable, str(SCRIPT)] + sys.argv[1:]).returncode)
