#!/usr/bin/env python3
"""Audit citation.depends substrate state for every active ASN.

Reports, per active ASN:
  - Declared deps in the inquiry frontmatter (`depends:` field)
  - Inquiry-side substrate citation.depends (count + shape)
  - Note-side substrate citation.depends (count + shape; LEGACY)
  - Per-dep resolution (note → sidecar → supersession_head → path)
  - End-to-end loader test (does load_foundation_for_note return non-empty?)

Classifies each ASN into one of:
  HEALTHY            — frontmatter matches inquiry-side fan-out, zero note-side, all deps resolve
  EMPTY_OK           — `depends: []` declared, zero substrate (foundation-ASN case)
  NEW_ONLY           — frontmatter declared, inquiry-side citations only (one-per-target shape), all deps resolve
  DEPS_UNRESOLVABLE  — substrate shape matches frontmatter, but per-dep resolution fails (e.g., dep note has no .statements.md sidecar yet — downstream pipeline state, not a substrate issue)
  LEGACY             — no frontmatter, note-side substrate citations present (loads fine — needs frontmatter backfill before retiring note-side)
  MIXED              — substrate citations on BOTH inquiry-side AND note-side
  DEFUNCT            — no frontmatter and no substrate at all (pre-modern / unused ASN; not a problem, just not part of operational lattice)
  SUBSTRATE_BROKEN   — frontmatter declares deps but substrate doesn't match (empty on both sides, OR inquiry-side targets ≠ declared)

Exit code is nonzero if any ASN is SUBSTRATE_BROKEN (CI gate).
DEPS_UNRESOLVABLE does not fail the gate — it signals downstream
pipeline state (e.g., missing sidecar), not a substrate issue.

Usage:
    python scripts/diagnostics/citation_depends_audit.py
    python scripts/diagnostics/citation_depends_audit.py --json
    python scripts/diagnostics/citation_depends_audit.py 96 97
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import List, Optional, Dict, Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.backend.predicates import active_links
from lib.lattice.labels import format_label, label_pattern
from lib.predicates import latest_doc_head, statements_sidecar_of
from lib.protocols.febe.session import open_session
from lib.shared.common import find_asn
from lib.shared.foundation import load_foundation_for_note
from lib.shared.frontmatter import read_doc_with_frontmatter
from lib.shared.paths import (
    INQUIRY_DIR, LATTICE, NOTE_DIR, WORKSPACE, inquiry_doc_path,
)


@dataclass
class DepResolution:
    dep_id: int
    status: str  # "ok" | "no-inquiry" | "no-note-addr" | "no-sidecar" | "no-path-after-supersession" | "retired"
    detail: str = ""


@dataclass
class AsnAudit:
    asn_id: int
    label: str
    state: str  # one of the classification strings above
    frontmatter_deps: Optional[List[int]] = None  # None = field absent
    inquiry_link_count: int = 0
    inquiry_link_shapes: List[str] = field(default_factory=list)  # e.g. ["fanout(7)"] or ["pair", "pair", ...]
    inquiry_targets: List[int] = field(default_factory=list)
    note_link_count: int = 0
    note_link_shapes: List[str] = field(default_factory=list)
    note_targets: List[int] = field(default_factory=list)
    dep_resolutions: List[DepResolution] = field(default_factory=list)
    loader_result: str = ""  # "ok(N chars)" | "empty" | "raised: ..."
    notes: List[str] = field(default_factory=list)


def _shape_label(link, fan_out_threshold: int = 2) -> str:
    """Classify a link's shape from its to_set cardinality."""
    n = len(link.to_set)
    if n == 0:
        return "empty"
    if n == 1:
        return "pair"
    return f"fanout({n})"


def _asn_id_from_path(path: str, pattern) -> Optional[int]:
    """Extract ASN id from a path string."""
    if not path:
        return None
    m = pattern.search(path)
    if not m:
        return None
    return int(m.group(1))


