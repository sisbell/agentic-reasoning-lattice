"""
Formalization pipeline — stabilize, repair, quality, verify, assemble.

Steps:
1. Stabilize — format gate + deps generation
2. Repair — standalone proofs for every property
3. Quality — Dijkstra rewrite + formal contracts
4. Audit — mechanical + LLM checks (if ASN has dependencies)
5. Verify — per-proof verification, dependency-ordered (opus)
6. Assembly — formal-statements.md + deps YAML
7. Cleanup — clear open-issues, update timestamps

Usage:
    from lib.formalization.run import run_pipeline
    run_pipeline(34)                    # full pipeline
    run_pipeline(34, force=True)        # ignore cached state
    run_pipeline(34, start_step="verify")  # start from proof verification
"""

import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import (WORKSPACE, ASNS_DIR, REVIEWS_DIR, load_manifest,
                   formal_stmts, dep_graph, open_issues_path, project_yaml)
from lib.shared.common import find_asn, step_commit_asn


STEPS = ["stabilize", "repair", "stabilize", "quality", "stabilize", "audit", "verify", "stabilize", "assembly", "cleanup"]


# ---------------------------------------------------------------------------
# Stabilize: Format Gate + Deps Generation
# ---------------------------------------------------------------------------

def step_stabilize(asn_num):
    """Run format gate + deps generation. Returns True on success."""
    from lib.formalization.format import normalize_format
    from lib.formalization.deps import generate_deps, write_deps_yaml

    print(f"\n  [STABILIZE] Format + Deps", file=sys.stderr)

    # Format gate
    ok = normalize_format(asn_num)
    if not ok:
        return False

    # Deps generation
    deps = generate_deps(asn_num)
    if deps:
        write_deps_yaml(asn_num, deps)

    step_commit_asn(asn_num, hint="stabilize")
    return True


# ---------------------------------------------------------------------------
# Step 3: Section Repair
# ---------------------------------------------------------------------------

def step_repair(asn_num):
    """Repair incomplete sections. Returns True on success."""
    from lib.formalization.repair import step_repair_sections
    print(f"\n  [3/9 REPAIR]", file=sys.stderr)
    repaired, skipped, failed = step_repair_sections(asn_num)
    if repaired > 0:
        step_commit_asn(asn_num, hint="section repair")
    return failed == 0


# ---------------------------------------------------------------------------
# Step 4: Quality Pass
# ---------------------------------------------------------------------------

def step_quality(asn_num):
    """Dijkstra rewrite + formal contracts. Returns True on success."""
    from lib.formalization.quality import step_quality_pass
    print(f"\n  [4/9 QUALITY]", file=sys.stderr)
    rewritten, failed = step_quality_pass(asn_num)
    if rewritten > 0:
        step_commit_asn(asn_num, hint="quality pass")
    return failed == 0


# ---------------------------------------------------------------------------
# Step 5: Audit (if ASN has dependencies)
# ---------------------------------------------------------------------------

def step_audit(asn_num):
    """Run audit checks — mechanical + LLM. Returns True on success."""
    manifest = load_manifest(asn_num)
    if not manifest.get("depends"):
        print(f"\n  [5/9 AUDIT] Skipped (no dependencies)", file=sys.stderr)
        return True

    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return False

    from lib.discovery.rebase import (
        step_surface_check, step_find_extensions, step_verify_transfer,
        step_audit as step_open_audit, _append_open_issues,
    )

    print(f"\n  [5/9 AUDIT]", file=sys.stderr)

    # 3a: Mechanical checker
    print(f"  [AUDIT 1/4] Mechanical checker...", file=sys.stderr)
    try:
        from lib.formalization.mechanical import check_asn, format_findings
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
        from lib.formalization.extensions import extract_claims, verify_claims
        from lib.formalization.extensions import format_findings as fmt_ext
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
    from lib.formalization.verify import step_verify_proofs
    print(f"\n  [6/9 VERIFY]", file=sys.stderr)
    verified, found, errors = step_verify_proofs(asn_num)
    step_commit_asn(asn_num, hint="proof verification")
    return found == 0 and errors == 0



# ---------------------------------------------------------------------------
# Step 6: Assembly
# ---------------------------------------------------------------------------

def step_assembly(asn_num):
    """Assemble formal-statements.md + final deps YAML. Returns True."""
    from lib.formalization.format import assemble_formal_statements
    from lib.formalization.deps import generate_deps, write_deps_yaml
    print(f"\n  [8/9 ASSEMBLY]", file=sys.stderr)

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
    print(f"\n  [9/9 CLEANUP]", file=sys.stderr)

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

