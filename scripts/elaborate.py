#!/usr/bin/env python3
"""
Elaborate — develop rigorous proofs for all properties in an ASN.

Runs the elaboration prompt on every non-definition property, then
proof-review catches mistakes. This is the phase between discovery
and formalization where proofs are developed and corollaries emerge.

Usage:
    python scripts/elaborate.py 40
    python scripts/elaborate.py 40 --max-cycles 3
    python scripts/elaborate.py 40 --dry-run
    python scripts/elaborate.py 40 --label B6
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import WORKSPACE, USAGE_LOG
from lib.shared.common import (find_asn, extract_property_sections,
                                step_commit_asn)
from lib.formalization.core.asn_normalizer import step_stabilize
from lib.formalization.core.build_dependency_graph import (
    find_property_table, parse_table_row, generate_deps,
)
from lib.formalization.core.topological_sort import topological_sort_labels
from lib.elaboration.standalone_proofs import build_repair_context
from importlib import import_module

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "elaboration"
ELABORATE_TEMPLATE = PROMPTS_DIR / "elaborate.md"


def _is_definition(section_text):
    """Check if a section is a definition."""
    return bool(re.match(r'^\*\*Definition\s*\(', section_text.strip()))


def _log_usage(elapsed, asn_num, label=""):
    """Append usage entry."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "elaborate",
            "asn": f"ASN-{asn_num:04d}",
            "elapsed_s": round(elapsed, 1),
        }
        if label:
            entry["label"] = label
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def _find_host_section(label, labels, sections):
    """Find a related section containing an embedded proof for this label."""
    patterns = [
        re.compile(r'Verification of.*\b' + re.escape(label) + r'\b'),
        re.compile(r'Claim[:\s]*\(?' + re.escape(label) + r'\)?'),
    ]
    for other_label in labels:
        if other_label == label:
            continue
        other_section = sections.get(other_label, "")
        if not other_section:
            continue
        for pattern in patterns:
            if pattern.search(other_section):
                return other_section
    return "(none)"


def _elaborate_one(asn_num, label, section, host_section, dep_text):
    """Run the elaborate prompt on one property. Returns True if file changed."""
    asn_path, _ = find_asn(str(asn_num))
    if asn_path is None:
        return False

    template = ELABORATE_TEMPLATE.read_text()
    rel_path = asn_path.relative_to(WORKSPACE)

    prompt = (template
              .replace("{{label}}", label)
              .replace("{{thin_section}}", section)
              .replace("{{host_section}}", host_section)
              .replace("{{dependency_sections}}", dep_text)
              .replace("{{asn_path}}", str(rel_path)))

    pre_content = asn_path.read_text()

    print(f"  [ELABORATE] {label} ({len(prompt) // 1024}KB)...",
          file=sys.stderr, end="", flush=True)

    cmd = [
        "claude", "-p",
        "--model", "claude-opus-4-6",
        "--output-format", "json",
        "--allowedTools", "Edit,Read,Glob,Grep",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = "high"

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE),
    )
    elapsed = time.time() - start
    _log_usage(elapsed, asn_num, label=label)

    if result.returncode != 0:
        print(f" FAILED ({elapsed:.0f}s)", file=sys.stderr)
        return False

    post_content = asn_path.read_text()
    changed = post_content != pre_content

    if changed:
        print(f" changed ({elapsed:.0f}s)", file=sys.stderr)
    else:
        print(f" unchanged ({elapsed:.0f}s)", file=sys.stderr)

    return changed


