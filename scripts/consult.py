#!/usr/bin/env python3
"""Consult — ad-hoc expert consultation.

Dispatches to per-domain consult scripts under domains/<lattice>/scripts/
based on the LATTICE env var (default: xanadu).
"""
import subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import DOMAIN

CMDS = {
    "theory":   DOMAIN / "scripts" / "theory.py",
    "evidence": DOMAIN / "scripts" / "evidence.py",
}

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        print(f"Usage: consult.py <{'|'.join(CMDS)}> [args...]", file=sys.stderr)
        sys.exit(1)
    script = CMDS[sys.argv[1]]
    if not script.exists():
        print(f"consult.py: {script} not found (LATTICE may be unset or the domain has no {sys.argv[1]} script)", file=sys.stderr)
        sys.exit(1)
    sys.exit(subprocess.run([sys.executable, str(script)] + sys.argv[2:]).returncode)

if __name__ == "__main__":
    main()
