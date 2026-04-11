"""
Mechanical reconciliation of _table.md against property files.

Checks that every property file has a table row and vice versa.
No LLM — pure file scanning. Returns a list of issue strings.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.shared.paths import FORMALIZATION_DIR
from lib.shared.common import find_asn, load_property_names, filename_to_label
from lib.formalization.core.build_dependency_graph import (
    find_property_table, parse_table_row, detect_columns,
)


def _normalize_label(label):
    """Normalize a table label to match filesystem conventions.

    T0(a) -> T0a, Def-Span -> Span, etc.
    """
    # Strip Def- prefix (definitions use bare name as filename)
    if label.startswith("Def-"):
        label = label[4:]
    # Remove parentheses: T0(a) -> T0a
    label = label.replace("(", "").replace(")", "")
    return label


def reconcile_table(asn_num):
    """Check _table.md consistency with property files.

    Returns list of issue strings (empty = all consistent).
    """
    _, asn_label = find_asn(str(asn_num))
    if asn_label is None:
        return [f"ASN-{asn_num:04d} not found"]

    prop_dir = FORMALIZATION_DIR / asn_label
    if not prop_dir.exists():
        return [f"No formalization directory for {asn_label}"]

    table_path = prop_dir / "_table.md"
    if not table_path.exists():
        return [f"No _table.md in {prop_dir}"]

    # --- Parse table ---
    table_text = table_path.read_text()
    table_rows = find_property_table(table_text)
    if table_rows is None:
        return [f"No property table found in _table.md"]

    data_rows = table_rows[2:]
    table_labels = set()
    norm_to_table = {}  # normalized -> original table label
    for row in data_rows:
        cells = parse_table_row(row)
        if len(cells) < 2:
            continue
        label = cells[0].strip().strip("`*")
        if label:
            table_labels.add(label)
            norm_to_table[_normalize_label(label)] = label

    # --- Scan property files ---
    _prop_names = load_property_names(prop_dir)
    file_labels = set()
    for f in sorted(prop_dir.glob("*.md")):
        if not f.name.startswith("_"):
            file_labels.add(filename_to_label(f.name, _prop_names))

    # --- Check correspondence (using normalized labels) ---
    norm_table = set(norm_to_table.keys())

    issues = []
    for label in sorted(file_labels - norm_table):
        issues.append(f"FILE_NO_ROW | {label}.md exists but no row in _table.md")

    for norm in sorted(norm_table - file_labels):
        orig = norm_to_table[norm]
        issues.append(f"ROW_NO_FILE | {orig} in _table.md but no {norm}.md file")

    return issues


def print_reconciliation(asn_num):
    """Run reconciliation and print results."""
    issues = reconcile_table(asn_num)
    _, asn_label = find_asn(str(asn_num))

    if not issues:
        print(f"  [RECONCILE] {asn_label} — clean", file=sys.stderr)
        return True

    print(f"  [RECONCILE] {asn_label} — {len(issues)} issues:",
          file=sys.stderr)
    for issue in issues:
        print(f"    {issue}", file=sys.stderr)
    return False
