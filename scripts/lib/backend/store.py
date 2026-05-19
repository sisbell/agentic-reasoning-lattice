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
import re
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from .addressing import Address
from .links import Link
from .persist import load_jsonl
from .state import State, TypeArg


_REGISTER_PATH_LOCK_FILE = ".register_path.lock"

# Path-prefix regex for substrate auto-routing. Lattice docs live at
# `_docuverse/documents/<node>/<user>/...` where <node> is a
# dot-separated address head (`1.1`, `1.3`, …) and <user> is one or
# more digits (`1`). register_path uses this to pick the right doc
# allocator from `State._doc_allocators` — emissions at `1.3/1/...`
# allocate from the (1.3, 1) account instead of the primary one.
_NODE_USER_PATH_RE = re.compile(
    r"^_docuverse/documents/([0-9]+(?:\.[0-9]+)*)/([0-9]+)/"
)


def _parse_node_user_from_path(path: str) -> Optional[Tuple[str, str]]:
    """Extract `(node, user)` from a substrate-relative path.

    Returns None if the path doesn't match the substrate doc layout —
    such paths fall back to the primary account's allocator.
    """
    m = _NODE_USER_PATH_RE.match(path)
    if m is None:
        return None
    return m.group(1), m.group(2)


def _account_from_node_user(node: str, user: str) -> Address:
    """Build the user-level account address for a (node, user) pair.

    The substrate's account = `<node>.0.<user>`, e.g. ("1.1", "1") →
    `1.1.0.1`. Always has `zeros()==1` (one zero separator between
    node and user fields).
    """
    return Address(f"{node}.0.{user}")


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


_EMIT_LOCK_FILE = ".link_emit.lock"


