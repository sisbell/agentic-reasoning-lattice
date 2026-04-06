"""
Standalone proofs — write rigorous proofs for properties that lack them.

Revived from repair_sections.py (commit c1d5eaf). Identifies properties
whose proofs are embedded in other properties' sections and writes
self-contained Dijkstra-style proofs in each property's own section.

Step functions for the elaboration orchestrator (scripts/elaborate.py):
- find_incomplete_sections: detect properties without standalone proofs
- build_repair_context: build dependency context for a repair
- repair_section: write one standalone proof via opus
"""

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import WORKSPACE, USAGE_LOG, formal_stmts
from lib.shared.common import find_asn, extract_property_sections
from lib.formalization.core.build_dependency_graph import (
    find_property_table, parse_table_row, generate_deps,
)

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "elaboration"
ELABORATE_TEMPLATE = PROMPTS_DIR / "elaborate.md"


def _log_usage(step, elapsed, asn_num, label=""):
    """Append usage entry."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": f"elaborate-{step}",
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
    """Find properties with no proof in their own section.

    Returns list of dicts:
        label: property label
        thin_section: the incomplete section text
        host_label: label of the property whose section contains the proof (or None)
        host_section: the host section text (or None)
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return []

    text = asn_path.read_text()
    rows = find_property_table(text)
    if rows is None:
        return []

    # Get all labels
    labels = []
    for row in rows[2:]:
        cells = parse_table_row(row)
        if cells and cells[0].strip():
            labels.append(cells[0].strip().strip("`*"))

    # Extract sections
    sections = extract_property_sections(text, known_labels=labels,
                                          truncate=False)

    # Find incomplete sections
    incomplete = []
    for label in labels:
        section = sections.get(label, "")
        if not section:
            continue
        if _is_definition(section):
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


def build_repair_context(asn_num, label, deps_data, sections):
    """Build dependency context for a section repair."""
    prop_data = deps_data.get("properties", {}).get(label, {})
    follows_from = prop_data.get("follows_from", [])
    all_labels = set(deps_data.get("properties", {}).keys())

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
    """Write a standalone proof for one property. Returns True on success."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return False

    template = ELABORATE_TEMPLATE.read_text()
    rel_path = asn_path.relative_to(WORKSPACE)

    prompt = (template
              .replace("{{label}}", label)
              .replace("{{thin_section}}", thin_section)
              .replace("{{host_section}}", host_section or "(no embedded proof found)")
              .replace("{{dependency_sections}}", dependency_text)
              .replace("{{asn_path}}", str(rel_path)))

    for cycle in range(1, max_cycles + 1):
        print(f"  [REPAIR] {label} (cycle {cycle}, "
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
        _log_usage("repair", elapsed, asn_num, label=label)

        if result.returncode != 0:
            print(f"  [REPAIR] Failed ({elapsed:.0f}s)", file=sys.stderr)
            return False

        print(f"  [REPAIR] Done ({elapsed:.0f}s)", file=sys.stderr)

        # Re-check: does the section now have a proof?
        text = asn_path.read_text()
        updated_sections = extract_property_sections(
            text, known_labels=[label], truncate=False)
        updated = updated_sections.get(label, "")

        if _has_proof(updated):
            print(f"  [REPAIR] {label} — section now has proof",
                  file=sys.stderr)
            return True

        print(f"  [REPAIR] {label} — still no proof, retrying...",
              file=sys.stderr)

    print(f"  [REPAIR] {label} — failed after {max_cycles} cycles",
          file=sys.stderr)
    return False
