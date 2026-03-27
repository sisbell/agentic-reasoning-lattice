"""
Unified ASN pipeline — one flow for discovery, review, and rebase.

Steps:
1. Format gate — normalize table + headers
2. Deps generation — mechanical property graph
3. Audit — mechanical + LLM checks (if ASN has dependencies)
4. Proof verification — per-proof, dependency-ordered (opus)
5. General review/revise — cross-cutting analysis (opus)
6. Assembly — formal-statements.md + deps YAML (post-convergence)
7. Cleanup — clear open-issues, update timestamps

Usage:
    from lib.asn_pipeline import run_pipeline
    run_pipeline(34)                    # full pipeline
    run_pipeline(34, force=True)        # ignore cached state
    run_pipeline(34, start_step="verify")  # start from proof verification
"""

import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from paths import (WORKSPACE, ASNS_DIR, REVIEWS_DIR, load_manifest,
                   formal_stmts, dep_graph, open_issues_path, project_yaml)
from lib.common import find_asn, step_commit_asn


STEPS = ["format", "deps", "repair", "audit", "verify", "review", "assembly", "cleanup"]


# ---------------------------------------------------------------------------
# Step 1: Format Gate
# ---------------------------------------------------------------------------

def step_format(asn_num):
    """Run format normalization. Returns True if clean."""
    from lib.normalize_format import normalize_format
    print(f"\n  [1/8 FORMAT]", file=sys.stderr)
    ok = normalize_format(asn_num)
    if ok:
        step_commit_asn(asn_num, hint="format normalized")
    return ok


# ---------------------------------------------------------------------------
# Step 2: Deps Generation
# ---------------------------------------------------------------------------

def step_deps(asn_num):
    """Generate dependency YAML. Returns True on success."""
    from lib.rebase_deps import generate_deps, write_deps_yaml
    print(f"\n  [2/8 DEPS]", file=sys.stderr)
    deps = generate_deps(asn_num)
    if deps:
        write_deps_yaml(asn_num, deps)
        step_commit_asn(asn_num, hint="deps generated")
        return True
    print(f"  [DEPS] No property table found", file=sys.stderr)
    return False


# ---------------------------------------------------------------------------
# Step 3: Section Repair
# ---------------------------------------------------------------------------

def step_repair(asn_num):
    """Repair incomplete sections. Returns True on success."""
    from lib.repair_sections import step_repair_sections
    print(f"\n  [3/8 REPAIR]", file=sys.stderr)
    repaired, skipped, failed = step_repair_sections(asn_num)
    if repaired > 0:
        step_commit_asn(asn_num, hint="section repair")
    return failed == 0


# ---------------------------------------------------------------------------
# Step 4: Audit (if ASN has dependencies)
# ---------------------------------------------------------------------------

