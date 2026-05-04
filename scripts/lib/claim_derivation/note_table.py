"""Parsers for the "Claims Introduced" markdown table in note files.

Notes carry a markdown table listing the claims they introduce. Claim
derivation reads this table to populate per-claim metadata (Name
column, etc.) before claims become first-class substrate documents.

The table layout varies by note: 3 columns (Label | Statement | Status),
4 columns adding Name or Type, or 5 columns with both. The Status
column is always last regardless of column count.
"""

import re


def find_claim_table(text):
    """Find the Claims Introduced table in note text.

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

    rows = []
    for i in range(table_start, len(lines)):
        line = lines[i].strip()
        if not line.startswith("|"):
            break
        rows.append(line)

    return rows


def parse_table_row(row):
    """Parse a markdown table row into cells, stripping whitespace."""
    parts = row.split("|")
    return [p.strip() for p in parts[1:-1]]


def detect_columns(header_cells):
    """Detect column layout from header.

    Returns a dict mapping role -> column index. Handles 3-column
    (Label | Statement | Status), 4-column with Name or Type, and
    5-column with both Name and Type. The "status" index is -1 (always
    last cell) so rows with pipes inside the Statement column still
    resolve correctly.
    """
    cols = {"label": 0, "status": -1}
    for i, cell in enumerate(header_cells):
        lower = cell.strip().lower()
        if lower == "name":
            cols["name"] = i
        elif lower == "type":
            cols["type"] = i
    return cols