def _link_targets_as_asn_ids(link, store, pattern) -> List[int]:
    """Resolve to_set addresses to ASN ids via path_for_addr."""
    out = []
    for addr in link.to_set:
        p = store.path_for_addr(addr)
        n = _asn_id_from_path(p, pattern)
        if n is not None:
            out.append(n)
    return sorted(out)


def _resolve_one_dep(session, dep_id: int, pattern) -> DepResolution:
    """Walk dep note → sidecar → supersession_head → path."""
    store = session.store
    dep_path, _ = find_asn(str(dep_id))
    if dep_path is None:
        return DepResolution(dep_id, "no-inquiry", "no on-disk note file")
    dep_rel = str(dep_path.resolve().relative_to(WORKSPACE.resolve()))
    dep_note_addr = store.path_to_addr.get(dep_rel)
    if dep_note_addr is None:
        return DepResolution(dep_id, "no-note-addr", f"note not path-registered: {dep_rel}")
    # Retired check
    if active_links(store.state, "retired", to_set=[dep_note_addr]):
        return DepResolution(dep_id, "retired", "")
    # Sidecar resolution
    sidecar = statements_sidecar_of(session, dep_note_addr)
    if sidecar is None:
        return DepResolution(dep_id, "no-sidecar", "")
    # Supersession walk + path resolution
    head = latest_doc_head(session, sidecar)
    head_path = store.path_for_addr(head)
    if head_path is None:
        return DepResolution(
            dep_id, "no-path-after-supersession",
            f"head {head} has no registered path",
        )
    return DepResolution(dep_id, "ok", f"resolved to {head_path}")


def _audit_one_asn(session, asn_id: int) -> AsnAudit:
    store = session.store
    label = format_label(asn_id)
    pattern = label_pattern()
    audit = AsnAudit(asn_id=asn_id, label=label, state="?")

    # Inquiry frontmatter
    inq_path = inquiry_doc_path(asn_id)
    declared: Optional[List[int]] = None
    if inq_path.exists():
        try:
            fm, _body = read_doc_with_frontmatter(inq_path)
            if fm is not None and "depends" in fm:
                raw = fm.get("depends") or []
                declared = sorted({int(d) for d in raw}) if raw else []
        except Exception as e:
            audit.notes.append(f"frontmatter read error: {e}")
    audit.frontmatter_deps = declared

    # Inquiry-side substrate
    inq_rel = str(inq_path.resolve().relative_to(WORKSPACE.resolve())) if inq_path.exists() else None
    inq_addr = store.path_to_addr.get(inq_rel) if inq_rel else None
    if inq_addr is not None:
        inq_links = list(active_links(
            store.state, "citation.depends", from_set=[inq_addr],
        ))
        audit.inquiry_link_count = len(inq_links)
        audit.inquiry_link_shapes = [_shape_label(L) for L in inq_links]
        targets = set()
        for L in inq_links:
            for n in _link_targets_as_asn_ids(L, store, pattern):
                targets.add(n)
        audit.inquiry_targets = sorted(targets)

    # Note-side substrate (legacy)
    note_addr = None
    note_prefix = str(NOTE_DIR.relative_to(WORKSPACE)) + f"/{label}-"
    for p, a in store.path_to_addr.items():
        if p.startswith(note_prefix) and not p.endswith(".statements.md"):
            note_addr = a
            break
    if note_addr is not None:
        note_links = list(active_links(
            store.state, "citation.depends", from_set=[note_addr],
        ))
        audit.note_link_count = len(note_links)
        audit.note_link_shapes = [_shape_label(L) for L in note_links]
        targets = set()
        for L in note_links:
            for n in _link_targets_as_asn_ids(L, store, pattern):
                targets.add(n)
        audit.note_targets = sorted(targets)

    # Per-dep resolution (uses frontmatter declaration; that's the spec)
    if declared:
        for dep_id in declared:
            audit.dep_resolutions.append(
                _resolve_one_dep(session, dep_id, pattern),
            )

    # End-to-end loader test
    if note_addr is not None:
        note_path_rel = store.path_for_addr(note_addr)
        asn_path = WORKSPACE / note_path_rel if note_path_rel else None
        if asn_path and asn_path.exists():
            try:
                result = load_foundation_for_note(asn_path, asn_id)
                if not result:
                    audit.loader_result = "empty"
                else:
                    audit.loader_result = f"ok({len(result)} chars)"
            except Exception as e:
                audit.loader_result = f"raised: {type(e).__name__}: {e}"
        else:
            audit.loader_result = "no-note-file"
    else:
        audit.loader_result = "no-note-addr"

    # Classification
    audit.state = _classify(audit)
    return audit


