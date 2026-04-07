"""Name column population — extract PascalCase names from prose headers.

Blueprinting step: populates the Name column in the property table
after format normalization ensures headers are PascalCase.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.common import find_asn


def _extract_header_names(text, labels):
    """Extract PascalCase names from prose headers.

    Handles:
      **T1 (LexicographicOrder).**  -> T1: LexicographicOrder
      **Definition (TumblerAddition).**  -> TumblerAddition: TumblerAddition
      **T7 — SubspaceDisjointness.**  -> T7: SubspaceDisjointness

    Returns dict of label -> PascalCase name.
    """
    names = {}
    for label in labels:
        # **LABEL (Name).** format
        m = re.search(
            r'\*\*' + re.escape(label) + r'\s*\(([^)]+)\)\.\*\*', text)
        if m:
            names[label] = m.group(1).strip()
            continue

        # **LABEL — Name.** format
        m = re.search(
            r'\*\*' + re.escape(label) + r'\s*[\u2014\u2013-]\s*([^.*]+)\.\*\*', text)
        if m:
            names[label] = m.group(1).strip()
            continue

        # **Definition (Label).** or **Definition — Label.** — label IS the name
        def_patterns = [
            re.compile(r'\*\*Definition\s*\(' + re.escape(label) + r'\)\.\*\*'),
            re.compile(r'\*\*Definition\s*[\u2014\u2013-]\s*' + re.escape(label) + r'\.\*\*'),
        ]
        if any(p.search(text) for p in def_patterns):
            names[label] = label

    return names


def step_populate_names(asn_num):
    """Add Name column and populate from PascalCase prose headers. Mechanical.

    Runs after format normalization (which ensures headers are PascalCase).
    Skips if the Name column already exists and all cells are populated.
    Returns True on success.
    """
    from lib.formalization.core.build_dependency_graph import find_property_table, parse_table_row, detect_columns

    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return True

    text = asn_path.read_text()
    rows = find_property_table(text)
    if rows is None:
        return True

    header = parse_table_row(rows[0])
    cols = detect_columns(header)
    has_name = "name" in cols
    data_rows = rows[2:]

    # Collect labels
    labels = []
    for row in data_rows:
        cells = parse_table_row(row)
        if len(cells) < 2:
            continue
        label = cells[0].strip().strip("`*")
        if label:
            labels.append(label)

    if not labels:
        return True

    # Check if already fully populated
    if has_name:
        all_populated = True
        for row in data_rows:
            cells = parse_table_row(row)
            if len(cells) < 2:
                continue
            label = cells[0].strip().strip("`*")
            if not label:
                continue
            if cols["name"] >= len(cells) or not cells[cols["name"]].strip():
                all_populated = False
                break
        if all_populated:
            print(f"  [NAMES] Already populated \u2014 skipping", file=sys.stderr)
            return True

    # Extract names from prose headers
    names = _extract_header_names(text, labels)

    populated = len(names)
    missing = len(labels) - populated
    if missing:
        print(f"  [NAMES] {populated}/{len(labels)} names from headers, "
              f"{missing} without headers", file=sys.stderr)

    # Rewrite the table in the ASN text
    lines = text.split("\n")
    table_start = None
    for i, line in enumerate(lines):
        if re.match(r"\|\s*Label\s*\|", line):
            table_start = i
            break

    if table_start is None:
        return True

    new_lines = list(lines)

    if has_name:
        # Name column exists — populate empty cells
        name_idx = cols["name"]
        for i in range(table_start + 2, len(new_lines)):
            line = new_lines[i]
            if not line.strip().startswith("|"):
                break
            parts = line.split("|")
            if len(parts) < 3:
                continue
            label = parts[1].strip().strip("`*")
            if not label:
                continue
            # name_idx is 0-based from parse_table_row, but parts is 1-based
            part_idx = name_idx + 1
            if part_idx < len(parts) and not parts[part_idx].strip():
                name = names.get(label, "")
                if name:
                    parts[part_idx] = f" {name} "
                    new_lines[i] = "|".join(parts)
    else:
        # Add Name column after Label
        header_line = new_lines[table_start]
        parts = header_line.split("|")
        new_lines[table_start] = "|".join(parts[:2] + [" Name "] + parts[2:])

        sep_line = new_lines[table_start + 1]
        sep_parts = sep_line.split("|")
        new_lines[table_start + 1] = "|".join(
            sep_parts[:2] + ["------"] + sep_parts[2:])

        for i in range(table_start + 2, len(new_lines)):
            line = new_lines[i]
            if not line.strip().startswith("|"):
                break
            parts = line.split("|")
            if len(parts) < 3:
                continue
            label = parts[1].strip().strip("`*")
            name = names.get(label, "")
            new_lines[i] = "|".join(
                parts[:2] + [f" {name} " if name else " "] + parts[2:])

    new_text = "\n".join(new_lines)
    if new_text != text:
        asn_path.write_text(new_text)
        action = "populated" if has_name else "added"
        print(f"  [NAMES] Column {action} ({populated} names)",
              file=sys.stderr)
    else:
        print(f"  [NAMES] No changes needed", file=sys.stderr)

    return True
