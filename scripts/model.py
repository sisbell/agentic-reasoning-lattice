#!/usr/bin/env python3
"""Model — produce formal modeling artifacts."""
import subprocess, sys
from pathlib import Path

LIB = Path(__file__).resolve().parent / "lib" / "modeling"
CMDS = {
    "index":        LIB / "index.py",
    "alloy":        LIB / "alloy.py",
    "dafny":        LIB / "dafny.py",
    "verify-dafny": LIB / "verify.py",
    "fix":          LIB / "fix.py",
    "status":       LIB / "status.py",
    "review":       LIB / "review.py",
}

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        print(f"Usage: model.py <{'|'.join(CMDS)}> [args...]", file=sys.stderr)
        sys.exit(1)
    script = CMDS[sys.argv[1]]
    sys.exit(subprocess.run([sys.executable, str(script)] + sys.argv[2:]).returncode)

if __name__ == "__main__":
    main()
