#!/usr/bin/env python3
"""
LLM-assisted dependency scanner for ASN claims.

For each claim in an ASN, extracts its derivation section and asks
a focused LLM call to identify foundation labels the claim logically
depends on. Merges results into the deps YAML and optionally updates
the ASN's claim table.

Usage:
    python scripts/lib/rebase_dep_scan.py 43           # scan and update deps YAML
    python scripts/lib/rebase_dep_scan.py 43 --dry-run  # scan and print, don't write
    python scripts/lib/rebase_dep_scan.py 43 --fix-asn  # also update ASN claim table
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import WORKSPACE, DOMAIN_PROMPTS, load_manifest, formal_stmts, dep_graph
from lib.shared.common import find_asn, read_file, extract_claim_sections, build_label_index, dump_yaml

PROMPT_TEMPLATE = DOMAIN_PROMPTS / "formalization" / "assembly" / "scan-dependency.md"


# ---------------------------------------------------------------------------
# Build available labels from dependency exports
# ---------------------------------------------------------------------------

def _build_available_labels(asn_num):
    """Build a formatted list of available foundation labels for the prompt."""
    manifest = load_manifest(asn_num)
    depends = manifest.get("depends", [])

    labels_by_asn = {}
    for dep_id in depends:
        dep_manifest = load_manifest(dep_id)
        title = dep_manifest.get("title", "")
        label = f"ASN-{dep_id:04d}"

        stmt_path = formal_stmts(dep_id)
        if not stmt_path.exists():
            continue

        text = stmt_path.read_text()
        labels = []
        for m in re.finditer(r'^## (\S+) — ', text, re.MULTILINE):
            labels.append(m.group(1))
        for m in re.finditer(r'^## Definition — \w+ \((\S+?)[\),]', text, re.MULTILINE):
            labels.append(m.group(1))

        labels_by_asn[f"{label} ({title})"] = sorted(set(labels))

    lines = []
    for asn_ref, lbls in labels_by_asn.items():
        lines.append(f"**{asn_ref}**: {', '.join(lbls)}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# LLM call per claim
# ---------------------------------------------------------------------------

def _scan_claim(label, claim_text, asn_label, depends, available_labels,
                  model="sonnet", effort="high"):
    """Call LLM to identify foundation dependencies for one claim."""
    template = read_file(PROMPT_TEMPLATE)
    if not template:
        print(f"  [ERROR] Prompt template not found: {PROMPT_TEMPLATE}",
              file=sys.stderr)
        return None

    prompt = (template
              .replace("{{label}}", label)
              .replace("{{asn_label}}", asn_label)
              .replace("{{depends}}", str(depends))
              .replace("{{claim_text}}", claim_text)
              .replace("{{available_labels}}", available_labels))

    model_flag = {"opus": "claude-opus-4-7", "sonnet": "claude-sonnet-4-6"}.get(model, model)

    cmd = ["claude", "--print", "--model", model_flag,
           "--output-format", "json", "--tools", ""]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["DISABLE_AUTOUPDATER"] = "1"
    if effort:
        env["CLAUDE_CODE_EFFORT_LEVEL"] = effort

    start = time.time()
    result = __import__("subprocess").run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        timeout=None,
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"    [{label}] FAILED ({elapsed:.0f}s)", file=sys.stderr)
        return None

    # Parse JSON response
    try:
        data = json.loads(result.stdout)
        text = data.get("result", result.stdout)
    except (json.JSONDecodeError, KeyError):
        text = result.stdout

    # Extract YAML block from response
    yaml_match = re.search(r'```yaml\s*\n(.*?)\n```', text, re.DOTALL)
    if yaml_match:
        try:
            parsed = yaml.safe_load(yaml_match.group(1))
            deps_list = parsed.get("depends_on", [])
            print(f"    [{label}] {len(deps_list)} deps ({elapsed:.0f}s)", file=sys.stderr)
            return deps_list
        except yaml.YAMLError:
            pass

    # Try parsing the whole response as YAML
    try:
        parsed = yaml.safe_load(text)
        if isinstance(parsed, dict) and "depends_on" in parsed:
            deps_list = parsed["depends_on"]
            print(f"    [{label}] {len(deps_list)} deps ({elapsed:.0f}s)", file=sys.stderr)
            return deps_list
    except yaml.YAMLError:
        pass

    print(f"    [{label}] could not parse response ({elapsed:.0f}s)", file=sys.stderr)
    return None


# ---------------------------------------------------------------------------
# ASN claim table fixer
# ---------------------------------------------------------------------------

def _build_table_fixes(updated_deps, original_deps):
    """Compare updated vs original deps to find claims needing Status fixes.

    Returns dict of label → new_status_text for claims that gained
    new foundation dependencies.
    """
    fixes = {}

    for label, prop in updated_deps["claims"].items():
        orig = original_deps["claims"].get(label, {})
        orig_labels = set(orig.get("follows_from", []))
        new_labels = set(prop.get("follows_from", []))
        added = new_labels - orig_labels

        if not added:
            continue

        # Build the new status text
        # Group added labels by ASN
        asn_groups = {}
        for lbl in sorted(added):
            # Find which ASN this label belongs to
            asn_ref = None
            for a in prop.get("follows_from_asns", []):
                asn_groups.setdefault(a, []).append(lbl)
                break
            else:
                asn_groups.setdefault(None, []).append(lbl)

        parts = []
        for asn_id, labels in sorted(asn_groups.items(), key=lambda x: x[0] or 0):
            label_str = ", ".join(labels)
            if asn_id:
                parts.append(f"{label_str} (ASN-{asn_id:04d})")
            else:
                parts.append(label_str)

        deps_text = "; ".join(parts)

        # Determine new status based on original status
        orig_status = orig.get("status", "introduced")
        if orig_status == "introduced":
            new_status = f"introduced; uses {deps_text}"
        elif orig_status in ("corollary", "from", "theorem", "cited", "confirms"):
            # Already has deps or references foundation — keep original
            new_status = None
        else:
            new_status = f"{orig_status}; uses {deps_text}"

        if new_status:
            fixes[label] = new_status

    return fixes


def _fix_asn_table(asn_path, fixes):
    """Update the ASN file's claim table Status column.

    For each label in fixes, find the table row and replace the Status cell.
    """
    text = asn_path.read_text()
    lines = text.split("\n")

    # Find the claim table
    table_start = None
    for i, line in enumerate(lines):
        if re.match(r"\|\s*Label\s*\|", line):
            table_start = i
            break

    if table_start is None:
        print(f"  [FIX-ASN] WARNING: claim table not found", file=sys.stderr)
        return

    fixed_count = 0
    for i in range(table_start + 2, len(lines)):  # Skip header + separator
        line = lines[i]
        if not line.strip().startswith("|"):
            break

        # Parse the row to get the label (first cell)
        parts = line.split("|")
        if len(parts) < 3:
            continue

        row_label = parts[1].strip().strip("`").strip("*").strip()

        if row_label in fixes:
            # Replace the last cell (Status) with the new text
            # Reconstruct the row with the new status
            new_status = fixes[row_label]
            parts[-2] = f" {new_status} "
            lines[i] = "|".join(parts)
            fixed_count += 1

    if fixed_count > 0:
        asn_path.write_text("\n".join(lines))
        print(f"  [FIX-ASN] Updated {fixed_count} claim table entries in "
              f"{asn_path.name}", file=sys.stderr)
    else:
        print(f"  [FIX-ASN] No table fixes needed", file=sys.stderr)


# ---------------------------------------------------------------------------
# Main: scan all claims and merge into deps YAML
# ---------------------------------------------------------------------------

def scan_asn(asn_num, model="sonnet", effort="high", dry_run=False):
    """Scan all claims in an ASN for foundation dependencies.

    Returns updated deps dict, or None on failure.
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  [ERROR] ASN-{asn_num:04d} not found", file=sys.stderr)
        return None

    # Build deps from per-claim YAMLs
    from lib.formalization.core.build_dependency_graph import generate_formalization_deps
    deps = generate_formalization_deps(asn_num)
    if deps is None:
        print(f"  [ERROR] Could not build deps from per-claim YAMLs",
              file=sys.stderr)
        return None

    asn_text = asn_path.read_text()
    sections = extract_claim_sections(asn_text)
    available_labels = _build_available_labels(asn_num)
    manifest = load_manifest(asn_num)
    depends = manifest.get("depends", [])

    # Snapshot original deps for diff after scan
    import copy
    original_deps = copy.deepcopy(deps)

    print(f"  [DEP-SCAN] ASN-{asn_num:04d}: {len(sections)} claim sections, "
          f"scanning with {model}...", file=sys.stderr)

    new_deps_found = 0

    for label, claim_text in sections.items():
        # Skip if not in the deps YAML (might be a worked example label)
        if label not in deps["claims"]:
            continue

        claim_data = deps["claims"][label]

        # Skip definitions with no derivation
        if claim_data.get("type") == "DEF" and claim_data.get("status") == "introduced":
            # Still scan — definitions can reference foundation
            pass

        result = _scan_claim(label, claim_text, asn_label, depends,
                               available_labels, model=model, effort=effort)

        if result is None:
            continue

        # Merge new dependencies into existing
        existing_labels = set(claim_data.get("follows_from", []))
        existing_asns = set(claim_data.get("follows_from_asns", []))

        for dep in result:
            dep_label = dep.get("label", "")
            dep_asn = dep.get("asn")

            if dep_label and dep_label not in existing_labels:
                existing_labels.add(dep_label)
                new_deps_found += 1

            if dep_asn and dep_asn not in existing_asns:
                existing_asns.add(dep_asn)

        # Update deps data
        if existing_labels:
            claim_data["follows_from"] = sorted(existing_labels)
        if existing_asns:
            claim_data["follows_from_asns"] = sorted(existing_asns)

    print(f"  [DEP-SCAN] Done: {new_deps_found} new dependencies found",
          file=sys.stderr)

    if not dry_run and new_deps_found > 0:
        # Write updated deps YAML
        with open(deps_path, "w") as f:
            yaml.dump(deps, f, default_flow_style=False, sort_keys=False,
                      allow_unicode=True, width=120)
        print(f"  [WROTE] {deps_path.relative_to(WORKSPACE)}", file=sys.stderr)

        # Update per-claim YAML depends fields
        from lib.shared.paths import FORMALIZATION_DIR
        claim_dir = FORMALIZATION_DIR / asn_label
        if claim_dir.exists():
            _label_index = build_label_index(claim_dir)
            for label, claim_data in deps.get("claims", {}).items():
                stem = _label_index.get(label)
                if stem is None:
                    continue
                yaml_path = claim_dir / f"{stem}.yaml"
                if not yaml_path.exists():
                    continue
                with open(yaml_path) as yf:
                    ydata = yaml.safe_load(yf)
                new_deps = claim_data.get("follows_from", [])
                old_deps = ydata.get("depends", [])
                # Add-only: merge new deps into existing
                merged = list(dict.fromkeys(old_deps + [d for d in new_deps if d not in old_deps]))
                if merged != old_deps:
                    ydata["depends"] = merged
                    dump_yaml(ydata, yaml_path)

    return deps


def main():
    parser = argparse.ArgumentParser(
        description="LLM-assisted dependency scanner for ASN claims")
    parser.add_argument("asn", help="ASN number (e.g., 43)")
    parser.add_argument("--model", "-m", default="sonnet",
                        choices=["opus", "sonnet"])
    parser.add_argument("--effort", default="high")
    parser.add_argument("--dry-run", action="store_true",
                        help="Scan and print, don't update deps YAML or ASN")
    parser.add_argument("--no-fix", action="store_true",
                        help="Update deps YAML but don't fix ASN claim table")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    deps = scan_asn(asn_num, model=args.model, effort=args.effort,
                    dry_run=args.dry_run)

    if deps is None:
        sys.exit(1)

    if args.dry_run:
        yaml.dump(deps, sys.stdout, default_flow_style=False, sort_keys=False,
                  allow_unicode=True, width=120)


if __name__ == "__main__":
    main()
