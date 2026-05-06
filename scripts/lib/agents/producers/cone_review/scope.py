"""Cone scope helpers — transitive dep walk + cone content assembly."""

import sys
from pathlib import Path
from typing import Dict, List, Set

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.shared.paths import CLAIM_DIR
from lib.shared.claim_files import build_label_index
from lib.backend.addressing import Address
from lib.protocols.febe.protocol import Session


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


def transitive_same_asn_deps(
    session: Session,
    apex_addr: Address,
    asn_labels: Set[str],
    rev_index: Dict[Address, str],
) -> List[str]:
    """BFS through citation.depends from `apex_addr`, returning the
    list of same-ASN labels reachable (excluding the apex itself).

    Walks only `citation.depends` (backward grounding); forward citations
    are deliberately not followed — the cone is the apex's grounding
    chain, not the downstream tree. Same-ASN only — cross-ASN deps are
    delivered separately via foundation_statements.

    `rev_index` maps tumbler addresses → label strings.
    """
    visited = {apex_addr}
    queue = [apex_addr]
    deps: List[str] = []
    while queue:
        cur = queue.pop(0)
        for link in session.active_links("citation.depends", from_set=[cur]):
            for target in link.to_set:
                if target in visited:
                    continue
                visited.add(target)
                label = rev_index.get(target)
                if label and label in asn_labels:
                    deps.append(label)
                    queue.append(target)
    return deps


def cross_asn_deps_in_cone(
    session: Session,
    cone_labels: List[str],
    label_index: Dict[str, Address],
    rev_index: Dict[Address, str],
    asn_labels: Set[str],
) -> List[str]:
    """Cross-ASN deps cited by anything in the cone.

    Used to narrow the foundation context loaded for the reviewer
    prompt: only deps that live outside this ASN need explicit
    foundation loading; same-ASN deps are already in `cone_labels`.

    Walks `citation.depends` from each cone member; collects every
    dep whose label resolves outside `asn_labels` (the set of labels
    in the apex's ASN). Preserves first-seen order; deduplicates.
    """
    cross: List[str] = []
    for label in cone_labels:
        from_addr = label_index.get(label)
        if from_addr is None:
            continue
        for link in session.active_links(
            "citation.depends", from_set=[from_addr],
        ):
            for cited in link.to_set:
                dep_label = rev_index.get(cited)
                if (
                    dep_label
                    and dep_label not in asn_labels
                    and dep_label not in cross
                ):
                    cross.append(dep_label)
    return cross
