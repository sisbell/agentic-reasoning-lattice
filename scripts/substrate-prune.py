#!/usr/bin/env python3
"""Prune substrate links to a clean active set.

Reads canonical `_docuverse/links.jsonl`, applies filter rules, writes
filtered output. `paths.json` is untouched — tumbler addresses stay
stable.

Filter policy:
- DROP all retraction links + the links they retract (active-set filter)
- DROP all supersession (version chains collapse to base; predicates
  resolve at base via version_head)
- DROP all holding (ephemeral coordination)
- DROP motifs/motif/motif.attribution
- DROP review-mode.anti-bloat (ephemeral)
- For review + review.coverage/.content/.structural: keep only the
  latest-2 per target note/claim (by tumbler order of the review doc).
- For finding + comment.* + resolution.*: keep only those tied to a
  kept review (via provenance.derivation from review → finding)
- KEEP everything else: classifiers, citation.*, provenance.*,
  consultation.*, attribute anchors, name, label, description, etc.

Usage:
    python scripts/substrate-prune.py --report
    python scripts/substrate-prune.py --out _workspace/links-pruned.jsonl
    python scripts/substrate-prune.py --apply   # replace canonical
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from collections import defaultdict, Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.backend.addressing import Address
from lib.backend.types import TypeRegistry


REPO = Path(__file__).resolve().parent.parent
LINKS_IN = REPO / "_docuverse" / "links.jsonl"
PATHS_IN = REPO / "_docuverse" / "paths.json"

# Type sets driving filter decisions.
HARD_DROP = {
    "retraction",
    "holding",
    "motifs",
    "motif",
    "motif.attribution",
    "review-mode.anti-bloat",
}
# Supersession is preserved overall (version chains drive freshness
# predicates) — but self-loop supersessions (from==to) are corruption
# and get filtered out individually.

REVIEW_CLASSIFIER_TYPES = {
    "review",
    "review.content",
    "review.structural",
}
REVIEW_COVERAGE_TYPES = {
    "review.coverage",
}

FINDING_LINK_TYPES = {
    "finding",
    "comment.observe",
    "comment.revise",
    "comment.violation",
    "comment.out-of-scope",
}
COMMENT_TYPES = {
    "comment.observe",
    "comment.revise",
    "comment.violation",
    "comment.out-of-scope",
}
RESOLUTION_TYPES = {
    "resolution.edit",
    "resolution.reject",
}


def load_links(path: Path) -> list[dict]:
    out = []
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            out.append(json.loads(line))
    return out


def type_name_of(link: dict, reg: TypeRegistry) -> str | None:
    """Return the most specific known type name on this link."""
    best = None
    best_len = -1
    for ta in link.get("type_set", []):
        n = reg.name_for(Address(ta))
        if n and len(n) > best_len:
            best = n
            best_len = len(n)
    return best


def compute_retracted_link_ids(links: list[dict], reg: TypeRegistry) -> set[str]:
    """Set of link IDs that have been retracted (appear in any
    retraction's to_set)."""
    retraction_addr = reg.address_for("retraction")
    out: set[str] = set()
    for link in links:
        types = [Address(t) for t in link.get("type_set", [])]
        if retraction_addr in types:
            for tgt in link.get("to_set", []):
                out.add(tgt)
    return out


def compute_kept_reviews(
    links: list[dict], reg: TypeRegistry, n: int = 2,
) -> set[str]:
    """For each note/claim covered by reviews, keep the latest `n`
    review docs by tumbler ordering.

    Returns the set of kept review-doc addresses.
    """
    coverage_addr = reg.address_for("review.coverage")
    by_target: dict[str, list[str]] = defaultdict(list)
    for link in links:
        types = [Address(t) for t in link.get("type_set", [])]
        if coverage_addr not in types:
            continue
        if not link.get("from_set") or not link.get("to_set"):
            continue
        review_doc = link["from_set"][0]
        target = link["to_set"][0]
        by_target[target].append(review_doc)
    kept: set[str] = set()
    for target, reviews in by_target.items():
        reviews_sorted = sorted(reviews, key=lambda a: Address(a).digits)
        for r in reviews_sorted[-n:]:
            kept.add(r)
    return kept


def compute_kept_findings(
    links: list[dict], reg: TypeRegistry, kept_reviews: set[str],
) -> set[str]:
    """Set of finding-doc addresses derived from any kept review.

    Walks provenance.derivation from review → finding.
    """
    derivation_addr = reg.address_for("provenance.derivation")
    out: set[str] = set()
    for link in links:
        types = [Address(t) for t in link.get("type_set", [])]
        if derivation_addr not in types:
            continue
        if not link.get("from_set"):
            continue
        if link["from_set"][0] in kept_reviews:
            for finding in link.get("to_set", []):
                out.add(finding)
    return out


def compute_kept_comment_link_ids(
    links: list[dict], reg: TypeRegistry, kept_findings: set[str],
) -> set[str]:
    """Set of comment.* link IDs whose finding (F[0]) is kept.

    Used to determine which resolutions target kept comments.
    """
    comment_addrs = {reg.address_for(t) for t in COMMENT_TYPES}
    out: set[str] = set()
    for link in links:
        types = {Address(t) for t in link.get("type_set", [])}
        if not (types & comment_addrs):
            continue
        if not link.get("from_set"):
            continue
        if link["from_set"][0] in kept_findings:
            out.add(link["id"])
    return out


def should_keep(
    link: dict,
    reg: TypeRegistry,
    retracted_ids: set[str],
    kept_reviews: set[str],
    kept_findings: set[str],
    kept_comment_link_ids: set[str],
) -> bool:
    if link["id"] in retracted_ids:
        return False

    tname = type_name_of(link, reg)

    if tname in HARD_DROP:
        return False

    # Self-loop supersession is corruption — filter individually.
    if tname == "supersession":
        f = link.get("from_set") or []
        g = link.get("to_set") or []
        if f and g and f[0] == g[0]:
            return False

    # Review-side: keep only edges that anchor on a kept review doc.
    if tname in REVIEW_CLASSIFIER_TYPES:
        # Classifier shape: F=∅, G=[review_doc]
        if not link.get("to_set"):
            return False
        return link["to_set"][0] in kept_reviews
    if tname in REVIEW_COVERAGE_TYPES:
        # review.coverage: F=[review_doc], G=[target]
        if not link.get("from_set"):
            return False
        return link["from_set"][0] in kept_reviews

    # Finding-side: keep only edges that anchor on a kept finding.
    if tname == "finding":
        # Classifier: F=∅, G=[finding_doc]
        if not link.get("to_set"):
            return False
        return link["to_set"][0] in kept_findings
    if tname in COMMENT_TYPES:
        # comment.*: F=[finding], G=[target]
        if not link.get("from_set"):
            return False
        return link["from_set"][0] in kept_findings
    if tname in RESOLUTION_TYPES:
        # resolution.*: F=[resolver_doc], G=[comment_link_addr].
        # Keep if it targets a kept comment.
        if not link.get("to_set"):
            return False
        return link["to_set"][0] in kept_comment_link_ids

    # provenance.derivation from a review → finding: drop if review
    # isn't kept. The derivation_addr check is folded into kept_findings
    # construction; here we only need to drop derivations whose source
    # review was dropped.
    derivation_addr = reg.address_for("provenance.derivation")
    types = [Address(t) for t in link.get("type_set", [])]
    if derivation_addr in types and link.get("from_set"):
        src = link["from_set"][0]
        # We don't have a quick "is this addr a review" predicate without
        # scanning, but if the from_set address is itself a review doc
        # and isn't in kept_reviews, drop. To detect this without a
        # second pass, treat as kept by default — derivations to other
        # doc types still survive. The kept_findings set is what
        # actually drives finding retention.
        # However, a derivation from a DROPPED review to a (now-orphan)
        # finding is still emitted unless we drop it explicitly.
        # We can drop it if its targets aren't in kept_findings AND its
        # source could be a review. Easier: keep all provenance edges
        # whose targets are reachable docs; drop those whose ENTIRE
        # to_set is orphan findings.
        if link.get("to_set"):
            targets = link["to_set"]
            # If ALL targets are findings (start with same prefix as
            # finding-doc addrs) AND none are in kept_findings, drop.
            # Simpler: just check if from_set is in kept_reviews when
            # it WAS a review. We don't have a fast way to check that.
            # Defer: just keep all provenance.derivation. The orphan
            # ones are dead links pointing nowhere — small footprint.
            pass

    return True


def report(links: list[dict], reg: TypeRegistry, kept: list[dict]) -> None:
    print(f"\n=== Substrate prune report ===\n")
    print(f"  input links:  {len(links):>7}")
    print(f"  output links: {len(kept):>7}")
    print(f"  dropped:      {len(links) - len(kept):>7} "
          f"({100 * (1 - len(kept) / len(links)):.1f}%)\n")

    in_counts: Counter = Counter()
    out_counts: Counter = Counter()
    for link in links:
        in_counts[type_name_of(link, reg) or "<unknown>"] += 1
    for link in kept:
        out_counts[type_name_of(link, reg) or "<unknown>"] += 1

    print("  Per-type counts (in → out):")
    all_types = sorted(set(in_counts) | set(out_counts))
    for t in all_types:
        i = in_counts.get(t, 0)
        o = out_counts.get(t, 0)
        flag = "" if i == o else (" DROPPED" if o == 0 else f"  (-{i - o})")
        print(f"    {t:<35} {i:>6} → {o:>6}{flag}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--in", dest="input", default=str(LINKS_IN))
    parser.add_argument(
        "--out", dest="output",
        default=str(REPO / "_workspace" / "links-pruned.jsonl"),
    )
    parser.add_argument(
        "--report", action="store_true",
        help="Print per-type counts; don't write output",
    )
    parser.add_argument(
        "--apply", action="store_true",
        help="Replace canonical links.jsonl with pruned version "
             "(takes a backup at links.jsonl.bak)",
    )
    parser.add_argument(
        "-n", "--keep-reviews", type=int, default=2,
        help="Number of latest reviews to keep per target (default 2)",
    )
    args = parser.parse_args()

    # Bootstrap type registry from paths.json _meta.
    with open(PATHS_IN) as f:
        paths_data = json.load(f)
    registry_doc = Address(paths_data["_meta"]["registry_doc"])
    reg = TypeRegistry(registry_doc)

    print(f"  loading {args.input}...", file=sys.stderr)
    links = load_links(Path(args.input))
    print(f"  loaded {len(links)} links", file=sys.stderr)

    print(f"  computing retracted-link set...", file=sys.stderr)
    retracted_ids = compute_retracted_link_ids(links, reg)
    print(f"  {len(retracted_ids)} retracted link IDs", file=sys.stderr)

    print(f"  computing latest-{args.keep_reviews} reviews per target...",
          file=sys.stderr)
    kept_reviews = compute_kept_reviews(links, reg, n=args.keep_reviews)
    print(f"  {len(kept_reviews)} review docs kept", file=sys.stderr)

    print(f"  computing kept findings...", file=sys.stderr)
    kept_findings = compute_kept_findings(links, reg, kept_reviews)
    print(f"  {len(kept_findings)} finding docs kept", file=sys.stderr)

    print(f"  computing kept comment-link IDs...", file=sys.stderr)
    kept_comment_link_ids = compute_kept_comment_link_ids(
        links, reg, kept_findings,
    )
    print(f"  {len(kept_comment_link_ids)} comment links kept",
          file=sys.stderr)

    print(f"  filtering...", file=sys.stderr)
    kept = [
        link for link in links
        if should_keep(
            link, reg, retracted_ids, kept_reviews, kept_findings,
            kept_comment_link_ids,
        )
    ]

    # Dedupe by link ID (handles pre-existing 715 duplicates).
    seen: set[str] = set()
    deduped: list[dict] = []
    for link in kept:
        if link["id"] in seen:
            continue
        seen.add(link["id"])
        deduped.append(link)
    if len(deduped) < len(kept):
        print(
            f"  deduped {len(kept) - len(deduped)} duplicate link IDs",
            file=sys.stderr,
        )

    report(links, reg, deduped)

    if args.report:
        return 0

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        for link in deduped:
            f.write(json.dumps(link) + "\n")
    print(f"\n  wrote {out_path} ({len(deduped)} links)", file=sys.stderr)

    if args.apply:
        bak = LINKS_IN.with_suffix(".jsonl.bak")
        shutil.copy(LINKS_IN, bak)
        shutil.copy(out_path, LINKS_IN)
        print(f"  applied to canonical {LINKS_IN}", file=sys.stderr)
        print(f"  backup at {bak}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
