"""Substrate Store — lattice-bound facade over State + JSONL persistence.

Plus the agent-attribution helpers (`default_store`, `agent_context`,
`attributed_to`) ported from `lib.store.store`. Orchestrators set
`XANADU_AGENT_DOC` to bind a process to an agent identity; `default_store`
returns an `AttributingStore` that auto-emits `manages` for every link.

The legacy `scripts/lib/store/store.py::Store` is path-keyed and
manages a JSONL log + SQLite index. This Store is the tumbler-keyed
equivalent: same semantic role (the substrate's IO boundary) but
operates on tumbler addresses throughout.

Reads on init from a lattice's `_docuverse/{links.jsonl, paths.json}`,
materializing a State pre-populated with all migrated links and a
TypeRegistry anchored at the registry doc address. Writes go to
State.make_link AND append to the on-disk JSONL.

This Store is intentionally simpler than the legacy:
- No SQLite indexing yet — in-memory queries over the LinkStore
  are fast enough at current scale (~7K links). Add SQLite back
  if/when needed.
- No content-derived hash IDs — link IDs ARE tumbler addresses,
  guaranteed unique by T10a allocator discipline.
- Path↔tumbler translation is exposed via helpers but not folded
  into the query API. Callers translate explicitly.
"""

from __future__ import annotations

import fcntl
import json
import os
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from .addressing import Address
from .links import Link
from .persist import load_jsonl
from .state import State, TypeArg


_REGISTER_PATH_LOCK_FILE = ".register_path.lock"


@contextmanager
def _register_path_lock(docuverse_dir: Path):
    """Cross-process file lock for register_path's allocate-and-persist
    sequence. Prevents two processes on the same machine from allocating
    the same address while concurrently writing paths.json.

    Blocks until the lock is acquired. The lock file lives in the
    docuverse dir (the same dir that contains paths.json + links.jsonl)
    so the lock is scoped to the substrate it protects.
    """
    docuverse_dir.mkdir(parents=True, exist_ok=True)
    lock_path = docuverse_dir / _REGISTER_PATH_LOCK_FILE
    fd = os.open(str(lock_path), os.O_RDWR | os.O_CREAT, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)


