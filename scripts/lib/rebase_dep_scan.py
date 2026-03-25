#!/usr/bin/env python3
"""
LLM-assisted dependency scanner for ASN properties.

For each property in an ASN, extracts its derivation section and asks
a focused LLM call to identify foundation labels the property logically
depends on. Merges results into the deps YAML and optionally updates
the ASN's property table.

Usage:
    python scripts/lib/rebase_dep_scan.py 43           # scan and update deps YAML
    python scripts/lib/rebase_dep_scan.py 43 --dry-run  # scan and print, don't write
    python scripts/lib/rebase_dep_scan.py 43 --fix-asn  # also update ASN property table
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from paths import WORKSPACE, STATEMENTS_DIR, load_manifest
from lib.common import find_asn

PROMPT_TEMPLATE = WORKSPACE / "scripts" / "prompts" / "discovery" / "rebase-dep-scan.md"


def read_file(path):
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


# ---------------------------------------------------------------------------
# Extract per-property derivation sections from ASN
# ---------------------------------------------------------------------------

def extract_property_sections(asn_text):
    """Extract the derivation text for each property.

    Finds bold property definitions like **L0 — Name.** and captures
    text up to the next property definition or section header.

    Returns dict of label → derivation text.
    """
    sections = {}

    # Pattern matches: **LABEL — Name.**  or  **LABEL (Name).**
    prop_pattern = re.compile(
        r'^\*\*([A-Z][A-Za-z0-9_()]*(?:-[A-Za-z0-9]+)*)\s*(?:—|–|-)\s*',
        re.MULTILINE
    )

    # Find all property starts
    matches = list(prop_pattern.finditer(asn_text))

    for i, m in enumerate(matches):
        label = m.group(1).strip("*").strip()
        start = m.start()

        # End is either next property or next ## section header
        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            # Find next section header
            next_section = re.search(r'^## ', asn_text[start + 1:], re.MULTILINE)
            end = start + 1 + next_section.start() if next_section else len(asn_text)

        text = asn_text[start:end].strip()

        # Limit to reasonable size (skip very long worked examples)
        if len(text) > 3000:
            text = text[:3000] + "\n[...truncated...]"

        sections[label] = text

    return sections


# ---------------------------------------------------------------------------
# Build available labels from dependency exports
# ---------------------------------------------------------------------------

def build_available_labels(asn_num):
    """Build a formatted list of available foundation labels for the prompt."""
    manifest = load_manifest(asn_num)
    depends = manifest.get("depends", [])

    labels_by_asn = {}
    for dep_id in depends:
        dep_manifest = load_manifest(dep_id)
        title = dep_manifest.get("title", "")
        label = f"ASN-{dep_id:04d}"

        stmt_path = STATEMENTS_DIR / f"{label}-statements.md"
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
# LLM call per property
# ---------------------------------------------------------------------------

def scan_property(label, property_text, asn_label, depends, available_labels,
                  model="sonnet", effort="high"):
    """Call LLM to identify foundation dependencies for one property."""
    template = read_file(PROMPT_TEMPLATE)
    if not template:
        print(f"  [ERROR] Prompt template not found: {PROMPT_TEMPLATE}",
              file=sys.stderr)
        return None

    prompt = (template
              .replace("{{label}}", label)
              .replace("{{asn_label}}", asn_label)
              .replace("{{depends}}", str(depends))
              .replace("{{property_text}}", property_text)
              .replace("{{available_labels}}", available_labels))

    model_flag = {"opus": "claude-opus-4-6", "sonnet": "claude-sonnet-4-6"}.get(model, model)

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
        timeout=120,
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
# Main: scan all properties and merge into deps YAML
# ---------------------------------------------------------------------------

def scan_asn(asn_num, model="sonnet", effort="high", dry_run=False):
    """Scan all properties in an ASN for foundation dependencies.

    Returns updated deps dict, or None on failure.
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  [ERROR] ASN-{asn_num:04d} not found", file=sys.stderr)
        return None

    # Load existing deps YAML
    deps_path = STATEMENTS_DIR / f"ASN-{asn_num:04d}-deps.yaml"
    if not deps_path.exists():
        print(f"  [ERROR] No deps YAML — run: python scripts/lib/rebase_deps.py {asn_num}",
              file=sys.stderr)
        return None

    with open(deps_path) as f:
        deps = yaml.safe_load(f)

    asn_text = asn_path.read_text()
    sections = extract_property_sections(asn_text)
    available_labels = build_available_labels(asn_num)
    manifest = load_manifest(asn_num)
    depends = manifest.get("depends", [])

    print(f"  [DEP-SCAN] ASN-{asn_num:04d}: {len(sections)} property sections, "
          f"scanning with {model}...", file=sys.stderr)

    new_deps_found = 0

    for label, prop_text in sections.items():
        # Skip if not in the deps YAML (might be a worked example label)
        if label not in deps["properties"]:
            continue

        prop_data = deps["properties"][label]

        # Skip definitions with no derivation
        if prop_data.get("type") == "DEF" and prop_data.get("status") == "introduced":
            # Still scan — definitions can reference foundation
            pass

        result = scan_property(label, prop_text, asn_label, depends,
                               available_labels, model=model, effort=effort)

        if result is None:
            continue

        # Merge new dependencies into existing
        existing_labels = set(prop_data.get("follows_from", []))
        existing_asns = set(prop_data.get("follows_from_asns", []))

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
            prop_data["follows_from"] = sorted(existing_labels)
        if existing_asns:
            prop_data["follows_from_asns"] = sorted(existing_asns)

    print(f"  [DEP-SCAN] Done: {new_deps_found} new dependencies found",
          file=sys.stderr)

    if not dry_run and new_deps_found > 0:
        with open(deps_path, "w") as f:
            yaml.dump(deps, f, default_flow_style=False, sort_keys=False,
                      allow_unicode=True, width=120)
        print(f"  [WROTE] {deps_path.relative_to(WORKSPACE)}", file=sys.stderr)

    return deps


def main():
    parser = argparse.ArgumentParser(
        description="LLM-assisted dependency scanner for ASN properties")
    parser.add_argument("asn", help="ASN number (e.g., 43)")
    parser.add_argument("--model", "-m", default="sonnet",
                        choices=["opus", "sonnet"])
    parser.add_argument("--effort", default="high")
    parser.add_argument("--dry-run", action="store_true",
                        help="Scan and print, don't update deps YAML")
    parser.add_argument("--fix-asn", action="store_true",
                        help="Also update the ASN property table (not yet implemented)")
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
