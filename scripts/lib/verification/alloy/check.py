"""Alloy checker — run java -jar alloy and parse results."""

import os
import re
import subprocess
import sys
import time

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.shared.paths import WORKSPACE

ALLOY_JAR_DEFAULT = (
    "/Applications/Alloy.app/Contents/Resources/org.alloytools.alloy.dist.jar"
)


def check(als_path):
    """Run the Alloy checker on the generated model.

    Returns (output_text, elapsed) or (None, 0) if Alloy not available.
    """
    alloy_jar = os.environ.get("ALLOY_JAR", ALLOY_JAR_DEFAULT)
    if not Path(alloy_jar).exists():
        print("  Alloy not installed — skipping check", file=sys.stderr)
        print(f"  Set ALLOY_JAR or install Alloy.app", file=sys.stderr)
        return None, 0.0

    print("  [ALLOY] running checker...", file=sys.stderr)
    start = time.time()
    result = subprocess.run(
        ["java", "-jar", str(alloy_jar), "exec", "-f", str(als_path)],
        capture_output=True, text=True, timeout=None,
        cwd=str(Path(als_path).parent),
    )
    elapsed = time.time() - start
    print(f"  [ALLOY] {elapsed:.0f}s", file=sys.stderr)

    output = (result.stdout or "") + "\n" + (result.stderr or "")
    return output.strip(), elapsed


def parse_alloy_results(output):
    """Parse Alloy output to detect counterexamples.

    Returns (has_counterexample, summary_lines).

    The Alloy CLI checker reports results like:
      01. check Irreflexive              0       UNSAT
      02. check Total                    1/1     SAT
    SAT on a check command means a counterexample was found.
    UNSAT means the assertion holds within scope.
    """
    if not output:
        return False, []

    lines = output.strip().split("\n")
    has_counterexample = False
    summary = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Detect SAT on check commands = counterexample found
        if re.search(r"check\s+\S+.*\bSAT\b", line):
            summary.append(line)
            # SAT (not UNSAT) on a check = counterexample
            if not re.search(r"\bUNSAT\b", line):
                has_counterexample = True
        elif re.search(r"check\s+\S+.*\bUNSAT\b", line):
            summary.append(line)
        # Legacy format: "Counterexample found" / "No counterexample found"
        elif "counterexample" in line.lower():
            summary.append(line)
            if "no counterexample" not in line.lower():
                has_counterexample = True
        elif "instance found" in line.lower():
            summary.append(line)
        elif "no instance found" in line.lower():
            summary.append(line)
        elif "executing" in line.lower():
            summary.append(line)

    return has_counterexample, summary


def classify_alloy_error(output):
    """Classify Alloy output as syntax-error, counterexample, or pass."""
    if not output:
        return "pass", []

    has_syntax_error = any(
        "syntax error" in line.lower() or "parse error" in line.lower()
        or "type error" in line.lower()
        for line in output.split("\n")
    )

    has_counterexample, summary = parse_alloy_results(output)

    if has_syntax_error:
        return "syntax-error", summary
    elif has_counterexample:
        return "counterexample", summary
    else:
        return "pass", summary
