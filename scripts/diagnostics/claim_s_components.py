#!/usr/bin/env python3
"""s-component analysis for an ASN's cone-set.

Diagnostic tool: reads the substrate, treats each ASN claim's cone
(claim ∪ same-ASN dependencies) as a hypergraph hyperedge, and computes
s-connected components for s in {1, 2, 3}.

s-connectivity (Aksoy et al. 2020): two hyperedges are s-adjacent iff
they share at least s nodes; an s-component is a maximal s-connected
set of hyperedges. At s=1 every hyperedge that shares any node is
adjacent; at higher s only deeply-overlapping hyperedges remain
connected.

Usage:
    python scripts/diagnostics/claim_s_components.py 34

Output:
    Markdown report at lattices/<lattice>/_workspace/s-components/<asn>.md
    Summary printed to stdout.
"""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.shared.paths import LATTICE, WORKSPACE_DIR
from lib.shared.common import find_asn
from lib.backend.store import Store
from lib.backend.predicates import active_links
from lib.predicates import is_doc_quiescent
from lib.lattice.labels import build_cross_asn_label_index


def build_cone_hypergraph(store, asn_label, label_index):
    """For each ASN claim, build its cone = {claim} ∪ same_asn_deps.

    Returns dict mapping claim label → frozenset of labels in the cone.
    """
    rev_index = {p: l for l, p in label_index.items()}
    asn_labels = {l for l, p in label_index.items() if asn_label in p}

    cones = {}
    for label in asn_labels:
        path = label_index[label]
        deps = set()
        for link in active_links(store, "citation.depends", from_set=[path]):
            if not link["to_set"]:
                continue
            dep_label = rev_index.get(link["to_set"][0])
            if dep_label and dep_label in asn_labels:
                deps.add(dep_label)
        cones[label] = frozenset({label} | deps)
    return cones


def compute_s_components(cones, s):
    """Compute s-connected components via union-find.

    Two cones are s-adjacent iff |cone(A) ∩ cone(B)| ≥ s.
    Returns list of components, each a list of apex labels, sorted by size desc.
    """
    apexes = list(cones.keys())
    parent = {a: a for a in apexes}

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for i, a in enumerate(apexes):
        for b in apexes[i + 1:]:
            if len(cones[a] & cones[b]) >= s:
                union(a, b)

    components = defaultdict(list)
    for a in apexes:
        components[find(a)].append(a)
    return sorted(
        (sorted(c) for c in components.values()),
        key=lambda c: (-len(c), c[0]),
    )


def claim_quiescent(store, label_index, label):
    md_path = label_index.get(label)
    if not md_path:
        return None
    return is_doc_quiescent(store, md_path)


def render_report(asn_label, cones, results, store, label_index):
    """Build the markdown report."""
    lines = [
        f"# s-component analysis — {asn_label}",
        "",
        f"**Cones (hyperedges):** {len(cones)}",
        "",
        "Each cone is the set `{claim} ∪ same_asn_deps(claim)`.",
        "Two cones are s-adjacent iff they share at least s claims.",
        "An s-component is a maximal s-connected set of cones.",
        "",
        "Reference: Aksoy et al. 2020, *Hypernetwork science via "
        "high-order hypergraph walks*. Implementation: union-find over "
        "the s-line graph.",
        "",
    ]

    for s in sorted(results.keys()):
        components = results[s]
        sizes = [len(c) for c in components]
        n_singletons = sum(1 for sz in sizes if sz == 1)

        lines.extend([
            f"## s = {s}",
            "",
            f"- **Components:** {len(components)}",
            f"- **Largest:** {max(sizes) if sizes else 0} cones",
            f"- **Singletons:** {n_singletons}",
            "",
        ])

        for i, members in enumerate(components, 1):
            shared_core = (
                frozenset.intersection(*[cones[m] for m in members])
                if members else frozenset()
            )
            quiescence = [
                (m, claim_quiescent(store, label_index, m))
                for m in members
            ]
            n_quiescent = sum(1 for _, c in quiescence if c)

            lines.append(f"### s={s} component {i} — size {len(members)}")
            lines.append("")
            lines.append(f"**Members ({len(members)}):** "
                         f"{', '.join(members)}")
            lines.append(f"**Shared core ({len(shared_core)}):** "
                         f"{', '.join(sorted(shared_core)) if shared_core else '—'}")
            lines.append(f"**Quiescence:** {n_quiescent}/{len(members)} "
                         f"doc-quiescent")
            lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    args = parser.parse_args()
    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    _, asn_label = find_asn(str(asn_num))
    if asn_label is None:
        print(f"ASN-{asn_num:04d} not found", file=sys.stderr)
        sys.exit(1)

    store = Store()
    label_index = build_cross_asn_label_index(store=store)
    cones = build_cone_hypergraph(store, asn_label, label_index)
    print(f"Built {len(cones)} cones for {asn_label}")

    results = {}
    for s in (1, 2, 3):
        components = compute_s_components(cones, s)
        results[s] = components
        sizes = [len(c) for c in components]
        top = sorted(sizes, reverse=True)[:5]
        n_singletons = sum(1 for sz in sizes if sz == 1)
        print(f"  s={s}: {len(components)} components "
              f"(top sizes: {top}, singletons: {n_singletons})")

    report = render_report(asn_label, cones, results, store, label_index)
    out_dir = WORKSPACE_DIR / "s-components"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{asn_label}.md"
    out_path.write_text(report)
    print(f"\nReport: {out_path.relative_to(LATTICE.parent.parent)}")


if __name__ == "__main__":
    main()
