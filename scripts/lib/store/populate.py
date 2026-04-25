"""Populate the link store's structural layer from claim YAML/MD artifacts.

Imports claim classifier, contract.<kind> classifier, and citation links by
walking every ASN under the formalization directory. Idempotent: re-runs
add only newly-discovered links.

Reviews, comments, resolutions, finding documents, and rationales are
explicitly out of scope at this step. They start accumulating from the
live-write wrappers in step 5.
"""

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import FORMALIZATION_DIR, WORKSPACE


def populate_structural(store, formalization_dir=None):
    """Walk every ASN and ensure structural links exist in the store.

    Returns a stats dict:
        claims_seen, claims_added, contracts_added,
        citations_seen, citations_added, unresolved_labels
    """
    formalization_dir = Path(formalization_dir) if formalization_dir else FORMALIZATION_DIR
    label_index = build_cross_asn_label_index(formalization_dir)

    stats = {
        "claims_seen": 0,
        "claims_added": 0,
        "contracts_added": 0,
        "citations_seen": 0,
        "citations_added": 0,
        "unresolved_labels": [],
    }

    for asn_dir in sorted(p for p in formalization_dir.iterdir() if p.is_dir()):
        for yaml_path in sorted(asn_dir.glob("*.yaml")):
            if yaml_path.name.startswith("_"):
                continue
            counts = import_one_claim(store, yaml_path, label_index)
            stats["claims_seen"] += 1
            stats["claims_added"] += counts["claim"]
            stats["contracts_added"] += counts["contract"]
            stats["citations_seen"] += counts["citations_seen"]
            stats["citations_added"] += counts["citation"]
            stats["unresolved_labels"].extend(counts["unresolved"])

    return stats


def build_cross_asn_label_index(formalization_dir=None):
    """Return {label: repo-relative md path} across every ASN.

    Skips underscore-prefixed yaml files. Cross-ASN dependencies in
    the lattice use bare labels — no ASN prefix — so a flat index works.
    """
    formalization_dir = Path(formalization_dir) if formalization_dir else FORMALIZATION_DIR
    index = {}
    for asn_dir in sorted(p for p in formalization_dir.iterdir() if p.is_dir()):
        for yaml_path in sorted(asn_dir.glob("*.yaml")):
            if yaml_path.name.startswith("_"):
                continue
            with open(yaml_path) as f:
                data = yaml.safe_load(f)
            if not data or "label" not in data:
                continue
            md_path = yaml_path.with_suffix(".md")
            index[data["label"]] = _repo_relative(md_path)
    return index


def import_one_claim(store, yaml_path, label_index):
    """Ensure claim/contract/citation links exist for one yaml file."""
    yaml_path = Path(yaml_path)
    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    if not data or "label" not in data:
        return _empty_counts()

    md_rel = _repo_relative(yaml_path.with_suffix(".md"))
    counts = _empty_counts()

    _, created = _ensure_link(store, [], [md_rel], ["claim"])
    counts["claim"] = int(created)

    contract_kind = data.get("type")
    if contract_kind:
        _, created = _ensure_link(
            store, [], [md_rel], [f"contract.{contract_kind}"],
        )
        counts["contract"] = int(created)

    for dep_label in data.get("depends", []) or []:
        counts["citations_seen"] += 1
        dep_path = label_index.get(dep_label)
        if dep_path is None:
            counts["unresolved"].append((data["label"], dep_label))
            continue
        _, created = _ensure_link(store, [md_rel], [dep_path], ["citation"])
        counts["citation"] += int(created)

    return counts


def _ensure_link(store, from_set, to_set, type_set):
    """Idempotent make_link: returns (link_id, created_bool).

    `find_links` returns the superset of links whose endpoints intersect
    `from_set`/`to_set`. We then filter to exact-set equality so a citation
    A→[B,C] doesn't match a query for A→B alone.
    """
    candidates = store.find_links(
        from_set=from_set if from_set else None,
        to_set=to_set if to_set else None,
        type_set=type_set,
    )
    for link in candidates:
        if (link["from_set"] == from_set
                and link["to_set"] == to_set
                and link["type_set"] == type_set):
            return link["id"], False

    link_id = store.make_link(
        from_set=from_set, to_set=to_set, type_set=type_set,
    )
    return link_id, True


def _empty_counts():
    return {
        "claim": 0,
        "contract": 0,
        "citation": 0,
        "citations_seen": 0,
        "unresolved": [],
    }


def _repo_relative(path):
    return str(Path(path).resolve().relative_to(Path(WORKSPACE).resolve()))
