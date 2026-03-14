"""Load foundation ASN statements for injection into prompts."""

import re
from pathlib import Path

import yaml

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from paths import PROJECT_MODEL_DIR


def load_foundation_statements(foundation_path, statements_dir):
    """Load formal statements for all foundation ASNs.

    Scans vault/project-model/ for ASNs with a 'covers' field (indicating
    foundation status), then loads their formal statements from statements_dir.

    foundation_path is ignored — kept for backward compatibility.
    """
    statements_dir = Path(statements_dir)

    if not PROJECT_MODEL_DIR.exists():
        return ""

    entries = []
    for path in sorted(PROJECT_MODEL_DIR.glob("ASN-*.yaml")):
        try:
            with open(path) as f:
                manifest = yaml.safe_load(f) or {}
        except (FileNotFoundError, yaml.YAMLError):
            continue

        if not manifest.get("covers"):
            continue

        m = re.match(r"ASN-(\d+)", path.stem)
        if m:
            label = f"ASN-{int(m.group(1)):04d}"
            title = manifest.get("title", "")
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
