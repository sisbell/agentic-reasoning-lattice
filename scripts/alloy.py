#!/usr/bin/env python3
"""
Alloy — generate Alloy models per ASN property with bounded checking.

Reads per-property files from vault/3-formalization/, generates one .als
per property using an agentic Claude session (with Bash access to run Alloy
and self-fix syntax errors), validates contracts, writes per-property reviews.

Parallel: 3 workers by default (each is an agent session + JVM).
Hash cache: skips unchanged properties since last successful run.

Requires: Alloy installed at /Applications/Alloy.app (macOS) or ALLOY_JAR set.

Usage:
    python scripts/alloy.py 34                    # full pipeline
    python scripts/alloy.py 34 --property T1      # single property
    python scripts/alloy.py 34 --workers 5        # more parallelism
    python scripts/alloy.py 34 --force             # ignore cache
    python scripts/alloy.py 34 --dry-run           # show property list
    python scripts/alloy.py 34 --skip-check        # generate only
"""

import argparse
import hashlib
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import WORKSPACE, FORMALIZATION_DIR, ALLOY_DIR
from lib.shared.common import find_asn, parallel_llm_calls
from lib.modeling.alloy.translate import (
    build_property_prompt, generate_one,
    PROMPTS_DIR, SYNTAX_REF,
)
from lib.modeling.alloy.align import align_validate_cycle
from lib.modeling.alloy.common import (
    read_file, log_usage, step_commit, cleanup_property_artifacts,
    make_result, print_summary,
)


def _hash_content(text):
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def _load_cache(path):
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, ValueError):
        return {}


