#!/usr/bin/env python3
"""Dump the note citation graph from the substrate.

Usage:
    python3 scripts/note-graph.py 9          # focus on ASN-0009
    python3 scripts/note-graph.py 9 --depth 2  # only 2 hops
    python3 scripts/note-graph.py --all       # full DAG dump

The substrate's `citation` links between notes form the dependency
graph. This tool reads those links and renders them in human-readable
form for inspection. Read-only — to modify the graph, run
convergence-link-cite.py / substrate/retract.py.
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from shared.paths import WORKSPACE
from store.populate import build_note_label_index
from store.queries import active_links
from store.store import Store


def asn_label(asn_arg):
    n = int(re.sub(r"[^0-9]", "", str(asn_arg)))
    return f"ASN-{n:04d}"


def build_edges(store):
    """Return list of (from_label, to_label) edges between notes only.

    Filters citation links to those whose endpoints are both classified
    notes. Cross-stage citations (note → claim) are skipped here — they
    belong to a different traversal.
    """
    note_index = build_note_label_index(store)
    path_to_label = {p: l for l, p in note_index.items()}

    edges = []
    for link in active_links(store, "citation.depends"):
        if not link["from_set"] or not link["to_set"]:
            continue
        src = link["from_set"][0]
        dst = link["to_set"][0]
        src_label = path_to_label.get(src)
        dst_label = path_to_label.get(dst)
        if src_label and dst_label:
            edges.append((src_label, dst_label))
    return note_index, edges


def cmd_focus(asn_label_str, depth, store):
    """Show ancestors and descendants of one note, up to `depth` hops."""
    note_index, edges = build_edges(store)
    if asn_label_str not in note_index:
        print(f"  {asn_label_str} not found in note classifier index",
              file=sys.stderr)
        print(f"  (run migration_tools/backfill-note-classifiers.py if missing)",
              file=sys.stderr)
        return 1

    # Forward adjacency: deps (this → that)
    fwd = {}
    # Reverse adjacency: dependents (that → this)
    rev = {}
    for src, dst in edges:
        fwd.setdefault(src, set()).add(dst)
        rev.setdefault(dst, set()).add(src)

    print(f"\n{asn_label_str} — {Path(note_index[asn_label_str]).name}")
    print()
    print("Depends on (ancestors):")
    _print_tree(asn_label_str, fwd, depth, indent=2)
    print()
    print("Depended on by (descendants):")
    _print_tree(asn_label_str, rev, depth, indent=2)
    return 0


def _print_tree(label, adjacency, depth, indent, seen=None):
    if seen is None:
        seen = set()
    if depth <= 0:
        return
    children = sorted(adjacency.get(label, set()))
    if not children:
        print(" " * indent + "(none)")
        return
    for child in children:
        marker = " (cycle)" if child in seen else ""
        print(" " * indent + f"- {child}{marker}")
        if child not in seen:
            _print_tree(child, adjacency, depth - 1, indent + 2,
                        seen | {label})


def cmd_all(store):
    """Print every note→note citation edge."""
    note_index, edges = build_edges(store)
    print(f"# Note citation graph — {len(note_index)} notes, "
          f"{len(edges)} edges")
    print()
    for src, dst in sorted(edges):
        print(f"  {src} → {dst}")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("asn", nargs="?",
                        help="ASN number (focus mode); omit with --all")
    parser.add_argument("--all", action="store_true",
                        help="Dump every edge (full DAG)")
    parser.add_argument("--depth", type=int, default=3,
                        help="Hops in focus mode (default 3)")
    args = parser.parse_args()

    if not args.all and not args.asn:
        parser.error("provide an ASN, or --all")

    with Store() as store:
        if args.all:
            return cmd_all(store)
        return cmd_focus(asn_label(args.asn), args.depth, store)


if __name__ == "__main__":
    sys.exit(main())
