"""
Produce Contract step — Dijkstra rewrite + formal contracts per property.

Step functions for the formalize orchestrator (scripts/formalize.py):
- find_properties_needing_quality: scan ASN for properties needing rewrite
- quality_rewrite: rewrite one property to Dijkstra standard with formal contract
"""

import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import WORKSPACE, USAGE_LOG, FORMALIZATION_DIR, formal_stmts
from lib.shared.common import find_asn, invoke_claude, build_label_index, load_property_metadata
from lib.formalization.core.build_dependency_graph import generate_formalization_deps

from lib.formalization.assembly.validate_contracts import validate_contract

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "formalization" / "formalize"
QUALITY_TEMPLATE = PROMPTS_DIR / "produce-contract.md"
REVIEW_REWRITE_TEMPLATE = PROMPTS_DIR / "review-rewrite.md"


def _log_usage(step, elapsed, asn_num, label=""):
    """Append usage entry."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": f"produce-contract-{step}",
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
    return bool(re.search(r'^\*\*Definition\s*\(', section_text, re.MULTILINE))


def _has_formal_contract(section_text):
    """Check if a section has a formal contract."""
    return '*Formal Contract:*' in section_text


def _downstream_dependents(changed_labels, deps_data):
    """Find properties that depend on any of the changed labels."""
    dependents = set()
    for label, prop_data in deps_data.get("properties", {}).items():
        follows = set(prop_data.get("follows_from", []))
        if follows & changed_labels:
            dependents.add(label)
    return dependents


def _compute_hash(text):
    """Compute a short content hash."""
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def _find_dirty(current_hashes, stored_hashes, deps_data):
    """Find properties that are dirty (changed or dependency changed).

    Returns set of dirty labels.
    """
    dirty = set()

    # First pass: mark directly changed
    for label, current in current_hashes.items():
        stored = stored_hashes.get(label)
        if stored is None or stored != current:
            dirty.add(label)

    # Transitive pass: mark dependents of dirty properties
    changed = True
    while changed:
        changed = False
        for label, prop in deps_data.get("properties", {}).items():
            if label in dirty:
                continue
            follows = set(prop.get("follows_from", []))
            if follows & dirty:
                dirty.add(label)
                changed = True

    return dirty


def find_properties_needing_quality(asn_num, force_all=True, force_rebuild=False):
    """Find properties that need a quality pass.

    Reads per-property files from vault/3-formalization/ASN-NNNN/.

    If force_rebuild=True, returns ALL (ignores hashes).
    If force_all=True, uses hash-based dirty detection.
    If force_all=False, returns only those missing formal contracts.
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return [], {}

    prop_dir = FORMALIZATION_DIR / asn_label
    if not prop_dir.exists():
        print(f"  No formalization directory for {asn_label}", file=sys.stderr)
        return [], {}
    label_index = build_label_index(prop_dir)
    _filename_to_label = {f"{stem}.md": lbl for lbl, stem in label_index.items()}

    # Read types from per-property YAMLs
    metadata = load_property_metadata(prop_dir)
    statuses = {lbl: data.get("type", "") for lbl, data in metadata.items()}

    # Read per-property files
    prop_files = sorted(
        f for f in prop_dir.glob("*.md")
        if not f.name.startswith("_")
    )

    # Build candidate list (exclude definitions, axioms)
    candidates = []
    for f in prop_files:
        content = f.read_text()
        if not content.strip():
            continue
        label = _filename_to_label.get(f.name, f.stem)
        if _is_definition(content):
            continue
        if statuses.get(label, "") in ("axiom", "design-requirement"):
            continue
        candidates.append({"label": label, "section": content, "path": f})

    if not force_all:
        return [c for c in candidates if not _has_formal_contract(c["section"])], {}

    if force_rebuild:
        return candidates, {}

    # Hash-based dirty detection
    deps_data = generate_formalization_deps(asn_num)
    if deps_data is None:
        return candidates, {}

    stored_hashes = {}
    skip_labels = set()
    for label, prop in deps_data.get("properties", {}).items():
        if "hash" in prop:
            stored_hashes[label] = prop["hash"]
        if prop.get("skip_quality"):
            skip_labels.add(label)

    current_hashes = {c["label"]: _compute_hash(c["section"])
                      for c in candidates}

    dirty = _find_dirty(current_hashes, stored_hashes, deps_data)

    # Dirty (hash changed) or missing contract → needs produce-contract.
    # Unchanged properties are cached. Convergence = no changes made.
    needs = []
    cached = 0
    for c in candidates:
        label = c["label"]
        if label in skip_labels:
            print(f"  [PRODUCE-CONTRACT] {label} — skip_quality set, skipping",
                  file=sys.stderr)
            cached += 1
            continue
        if label in dirty or not _has_formal_contract(c["section"]):
            needs.append(c)
        else:
            cached += 1

    if cached:
        print(f"  [CACHE] {cached} properties cached, {len(needs)} dirty",
              file=sys.stderr)

    return needs, current_hashes



