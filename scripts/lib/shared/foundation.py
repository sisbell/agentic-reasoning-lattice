"""Load foundation ASN statements for injection into prompts.

Reads directly from per-property YAML (summary) + .md (formal contract)
files. No dependency on pre-built export files.
"""

import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import WORKSPACE, FORMALIZATION_DIR, PROJECT_MODEL_DIR, load_manifest
from lib.shared.common import build_label_index, load_property_metadata


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


def _extract_formal_contract(md_text):
    """Extract *Formal Contract:* section from .md text."""
    marker = "*Formal Contract:*"
    idx = md_text.find(marker)
    if idx == -1:
        return ""
    return md_text[idx:].strip()


def _load_property_statement(dep_asn_num, label):
    """Load one property's foundation statement from per-property files.

    Returns formatted section text or None if not found.
    """
    asn_label = f"ASN-{int(dep_asn_num):04d}"
    prop_dir = FORMALIZATION_DIR / asn_label
    if not prop_dir.exists():
        return None

    meta = load_property_metadata(prop_dir, label=label)
    if not meta or not meta.get("summary"):
        return None

    label_index = build_label_index(prop_dir)
    stem = label_index.get(label)
    if not stem:
        return None

    md_path = prop_dir / f"{stem}.md"
    if not md_path.exists():
        return None

    contract = _extract_formal_contract(md_path.read_text())
    name = meta.get("name", label)
    summary = meta["summary"]

    section = f"## {label} — {name}\n\n{summary}"
    if contract:
        section += f"\n\n{contract}"
    return section


def _dep_ids_with_extensions(asn_id):
    """Get all dependency ASN IDs including extensions."""
    manifest = load_manifest(asn_id)
    dep_ids = manifest.get("depends", [])
    all_ids = []
    for dep_id in dep_ids:
        all_ids.append(dep_id)
        for ext_id in find_extensions(dep_id):
            if ext_id != asn_id:
                all_ids.append(ext_id)
    return all_ids


def load_foundation_statements(asn_id):
    """Load all foundation statements from per-property files.

    Reads YAML summaries + .md formal contracts for every property
    in each dependency ASN. Errors if summaries are missing.
    """
    all_dep_ids = _dep_ids_with_extensions(asn_id)
    if not all_dep_ids:
        return ""

    sections = []
    for dep_id in all_dep_ids:
        asn_label = f"ASN-{int(dep_id):04d}"
        prop_dir = FORMALIZATION_DIR / asn_label
        if not prop_dir.exists():
            print(f"  [ERROR] No formalization dir for {asn_label}",
                  file=sys.stderr)
            continue

        all_meta = load_property_metadata(prop_dir)
        if not all_meta:
            print(f"  [ERROR] No property metadata for {asn_label}",
                  file=sys.stderr)
            continue

        missing = [l for l, m in all_meta.items() if not m.get("summary")]
        if missing:
            print(f"  [ERROR] {asn_label} missing summaries for "
                  f"{len(missing)} properties — "
                  f"run: python scripts/summarize.py {dep_id}",
                  file=sys.stderr)
            sys.exit(1)

        for label in all_meta:
            stmt = _load_property_statement(dep_id, label)
            if stmt:
                sections.append(stmt)

    return "\n\n---\n\n".join(sections)


def load_foundation_for_labels(asn_id, labels):
    """Load foundation statements for specific labels from per-property files.

    Reads YAML summary + .md formal contract for each label.
    Warns if a label is not found in any dependency ASN.
    """
    if not labels:
        return ""

    all_dep_ids = _dep_ids_with_extensions(asn_id)
    if not all_dep_ids:
        return ""

    sections = []
    for label in labels:
        found = False
        for dep_id in all_dep_ids:
            stmt = _load_property_statement(dep_id, label)
            if stmt:
                sections.append(stmt)
                found = True
                break
        if not found:
            print(f"  [WARNING] Foundation label '{label}' not found — "
                  f"run: python scripts/summarize.py on dependency",
                  file=sys.stderr)

    return "\n\n---\n\n".join(sections)
