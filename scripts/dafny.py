#!/usr/bin/env python3
"""
Dafny — generate Dafny declarations incrementally per ASN property.

For each property in the ASN table, builds the prompt, launches a Claude
agent with Read/Write/Bash tools, and lets it write + verify + fix the .dfy
file autonomously. Each run creates a new modeling-N/ directory.

Requires: formal-statements.md (run normalize.py first)

Usage:
    python scripts/dafny.py 1
    python scripts/dafny.py ASN-0001 --property T5
    python scripts/dafny.py 1 --modeling 3       # into existing run
    python scripts/dafny.py 1 --dry-run
"""

import argparse
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import (WORKSPACE, DAFNY_DIR, USAGE_LOG,
                    next_modeling_number, load_manifest,
                    formal_stmts, check_dafny_module_coverage)
from lib.shared.common import extract_property_sections, find_asn
from lib.formalization.core.build_dependency_graph import generate_deps
from lib.formalization.core.topological_sort import topological_sort_labels
from lib.modeling.dafny.translate import (
    build_property_list_from_asn, read_proof_modules,
    build_property_prompt, translate_one, TEMPLATE,
)
from lib.modeling.dafny.verify import verify
from lib.modeling.dafny.align import align_validate_cycle
from lib.modeling.dafny.common import read_file, write_status_file, run_commit, log_usage