def _save_cache(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Generate Alloy models from ASN and run bounded checking")
    parser.add_argument("asn",
                        help="ASN number (e.g., 34)")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"],
                        help="Model (default: opus)")
    parser.add_argument("--effort", default=None,
                        help="Thinking effort level")
    parser.add_argument("--with-reference", action="store_true",
                        help="Include reference model in prompt")
    parser.add_argument("--skip-check", action="store_true",
                        help="Generate model only, don't run Alloy")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show property list and prompt sizes")
    parser.add_argument("--property", "-p", default=None,
                        help="Specific properties, comma-separated")
    parser.add_argument("--max-turns", type=int, default=12,
                        help="Max agentic turns (default: 12)")
    parser.add_argument("--workers", type=int, default=3,
                        help="Parallel workers (default: 3)")
    parser.add_argument("--force", action="store_true",
                        help="Ignore cache, regenerate all")
    parser.add_argument("--no-cleanup", action="store_true",
                        help="Keep Alloy build artifacts")
    args = parser.parse_args()

    # Find ASN
    asn_path, asn_label = find_asn(args.asn)
    if asn_path is None:
        print(f"  No ASN found for {args.asn}", file=sys.stderr)
        sys.exit(1)

    # Load from per-property files
    asn_num = int(re.search(r'\d+', asn_label).group())
    prop_dir = FORMALIZATION_DIR / asn_label
    if not prop_dir.exists():
        print(f"  No formalization directory for {asn_label}", file=sys.stderr)
        print(f"  Run: python scripts/promote-blueprint.py {args.asn}",
              file=sys.stderr)
        sys.exit(1)

    # Output directory (flat, no modeling-N versioning)
    out_dir = ALLOY_DIR / asn_label
    out_dir.mkdir(parents=True, exist_ok=True)
    review_dir = out_dir / "reviews"
    review_dir.mkdir(parents=True, exist_ok=True)

    # Load syntax reference
    syntax_ref = read_file(SYNTAX_REF)
    if not syntax_ref:
        print("  Warning: no syntax reference", file=sys.stderr)

    # Read per-property files
    definitions = []
    properties = []
    source_hashes = {}
    for f in sorted(prop_dir.glob("*.md")):
        if f.name.startswith("_"):
            continue
        content = f.read_text()
        label = f.name.replace(".md", "")
        source_hashes[label] = _hash_content(content)
        if re.search(r'^\*\*Definition\s', content, re.MULTILINE):
            # Header + formal contract only (skip derivation prose)
            header = content.split("\n", 1)[0]
            m = re.search(r'(\*Formal Contract:\*.*)', content, re.DOTALL)
            contract = m.group(1).strip() if m else ""
            definitions.append(f"{header}\n\n{contract}" if contract else header)
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
        print(f"  No properties found", file=sys.stderr)
        sys.exit(1)

    # Filter to specific properties
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
                sys.exit(1)
            matches.extend(found)
        properties = matches

    # Hash cache — skip unchanged
    cache_path = out_dir / "_alloy-cache.json"
    cache = {} if args.force else _load_cache(cache_path)

    candidates = []
    cached = 0
    for prop in properties:
        label = prop["label"]
        als_path = out_dir / f"{label}.als"
        entry = cache.get(label, {})
        if (not args.force
                and entry.get("hash") == source_hashes.get(label)
                and als_path.exists()):
            cached += 1
        else:
            candidates.append(prop)

    if cached:
        print(f"  [CACHE] {cached} properties unchanged — skipping",
              file=sys.stderr)

    print(f"  {asn_label} — {len(candidates)} to process "
          f"({len(properties)} total, {len(definitions)} definitions)",
          file=sys.stderr)

    if args.dry_run:
        for prop in candidates:
            prompt = build_property_prompt(
                definitions_text, prop, syntax_ref=syntax_ref,
                )
            print(f"\n  [{prop['label']}] {prop['name']}  "
                  f"({len(prompt) // 1024}KB prompt)", file=sys.stderr)
        return

    if not candidates:
        print(f"  Nothing to do.", file=sys.stderr)
        return

    # Process properties in parallel
    def _process_property(prop):
        label = prop["label"]
        result = make_result(prop, out_dir)
        generate_one(result, prop, definitions_text, asn_label, args,
                      syntax_ref=syntax_ref,
)
        if not args.no_cleanup:
            cleanup_property_artifacts(result["als_path"])

        # Validate contract
        if not args.skip_check and result["als_path"].exists():
            section = prop["body"]
            if section:
                contract_result, reason, a_cost = align_validate_cycle(
                    result["als_path"], section, label,
                    syntax_ref=syntax_ref, model=args.model)
                result["contract"] = contract_result
                result["review_reason"] = reason if contract_result == "FLAG" else ""

        return label, result

    results_list = parallel_llm_calls(
        candidates, _process_property, max_workers=args.workers)

    # Collect results, write per-property reviews, update cache
    all_results = []
    flag_count = 0
    clean_count = 0

    for label, result in results_list:
        if result is None:
            continue
        all_results.append(result)

        # Update cache
        status = result.get("status", "")
        contract = result.get("contract", "")
        cache[label] = {
            "hash": source_hashes.get(label, ""),
            "status": status,
            "contract": contract,
        }

        # Write per-property review for findings
        review_path = review_dir / f"{label}.md"
        if status == "counterexample":
            flag_count += 1
            with open(review_path, "w") as rf:
                rf.write(f"# {label} — Counterexample\n\n")
                rf.write(f"*{time.strftime('%Y-%m-%d %H:%M')}*\n\n")
                rf.write(result.get("alloy_output", "") + "\n")
        elif contract == "FLAG":
            flag_count += 1
            with open(review_path, "w") as rf:
                rf.write(f"# {label} — Contract FLAG\n\n")
                rf.write(f"*{time.strftime('%Y-%m-%d %H:%M')}*\n\n")
                rf.write(result.get("review_reason", "") + "\n")
        else:
            clean_count += 1
            # Delete stale review if property now passes
            if review_path.exists():
                review_path.unlink()

    _save_cache(cache_path, cache)

    # Summary
    if all_results:
        print_summary(asn_label, all_results)

    if clean_count or flag_count:
        print(f"  Contract: {clean_count} CLEAN, {flag_count} FLAG",
              file=sys.stderr)
        if flag_count > 0:
            print(f"  Reviews: {review_dir.relative_to(WORKSPACE)}/",
                  file=sys.stderr)

    # Commit
    if not args.skip_check and not args.dry_run:
        any_counterexample = any(r.get("status") == "counterexample"
                                  for r in all_results)
        if any_counterexample:
            step_commit(f"alloy(asn): {asn_label} — counterexamples found")
        elif all_results:
            step_commit(f"alloy(asn): {asn_label} — {len(all_results)} properties checked")

    # Output paths for scripting
    for r in all_results:
        if r["als_path"].exists():
            print(str(r["als_path"]))

    if any(r.get("status") == "counterexample" for r in all_results):
        sys.exit(2)


if __name__ == "__main__":
    main()