def _classify(a: AsnAudit) -> str:
    """Assign a single state label based on collected facts.

    Order of checks matters — DEFUNCT and LEGACY catch the
    no-frontmatter cases before BROKEN/HEALTHY which require
    frontmatter to be present.
    """
    # No frontmatter `depends:` field at all
    if a.frontmatter_deps is None:
        if a.inquiry_link_count == 0 and a.note_link_count == 0:
            return "DEFUNCT"  # pre-modern, no substrate, not operational
        if a.inquiry_link_count > 0 and a.note_link_count > 0:
            return "MIXED"  # bilateral citations without frontmatter declaration
        if a.note_link_count > 0:
            return "LEGACY"  # operational via note-side; needs frontmatter backfill
        # inquiry-side citations only, without frontmatter declaration
        # — unusual; classify as MIXED because substrate is over-declaring
        return "MIXED"

    # `depends: []` — foundation ASN case
    if not a.frontmatter_deps:
        if a.inquiry_link_count == 0 and a.note_link_count == 0:
            return "EMPTY_OK"
        return "MIXED"  # frontmatter says none, substrate has some

    # Frontmatter declares non-empty deps
    declared = set(a.frontmatter_deps)
    inq_match = set(a.inquiry_targets) == declared
    res_ok = all(r.status == "ok" for r in a.dep_resolutions)

    if a.inquiry_link_count > 0 and a.note_link_count > 0:
        return "MIXED"
    if a.inquiry_link_count == 0 and a.note_link_count == 0:
        return "SUBSTRATE_BROKEN"  # frontmatter declares but substrate empty
    if a.inquiry_link_count > 0:
        if not inq_match:
            # Substrate shape disagrees with frontmatter declaration
            return "SUBSTRATE_BROKEN"
        # Substrate aligns with frontmatter. Resolution status decides next.
        if not res_ok:
            # Substrate is fine; deps don't resolve at loader time (e.g.,
            # dep note has no sidecar yet — downstream pipeline state).
            return "DEPS_UNRESOLVABLE"
        # HEALTHY iff substrate has exactly ONE inquiry-side link
        # covering all declared deps. For single-dep ASNs this is a
        # `pair`; for multi-dep ASNs it must be `fanout(N)`. Multiple
        # links (one-per-target legacy shape) is NEW_ONLY.
        if len(a.inquiry_link_shapes) == 1:
            return "HEALTHY"
        return "NEW_ONLY"
    # Note-side only with frontmatter declared — call it MIXED, since
    # frontmatter is the authoritative source and substrate is on the wrong side
    return "MIXED"


def _iter_active_asns(session) -> List[int]:
    pattern = label_pattern()
    note_prefix = str(NOTE_DIR.relative_to(WORKSPACE)) + "/"
    found = set()
    for path, addr in session.store.path_to_addr.items():
        if not path.startswith(note_prefix):
            continue
        if path.endswith(".statements.md"):
            continue
        if not session.active_links("note", to_set=[addr]):
            continue
        m = pattern.search(path)
        if not m:
            continue
        found.add(int(m.group(1)))
    return sorted(found)


