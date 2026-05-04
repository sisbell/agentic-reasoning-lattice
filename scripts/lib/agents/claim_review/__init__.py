"""Claim-review agent — Opus deep structural review.

LLM invocation that reads claim prose + foundation statements and
produces structured findings with REVISE/OBSERVE class plus VERDICT.
Same agent for whole-ASN reviews and regional cone reviews — the
`foundation_labels` parameter narrows which foundation statements
load (None = all upstream; list = just those labels).

Pure agent: returns (verdict, text, elapsed). No substrate writes,
no filesystem mutations beyond reading. Orchestrators
(`lib/orchestrators/{cone_review, claim_full_review}.py`) commit
the review document, emit findings, and apply per-finding revises.
"""

from .body import (
    cycle_verdict,
    extract_findings,
    filter_revise,
    findings_summary,
    parse_verdict,
    run_review,
)

__all__ = [
    "cycle_verdict",
    "extract_findings",
    "filter_revise",
    "findings_summary",
    "parse_verdict",
    "run_review",
]
