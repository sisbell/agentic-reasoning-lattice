"""Claim-review agent body.

One LLM invocation: assemble prompt (template + ASN content +
foundation + previous findings + depends list), call Opus, parse
verdict. Same agent invoked from both whole-ASN reviews and
regional cone reviews — `foundation_labels` selects narrowed
loading vs full loading.

Public:
- `run_review(asn_num, asn_content, asn_label, previous_findings,
   *, model, foundation_labels) -> (verdict, text, elapsed)`
- `extract_findings(text)` — parse `### `-prefixed sections into
   (title, cls, body) tuples
- `filter_revise(findings)` — keep REVISE-class only
- `cycle_verdict(reviewer_verdict, revise_count)` — reconcile
   reviewer's VERDICT line with actual filed revises
- `findings_summary(findings, revise_count)` — one-line summary
- `parse_verdict(text)` — extract the VERDICT line
"""

from __future__ import annotations

import re
import sys
from typing import Optional, Tuple

from lib.shared.common import invoke_claude, read_file
from lib.shared.foundation import (
    claim_asn_dep_ids, load_foundation_for_claim_asn,
    load_foundation_for_labels,
)
from lib.shared.paths import prompt_path


REVIEW_TEMPLATE = prompt_path("claim-convergence/full-review/review.md")

_VERDICT_RE = re.compile(
    r'^VERDICT:\s*(CONVERGED|OBSERVE|REVISE)\s*$', re.MULTILINE,
)
_CLASS_RE = re.compile(r'\*\*Class\*\*:\s*(REVISE|OBSERVE)', re.IGNORECASE)
_FINDING_FIELD_RE = re.compile(
    r'^\s*\*\*(Class|Foundation|ASN|Issue|What needs resolving)\*\*\s*:',
    re.MULTILINE,
)


def parse_verdict(text: str) -> str:
    """Return 'CONVERGED' | 'OBSERVE' | 'REVISE' from the reviewer's
    mandatory VERDICT line, or 'UNKNOWN' if the line is missing."""
    m = _VERDICT_RE.search(text)
    return m.group(1) if m else "UNKNOWN"


def run_review(
    asn_num: int,
    asn_content: str,
    asn_label: str,
    previous_findings: str = "",
    model: str = "opus",
    foundation_labels: Optional[list] = None,
) -> Tuple[str, Optional[str], float]:
    """Run Opus deep review. Returns (verdict, text, elapsed).

    verdict ∈ {'CONVERGED', 'OBSERVE', 'REVISE', 'UNKNOWN', 'ERROR'}.
    On ERROR, text is None. On UNKNOWN, the VERDICT line was missing;
    text is still returned so the caller can decide how to handle it.

    If foundation_labels is provided, only loads foundation statements
    for those specific labels (regional review). Otherwise loads all
    upstream foundation (whole-ASN review).
    """
    if foundation_labels is not None:
        foundation = load_foundation_for_labels(
            asn_num, foundation_labels,
            dep_ids=claim_asn_dep_ids(asn_num),
        )
    else:
        foundation = load_foundation_for_claim_asn(asn_num)
    if not foundation:
        foundation = (
            "(none — this is a foundation ASN; review internal "
            "consistency only)"
        )

    template = read_file(REVIEW_TEMPLATE)
    if not template:
        print("  [ERROR] Audit template not found", file=sys.stderr)
        return "ERROR", None, 0

    depends = claim_asn_dep_ids(asn_num)
    depends_str = ", ".join(f"ASN-{d:04d}" for d in depends)

    prior = previous_findings if previous_findings else "(none)"

    prompt = (
        template
        .replace("{{foundation_statements}}", foundation)
        .replace("{{asn_content}}", asn_content)
        .replace("{{asn_label}}", asn_label)
        .replace("{{depends}}", depends_str)
        .replace("{{previous_findings}}", prior)
    )

    print(
        "  [REVIEW] Reading ASN + foundation (Opus)...",
        end="", file=sys.stderr, flush=True,
    )

    text, elapsed = invoke_claude(prompt, model=model, effort="high")

    if not text:
        print(f"  FAILED (exit 1, {elapsed:.0f}s)", file=sys.stderr)
        return "ERROR", None, elapsed

    verdict = parse_verdict(text)
    finding_count = len(re.findall(r'^### ', text, re.MULTILINE))
    print(
        f" verdict={verdict}, {finding_count} finding(s) ({elapsed:.0f}s)",
        file=sys.stderr,
    )

    return verdict, text, elapsed


def extract_findings(text: str) -> list:
    """Extract individual findings from review output.

    Returns list of (title, cls, finding_text) tuples where cls is
    'REVISE', 'OBSERVE', or 'UNKNOWN' (Class field missing).

    A `### `-prefixed section is treated as a finding only if its body
    contains at least one finding field (**Class**, **Foundation**,
    **ASN**, **Issue**, or **What needs resolving**). Sections without
    any of these are narrative/audit prose using `### ` as a heading;
    they are ignored.
    """
    findings = []
    parts = re.split(r'^### ', text, flags=re.MULTILINE)
    for part in parts[1:]:  # skip preamble before first ###
        lines = part.strip().split('\n', 1)
        title = lines[0].strip()
        body = lines[1].strip() if len(lines) > 1 else ""
        if not _FINDING_FIELD_RE.search(body):
            continue
        cls_match = _CLASS_RE.search(body)
        cls = cls_match.group(1).upper() if cls_match else "UNKNOWN"
        findings.append((title, cls, f"### {title}\n{body}"))
    return findings


def filter_revise(findings: list) -> list:
    """Narrow findings to REVISE-class only.

    UNKNOWN falls through to REVISE — conservative: if the reviewer
    didn't classify, act on it.
    """
    return [f for f in findings if f[1] in ("REVISE", "UNKNOWN")]


def cycle_verdict(reviewer_verdict: str, revise_count: int) -> str:
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


def findings_summary(findings: list, revise_count: int) -> str:
    """Format a one-line summary of findings counts: '1 REVISE, 2 OBSERVE'."""
    if not findings:
        return "0 findings"
    observe_count = len(findings) - revise_count
    if revise_count and observe_count:
        return f"{revise_count} REVISE, {observe_count} OBSERVE"
    if revise_count:
        return f"{revise_count} REVISE"
    return f"{observe_count} OBSERVE"
