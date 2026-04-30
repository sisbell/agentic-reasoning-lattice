"""Sonnet REVISE/OBSERVE classifier — confirms reviewer self-classification.

The reviewer self-classifies each finding (`**Class**: REVISE | OBSERVE`).
This module runs an independent Sonnet pass against the strict test
("would the artifact be wrong without the fix?") and emits a WARN when
its verdict disagrees with the reviewer's. The classifier never
overrides; it only surfaces disagreement for audit.

Usage:
    findings = extract_findings(text)  # (title, reviewer_cls, body) tuples
    warn_on_disagreement(findings)     # prints [WARN] lines on stderr
    revise_findings = filter_revise(findings)  # uses reviewer's class
"""

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import prompt_path
from lib.shared.common import read_file


CLASSIFY_TEMPLATE = prompt_path("claim-convergence/full-review/classify-finding.md")

_VALID_CLASSES = {"REVISE", "OBSERVE"}


def _strip_class_marker(body):
    return "\n".join(
        line for line in body.split("\n")
        if not line.strip().lower().startswith("**class**")
    )


def classify_finding(finding_body, model="claude-sonnet-4-6"):
    """Run the classifier on one finding body. Returns (cls, rationale, cost).

    cls ∈ {"REVISE", "OBSERVE", "UNKNOWN"}. UNKNOWN signals the
    classifier could not produce a verdict (template missing, timeout,
    parse failure); the caller should treat it as no-signal, not as a
    silent OBSERVE.
    """
    template = read_file(CLASSIFY_TEMPLATE)
    if not template:
        return "UNKNOWN", "classifier template missing", 0.0

    prompt = template.replace("{{finding_body}}", _strip_class_marker(finding_body))

    cmd = ["claude", "-p", "--model", model, "--output-format", "json"]
    try:
        result = subprocess.run(
            cmd, input=prompt, capture_output=True, text=True, timeout=60,
        )
    except subprocess.TimeoutExpired:
        return "UNKNOWN", "classifier timed out", 0.0

    if result.returncode != 0:
        return "UNKNOWN", f"classifier exit {result.returncode}", 0.0

    try:
        data = json.loads(result.stdout)
        text = data.get("result", "")
        cost = data.get("total_cost_usd", 0.0)
    except (json.JSONDecodeError, KeyError):
        return "UNKNOWN", "classifier output not parseable as JSON", 0.0

    cls = "UNKNOWN"
    rationale = ""
    for line in text.split("\n"):
        if line.startswith("CLASS:"):
            candidate = line.replace("CLASS:", "").strip().upper()
            if candidate in _VALID_CLASSES:
                cls = candidate
        elif line.startswith("RATIONALE:"):
            rationale = line.replace("RATIONALE:", "").strip()

    return cls, rationale, cost


def warn_on_disagreement(findings, model="claude-sonnet-4-6"):
    """Confirm the reviewer's self-classification with an independent
    Sonnet pass. Emits a WARN line on stderr for each disagreement.
    Never modifies the input or downstream behavior.

    `findings` is the list produced by `extract_findings` —
    (title, reviewer_cls, body) tuples.
    """
    total_cost = 0.0
    disagreements = 0
    for title, reviewer_cls, body in findings:
        cls, rationale, cost = classify_finding(body, model=model)
        total_cost += cost
        if cls in _VALID_CLASSES and reviewer_cls in _VALID_CLASSES and cls != reviewer_cls:
            disagreements += 1
            print(f"  [CLASSIFIER WARN] reviewer={reviewer_cls} classifier={cls}: "
                  f"{title[:70]}", file=sys.stderr)
            if rationale:
                print(f"  [CLASSIFIER WARN]   rationale: {rationale}",
                      file=sys.stderr)
    if findings:
        print(f"  [CLASSIFIER] {len(findings)} finding(s) confirmed, "
              f"{disagreements} disagreement(s), ${total_cost:.4f}",
              file=sys.stderr)