def _review_rewrite(pre_section, post_section, label):
    """Review a quality rewrite for damage. Returns (ok, detail)."""
    from lib.shared.common import invoke_claude

    template = REVIEW_REWRITE_TEMPLATE.read_text()
    prompt = (template
              .replace("{{label}}", label)
              .replace("{{before}}", pre_section)
              .replace("{{after}}", post_section))

    result, elapsed = invoke_claude(prompt, model="sonnet", effort="high")

    if result is None:
        return True, ""  # LLM failed, don't block

    if "RESULT: PASS" in result:
        return True, ""

    if "RESULT: FAIL" in result:
        idx = result.find("RESULT: FAIL")
        detail = result[idx + len("RESULT: FAIL"):].strip()
        return False, detail

    return True, ""  # Unclear, don't block


def _build_dep_context(asn_num, label):
    """Build dependency context for a property — same-ASN files + foundation excerpts."""
    deps_data = generate_formalization_deps(asn_num)
    if not deps_data:
        return "(none)"

    prop_data = deps_data.get("properties", {}).get(label, {})
    follows_from = prop_data.get("follows_from", [])
    all_labels = set(deps_data.get("properties", {}).keys())

    _, asn_label = find_asn(str(asn_num))
    prop_dir = FORMALIZATION_DIR / asn_label
    _label_index = build_label_index(prop_dir)

    dep_parts = []
    for dep_label in follows_from:
        if dep_label in all_labels:
            dep_stem = _label_index.get(dep_label, dep_label.replace("(", "").replace(")", ""))
            dep_file = prop_dir / f"{dep_stem}.md"
            if dep_file.exists():
                dep_parts.append(f"### {dep_label}\n\n{dep_file.read_text().strip()}")

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


def produce_contract(asn_num, label, section, prop_path=None, max_cycles=3):
    """Rewrite one property to Dijkstra standard.

    Print-mode only — model receives the section + dependency context,
    returns the rewritten section. Writes directly to the property file.

    Returns (ok, changed, response_text):
        ok: bool — whether the property now has a formal contract
        changed: bool — whether the property file was actually modified
        response_text: str — LLM response for the review file
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return False, False, ""

    template = QUALITY_TEMPLATE.read_text()

    # Build dependency context (same-ASN files + foundation excerpts)
    dep_text = _build_dep_context(asn_num, label)

    prompt = (template
              .replace("{{label}}", label)
              .replace("{{section}}", section)
              .replace("{{dependency_sections}}", dep_text))

    pre_content = section

    for cycle in range(1, max_cycles + 1):
        print(f"  [PRODUCE-CONTRACT] {label} (cycle {cycle}, "
              f"{len(prompt) // 1024}KB)...",
              file=sys.stderr)

        # Print mode — no tools, model returns the rewritten section
        response_text, elapsed = invoke_claude(prompt, model="opus",
                                                effort="high")
        _log_usage("rewrite", elapsed, asn_num, label=label)

        if not response_text:
            print(f"  [PRODUCE-CONTRACT] Failed ({elapsed:.0f}s)", file=sys.stderr)
            return False, False, ""

        # Parse response — should be the complete rewritten section
        new_section = response_text.strip()

        # Reject tool_call leaks
        if "<tool_call>" in new_section:
            print(f"  [PRODUCE-CONTRACT] REJECTED (tool_call leak)", file=sys.stderr)
            continue

        # Check if unchanged
        if new_section == section.strip():
            print(f"  [PRODUCE-CONTRACT] {label} — no changes", file=sys.stderr)
            return True, False, response_text

        # Review gate
        review_ok, review_detail = _review_rewrite(
            section, new_section, label)
        if not review_ok:
            print(f"  [PRODUCE-CONTRACT] REJECTED — {review_detail}",
                  file=sys.stderr)
            return False, False, f"REJECTED: {review_detail}"

        # Write directly to property file
        if prop_path:
            prop_path.write_text(new_section + "\n")
        print(f"  [PRODUCE-CONTRACT] Done ({elapsed:.0f}s)", file=sys.stderr)

        if _has_formal_contract(new_section):
            # Validate contract — report result, outer cycle handles retries
            match, detail = validate_contract(label, new_section)
            file_changed = new_section.strip() != pre_content.strip()
            if match:
                print(f"  [CONTRACT] {label} — MATCH", file=sys.stderr)
            else:
                print(f"  [CONTRACT] {label} — MISMATCH", file=sys.stderr)
                for line in detail.split('\n')[:3]:
                    if line.strip():
                        print(f"    {line.strip()}", file=sys.stderr)
            return True, file_changed, detail if detail else response_text

        # Update section for next cycle (it changed)
        section = new_section
        print(f"  [PRODUCE-CONTRACT] {label} — missing formal contract, retrying...",
              file=sys.stderr)

    print(f"  [PRODUCE-CONTRACT] {label} — failed after {max_cycles} cycles",
          file=sys.stderr)
    return False, False, ""
