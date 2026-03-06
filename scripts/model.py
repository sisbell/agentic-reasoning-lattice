#!/usr/bin/env python3
"""Model — produce formal modeling artifacts."""
import subprocess, sys
from pathlib import Path

LIB = Path(__file__).resolve().parent / "lib"
CMDS = {
    "index":        LIB / "model_index.py",
    "statements":   LIB / "model_statements.py",
    "alloy":        LIB / "model_alloy.py",
    "dafny":        LIB / "model_dafny.py",
    "verify-dafny": LIB / "model_verify.py",
    "fix":          LIB / "model_fix.py",
    "status":       LIB / "model_status.py",
}

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        print(f"Usage: model.py <{'|'.join(CMDS)}> [args...]", file=sys.stderr)
        sys.exit(1)
    script = CMDS[sys.argv[1]]
    sys.exit(subprocess.run([sys.executable, str(script)] + sys.argv[2:]).returncode)

if __name__ == "__main__":
    main()
