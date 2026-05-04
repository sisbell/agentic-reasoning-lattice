"""Markdown frontmatter helpers — `---\\n<yaml>\\n---\\n<body>` round-trip.

Used by inquiry/campaign descriptor docs that carry a YAML header.
"""

from pathlib import Path

import yaml


def _parse_frontmatter(text):
    """Parse `---\\n<yaml>\\n---\\n<body>`.

    Returns (frontmatter_dict, body_str). If the text doesn't start with
    `---`, returns ({}, text) — treats the whole thing as body.
    """
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return {}, text
    rest = text.split("---\n", 2)
    if len(rest) < 3:
        return {}, text
    _, fm_text, body = rest
    fm = yaml.safe_load(fm_text) or {}
    if not isinstance(fm, dict):
        return {}, text
    return fm, body.lstrip("\n")


def write_frontmatter(fm, body=""):
    """Format `---\\n<yaml>\\n---\\n<body>` text. Inverse of _parse_frontmatter."""
    fm_text = yaml.safe_dump(
        fm, default_flow_style=False, sort_keys=False, allow_unicode=True,
    )
    if body and not body.endswith("\n"):
        body = body + "\n"
    return f"---\n{fm_text}---\n\n{body}"


def read_doc_frontmatter(path):
    """Read frontmatter dict from a markdown doc. Returns {} on missing
    file or malformed frontmatter."""
    try:
        text = Path(path).read_text()
    except FileNotFoundError:
        return {}
    fm, _ = _parse_frontmatter(text)
    return fm
