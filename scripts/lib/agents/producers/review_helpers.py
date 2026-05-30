"""Shared helpers for the review producers (cone_review, full_review)
and the downstream claim_findings producer.

This module hosts no Agent class — it is the helper surface that the
review producers compose. Three concerns live here:

- LLM invocation: `run_review` assembles the review prompt
  (template + ASN content + foundation + previous findings +
  depends list), calls the model, and returns (verdict, text,
  elapsed). Same call shape for whole-ASN reviews and regional
  cone reviews; `foundation_labels` selects narrowed loading vs
  full loading.
- Output parsing: `parse_verdict` extracts the VERDICT line;
  `extract_findings` splits `### `-prefixed sections into
  (title, cls, body) tuples (used by claim_findings).
- Prompt context: `previously_declined_findings` walks
  `resolution.reject` substrate links and surfaces previously-
  rejected findings + the reviser's rationale, so the next
  reviewer doesn't re-raise them.
"""

from __future__ import annotations

import re
import sys
from typing import List, Optional, Tuple

from lib.backend.addressing import Address
from lib.lattice.labels import format_label
from lib.lattice.render import read_doc
from lib.protocols.febe.protocol import Session
from lib.shared.common import read_file
from lib.shared.invoke_claude import invoke_claude
from lib.shared.foundation import (
    claim_asn_dep_ids, load_foundation_for_claim_asn,
    load_foundation_for_labels,
)
from lib.shared.paths import prompt_path
from lib.shared.prompts import read_prompt


REVIEW_TEMPLATE = prompt_path("agents/producers/review_helpers.md")

_VERDICT_RE = re.compile(
    r'^VERDICT:\s*(CONVERGED|OBSERVE|REVISE)\s*$', re.MULTILINE,
)
_CLASS_RE = re.compile(r'\*\*Class\*\*:\s*(REVISE|OBSERVE)', re.IGNORECASE)
_FINDING_FIELD_RE = re.compile(
    r'^\s*\*\*(Class|Foundation|ASN|Issue|What needs resolving)\*\*\s*:',
    re.MULTILINE,
)

# Phantom rejection: the original finding quoted phrases that don't
# exist in the note (reviewer hallucination). The reviser's rationale
# typically says "is not present" / "is absent" / "already resolved" /
# "no longer contains" / "does not appear". Carrying these forward into
# the next reviewer's prompt poisons it — the reviewer pattern-matches
# on the fabricated-quote shape and produces a fresh fabrication. Skip
# them so only substantive rejections (where the reviser argued the
# finding was wrong on the merits) influence subsequent reviews.
_PHANTOM_RATIONALE_RE = re.compile(
    r"\b(not present|is absent|are absent|already resolved"
    r"|no longer contains?|do(?:es)? not appear"
    r"|is not in the current|are not in the current)\b",
    re.IGNORECASE,
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

    template = read_prompt(REVIEW_TEMPLATE)
    if not template:
        print("  [ERROR] Audit template not found", file=sys.stderr)
        return "ERROR", None, 0

    depends = claim_asn_dep_ids(asn_num)
    depends_str = ", ".join(format_label(d) for d in depends)

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

    result = invoke_claude(prompt, model=model, effort="high")

    if not result.text:
        print(f"  FAILED (exit 1, {result.elapsed:.0f}s)", file=sys.stderr)
        return "ERROR", None, result.elapsed

    verdict = parse_verdict(result.text)
    finding_count = len(re.findall(r'^### ', result.text, re.MULTILINE))
    print(
        f" verdict={verdict}, {finding_count} finding(s) ({result.elapsed:.0f}s)",
        file=sys.stderr,
    )

    return verdict, result.text, result.elapsed


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


def previously_declined_findings(
    session: Session,
    cone_addrs: List[Address],
    max_rejects: int = 5,
) -> str:
    """Return text of recently-declined findings on this cone.

    A declined finding is a `comment.revise` targeting any cone claim
    that was closed by `resolution.reject` (the reviser refused to act).
    Each block contains the original finding body plus the reviser's
    rationale text. Sorted by recency, capped at `max_rejects`.

    Accepted findings (closed by `resolution.edit`) are NOT included —
    their resolution lives in the prose itself, so re-evaluating the
    current prose is the correct check on whether the issue persists.
    Open findings (no resolution yet) are NOT included either — the
    runner closes them naturally via the claim-revise refiner.
    """
    cone_addr_set = set(a for a in cone_addrs if a is not None)
    rejects = session.find_links(type_="resolution.reject")

    blocks = []
    # Newest-first: LinkStore preserves emission order, so reverse it
    for r in reversed(rejects):
        if len(blocks) >= max_rejects:
            break
        if not r.to_set or len(r.to_set) < 2:
            continue
        # Substrate convention (matches legacy + migrated data):
        # resolution.reject has F=[rationale_doc], G=[comment_addr, ...]
        # — the comment is in to_set; rationale path is the second to_set
        # entry under the legacy convention. Preserve that here.
        comment_addr = r.to_set[0]
        rationale_addr = r.to_set[1]

        try:
            comment = session.get_link(comment_addr)
        except KeyError:
            continue
        if not comment.to_set:
            continue
        if comment.to_set[0] not in cone_addr_set:
            continue
        if not comment.from_set:
            continue

        try:
            finding_body = read_doc(session, comment.from_set[0]).strip()
        except (KeyError, FileNotFoundError):
            continue

        try:
            rationale_text = read_doc(session, rationale_addr).strip()
        except (KeyError, FileNotFoundError):
            rationale_text = "(rationale missing)"

        if _PHANTOM_RATIONALE_RE.search(rationale_text):
            # Reviewer hallucinated the original quote — skip to avoid
            # priming the next reviewer with the fabricated-quote shape.
            continue

        blocks.append(
            f"### Declined\n\n"
            f"**Finding (rejected as invalid):**\n\n{finding_body}\n\n"
            f"**Reviser's rationale for declining:**\n\n{rationale_text}"
        )

    return "\n\n---\n\n".join(blocks) if blocks else ""
