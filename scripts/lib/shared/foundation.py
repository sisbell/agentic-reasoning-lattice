"""Load foundation ASN statements for injection into prompts.

Reads metadata via `load_claim_metadata` (substrate-sourced — name from
the substrate name link, summary from the description sidecar) and the
Formal Contract section from each claim's .md.
"""

import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import WORKSPACE, CLAIM_CONVERGENCE_DIR, MANIFESTS_DIR, load_manifest
from lib.shared.common import build_label_index, load_claim_metadata


def find_extensions(base_id):
    """Find all ASNs that extend a given base ASN.

    Scans project model manifests for extends: <base_id> and returns
    their ASN IDs sorted numerically.
    """
    if not MANIFESTS_DIR.exists():
        return []

    extensions = []
    for path in sorted(MANIFESTS_DIR.glob("ASN-*/note.yaml")):
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


def _load_claim_statement(dep_asn_num, label):
    """Load one claim's foundation statement from per-claim files.

    Returns formatted section text or None if not found.
    """
    asn_label = f"ASN-{int(dep_asn_num):04d}"
    claim_dir = CLAIM_CONVERGENCE_DIR / asn_label
    if not claim_dir.exists():
        return None

    meta = load_claim_metadata(claim_dir, label=label)
    if not meta or not meta.get("summary"):
        return None

    label_index = build_label_index(claim_dir)
    stem = label_index.get(label)
    if not stem:
        return None

    md_path = claim_dir / f"{stem}.md"
    if not md_path.exists():
        return None

    contract = _extract_formal_contract(md_path.read_text())
    name = meta.get("name", label)
    summary = meta["summary"]

    section = f"## {label} — {name}\n\n{summary}"
    if contract:
        section += f"\n\n{contract}"
    return section


def _dep_ids_with_extensions(asn_id, dep_ids=None):
    """Get all dependency ASN IDs including extensions.

    If `dep_ids` is provided (e.g., sourced from substrate citations on
    a note), it overrides the manifest depends: read.
    """
    if dep_ids is None:
        manifest = load_manifest(asn_id)
        dep_ids = manifest.get("depends", [])
    all_ids = []
    for dep_id in dep_ids:
        all_ids.append(dep_id)
        for ext_id in find_extensions(dep_id):
            if ext_id != asn_id:
                all_ids.append(ext_id)
    return all_ids


def load_foundation_statements(asn_id, dep_ids=None):
    """Load all foundation statements from per-claim files.

    Reads substrate-sourced summaries (description sidecars) + .md
    formal contracts for every claim in each dependency ASN. Errors if
    summaries are missing.

    `dep_ids` overrides the manifest `depends:` read — note-side
    callers pass substrate-derived ids via `note_dep_asn_ids`; claim-side
    callers omit and the manifest is consulted (legacy path).
    """
    all_dep_ids = _dep_ids_with_extensions(asn_id, dep_ids=dep_ids)
    if not all_dep_ids:
        return ""

    sections = []
    for dep_id in all_dep_ids:
        asn_label = f"ASN-{int(dep_id):04d}"
        claim_dir = CLAIM_CONVERGENCE_DIR / asn_label
        if not claim_dir.exists():
            print(f"  [ERROR] No claim-convergence dir for {asn_label}",
                  file=sys.stderr)
            continue

        all_meta = load_claim_metadata(claim_dir)
        if not all_meta:
            print(f"  [ERROR] No claim metadata for {asn_label}",
                  file=sys.stderr)
            continue

        missing = [l for l, m in all_meta.items() if not m.get("summary")]
        if missing:
            print(f"  [ERROR] {asn_label} missing summaries for "
                  f"{len(missing)} claims — "
                  f"run: python scripts/summarize.py {dep_id}",
                  file=sys.stderr)
            sys.exit(1)

        for label in all_meta:
            stmt = _load_claim_statement(dep_id, label)
            if stmt:
                sections.append(stmt)

    return "\n\n---\n\n".join(sections)


def load_foundation_for_note(asn_path, asn_id):
    """Load foundation statements for a note, sourcing dep ASN ids from
    substrate citations on the note md.

    Wraps the substrate query so callers don't repeat the boilerplate.
    Falls back to an empty list (no foundation) if the note has no
    citations — distinct from the manifest path, which would also use
    the manifest's depends declaration.
    """
    from lib.store.populate import note_dep_asn_ids
    from lib.store.store import default_store
    note_rel = str(asn_path.resolve().relative_to(Path(WORKSPACE).resolve()))
    with default_store() as store:
        dep_ids = note_dep_asn_ids(store, note_rel)
    return load_foundation_statements(asn_id, dep_ids=dep_ids)


def load_foundation_for_claim_asn(asn_id):
    """Load foundation statements for a claim ASN, sourcing dep ASN ids
    from per-claim substrate citations aggregated up to ASN granularity.

    Parallels `load_foundation_for_note`. The claim-side aggregation is
    the union of cross-ASN citations sourced from any claim md in this
    ASN's claim-convergence directory.
    """
    from lib.store.populate import aggregate_asn_deps
    from lib.store.store import default_store
    asn_label = f"ASN-{int(asn_id):04d}"
    with default_store() as store:
        dep_ids = aggregate_asn_deps(store, asn_label)
    return load_foundation_statements(asn_id, dep_ids=dep_ids)


def claim_asn_dep_ids(asn_id):
    """Substrate-aggregated dep ASN ids for a claim ASN.

    Standalone form for callers that need the dep id list without the
    full foundation text (e.g., load_foundation_for_labels which takes
    labels separately).
    """
    from lib.store.populate import aggregate_asn_deps
    from lib.store.store import default_store
    asn_label = f"ASN-{int(asn_id):04d}"
    with default_store() as store:
        return aggregate_asn_deps(store, asn_label)


def load_foundation_for_labels(asn_id, labels, dep_ids=None):
    """Load foundation statements for specific labels from per-claim files.

    Reads the substrate-sourced summary + .md formal contract for each
    label. Warns if a label is not found in any dependency ASN.

    `dep_ids` override behaves the same as in `load_foundation_statements`.
    """
    if not labels:
        return ""

    all_dep_ids = _dep_ids_with_extensions(asn_id, dep_ids=dep_ids)
    if not all_dep_ids:
        return ""

    sections = []
    for label in labels:
        found = False
        for dep_id in all_dep_ids:
            stmt = _load_claim_statement(dep_id, label)
            if stmt:
                sections.append(stmt)
                found = True
                break
        if not found:
            print(f"  [WARNING] Foundation label '{label}' not found — "
                  f"run: python scripts/summarize.py on dependency",
                  file=sys.stderr)

    return "\n\n---\n\n".join(sections)