def _print_human(audits: List[AsnAudit]) -> None:
    print(f"\n  {'ASN':10s} {'STATE':22s} {'FRONT':6s} {'INQUIRY':16s} {'NOTE':14s} {'RESOLVED':12s} {'LOADER':16s}",
          file=sys.stderr)
    print(f"  {'-'*10} {'-'*22} {'-'*6} {'-'*16} {'-'*14} {'-'*12} {'-'*16}",
          file=sys.stderr)
    for a in audits:
        front = "—" if a.frontmatter_deps is None else str(len(a.frontmatter_deps))
        inq = f"{a.inquiry_link_count}/{','.join(a.inquiry_link_shapes) or '-'}"
        note = f"{a.note_link_count}/{','.join(a.note_link_shapes) or '-'}"
        if a.frontmatter_deps:
            ok = sum(1 for r in a.dep_resolutions if r.status == "ok")
            resolved = f"{ok}/{len(a.frontmatter_deps)}"
        else:
            resolved = "—"
        print(f"  {a.label:10s} {a.state:22s} {front:6s} {inq:16s} {note:14s} {resolved:12s} {a.loader_result:16s}",
              file=sys.stderr)

    # Summary
    by_state: Dict[str, int] = {}
    for a in audits:
        by_state[a.state] = by_state.get(a.state, 0) + 1
    print(f"\n  Summary ({len(audits)} active ASNs):", file=sys.stderr)
    for state, count in sorted(by_state.items()):
        print(f"    {state:22s} {count}", file=sys.stderr)

    # Detail for problematic ASNs — exclude DEFUNCT (not actionable) and
    # LEGACY (working, just needs frontmatter backfill — bulk operation).
    # DEPS_UNRESOLVABLE is also excluded — it's a downstream pipeline
    # state (missing sidecar), not a substrate problem.
    problems = [
        a for a in audits
        if a.state in ("SUBSTRATE_BROKEN", "MIXED", "NEW_ONLY")
    ]
    if problems:
        print(f"\n  Detail for {len(problems)} actionable ASNs:", file=sys.stderr)
        for a in problems:
            print(f"    {a.label} [{a.state}]:", file=sys.stderr)
            if a.frontmatter_deps is not None:
                print(f"      frontmatter declared: {a.frontmatter_deps}", file=sys.stderr)
            print(f"      inquiry: {a.inquiry_link_count} links, shapes={a.inquiry_link_shapes}, targets={a.inquiry_targets}", file=sys.stderr)
            print(f"      note:    {a.note_link_count} links, shapes={a.note_link_shapes}, targets={a.note_targets}", file=sys.stderr)
            for r in a.dep_resolutions:
                if r.status != "ok":
                    print(f"      dep ASN-{r.dep_id:04d}: {r.status} {r.detail}", file=sys.stderr)
            print(f"      loader: {a.loader_result}", file=sys.stderr)


def _print_json(audits: List[AsnAudit]) -> None:
    payload = {
        "audits": [asdict(a) for a in audits],
        "summary": {},
    }
    for a in audits:
        payload["summary"][a.state] = payload["summary"].get(a.state, 0) + 1
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "asn", nargs="*", type=int,
        help="Optional ASN numbers to restrict to. Default: every active ASN.",
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Emit machine-readable JSON to stdout (default: human table to stderr).",
    )
    args = parser.parse_args()

    audits: List[AsnAudit] = []
    with open_session(LATTICE) as session:
        active = _iter_active_asns(session)
        targets = [n for n in active if not args.asn or n in args.asn]
        for asn_id in targets:
            audits.append(_audit_one_asn(session, asn_id))

    if args.json:
        _print_json(audits)
    else:
        _print_human(audits)

    # Exit nonzero if any ASN is SUBSTRATE_BROKEN (CI gate).
    # DEPS_UNRESOLVABLE is excluded — it's a downstream pipeline state
    # (e.g., dep note has no sidecar yet), not a substrate problem.
    broken = sum(1 for a in audits if a.state == "SUBSTRATE_BROKEN")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
