"""
Full Review step — whole-ASN deep structural analysis.

Reads the entire ASN + foundation and finds issues that per-claim
pipelines can't catch: carrier-set conflation, precondition chain gaps,
arguments that assume what they prove, missing cases.

Step functions for the orchestrator (scripts/full-review.py):
- run_review: run Opus deep review, return (verdict, text, elapsed)
- extract_findings: parse findings into (title, cls, text) tuples
- filter_revise: narrow findings to REVISE-class only
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import prompt_path, load_manifest
from lib.shared.common import read_file, invoke_claude
from lib.shared.foundation import load_foundation_statements, load_foundation_for_labels

REVIEW_TEMPLATE = prompt_path("formalization/full-review/review.md")

_VERDICT_RE = re.compile(r'^VERDICT:\s*(CONVERGED|OBSERVE|REVISE)\s*$', re.MULTILINE)
_CLASS_RE = re.compile(r'\*\*Class\*\*:\s*(REVISE|OBSERVE)', re.IGNORECASE)


def parse_verdict(text):
    """Return 'CONVERGED' | 'OBSERVE' | 'REVISE' from the reviewer's
    mandatory VERDICT line, or 'UNKNOWN' if the line is missing."""
    m = _VERDICT_RE.search(text)
    return m.group(1) if m else "UNKNOWN"


def run_review(asn_num, asn_content, asn_label, previous_findings="", model="opus",
               foundation_labels=None):
    """Run Opus deep review. Returns (verdict, text, elapsed).

    verdict ∈ {'CONVERGED', 'OBSERVE', 'REVISE', 'UNKNOWN', 'ERROR'}.
    On ERROR, text is None. On UNKNOWN, the VERDICT line was missing;
    text is still returned so the caller can decide how to handle it.

    If foundation_labels is provided, only loads foundation statements for
    those specific labels (for regional review). Otherwise loads all.
    """
    if foundation_labels is not None:
        foundation = load_foundation_for_labels(asn_num, foundation_labels)
    else:
        foundation = load_foundation_statements(asn_num)
    if not foundation:
        foundation = "(none — this is a foundation ASN; review internal consistency only)"

    template = read_file(REVIEW_TEMPLATE)
    if not template:
        print(f"  [ERROR] Audit template not found", file=sys.stderr)
        return "ERROR", None, 0

    manifest = load_manifest(asn_num)
    depends = manifest.get("depends", []) if manifest else []
    depends_str = ", ".join(f"ASN-{d:04d}" for d in depends)

    # Pass previous findings so reviewer doesn't repeat them
    prior = previous_findings if previous_findings else "(none)"

    prompt = (template
              .replace("{{foundation_statements}}", foundation)
              .replace("{{asn_content}}", asn_content)
              .replace("{{asn_label}}", asn_label)
              .replace("{{depends}}", depends_str)
              .replace("{{previous_findings}}", prior))

    print(f"  [REVIEW] Reading ASN + foundation (Opus)...",
          end="", file=sys.stderr, flush=True)

    text, elapsed = invoke_claude(prompt, model=model, effort="high")

    if not text:
        print(f"  FAILED (exit 1, {elapsed:.0f}s)", file=sys.stderr)
        return "ERROR", None, elapsed

    verdict = parse_verdict(text)
    finding_count = len(re.findall(r'^### ', text, re.MULTILINE))
    print(f" verdict={verdict}, {finding_count} finding(s) ({elapsed:.0f}s)",
          file=sys.stderr)

    return verdict, text, elapsed


def extract_findings(text):
    """Extract individual findings from review output.

    Returns list of (title, cls, finding_text) tuples where cls is
    'REVISE', 'OBSERVE', or 'UNKNOWN' (Class field missing).
    """
    findings = []
    parts = re.split(r'^### ', text, flags=re.MULTILINE)
    for part in parts[1:]:  # skip preamble before first ###
        lines = part.strip().split('\n', 1)
        title = lines[0].strip()
        body = lines[1].strip() if len(lines) > 1 else ""
        cls_match = _CLASS_RE.search(body)
        cls = cls_match.group(1).upper() if cls_match else "UNKNOWN"
        findings.append((title, cls, f"### {title}\n{body}"))
    return findings


def filter_revise(findings):
    """Narrow findings to REVISE-class only. UNKNOWN falls through to
    REVISE (conservative — if the reviewer didn't classify, act on it)."""
    return [f for f in findings if f[1] in ("REVISE", "UNKNOWN")]
