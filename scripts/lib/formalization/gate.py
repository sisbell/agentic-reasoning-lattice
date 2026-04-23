"""Validate-revise gate for V-cycle drivers.

Runs the validator at the top of each review/revise cycle and invokes
validate-revise to clear structural violations before the LLM reviewer
reads state. Implements the Validation Principle operationally: no LLM
review cycle operates on state that has not been mechanically verified.

Filter semantics per driver (set by passing scope_labels):
  - full-review:   scope_labels=None (whole ASN)
  - regional:      scope_labels={apex} | deps
  - local-review:  scope_labels=set(review_labels)

Cycle findings (acyclic-depends) are propose-only; the gate logs them as
warnings but does not try to fix them, and does not block the driver.
"""

import importlib.util
import sys
from pathlib import Path


_SCRIPTS = Path(__file__).resolve().parent.parent.parent


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


VALIDATE = _load("formalization_validate", _SCRIPTS / "formalization-validate.py")
REVISE = _load("formalization_validate_revise",
               _SCRIPTS / "formalization-validate-revise.py")


def _run_validator(asn_label):
    claim_dir = VALIDATE.formalization_dir(asn_label)
    pairs = VALIDATE.load_pairs(claim_dir)
    return VALIDATE.run_all_checks(pairs)


def run_validate_gate(asn_label, scope_labels=None, max_iterations=3):
    """Run validator + validate-revise until clean or iterations exhausted.

    Returns:
      "clean"  — no fixable findings in scope (cycles may be logged)
      "dirty"  — findings remain after max_iterations
      "failed" — reviser raised an exception
    """
    scope = set(scope_labels) if scope_labels is not None else None

    for iteration in range(1, max_iterations + 1):
        findings = _run_validator(asn_label)
        relevant = REVISE.filter_findings_by_scope(findings, scope)

        cycle_findings = [f for f in relevant if f["rule"] == "acyclic-depends"]
        fixable = [f for f in relevant if f["rule"] != "acyclic-depends"]

        if not fixable:
            if cycle_findings:
                print(f"  [GATE] {len(cycle_findings)} cycle finding(s) "
                      f"in scope (propose-only; not blocking):",
                      file=sys.stderr)
                for f in cycle_findings:
                    print(f"    {f['detail']}", file=sys.stderr)
            return "clean"

        print(f"  [GATE iter {iteration}] {len(fixable)} fixable "
              f"finding(s) in scope; invoking validate-revise",
              file=sys.stderr)

        try:
            before, after = REVISE.run_passes(
                asn_label,
                scope_labels=scope,
                mode="apply",
                commit=True,
            )
        except Exception as e:
            print(f"  [GATE] reviser raised: {e}", file=sys.stderr)
            return "failed"

        if after >= before:
            print(f"  [GATE] no progress ({before} → {after}); halting",
                  file=sys.stderr)
            return "dirty"

    print(f"  [GATE] max iterations ({max_iterations}) reached; "
          f"halting with remaining findings",
          file=sys.stderr)
    return "dirty"
