#!/usr/bin/env python3
"""Promote — spawn new inquiries from ASN open questions or review deferrals."""
import subprocess, sys
from pathlib import Path

LIB = Path(__file__).resolve().parent / "lib"
CMDS = {
    "questions": LIB / "promote_questions.py",
    "scope":     LIB / "promote_scope.py",
}

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        print(f"Usage: promote.py <{'|'.join(CMDS)}> [args...]", file=sys.stderr)
        sys.exit(1)
    script = CMDS[sys.argv[1]]
    sys.exit(subprocess.run([sys.executable, str(script)] + sys.argv[2:]).returncode)

if __name__ == "__main__":
    main()