def step_audit(asn_num):
    """Run audit checks — mechanical + LLM. Returns True on success."""
    manifest = load_manifest(asn_num)
    if not manifest.get("depends"):
        print(f"\n  [4/8 AUDIT] Skipped (no dependencies)", file=sys.stderr)
        return True

    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return False

    from lib.rebase_asn import (
        step_surface_check, step_find_extensions, step_verify_transfer,
        step_audit as step_open_audit, _append_open_issues,
    )

    print(f"\n  [4/8 AUDIT]", file=sys.stderr)

    # 3a: Mechanical checker
    print(f"  [AUDIT 1/4] Mechanical checker...", file=sys.stderr)
    try:
        from lib.rebase_mechanical import check_asn, format_findings
        findings = check_asn(asn_num)
        if findings:
            _append_open_issues(asn_num, format_findings(findings))
            print(f"  [MECHANICAL] {len(findings)} findings", file=sys.stderr)
        else:
            print(f"  [MECHANICAL] Clean", file=sys.stderr)
    except Exception as e:
        print(f"  [MECHANICAL] WARNING: {e}", file=sys.stderr)

    # 3b: Extension verification
    print(f"  [AUDIT 2/4] Extension verification...", file=sys.stderr)
    try:
        from lib.rebase_extensions import extract_claims, verify_claims
        from lib.rebase_extensions import format_findings as fmt_ext
        claims = extract_claims(asn_num)
        if claims:
            results = verify_claims(claims, model="sonnet", effort="high")
            ext_findings = fmt_ext(results)
            if ext_findings:
                _append_open_issues(asn_num, ext_findings)
                print(f"  [EXTENSIONS] Gaps found", file=sys.stderr)
            else:
                print(f"  [EXTENSIONS] All verified", file=sys.stderr)
        else:
            print(f"  [EXTENSIONS] No claims", file=sys.stderr)
    except Exception as e:
        print(f"  [EXTENSIONS] WARNING: {e}", file=sys.stderr)

    # 3c: Surface check
    print(f"  [AUDIT 3/4] Surface check...", file=sys.stderr)
    step_surface_check(asn_num, asn_path, asn_label)

    # 3d: Open-ended audit
    print(f"  [AUDIT 4/4] Open-ended audit...", file=sys.stderr)
    step_open_audit(asn_num, asn_path, asn_label)

    step_commit_asn(asn_num, hint="audit complete")
    return True


# ---------------------------------------------------------------------------
# Step 4: Proof Verification
# ---------------------------------------------------------------------------

def step_verify(asn_num):
    """Per-proof verification. Returns True if all verified."""
    from lib.verify_proofs import step_verify_proofs
    print(f"\n  [5/8 VERIFY]", file=sys.stderr)
    verified, found, errors = step_verify_proofs(asn_num)
    step_commit_asn(asn_num, hint="proof verification")
    return found == 0 and errors == 0


# ---------------------------------------------------------------------------
# Step 5: General Review/Revise
# ---------------------------------------------------------------------------

def step_review(asn_num, max_cycles=30):
    """General review/revise cycle. Returns True if converged."""
    print(f"\n  [6/8 REVIEW]", file=sys.stderr)

    # Run initial review
    review_cmd = [sys.executable,
                  str(WORKSPACE / "scripts" / "review.py"),
                  str(asn_num), "--general"]
    review_result = subprocess.run(review_cmd, capture_output=False,
                                   text=True, cwd=str(WORKSPACE))

    if review_result.returncode == 2:
        print(f"  [REVIEW] CONVERGED", file=sys.stderr)
        return True
    elif review_result.returncode == 1:
        print(f"  [REVIEW] Failed", file=sys.stderr)
        return False

    # Has findings — run convergence
    print(f"  [REVIEW] Running convergence...", file=sys.stderr)
    converge_cmd = [sys.executable,
                    str(WORKSPACE / "scripts" / "revise.py"),
                    str(asn_num),
                    "--converge", str(max_cycles)]
    converge_result = subprocess.run(converge_cmd, capture_output=False,
                                     text=True, cwd=str(WORKSPACE))
    return converge_result.returncode == 0


# ---------------------------------------------------------------------------
# Step 6: Assembly
# ---------------------------------------------------------------------------

def step_assembly(asn_num):
    """Assemble formal-statements.md + final deps YAML. Returns True."""
    from lib.normalize_format import assemble_formal_statements
    from lib.rebase_deps import generate_deps, write_deps_yaml
    print(f"\n  [7/8 ASSEMBLY]", file=sys.stderr)

    assemble_formal_statements(asn_num)

    deps = generate_deps(asn_num)
    if deps:
        write_deps_yaml(asn_num, deps)

    step_commit_asn(asn_num, hint="assembly")
    return True


# ---------------------------------------------------------------------------
# Step 7: Cleanup
# ---------------------------------------------------------------------------

