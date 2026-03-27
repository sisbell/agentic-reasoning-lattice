"""
Quality pass — Dijkstra-style rewrite + formal contracts for all properties.

Rewrites every non-definition property's proof to Dijkstra standard
and ensures each has a complete formal contract. Narrow scope — one
property at a time, no dependency context needed.

Usage (standalone):
    python scripts/lib/quality_pass.py 34
    python scripts/lib/quality_pass.py 34 --label T1
    python scripts/lib/quality_pass.py 34 --dry-run
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import WORKSPACE, USAGE_LOG
from lib.shared.common import find_asn, extract_property_sections, step_commit_asn
from lib.formalization.deps import (find_property_table, parse_table_row,
                              detect_columns, generate_deps)

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "formalization"
QUALITY_TEMPLATE = PROMPTS_DIR / "quality-pass.md"


def _log_usage(step, elapsed, asn_num, label=""):
    """Append usage entry."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": f"quality-{step}",
            "asn": f"ASN-{asn_num:04d}",
            "elapsed_s": round(elapsed, 1),
        }
        if label:
            entry["label"] = label
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def _is_definition(section_text):
    """Check if a section is a definition."""
    return bool(re.match(r'^\*\*Definition\s*\(', section_text.strip()))


def _has_formal_contract(section_text):
    """Check if a section has a formal contract."""
    return '*Formal Contract:*' in section_text


def find_properties_needing_quality(asn_num, force_all=True):
    """Find properties that need a quality pass.

    If force_all=True, returns ALL non-definition properties.
    If force_all=False, returns only those missing formal contracts.
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return []

    text = asn_path.read_text()
    rows = find_property_table(text)
    if rows is None:
        return []

    labels = []
    for row in rows[2:]:
        cells = parse_table_row(row)
        if cells and cells[0].strip():
            labels.append(cells[0].strip().strip("`*"))

    sections = extract_property_sections(text, known_labels=labels,
                                          truncate=False)

    needs_quality = []
    for label in labels:
        section = sections.get(label, "")
        if not section:
            continue
        if _is_definition(section):
            continue

        if force_all or not _has_formal_contract(section):
            needs_quality.append({
                "label": label,
                "section": section,
            })

    return needs_quality


def quality_rewrite(asn_num, label, section, max_cycles=3):
    """Rewrite one property to Dijkstra standard. Returns True on success."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return False

    template = QUALITY_TEMPLATE.read_text()
    rel_path = asn_path.relative_to(WORKSPACE)

    prompt = (template
              .replace("{{label}}", label)
              .replace("{{section}}", section)
              .replace("{{asn_path}}", str(rel_path)))

    for cycle in range(1, max_cycles + 1):
        print(f"  [QUALITY] {label} (cycle {cycle}, "
              f"{len(prompt) // 1024}KB)...",
              file=sys.stderr)

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
        _log_usage("rewrite", elapsed, asn_num, label=label)

        if result.returncode != 0:
            print(f"  [QUALITY] Failed ({elapsed:.0f}s)", file=sys.stderr)
            return False

        print(f"  [QUALITY] Done ({elapsed:.0f}s)", file=sys.stderr)

        # Re-check: does the section now have a formal contract?
        text = asn_path.read_text()
        updated = extract_property_sections(
            text, known_labels=[label], truncate=False)
        updated_section = updated.get(label, "")

        if _has_formal_contract(updated_section):
            print(f"  [QUALITY] {label} — has formal contract",
                  file=sys.stderr)
            step_commit_asn(asn_num,
                            hint=f"{label} quality rewrite")
            return True

        print(f"  [QUALITY] {label} — missing formal contract, retrying...",
              file=sys.stderr)

    print(f"  [QUALITY] {label} — failed after {max_cycles} cycles",
          file=sys.stderr)
    return False


def _topological_sort_labels(deps_data):
    """Sort property labels in dependency order."""
    props = deps_data.get("properties", {})
    all_labels = set(props.keys())
    graph = {}
    for label, prop in props.items():
        graph[label] = set(prop.get("follows_from", [])) & all_labels

    result = []
    visited = set()
    visiting = set()

    def visit(node):
        if node in visited:
            return
        if node in visiting:
            return
        visiting.add(node)
        for dep in graph.get(node, set()):
            visit(dep)
        visiting.remove(node)
        visited.add(node)
        result.append(node)

    for label in sorted(graph.keys()):
        visit(label)
    return result


def step_quality_pass(asn_num, force_all=True):
    """Quality pass on all properties. Returns (rewritten, failed)."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return 0, 0

    needs_quality = find_properties_needing_quality(asn_num,
                                                     force_all=force_all)
    if not needs_quality:
        print(f"\n  [QUALITY] {asn_label}: all properties at quality standard",
              file=sys.stderr)
        return 0, 0

    needs_labels = {item["label"] for item in needs_quality}
    needs_map = {item["label"]: item for item in needs_quality}

    # Sort in dependency order
    deps_data = generate_deps(asn_num)
    ordered = _topological_sort_labels(deps_data) if deps_data else sorted(needs_labels)

    print(f"\n  [QUALITY] {asn_label}: {len(needs_quality)} properties "
          f"need quality pass", file=sys.stderr)

    rewritten = 0
    failed = 0

    for label in ordered:
        if label not in needs_labels:
            continue

        item = needs_map[label]
        ok = quality_rewrite(asn_num, label, item["section"])

        if ok:
            rewritten += 1
            # Re-read sections for subsequent properties
            text = asn_path.read_text()
            all_labels = list(deps_data.get("properties", {}).keys())
            sections = extract_property_sections(
                text, known_labels=all_labels, truncate=False)
            # Update the map with fresh sections
            for l in needs_labels:
                if l in sections:
                    needs_map[l]["section"] = sections[l]
        else:
            failed += 1

    print(f"\n  [QUALITY] Done: {rewritten} rewritten, {failed} failed",
          file=sys.stderr)
    return rewritten, failed


def main():
    parser = argparse.ArgumentParser(
        description="Quality pass — Dijkstra rewrite + formal contracts")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument("--label", help="Rewrite a single label only")
    parser.add_argument("--dry-run", action="store_true",
                        help="List properties needing quality pass")
    parser.add_argument("--contracts-only", action="store_true",
                        help="Only target properties missing formal contracts")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    force_all = not args.contracts_only

    if args.dry_run:
        needs = find_properties_needing_quality(asn_num, force_all=force_all)
        print(f"\n  {len(needs)} properties need quality pass:")
        for item in needs:
            has_contract = _has_formal_contract(item["section"])
            status = "has contract" if has_contract else "NO contract"
            print(f"    {item['label']:30s} {status}")
        return

    if args.label:
        needs = find_properties_needing_quality(asn_num, force_all=True)
        item = next((i for i in needs if i["label"] == args.label), None)
        if item is None:
            print(f"  {args.label} not found or is a definition",
                  file=sys.stderr)
            sys.exit(1)
        ok = quality_rewrite(asn_num, args.label, item["section"])
        sys.exit(0 if ok else 1)

    r, f = step_quality_pass(asn_num, force_all=force_all)
    sys.exit(0 if f == 0 else 1)


if __name__ == "__main__":
    main()
