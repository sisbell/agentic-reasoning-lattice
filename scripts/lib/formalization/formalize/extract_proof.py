"""
Section repair — write standalone proofs for embedded claims.

Identifies claims whose proofs are embedded in other claims'
sections and writes self-contained Dijkstra-style proofs in each
claim's own section.

Usage (standalone):
    python scripts/lib/repair_sections.py 34
    python scripts/lib/repair_sections.py 34 --label TA1-strict
    python scripts/lib/repair_sections.py 34 --dry-run
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
from lib.shared.paths import (WORKSPACE, USAGE_LOG, REVIEWS_DIR,
                   prompt_path, formal_stmts, load_manifest,
                   next_review_number)
from lib.shared.common import find_asn, extract_claim_sections, step_commit_asn
from lib.formalization.core.build_dependency_graph import (find_claim_table, parse_table_row,
                              detect_columns, generate_formalization_deps)
from lib.formalization.core.topological_sort import topological_sort_labels

REPAIR_TEMPLATE = prompt_path("formalization/formalize/extract-proof.md")


def _log_usage(step, elapsed, asn_num, label=""):
    """Append usage entry."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": f"repair-section-{step}",
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
    """Check if a section is a definition (no proof needed)."""
    return bool(re.match(r'^\*\*Definition\s*\(', section_text.strip()))


def _has_proof(section_text):
    """Check if a section contains proof text."""
    proof_markers = ['*Proof.*', '*Proof.* ', 'Proof.', '∎',
                     '*Verification', '*Derivation', '*Claim']
    return any(marker in section_text for marker in proof_markers)


def find_incomplete_sections(asn_num):
    """Find claims with no proof in their own section.

    Returns list of dicts:
        label: claim label
        thin_section: the incomplete section text
        host_label: label of the claim whose section contains the proof (or None)
        host_section: the host section text (or None)
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return []

    text = asn_path.read_text()
    rows = find_claim_table(text)
    if rows is None:
        return []

    # Get all labels and statuses
    labels = []
    statuses = {}
    for row in rows[2:]:
        cells = parse_table_row(row)
        if cells and cells[0].strip():
            label = cells[0].strip().strip("`*")
            labels.append(label)
            statuses[label] = cells[-1].strip().lower()

    # Extract sections
    sections = extract_claim_sections(text, known_labels=labels,
                                          truncate=False)

    # Find incomplete sections
    incomplete = []
    for label in labels:
        section = sections.get(label, "")
        if not section:
            continue
        if _is_definition(section):
            continue
        if statuses.get(label, "") in ("axiom", "design requirement"):
            continue
        if _has_proof(section):
            continue

        # Find the host section containing the embedded proof
        host_label = None
        host_section = None

        # Scan for "Verification of LABEL", "Claim (LABEL)", "Claim: (LABEL)"
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
                    host_label = other_label
                    host_section = other_section
                    break
            if host_label:
                break

        incomplete.append({
            "label": label,
            "thin_section": section,
            "host_label": host_label,
            "host_section": host_section,
        })

    return incomplete


def find_oversized_sections(asn_num):
    """Find sections containing proofs for OTHER claims.

    Returns list of dicts:
        label: the embedded claim label (needs its own section)
        thin_section: the embedded claim's own section (if it exists)
        host_label: the claim whose section contains the embedded proof
        host_section: the host section text
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return []

    text = asn_path.read_text()
    rows = find_claim_table(text)
    if rows is None:
        return []

    labels = []
    for row in rows[2:]:
        cells = parse_table_row(row)
        if cells and cells[0].strip():
            labels.append(cells[0].strip().strip("`*"))

    label_set = set(labels)
    sections = extract_claim_sections(text, known_labels=labels,
                                          truncate=False)

    # For each section, check if it contains proofs for other claims
    oversized = []
    seen = set()

    for host_label in labels:
        host_section = sections.get(host_label, "")
        if not host_section:
            continue

        for other_label in labels:
            if other_label == host_label:
                continue
            if other_label in seen:
                continue

            patterns = [
                re.compile(r'Verification of.*\b' + re.escape(other_label) + r'\b'),
                re.compile(r'Claim[:\s]*\(?' + re.escape(other_label) + r'\)?'),
            ]

            for pattern in patterns:
                if pattern.search(host_section):
                    # Check if other_label already has its own proof
                    other_section = sections.get(other_label, "")
                    if not _has_proof(other_section) and not _is_definition(other_section):
                        oversized.append({
                            "label": other_label,
                            "thin_section": other_section,
                            "host_label": host_label,
                            "host_section": host_section,
                        })
                        seen.add(other_label)
                    break

    return oversized


def build_repair_context(asn_num, label, deps_data, sections):
    """Build dependency context for a section repair."""
    claim_data = deps_data.get("claims", {}).get(label, {})
    follows_from = claim_data.get("follows_from", [])
    all_labels = set(deps_data.get("claims", {}).keys())

    dep_parts = []
    for dep_label in follows_from:
        if dep_label in all_labels and dep_label in sections:
            dep_parts.append(f"### {dep_label}\n\n{sections[dep_label]}")

    # Foundation deps
    depends = deps_data.get("depends", [])
    for dep_label in follows_from:
        if dep_label not in all_labels:
            for dep_asn in depends:
                stmt_path = formal_stmts(dep_asn)
                if stmt_path.exists():
                    ftext = stmt_path.read_text()
                    pattern = re.compile(
                        r'^## ' + re.escape(dep_label) + r'\s*—.*?\n'
                        r'(.*?)(?=^## |\Z)',
                        re.MULTILINE | re.DOTALL
                    )
                    m = pattern.search(ftext)
                    if m:
                        dep_parts.append(
                            f"### {dep_label} (ASN-{dep_asn:04d})\n\n"
                            f"{m.group(0).strip()}"
                        )
                        break

    return "\n\n".join(dep_parts) if dep_parts else "(none)"


