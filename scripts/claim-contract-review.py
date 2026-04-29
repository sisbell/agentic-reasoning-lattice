#!/usr/bin/env python3
"""
Contract Review — validate formal contracts against proofs.

Runs contract validation (sonnet, ~4s per claim) on all claims
with formal contracts. On MISMATCH, re-runs produce-contract (opus)
to rewrite the contract with full proof + deps context.

Usage:
    python scripts/claim-contract-review.py 34
    python scripts/claim-contract-review.py 34 --label T1
    python scripts/claim-contract-review.py 34 --dry-run
    python scripts/claim-contract-review.py 34 --max-cycles 1
"""

import argparse
import hashlib
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import (WORKSPACE, CLAIM_CONVERGENCE_DIR, CLAIM_DIR,
                                CLAIM_REVIEWS_DIR, prompt_path,
                                next_review_number)
from lib.shared.common import find_asn, invoke_claude, parallel_llm_calls, step_commit_asn, build_label_index, aggregate_signature
from lib.claim_convergence.assembly.validate_contracts import validate_contract
from lib.claim_derivation.produce_contract import _has_formal_contract

FIX_CONTRACT_TEMPLATE = prompt_path("claim-convergence/contract-review/fix-contract.md")


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


def run_contract_review(asn_num, max_cycles=5, dry_run=False,
                         single_label=None, validate_model="sonnet",
                         force=False):
    """Run contract review — validate and fix contracts.

    Returns "converged" or "not_converged".
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return "failed"

    print(f"\n  [CONTRACT-REVIEW] {asn_label}", file=sys.stderr)

    review_dir = CLAIM_REVIEWS_DIR / asn_label
    cc_dir = CLAIM_CONVERGENCE_DIR / asn_label
    claim_dir = CLAIM_DIR / asn_label
    if not claim_dir.exists():
        print(f"  No claim doc directory for {asn_label}", file=sys.stderr)
        return "failed"

    label_index = build_label_index(claim_dir)
    _filename_to_label = {f"{stem}.md": lbl for lbl, stem in label_index.items()}
    print(f"  Directory: {claim_dir.relative_to(WORKSPACE)}", file=sys.stderr)

    signature = aggregate_signature(claim_dir)

    cc_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cc_dir / "_contract-cache.json"
    validated_hashes = {} if force else _load_cache(cache_path)

    start_time = time.time()
    converged = False
    had_findings = False

    for cycle in range(1, max_cycles + 1):
        # Read per-claim files
        prop_files = sorted(
            f for f in claim_dir.glob("*.md")
            if not f.name.startswith("_")
        )

        if single_label:
            prop_files = [f for f in prop_files
                          if _filename_to_label.get(f.name, f.stem) == single_label]

        # Filter to claims with formal contracts, skip cached
        candidates = []
        cached = 0
        for f in prop_files:
            label = _filename_to_label.get(f.name, f.stem)
            content = f.read_text()
            if not content or not _has_formal_contract(content):
                continue
            current_hash = _hash_content(content)
            if validated_hashes.get(label) == current_hash:
                cached += 1
                continue
            candidates.append((label, content, f))

        if cached:
            print(f"  [CACHE] {cached} contracts unchanged — skipping",
                  file=sys.stderr)

        print(f"\n  [CYCLE {cycle}/{max_cycles}] {len(candidates)} claims to validate",
              file=sys.stderr)

        # Pre-build dependency contexts (generate_deps called once)
        from lib.claim_convergence.core.build_dependency_graph import generate_claim_convergence_deps
        deps_data = generate_claim_convergence_deps(asn_num)
        dep_contexts = {}
        for label, content, f in candidates:
            if deps_data:
                claim_data = deps_data.get("claims", {}).get(label, {})
                follows_from = claim_data.get("follows_from", [])
                parts = []
                for dep_label in follows_from:
                    dep_stem = label_index.get(dep_label, dep_label.replace("(", "").replace(")", ""))
                    dep_file = claim_dir / f"{dep_stem}.md"
                    if dep_file.exists():
                        parts.append(f"### {dep_label}\n\n{dep_file.read_text().strip()}")
                dep_contexts[label] = "\n\n".join(parts) if parts else "(none)"
            else:
                dep_contexts[label] = "(none)"

        # Validate all in parallel (read-only sonnet calls)
        def _validate_one(item):
            label, content, f = item
            match, detail = validate_contract(label, content,
                                              signature=signature,
                                              dependencies=dep_contexts.get(label, ""),
                                              model=validate_model)
            return label, (match, detail, f)

        results = parallel_llm_calls(candidates, _validate_one, max_workers=10)

        mismatches = []
        for label, result_tuple in results:
            if result_tuple is None:
                continue
            match, detail, f = result_tuple
            if match:
                # Cache this claim as validated
                content = f.read_text()
                validated_hashes[label] = _hash_content(content)
            else:
                print(f"    {label}: MISMATCH", file=sys.stderr)
                for line in detail.split('\n')[:3]:
                    if line.strip():
                        print(f"      {line.strip()}", file=sys.stderr)
                mismatches.append((label, detail, f))

        print(f"\n  {len(candidates)} checked, {len(mismatches)} mismatches",
              file=sys.stderr)

        # Save cache after validation
        _save_cache(cache_path, validated_hashes)

        if not mismatches:
            converged = True
            print(f"\n  Converged after {cycle} cycle{'s' if cycle > 1 else ''}.",
                  file=sys.stderr)
            if not had_findings:
                print(f"  Nothing to do.", file=sys.stderr)
            break

        had_findings = True

        if dry_run:
            print(f"\n  {len(mismatches)} mismatches reported.",
                  file=sys.stderr)
            break

        # Fix mismatches — surgical contract edit only
        print(f"\n  [FIX] {len(mismatches)} mismatches — fix-contract...",
              file=sys.stderr)

        template = FIX_CONTRACT_TEMPLATE.read_text()

        def _fix_one(item):
            label, detail, claim_path = item
            content = claim_path.read_text()

            prompt = (template
                      .replace("{{label}}", label)
                      .replace("{{section}}", content)
                      .replace("{{finding}}", detail)
                      .replace("{{signature}}", signature)
                      .replace("{{dependencies}}", dep_contexts.get(label, "(none)")))
            response, elapsed = invoke_claude(prompt, model="opus",
                                              effort="high")
            if not response or "<tool_call>" in response:
                return label, (False, False)
            new_content = response.strip()
            if len(new_content) < len(content) * 0.5:
                return label, (False, False)
            if new_content == content.strip():
                return label, (True, False)
            claim_path.write_text(new_content + "\n")
            return label, (True, True)

        fix_results = parallel_llm_calls(mismatches, _fix_one, max_workers=10)

        any_changed = False
        for label, result_tuple in fix_results:
            if result_tuple is None:
                continue
            ok, changed = result_tuple
            if changed:
                any_changed = True

        if any_changed:
            # Invalidate cache for fixed claims
            for label, _, _ in mismatches:
                validated_hashes.pop(label, None)
            _save_cache(cache_path, validated_hashes)
            step_commit_asn(asn_num, hint="contract-review fixes")

        # Write review
        review_dir.mkdir(parents=True, exist_ok=True)
        review_num = next_review_number(asn_label, kind="claim", reviews_dir=review_dir)
        review_path = review_dir / f"review-{review_num}.md"
        with open(review_path, "w") as rf:
            rf.write(f"# Contract Review — {asn_label} (cycle {cycle})\n\n")
            rf.write(f"*{time.strftime('%Y-%m-%d %H:%M')}*\n\n")
            for label, detail, _ in mismatches:
                rf.write(f"### {label}\n\n{detail}\n\n")
            rf.write(f"{len(mismatches)} mismatches.\n")

    elapsed = time.time() - start_time
    print(f"  Elapsed: {elapsed:.0f}s", file=sys.stderr)

    # Commit any remaining review files (e.g. clean convergence cycle)
    if had_findings:
        step_commit_asn(asn_num, hint="contract-review")

    return "converged" if converged else "not_converged"


def main():
    parser = argparse.ArgumentParser(
        description="Contract Review — validate and fix formal contracts")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument("--max-cycles", type=int, default=5,
                        help="Maximum convergence cycles (default: 5)")
    parser.add_argument("--label", help="Review a single claim only")
    parser.add_argument("--model", default="sonnet",
                        help="Model for validation (default: sonnet)")
    parser.add_argument("--force", action="store_true",
                        help="Ignore cache, re-validate all claims")
    parser.add_argument("--dry-run", action="store_true",
                        help="Report mismatches without fixing")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    result = run_contract_review(asn_num, max_cycles=args.max_cycles,
                                  dry_run=args.dry_run,
                                  single_label=args.label,
                                  validate_model=args.model,
                                  force=args.force)
    sys.exit(0 if result == "converged" else 1)


if __name__ == "__main__":
    main()
