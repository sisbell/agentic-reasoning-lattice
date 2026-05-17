"""Claim structural-audit scout — first scout-caste agent.

Fires per-claim. One fire = run the structural validator on the
claim's directory, emit an audit doc capturing what was checked,
emit per-violation findings + comment.violation links so the
structural-fix refiner can close them via existing resolution
machinery.

The audit doc carries `review.structural` classifier (parallel to
`review.content` for LLM reviews) and a `review.coverage` link to
the claim. Even on a zero-violations fire, the audit doc is still
emitted — it's the structural fact "audit ran on this claim at
moment T," carried by the audit.coverage tumbler addr.

No verb-flag classifiers. The substrate state itself (audit doc +
review.coverage + per-violation findings + their resolution status)
carries everything the predicate needs to decide whether to re-fire.

Caste: scout. Working surface = structural form (validator rules
over claim md content). Identity grant = audit doc + per-finding
docs. Detection happens *here* (the validator runs inside the
agent), distinguishing this from a producer that just persists
detection done upstream.
"""

from __future__ import annotations

import importlib.util
import re
import sys
import time
from pathlib import Path
from typing import ClassVar

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.backend.emit import (
    emit_comment, emit_derivation, emit_finding,
    emit_review_coverage, emit_review_structural,
)
from lib.protocols.febe.protocol import Session
from lib.lattice.labels import parse_claim_doc_path
from lib.shared.paths import (
    CLAIM_AUDITS_DIR, CLAIM_FINDINGS_DIR, WORKSPACE,
    audit_doc_path, next_audit_number,
)


REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPTS_DIR = REPO_ROOT / "scripts"


def _load_validator():
    spec = importlib.util.spec_from_file_location(
        "claim_validate", SCRIPTS_DIR / "claim-validate.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


VALIDATOR = _load_validator()


def _run_validator(asn_label: str, claim_base_dir: Path) -> list:
    claim_dir = claim_base_dir / asn_label
    pairs = VALIDATOR.load_pairs(claim_dir)
    return VALIDATOR.run_all_checks(pairs, claim_dir=claim_dir)


def _filter_to_claim(findings: list, claim_label: str) -> list:
    """Restrict findings to those targeting this claim's stem."""
    relevant = []
    for f in findings:
        if f["rule"] == "acyclic-depends":
            continue  # propose-mode, retired
        filename = f.get("file")
        if filename and Path(filename).stem == claim_label:
            relevant.append(f)
        elif not filename and claim_label in f.get("detail", ""):
            relevant.append(f)
    return relevant


def _render_audit_body(
    asn_label: str, claim_label: str,
    rule_outcomes: dict, audit_num: int,
) -> str:
    """Render the audit doc's markdown body.

    rule_outcomes is {rule_name: count_of_violations}; rules with
    zero violations are listed as 'clean' for audit-trail clarity.
    """
    lines = [
        f"# Structural Audit — {asn_label}/{claim_label} (audit-{audit_num})",
        "",
        f"**Timestamp:** {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}",
        "",
        "## Rules checked",
        "",
    ]
    for rule, count in sorted(rule_outcomes.items()):
        status = "clean" if count == 0 else f"{count} violation(s)"
        lines.append(f"- {rule}: {status}")
    lines.append("")
    return "\n".join(lines)


def _render_violation_body(
    asn_label: str, claim_label: str, finding: dict,
) -> str:
    """Render a per-violation finding doc body."""
    rule = finding["rule"]
    file = finding.get("file") or "(unknown)"
    line = finding.get("line")
    detail = finding.get("detail", "")
    body_lines = [
        f"# Structural Violation: {rule}",
        "",
        f"**Claim:** {asn_label}/{claim_label}",
        f"**File:** {file}",
    ]
    if line:
        body_lines.append(f"**Line:** {line}")
    body_lines.extend(["", "## Detail", "", detail, ""])
    return "\n".join(body_lines)


def _violation_finding_path(
    asn_label: str, claim_label: str, audit_num: int,
    rule: str, n: int,
):
    """Path for a per-violation finding doc.

    Co-located with content-review findings under CLAIM_FINDINGS_DIR
    by the shared `audit-N` token (parallel to `review-N` for content
    findings).
    """
    return (
        CLAIM_FINDINGS_DIR / asn_label / f"audit-{audit_num}"
        / f"{rule}-{n}.md"
    )


# ─── Agent class ────────────────────────────────────────────────────


class ClaimStructuralAuditAgent(Agent):
    """One claim's structural audit per fire.

    Runs the validator, emits audit doc + review.structural
    classifier + review.coverage link, then per-violation finding
    docs + finding classifier + comment.violation + provenance.
    Always emits the audit doc, even when zero violations are found —
    the audit-coverage tumbler is the structural fact "audit ran."
    """

    role: ClassVar[str] = "claim-structural-audit"
    node: ClassVar[str] = "1.3"

    def run(self, session: Session, claim_addr: Address) -> AgentResult:
        claim_rel = session.get_path_for_addr(claim_addr)
        if claim_rel is None:
            return AgentResult(success=False, detail="no-claim-path")

        parsed = parse_claim_doc_path(claim_rel)
        if parsed is None:
            return AgentResult(success=False, detail="unparseable-claim-path")
        asn_label, claim_label, asn_num = parsed

        # Run validator + filter to this claim.
        all_findings = _run_validator(asn_label, self.claim_dir)
        relevant = _filter_to_claim(all_findings, claim_label)

        # Per-rule outcome counts (every checked rule appears, even clean ones).
        rules_checked = {
            "body-uniqueness", "declaration-label-mismatch",
            "declared-symbols-resolve", "depends-agreement",
            "references-resolve",
        }
        rule_outcomes = {r: 0 for r in rules_checked}
        for f in relevant:
            if f["rule"] in rule_outcomes:
                rule_outcomes[f["rule"]] += 1

        # Emit the audit doc.
        audit_num = next_audit_number(asn_label, claim_label)
        audit_path = audit_doc_path(asn_label, claim_label, audit_num)
        audit_body = _render_audit_body(
            asn_label, claim_label, rule_outcomes, audit_num,
        )
        audit_rel = str(
            audit_path.resolve().relative_to(WORKSPACE.resolve())
        )
        session.update_document(audit_rel, audit_body)
        audit_addr = session.register_path(audit_rel)
        emit_review_structural(session.store, audit_addr)
        emit_review_coverage(session.store, audit_addr, claim_addr)

        # Per-violation findings + comment.violation + provenance.
        for n, f in enumerate(relevant):
            finding_path = _violation_finding_path(
                asn_label, claim_label, audit_num, f["rule"], n,
            )
            finding_body = _render_violation_body(
                asn_label, claim_label, f,
            )
            finding_rel = str(
                finding_path.resolve().relative_to(WORKSPACE.resolve())
            )
            session.update_document(finding_rel, finding_body)
            finding_addr = session.register_path(finding_rel)
            emit_finding(session.store, finding_addr)
            emit_comment(
                session.store, finding_addr, claim_addr, kind="violation",
            )
            emit_derivation(session.store, audit_addr, finding_addr)

        print(
            f"  [STRUCTURAL-AUDIT] {asn_label}/{claim_label} "
            f"audit-{audit_num} violations={len(relevant)}",
            file=sys.stderr,
        )

        return AgentResult(
            success=True,
            detail=f"violations={len(relevant)}",
        )