def run_pipeline(asn_num, force=False, start_step=None, cycles=None):
    """Run the formalization pipeline.

    Args:
        asn_num: ASN number
        force: ignore cached state, run all steps
        start_step: start from this step (skip earlier steps)
        cycles: if set, run core loop N times without assembly/cleanup

    Returns:
        "completed" — pipeline converged
        "failed" — a step failed
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return "failed"

    # Clear open-issues at pipeline start
    path = open_issues_path(asn_num)
    if path.exists():
        path.unlink()
        print(f"  [CLEARED] open-issues", file=sys.stderr)

    if cycles is not None:
        mode = f"formalization ({cycles} cycle{'s' if cycles > 1 else ''})"
    else:
        mode = "formalization"
    print(f"\n  {'='*50}", file=sys.stderr)
    print(f"  {asn_label} — {mode}", file=sys.stderr)
    print(f"  {'='*50}", file=sys.stderr)

    start_time = time.time()

    # Core loop: stabilize → repair → quality → stabilize → audit → verify
    core_steps = [
        ("stabilize", step_stabilize),
        ("repair",    step_repair),
        ("stabilize", step_stabilize),
        ("quality",   step_quality),
        ("stabilize", step_stabilize),
        ("audit",     step_audit),
        ("verify",    step_verify),
    ]

    # Final steps: stabilize → assembly → cleanup (run once)
    final_steps = [
        ("stabilize", step_stabilize),
        ("assembly",  step_assembly),
        ("cleanup",   step_cleanup),
    ]

    # Determine where to start
    start_idx = 0
    skip_core = False
    final_start = 0

    if start_step:
        if start_step not in STEPS:
            print(f"  Unknown step: {start_step}. "
                  f"Valid: {', '.join(STEPS)}", file=sys.stderr)
            return "failed"
        final_names = [n for n, _ in final_steps]
        if start_step in final_names:
            skip_core = True
            final_start = final_names.index(start_step)
        else:
            core_names = [n for n, _ in core_steps]
            if start_step in core_names:
                start_idx = core_names.index(start_step)

    # Core loop
    num_cycles = cycles if cycles is not None else 1
    if not skip_core:
        for cycle in range(1, num_cycles + 1):
            if num_cycles > 1:
                print(f"\n  --- Cycle {cycle}/{num_cycles} ---", file=sys.stderr)

            for i, (name, fn) in enumerate(core_steps):
                if cycle == 1 and i < start_idx:
                    continue

                ok = fn(asn_num)
                if not ok and name == "stabilize":
                    print(f"\n  [FAILED] {asn_label} — stabilize step failed",
                          file=sys.stderr)
                    return "failed"

    # Final: stabilize → assembly → cleanup
    # Run when: no --cycles flag (full flow) OR --step targets a final step
    if cycles is None or skip_core:
        for i, (name, fn) in enumerate(final_steps):
            if i < final_start:
                continue

            ok = fn(asn_num)
            if not ok and name == "stabilize":
                print(f"\n  [FAILED] {asn_label} — stabilize step failed",
                      file=sys.stderr)
                return "failed"

    elapsed = time.time() - start_time
    print(f"\n  {'='*50}", file=sys.stderr)
    print(f"  {asn_label} — completed ({elapsed:.0f}s)",
          file=sys.stderr)
    print(f"  {'='*50}", file=sys.stderr)

    # Hint for cycles-only runs
    if cycles is not None and not skip_core:
        asn_short = str(asn_num).lstrip("0") or "0"
        print(f"\n  [NEXT] Assembly: python scripts/formalize.py {asn_short} --step assembly",
              file=sys.stderr)

    return "completed"


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Formalization pipeline — stabilize, repair, quality, verify, assemble")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument("--force", action="store_true",
                        help="Ignore cached state, run all steps")
    parser.add_argument("--step",
                        choices=["repair", "quality", "audit", "verify",
                                 "assembly", "cleanup"],
                        help="Start from this step (skip earlier)")
    parser.add_argument("--cycles", type=int, default=None,
                        help="Run core loop N times without assembly/cleanup")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    result = run_pipeline(asn_num, force=args.force, start_step=args.step,
                          cycles=args.cycles)
    sys.exit(0 if result == "completed" else 1)


if __name__ == "__main__":
    main()
