#!/usr/bin/env python3
"""
Alloy — generate Alloy models per ASN property with bounded checking.

Per-property: parses the extract into individual properties, generates one .als
per property using an agentic Claude session (with Bash access to run Alloy
and self-fix syntax errors), produces a review if failures remain, then runs
contract validation with align cycle.

Requires: formal statements in vault/project-model/ASN-NNNN/ (run normalize.py first)
Requires: Alloy installed at /Applications/Alloy.app (macOS) or ALLOY_JAR set.

Usage:
    python scripts/alloy.py 1                    # full pipeline
    python scripts/alloy.py 1 --property T1      # single property
    python scripts/alloy.py 1 --skip-check       # generate only
    python scripts/alloy.py 1 --dry-run           # show property list
    python scripts/alloy.py 1 --max-turns 16      # more agentic turns
"""

import argparse
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import WORKSPACE, FORMALIZATION_DIR, ALLOY_DIR
from lib.shared.common import find_asn
from lib.modeling.alloy.translate import (
    build_property_prompt, generate_one,
    PROMPTS_DIR, SYNTAX_REF,
)
from lib.modeling.alloy.align import align_validate_cycle
from lib.modeling.alloy.common import (
    read_file, log_usage, step_commit, cleanup_property_artifacts,
    make_result, print_summary, next_run_number,
)