def repair_section(asn_num, label, thin_section, host_section,
                   dependency_text, max_cycles=5):
    """Write a standalone proof for one claim. Returns True on success."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return False

    template = REPAIR_TEMPLATE.read_text()
    rel_path = asn_path.relative_to(WORKSPACE)

    prompt = (template
              .replace("{{label}}", label)
              .replace("{{thin_section}}", thin_section)
              .replace("{{host_section}}", host_section or "(no embedded proof found)")
              .replace("{{dependency_sections}}", dependency_text)
              .replace("{{asn_file}}", str(rel_path)))

    for cycle in range(1, max_cycles + 1):
        print(f"  [REPAIR] {label} (cycle {cycle}, "
              f"{len(prompt) // 1024}KB)...",
              file=sys.stderr)

        cmd = [
            "claude", "-p",
            "--model", "claude-opus-4-7",
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
        _log_usage("repair", elapsed, asn_num, label=label)

        if result.returncode != 0:
            print(f"  [REPAIR] Failed ({elapsed:.0f}s)", file=sys.stderr)
            return False

        print(f"  [REPAIR] Done ({elapsed:.0f}s)", file=sys.stderr)

        # Re-check: does the section now have a proof?
        text = asn_path.read_text()
        labels_list = [label]
        updated_sections = extract_claim_sections(
            text, known_labels=labels_list, truncate=False)
        updated = updated_sections.get(label, "")

        if _has_proof(updated):
            print(f"  [REPAIR] {label} — section now has proof",
                  file=sys.stderr)
            step_commit_asn(asn_num,
                            hint=f"{label} standalone proof")
            return True

        print(f"  [REPAIR] {label} — still no proof, retrying...",
              file=sys.stderr)

    print(f"  [REPAIR] {label} — failed after {max_cycles} cycles",
          file=sys.stderr)
    return False


def step_repair_sections(asn_num):
    """Repair all incomplete sections in dependency order.

    Returns (repaired_count, skipped_count, failed_count).
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return 0, 0, 0

    # Find sections needing repair: incomplete + oversized
    incomplete = find_incomplete_sections(asn_num)
    oversized = find_oversized_sections(asn_num)

    # Merge, dedup by label (incomplete takes priority if both detect same label)
    needs_repair_map = {}
    for item in incomplete:
        needs_repair_map[item["label"]] = item
    for item in oversized:
        if item["label"] not in needs_repair_map:
            needs_repair_map[item["label"]] = item

    if not needs_repair_map:
        print(f"\n  [REPAIR] {asn_label}: all sections complete",
              file=sys.stderr)
        return 0, 0, 0

    incomplete_labels = set(needs_repair_map.keys())
    incomplete_map = needs_repair_map

    # Generate deps for context building
    deps_data = generate_formalization_deps(asn_num)
    if deps_data is None:
        return 0, 0, 0

    # Get all sections
    text = asn_path.read_text()
    all_labels = list(deps_data.get("claims", {}).keys())
    sections = extract_claim_sections(text, known_labels=all_labels,
                                          truncate=False)

    # Sort in dependency order
    ordered = topological_sort_labels(deps_data)

    print(f"\n  [REPAIR] {asn_label}: {len(incomplete)} claims "
          f"need repair", file=sys.stderr)

    repaired = 0
    skipped = 0
    failed = 0

    for label in ordered:
        if label not in incomplete_labels:
            continue

        item = incomplete_map[label]
        dep_text = build_repair_context(asn_num, label, deps_data, sections)

        ok = repair_section(
            asn_num, label,
            thin_section=item["thin_section"],
            host_section=item["host_section"],
            dependency_text=dep_text,
        )

        if ok:
            repaired += 1
            # Re-read ASN and sections (changed by repair)
            text = asn_path.read_text()
            sections = extract_claim_sections(
                text, known_labels=all_labels, truncate=False)
        else:
            failed += 1

    print(f"\n  [REPAIR] Done: {repaired} repaired, {skipped} skipped, "
          f"{failed} failed", file=sys.stderr)
    return repaired, skipped, failed


def main():
    parser = argparse.ArgumentParser(
        description="Section repair — standalone proofs for embedded claims")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument("--label", help="Repair a single label only")
    parser.add_argument("--dry-run", action="store_true",
                        help="List incomplete sections without repairing")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))

    if args.dry_run:
        incomplete = find_incomplete_sections(asn_num)
        print(f"\n  {len(incomplete)} claims need repair:")
        for item in incomplete:
            host = f" (proof in {item['host_label']})" if item['host_label'] else " (no embedded proof found)"
            print(f"    {item['label']:30s}{host}")
        return

    if args.label:
        incomplete = find_incomplete_sections(asn_num)
        item = next((i for i in incomplete if i["label"] == args.label), None)
        if item is None:
            print(f"  {args.label} not found or already has proof",
                  file=sys.stderr)
            sys.exit(1)
        deps_data = generate_formalization_deps(asn_num)
        asn_path, _ = find_asn(str(asn_num))
        text = asn_path.read_text()
        all_labels = list(deps_data.get("claims", {}).keys())
        sections = extract_claim_sections(text, known_labels=all_labels,
                                              truncate=False)
        dep_text = build_repair_context(asn_num, args.label, deps_data, sections)
        ok = repair_section(asn_num, args.label,
                            item["thin_section"], item["host_section"],
                            dep_text)
        sys.exit(0 if ok else 1)

    r, s, f = step_repair_sections(asn_num)
    sys.exit(0 if f == 0 else 1)


if __name__ == "__main__":
    main()
