"""Cone scope helpers — transitive dep walk + cone content assembly."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.shared.paths import CLAIM_DIR
from lib.shared.common import build_label_index
from lib.store.queries import active_links


def assemble_cone(asn_label, apex_label, dep_labels):
    """Assemble just the cone claims for focused review.

    Returns concatenated text of apex + same-ASN dependency claims.
    """
    claim_dir = CLAIM_DIR / asn_label
    label_index = build_label_index(claim_dir)
    parts = []

    # Include dependencies first (context), then apex
    for label in dep_labels + [apex_label]:
        stem = label_index.get(label)
        if stem is None:
            continue
        md_path = claim_dir / f"{stem}.md"
        if md_path.exists():
            parts.append(md_path.read_text().strip())

    return "\n\n---\n\n".join(parts)


def transitive_same_asn_deps(store, apex_path, asn_labels, rev_index):
    """BFS through citation.depends from `apex_path`, returning the
    list of same-ASN labels reachable (excluding the apex itself).

    Walks only `citation.depends` (backward grounding); forward citations
    are deliberately not followed — the cone is the apex's grounding
    chain, not the downstream tree. Same-ASN only — cross-ASN deps are
    delivered separately via foundation_statements.
    """
    visited = {apex_path}
    queue = [apex_path]
    deps = []
    while queue:
        cur = queue.pop(0)
        for link in active_links(store, "citation.depends", from_set=[cur]):
            if not link["to_set"]:
                continue
            target = link["to_set"][0]
            if target in visited:
                continue
            visited.add(target)
            label = rev_index.get(target)
            if label and label in asn_labels:
                deps.append(label)
                queue.append(target)
    return deps
