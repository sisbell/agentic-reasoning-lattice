"""Load foundation ASN statements for injection into prompts."""

import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from paths import PROJECT_MODEL_DIR, asn_dir, formal_stmts, load_manifest


def find_extensions(base_id):
    """Find all ASNs that extend a given base ASN.

    Scans project model manifests for extends: <base_id> and returns
    their ASN IDs sorted numerically.
    """
    if not PROJECT_MODEL_DIR.exists():
        return []

    extensions = []
    for path in sorted(PROJECT_MODEL_DIR.glob("ASN-*/project.yaml")):
        try:
            with open(path) as f:
                m_data = yaml.safe_load(f) or {}
        except (FileNotFoundError, yaml.YAMLError):
            continue

        if m_data.get("extends") == base_id:
            m = re.match(r"ASN-(\d+)", path.parent.name)
            if m:
                extensions.append(int(m.group(1)))

    return sorted(extensions)


def load_foundation_statements(asn_id):
    """Load formal statements for an ASN's dependencies.

    Reads the ASN's depends field from its manifest, then loads formal
    statements for each dependency. Extensions (ASNs with extends: <dep>)
    are automatically bundled with their base ASN.
    """
    manifest = load_manifest(asn_id)
    dep_ids = manifest.get("depends", [])
    if not dep_ids:
        return ""

    sections = []
    for dep_id in dep_ids:
        # Load base dependency
        dep_manifest = load_manifest(dep_id)
        title = dep_manifest.get("title", "")
        label = f"ASN-{int(dep_id):04d}"
        stmt_path = formal_stmts(dep_id)
        if stmt_path.exists():
            content = stmt_path.read_text().strip()
            sections.append(
                f"## Foundation: {label} ({title})\n\n{content}"
            )
        else:
            print(f"  [ERROR] Dependency {label} has no formal statements — "
                  f"run: python scripts/export.py {dep_id}",
                  file=sys.stderr)
            sys.exit(1)

        # Load extensions of this dependency
        for ext_id in find_extensions(dep_id):
            # Don't include self as own extension
            if ext_id == asn_id:
                continue
            ext_manifest = load_manifest(ext_id)
            ext_title = ext_manifest.get("title", "")
            ext_label = f"ASN-{int(ext_id):04d}"
            ext_path = formal_stmts(ext_id)
            if ext_path.exists():
                ext_content = ext_path.read_text().strip()
                sections.append(
                    f"## Foundation: {ext_label} ({ext_title}, extends {label})\n\n{ext_content}"
                )

    return "\n\n".join(sections)
