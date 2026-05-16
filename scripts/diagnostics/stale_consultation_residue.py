#!/usr/bin/env python3
"""Find consultation substrate state where on-disk files are missing —
worker-death residue — and offer retraction.

The pattern: an agent emits `consultation.assessment` (or `.answer`,
or `.questions`) classifiers and `consultation.coverage` links during
a fire, then crashes before the file write or classifier completes.
After operator cleanup (deleting the partial file), substrate still
references the now-missing doc. `is_finding_consulted` returns True
for findings the phantom covers, so `note_consult` doesn't re-fire,
and `note_revise` runs with empty consultation context.

This tool:
  - Scans `consultation.assessment` / `.answer.*` / `.questions`
    classifiers, identifies addresses whose path-registered file is
    missing from disk.
  - For each phantom doc, enumerates the coverage links emanating
    from it (these are what gate `is_finding_consulted`).
  - In retract mode, emits `retraction` links nullifying the
    classifier(s) and coverage links. Leaves the path registration
    alone — substrate addresses are append-only; the path can be
    re-emitted by a future re-fire (the address is reused).

Usage:
    # Operator-facing scan (verbose: prints when clean too)
    python scripts/diagnostics/stale_consultation_residue.py

    # Runner-facing check (silent when clean, loud banner otherwise)
    python scripts/diagnostics/stale_consultation_residue.py --quiet

    # Retract all phantoms found
    python scripts/diagnostics/stale_consultation_residue.py --retract

    # Retract phantoms for one ASN's consultation tree
    python scripts/diagnostics/stale_consultation_residue.py --retract --asn 47

Exits 0 in scan/quiet modes whether or not residue is found
(observability, not error). Retract mode exits non-zero on any
emit failure.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.backend.addressing import Address
from lib.backend.emit import emit_retraction
from lib.protocols.febe.session import open_session
from lib.shared.paths import LATTICE, WORKSPACE


# Classifier types that mark a doc as a consultation artifact. If any
# of these classify a doc whose path-registered file is missing, the
# doc is phantom.
_CONSULT_CLASSIFIERS = (
    "consultation.assessment",
    "consultation.questions",
    "consultation.answer.theory",
    "consultation.answer.evidence",
    "consultation.answer",  # parent type — covers legacy answer-classifier
)

# Asn-label parser for consultation paths.
_ASN_PAT = re.compile(r"/consultation/ASN-(\d{4})/")


def _asn_label_for_path(path: str) -> Optional[str]:
    m = _ASN_PAT.search(path)
    return f"ASN-{m.group(1)}" if m else None


def _file_missing(path: str) -> bool:
    """True if the path is registered but the on-disk file is missing."""
    return not (WORKSPACE / path).exists()


def _scan_phantoms(session) -> List[dict]:
    """Return a list of phantom-doc descriptors:
        {
          "addr": Address,
          "path": str,
          "asn": str,
          "classifiers": [Link, ...],     # active consult classifiers
          "coverage_out": [Link, ...],    # active coverage FROM this doc
        }
    Empty if the substrate has no consultation/filesystem drift.
    """
    state = session.store
    seen: dict[Address, dict] = {}

    for cls_name in _CONSULT_CLASSIFIERS:
        for link in session.active_links(cls_name):
            if not link.to_set:
                continue
            addr = link.to_set[0]
            path = state.path_for_addr(addr)
            if path is None or not _file_missing(path):
                continue
            entry = seen.setdefault(addr, {
                "addr": addr,
                "path": path,
                "asn": _asn_label_for_path(path) or "?",
                "classifiers": [],
                "coverage_out": [],
            })
            entry["classifiers"].append(link)

    # For each phantom, also enumerate outgoing coverage links — these
    # are the load-bearing ones for is_finding_consulted.
    for entry in seen.values():
        for cov in session.active_links(
            "consultation.coverage", from_set=[entry["addr"]],
        ):
            entry["coverage_out"].append(cov)

    return list(seen.values())


_WIDTH = 64


def _bline(text: str) -> str:
    return f"  ║{text.ljust(_WIDTH)}║"


def _print_banner(phantoms: List[dict]) -> None:
    bar = "═" * _WIDTH
    total_links = sum(
        len(e["classifiers"]) + len(e["coverage_out"]) for e in phantoms
    )
    print("", file=sys.stderr)
    print(f"  ╔{bar}╗", file=sys.stderr)
    print(
        _bline(
            f"  PHANTOM CONSULTATION RESIDUE — "
            f"{len(phantoms)} doc(s), {total_links} zombie link(s)"
        ),
        file=sys.stderr,
    )
    print(f"  ╠{bar}╣", file=sys.stderr)
    for entry in phantoms:
        label = entry["path"]
        if len(label) > _WIDTH - 4:
            label = "..." + label[-(_WIDTH - 7):]
        print(_bline(f"  {label}"), file=sys.stderr)
        print(
            _bline(
                f"    classifier x{len(entry['classifiers'])}, "
                f"coverage x{len(entry['coverage_out'])}"
            ),
            file=sys.stderr,
        )
    print(_bline(""), file=sys.stderr)
    print(
        _bline(
            "  Findings these phantoms 'cover' read as consulted —"
        ),
        file=sys.stderr,
    )
    print(
        _bline(
            "  revise fires with empty consultation context."
        ),
        file=sys.stderr,
    )
    print(_bline(""), file=sys.stderr)
    print(_bline("  Retract:"), file=sys.stderr)
    print(
        _bline(
            "    scripts/diagnostics/stale_consultation_residue.py --retract"
        ),
        file=sys.stderr,
    )
    asns = sorted({e["asn"] for e in phantoms if e["asn"] != "?"})
    if len(asns) > 1:
        for asn in asns:
            num = asn.replace("ASN-", "").lstrip("0") or "0"
            print(
                _bline(
                    f"    ... --retract --asn {num}     "
                    f"(scoped to {asn})"
                ),
                file=sys.stderr,
            )
    print(f"  ╚{bar}╝", file=sys.stderr)
    print("", file=sys.stderr)


def _retract_phantom(session, entry: dict) -> Tuple[int, int]:
    """Emit retractions for each classifier + coverage link on a
    phantom. Returns (retracted, failed)."""
    retracted = 0
    failed = 0
    by_doc = entry["addr"]
    for link in entry["classifiers"] + entry["coverage_out"]:
        try:
            emit_retraction(session.store, by_doc, link.addr)
            retracted += 1
        except Exception as exc:
            print(
                f"    [ERROR] retract {link.addr} failed: {exc!r}",
                file=sys.stderr,
            )
            failed += 1
    return retracted, failed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--quiet", action="store_true",
        help="Silent when no phantom residue found (runner use).",
    )
    parser.add_argument(
        "--retract", action="store_true",
        help="Retract phantom classifier + coverage links.",
    )
    parser.add_argument(
        "--asn", type=int, default=None,
        help="Scope retract to one ASN's consultation tree.",
    )
    args = parser.parse_args()

    with open_session(LATTICE) as session:
        phantoms = _scan_phantoms(session)

        if args.asn is not None:
            scope_label = f"ASN-{args.asn:04d}"
            phantoms = [e for e in phantoms if e["asn"] == scope_label]

        if not phantoms:
            if not args.quiet:
                scope_note = (
                    f" in {f'ASN-{args.asn:04d}'}"
                    if args.asn is not None else ""
                )
                print(
                    f"  [STALE-CONSULTATION] no phantom residue{scope_note}",
                    file=sys.stderr,
                )
            return 0

        if not args.retract:
            _print_banner(phantoms)
            return 0

        # Retract path
        total_retracted = 0
        total_failed = 0
        for entry in phantoms:
            r, f = _retract_phantom(session, entry)
            total_retracted += r
            total_failed += f
            print(
                f"  [RETRACT] {entry['path']}: "
                f"{r} retracted, {f} failed",
                file=sys.stderr,
            )
        print(
            f"\n  [STALE-CONSULTATION] retracted={total_retracted}, "
            f"failed={total_failed}",
            file=sys.stderr,
        )
        return 0 if total_failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
