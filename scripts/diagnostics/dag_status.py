#!/usr/bin/env python3
"""DAG diagnostics — show every active note in topo-sorted walk order,
its dependencies, current quiescence state, and the next trigger that
would fire on it.

Read-only. Mirrors note-scheduler.py --dag's discovery + topo sort,
then evaluates each of the four note-cycle trigger predicates against
each note to report state. Useful for confirming what the next pass
of the scheduler will do without actually running it.

Usage:
    python scripts/diagnostics/dag_status.py
"""

from __future__ import annotations

import re
import sys
from glob import glob
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import triggers as triggers_module
from lib.backend.predicates import active_links
from lib.predicates import is_retired
from lib.protocols.febe.session import open_session
from lib.runner import Trigger
from lib.shared.paths import LATTICE


NOTE_TRIGGER_NAMES = (
    "note_review", "note_consult", "note_revise", "note_statements",
)


def _note_triggers() -> list[Trigger]:
    found = []
    for name in NOTE_TRIGGER_NAMES:
        trig = getattr(triggers_module, name, None)
        if isinstance(trig, Trigger):
            found.append(trig)
    return found


def _topo_sorted(session) -> tuple[list[str], dict[str, set[str]]]:
    """Return (topo_order, deps_map) for active non-retired notes.

    Mirrors note-scheduler.py's _active_notes_topo_sorted helper.
    """
    asn_pat = re.compile(r"(ASN-\d{4})")
    discovered: set[str] = set()
    for f in glob("_docuverse/documents/**/note/ASN-*.md", recursive=True):
        if ".statements.md" in f or ".motif." in f:
            continue
        m = asn_pat.search(f)
        if m:
            discovered.add(m.group(1))

    state = session.store

    # Filter out substrate-retired
    active: set[str] = set()
    asn_to_note_addr: dict[str, object] = {}
    for asn in discovered:
        note_addr = None
        for path, addr in state.path_to_addr.items():
            if f"/note/{asn}-" in path and not path.endswith(".statements.md"):
                note_addr = addr
                break
        if note_addr is None:
            active.add(asn)
            continue
        if not is_retired(session, note_addr):
            active.add(asn)
            asn_to_note_addr[asn] = note_addr

    # Edges
    deps: dict[str, set[str]] = {a: set() for a in active}
    for link in active_links(state, "citation.depends"):
        from_asns: set[str] = set()
        to_asns: set[str] = set()
        for a in link.from_set:
            p = state.path_for_addr(a)
            if p:
                m = asn_pat.search(p)
                if m:
                    from_asns.add(m.group(1))
        for a in link.to_set:
            p = state.path_for_addr(a)
            if p:
                m = asn_pat.search(p)
                if m:
                    to_asns.add(m.group(1))
        for f_ in from_asns & active:
            for t in to_asns & active:
                if f_ != t:
                    deps[f_].add(t)

    # Kahn's
    sorted_list: list[str] = []
    remaining = {a: set(deps[a]) for a in active}
    while remaining:
        ready = sorted(a for a, d in remaining.items() if not d)
        if not ready:
            ready = sorted(remaining.keys())
        for a in ready:
            sorted_list.append(a)
            remaining.pop(a)
        for a in remaining:
            remaining[a] -= set(ready)
    return sorted_list, deps


def _note_addr_for(session, asn: str):
    state = session.store
    for path, addr in state.path_to_addr.items():
        if f"/note/{asn}-" in path and not path.endswith(".statements.md"):
            return addr
    return None


def main() -> int:
    triggers = _note_triggers()
    with open_session(LATTICE) as session:
        order, deps_map = _topo_sorted(session)
        print(f"{'#':<4}{'ASN':<10}{'deps':<32}{'state':<14}  next-trigger(s)")
        print("─" * 95)
        for i, asn in enumerate(order, 1):
            note_addr = _note_addr_for(session, asn)
            dep_str = ",".join(d.replace("ASN-", "") for d in sorted(deps_map.get(asn, set()))) or "(none)"

            if note_addr is None:
                state_label = "no-addr"
                next_trigger = "?"
            else:
                # Evaluate each predicate. Predicate True = SKIP.
                # Trigger fires if predicate returns False.
                fires = []
                for trig in triggers:
                    try:
                        skip = trig.predicate(session, note_addr)
                    except Exception as e:
                        skip = f"err:{e.__class__.__name__}"
                    if skip is False:
                        fires.append(trig.name)
                if not fires:
                    state_label = "quiescent"
                    next_trigger = "-"
                else:
                    state_label = "pending"
                    next_trigger = ", ".join(fires)

            print(f"{i:<4}{asn:<10}{dep_str:<32}{state_label:<14}  {next_trigger}")

    print()
    print(f"  {len(order)} active notes in DAG walk order.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
