"""Citation-target-existence check.

Every active citation link (`citation.depends`, `citation.forward`,
`citation.resolve`) must point at an address that resolves to a
registered, on-disk doc — walked via the version-parent map to the
base, then looked up in `paths.json`. A citation whose base isn't
registered is dangling: the target doc was deleted (or never
existed), and the citation points at nothing.

This catches the common cross-ASN soft-rot mode: claim A in one
ASN cites claim B in another, then B gets reverted/deleted, A's
citation silently dangles. Also flags any post-revert state where
substrate retains citations to addresses no longer in the path map.

Two severities:
  - ERROR: cited base address has no entry in `paths.json` — the
    doc identity itself is gone from substrate.
  - WARNING: base IS registered but the file on disk doesn't exist
    — substrate / filesystem drift.

Aggregates per citation type to avoid one-Issue-per-link noise.
"""

from __future__ import annotations

from typing import Iterable

from lib.backend.addressing import Address
from lib.protocols.febe.protocol import Session

from . import Issue, Severity


CHECK_NAME = "citation-targets-exist"
CHECK_DESCRIPTION = (
    "Every active citation link's target must walk (via the "
    "version-parent map) to a base address registered in paths.json "
    "with a file present on disk. Dangling citations indicate a "
    "doc was deleted without retracting incoming references."
)
_SAMPLE_SIZE = 3
_CITATION_TYPES = ("citation.depends", "citation.forward", "citation.resolve")


def _walk_to_base(session: Session, addr: Address) -> Address:
    parent_map = session.store.state.parent
    cur = addr
    while parent_map.get(cur) is not None:
        cur = parent_map[cur]
    return cur


def check_citation_targets_exist(session: Session) -> Iterable[Issue]:
    """Yield aggregate Issues per citation type for dangling targets."""
    addr_to_path = session.store.addr_to_path
    lattice_root = session.store.lattice_dir

    for cit_type in _CITATION_TYPES:
        total = 0
        missing_path = []   # base not in paths.json
        missing_file = []   # path registered but file gone
        for link in session.active_links(cit_type):
            for target in link.to_set:
                total += 1
                base = _walk_to_base(session, target)
                if base not in addr_to_path:
                    missing_path.append((link.addr, target, base))
                    continue
                rel = addr_to_path[base]
                if not (lattice_root / rel).exists():
                    missing_file.append((link.addr, target, base, rel))

        if missing_path:
            sample = ", ".join(
                f"link={l} target={t} base={b}"
                for l, t, b in missing_path[:_SAMPLE_SIZE]
            )
            extra = (
                f" (+{len(missing_path) - _SAMPLE_SIZE} more)"
                if len(missing_path) > _SAMPLE_SIZE else ""
            )
            yield Issue(
                severity=Severity.ERROR,
                check=CHECK_NAME,
                message=(
                    f"{cit_type}: {len(missing_path)}/{total} citations "
                    f"with no registered base; sample: {sample}{extra}"
                ),
            )

        if missing_file:
            sample = ", ".join(
                f"link={l} base={b} path={p}"
                for l, _, b, p in missing_file[:_SAMPLE_SIZE]
            )
            extra = (
                f" (+{len(missing_file) - _SAMPLE_SIZE} more)"
                if len(missing_file) > _SAMPLE_SIZE else ""
            )
            yield Issue(
                severity=Severity.WARNING,
                check=CHECK_NAME,
                message=(
                    f"{cit_type}: {len(missing_file)}/{total} citations "
                    f"whose target file is missing on disk; "
                    f"sample: {sample}{extra}"
                ),
            )
