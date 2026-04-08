#!/usr/bin/env python3
"""
Dafny — generate Dafny declarations per ASN property.

Reads per-property files from vault/3-formalization/, generates one .dfy
per property using an agentic Claude session (with Read/Write/Bash tools
to write, verify, and self-fix), validates contracts, writes per-property reviews.

Parallel: level-based (topological order). Properties at the same dependency
level run concurrently (default 3 workers). Between levels, waits for all
verified files before proceeding (next level may include earlier .dfy files).

Hash cache: skips unchanged properties since last successful run.

Usage:
    python scripts/dafny.py 34                    # full pipeline
    python scripts/dafny.py 34 --property T1      # single property
    python scripts/dafny.py 34 --workers 5        # more parallelism
    python scripts/dafny.py 34 --force            # ignore cache
    python scripts/dafny.py 34 --dry-run          # show property list
"""

import argparse
import hashlib
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import (WORKSPACE, FORMALIZATION_DIR, DAFNY_DIR, USAGE_LOG,
                    load_manifest)
from lib.shared.common import find_asn, parallel_llm_calls
from lib.formalization.core.build_dependency_graph import generate_deps
from lib.formalization.core.topological_sort import topological_sort_labels, topological_levels
from lib.modeling.dafny.translate import (
    build_property_list_from_asn, read_proof_modules,
    build_property_prompt, translate_one, TEMPLATE,
)
from lib.modeling.dafny.verify import verify
from lib.modeling.dafny.align import align_validate_cycle
from lib.modeling.dafny.common import read_file, run_commit, log_usage

REVIEW_PROMPT = WORKSPACE / "scripts" / "prompts" / "modeling" / "dafny" / "review-failure.md"


