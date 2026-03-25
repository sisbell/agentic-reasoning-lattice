#!/usr/bin/env python3
"""
Generate property dependency YAML from an ASN's property table.

Parses the "Properties Introduced" table in the ASN reasoning doc,
extracting labels, types, and declared dependencies from the Status column.
Produces a structured YAML file alongside the ASN's formal statements export.

Usage:
    python scripts/lib/rebase_deps.py 43          # generate deps YAML
    python scripts/lib/rebase_deps.py 43 --dry-run # parse and print, don't write
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from paths import WORKSPACE, STATEMENTS_DIR, load_manifest
from lib.common import find_asn


# ---------------------------------------------------------------------------
# Property table parser
# ---------------------------------------------------------------------------

def find_property_table(text):
    """Find the Properties Introduced table in the ASN text.

    Returns the lines of the table (header + separator + data rows),
    or None if not found.
    """
    lines = text.split("\n")
    table_start = None

    for i, line in enumerate(lines):
        if re.match(r"\|\s*Label\s*\|", line):
            table_start = i
            break

    if table_start is None:
        return None

    # Collect rows: header, separator, then data rows until non-table line
    rows = []
    for i in range(table_start, len(lines)):
        line = lines[i].strip()
        if not line.startswith("|"):
            break
        rows.append(line)

    return rows


def parse_table_row(row):
    """Parse a markdown table row into cells, stripping whitespace."""
    # Split on | and drop the empty strings from leading/trailing |
    parts = row.split("|")
    # parts[0] is empty (before first |), parts[-1] is empty (after last |)
    return [p.strip() for p in parts[1:-1]]


def detect_columns(header_cells):
    """Detect column layout from header.

    Returns a dict mapping role -> column index.
    Handles 3-column (Label|Statement|Status) and 4-column (Label|Type|Statement|Status).
    The "status" index is -1 meaning "always last cell" to handle rows where
    pipes in the Statement column create extra cells.
    """
    cols = {}
    cols["label"] = 0  # Always first
    cols["status"] = -1  # Always last

    has_type = any(c.strip().lower() == "type" for c in header_cells)
    if has_type:
        cols["type"] = 1

    return cols


# ---------------------------------------------------------------------------
# Status column parser
# ---------------------------------------------------------------------------

def parse_status(status_text):
    """Parse a Status column value into structured dependency info.

    Returns a dict with:
        kind: str  — "introduced", "corollary", "from", "theorem", "extends",
                     "consistent", "design", "cited"
        labels: list[str]  — foundation/local labels referenced
        asn_refs: list[int]  — ASN numbers referenced
        extends: dict|None  — {label, name, asn} if extends pattern found
        parallels: dict|None  — {label, asn} if parallels pattern found
    """
    status = status_text.strip()
    result = {
        "kind": "introduced",
        "labels": [],
        "asn_refs": [],
        "extends": None,
        "parallels": None,
    }

    if not status or status == "introduced":
        return result

    # "design requirement"
    if status.startswith("design"):
        result["kind"] = "design"
        return result

    # "cited" or "cited (ASN-NNNN)"
    if status.startswith("cited"):
        result["kind"] = "cited"
        m = re.search(r"ASN-(\d{4})", status)
        if m:
            result["asn_refs"] = [int(m.group(1))]
        return result

    # "consistent with LABELS (description)"
    if status.startswith("consistent"):
        result["kind"] = "consistent"
        labels, asns = _extract_labels_and_asns(status)
        result["labels"] = labels
        result["asn_refs"] = asns
        return result

    # "extends LABEL (Name, ASN-NNNN) ..."
    m = re.match(r"extends\s+(\S+)\s*\(([^,]+),\s*ASN-(\d{4})\)", status)
    if m:
        result["kind"] = "extends"
        result["extends"] = {
            "label": m.group(1),
            "name": m.group(2).strip(),
            "asn": int(m.group(3)),
        }
        # Also extract labels from the "via ..." part
        via_part = status[m.end():]
        labels, asns = _extract_labels_and_asns(via_part)
        result["labels"] = labels
        result["asn_refs"] = list(set([int(m.group(3))] + asns))
        return result

    # "corollary of LABEL" or "corollary from LABEL1, LABEL2, ..."
    if status.startswith("corollary"):
        result["kind"] = "corollary"
        labels, asns = _extract_labels_and_asns(status)
        result["labels"] = labels
        result["asn_refs"] = asns
        return result

    # "theorem from LABELS" or "from LABELS"
    if status.startswith("theorem") or status.startswith("from"):
        result["kind"] = "theorem" if status.startswith("theorem") else "from"
        labels, asns = _extract_labels_and_asns(status)
        result["labels"] = labels
        result["asn_refs"] = asns
        return result

    # Fallback: try to extract any labels
    labels, asns = _extract_labels_and_asns(status)
    if labels:
        result["kind"] = "other"
        result["labels"] = labels
        result["asn_refs"] = asns

    return result


def _extract_labels_and_asns(text):
    """Extract property labels and ASN references from text.

    Labels are patterns like T1, T10a, TA5(c), S7b, S8-fin, D-CTG-depth,
    PrefixSpanCoverage, etc.

    Returns (labels, asn_refs).
    """
    # Extract ASN references
    asn_refs = [int(m.group(1)) for m in re.finditer(r"ASN-(\d{4})", text)]

    # Extract labels: uppercase letter(s) followed by digits, optional suffix
    # Handles: T1, T10a, TA5, TA5(c), T0(a), S7b, S8-fin, D-CTG, D-CTG-depth,
    #          PrefixSpanCoverage, ValidInsertionPosition, etc.
    label_pattern = re.compile(
        r'([A-Z][A-Za-z0-9]*(?:[-][A-Za-z0-9]+)*(?:\([a-z]\))?)'
    )

    # Remove ASN references and common words before scanning
    cleaned = re.sub(r'ASN-\d{4}', '', text)
    cleaned = re.sub(r'\b(corollary|from|of|theorem|via|beyond|extends|consistent|with|witness|construction|design|requirement|cited)\b',
                     '', cleaned, flags=re.IGNORECASE)

    labels = []
    for m in label_pattern.finditer(cleaned):
        label = m.group(1)
        # Filter out common words that look like labels
        if label in ("I", "A", "E", "N", "In", "The", "For", "By", "If", "No",
                      "INV", "DEF", "LEMMA", "META", "PRE", "POST", "FRAME",
                      "Type", "Status", "Label", "Statement"):
            continue
        labels.append(label)

    return labels, asn_refs


# ---------------------------------------------------------------------------
# Statement column parser (for extends/parallels in ASN-0043 style)
# ---------------------------------------------------------------------------

def parse_statement_for_relations(statement_text):
    """Extract extends/parallels claims from the Statement column text.

    Some ASNs put cross-ASN relationships in the Statement rather than Status.
    E.g., "extends S4 (OriginBasedIdentity, ASN-0036) beyond I-addresses via ..."
    """
    relations = {}

    # "extends LABEL (Name, ASN-NNNN)"
    m = re.search(r"extends\s+(\S+)\s*\(([^,]+),\s*ASN-(\d{4})\)", statement_text)
    if m:
        relations["extends"] = {
            "label": m.group(1),
            "name": m.group(2).strip(),
            "asn": int(m.group(3)),
        }

    # "parallels LABEL" or "parallels LABEL (ASN-NNNN)" or "analog of LABEL"
    m = re.search(r"(?:parallels|analog of)\s+(\S+)(?:\s*\(ASN-(\d{4})\))?", statement_text)
    if m:
        relations["parallels"] = {
            "label": m.group(1),
            "asn": int(m.group(2)) if m.group(2) else None,
        }

    # "via LABEL1, LABEL2, ... (ASN-NNNN)" — additional deps in statement
    via_match = re.search(r"via\s+(.+?)(?:\(ASN-(\d{4})\))?$", statement_text)
    if via_match:
        labels, asns = _extract_labels_and_asns(via_match.group(0))
        if labels:
            relations["via_labels"] = labels
            relations["via_asns"] = asns

    return relations


# ---------------------------------------------------------------------------
# Main: generate deps YAML
# ---------------------------------------------------------------------------

def generate_deps(asn_num):
    """Parse the ASN property table and generate structured dependency data.

    Returns a dict suitable for YAML serialization, or None on failure.
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  [ERROR] ASN-{asn_num:04d} not found", file=sys.stderr)
        return None

    text = asn_path.read_text()
    table_rows = find_property_table(text)
    if table_rows is None:
        print(f"  [ERROR] No property table found in {asn_path.name}", file=sys.stderr)
        return None

    # Parse header
    header_cells = parse_table_row(table_rows[0])
    cols = detect_columns(header_cells)

    # Skip separator row (row 1)
    data_rows = table_rows[2:]

    # Get manifest for ASN-level depends
    manifest = load_manifest(asn_num)
    depends = manifest.get("depends", [])

    # Parse each property row
    has_type = "type" in cols
    properties = {}
    for row in data_rows:
        cells = parse_table_row(row)
        if len(cells) < 2:
            continue

        label = cells[0].strip()
        if not label:
            continue

        # Clean label: remove backticks, formatting
        label = label.strip("`").strip("*").strip()

        # Status is always the last cell
        status_text = cells[-1].strip()

        # Type is second cell if present
        type_text = cells[1].strip() if has_type and len(cells) > 2 else ""

        # Statement is everything between label (and type if present) and status
        stmt_start = 2 if has_type else 1
        stmt_end = -1  # exclude status
        statement_text = "|".join(cells[stmt_start:stmt_end]).strip() if len(cells) > 2 else ""

        # Parse status for dependencies
        status_info = parse_status(status_text)

        # Parse statement for extends/parallels
        stmt_relations = parse_statement_for_relations(statement_text)

        # Build property entry
        prop = {"status": status_info["kind"]}

        if type_text:
            prop["type"] = type_text

        if status_info["labels"]:
            prop["follows_from"] = status_info["labels"]

        if status_info["asn_refs"]:
            prop["follows_from_asns"] = sorted(set(status_info["asn_refs"]))

        # Merge extends/parallels from Status and Statement
        extends = status_info.get("extends") or stmt_relations.get("extends")
        if extends:
            prop["extends"] = extends

        parallels = status_info.get("parallels") or stmt_relations.get("parallels")
        if parallels:
            prop["parallels"] = parallels

        # Additional via labels from statement
        if "via_labels" in stmt_relations:
            existing = prop.get("follows_from", [])
            prop["follows_from"] = list(dict.fromkeys(existing + stmt_relations["via_labels"]))
        if "via_asns" in stmt_relations:
            existing = prop.get("follows_from_asns", [])
            prop["follows_from_asns"] = sorted(set(existing + stmt_relations["via_asns"]))

        properties[label] = prop

    return {
        "asn": asn_num,
        "depends": depends,
        "properties": properties,
    }


def write_deps_yaml(asn_num, deps_data):
    """Write deps YAML to the export directory."""
    output_path = STATEMENTS_DIR / f"ASN-{asn_num:04d}-deps.yaml"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        yaml.dump(deps_data, f, default_flow_style=False, sort_keys=False,
                  allow_unicode=True, width=120)

    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate property dependency YAML")
    parser.add_argument("asn", help="ASN number (e.g., 43)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Parse and print, don't write")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    deps = generate_deps(asn_num)

    if deps is None:
        sys.exit(1)

    if args.dry_run:
        yaml.dump(deps, sys.stdout, default_flow_style=False, sort_keys=False,
                  allow_unicode=True, width=120)
        print(f"\n  [{len(deps['properties'])} properties parsed]", file=sys.stderr)
    else:
        path = write_deps_yaml(asn_num, deps)
        print(f"  [WROTE] {path.relative_to(WORKSPACE)}", file=sys.stderr)
        print(f"  [{len(deps['properties'])} properties]", file=sys.stderr)
        print(str(path))


if __name__ == "__main__":
    main()
