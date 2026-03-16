"""Load foundation ASN statements for injection into prompts."""

import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from paths import PROJECT_MODEL_DIR, load_manifest


def load_foundation_statements(foundation_path, statements_dir, asn_id=None):
    """Load formal statements for an ASN's dependencies.

    Reads the ASN's depends field from its manifest, then loads formal
    statements for each dependency. A dependency's statements are loaded
    if the statements file exists — no other gate.

    If asn_id is None, falls back to loading statements for all ASNs
    that have statements files (backward compatibility).

    foundation_path is ignored — kept for backward compatibility.
    """
    statements_dir = Path(statements_dir)

    if asn_id is not None:
        manifest = load_manifest(asn_id)
        dep_ids = manifest.get("depends", [])
        if not dep_ids:
            return ""

        sections = []
        for dep_id in dep_ids:
            dep_manifest = load_manifest(dep_id)
            title = dep_manifest.get("title", "")
            label = f"ASN-{int(dep_id):04d}"
            stmt_path = statements_dir / f"{label}-statements.md"
            if stmt_path.exists():
                content = stmt_path.read_text().strip()
                sections.append(
                    f"## Foundation: {label} ({title})\n\n{content}"
                )
            else:
                print(f"  [ERROR] Dependency {label} has no formal statements — "
                      f"run modeling pipeline for {label} first",
                      file=sys.stderr)
                sys.exit(1)

        return "\n\n".join(sections)

    # Fallback: load all ASNs that have statements files
    if not PROJECT_MODEL_DIR.exists():
        return ""

    sections = []
    for path in sorted(PROJECT_MODEL_DIR.glob("ASN-*.yaml")):
        try:
            with open(path) as f:
                m_data = yaml.safe_load(f) or {}
        except (FileNotFoundError, yaml.YAMLError):
            continue

        m = re.match(r"ASN-(\d+)", path.stem)
        if not m:
            continue

        label = f"ASN-{int(m.group(1)):04d}"
        title = m_data.get("title", "")
        stmt_path = statements_dir / f"{label}-statements.md"
        if stmt_path.exists():
            sections.append(
                f"## Foundation: {label} ({title})\n\n{stmt_path.read_text().strip()}"
            )

    return "\n\n".join(sections)
