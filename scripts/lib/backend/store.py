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

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from .addressing import Address
from .links import Link
from .persist import load_jsonl
from .state import State, TypeArg


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
        """
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

    def register_version(self, prev_addr: Address) -> Address:
        """Allocate a new tumbler version marker for an existing doc.

        Per LM 4/52-4/53. Emits a `supersession(prev_addr, new_addr)`
        link recording that an edit happened. The new address is a
        bare marker — no classifier, no lattice membership, no path
        mapping. Existing relations (descriptions, citations,
        attributes, comments) all continue to point at prev_addr;
        readers walk the supersession chain when they need to know
        whether the base has been edited.

        Mirror of how Xanadu inherits links via supersession rather
        than copying them. The new version exists only to mark the
        progression — the real substrate facts stay on the base.

        Returns the new version's address.
        """
        if prev_addr not in self.state._owner:
            raise ValueError(f"unknown doc address {prev_addr}")

        new_addr = self.state._allocate_child(prev_addr)
        self.state.parent[new_addr] = prev_addr
        self.state.kind[new_addr] = self.state.kind.get(prev_addr, "doc")
        self.state.content[new_addr] = ""

        from .emit import emit_supersession
        emit_supersession(self, prev_addr, new_addr)

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
        link = self.state.make_link(homedoc, from_set, to_set, type_)
        self._append_record(link, ts=_utcnow_iso())
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
        """After load_jsonl, the State's _owner map is empty. Re-register
        every doc address (zeros=2) under the global doc allocator and
        every link address (zeros=3) under its homedoc's link allocator.
        Without this, make_link can't allocate fresh links and create_doc
        would re-use already-taken positions.
        """
        from .allocator import Allocator
        from .state import link_subspace_base

        max_doc_position = 0
        for link in self.state.links:
            for endset in (link.from_set, link.to_set, (link.addr,)):
                for a in endset:
                    if a.zeros() == 2:
                        # Doc address — register under doc_allocator
                        self.state._owner.setdefault(a, self.state.doc_allocator)
                        # Track high-water mark of doc-allocator position
                        # (last element of the doc-field).
                        # The doc address has form <user>.0.<doc_field>;
                        # the last digit of doc_field is the sibling position
                        # for a top-level doc. For deeper versions we'd
                        # need a different rule — defer for now.
                        if len(a.digits) == len(self.state.doc_allocator.base.digits):
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

    def _append_record(self, link: Link, ts: str) -> None:
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