def main():
    parser = argparse.ArgumentParser(
        description="Generate Dafny declarations incrementally per ASN property")
    parser.add_argument("asn",
                        help="ASN number (e.g., 1, 0001, ASN-0001)")
    parser.add_argument("--property", "-p",
                        help="Generate specific properties, comma-separated (e.g., T5 or T1,T3,TA0)")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"],
                        help="Model (default: opus)")
    parser.add_argument("--effort", default="max",
                        help="Thinking effort level (low/medium/high/max)")
    parser.add_argument("--max-turns", type=int, default=24,
                        help="Max agent turns per property (default: 24)")
    parser.add_argument("--modeling", type=int, default=None,
                        help="Target existing modeling-N directory")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be generated without invoking Claude")
    parser.add_argument("--contract-only", action="store_true",
                        help="Skip generation, run contract review on existing .dfy files")
    parser.add_argument("--export", action="store_true",
                        help="Copy verified .dfy files to vault/4-proofs-staging/ASN-NNNN/")
    parser.add_argument("--force", action="store_true",
                        help="Rebuild all properties, ignore existing")
    args = parser.parse_args()

    # --- Locate inputs ---

    asn_number = int(re.sub(r"[^0-9]", "", str(args.asn)))
    asn_label = f"ASN-{asn_number:04d}"
    extract_path = formal_stmts(asn_number)
    if not extract_path.exists():
        print(f"  No formal statements found for {args.asn} at {extract_path}",
              file=sys.stderr)
        print(f"  Run: python scripts/normalize.py {args.asn}",
              file=sys.stderr)
        sys.exit(1)

    template_text = read_file(TEMPLATE)
    if not template_text:
        print("  Prompt template not found: scripts/prompts/modeling/dafny/translate-property.md",
              file=sys.stderr)
        sys.exit(1)

    # --- Parse inputs ---

    index_rows = build_property_list_from_asn(asn_number)
    print(f"  [SOURCE] ASN table + formal contracts", file=sys.stderr)

    extract_text = extract_path.read_text()

    if not index_rows:
        print(f"  No properties found", file=sys.stderr)
        sys.exit(1)

    # Coverage check: dafny_modules buckets should match formal-statements
    # Non-fatal — Level 2 builds work without module grouping
    coverage_errors = check_dafny_module_coverage(asn_number)
    if coverage_errors:
        for e in coverage_errors:
            print(f"  [COVERAGE] {e}", file=sys.stderr)
        print(f"  [COVERAGE] Continuing without module coverage (Level 2)",
              file=sys.stderr)

    # Proof module dependencies from project model manifest
    manifest = load_manifest(asn_number)
    module_names = manifest.get("modeling", {}).get("proof_imports", [])

    # Always include TumblerAlgebra as a base module
    base_modules = ["TumblerAlgebra"]
    all_modules = base_modules + [m for m in module_names if m not in base_modules]

    # Build imports map text for the prompt template
    imports_text = f"| ASN | Proof modules |\n|-----|---------------|\n| {asn_label} | {', '.join(all_modules)} |"

    proof_modules, proof_modules_text = read_proof_modules(all_modules)

    # Filter to specific properties if requested
    if args.property:
        targets = [t.strip() for t in args.property.split(",")]
        matches = []
        for target in targets:
            found = [r for r in index_rows
                     if r["label"] == target or r["proof_label"] == target]
            if not found:
                # Try prefix match
                found = [r for r in index_rows
                         if r["label"].lower().startswith(target.lower())
                         or r["proof_label"].lower().startswith(target.lower())]
            if not found:
                print(f"  Property '{target}' not found in property list",
                      file=sys.stderr)
                print(f"  Available: {', '.join(r['label'] for r in index_rows)}",
                      file=sys.stderr)
                sys.exit(1)
            matches.extend(found)
        index_rows = matches

    # --- Dependency ordering ---

    deps_data = generate_deps(asn_number)
    if deps_data:
        ordered_labels = topological_sort_labels(deps_data)
        label_to_row = {r["label"]: r for r in index_rows}
        ordered_rows = [label_to_row[l] for l in ordered_labels if l in label_to_row]
        # Add any not in the graph
        ordered_labels_set = set(ordered_labels)
        ordered_rows += [r for r in index_rows if r["label"] not in ordered_labels_set]
        index_rows = ordered_rows
        print(f"  [ORDER] Dependency-ordered ({len(index_rows)} properties)",
              file=sys.stderr)

    # Track verified files for dependency includes
    verified_files = {}  # label -> relative path within gen_dir

    # --- Contract-only mode ---

    if args.contract_only:
        from lib.modeling.dafny.validate import validate_batch
        from lib.modeling.dafny.common import find_modeling_dir
        modeling_dir = find_modeling_dir(asn_label, args.modeling)
        if modeling_dir is None:
            print(f"  No modeling directory found for {asn_label}",
                  file=sys.stderr)
            sys.exit(1)
        validate_batch(asn_number, modeling_dir)
        sys.exit(0)

    # --- Generate ---

    if args.modeling is not None:
        gen_num = args.modeling
        gen_dir = DAFNY_DIR / asn_label / f"modeling-{gen_num}"
        if not gen_dir.exists():
            print(f"  modeling-{gen_num} does not exist for {asn_label}",
                  file=sys.stderr)
            sys.exit(1)
    else:
        gen_num = next_modeling_number(asn_label)
        gen_dir = DAFNY_DIR / asn_label / f"modeling-{gen_num}"

    print(f"  [DAFNY-PROPERTY] {asn_label} (modeling-{gen_num})",
          file=sys.stderr)
    print(f"  Imports: {', '.join(module_names)}", file=sys.stderr)
    print(f"  Properties: {len(index_rows)}", file=sys.stderr)

    resuming = args.modeling is not None
    generated = 0
    skipped = 0
    failed = 0
    verified_ok = 0
    clean_count = 0
    flag_count = 0
    total_cost = 0
    results = []

    # Setup contract sections for validation
    stmts_text = extract_text  # formal-statements.md content
    # Build label map: PascalCase name -> label
    _label_map = {}
    for _line in stmts_text.split("\n"):
        _m = re.match(r'^##\s+(.+?)\s+\u2014\s+(.+?)(?:\s+\(|$)', _line)
        if _m:
            _label = _m.group(1).strip()
            _name = _m.group(2).strip()
            _pascal = re.match(r'^([A-Z][a-zA-Z0-9]+)', _name)
            if _pascal:
                _label_map[_pascal.group(1)] = _label
    _all_labels = list(set(_label_map.values()))
    contract_sections = extract_property_sections(stmts_text,
                                                   known_labels=_all_labels,
                                                   truncate=False)

    # Initialize CONTRACT-REVIEW.md
    review_path = gen_dir / "CONTRACT-REVIEW.md"
    gen_dir.mkdir(parents=True, exist_ok=True)
    with open(review_path, "w") as rf:
        rf.write(f"# Contract Review \u2014 {asn_label} (modeling-{gen_num})\n\n")
        rf.write(f"*Reviewed: {time.strftime('%Y-%m-%d %H:%M')}*\n\n")

    for row in index_rows:
        label = row["label"]
        proof_label = row["proof_label"]
        out_path = gen_dir / f"{proof_label}.dfy"

        # Skip existing when resuming into an existing run
        if resuming and out_path.exists():
            print(f"  [SKIP] {label} \u2192 {proof_label} (exists)", file=sys.stderr)
            verified_files[label] = f"{proof_label}.dfy"
            skipped += 1
            continue

        # Build dependency context for this property
        dep_context = ""
        if deps_data and label in deps_data.get("properties", {}):
            follows = deps_data["properties"][label].get("follows_from", [])
            available = [(dep, verified_files[dep]) for dep in follows
                         if dep in verified_files]
            if available:
                lines = ["## Available verified lemmas (from this build)\n"]
                for dep_label, dep_file in available:
                    lines.append(f"- {dep_label}: `include \"./{dep_file}\"`")
                dep_context = "\n".join(lines) + "\n"

        # Build prompt
        prompt = build_property_prompt(
            template_text, imports_text, proof_modules_text,
            row, extract_text, dep_context=dep_context,
        )

        if args.dry_run:
            print(f"  [DRY] {label} \u2192 {proof_label}.dfy"
                  f" (~{len(prompt) // 4} tokens)",
                  file=sys.stderr)
            continue

        # Launch agent — it writes, verifies, and fixes autonomously
        gen_dir.mkdir(parents=True, exist_ok=True)
        print(f"  [{label}] {proof_label}...",
              file=sys.stderr, end="", flush=True)
        wrote, elapsed, cost = translate_one(
            prompt, out_path,
            model=args.model, effort=args.effort, max_turns=args.max_turns,
        )
        total_cost += cost

        if not wrote:
            print(f" no file written", file=sys.stderr)
            failed += 1
            continue

        # Final verification — three-way check
        status, vout = verify(out_path)
        contract_result = ""

        if status == "verified":
            m = re.search(r"(\d+) verified", vout)
            n = m.group(1) if m else "?"
            print(f" verified({n})", file=sys.stderr, end="", flush=True)
            verified_ok += 1
            verified_files[label] = f"{proof_label}.dfy"

            # Validate contract — align cycle if FLAG
            section = contract_sections.get(label, "")
            if section:
                contract_result, reason, a_cost = align_validate_cycle(
                    out_path, section, label,
                    model=args.model, effort=args.effort)
                total_cost += a_cost

                if contract_result == "FLAG":
                    flag_count += 1
                    with open(review_path, "a") as rf:
                        rf.write(f"## {label} \u2014 {proof_label}\n\n{reason}\n\n")
                elif contract_result == "CLEAN":
                    clean_count += 1
            else:
                print(f" (no contract)", file=sys.stderr)
        elif status == "compile_failure":
            print(f" COMPILE FAILURE", file=sys.stderr)
            for line in vout.split("\n"):
                if re.search(r"Error:", line):
                    print(f"    {line.strip()}", file=sys.stderr)
                    break
        elif status == "proof_failure":
            print(f" PROOF FAILURE", file=sys.stderr)
            for line in vout.split("\n"):
                if re.search(r"Error:", line):
                    print(f"    {line.strip()}", file=sys.stderr)
                    break
        else:
            print(f" {status.upper()}", file=sys.stderr)

        generated += 1
        results.append({
            "label": label,
            "proof_label": proof_label,
            "dfy_path": out_path,
            "status": status,
            "contract": contract_result,
        })
        log_usage(asn_label, proof_label, elapsed, status == "verified", cost)

    # Summary
    if not args.dry_run:
        skip_msg = f", {skipped} skipped" if skipped else ""
        print(f"\n  Done: {generated} generated{skip_msg}, {failed} failed",
              file=sys.stderr)
        if generated > 0:
            print(f"  Verified: {verified_ok}/{generated}", file=sys.stderr)
            if clean_count or flag_count:
                print(f"  Contract: {clean_count} CLEAN, {flag_count} FLAG",
                      file=sys.stderr)
            print(f"  Cost: ${total_cost:.2f}", file=sys.stderr)

    # Write status file and commit
    if not args.dry_run and results:
        write_status_file(gen_dir, results, source="generate")
        print(f"  Status: {gen_dir.name}/STATUS.md", file=sys.stderr)
        if flag_count > 0:
            print(f"  Flags: {review_path.relative_to(WORKSPACE)}",
                  file=sys.stderr)
        run_commit(f"{asn_label} dafny modeling-{gen_num}")

    # Export verified files to vault/4-proofs-staging/
    if args.export and verified_files:
        import shutil
        proofs_dir = WORKSPACE / "vault" / "5-proofs" / asn_label
        proofs_dir.mkdir(parents=True, exist_ok=True)
        exported = 0
        for lbl, dfy_name in verified_files.items():
            src = gen_dir / dfy_name
            if src.exists():
                shutil.copy2(str(src), str(proofs_dir / dfy_name))
                exported += 1
        print(f"\n  [EXPORT] {exported} files → {proofs_dir.relative_to(WORKSPACE)}",
              file=sys.stderr)


if __name__ == "__main__":
    main()