def _review_failure(prop_text, dfy_path, verification_errors):
    """Classify a verification failure as spec issue vs proof artifact."""
    template = read_file(REVIEW_PROMPT)
    if not template:
        return verification_errors
    dfy_source = read_file(dfy_path)
    prompt = (template
              .replace("{{property_text}}", prop_text)
              .replace("{{dafny_source}}", dfy_source)
              .replace("{{verification_errors}}", verification_errors))
    import os, subprocess
    cmd = ["claude", "--print", "--model", "claude-opus-4-6"]
    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = "high"
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        return verification_errors
    return result.stdout.strip()


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
        description="Generate Dafny declarations per ASN property")
    parser.add_argument("asn",
                        help="ASN number (e.g., 1, 0001, ASN-0001)")
    parser.add_argument("--property", "-p",
                        help="Generate specific properties, comma-separated")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"],
                        help="Model (default: opus)")
    parser.add_argument("--effort", default="max",
                        help="Thinking effort level (low/medium/high/max)")
    parser.add_argument("--max-turns", type=int, default=24,
                        help="Max agent turns per property (default: 24)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be generated without invoking Claude")
    parser.add_argument("--workers", type=int, default=3,
                        help="Parallel workers per level (default: 3)")
    parser.add_argument("--force", action="store_true",
                        help="Ignore cache, regenerate all")
    args = parser.parse_args()

    # --- Locate inputs ---

    asn_number = int(re.sub(r"[^0-9]", "", str(args.asn)))
    asn_label = f"ASN-{asn_number:04d}"
    prop_dir = FORMALIZATION_DIR / asn_label
    if not prop_dir.exists():
        print(f"  No formalization directory for {asn_label}",
              file=sys.stderr)
        print(f"  Run: python scripts/promote-blueprint.py {args.asn}",
              file=sys.stderr)
        sys.exit(1)

    template_text = read_file(TEMPLATE)
    if not template_text:
        print("  Prompt template not found: scripts/prompts/modeling/dafny/translate-property.md",
              file=sys.stderr)
        sys.exit(1)

    # --- Parse inputs ---

    index_rows = build_property_list_from_asn(asn_number)
    print(f"  [SOURCE] per-property files from {prop_dir.relative_to(WORKSPACE)}",
          file=sys.stderr)

    if not index_rows:
        print(f"  No properties found", file=sys.stderr)
        sys.exit(1)

    # Proof module dependencies from project model manifest
    manifest = load_manifest(asn_number)
    module_names = manifest.get("modeling", {}).get("proof_imports", [])
    all_modules = list(module_names)

    imports_text = (f"| ASN | Proof modules |\n|-----|---------------|\n"
                    f"| {asn_label} | {', '.join(all_modules)} |")

    proof_modules, proof_modules_text = read_proof_modules(all_modules)

    # Filter to specific properties if requested
    if args.property:
        targets = [t.strip() for t in args.property.split(",")]
        matches = []
        for target in targets:
            found = [r for r in index_rows
                     if r["label"] == target or r["proof_label"] == target]
            if not found:
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

    # --- Output directory (flat, no modeling-N) ---

    out_dir = DAFNY_DIR / asn_label
    out_dir.mkdir(parents=True, exist_ok=True)
    review_dir = out_dir / "reviews"
    review_dir.mkdir(parents=True, exist_ok=True)

    # --- Read per-property source files + hashes ---

    source_hashes = {}
    prop_contents = {}
    for f in sorted(prop_dir.glob("*.md")):
        if not f.name.startswith("_"):
            label = f.name.replace(".md", "")
            content = f.read_text()
            source_hashes[label] = _hash_content(content)
            prop_contents[label] = content

    # --- Dependency graph ---

    deps_data = generate_deps(asn_number)

    # --- Hash cache — skip unchanged ---

    cache_path = out_dir / "_dafny-cache.json"
    cache = {} if args.force else _load_cache(cache_path)

    candidates = []
    cached = 0
    for row in index_rows:
        label = row["label"]
        dfy_path = out_dir / f"{row['proof_label']}.dfy"
        entry = cache.get(label, {})
        if (not args.force
                and entry.get("hash") == source_hashes.get(label)
                and entry.get("status") == "verified"
                and dfy_path.exists()):
            cached += 1
        else:
            candidates.append(row)

    if cached:
        print(f"  [CACHE] {cached} properties unchanged — skipping",
              file=sys.stderr)

    print(f"  [DAFNY] {asn_label} — {len(candidates)} to process "
          f"({len(index_rows)} total)",
          file=sys.stderr)
    print(f"  Imports: {', '.join(all_modules)}", file=sys.stderr)

    if args.dry_run:
        for row in candidates:
            prompt = build_property_prompt(
                template_text, imports_text, proof_modules_text,
                row, "")
            print(f"  [{row['label']}] {row['proof_label']}  "
                  f"({len(prompt) // 1024}KB prompt)", file=sys.stderr)
        return

    if not candidates:
        print(f"  Nothing to do.", file=sys.stderr)
        return

    # --- Build topological levels ---

    if deps_data:
        levels = topological_levels(deps_data)
    else:
        levels = [[r["label"] for r in candidates]]

    # Track verified files across levels (label -> proof_label)
    verified_files = {}

    # Pre-populate from cache (for dep context of first levels)
    for row in index_rows:
        label = row["label"]
        entry = cache.get(label, {})
        if entry.get("status") == "verified":
            dfy_path = out_dir / f"{row['proof_label']}.dfy"
            if dfy_path.exists():
                verified_files[label] = row["proof_label"]

    all_results = []
    total_cost = 0

    for level_idx, level_labels in enumerate(levels):
        level_set = set(level_labels)
        level_candidates = [r for r in candidates if r["label"] in level_set]

        if not level_candidates:
            continue

        print(f"\n  [LEVEL {level_idx}] {len(level_candidates)} properties",
              file=sys.stderr)

        # Snapshot verified_files for this level (read-only in workers)
        level_verified = dict(verified_files)

        def _process_one(row):
            label = row["label"]
            proof_label = row["proof_label"]
            out_path = out_dir / f"{proof_label}.dfy"

            # Build dependency context from earlier levels
            dep_context = ""
            if deps_data and label in deps_data.get("properties", {}):
                follows = deps_data["properties"][label].get("follows_from", [])
                available = [(dep, level_verified[dep]) for dep in follows
                             if dep in level_verified]
                if available:
                    lines = ["## Available verified lemmas (from this build)\n"]
                    for dep_label, dep_proof in available:
                        lines.append(f"- {dep_label}: `include \"./{dep_proof}.dfy\"`")
                    dep_context = "\n".join(lines) + "\n"

            # Build prompt
            prompt = build_property_prompt(
                template_text, imports_text, proof_modules_text,
                row, "", dep_context=dep_context,
            )

            # Launch agent
            print(f"  [{label}] {proof_label}...",
                  file=sys.stderr, end="", flush=True)
            wrote, elapsed, cost = translate_one(
                prompt, out_path,
                model=args.model, effort=args.effort, max_turns=args.max_turns,
            )

            result = {
                "label": label,
                "proof_label": proof_label,
                "dfy_path": out_path,
                "status": "gen_fail",
                "contract": "",
                "review_reason": "",
                "cost": cost,
                "elapsed": elapsed,
            }

            if not wrote:
                print(f" no file written", file=sys.stderr)
                return label, result

            # Final verification
            status, vout = verify(out_path)
            result["status"] = status

            if status == "verified":
                m = re.search(r"(\d+) verified", vout)
                n = m.group(1) if m else "?"
                print(f" verified({n})", file=sys.stderr, end="", flush=True)

                # Validate contract
                section = prop_contents.get(label, "")
                if section:
                    contract_result, reason, a_cost = align_validate_cycle(
                        out_path, section, label,
                        model=args.model, effort=args.effort)
                    result["contract"] = contract_result
                    result["review_reason"] = reason if contract_result == "FLAG" else ""
                    result["cost"] += a_cost
                else:
                    print(f" (no contract)", file=sys.stderr)
            elif status in ("compile_failure", "proof_failure"):
                print(f" {status.upper().replace('_', ' ')}", file=sys.stderr)
                result["verification_errors"] = vout
            else:
                print(f" {status.upper()}", file=sys.stderr)

            log_usage(asn_label, proof_label, elapsed, status == "verified", cost)
            return label, result

        level_results = parallel_llm_calls(
            level_candidates, _process_one, max_workers=args.workers)

        # Collect results, update verified_files for next level
        for label, result in level_results:
            if result is None:
                continue
            all_results.append(result)
            total_cost += result.get("cost", 0)

            if result["status"] == "verified":
                verified_files[label] = result["proof_label"]

            # Update cache
            cache[label] = {
                "hash": source_hashes.get(label, ""),
                "status": result["status"],
                "contract": result.get("contract", ""),
            }

            # Write per-property review
            review_path = review_dir / f"{label}.md"
            if result["status"] in ("proof_failure", "compile_failure", "gen_fail"):
                errors = result.get("verification_errors", "")
                prop_text = prop_contents.get(label, "")
                dfy_path = result.get("dfy_path")
                if errors and prop_text and dfy_path and dfy_path.exists():
                    analysis = _review_failure(prop_text, dfy_path, errors)
                else:
                    analysis = errors or result["status"]
                with open(review_path, "w") as rf:
                    rf.write(f"# {label} — {result['status'].replace('_', ' ').title()}\n\n")
                    rf.write(f"*{time.strftime('%Y-%m-%d %H:%M')}*\n\n")
                    rf.write(analysis + "\n")
            elif result.get("contract") == "FLAG":
                with open(review_path, "w") as rf:
                    rf.write(f"# {label} — Contract FLAG\n\n")
                    rf.write(f"*{time.strftime('%Y-%m-%d %H:%M')}*\n\n")
                    rf.write(result.get("review_reason", "") + "\n")
            else:
                if review_path.exists():
                    review_path.unlink()

        # Flush cache after each level (resume picks up here if interrupted)
        _save_cache(cache_path, cache)

    # --- Summary ---

    if all_results:
        verified_count = sum(1 for r in all_results if r["status"] == "verified")
        failed_count = sum(1 for r in all_results if r["status"] != "verified")
        clean_count = sum(1 for r in all_results if r.get("contract") == "CLEAN")
        flag_count = sum(1 for r in all_results if r.get("contract") == "FLAG")

        print(f"\n  Done: {len(all_results)} generated, "
              f"{verified_count} verified, {failed_count} failed",
              file=sys.stderr)
        if clean_count or flag_count:
            print(f"  Contract: {clean_count} CLEAN, {flag_count} FLAG",
                  file=sys.stderr)
        print(f"  Cost: ${total_cost:.2f}", file=sys.stderr)

        if flag_count > 0:
            print(f"  Reviews: {review_dir.relative_to(WORKSPACE)}/",
                  file=sys.stderr)

        import subprocess
        subprocess.run(
            ["git", "add", str(out_dir)],
            capture_output=True, text=True, cwd=str(WORKSPACE))
        run_commit(f"{asn_label} dafny — {len(all_results)} properties")


if __name__ == "__main__":
    main()
