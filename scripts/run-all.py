#!/usr/bin/env python3
"""Backward compatibility shim — use formalize-all.py instead."""
import subprocess, sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "formalize-all.py"

print("  [DEPRECATED] run-all.py -> use formalize-all.py", file=sys.stderr)
sys.exit(subprocess.run([sys.executable, str(SCRIPT)] + sys.argv[1:]).returncode)
