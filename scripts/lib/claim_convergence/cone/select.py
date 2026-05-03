"""Cone auto-detection — heuristic to pick a cone needing focused review."""

import sys
from pathlib import Path
from typing import Optional, Tuple, List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.shared.paths import CLAIM_DIR, CLAIM_REVIEWS_DIR, LATTICE
from lib.shared.common import find_asn, build_label_index
from lib.lattice.labels import build_cross_asn_label_index
from lib.febe.session import open_session


def detect_dependency_cone(
    asn_num: int, window: int = 5, threshold: int = 3,
) -> Optional[Tuple[str, List[str]]]:
    """Detect a dependency cone from substrate review history.

    Looks at the last `window` review events for this ASN (review classifier
    links sorted by emission order). Counts active comment.revise links
    sourced from those reviews' finding documents, grouped by target claim.
    If one claim has >= `threshold` revise comments while its dependencies
    are stable (each <= half the apex's count), returns (apex_label, dep_labels).
    Otherwise returns None.
    """
    _, asn_label = find_asn(str(asn_num))
    if asn_label is None:
        return None

    claim_dir = CLAIM_DIR / asn_label
    if not claim_dir.exists():
        return None

    label_index_legacy = build_label_index(claim_dir)
    asn_labels = set(label_index_legacy.keys())

    reviews_prefix = str((CLAIM_REVIEWS_DIR / asn_label).relative_to(LATTICE))

    session = open_session(LATTICE)
    cross_index = build_cross_asn_label_index(session.store)
    addr_to_label = {addr: label for label, addr in cross_index.items()}

    # Reviews scoped to this ASN's review dir
    scoped_reviews = []
    for r in session.find_links(type_="review"):
        if not r.to_set:
            continue
        target_addr = r.to_set[0]
        target_path = session.get_path_for_addr(target_addr)
        if target_path and target_path.startswith(reviews_prefix):
            scoped_reviews.append(r)

    # LinkStore preserves emission order, so reversed = newest first
    scoped_reviews = list(reversed(scoped_reviews))
    recent = scoped_reviews[:window]
    if len(recent) < threshold:
        return None

    # Collect review-N stems from the window. The review classifier link
    # targets `_docuverse/documents/review/claims/<asn>/review-N.md`; per-
    # finding docs sit under `_docuverse/documents/finding/claims/<asn>/
    # review-N/<n>.md` and pair with their aggregate by the shared stem.
    recent_stems = set()
    for r in recent:
        target_addr = r.to_set[0]
        target_path = session.get_path_for_addr(target_addr)
        if target_path:
            stem = Path(target_path).stem
            if stem.startswith("review-"):
                recent_stems.add(stem)

    revise_counts = {}
    for link in session.active_links("comment.revise"):
        if not link.from_set or not link.to_set:
            continue
        src_addr = link.from_set[0]
        src_path = session.get_path_for_addr(src_addr)
        if src_path is None:
            continue
        src_parent = Path(src_path).parent.name
        if src_parent not in recent_stems:
            continue
        claim_label = addr_to_label.get(link.to_set[0])
        if claim_label in asn_labels:
            revise_counts[claim_label] = revise_counts.get(claim_label, 0) + 1

    if not revise_counts:
        return None

    apex = max(revise_counts, key=revise_counts.get)
    apex_count = revise_counts[apex]
    if apex_count < threshold:
        return None

    apex_addr = cross_index.get(apex)
    if apex_addr is None:
        return None
    cites = session.active_links("citation.depends", from_set=[apex_addr])
    dep_labels = [
        addr_to_label[link.to_set[0]]
        for link in cites
        if link.to_set
        and addr_to_label.get(link.to_set[0]) in asn_labels
    ]

    max_dep = max((revise_counts.get(d, 0) for d in dep_labels), default=0)
    if max_dep > apex_count // 2:
        return None

    return (apex, dep_labels)
