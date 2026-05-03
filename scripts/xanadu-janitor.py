#!/usr/bin/env python3
"""xanadu-janitor — detection-only reconciliation pass over the lattice.

Runs every reconciliation predicate against the lattice and reports
inconsistencies between filesystem state and substrate state. Per
docs/hypergraph-protocol/error-handling.md, the simulator's
non-atomic operations can leave the lattice in partial-failure
states (orphan files, dangling links). The janitor surfaces them.

Detection-only — no destructive action. The output is for diagnosis;
operators decide whether to retract dangling links, delete orphan
files, back-fill missing data, or investigate further.

Usage:
    python scripts/xanadu-janitor.py
    python scripts/xanadu-janitor.py --surface attributes
    python scripts/xanadu-janitor.py --surface claim-findings,note-findings
    python scripts/xanadu-janitor.py --quiet

Exit codes:
    0 — everything clean
    1 — at least one inconsistency found
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import (
    CLAIM_DIR, CLAIM_FINDINGS_DIR, LATTICE, NOTE_FINDINGS_DIR,
)
from lib.febe.session import open_session
from lib.predicates import (
    dangling_attribute_links,
    dangling_claim_finding_links,
    dangling_note_finding_links,
    orphan_claim_finding_docs,
    orphan_note_finding_docs,
    orphan_sidecars,
)


SURFACES = ("attributes", "claim-findings", "note-findings")


def _check_attributes(session, quiet):
    """Run reconciliation predicates against attribute sidecars."""
    orphans = []
    if CLAIM_DIR.exists():
        # Walk every ASN dir under CLAIM_DIR
        for asn_dir in sorted(CLAIM_DIR.iterdir()):
            if not asn_dir.is_dir() or asn_dir.name.startswith("_"):
                continue
            orphans.extend(orphan_sidecars(session, asn_dir))
    danglers = dangling_attribute_links(session)
    return orphans, danglers


def _check_claim_findings(session, quiet):
    """Run reconciliation predicates against claim-layer findings."""
    orphans = []
    if CLAIM_FINDINGS_DIR.exists():
        orphans.extend(orphan_claim_finding_docs(session, CLAIM_FINDINGS_DIR))
    danglers = dangling_claim_finding_links(session)
    return orphans, danglers


def _check_note_findings(session, quiet):
    """Run reconciliation predicates against note-layer findings."""
    orphans = []
    if NOTE_FINDINGS_DIR.exists():
        orphans.extend(orphan_note_finding_docs(session, NOTE_FINDINGS_DIR))
    danglers = dangling_note_finding_links(session)
    return orphans, danglers


_CHECKERS = {
    "attributes": _check_attributes,
    "claim-findings": _check_claim_findings,
    "note-findings": _check_note_findings,
}


def _print_surface_report(label, orphans, danglers):
    """Print a per-surface summary block."""
    lattice_root = LATTICE.resolve()
    print(f"## {label}")
    print(f"  orphan files:     {len(orphans)}")
    print(f"  dangling links:   {len(danglers)}")
    if orphans:
        print(f"  orphan paths:")
        for path in orphans:
            try:
                rel = path.resolve().relative_to(lattice_root)
                print(f"    {rel}")
            except ValueError:
                print(f"    {path}")
    if danglers:
        print(f"  dangling link addrs:")
        for link in danglers:
            print(f"    {link.addr}  (type={_type_name(link)})")
    print()


def _type_name(link):
    """Render a link's type set for display."""
    return ", ".join(str(t) for t in link.type_set) if link.type_set else "?"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--surface",
        default=",".join(SURFACES),
        help=(
            "Comma-separated list of surfaces to check. "
            f"Choices: {', '.join(SURFACES)}, all. Default: all."
        ),
    )
    parser.add_argument(
        "--quiet", "-q", action="store_true",
        help="Print only the total counts; suppress per-surface details.",
    )
    args = parser.parse_args()

    requested = args.surface.split(",") if args.surface != "all" else list(SURFACES)
    requested = [s.strip() for s in requested if s.strip()]
    unknown = [s for s in requested if s not in SURFACES]
    if unknown:
        print(
            f"error: unknown surface(s) {unknown}; "
            f"valid: {', '.join(SURFACES)}",
            file=sys.stderr,
        )
        return 2

    if not args.quiet:
        print(f"# xanadu-janitor — lattice: {LATTICE}\n")

    session = open_session(LATTICE)

    total_orphans = 0
    total_danglers = 0
    for surface in requested:
        orphans, danglers = _CHECKERS[surface](session, args.quiet)
        total_orphans += len(orphans)
        total_danglers += len(danglers)
        if not args.quiet:
            _print_surface_report(surface, orphans, danglers)

    if args.quiet:
        print(
            f"orphan_files={total_orphans} "
            f"dangling_links={total_danglers}"
        )
    else:
        print(f"## Summary")
        print(f"  total orphan files:    {total_orphans}")
        print(f"  total dangling links:  {total_danglers}")
        if total_orphans == 0 and total_danglers == 0:
            print(f"\n  Lattice is clean.")
        else:
            print(
                f"\n  Lattice has {total_orphans} orphan file(s) and "
                f"{total_danglers} dangling link(s)."
            )
            print(
                "  These are inconsistencies between filesystem state "
                "and substrate state."
            )
            print(
                "  See docs/hypergraph-protocol/error-handling.md for "
                "what they mean and how to recover."
            )

    return 0 if (total_orphans == 0 and total_danglers == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
