"""Validate-revise gate for V-cycle drivers.

Runs the validator at the top of each review/revise cycle and invokes
validate-revise to clear structural violations before the LLM reviewer
reads state. Implements the Validation Principle operationally: no LLM
review cycle operates on state that has not been mechanically verified.

Filter semantics per driver (set by passing scope_labels):
  - full-review:   scope_labels=None (whole ASN)
  - regional:      scope_labels={apex} | deps

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


VALIDATE = _load("convergence_validate", _SCRIPTS / "convergence-validate.py")
REVISE = _load("convergence_validate_revise",
               _SCRIPTS / "convergence-validate-revise.py")


def _run_validator(asn_label):
    claim_dir = VALIDATE.claim_convergence_dir(asn_label)
    pairs = VALIDATE.load_pairs(claim_dir)
    return VALIDATE.run_all_checks(pairs)


def _actionable(findings, declined):
    """Subset of findings that the reviser should act on: non-cycle,
    not-yet-declined by reviser judgment.

    Declined keys are (stem, rule) — yaml/md variants of the same claim
    share a stem, so a decline on either side suppresses the other.
    """
    out = []
    for f in findings:
        if f["rule"] == "acyclic-depends":
            continue
        filename = f.get("file")
        if filename and (Path(filename).stem, f["rule"]) in declined:
            continue
        out.append(f)
    return out


def run_validate_gate(asn_label, scope_labels=None, max_iterations=3):
    """Run validator + validate-revise until clean or iterations exhausted.

    The gate tracks (filename, rule) pairs where the reviser produced no
    change — those are treated as declined-by-design and not re-attempted.
    A declined pair still surfaces in validator output; the gate just stops
    acting on it.

    Returns:
      "clean"  — no actionable findings in scope (cycles/declines may remain)
      "dirty"  — actionable findings remain after max_iterations or halted
      "failed" — reviser raised an exception
    """
    scope = set(scope_labels) if scope_labels is not None else None
    declined = set()
    prev_actionable = None

    for iteration in range(1, max_iterations + 1):
        findings = _run_validator(asn_label)
        relevant = REVISE.filter_findings_by_scope(findings, scope)
        cycle_findings = [f for f in relevant if f["rule"] == "acyclic-depends"]
        actionable = _actionable(relevant, declined)

        if not actionable:
            if declined:
                print(f"  [GATE] {len(declined)} (file, rule) pair(s) "
                      f"declined by reviser; treating as terminal",
                      file=sys.stderr)
            if cycle_findings:
                print(f"  [GATE] {len(cycle_findings)} cycle finding(s) "
                      f"in scope (propose-only; not blocking):",
                      file=sys.stderr)
                for f in cycle_findings:
                    print(f"    {f['detail']}", file=sys.stderr)
            return "clean"

        if prev_actionable is not None and len(actionable) >= prev_actionable:
            print(f"  [GATE] no progress ({prev_actionable} → "
                  f"{len(actionable)} actionable); halting",
                  file=sys.stderr)
            return "dirty"
        prev_actionable = len(actionable)

        print(f"  [GATE iter {iteration}] {len(actionable)} actionable "
              f"finding(s) in scope; invoking validate-revise",
              file=sys.stderr)

        try:
            _before, _after, declined = REVISE.run_passes(
                asn_label,
                scope_labels=scope,
                mode="apply",
                commit=True,
                skip_pairs=declined,
            )
        except Exception as e:
            print(f"  [GATE] reviser raised: {e}", file=sys.stderr)
            return "failed"

    print(f"  [GATE] max iterations ({max_iterations}) reached; "
          f"halting with remaining findings",
          file=sys.stderr)
    return "dirty"
