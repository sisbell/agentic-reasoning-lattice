#!/usr/bin/env python3
"""Requirements — extract Nelson design features from ASNs."""
import subprocess, sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "lib" / "shared" / "requirements_extract.py"

if __name__ == "__main__":
    sys.exit(subprocess.run([sys.executable, str(SCRIPT)] + sys.argv[1:]).returncode)
