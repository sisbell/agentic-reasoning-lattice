#!/usr/bin/env python3
"""Mechanical Dafny verification — three-way status check."""

import re
import subprocess
import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.shared.paths import WORKSPACE

# Tier 1 patterns (compile errors)
COMPILE_PATTERNS = [
    r"unresolved identifier", r"wrong number of", r"type mismatch",
    r"member does not exist", r"invalid expression", r"undeclared",
    r"not a type", r"syntax error", r"expected", r"invalid token",
]


def verify(path):
    """Run dafny verify. Returns (status, output).

    Status is one of:
    - "verified" — proof passes
    - "proof_failure" — compiles but solver rejects proof
    - "compile_failure" — syntax/type errors, doesn't compile
    - "timeout" — verification timed out
    """
    result = subprocess.run(
        ["dafny", "verify", str(path)],
        capture_output=True, text=True, timeout=None,
        cwd=str(WORKSPACE),
    )
    output = (result.stdout + result.stderr).strip()
    ok = result.returncode == 0 or re.search(r"\d+ verified, 0 errors", output)
    has_errors = bool(re.search(r"^.*Error:.*$", output, re.MULTILINE))

    if bool(ok) and not has_errors:
        return "verified", output

    # Classify: compile failure vs proof failure
    is_compile = any(
        re.search(pat, output, re.IGNORECASE)
        for pat in COMPILE_PATTERNS
    )
    if is_compile:
        return "compile_failure", output
    return "proof_failure", output