def main():
    parser = argparse.ArgumentParser(
        description="Generate Alloy models from ASN and run bounded checking")
    parser.add_argument("asn",
                        help="ASN number (e.g., 4, 0004, ASN-0004) or path")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"],
                        help="Model (default: opus)")
    parser.add_argument("--effort", default=None,
                        help="Thinking effort level")
    parser.add_argument("--with-reference", action="store_true",
                        help="Include reference model in prompt for syntax grounding")
    parser.add_argument("--skip-check", action="store_true",
                        help="Generate model only, don't run Alloy")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show property list and prompt sizes")
    parser.add_argument("--property", "-p", default=None,
                        help="Check specific properties by label, comma-separated (e.g., T1,T3,TA0)")
    parser.add_argument("--recheck", action="store_true",
                        help="Reuse existing .als files, skip generation")
    parser.add_argument("--contract-only", action="store_true",
                        help="Run contract validation on existing .als files, no generation")
    parser.add_argument("--max-turns", type=int, default=12,
                        help="Max agentic turns for generation (default: 12)")
    parser.add_argument("--run", type=int, default=None,
                        help="Use specific run number (for incremental runs)")
    parser.add_argument("--no-cleanup", action="store_true",
                        help="Keep Alloy build artifacts (removed by default)")
    args = parser.parse_args()

    # Find ASN
    asn_path, asn_label = find_asn(args.asn)
    if asn_path is None:
        print(f"  No ASN found for {args.asn} in vault/1-reasoning-docs/",
              file=sys.stderr)
        sys.exit(1)

    # Load from per-property files
    asn_num = int(re.search(r'\d+', asn_label).group())
    prop_dir = FORMALIZATION_DIR / asn_label
    if not prop_dir.exists():
        print(f"  No formalization directory for {asn_label}", file=sys.stderr)
        print(f"  Run: python scripts/promote-blueprint.py {args.asn}",
              file=sys.stderr)
        sys.exit(1)

    # Load syntax reference for prompt injection
    syntax_ref = read_file(SYNTAX_REF)
    if not syntax_ref:
        print("  Warning: no syntax reference at "
              "scripts/prompts/modeling/alloy/syntax-reference.md",
              file=sys.stderr)

    # Read per-property files — separate definitions from properties
    definitions = []
    properties = []
    for f in sorted(prop_dir.glob("*.md")):
        if f.name.startswith("_"):
            continue
        content = f.read_text()
        label = f.name.replace(".md", "")
        if re.search(r'^\*\*Definition\s', content, re.MULTILINE):
            definitions.append(content)
        else:
            m = re.search(r'^\*\*\S+\s*\(([^)]+)\)', content, re.MULTILINE)
            name = m.group(1) if m else label
            properties.append({
                "label": label,
                "name": name,
                "type": "",
                "construct": "",
                "body": content,
            })
    definitions_text = "\n\n---\n\n".join(definitions)

    if not properties:
        print(f"  No properties found in {prop_dir.relative_to(WORKSPACE)}",
              file=sys.stderr)
        sys.exit(1)

    # Build dependency context per property (generate_deps called once)
    from lib.formalization.core.build_dependency_graph import generate_deps
    deps_data = generate_deps(asn_num)
    dep_contexts = {}
    for prop in properties:
        label = prop["label"]
        if deps_data:
            follows = deps_data.get("properties", {}).get(label, {}).get("follows_from", [])
            parts = []
            for dep in follows:
                dep_file = prop_dir / (dep.replace("(", "").replace(")", "") + ".md")
                if dep_file.exists():
                    parts.append(dep_file.read_text().strip())
            dep_contexts[label] = "\n\n---\n\n".join(parts)
        else:
            dep_contexts[label] = ""

    # Filter to specific properties if requested
    if args.property:
        targets = [t.strip() for t in args.property.split(",")]
        matches = []
        for target in targets:
            found = [p for p in properties if p["label"] == target]
            if not found:
                found = [p for p in properties
                         if p["label"].lower().startswith(target.lower())]
            if not found:
                print(f"  No property matching '{target}'", file=sys.stderr)
                print(f"  Available: {', '.join(p['label'] for p in properties)}",
                      file=sys.stderr)
                sys.exit(1)
            matches.extend(found)
        properties = matches

    # Contract-only mode: validate existing .als files
    if args.contract_only:
        from lib.modeling.alloy.validate import validate
        existing = sorted(
            (ALLOY_DIR / asn_label).glob("modeling-*"),
            key=lambda p: int(re.search(r"modeling-(\d+)", p.name).group(1))
                if re.search(r"modeling-(\d+)", p.name) else 0
        )
        if not existing:
            print(f"  No modeling directory found for {asn_label}",
                  file=sys.stderr)
            sys.exit(1)
        out_dir = existing[-1]
        print(f"  [CONTRACT] {asn_label} ({out_dir.name})", file=sys.stderr)
        for als_file in sorted(out_dir.glob("*.als")):
            prop_file = prop_dir / (als_file.stem + ".md")
            if not prop_file.exists():
                continue
            section = prop_file.read_text()
            alloy_source = read_file(als_file)
            rec, reason, elapsed = validate(alloy_source, section, als_file.stem)
            print(f"  {als_file.stem}: {rec.upper()} ({elapsed:.0f}s)",
                  file=sys.stderr)
        return

    if args.run is not None:
        run_num = args.run
        out_dir = ALLOY_DIR / asn_label / f"modeling-{run_num}"
        out_dir.mkdir(parents=True, exist_ok=True)
        print(f"  [RUN] Using modeling-{run_num}", file=sys.stderr)
    elif args.recheck:
        # Find the latest modeling directory
        existing = sorted(
            (ALLOY_DIR / asn_label).glob("modeling-*"),
            key=lambda p: int(re.search(r"modeling-(\d+)", p.name).group(1))
                if re.search(r"modeling-(\d+)", p.name) else 0
        )
        if not existing:
            print("  No existing modeling directory to recheck", file=sys.stderr)
            sys.exit(1)
        out_dir = existing[-1]
        m = re.search(r"modeling-(\d+)", out_dir.name)
        run_num = int(m.group(1)) if m else 1
        print(f"  [RECHECK] Using {out_dir.name}", file=sys.stderr)
    else:
        run_num = next_run_number(asn_label)
        out_dir = ALLOY_DIR / asn_label / f"modeling-{run_num}"
        out_dir.mkdir(parents=True, exist_ok=True)

    print(f"  {asn_label} — {len(properties)} properties, "
          f"definitions {len(definitions)}B", file=sys.stderr)

    # Initialize CONTRACT-REVIEW.md
    review_path = out_dir / "CONTRACT-REVIEW.md"
    with open(review_path, "w") as rf:
        rf.write(f"# Contract Review \u2014 {asn_label} (modeling-{run_num})\n\n")
        rf.write(f"*Reviewed: {time.strftime('%Y-%m-%d %H:%M')}*\n\n")
    clean_count = 0
    flag_count = 0

    # Generate + self-check all .als files (agent writes, runs Alloy, fixes)
    results = []
    for prop in properties:
        result = make_result(prop, out_dir)
        generate_one(result, prop, definitions_text, asn_label, args,
                      syntax_ref=syntax_ref,
                      dep_context=dep_contexts.get(prop["label"], ""))
        if not args.no_cleanup:
            cleanup_property_artifacts(result["als_path"])

        # Validate contract — align cycle if FLAG
        if not args.dry_run and result["als_path"].exists():
            section = prop["body"]
            if section:
                print(f"    [CONTRACT]", file=sys.stderr, end="", flush=True)
                contract_result, reason, a_cost = align_validate_cycle(
                    result["als_path"], section, prop["label"],
                    syntax_ref=syntax_ref, model=args.model)
                result["contract"] = contract_result

                if contract_result == "FLAG":
                    flag_count += 1
                    with open(review_path, "a") as rf:
                        rf.write(f"## {prop['label']} \u2014 {prop['name']}\n\n"
                                 f"{reason}\n\n")
                elif contract_result == "CLEAN":
                    clean_count += 1

        results.append(result)

    # Summary
    any_counterexample = any(r["status"] == "counterexample"
                             for r in results)

    if len(results) > 1 or args.dry_run:
        print_summary(asn_label, results)

    if not args.dry_run and (clean_count or flag_count):
        print(f"  Contract: {clean_count} CLEAN, {flag_count} FLAG",
              file=sys.stderr)
        if flag_count > 0:
            print(f"  Flags: {review_path.relative_to(WORKSPACE)}",
                  file=sys.stderr)

    # Commit results
    if not args.skip_check and not args.dry_run:
        if any_counterexample:
            step_commit(f"alloy(asn): {asn_label} — counterexamples found")
        else:
            step_commit(f"alloy(asn): {asn_label} — all properties pass bounded check")

    # Output: list of generated .als paths (for scripting)
    for r in results:
        if r["als_path"].exists():
            print(str(r["als_path"]))

    if any_counterexample:
        sys.exit(2)


if __name__ == "__main__":
    main()
