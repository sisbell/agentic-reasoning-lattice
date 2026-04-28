"""
Full Review step — whole-ASN deep structural analysis.

Reads the entire ASN + foundation and finds issues that per-claim
pipelines can't catch: carrier-set conflation, precondition chain gaps,
arguments that assume what they prove, missing cases.

Step functions for the orchestrator (scripts/full-review.py):
- run_review: run Opus deep review, return (verdict, text, elapsed)
- extract_findings: parse findings into (title, cls, text) tuples
- filter_revise: narrow findings to REVISE-class only
- cycle_verdict, findings_summary: format meta fields for emit_meta
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import prompt_path
from lib.shared.common import read_file, invoke_claude
from lib.shared.foundation import (
    claim_asn_dep_ids, load_foundation_for_claim_asn,
    load_foundation_for_labels,
)

REVIEW_TEMPLATE = prompt_path("claim-convergence/full-review/review.md")

_VERDICT_RE = re.compile(r'^VERDICT:\s*(CONVERGED|OBSERVE|REVISE)\s*$', re.MULTILINE)
_CLASS_RE = re.compile(r'\*\*Class\*\*:\s*(REVISE|OBSERVE)', re.IGNORECASE)
_MISSING_RE = re.compile(
    r'^MISSING-REFERENCES:\s*\n((?:\S.*\n)+)',
    re.MULTILINE,
)


def parse_verdict(text):
    """Return 'CONVERGED' | 'OBSERVE' | 'REVISE' from the reviewer's
    mandatory VERDICT line, or 'UNKNOWN' if the line is missing."""
    m = _VERDICT_RE.search(text)
    return m.group(1) if m else "UNKNOWN"


def parse_missing_references(text):
    """Return a list of claim labels the reviewer flagged as referenced
    but not present in the content shown. Empty list when the section
    is absent or empty."""
    m = _MISSING_RE.search(text)
    if not m:
        return []
    return [line.strip() for line in m.group(1).splitlines() if line.strip()]


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
        foundation = load_foundation_for_labels(
            asn_num, foundation_labels,
            dep_ids=claim_asn_dep_ids(asn_num),
        )
    else:
        foundation = load_foundation_for_claim_asn(asn_num)
    if not foundation:
        foundation = "(none — this is a foundation ASN; review internal consistency only)"

    template = read_file(REVIEW_TEMPLATE)
    if not template:
        print(f"  [ERROR] Audit template not found", file=sys.stderr)
        return "ERROR", None, 0

    depends = claim_asn_dep_ids(asn_num)
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


def cycle_verdict(reviewer_verdict, revise_count):
    """Reconcile reviewer's verdict line with the per-finding revise count.

    Reviewer may emit VERDICT: CONVERGED while still filing REVISE-class
    findings (rare but possible). The cycle's effective verdict reflects
    what was actually filed.
    """
    if reviewer_verdict == "CONVERGED" and revise_count == 0:
        return "CONVERGED"
    if revise_count > 0:
        return "REVISE"
    return reviewer_verdict


def findings_summary(findings, revise_count):
    """Format a one-line summary of findings counts: '1 REVISE, 2 OBSERVE'."""
    if not findings:
        return "0 findings"
    observe_count = len(findings) - revise_count
    if revise_count and observe_count:
        return f"{revise_count} REVISE, {observe_count} OBSERVE"
    if revise_count:
        return f"{revise_count} REVISE"
    return f"{observe_count} OBSERVE"
