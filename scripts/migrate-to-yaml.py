#!/usr/bin/env python3
"""
Migrate old formalization format to per-property YAML + MD pairs.

Reads _table.md + per-property .md files from vault/3-formalization/ASN-NNNN/,
generates per-property .yaml metadata files alongside the existing .md files.

Usage:
    python scripts/migrate-to-yaml.py 34
    python scripts/migrate-to-yaml.py 34 --dry-run
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import WORKSPACE, FORMALIZATION_DIR
from lib.shared.common import find_asn, label_to_filename, dump_yaml


# Status string → type classification
STATUS_TYPE_MAP = {
    "axiom": "axiom",
    "definition": "definition",
    "design requirement": "design-requirement",
    "introduced": "definition",
}


def _parse_status(status_text):
    """Parse status string into (type, depends).

    Examples:
        'axiom' → ('axiom', [])
        'from S0' → ('corollary', ['S0'])
        'theorem from S8-fin, S2, S8a' → ('theorem', ['S8-fin', 'S2', 'S8a'])
        'corollary of T4' → ('corollary', ['T4'])
        'lemma (from T1, T3)' → ('lemma', ['T1', 'T3'])
        'consistent with S0, S1' → ('theorem', ['S0', 'S1'])
        'design requirement' → ('design-requirement', [])
    """
    text = status_text.strip().lower()

    # Direct type matches
    for key, ptype in STATUS_TYPE_MAP.items():
        if text == key:
            return ptype, []

    # 'axiom (postconditions from X)' pattern
    if text.startswith("axiom"):
        return "axiom", []

    # 'design requirement' variations
    if "design" in text and "requirement" in text:
        return "design-requirement", []
    if text.startswith("design"):
        return "design-requirement", []

    # Extract dep labels from status string
    dep_labels = []
    # Remove known prefix patterns
    cleaned = re.sub(r'^(theorem|lemma|corollary|from|consistent with|cited|confirms|extends)\s*', '', text)
    cleaned = re.sub(r'^\(?(from|of)\s*', '', cleaned)
    cleaned = cleaned.rstrip(')')

    # Extract labels: sequences of word chars, dots, hyphens
    for m in re.finditer(r'[A-Z][A-Za-z0-9\.\-]+', status_text):
        label = m.group(0).rstrip(',').strip()
        if label and label.lower() not in ('asn', 'from', 'of', 'with'):
            dep_labels.append(label)

    # Also catch ASN references like (ASN-0034)
    for m in re.finditer(r'\(ASN-\d+\)', status_text):
        pass  # We strip ASN refs per new convention

    # Determine type from prefix
    if text.startswith("theorem"):
        return "theorem", dep_labels
    elif text.startswith("lemma"):
        return "lemma", dep_labels
    elif text.startswith("corollary"):
        return "corollary", dep_labels
    elif text.startswith("from"):
        # 'from X' — could be corollary or derived
        return "corollary", dep_labels
    elif text.startswith("consistent"):
        return "theorem", dep_labels
    elif text.startswith("cited") or text.startswith("confirms"):
        return "theorem", dep_labels
    elif text.startswith("extends"):
        return "theorem", dep_labels

    # Fallback
    return "definition", dep_labels


def _parse_table(table_text):
    """Parse _table.md into list of {label, name, status, type, depends}."""
    rows = []
    for line in table_text.split("\n"):
        line = line.strip()
        if not line.startswith("|") or line.startswith("| Label") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.split("|")]
        cells = [c for c in cells if c]  # remove empty from leading/trailing |
        if len(cells) < 2:
            continue

        label = cells[0].strip("`*")
        name = cells[1] if len(cells) > 2 else ""
        status = cells[-1].strip() if cells else ""

        ptype, deps = _parse_status(status)

        rows.append({
            "label": label,
            "name": name,
            "status": status,
            "type": ptype,
            "depends": deps,
        })

    return rows


def migrate_asn(asn_num, dry_run=False):
    """Generate per-property YAML files from old format."""
    _, asn_label = find_asn(str(asn_num))
    if asn_label is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return False

    prop_dir = FORMALIZATION_DIR / asn_label
    if not prop_dir.exists():
        print(f"  No formalization directory for {asn_label}", file=sys.stderr)
        return False

    table_path = prop_dir / "_table.md"
    if not table_path.exists():
        print(f"  No _table.md found", file=sys.stderr)
        return False

    print(f"\n  [MIGRATE] {asn_label}", file=sys.stderr)
    print(f"  Source: {prop_dir.relative_to(WORKSPACE)}", file=sys.stderr)

    # Parse table
    table_rows = _parse_table(table_path.read_text())
    print(f"  {len(table_rows)} properties in table", file=sys.stderr)

    # Generate YAML for each property
    created = 0
    skipped = 0
    missing_md = 0

    for row in table_rows:
        label = row["label"]
        stem = label_to_filename(label).replace(".md", "")
        yaml_path = prop_dir / f"{stem}.yaml"
        md_path = prop_dir / f"{stem}.md"

        if yaml_path.exists():
            skipped += 1
            continue

        if not md_path.exists():
            print(f"    WARNING: {stem}.md not found for label '{label}'",
                  file=sys.stderr)
            missing_md += 1
            continue

        meta = {
            "label": label,
            "name": row["name"],
            "type": row["type"],
            "depends": row["depends"],
        }

        if dry_run:
            print(f"    {stem}.yaml  ({row['type']}, {len(row['depends'])} deps)",
                  file=sys.stderr)
        else:
            dump_yaml(meta, yaml_path)
            print(f"    {stem}.yaml", file=sys.stderr)

        created += 1

    print(f"\n  [MIGRATE] {created} created, {skipped} skipped (already exist), "
          f"{missing_md} missing .md files", file=sys.stderr)
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Migrate old formalization format to per-property YAML")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be created")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    ok = migrate_asn(asn_num, dry_run=args.dry_run)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
