#!/usr/bin/env python3
"""One-shot migration: relocate findings + review docs into _docuverse.

Closes the substrate-citizenship gap between two doc types that the
convergence protocols already classify (`review` link on aggregate
review docs; `comment.<kind>` relation pinning per-finding docs) yet
which sit outside `_docuverse/documents/`:

    _workspace/findings/claims/ASN-NNNN/review-N/*.md
        → _docuverse/documents/finding/claims/ASN-NNNN/review-N/*.md
    _workspace/findings/notes/ASN-NNNN/review-N/*.md
        → _docuverse/documents/finding/notes/ASN-NNNN/review-N/*.md
    claim-convergence/ASN-NNNN/reviews/review-N.md
        → _docuverse/documents/review/claims/ASN-NNNN/review-N.md
    discovery/review/ASN-NNNN/...
        → _docuverse/documents/review/notes/ASN-NNNN/...

After moving the files, this script:
  - Rewrites every matching path-string in the substrate JSONL via
    the existing `migrate_paths` machinery.
  - Backfills a `finding` classifier on each per-finding doc.
  - Backfills a `provenance.derivation` link from each aggregate review
    doc to each per-finding doc that came from it (path-token pairing:
    `…/review-N.md` aggregates `…/review-N/*.md` findings).
  - Rebuilds the SQLite index from the rewritten JSONL.

Idempotent: re-running on a migrated lattice is a no-op. File moves
skip when the destination already exists; substrate path migration is
already idempotent (no matching prefixes → no rewrites); classifier and
provenance emits are idempotent (return existed=False on re-run).

Usage:
    LATTICE=xanadu    python scripts/migration_tools/migrate-findings-and-reviews.py
    LATTICE=xanadu    python scripts/migration_tools/migrate-findings-and-reviews.py --dry-run
    LATTICE=materials python scripts/migration_tools/migrate-findings-and-reviews.py

Caller responsibility: run inside a clean working tree (or stage to a
single commit afterward), since this script moves many files. The new
paths inherit per-file history through git's rename detection.
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from shared.paths import (
    LATTICE, LATTICE_NAME, DOCUVERSE_LOG, DOCUVERSE_DOCS_DIR,
    WORKSPACE_DIR, CLAIM_CONVERGENCE_DIR,
)
from shared.migrate_substrate_paths import migrate_paths
from store.emit import emit_derivation, emit_finding
from store.store import Store


ASN_RE = re.compile(r"^ASN-(\d+)$")
REVIEW_MD_RE = re.compile(r"^review-\d+\.md$")
REVIEW_DIR_RE = re.compile(r"^review-\d+$")


def _findings_moves(workspace_findings_root, kind):
    """Yield (src_dir, dst_dir) tuples for one ASN's per-review subdirs.

    workspace_findings_root: e.g. _workspace/findings/claims
    kind: "claims" or "notes" (just used to build the dst)
    """
    if not workspace_findings_root.exists():
        return
    dst_root = DOCUVERSE_DOCS_DIR / "finding" / kind
    for asn_dir in sorted(workspace_findings_root.iterdir()):
        if not asn_dir.is_dir() or not ASN_RE.match(asn_dir.name):
            continue
        for review_dir in sorted(asn_dir.iterdir()):
            if not review_dir.is_dir() or not REVIEW_DIR_RE.match(review_dir.name):
                continue
            yield (review_dir, dst_root / asn_dir.name / review_dir.name)


def _claim_review_moves():
    """Yield (src_md, dst_md) for each per-ASN aggregate review file under
    claim-convergence/ASN-NNNN/reviews/review-N.md.
    """
    if not CLAIM_CONVERGENCE_DIR.exists():
        return
    dst_root = DOCUVERSE_DOCS_DIR / "review" / "claims"
    for asn_dir in sorted(CLAIM_CONVERGENCE_DIR.iterdir()):
        if not asn_dir.is_dir() or not ASN_RE.match(asn_dir.name):
            continue
        reviews_dir = asn_dir / "reviews"
        if not reviews_dir.is_dir():
            continue
        for review_md in sorted(reviews_dir.iterdir()):
            if not review_md.is_file() or not REVIEW_MD_RE.match(review_md.name):
                continue
            yield (review_md, dst_root / asn_dir.name / review_md.name)


def _note_review_moves():
    """Yield (src_md, dst_md) for each per-ASN note-side review file under
    discovery/review/ASN-NNNN/*.md.
    """
    src_root = LATTICE / "discovery" / "review"
    if not src_root.exists():
        return
    dst_root = DOCUVERSE_DOCS_DIR / "review" / "notes"
    for asn_dir in sorted(src_root.iterdir()):
        if not asn_dir.is_dir() or not ASN_RE.match(asn_dir.name):
            continue
        for f in sorted(asn_dir.iterdir()):
            if not f.is_file() or not f.name.endswith(".md"):
                continue
            yield (f, dst_root / asn_dir.name / f.name)


def _move_file(src, dst, dry_run):
    if dst.exists():
        return False  # already migrated
    if dry_run:
        return True
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dst))
    return True


def _move_dir(src, dst, dry_run):
    """Move every file under `src` into `dst`. Skip files already at `dst`."""
    moved = 0
    for f in sorted(src.rglob("*")):
        if not f.is_file():
            continue
        rel = f.relative_to(src)
        target = dst / rel
        if target.exists():
            continue
        if dry_run:
            moved += 1
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(f), str(target))
        moved += 1
    # Try to remove now-empty source dir tree (only outside dry_run).
    if not dry_run:
        for d in sorted(src.rglob("*"), reverse=True):
            if d.is_dir():
                try:
                    d.rmdir()
                except OSError:
                    pass
        try:
            src.rmdir()
        except OSError:
            pass
    return moved


def _path_substitutions():
    """Build the substrate-path prefix substitutions.

    The two _workspace/findings/* and discovery/review/ prefixes are
    flat; claim-convergence/ASN-NNNN/reviews/ is per-ASN, so we
    enumerate the ASN dirs that exist on disk.
    """
    subs = {
        "_workspace/findings/claims/": "_docuverse/documents/finding/claims/",
        "_workspace/findings/notes/":  "_docuverse/documents/finding/notes/",
        "discovery/review/":           "_docuverse/documents/review/notes/",
    }
    if CLAIM_CONVERGENCE_DIR.exists():
        for asn_dir in sorted(CLAIM_CONVERGENCE_DIR.iterdir()):
            if not asn_dir.is_dir() or not ASN_RE.match(asn_dir.name):
                continue
            old = f"claim-convergence/{asn_dir.name}/reviews/"
            new = f"_docuverse/documents/review/claims/{asn_dir.name}/"
            subs[old] = new
    return subs


def _backfill_finding_classifiers(dry_run):
    """Walk _docuverse/documents/finding/ and emit `finding` classifier per doc."""
    finding_root = DOCUVERSE_DOCS_DIR / "finding"
    if not finding_root.exists():
        return 0, 0
    created = 0
    existed = 0
    if dry_run:
        # Just count target files; no substrate read.
        return sum(1 for _ in finding_root.rglob("*.md")), 0
    with Store() as store:
        for f in sorted(finding_root.rglob("*.md")):
            if not f.is_file():
                continue
            _id, was_created = emit_finding(store, f)
            if was_created:
                created += 1
            else:
                existed += 1
    return created, existed


def _backfill_provenance(dry_run):
    """Pair each aggregate review doc with its per-finding docs by the
    matching `review-N` path token, emitting a `provenance.derivation`
    from aggregate to each finding.
    """
    review_root = DOCUVERSE_DOCS_DIR / "review"
    finding_root = DOCUVERSE_DOCS_DIR / "finding"
    if not review_root.exists() or not finding_root.exists():
        return 0, 0
    created = 0
    existed = 0

    pairs = []
    for kind in ("claims", "notes"):
        rev_kind = review_root / kind
        find_kind = finding_root / kind
        if not rev_kind.exists():
            continue
        for asn_dir in sorted(rev_kind.iterdir()):
            if not asn_dir.is_dir() or not ASN_RE.match(asn_dir.name):
                continue
            for aggregate_md in sorted(asn_dir.iterdir()):
                if not aggregate_md.is_file() or not REVIEW_MD_RE.match(aggregate_md.name):
                    continue
                stem = aggregate_md.stem  # "review-N"
                finding_dir = find_kind / asn_dir.name / stem
                if not finding_dir.is_dir():
                    continue
                for finding_md in sorted(finding_dir.iterdir()):
                    if (finding_md.is_file()
                            and finding_md.suffix == ".md"
                            and finding_md.name != "_meta.md"):
                        pairs.append((aggregate_md, finding_md))

    if dry_run:
        return len(pairs), 0
    with Store() as store:
        for aggregate, finding in pairs:
            _id, was_created = emit_derivation(store, aggregate, finding)
            if was_created:
                created += 1
            else:
                existed += 1
    return created, existed


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true",
                    help="Report what would be done without moving files "
                         "or writing to the substrate.")
    args = ap.parse_args()

    print(f"Lattice: {LATTICE_NAME} ({LATTICE})", file=sys.stderr)
    if args.dry_run:
        print("DRY RUN — no files moved, no substrate writes.", file=sys.stderr)

    # === Phase 1: file moves ===
    print("\n=== Phase 1: file moves ===", file=sys.stderr)
    move_groups = [
        ("workspace findings (claims)",
         _findings_moves(WORKSPACE_DIR / "findings" / "claims", "claims"),
         "dir"),
        ("workspace findings (notes)",
         _findings_moves(WORKSPACE_DIR / "findings" / "notes", "notes"),
         "dir"),
        ("claim-convergence reviews", _claim_review_moves(), "file"),
        ("discovery/review (notes)",  _note_review_moves(), "file"),
    ]
    total_moved = 0
    for label, items, kind in move_groups:
        moved = 0
        for src, dst in items:
            if kind == "dir":
                moved += _move_dir(src, dst, args.dry_run)
            else:
                if _move_file(src, dst, args.dry_run):
                    moved += 1
        print(f"  {label:36s} {moved} file(s)", file=sys.stderr)
        total_moved += moved
    print(f"  total moved: {total_moved}", file=sys.stderr)

    # === Phase 2: substrate path rewrite ===
    print("\n=== Phase 2: substrate path rewrite ===", file=sys.stderr)
    subs = _path_substitutions()
    print(f"  {len(subs)} path-prefix substitutions", file=sys.stderr)
    if args.dry_run:
        changed = migrate_paths(DOCUVERSE_LOG, subs, dry_run=True)
        print(f"  [dry-run] would rewrite {changed} link(s)", file=sys.stderr)
    else:
        changed = migrate_paths(DOCUVERSE_LOG, subs, dry_run=False)
        print(f"  rewrote {changed} link(s)", file=sys.stderr)

    # === Phase 3: rebuild SQLite index (so backfill sees consistent state) ===
    if not args.dry_run:
        print("\n=== Phase 3: rebuild SQLite index ===", file=sys.stderr)
        with Store() as store:
            store.rebuild_index()
        print("  index rebuilt", file=sys.stderr)
    else:
        print("\n=== Phase 3: rebuild SQLite index (skipped, dry-run) ===",
              file=sys.stderr)

    # === Phase 4: backfill finding classifier ===
    print("\n=== Phase 4: backfill finding classifier ===", file=sys.stderr)
    created, existed = _backfill_finding_classifiers(args.dry_run)
    if args.dry_run:
        print(f"  [dry-run] {created} per-finding doc(s) would be classified",
              file=sys.stderr)
    else:
        print(f"  {created} new + {existed} pre-existing = "
              f"{created + existed} classified", file=sys.stderr)

    # === Phase 5: backfill provenance.derivation ===
    print("\n=== Phase 5: backfill provenance.derivation ===", file=sys.stderr)
    created, existed = _backfill_provenance(args.dry_run)
    if args.dry_run:
        print(f"  [dry-run] {created} (aggregate, finding) pair(s) would be linked",
              file=sys.stderr)
    else:
        print(f"  {created} new + {existed} pre-existing = "
              f"{created + existed} provenance link(s)", file=sys.stderr)

    print("\nDone.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
