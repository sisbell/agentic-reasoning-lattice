#!/usr/bin/env python3
"""
Proof Review — verify proofs with incremental convergence.

Reviews each property's proof against a 7-point checklist. On FOUND,
revises and re-verifies in the next cycle. Dirty set tracks changed
properties + their downstream dependents.

Usage:
    python scripts/proof-review.py 40
    python scripts/proof-review.py 40 --max-cycles 1     # single pass, no fixing
    python scripts/proof-review.py 40 --mode full_sweep   # check all each cycle
    python scripts/proof-review.py 40 --label B0a         # single property
    python scripts/proof-review.py 40 --dry-run           # verify only, no fixes
"""

import argparse
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hashlib
import json

from lib.shared.paths import WORKSPACE, FORMALIZATION_DIR, next_review_number
from lib.shared.common import find_asn, parallel_llm_calls, step_commit_asn
from lib.formalization.core.build_dependency_graph import generate_deps
from lib.formalization.core.topological_sort import topological_sort_labels
from lib.formalization.proof_review.verify import review_property
from lib.formalization.proof_review.revise import revise


def _hash_content(text):
    """Short content hash."""
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def _load_verified_hashes(cache_path):
    """Load {label: hash} of properties that passed verification."""
    if not cache_path.exists():
        return {}
    try:
        return json.loads(cache_path.read_text())
    except (json.JSONDecodeError, ValueError):
        return {}


def _save_verified_hashes(cache_path, hashes):
    """Save verified hashes."""
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(hashes, indent=2) + "\n")


def _downstream_dependents(changed_labels, deps_data):
    """Find properties that depend on any of the changed labels."""
    dependents = set()
    for label, prop_data in deps_data.get("properties", {}).items():
        follows = set(prop_data.get("follows_from", []))
        if follows & changed_labels:
            dependents.add(label)
    return dependents


