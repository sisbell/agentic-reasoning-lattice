"""Validate-revise gate for review producers.

Runs the structural validator at the top of each review/revise cycle
and dispatches the lifted ClaimStructuralFixAgent (via runner) to
clear violations before the LLM reviewer reads state. Implements the
Validation Principle operationally: no LLM review cycle operates on
state that has not been mechanically verified.

Filter semantics per driver (set by passing scope_labels):
  - full-review:   scope_labels=None (whole ASN — all derived claims)
  - regional:      scope_labels={apex} | deps

Cycle findings (acyclic-depends) are propose-only; the gate logs them
as warnings but does not try to fix them, and does not block the
driver. Propose mode itself was retired in the structural-rule-fix
lift; surfacing cycle warnings here is purely informational.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from lib.runner import Scope, run_until_quiescent
from lib.shared.paths import CLAIM_DIR


_SCRIPTS = Path(__file__).resolve().parent.parent.parent


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


VALIDATE = _load("claim_validate", _SCRIPTS / "claim-validate.py")


def _run_validator(asn_label):
    claim_dir = CLAIM_DIR / asn_label
    pairs = VALIDATE.load_pairs(claim_dir)
    return VALIDATE.run_all_checks(pairs, claim_dir=claim_dir)


def _cycle_findings(findings, scope_labels):
    """Cycle findings (acyclic-depends) within scope, for reporting."""
    if scope_labels is None:
        return [f for f in findings if f["rule"] == "acyclic-depends"]
    out = []
    for f in findings:
        if f["rule"] != "acyclic-depends":
            continue
        detail = f.get("detail", "")
        if any(lbl in detail for lbl in scope_labels):
            out.append(f)
    return out


def run_validate_gate(asn_label, scope_labels=None, max_iterations=3):
    """Run the structural-fix trigger over scope until clean.

    The runner walks ClaimStructuralFixAgent over claims in scope;
    each fire runs the validator on that claim and applies fixes pass
    by pass. The gate is satisfied when the runner reaches quiescence.

    Returns:
      "clean"  — runner reached quiescence; cycle findings (if any)
                 are logged but not blocking
      "dirty"  — runner exhausted max_iterations with findings remaining
      "failed" — runner reported errors on one or more fires
    """
    # Lazy import to avoid the circular path validate_gate → triggers
    # → cone_review trigger → cone_review agent → validate_gate.
    from lib.triggers import claim_structural_audit, claim_structural_fix

    asn_num = int(asn_label[4:])
    labels = (
        frozenset(scope_labels) if scope_labels is not None else None
    )
    scope = Scope(asn_label=asn_label, labels=labels)

    print(
        f"  [GATE] validate-revise on {asn_label}"
        + (f" scope={sorted(scope_labels)}" if scope_labels else ""),
        file=sys.stderr,
    )
    result = run_until_quiescent(
        triggers=[claim_structural_audit, claim_structural_fix],
        scope=scope,
        max_iterations=max_iterations,
    )

    if result.errors:
        for trigger_name, addr, err in result.errors[:3]:
            print(
                f"  [GATE] {trigger_name} on {addr} failed: {err}",
                file=sys.stderr,
            )
        return "failed"

    cycles = _cycle_findings(_run_validator(asn_label), scope_labels)
    if cycles:
        print(
            f"  [GATE] {len(cycles)} cycle finding(s) in scope "
            f"(propose-only; not blocking):",
            file=sys.stderr,
        )
        for f in cycles:
            print(f"    {f['detail']}", file=sys.stderr)

    if not result.quiescent:
        print(
            f"  [GATE] max iterations ({max_iterations}) reached; "
            f"halting with remaining findings",
            file=sys.stderr,
        )
        return "dirty"
    return "clean"
