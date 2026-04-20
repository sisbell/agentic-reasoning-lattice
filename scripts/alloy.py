#!/usr/bin/env python3
"""
Alloy — generate Alloy models per ASN claim with bounded checking.

Reads per-claim files from lattices/xanadu/formalization/, generates one .als
per claim using an agentic Claude session (with Bash access to run Alloy
and self-fix syntax errors), validates contracts, writes per-claim reviews.

Parallel: 3 workers by default (each is an agent session + JVM).
Hash cache: skips unchanged claims since last successful run.

Requires: Alloy installed at /Applications/Alloy.app (macOS) or ALLOY_JAR set.

Usage:
    python scripts/alloy.py 34                    # full pipeline
    python scripts/alloy.py 34 --claim T1      # single claim
    python scripts/alloy.py 34 --workers 5        # more parallelism
    python scripts/alloy.py 34 --force             # ignore cache
    python scripts/alloy.py 34 --dry-run           # show claim list
    python scripts/alloy.py 34 --skip-check        # generate only
"""

import argparse
import hashlib
import json
import re
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import WORKSPACE, FORMALIZATION_DIR, ALLOY_DIR
from lib.shared.common import find_asn, parallel_llm_calls, build_label_index
from lib.verification.alloy.translate import (
    build_claim_prompt, generate_one,
    PROMPTS_DIR, SYNTAX_REF,
)
from lib.verification.alloy.align import align_validate_cycle
from lib.verification.alloy.common import (
    read_file, invoke_claude, log_usage, step_commit,
    cleanup_claim_artifacts, make_result, print_summary,
)

REVIEW_PROMPT = PROMPTS_DIR / "review-counterexample.md"


