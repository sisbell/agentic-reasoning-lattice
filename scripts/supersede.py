#!/usr/bin/env python3
"""Supersede — replace an old ASN with a new one, carrying forward project model and questions."""
import subprocess, sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "lib" / "supersede_asn.py"

if __name__ == "__main__":
    sys.exit(subprocess.run([sys.executable, str(SCRIPT)] + sys.argv[1:]).returncode)