def _elaborate_all_properties(asn_num, single_label=None, dry_run=False):
    """Run elaborate prompt on all non-definition properties.

    Returns number of properties that changed.
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return 0

    text = asn_path.read_text()
    rows = find_property_table(text)
    if rows is None:
        return 0

    # Get all labels and sections
    labels = []
    statuses = {}
    for row in rows[2:]:
        cells = parse_table_row(row)
        if cells and cells[0].strip():
            label = cells[0].strip().strip("`*")
            labels.append(label)
            statuses[label] = cells[-1].strip().lower()

    sections = extract_property_sections(text, known_labels=labels,
                                          truncate=False)

    # Filter: skip definitions, axioms
    candidates = []
    for label in labels:
        section = sections.get(label, "")
        if not section:
            continue
        if _is_definition(section):
            continue
        if statuses.get(label, "") in ("axiom", "design requirement"):
            continue
        candidates.append(label)

    if single_label:
        candidates = [l for l in candidates if l == single_label]

    # Dependency ordering
    deps_data = generate_deps(asn_num)
    if deps_data:
        ordered = topological_sort_labels(deps_data)
        ordered_candidates = [l for l in ordered if l in set(candidates)]
        ordered_candidates += [l for l in candidates if l not in set(ordered)]
        candidates = ordered_candidates
    else:
        deps_data = {"properties": {}, "depends": []}

    print(f"  [ELABORATE] {len(candidates)} properties", file=sys.stderr)

    if dry_run:
        for label in candidates:
            section = sections.get(label, "")
            has_proof = '∎' in section or '*Proof.*' in section
            has_contract = '*Formal Contract:*' in section
            status = []
            if has_proof:
                status.append("proof")
            if has_contract:
                status.append("contract")
            print(f"    {label:30s} {', '.join(status) if status else 'EMPTY'}",
                  file=sys.stderr)
        return 0

    # Elaborate each property
    changed_count = 0
    for label in candidates:
        section = sections.get(label, "")
        host_section = _find_host_section(label, labels, sections)
        dep_text = build_repair_context(asn_num, label, deps_data, sections)

        changed = _elaborate_one(asn_num, label, section, host_section,
                                  dep_text)

        if changed:
            changed_count += 1
            step_commit_asn(asn_num, hint=f"{label} elaborate")
            # Re-read for downstream properties
            text = asn_path.read_text()
            sections = extract_property_sections(
                text, known_labels=labels, truncate=False)

    return changed_count


def run_elaborate(asn_num, max_cycles=10, dry_run=False, single_label=None):
    """Run the elaboration pipeline.

    Outer loop: format → elaborate all → proof-review (inner, max 3).
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return 0, 0

    print(f"\n  [ELABORATE] {asn_label}", file=sys.stderr)
    start_time = time.time()

    total_changed = 0

    for cycle in range(1, max_cycles + 1):
        print(f"\n  [CYCLE {cycle}/{max_cycles}]", file=sys.stderr)

        # 1. Format gate
        step_stabilize(asn_num)

        # 2. Elaborate all properties
        changed = _elaborate_all_properties(asn_num, single_label,
                                             dry_run=dry_run)
        total_changed += changed

        if dry_run:
            break

        # 3. Inner proof-review (max 3 cycles)
        if changed:
            # Import here to avoid circular/path issues
            sys.path.insert(0, str(Path(__file__).resolve().parent))
            proof_review = import_module("proof_review")
            proof_review.run_proof_review(asn_num, max_cycles=3,
                                          mode="full_sweep")

        # 4. Convergence
        if not changed:
            print(f"\n  Converged after {cycle} cycle{'s' if cycle > 1 else ''}.",
                  file=sys.stderr)
            break

        if single_label:
            break

    elapsed = time.time() - start_time
    print(f"\n  Done: {total_changed} properties changed.",
          file=sys.stderr)
    print(f"  Elapsed: {elapsed:.0f}s", file=sys.stderr)

    return total_changed, 0


def main():
    parser = argparse.ArgumentParser(
        description="Elaborate — develop rigorous proofs for all properties")
    parser.add_argument("asn", help="ASN number (e.g., 40)")
    parser.add_argument("--max-cycles", type=int, default=10,
                        help="Maximum outer cycles (default: 10)")
    parser.add_argument("--label", help="Elaborate a single property only")
    parser.add_argument("--dry-run", action="store_true",
                        help="List properties without elaborating")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    changed, _ = run_elaborate(asn_num, max_cycles=args.max_cycles,
                                dry_run=args.dry_run,
                                single_label=args.label)
    sys.exit(0)


if __name__ == "__main__":
    main()
