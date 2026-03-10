"""Load foundation ASN statements for injection into prompts."""

import re
from pathlib import Path


def load_foundation_statements(foundation_path, statements_dir):
    """Read foundation.md, load each ASN's statements, return formatted text.

    Returns a string with one section per foundation ASN:
        ## Foundation: ASN-0001 (Tumbler Algebra)
        <statements>

        ## Foundation: ASN-0026 (I-Space and V-Space)
        <statements>

    Returns empty string if foundation_path doesn't exist or has no entries.
    """
    foundation_path = Path(foundation_path)
    statements_dir = Path(statements_dir)

    if not foundation_path.exists():
        return ""

    text = foundation_path.read_text()

    # Parse markdown table rows: | ASN-NNNN | Title |
    entries = []
    for line in text.splitlines():
        m = re.match(r"\|\s*(ASN-\d+)\s*\|\s*(.+?)\s*\|", line)
        if m:
            label, title = m.group(1), m.group(2)
            # Skip table header row
            if title.startswith("-") or title == "Title":
                continue
            entries.append((label, title))

    if not entries:
        return ""

    sections = []
    for label, title in entries:
        stmt_path = statements_dir / f"{label}-statements.md"
        if stmt_path.exists():
            content = stmt_path.read_text().strip()
            sections.append(
                f"## Foundation: {label} ({title})\n\n{content}"
            )

    return "\n\n".join(sections)
