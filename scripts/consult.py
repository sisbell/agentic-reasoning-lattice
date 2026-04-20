#!/usr/bin/env python3
"""Consult — ad-hoc expert consultation."""
import subprocess, sys
from pathlib import Path

LIB = Path(__file__).resolve().parent / "lib" / "discovery"
CMDS = {
    "theory":   LIB / "consult_theory.py",
    "evidence": LIB / "consult_evidence.py",
}

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        print(f"Usage: consult.py <{'|'.join(CMDS)}> [args...]", file=sys.stderr)
        sys.exit(1)
    script = CMDS[sys.argv[1]]
    sys.exit(subprocess.run([sys.executable, str(script)] + sys.argv[2:]).returncode)

if __name__ == "__main__":
    main()
