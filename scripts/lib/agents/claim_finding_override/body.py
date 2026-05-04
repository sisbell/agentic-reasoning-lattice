"""Claim-finding-override agent body.

Two entry points:
- `classify_finding(body)` — single Sonnet call, returns
  (cls, rationale, cost). For one-off testing or per-finding use.
- `apply_classifier_verdict(findings)` — batch mode: run the agent on
  every finding in a list, override the reviewer's class on
  disagreement, annotate body with effective-class + rationale, log
  overrides to stderr, mutate the list in place.

The override is justified empirically: across the disagreements
observed on ASN-0034 cone-sweep, the classifier was right ~73% of the
time and the reviewer was right ~27%. The classifier's failure mode
is mild (over-flagging prose-clarity issues as REVISE — extra revise
work, no correctness loss); the reviewer's failure mode is severe
(under-flagging contract-completeness and proof-step-grounding
defects — real defects left in the artifact).
"""

from __future__ import annotations

import json
import subprocess
import sys
from typing import List, Tuple

from lib.shared.common import read_file
from lib.shared.paths import prompt_path


CLASSIFY_TEMPLATE = prompt_path(
    "claim-convergence/full-review/classify-finding.md"
)

_VALID_CLASSES = {"REVISE", "OBSERVE"}


def classify_finding(
    finding_body: str, model: str = "claude-sonnet-4-6",
) -> Tuple[str, str, float]:
    """Run the classifier on one finding body.

    Returns (cls, rationale, cost). cls ∈ {"REVISE", "OBSERVE",
    "UNKNOWN"}. UNKNOWN signals the classifier could not produce a
    verdict (template missing, timeout, parse failure); the caller
    should treat it as no-signal, not as a silent OBSERVE.
    """
    template = read_file(CLASSIFY_TEMPLATE)
    if not template:
        return "UNKNOWN", "classifier template missing", 0.0

    prompt = template.replace(
        "{{finding_body}}", _strip_class_marker(finding_body),
    )

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


def apply_classifier_verdict(
    findings: List[Tuple[str, str, str]],
    model: str = "claude-sonnet-4-6",
) -> None:
    """Run the classifier on each finding; override on disagreement.

    Mutates `findings` in place — each (title, cls, body) tuple is
    replaced when an override occurs. Logs overrides to stderr with
    `[CLASSIFIER OVERRIDE]`. The body annotation is the persistent
    audit trail; the stderr log is for operator visibility mid-run.

    `findings` is the list produced by `extract_findings` —
    (title, reviewer_cls, body) tuples.
    """
    total_cost = 0.0
    overrides = 0
    for i, (title, reviewer_cls, body) in enumerate(findings):
        cls, rationale, cost = classify_finding(body, model=model)
        total_cost += cost
        if (
            cls in _VALID_CLASSES
            and reviewer_cls in _VALID_CLASSES
            and cls != reviewer_cls
        ):
            overrides += 1
            print(
                f"  [CLASSIFIER OVERRIDE] reviewer={reviewer_cls} → "
                f"classifier={cls}: {title[:70]}",
                file=sys.stderr,
            )
            if rationale:
                print(
                    f"  [CLASSIFIER OVERRIDE]   rationale: {rationale}",
                    file=sys.stderr,
                )
            annotated = _annotate_body(body, cls, rationale)
            findings[i] = (title, cls, annotated)
    if findings:
        print(
            f"  [CLASSIFIER] {len(findings)} finding(s) processed, "
            f"{overrides} override(s), ${total_cost:.4f}",
            file=sys.stderr,
        )


def _strip_class_marker(body: str) -> str:
    return "\n".join(
        line for line in body.split("\n")
        if not line.strip().lower().startswith("**class**")
    )


def _annotate_body(body: str, classifier_cls: str, rationale: str) -> str:
    """Insert effective-class + rationale lines after the reviewer's
    `**Class**:` line. Preserves the reviewer's original call as
    audit history. If the body has no `**Class**:` line (legacy or
    malformed), appends the annotation at the end so it isn't lost.
    """
    lines = body.split("\n")
    rationale_line = (
        f"**Classifier rationale**: {rationale}" if rationale
        else "**Classifier rationale**: (none provided)"
    )
    annotation = [
        f"**Effective class**: {classifier_cls} (classifier override)",
        rationale_line,
    ]
    for i, line in enumerate(lines):
        if line.strip().lower().startswith("**class**"):
            for offset, ann in enumerate(annotation, 1):
                lines.insert(i + offset, ann)
            return "\n".join(lines)
    return body.rstrip() + "\n\n" + "\n".join(annotation) + "\n"