def _utcnow_unix() -> int:
    """Current UTC time as Unix epoch seconds (int).

    Replaces the prior ISO-string format. Numeric storage is more
    compact and faster to compare; ts is scoped to agentic concerns
    per `feedback_ts_scoped_to_agentic.md`.
    """
    import time
    return int(time.time())


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Store:
    """Lattice-bound substrate store.

    Loads `_docuverse/{links.jsonl, paths.json}` from a lattice
    directory; exposes State-shaped queries; appends new links to
    JSONL on write.
    """

    def __init__(
        self,
        lattice_dir: str | Path,
        *,
        account: Address = None,
    ) -> None:
        self.lattice_dir = Path(lattice_dir)
        self.docuverse = self.lattice_dir / "_docuverse"
        # Unified-docuverse migration: the substrate now lives at repo
        # root rather than under each lattice. If no _docuverse/ is
        # found at lattice_dir, walk up to WORKSPACE root.
        if not self.docuverse.exists():
            from lib.shared.paths import WORKSPACE
            self.lattice_dir = WORKSPACE
            self.docuverse = WORKSPACE / "_docuverse"
        self.jsonl_path = self.docuverse / "links.jsonl"
        self.paths_path = self.docuverse / "paths.json"

        if not self.paths_path.exists():
            raise FileNotFoundError(
                f"paths.json not found at {self.paths_path} — has the "
                f"substrate been migrated? Run scripts/migrate-to-tumbler.py."
            )
        with open(self.paths_path) as f:
            paths_data = json.load(f)
        self._meta = paths_data["_meta"]
        self.path_to_addr: Dict[str, Address] = {
            p: Address(t) for p, t in paths_data["paths"].items()
        }
        self.addr_to_path: Dict[Address, str] = {
            a: p for p, a in self.path_to_addr.items()
        }

        # Bootstrap State at the registry doc address recorded in
        # paths.json. Account is implied by the registry's location:
        # registry_doc = inc(account, 2) + 1, so account is registry_doc
        # truncated to 4 components.
        registry_doc = Address(self._meta["registry_doc"])
        if account is None:
            # Reverse-derive: registry doc has zeros=2 (doc-level); the
            # account address is the registry's user-prefix (zeros=1).
            account = self._account_from_registry(registry_doc)

        self.state = State(account=account)
        # Discard the State's auto-bootstrapped registry doc and replace
        # the link store with the loaded one. The State's allocator state
        # cursor is now misaligned with what's persisted, but we don't
        # need create_doc / create_version for read-only queries; for
        # writes, we'll allocate via make_link's per-homedoc allocator
        # which tracks each homedoc's link subspace independently.
        self.state.links = load_jsonl(self.jsonl_path)

        # Re-register every doc address so make_link can locate
        # homedoc-owning allocators. The persisted links don't tell us
        # which addresses are docs vs links, but we know docs have
        # zeros=2 and links have zeros=3.
        self._reattach_doc_owners()

    def __enter__(self) -> "Store":
        return self

    def __exit__(self, *args) -> None:
        return None

    def close(self) -> None:
        """No-op for legacy callers expecting a closeable handle.
        The substrate is in-memory + on-disk JSONL; nothing to release."""
        return None

    @property
    def lattice_doc(self) -> Address:
        return Address(self._meta["lattice_doc"])

    @property
    def registry_doc(self) -> Address:
        return Address(self._meta["registry_doc"])

    @property
    def lattice_name(self) -> str:
        return self._meta.get("lattice_name", "")

    # ----- path↔tumbler translation -----

    def addr_for_path(self, path: str) -> Address:
        if path not in self.path_to_addr:
            raise KeyError(f"path not in path map: {path!r}")
        return self.path_to_addr[path]

    def path_for_addr(self, addr: Address) -> Optional[str]:
        return self.addr_to_path.get(addr)

    # ----- queries -----

    def find_links(
        self,
        from_set: Optional[Iterable[Address]] = None,
        to_set: Optional[Iterable[Address]] = None,
        type_: Optional[TypeArg] = None,
        homedoc: Optional[Address] = None,
    ) -> List[Link]:
        return self.state.find_links(
            from_set=from_set, to_set=to_set, type_=type_, homedoc=homedoc,
        )

    def get(self, addr: Address) -> Link:
        return self.state.links.get(addr)

    # ----- registration -----

    def register_path(self, path: str) -> Address:
        """Get-or-allocate a tumbler for a filesystem path.

        If the path is already in the path map, return its tumbler.
        Otherwise allocate a fresh doc-level tumbler, persist the
        updated map, and emit a `lattice` link recording the doc's
        membership in this lattice.

        Callers should pass lattice-relative paths.

        Cross-process safety: the allocate-and-persist sequence runs
        under a file lock (`.register_path.lock` in the docuverse
        dir). Before allocating, re-reads paths.json from disk to
        pick up any allocations another process committed while this
        process was waiting. Prevents two concurrent runners from
        allocating the same address.
        """
        if path in self.path_to_addr:
            return self.path_to_addr[path]
        with _register_path_lock(self.docuverse):
            # Another process may have allocated this path or other
            # paths while we were waiting for the lock. Refresh.
            self._refresh_path_map_from_disk()
            if path in self.path_to_addr:
                return self.path_to_addr[path]
            # Allocate doc address without auto-emitting any classifier
            addr = self.state._emit(self.state.doc_allocator)
            self.state.parent[addr] = None
            self.state.kind[addr] = "doc"
            self.state.content[addr] = ""
            self.path_to_addr[path] = addr
            self.addr_to_path[addr] = path
            self._persist_paths()
            # Emit lattice membership through Store.make_link so it lands
            # in the JSONL.
            self.make_link(
                homedoc=addr,
                from_set=[addr],
                to_set=[self.lattice_doc],
                type_="lattice",
            )
            return addr

    def _refresh_path_map_from_disk(self) -> None:
        """Re-read paths.json and absorb any new path→addr mappings.

        Called inside `register_path`'s lock to pick up other
        processes' allocations. Advances the doc_allocator's cursor
        past any new addresses we discover under the active account's
        subspace, so the next allocation doesn't collide.

        Existing in-memory mappings are preserved (we only ADD;
        nothing is removed). New addresses get a minimal owner
        registration so subsequent operations (make_link, etc.) can
        find them.
        """
        try:
            with open(self.paths_path) as f:
                paths_data = json.load(f)
        except (OSError, json.JSONDecodeError):
            return
        on_disk = paths_data.get("paths") or {}
        active_base_len = len(self.state.doc_allocator.base.digits)
        account_prefix = self.state.doc_allocator.base.digits[:-1]
        max_position = self.state.doc_allocator._cursor.digits[-1] if hasattr(
            self.state.doc_allocator, "_cursor"
        ) and self.state.doc_allocator._cursor is not None else 0
        for p, addr_str in on_disk.items():
            if p in self.path_to_addr:
                continue
            addr = Address(addr_str)
            self.path_to_addr[p] = addr
            self.addr_to_path[addr] = p
            self.state._owner.setdefault(addr, self.state.doc_allocator)
            self.state.parent.setdefault(addr, None)
            self.state.kind.setdefault(addr, "doc")
            self.state.content.setdefault(addr, "")
            # Track high-water mark for the allocator's cursor in the
            # active account's subspace.
            if (
                len(addr.digits) == active_base_len
                and addr.digits[:-1] == account_prefix
            ):
                max_position = max(max_position, addr.digits[-1])
        # Advance cursor past the new high-water mark
        if max_position > 0:
            target = Address(
                self.state.doc_allocator.base.digits[:-1]
                + (max_position + 1,)
            )
            try:
                cur_cursor = self.state.doc_allocator._cursor
                cur_pos = cur_cursor.digits[-1] if cur_cursor else 0
                if max_position >= cur_pos:
                    self.state.doc_allocator._cursor = target
            except (AttributeError, IndexError):
                pass

    def register_version(self, addr: Address) -> Address:
        """Advance the supersession chain for `addr`'s doc by one.

        Per LM 4/52-4/53. Walks `addr`'s parent-map descendants to find
        the current chain head, then allocates a tumbler-child of the
        head and emits a `supersession(head, new_addr)` link.

        The new address is a bare marker — no classifier, no lattice
        membership, no path mapping. Existing relations (descriptions,
        citations, attributes, comments) all continue to point at the
        prior addresses; readers walk the supersession chain when they
        need to know whether the base has been edited.

        Resolving to head before allocating produces a linear chain:
        identity → v1 → v2 → v3 → … . `supersession_chain_length`
        grows monotonically with each call (load-bearing for sidecar
        freshness predicates that compare chain lengths). Callers may
        pass any address along the chain (identity, current head, or a
        stale version reference); the chain always extends from the
        current head.

        Returns the new version's address.
        """
        if addr not in self.state._owner:
            raise ValueError(f"unknown doc address {addr}")

        # Walk to current chain head — deepest descendant via the
        # parent map. If the chain is already linear (each node has
        # at most one child), this picks the leaf; if a fan-out
        # exists from earlier versions, picks the highest-tumbler
        # child at each step (matching version_head's algorithm).
        head = addr
        while True:
            children = sorted(
                (a for a, p in self.state.parent.items() if p == head),
                key=lambda a: a.digits,
            )
            if not children:
                break
            head = children[-1]

        new_addr = self.state._allocate_child(head)
        self.state.parent[new_addr] = head
        self.state.kind[new_addr] = self.state.kind.get(head, "doc")
        self.state.content[new_addr] = ""

        from .emit import emit_supersession
        emit_supersession(self, head, new_addr)

        return new_addr

    def _persist_paths(self) -> None:
        """Write the current path map back to paths.json."""
        out = {
            "_meta": self._meta,
            "paths": {
                p: str(a) for p, a in sorted(self.path_to_addr.items())
            },
        }
        with open(self.paths_path, "w") as f:
            json.dump(out, f, indent=2, sort_keys=True)

    # ----- writes -----

    def make_link(
        self,
        homedoc: Address,
        from_set: Iterable[Address],
        to_set: Iterable[Address],
        type_: TypeArg,
    ) -> Link:
        ts = _utcnow_unix()
        link = self.state.make_link(homedoc, from_set, to_set, type_, ts=ts)
        self._append_record(link, ts=ts)
        return link

    # ----- internals -----

    def _account_from_registry(self, registry_doc: Address) -> Address:
        """Recover the account address from the registry doc address.

        The registry doc was emitted as the first sibling at the doc
        allocator's base = inc(account, 2). For a doc-allocator base
        of N.0.U.0.D.0.1, the account is N.0.U.0.D — but we usually
        want the *user* address (zeros=1) such that inc(user, 2) = base.
        """
        # registry_doc has zeros=2; the user (account) has zeros=1.
        # registry_doc = account.0.D.0.1 — drop the trailing .0.D.
        # In our default bootstrap account=1.1.0.1, registry_doc=1.1.0.1.0.1.
        # Drop the last 2 digits (the .0.1 element-field appendix from
        # inc(account, 2) which means .0.<position>=.0.1 since position 1).
        digits = registry_doc.digits
        if registry_doc.zeros() == 2 and len(digits) >= 2 and digits[-2] == 0:
            return Address(digits[:-2])
        # Fallback: trust caller-provided default
        return Address("1.1.0.1")

    def _reattach_doc_owners(self) -> None:
        """After load_jsonl, the State's _owner and parent maps are empty.
        Re-register every doc address (zeros=2) under the global doc
        allocator, every link address (zeros=3) under its homedoc's link
        allocator, and every supersession-link target as a child of its
        from-side parent. Without this, make_link can't allocate fresh
        links, create_doc would re-use already-taken positions, and
        `version_head` would return the base address for any doc
        versioned in a prior session (the supersession chain in
        `links.jsonl` survived but the in-memory parent map didn't).

        High-water mark for the doc-allocator cursor is computed only
        over addresses in the **active account's** subspace. With
        multiple authors co-residing in one substrate, considering all
        addresses would advance the cursor past the OTHER author's
        max — which would cause new allocations to land in the wrong
        author's tumbler space.
        """
        from .allocator import Allocator
        from .predicates import active_links as _active_links
        from .state import link_subspace_base

        active_base_len = len(self.state.doc_allocator.base.digits)
        # Account user-prefix: doc_allocator.base is inc(account, 2) =
        # account.digits + (0, 1). Strip the trailing (0, 1) to get the
        # account user-address. The user-prefix that account-owned doc
        # addresses begin with is account.digits + (0,).
        account_prefix = self.state.doc_allocator.base.digits[:-1]

        max_doc_position = 0
        for link in self.state.links:
            for endset in (link.from_set, link.to_set, (link.addr,)):
                for a in endset:
                    if a.zeros() == 2:
                        # Doc address — register under doc_allocator
                        self.state._owner.setdefault(a, self.state.doc_allocator)
                        # Track high-water mark only for docs in the
                        # active account's subspace (same prefix +
                        # length).
                        if (
                            len(a.digits) == active_base_len
                            and a.digits[:-1] == account_prefix
                        ):
                            max_doc_position = max(max_doc_position, a.digits[-1])

        # Advance doc_allocator's cursor past all known docs so future
        # create_doc calls don't collide.
        if max_doc_position > 0:
            from .addressing import inc
            target = Address(
                self.state.doc_allocator.base.digits[:-1] + (max_doc_position + 1,)
            )
            self.state.doc_allocator._cursor = target

        # Per-homedoc link allocators
        for link in self.state.links:
            homedoc = link.homedoc
            if homedoc not in self.state._link_allocators:
                self.state._link_allocators[homedoc] = Allocator(
                    link_subspace_base(homedoc)
                )
            # Advance link allocator past this link's position
            link_alloc = self.state._link_allocators[homedoc]
            # Link's last digit is its position in the link subspace.
            # Advance cursor to next sibling beyond the highest seen.
            current_pos = link.addr.digits[-1]
            cursor_pos = link_alloc._cursor.digits[-1]
            if current_pos >= cursor_pos:
                link_alloc._cursor = Address(
                    link_alloc._cursor.digits[:-1] + (current_pos + 1,)
                )
            self.state._owner[link.addr] = link_alloc

        # Reconstruct the version-parent map from active supersession
        # links. Each supersession(from=parent, to=child) records one
        # parent edge; ignore retracted ones. Without this, version_head
        # walks an empty/incomplete parent map after reload and returns
        # the base address for any doc versioned in a prior session.
        for link in _active_links(self.state, "supersession"):
            if not link.from_set or not link.to_set:
                continue
            parent_addr = link.from_set[0]
            child_addr = link.to_set[0]
            self.state.parent[child_addr] = parent_addr
            self.state.kind.setdefault(
                child_addr, self.state.kind.get(parent_addr, "doc"),
            )
            self.state.content.setdefault(child_addr, "")

    def _append_record(self, link: Link, ts: int) -> None:
        record = {
            "op": "create",
            "id": str(link.addr),
            "from_set": [str(a) for a in link.from_set],
            "to_set": [str(a) for a in link.to_set],
            "type_set": [str(a) for a in link.type_set],
            "ts": ts,
        }
        with open(self.jsonl_path, "a") as f:
            f.write(json.dumps(record, sort_keys=True) + "\n")


