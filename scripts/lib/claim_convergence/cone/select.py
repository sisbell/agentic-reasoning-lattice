"""Cone auto-detection — heuristic to pick a cone needing focused review."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.shared.paths import CLAIM_DIR, CLAIM_REVIEWS_DIR, LATTICE
from lib.shared.common import find_asn, build_label_index
from lib.store.populate import build_cross_asn_label_index
from lib.store.queries import active_links
from lib.store.store import Store


def detect_dependency_cone(asn_num, window=5, threshold=3):
    """Detect a dependency cone from substrate review history.

    Looks at the last `window` review events for this ASN (review classifier
    links sorted by timestamp). Counts active comment.revise links sourced
    from those reviews' finding documents, grouped by target claim. If one
    claim has >= `threshold` revise comments while its dependencies are
    stable (each <= half the apex's count), returns (apex_label, dep_labels).
    Otherwise returns None.
    """
    _, asn_label = find_asn(str(asn_num))
    if asn_label is None:
        return None

    claim_dir = CLAIM_DIR / asn_label
    if not claim_dir.exists():
        return None

    label_index = build_label_index(claim_dir)
    asn_labels = set(label_index.keys())

    reviews_prefix = str((CLAIM_REVIEWS_DIR / asn_label).relative_to(LATTICE))

    store = Store()
    try:
        scoped_reviews = []
        for r in store.find_links(type_set=["review"]):
            if not r["to_set"]:
                continue
            target = r["to_set"][0]
            if target.startswith(reviews_prefix):
                scoped_reviews.append(r)

        scoped_reviews.sort(key=lambda r: r["ts"], reverse=True)
        recent = scoped_reviews[:window]
        if len(recent) < threshold:
            return None

        # Collect review-N stems from the window. The review classifier link
        # targets `_docuverse/documents/review/claims/<asn>/review-N.md`; per-
        # finding docs sit under `_docuverse/documents/finding/claims/<asn>/
        # review-N/<n>.md` and pair with their aggregate by the shared stem.
        recent_stems = set()
        for r in recent:
            target_path = Path(r["to_set"][0])
            stem = target_path.stem
            if stem.startswith("review-"):
                recent_stems.add(stem)

        cross_index = build_cross_asn_label_index(store=store)
        path_to_label = {p: l for l, p in cross_index.items()}

        revise_counts = {}
        for link in active_links(store, "comment.revise"):
            if not link["from_set"] or not link["to_set"]:
                continue
            src_parent = Path(link["from_set"][0]).parent.name
            if src_parent not in recent_stems:
                continue
            claim_label = path_to_label.get(link["to_set"][0])
            if claim_label in asn_labels:
                revise_counts[claim_label] = revise_counts.get(claim_label, 0) + 1

        if not revise_counts:
            return None

        apex = max(revise_counts, key=revise_counts.get)
        apex_count = revise_counts[apex]
        if apex_count < threshold:
            return None

        apex_path = cross_index.get(apex)
        if not apex_path:
            return None
        cites = active_links(store, "citation.depends", from_set=[apex_path])
        dep_labels = [
            path_to_label[link["to_set"][0]]
            for link in cites
            if link["to_set"]
            and path_to_label.get(link["to_set"][0]) in asn_labels
        ]

        max_dep = max((revise_counts.get(d, 0) for d in dep_labels), default=0)
        if max_dep > apex_count // 2:
            return None

        return (apex, dep_labels)
    finally:
        store.close()
