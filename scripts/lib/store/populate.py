"""Populate the link store's structural layer from claim YAML/MD artifacts.

Imports claim classifier, contract.<kind> classifier, and citation links by
walking every ASN under the claim-convergence directory. Idempotent: re-runs
add only newly-discovered links.

Reviews, comments, resolutions, finding documents, and rationales are
explicitly out of scope at this step. They start accumulating from the
live-write wrappers in step 5.
"""

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import CLAIM_DIR, LATTICE


def populate_structural(store, claim_root_dir=None):
    """Walk every ASN and ensure structural links exist in the store.

    Returns a stats dict:
        claims_seen, claims_added, contracts_added,
        citations_seen, citations_added, unresolved_labels
    """
    claim_root_dir = Path(claim_root_dir) if claim_root_dir else CLAIM_DIR
    label_index = build_cross_asn_label_index(claim_root_dir)

    stats = {
        "claims_seen": 0,
        "claims_added": 0,
        "contracts_added": 0,
        "citations_seen": 0,
        "citations_added": 0,
        "unresolved_labels": [],
    }

    for asn_dir in sorted(p for p in claim_root_dir.iterdir() if p.is_dir()):
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


def build_cross_asn_label_index(claim_root_dir=None, store=None):
    """Return {label: lattice-relative md path} across every ASN.

    Sources from substrate `label` links when a `store` is provided —
    the canonical post-migration path. Falls back to walking `*.yaml`
    files when no store is given; that path exists for the bootstrap
    case (`populate_structural`), where the substrate has no label
    links yet because we are populating it for the first time.

    Cross-ASN dependencies in the lattice use bare labels — no ASN
    prefix — so a flat index works.
    """
    if store is not None:
        return _build_label_index_from_substrate(store)
    return _build_label_index_from_yaml(claim_root_dir)


def build_note_label_index(store):
    """Return {ASN-NNNN: repo-relative note md path} across every note.

    Sources from substrate `note` classifier links. Notes use their ASN
    label (e.g., "ASN-0009") as the citation target — there is no
    separate label primitive at note scale.
    """
    import re
    from lib.store.queries import active_links
    index = {}
    for link in active_links(store, "note"):
        if not link["to_set"]:
            continue
        note_path = link["to_set"][0]
        m = re.search(r"(ASN-\d+)", Path(note_path).name)
        if m:
            index[m.group(1)] = note_path
    return index


def is_note_path(doc_path):
    """True iff doc_path is under any lattice's substrate-managed note dir."""
    rel = str(doc_path)
    return "/_store/documents/note/" in rel or rel.startswith("_store/documents/note/")


def aggregate_asn_deps(store, asn_label, claim_root_dir=None):
    """Cross-ASN ASN ids derived from per-claim citations.

    Walks every claim md in `claim_root_dir/<asn_label>/`, reads
    the active citation links sourced from each, and extracts the
    target's ASN id from the cited claim's path. Self-references
    (within-ASN citations) are excluded — the aggregate is the set of
    ASNs this ASN depends on, not its internal graph.

    Returns sorted list of int ASN ids.
    """
    import re
    from lib.shared.paths import CLAIM_DIR
    from lib.store.queries import active_links

    cdir = Path(claim_root_dir) if claim_root_dir else CLAIM_DIR
    asn_dir = cdir / asn_label
    if not asn_dir.exists():
        return []

    workspace = Path(LATTICE).resolve()
    sidecar_suffixes = (".label.md", ".name.md", ".description.md")
    deps = set()
    for claim_md in asn_dir.glob("*.md"):
        if claim_md.name.startswith("_"):
            continue
        if claim_md.name.endswith(sidecar_suffixes):
            continue
        rel = str(claim_md.resolve().relative_to(workspace))
        for link in active_links(store, "citation", from_set=[rel]):
            if not link["to_set"]:
                continue
            to_path = link["to_set"][0]
            m = re.search(r"_store/documents/claim/(ASN-\d+)/", to_path)
            if m and m.group(1) != asn_label:
                deps.add(int(m.group(1).split("-")[1]))
    return sorted(deps)


def note_dep_asn_ids(store, note_md_path):
    """Return sorted ASN ids the note depends on, sourced from substrate
    citation links.

    Each citation is a substrate edge from the given note md to another
    note md. The dep ASN id is parsed from the target note's filename
    (ASN-NNNN-<slug>.md). Cross-stage citations (note → claim) are
    skipped — only note-to-note edges count as upstream foundation here.
    """
    import re
    from lib.store.queries import active_links
    note_rel = str(note_md_path)
    note_index_paths = set(build_note_label_index(store).values())
    ids = []
    for link in active_links(store, "citation", from_set=[note_rel]):
        if not link["to_set"]:
            continue
        to_path = link["to_set"][0]
        if to_path not in note_index_paths:
            continue
        m = re.search(r"ASN-(\d+)", Path(to_path).name)
        if m:
            ids.append(int(m.group(1)))
    return sorted(set(ids))


def build_doc_label_index(store, doc_path):
    """Return the label-to-doc index appropriate for `doc_path`.

    Note docs use ASN-NNNN as the citation target; claim docs use claim
    labels (T0, NAT-zero, ...). Callers pass the from-doc; this picks
    the matching index for `--to <label>` resolution.
    """
    if is_note_path(doc_path):
        return build_note_label_index(store)
    return build_cross_asn_label_index(store=store)


def _build_label_index_from_substrate(store):
    from lib.store.queries import active_links
    workspace = Path(LATTICE).resolve()
    index = {}
    for link in active_links(store, "label"):
        if not link["from_set"] or not link["to_set"]:
            continue
        md_path = link["from_set"][0]
        doc_path = link["to_set"][0]
        full = workspace / doc_path
        if not full.exists():
            continue
        first_line = full.read_text().strip().split("\n", 1)[0].strip()
        if first_line:
            index[first_line] = md_path
    return index


def _build_label_index_from_yaml(claim_root_dir=None):
    claim_root_dir = Path(claim_root_dir) if claim_root_dir else CLAIM_DIR
    index = {}
    for asn_dir in sorted(p for p in claim_root_dir.iterdir() if p.is_dir()):
        for yaml_path in sorted(asn_dir.glob("*.yaml")):
            if yaml_path.name.startswith("_"):
                continue
            with open(yaml_path) as f:
                data = yaml.safe_load(f)
            if not data or "label" not in data:
                continue
            md_path = yaml_path.with_suffix(".md")
            index[data["label"]] = _lattice_relative(md_path)
    return index


def import_one_claim(store, yaml_path, label_index):
    """Ensure claim/contract/citation links exist for one yaml file."""
    yaml_path = Path(yaml_path)
    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    if not data or "label" not in data:
        return _empty_counts()

    md_rel = _lattice_relative(yaml_path.with_suffix(".md"))
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


def _lattice_relative(path):
    return str(Path(path).resolve().relative_to(Path(LATTICE).resolve()))