def run_proof_review(asn_num, max_cycles=5, mode="incremental",
                     dry_run=False, single_label=None, force=False):
    """Run the proof review pipeline.

    Args:
        asn_num: ASN number
        max_cycles: Maximum convergence cycles
        mode: "incremental" (dirty set + dependents) or "full_sweep"
        dry_run: Verify only, don't fix
        single_label: If set, only review this one property

    Returns:
        "converged" or "not_converged"
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return "failed"

    print(f"\n  [PROOF REVIEW] {asn_label}", file=sys.stderr)

    review_dir = FORMALIZATION_DIR / asn_label / "reviews"
    prop_dir = FORMALIZATION_DIR / asn_label
    if not prop_dir.exists():
        print(f"  No formalization directory for {asn_label}", file=sys.stderr)
        return "failed"

    print(f"  Directory: {prop_dir.relative_to(WORKSPACE)}", file=sys.stderr)

    # Load verification cache — skip properties unchanged since last VERIFIED
    cache_path = prop_dir / "_verify-cache.json"
    verified_hashes = {} if force else _load_verified_hashes(cache_path)

    start_time = time.time()
    all_findings = {}   # label → finding_text (latest)
    all_verified = set()
    converged = False
    had_findings = False

    for cycle in range(1, max_cycles + 1):
        # Generate fresh deps
        deps_data = generate_deps(asn_num)
        if deps_data is None:
            print(f"  No dependency data — cannot review", file=sys.stderr)
            return "failed"

        # Read per-property files (normalized lookup handles T0(a) → T0a etc.)
        from lib.shared.common import load_property_sections
        sections = load_property_sections(prop_dir)
        ordered = topological_sort_labels(deps_data)

        # Determine which properties to review
        if single_label:
            review_labels = [single_label]
        elif cycle == 1 or mode == "full_sweep":
            # Skip properties unchanged since last verified run
            review_labels = []
            cached = 0
            for label in ordered:
                content = sections.get(label, "")
                current_hash = _hash_content(content) if content else ""
                if current_hash and verified_hashes.get(label) == current_hash:
                    cached += 1
                    all_verified.add(label)
                else:
                    review_labels.append(label)
            if cached:
                print(f"  [CACHE] {cached} properties unchanged — skipping",
                      file=sys.stderr)
        else:
            # Incremental: only dirty set, in dependency order
            review_labels = [l for l in ordered if l in dirty_set]

        label_desc = (f"{len(review_labels)} properties"
                      + (f" (dirty set)" if cycle > 1 and mode == "incremental" else ""))
        print(f"\n  [CYCLE {cycle}/{max_cycles}] {label_desc}",
              file=sys.stderr)

        # Pre-populate foundation cache (shared read-only data)
        from lib.shared.paths import formal_stmts, load_manifest
        foundation_cache = {}
        manifest = load_manifest(asn_num)
        for dep_asn in manifest.get("depends", []) if manifest else []:
            stmt_path = formal_stmts(dep_asn)
            if stmt_path.exists():
                foundation_cache[dep_asn] = stmt_path.read_text()

        # Review all properties in parallel (verify is read-only)
        cycle_findings = {}
        cycle_verified = set()

        def _verify_one(label):
            result, finding_text = review_property(
                asn_num, label, deps_data, sections, foundation_cache)
            return label, (result, finding_text)

        results = parallel_llm_calls(review_labels, _verify_one, max_workers=10)

        for label, result_tuple in results:
            if result_tuple is None:
                continue
            result, finding_text = result_tuple
            if result == "verified":
                cycle_verified.add(label)
            elif result == "found":
                cycle_findings[label] = finding_text

        all_verified.update(cycle_verified)
        for label in cycle_findings:
            all_verified.discard(label)
        all_findings.update(cycle_findings)

        # Update verification cache — save hashes for verified properties
        for label in cycle_verified:
            content = sections.get(label, "")
            if content:
                verified_hashes[label] = _hash_content(content)
        # Invalidate cache for properties with findings
        for label in cycle_findings:
            verified_hashes.pop(label, None)
        _save_verified_hashes(cache_path, verified_hashes)

        print(f"\n  {len(cycle_findings)} found, {len(cycle_verified)} verified",
              file=sys.stderr)

        if not cycle_findings:
            converged = True
            print(f"\n  Converged after {cycle} cycle{'s' if cycle > 1 else ''}.",
                  file=sys.stderr)
            if not had_findings:
                print(f"  Nothing to do.", file=sys.stderr)
            break

        had_findings = True

        # New review file per cycle
        review_dir.mkdir(parents=True, exist_ok=True)
        review_num = next_review_number(asn_label, reviews_dir=review_dir)
        review_path = review_dir / f"review-{review_num}.md"
        with open(review_path, "w") as rf:
            rf.write(f"# Proof Review — {asn_label} (cycle {cycle})\n\n")
            rf.write(f"*{time.strftime('%Y-%m-%d %H:%M')}*\n\n")
            rf.write(f"{len(review_labels)} properties")
            if cycle > 1 and mode == "incremental":
                rf.write(f" ({', '.join(sorted(review_labels))})")
            rf.write(f"\n\n")
            for label, finding_text in cycle_findings.items():
                rf.write(f"### {label}\n\n{finding_text}\n\n")
            rf.write(f"{len(cycle_verified)} verified, "
                     f"{len(cycle_findings)} found.\n")

        if dry_run:
            break

        # Revise each found property
        changed = set()
        for label, finding_text in cycle_findings.items():
            prop_path = prop_dir / (label.replace("(", "").replace(")", "") + ".md")
            ok = revise(asn_num, label, finding_text, prop_path=prop_path)
            if ok:
                changed.add(label)

        if not changed:
            print(f"  No changes made — stopping.", file=sys.stderr)
            break

        # Commit
        step_commit_asn(asn_num,
                        f"proof-review(asn): {asn_label} — cycle {cycle}")

        # Dirty set for next cycle
        dirty_set = changed | _downstream_dependents(changed, deps_data)

        # Invalidate cache for changed + dependents
        for label in dirty_set:
            verified_hashes.pop(label, None)
        _save_verified_hashes(cache_path, verified_hashes)

        # Remove fixed properties from findings if they'll be re-checked
        for label in changed:
            all_findings.pop(label, None)

    # Append final result to last review file
    elapsed = time.time() - start_time
    if had_findings:
        with open(review_path, "a") as rf:
            rf.write(f"\n## Result\n\n")
            if converged:
                rf.write(f"Converged after {cycle} cycle{'s' if cycle > 1 else ''}. "
                         f"{len(all_verified)} verified.\n")
            else:
                rf.write(f"Not converged after {cycle} cycles. "
                         f"{len(all_findings)} findings remain.\n")
            rf.write(f"\n*Elapsed: {elapsed:.0f}s*\n")

        print(f"\n  Review: {review_path.relative_to(WORKSPACE)}",
              file=sys.stderr)

    print(f"  Elapsed: {elapsed:.0f}s", file=sys.stderr)

    if had_findings and not dry_run:
        step_commit_asn(asn_num, hint="proof-review")

    return "converged" if converged else "not_converged"


def main():
    parser = argparse.ArgumentParser(
        description="Proof Review — verify proofs with convergence loop")
    parser.add_argument("asn", help="ASN number (e.g., 40)")
    parser.add_argument("--max-cycles", type=int, default=5,
                        help="Maximum convergence cycles (default: 5)")
    parser.add_argument("--mode", choices=["incremental", "full_sweep"],
                        default="incremental",
                        help="Convergence mode (default: incremental)")
    parser.add_argument("--label", help="Review a single property only")
    parser.add_argument("--force", action="store_true",
                        help="Ignore cache, re-verify all properties")
    parser.add_argument("--dry-run", action="store_true",
                        help="Verify only, don't fix")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    result = run_proof_review(asn_num, max_cycles=args.max_cycles,
                               mode=args.mode, dry_run=args.dry_run,
                               single_label=args.label,
                               force=args.force)
    sys.exit(0 if result == "converged" else 1)


if __name__ == "__main__":
    main()