def _review_counterexample(claim_text, als_path, checker_output):
    """Classify a counterexample as spec issue vs modeling artifact."""
    template = read_file(REVIEW_PROMPT)
    if not template:
        return checker_output
    als_source = read_file(als_path)
    prompt = (template
              .replace("{{claim_text}}", claim_text)
              .replace("{{alloy_source}}", als_source)
              .replace("{{checker_output}}", checker_output))
    import os, subprocess
    cmd = ["claude", "--print", "--model", "claude-opus-4-7"]
    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = "high"
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        return checker_output
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
                        help="Show claim list and prompt sizes")
    parser.add_argument("--claim", "-p", default=None,
                        help="Specific claims, comma-separated")
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

    # Load from per-claim files
    asn_num = int(re.search(r'\d+', asn_label).group())
    claim_dir = FORMALIZATION_DIR / asn_label
    if not claim_dir.exists():
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

    # Read per-claim files
    _label_index = build_label_index(claim_dir)
    _filename_to_label = {f"{stem}.md": lbl for lbl, stem in _label_index.items()}
    definitions = []
    claims = []
    source_hashes = {}
    for f in sorted(claim_dir.glob("*.md")):
        if f.name.startswith("_"):
            continue
        content = f.read_text()
        label = _filename_to_label.get(f.name, f.stem)
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
            claims.append({
                "label": label,
                "name": name,
                "type": "",
                "construct": "",
                "body": content,
            })
    definitions_text = "\n\n---\n\n".join(definitions)

    if not claims:
        print(f"  No claims found", file=sys.stderr)
        sys.exit(1)

    # Filter to specific claims
    if args.claim:
        targets = [t.strip() for t in args.claim.split(",")]
        matches = []
        for target in targets:
            found = [p for p in claims if p["label"] == target]
            if not found:
                found = [p for p in claims
                         if p["label"].lower().startswith(target.lower())]
            if not found:
                print(f"  No claim matching '{target}'", file=sys.stderr)
                sys.exit(1)
            matches.extend(found)
        claims = matches

    # Hash cache — skip unchanged
    cache_path = out_dir / "_alloy-cache.json"
    cache = {} if args.force else _load_cache(cache_path)

    candidates = []
    cached = 0
    for prop in claims:
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
        print(f"  [CACHE] {cached} claims unchanged — skipping",
              file=sys.stderr)

    print(f"  {asn_label} — {len(candidates)} to process "
          f"({len(claims)} total, {len(definitions)} definitions)",
          file=sys.stderr)

    if args.dry_run:
        for prop in candidates:
            prompt = build_claim_prompt(
                definitions_text, prop, syntax_ref=syntax_ref,
                )
            print(f"\n  [{prop['label']}] {prop['name']}  "
                  f"({len(prompt) // 1024}KB prompt)", file=sys.stderr)
        return

    if not candidates:
        print(f"  Nothing to do.", file=sys.stderr)
        return

    # Process claims in parallel — flush cache + reviews per claim
    cache_lock = threading.Lock()
    all_results = []
    results_lock = threading.Lock()

    def _process_property(prop):
        label = prop["label"]
        result = make_result(prop, out_dir)
        generate_one(result, prop, definitions_text, asn_label, args,
                      syntax_ref=syntax_ref,
)

        # Validate contract (may re-invoke Alloy via align cycles)
        if not args.skip_check and result["als_path"].exists():
            section = prop["body"]
            if section:
                contract_result, reason, a_cost = align_validate_cycle(
                    result["als_path"], section, label,
                    syntax_ref=syntax_ref, model=args.model)
                result["contract"] = contract_result
                result["review_reason"] = reason if contract_result == "FLAG" else ""

        # Cleanup after align (align may re-invoke Alloy, creating new artifacts)
        if not args.no_cleanup:
            cleanup_claim_artifacts(result["als_path"])

        # Flush review file (each claim writes its own file — no contention)
        status = result.get("status", "")
        contract = result.get("contract", "")
        review_path = review_dir / f"{label}.md"
        if status == "counterexample":
            analysis = _review_counterexample(
                prop["body"], result["als_path"],
                result.get("alloy_output", ""))
            result["review_analysis"] = analysis
            with open(review_path, "w") as rf:
                rf.write(f"# {label} — Counterexample\n\n")
                rf.write(f"*{time.strftime('%Y-%m-%d %H:%M')}*\n\n")
                rf.write(analysis + "\n")
        elif contract == "FLAG":
            with open(review_path, "w") as rf:
                rf.write(f"# {label} — Contract FLAG\n\n")
                rf.write(f"*{time.strftime('%Y-%m-%d %H:%M')}*\n\n")
                rf.write(result.get("review_reason", "") + "\n")
        else:
            if review_path.exists():
                review_path.unlink()

        # Flush cache (shared file — needs lock)
        with cache_lock:
            cache[label] = {
                "hash": source_hashes.get(label, ""),
                "status": status,
                "contract": contract,
            }
            _save_cache(cache_path, cache)

        with results_lock:
            all_results.append(result)

        return label, result

    parallel_llm_calls(
        candidates, _process_property, max_workers=args.workers)

    # Counters for summary
    flag_count = sum(1 for r in all_results
                     if r.get("status") == "counterexample"
                     or r.get("contract") == "FLAG")
    clean_count = sum(1 for r in all_results
                      if r.get("status") != "counterexample"
                      and r.get("contract") != "FLAG")

    # Summary
    if all_results:
        print_summary(asn_label, all_results)

    if clean_count or flag_count:
        print(f"  Contract: {clean_count} CLEAN, {flag_count} FLAG",
              file=sys.stderr)
        if flag_count > 0:
            print(f"  Reviews: {review_dir.relative_to(WORKSPACE)}/",
                  file=sys.stderr)

    # Commit — git add first so commit.py sees the new files
    if not args.skip_check and not args.dry_run and all_results:
        import subprocess
        subprocess.run(
            ["git", "add", str(out_dir)],
            capture_output=True, text=True, cwd=str(WORKSPACE))
        any_counterexample = any(r.get("status") == "counterexample"
                                  for r in all_results)
        if any_counterexample:
            step_commit(f"alloy(asn): {asn_label} — counterexamples found")
        else:
            step_commit(f"alloy(asn): {asn_label} — {len(all_results)} claims checked")

    # Output paths for scripting
    for r in all_results:
        if r["als_path"].exists():
            print(str(r["als_path"]))

    if any(r.get("status") == "counterexample" for r in all_results):
        sys.exit(2)


if __name__ == "__main__":
    main()