@contextmanager
def _emit_lock(docuverse_dir: Path):
    """Cross-process lock around a single link emission.

    Prevents two workers from claiming the same id from a shared
    per-homedoc allocator (e.g., agent doc's link allocator). Before
    emitting, the caller holds this lock, scans all worker pending
    files for the highest position already claimed under the allocator
    base, advances the in-memory cursor past it, and only then emits.

    The lock is held for microseconds (a pending-file scan + cursor
    update + one append). Cross-worker contention is negligible at
    typical fire rates (5-20 emissions per fire, fire every 60-1800s).

    Scoped per docuverse dir so multiple lattices (if ever) get
    independent locks.
    """
    docuverse_dir.mkdir(parents=True, exist_ok=True)
    lock_path = docuverse_dir / _EMIT_LOCK_FILE
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

        # Per-worker substrate-emission buffer. When CLAUDE_WORKER_INDEX
        # is set (= we're inside a runner worker), emissions are appended
        # to a per-worker pending file under `_workspace/` rather than
        # the canonical jsonl. The commit step (`flush_pending`) holds a
        # short substrate-write lock, appends pending → canonical,
        # truncates pending. Isolates one worker's emissions from
        # another worker's git commit. For non-runner contexts (operator
        # CLIs, tests), pending_jsonl_path is None and emit writes
        # directly to canonical — single-process, no isolation needed.
        from lib.shared.paths import worker_pending_jsonl
        worker_idx = os.environ.get("CLAUDE_WORKER_INDEX")
        self.pending_jsonl_path = (
            worker_pending_jsonl(int(worker_idx))
            if worker_idx is not None and worker_idx != ""
            else None
        )

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
        # Merge any per-worker pending emissions into the in-memory
        # LinkStore so queries see emissions that haven't been flushed
        # to canonical yet. The canonical jsonl is loaded first; per-
        # worker pending files come after and append. At commit time
        # the pending files are flushed → canonical (see
        # `flush_pending`).
        self._merge_pending_into_linkstore()

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
            # Auto-route: pick the doc allocator for this path's
            # (node, user) prefix. Falls back to the primary allocator
            # for paths that don't match the standard substrate layout
            # (legacy or test paths).
            allocator = self._doc_allocator_for_path(path)
            # Allocate doc address without auto-emitting any classifier
            addr = self.state._emit(allocator)
            self.state._set_parent(addr, None)
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

    def _doc_allocator_for_path(self, path: str):
        """Return the State doc allocator for a path's (node, user).

        Parses the substrate-relative path prefix; on match, asks State
        for the corresponding account's allocator (creating one on
        first request). On no match, returns State's primary allocator
        — preserves single-account behavior for paths outside the
        `_docuverse/documents/<node>/<user>/...` layout.
        """
        nu = _parse_node_user_from_path(path)
        if nu is None:
            return self.state.doc_allocator
        node, user = nu
        account = _account_from_node_user(node, user)
        return self.state.get_or_create_doc_allocator(account)

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
        """Allocate a new version of `addr`'s doc — fan-out shape.

        Per LM 4/52-4/53. Walks `addr` up its version-parent chain to
        find the doc's identity (the version root), then allocates a
        sibling-child of identity. The new version is `identity.N`
        where N is the next available sibling — a flat shape rather
        than a chain extension:

            identity                identity
            ├── v1 (= identity.1)   ├── v1
            ├── v2 (= identity.2)   ├── v2
            └── v3 (= identity.3)   └── v3

        Allocating from identity (not from the previous head) keeps
        the parent-map depth at 1 regardless of revision count. At
        N versions, `version_head(identity)` does one `version_children`
        lookup and picks the max-tumbler child — O(1) with the index.
        The prior design walked to head before allocating, producing
        a depth-N linear chain whose walks scaled O(depth × N) and
        became a measurable hot spot on ASN-51's 165-deep chain.

        Existing relations (descriptions, citations, attributes,
        comments) continue to point at the prior addresses; readers
        normalize via walk-up to identity before resolving to head.

        Supersession link emission: `supersession(prior_head, new)`
        where `prior_head` is the highest-tumbler existing sibling
        (or identity itself for the first version). Walking
        supersession links from identity picks the max-tumbler target
        at each step and terminates at the latest version. For docs
        with legacy linear chains (rooted at identity.1), the legacy
        chain stays addressable as historical depth — the new
        sibling supersedes the legacy root, and walks across the new
        edge bypass the legacy descent.

        Callers may pass any address (identity, current head, prior
        version, or — in legacy mixed mode — any node in a deep
        chain); register_version always normalizes to identity before
        allocating, so the new version is uniformly `identity.N`.

        Returns the new version's address.
        """
        if addr not in self.state._owner:
            raise ValueError(f"unknown doc address {addr}")

        # Normalize to identity (version root). For identity-rooted
        # addresses, this is a no-op. For descendant or sibling
        # addresses, walks up via parent map until reaching None.
        identity = addr
        while True:
            parent = self.state.parent.get(identity)
            if parent is None:
                break
            identity = parent

        # Prior head for the supersession FROM target. Empty siblings
        # means this is the first version; the identity itself is the
        # supersession source.
        siblings = self.state.version_children(identity)
        prior_head = siblings[-1] if siblings else identity

        # Reconcile the version-sub-allocator's cursor with existing
        # siblings before emission. Sub-allocators are NOT reconstructed
        # at session load (only doc-level allocators are populated by
        # _reattach_doc_owners), so on the second-or-later versioning
        # of a doc, the freshly-spawned sub-allocator's cursor starts
        # at its base — which equals the existing first sibling's
        # address. Without reconciliation, emit_sibling returns an
        # already-occupied position and emit_supersession lands as a
        # self-loop (prior_head == new_addr). Parallel to
        # _reconcile_link_cursor for link allocators.
        if siblings:
            from .addressing import inc
            owner = self.state._owner[identity]
            child_alloc = owner.get_or_spawn_child(identity, k_prime=1)
            max_existing = siblings[-1]
            while child_alloc._cursor.digits <= max_existing.digits:
                child_alloc._cursor = inc(child_alloc._cursor, 0)

        new_addr = self.state._allocate_child(identity)
        self.state._set_parent(new_addr, identity)
        self.state.kind[new_addr] = self.state.kind.get(identity, "doc")
        self.state.content[new_addr] = ""

        from .emit import emit_supersession
        emit_supersession(self, prior_head, new_addr)

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
        # In worker context, take the cross-process emit lock to keep
        # ID allocation atomic across concurrent workers. Workers share
        # in-memory allocator state separately, so without this lock
        # two workers running parallel fires on the same agent doc both
        # see cursor at N, both emit at N → L11a violation in canonical.
        # The lock briefly (microseconds) serializes the cursor
        # reconcile + emit step.
        if self.pending_jsonl_path is not None:
            with _emit_lock(self.docuverse):
                self._reconcile_link_cursor(homedoc)
                link = self.state.make_link(
                    homedoc, from_set, to_set, type_, ts=ts,
                )
                self._append_record(link, ts=ts)
                return link
        # Single-process (operator CLI, test harness, etc.): no race.
        link = self.state.make_link(homedoc, from_set, to_set, type_, ts=ts)
        self._append_record(link, ts=ts)
        return link

    def _reconcile_link_cursor(self, homedoc: Address) -> None:
        """Advance `homedoc`'s link-allocator cursor past any positions
        already claimed in worker pending files.

        Called under `_emit_lock` immediately before emitting a link
        from `homedoc`'s link allocator. Scans every
        `_workspace/links.worker-*.jsonl` for IDs of the form
        `<homedoc>.0.2.<N>` and, if any exceeds the in-memory cursor,
        advances the cursor past the max. This catches the case where
        another worker emitted in the same allocator since we last
        loaded state — without the catch, both workers would assign
        the same position N.

        Idempotent on no-pending-conflict (cheap fall-through). Bounded
        by per-pending-file size (each ~KB for typical fires).
        """
        from .allocator import Allocator
        from .state import link_subspace_base
        from lib.shared.paths import WORKER_PENDING_DIR

        if not WORKER_PENDING_DIR.exists():
            return

        # Ensure the allocator exists; create if homedoc is new.
        if homedoc not in self.state._link_allocators:
            self.state._link_allocators[homedoc] = Allocator(
                link_subspace_base(homedoc),
            )
        allocator = self.state._link_allocators[homedoc]

        # IDs from this allocator look like `<homedoc>.0.2.<N>`. We need
        # to find the max N across all pending files.
        homedoc_str = str(homedoc)
        id_prefix = f'"id": "{homedoc_str}.0.2.'
        max_pos = 0
        for pending_path in WORKER_PENDING_DIR.glob("links.worker-*.jsonl"):
            try:
                if pending_path.stat().st_size == 0:
                    continue
            except OSError:
                continue
            with open(pending_path) as f:
                for line in f:
                    # Fast prefix check before full JSON parse — most
                    # lines in a pending file are unrelated to this
                    # specific allocator.
                    if id_prefix not in line:
                        continue
                    # Extract the id field's numeric tail.
                    try:
                        idx = line.index(id_prefix) + len(id_prefix)
                        end = line.index('"', idx)
                        n = int(line[idx:end])
                        if n > max_pos:
                            max_pos = n
                    except (ValueError, IndexError):
                        continue

        if max_pos == 0:
            return  # Nothing else has emitted in this allocator yet.

        # Advance cursor past max_pos if not already there. Cursor's
        # last digit is the *next* free position; max_pos is the
        # highest claimed. So cursor should be at least max_pos + 1.
        cursor_pos = allocator._cursor.digits[-1]
        if max_pos >= cursor_pos:
            allocator._cursor = Address(
                allocator._cursor.digits[:-1] + (max_pos + 1,)
            )

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

        # First pass: discover every (node, user) account that has at
        # least one registered path, and create its allocator. Walks
        # path_to_addr so docs registered to paths_json — even ones
        # without links emitted yet — count toward allocator
        # provisioning.
        seen_accounts: set[Address] = set()
        for path in self.path_to_addr:
            nu = _parse_node_user_from_path(path)
            if nu is None:
                continue
            account = _account_from_node_user(*nu)
            if account not in seen_accounts:
                seen_accounts.add(account)
                # Ensures the allocator dict has an entry for this
                # account. Cursor advancement happens in the second
                # pass below.
                self.state.get_or_create_doc_allocator(account)

        # Build a map from each known account → its doc allocator's
        # base prefix (used for matching addresses to accounts in the
        # link scan below). `base.digits == account.digits + (0, 1)`,
        # so the user-prefix on doc addresses is `base.digits[:-1]`.
        account_prefixes: dict[tuple, Allocator] = {
            allocator.base.digits[:-1]: allocator
            for allocator in self.state._doc_allocators.values()
        }
        active_base_len = len(self.state.doc_allocator.base.digits)
        # Track high-water mark per allocator. Each entry maps a
        # user-prefix tuple → max position seen at that prefix.
        max_pos_per_account: dict[tuple, int] = {
            prefix: 0 for prefix in account_prefixes
        }

        for link in self.state.links:
            for endset in (link.from_set, link.to_set, (link.addr,)):
                for a in endset:
                    if a.zeros() != 2:
                        continue
                    # Doc address — assign owner based on its prefix.
                    if (
                        len(a.digits) == active_base_len
                        and a.digits[:-1] in account_prefixes
                    ):
                        owner_allocator = account_prefixes[a.digits[:-1]]
                        self.state._owner.setdefault(a, owner_allocator)
                        max_pos_per_account[a.digits[:-1]] = max(
                            max_pos_per_account[a.digits[:-1]],
                            a.digits[-1],
                        )
                    else:
                        # Doc address outside any known account's
                        # subspace — fall back to primary allocator
                        # for ownership (matches legacy behavior;
                        # tracking these doesn't advance any cursor).
                        self.state._owner.setdefault(
                            a, self.state.doc_allocator,
                        )

        # Advance each allocator's cursor past its account's known
        # high-water mark.
        from .addressing import inc
        for prefix, max_pos in max_pos_per_account.items():
            if max_pos > 0:
                allocator = account_prefixes[prefix]
                target = Address(
                    allocator.base.digits[:-1] + (max_pos + 1,)
                )
                allocator._cursor = target

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
            self.state._set_parent(child_addr, parent_addr)
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
        # Route to per-worker pending file when we're inside a runner
        # worker (CLAUDE_WORKER_INDEX set at Store-init time); otherwise
        # append directly to canonical for one-shot operator scripts /
        # tests. See `flush_pending` for the canonical merge step.
        target = self.pending_jsonl_path or self.jsonl_path
        if self.pending_jsonl_path is not None:
            target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "a") as f:
            f.write(json.dumps(record, sort_keys=True) + "\n")

    # ----- per-worker pending flush -----

    def _merge_pending_into_linkstore(self) -> None:
        """Append every per-worker pending file's content into the
        in-memory LinkStore so queries see unflushed emissions.

        Walks `_workspace/links.worker-*.jsonl` regardless of which
        worker we are — the substrate's logical state is the merge of
        canonical + all live worker buffers.
        """
        from lib.shared.paths import WORKER_PENDING_DIR
        if not WORKER_PENDING_DIR.exists():
            return
        pending_files = sorted(
            WORKER_PENDING_DIR.glob("links.worker-*.jsonl")
        )
        pending_files = [p for p in pending_files if p.stat().st_size > 0]
        if not pending_files:
            return
        # Pre-build a set of canonical addresses for O(1) dedupe lookup.
        seen = {link.addr for link in self.state.links}
        for pending_path in pending_files:
            with open(pending_path) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    addr = Address(data["id"])
                    if addr in seen:
                        continue
                    seen.add(addr)
                    self.state.links.emit(
                        addr,
                        [Address(a) for a in data.get("from_set", [])],
                        [Address(a) for a in data.get("to_set", [])],
                        [Address(a) for a in data.get("type_set", [])],
                        ts=data.get("ts"),
                    )

    def flush_pending(self) -> int:
        """Move emissions from this worker's pending file into canonical.

        No-op when there's no pending file (non-runner context) or the
        pending file is empty. Otherwise: acquire substrate write lock,
        append pending → canonical, truncate pending, release.

        Returns the number of lines flushed.
        """
        if self.pending_jsonl_path is None:
            return 0
        if not self.pending_jsonl_path.exists():
            return 0
        if self.pending_jsonl_path.stat().st_size == 0:
            return 0

        with _register_path_lock(self.docuverse):
            # Re-check size under lock (defensive).
            if (not self.pending_jsonl_path.exists() or
                    self.pending_jsonl_path.stat().st_size == 0):
                return 0
            with open(self.pending_jsonl_path) as src:
                content = src.read()
            flushed_lines = sum(
                1 for line in content.splitlines() if line.strip()
            )
            with open(self.jsonl_path, "a") as dst:
                dst.write(content)
            # Truncate pending. Equivalent to deletion + recreation.
            open(self.pending_jsonl_path, "w").close()
        return flushed_lines