def step_cleanup(asn_num):
    """Clear open-issues, update timestamps. Returns True."""
    print(f"\n  [8/8 CLEANUP]", file=sys.stderr)

    # Clear open-issues (converged — all resolved)
    path = open_issues_path(asn_num)
    if path.exists():
        path.unlink()
        print(f"  [CLEANUP] Cleared open-issues", file=sys.stderr)

    # Update timestamps
    yaml_path = project_yaml(asn_num)
    if yaml_path.exists():
        import time as _time
        content = yaml_path.read_text()
        ts = _time.strftime("%Y-%m-%dT%H:%M:%S")

        if "last_pipeline_run:" in content:
            content = re.sub(r'^last_pipeline_run:.*$',
                             f'last_pipeline_run: "{ts}"', content,
                             flags=re.MULTILINE)
        else:
            content = content.rstrip() + f'\nlast_pipeline_run: "{ts}"\n'

        yaml_path.write_text(content)

    step_commit_asn(asn_num, hint="cleanup")
    return True


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

def run_pipeline(asn_num, force=False, start_step=None, max_review_cycles=30,
                 clear_issues=False):
    """Run the unified ASN pipeline.

    Args:
        asn_num: ASN number
        force: ignore cached state, run all steps
        start_step: start from this step (skip earlier steps)
        max_review_cycles: max cycles for general review convergence
        clear_issues: clear open-issues before running

    Returns:
        "completed" — pipeline converged
        "failed" — a step failed
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return "failed"

    if clear_issues:
        path = open_issues_path(asn_num)
        if path.exists():
            path.unlink()
            print(f"  [CLEARED] open-issues", file=sys.stderr)

    print(f"\n  {'='*50}", file=sys.stderr)
    print(f"  {asn_label} — pipeline", file=sys.stderr)
    print(f"  {'='*50}", file=sys.stderr)

    start_time = time.time()

    # Determine which steps to run
    start_idx = 0
    if start_step:
        if start_step in STEPS:
            start_idx = STEPS.index(start_step)
        else:
            print(f"  Unknown step: {start_step}. "
                  f"Valid: {', '.join(STEPS)}", file=sys.stderr)
            return "failed"

    steps = [
        ("format",   step_format),
        ("deps",     step_deps),
        ("repair",   step_repair),
        ("audit",    step_audit),
        ("verify",   step_verify),
        ("review",   lambda n: step_review(n, max_review_cycles)),
        ("assembly", step_assembly),
        ("cleanup",  step_cleanup),
    ]

    for i, (name, fn) in enumerate(steps):
        if i < start_idx:
            continue

        ok = fn(asn_num)
        if not ok and name in ("format", "deps"):
            # Critical steps — can't continue without them
            print(f"\n  [FAILED] {asn_label} — {name} step failed",
                  file=sys.stderr)
            return "failed"
        elif not ok and name == "review":
            # Review didn't converge
            print(f"\n  [FAILED] {asn_label} — review did not converge",
                  file=sys.stderr)
            return "failed"
        # verify and audit can have findings without blocking the pipeline
        # — the review step picks them up from open-issues

    elapsed = time.time() - start_time
    print(f"\n  {'='*50}", file=sys.stderr)
    print(f"  {asn_label} — completed ({elapsed:.0f}s)",
          file=sys.stderr)
    print(f"  {'='*50}", file=sys.stderr)
    return "completed"


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Unified ASN pipeline — format, verify, review, assemble")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument("--force", action="store_true",
                        help="Ignore cached state, run all steps")
    parser.add_argument("--step", choices=STEPS,
                        help="Start from this step (skip earlier)")
    parser.add_argument("--max-review-cycles", type=int, default=30,
                        help="Max general review/revise cycles")
    parser.add_argument("--clear-issues", action="store_true",
                        help="Clear open-issues before running")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    result = run_pipeline(asn_num, force=args.force, start_step=args.step,
                          clear_issues=args.clear_issues,
                          max_review_cycles=args.max_review_cycles)
    sys.exit(0 if result == "completed" else 1)


if __name__ == "__main__":
    main()
