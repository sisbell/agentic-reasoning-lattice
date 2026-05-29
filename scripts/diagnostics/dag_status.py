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
    python scripts/diagnostics/dag_status.py --workers 4   # show partition preview
"""

from __future__ import annotations

import argparse
import re
import sys
from glob import glob
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import triggers as triggers_module
from lib.backend.predicates import active_links
from lib.predicates import is_retired
from lib.protocols.febe.session import open_session
from lib.runner import Trigger, compute_active_ready_partition
from lib.shared.paths import LATTICE


NOTE_TRIGGER_NAMES = (
    "inquiry_consult",
    "note_draft",
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
    # Also discover ASNs that have an inquiry but no note yet (pre-draft
    # state — surfaces with next-trigger=note-draft).
    for f in glob("_docuverse/documents/**/inquiry/ASN-*.md", recursive=True):
        m = asn_pat.search(f)
        if m:
            discovered.add(m.group(1))

    state = session.store

    # Filter out substrate-retired. For inquiry-only ASNs (no note),
    # check retirement on the inquiry address — mirrors note-scheduler.
    active: set[str] = set()
    asn_to_note_addr: dict[str, object] = {}
    for asn in discovered:
        note_addr = None
        for path, addr in state.path_to_addr.items():
            if f"/note/{asn}-" in path and not path.endswith(".statements.md"):
                note_addr = addr
                break
        if note_addr is None:
            inquiry_rel = f"_docuverse/documents/1.1/1/inquiry/{asn}.md"
            inquiry_addr = state.path_to_addr.get(inquiry_rel)
            if inquiry_addr is None or not is_retired(session, inquiry_addr):
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


def _inquiry_addr_for(session, asn: str):
    """Look up the inquiry doc address for an ASN. Used for pre-draft
    ASNs where no note exists yet but an inquiry does."""
    state = session.store
    rel = f"_docuverse/documents/1.1/1/inquiry/{asn}.md"
    return state.path_to_addr.get(rel)


def _note_title_for(asn: str) -> str:
    """Read the first H1 from the ASN's note file on disk, or fall back
    to the inquiry's frontmatter `title` when no note exists yet.
    Strips the `ASN-NNNN:` prefix when present.
    """
    matches = glob(f"_docuverse/documents/**/note/{asn}-*.md", recursive=True)
    matches = [m for m in matches if ".statements.md" not in m and ".motif." not in m]
    if matches:
        try:
            with open(matches[0]) as f:
                first_line = f.readline().strip()
        except OSError:
            first_line = ""
        title = re.sub(r"^#+\s*", "", first_line)
        title = re.sub(r"^ASN-\d{4}\s*[:\-]\s*", "", title)
        return title

    # Pre-draft fallback: read title from the inquiry frontmatter.
    inq = Path(f"_docuverse/documents/1.1/1/inquiry/{asn}.md")
    if not inq.exists():
        return ""
    try:
        text = inq.read_text()
    except OSError:
        return ""
    m = re.search(r"^title:\s*(.+?)\s*$", text, re.MULTILINE)
    if not m:
        return ""
    return m.group(1).strip().strip('"').strip("'")


def _print_partitions(
    session, order: list[str], states: dict[str, str],
    triggers: list, n_workers: int,
) -> None:
    """Show what each worker will actually do on the first outer pass
    of the next scheduler run, using the same two-clause filter the
    scheduler uses:

      active  = ASNs with at least one fire-able trigger
      ready   = active ∧ no declared dep is also active
      partition = round-robin slice of ready per worker

    This is NOT a simple round-robin over the topo-sorted list — the
    DAG-honoring filter excludes downstream ASNs whose foundations are
    still active. Those dependents enter ready on a later outer pass
    after the upstream settles.
    """
    if n_workers <= 0:
        return
    print()

    # Compute the same active/ready set the scheduler will see. Single
    # filter call gives us the canonical sets; per-worker we slice.
    active_set, ready_topo, _ = compute_active_ready_partition(
        session, order, triggers, 0, n_workers,
    )

    if not active_set:
        print(f"  Partition preview ({n_workers} workers): all ASNs "
              f"quiescent — no work this pass.")
        return

    deferred = sorted(active_set - set(ready_topo))

    print(f"  Partition preview ({n_workers} workers, DAG-honoring filter):")
    print(f"    active total: {len(active_set)} ASNs")
    print(f"    ready this pass: {len(ready_topo)} "
          f"({', '.join(a.replace('ASN-', '') for a in ready_topo) or '(none)'})")
    if deferred:
        print(f"    deferred (dep active): {len(deferred)} "
              f"({', '.join(a.replace('ASN-', '') for a in deferred)})")
    print()
    for w in range(n_workers):
        partition = [
            ready_topo[i] for i in range(len(ready_topo))
            if i % n_workers == w
        ]
        if not partition:
            print(f"    worker {w}: empty this pass "
                  f"(waiting on upstream)")
            continue
        asn_str = ", ".join(a.replace("ASN-", "") for a in partition)
        print(f"    worker {w}: {len(partition)} ASN(s) ready")
        print(f"      {asn_str}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="DAG status diagnostic — walk order, state, partition preview.",
    )
    parser.add_argument(
        "--workers", type=int, default=0,
        help="Show how the topo-sorted ASN list would split across N workers "
             "(round-robin). 0 (default) skips partition preview.",
    )
    parser.add_argument(
        "--exclude", metavar="CLASSES", default=None,
        help=(
            "Comma-separated class labels to exclude from the listing. "
            "Any class declared in the YAML is valid (plus 'core' for the implicit-default set). "
            "Class membership is read from _workspace/asn-classes.yaml."
        ),
    )
    args = parser.parse_args()

    from lib.shared.asn_classes import (
        apply_exclude, class_for, parse_exclude_arg,
    )
    try:
        excluded_classes = parse_exclude_arg(args.exclude)
    except ValueError as exc:
        parser.error(str(exc))

    triggers = _note_triggers()
    states: dict[str, str] = {}
    with open_session(LATTICE) as session:
        order, deps_map = _topo_sorted(session)
        if excluded_classes:
            before = len(order)
            order = apply_exclude(order, excluded_classes)
            print(
                f"  [DAG-STATUS] --exclude {','.join(sorted(excluded_classes))}: "
                f"{before} → {len(order)} ASNs",
            )
        print(f"{'#':<4}{'ASN':<10}{'title':<32}{'class':<12}{'deps':<32}{'state':<12}  next-trigger(s)")
        print("─" * 142)
        for i, asn in enumerate(order, 1):
            note_addr = _note_addr_for(session, asn)
            title = _note_title_for(asn)
            # Truncate long titles to keep the table aligned
            if len(title) > 30:
                title = title[:29] + "…"
            dep_str = ",".join(d.replace("ASN-", "") for d in sorted(deps_map.get(asn, set()))) or "(none)"

            # Triggers come in two flavors:
            #   - note-scope (per_active_note / per_asn_note): predicate
            #     wants a note address. Skip if no note exists yet.
            #   - inquiry-scope (per_inquiry_of_asn — note_draft): predicate
            #     wants an inquiry address.
            # Evaluate each against the address it expects; collect names
            # of those that would fire (predicate returns False = fire).
            inquiry_addr = _inquiry_addr_for(session, asn)
            fires = []
            for trig in triggers:
                if trig.name in ("note-draft", "inquiry-consult"):
                    eval_addr = inquiry_addr
                else:
                    eval_addr = note_addr
                if eval_addr is None:
                    continue
                try:
                    skip = trig.predicate(session, eval_addr)
                except Exception as e:
                    skip = f"err:{e.__class__.__name__}"
                if skip is False:
                    fires.append(trig.name)

            if note_addr is None and inquiry_addr is None:
                state_label = "no-addr"
                next_trigger = "?"
            elif not fires:
                state_label = "quiescent"
                next_trigger = "-"
            else:
                state_label = "pending"
                next_trigger = ", ".join(fires)

            states[asn] = state_label
            asn_num = int(asn.replace("ASN-", ""))
            cls = class_for(asn_num)
            print(f"{i:<4}{asn:<10}{title:<32}{cls:<12}{dep_str:<32}{state_label:<12}  {next_trigger}")

    print()
    print(f"  {len(order)} active notes in DAG walk order.")

    if args.workers > 0:
        _print_partitions(session, order, states, triggers, args.workers)

    return 0


if __name__ == "__main__":
    sys.exit(main())
