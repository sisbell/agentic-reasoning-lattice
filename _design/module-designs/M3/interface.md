# M3 — Interface (for dependents)

M3 owns the authoritative permanent name space: it mints every fresh, globally-unique, T4-valid address, records which entities (nodes, accounts, documents) exist, and answers *"is this allocated?"* and *"who owns this?"* by prefix. It owns identity, not content.

## Public interface

All types `Tumbler`/`Address`/`Level`/`Span`/`Nat` are M1's; `Kernel`/`Snapshot`/`LockKey`/`Seq`/`TxnError` are M2's. M3State is reached through a named accessor trait the engine implements; the write path is its mirror bound.

```rust
pub trait HasM3 { fn m3(&self) -> &M3State; }   // engine: W: WorldState + HasM3
// Write path: transact-driving B-ops are bound `where W::Record: From<M3Rec>` and stage via `stg.push(rec.into())`.
```

```rust
#[derive(Clone, Copy, PartialEq, Eq, Hash, Debug)]
pub struct PrincipalId(pub u64);                 // opaque external identity, supplied by M10/session
#[derive(Clone)] pub struct Principal { pub id: PrincipalId, pub prefix: Address }  // prefix: T4-valid, zeros ≤ 1
pub const BOOTSTRAP_PRINCIPAL: PrincipalId = PrincipalId(0);  // π₀'s fixed id (genesis)

pub enum MintError    { HomeNotRegistered, SourceNotRegistered, NotAnAccount, Gate(GateViolation) }
pub enum OpError      { NotOwner, Mint(MintError) }
pub enum DelegateError{ DelegatorUnknown, DuplicateId, NotAncestor, NotAuthorized, NotAccountTier,
                        NotTopDown, NotFresh, NotNextForm, NotValid, ParentNotRegistered }
pub enum NodeError    { NotValid, NotNode, NotFresh, NotDescendantOfBootstrap }
```

### A. Frontier allocation — *pure, composable* (folded into M5/M7 composites)

Each returns the minted address and the one journal delta the caller stages; the caller takes the matching `LockKey` from the `*_lock_key` constructor **before** opening the closure.

```rust
impl M3State {
    /// Next content address under d: namespace (b_C(d), 1), element field [s_C, m+1]. [M5: INSERT]
    pub fn mint_content(&self, home: &Address)    -> Result<(Address, M3Rec), MintError>;
    /// Next link address under d: namespace (b_L(d), 1), element field [s_L, m+1]. [M7: MAKELINK]
    pub fn mint_link(&self, home: &Address)        -> Result<(Address, M3Rec), MintError>;
    /// Next version identity: namespace (source, 1) — the version chain, kept SEPARATE
    /// from the document chain. [M5: owned CREATENEWVERSION]
    pub fn mint_version(&self, source: &Address)   -> Result<(Address, M3Rec), MintError>;
    /// Next document identity under an account: namespace (account, 2).
    /// [CREATENEWDOCUMENT; cross-owner VERSION; fork]
    pub fn mint_document(&self, account: &Address) -> Result<(Address, M3Rec), MintError>;

    /// Namespace LockKey for transact's `keys` arg (call before the closure; the mint advances the same key).
    pub fn content_lock_key(home: &Address)      -> LockKey;   // = (b_C(home), 1)
    pub fn link_lock_key(home: &Address)         -> LockKey;   // = (b_L(home), 1)
    pub fn version_lock_key(source: &Address)    -> LockKey;   // = (source, 1)
    pub fn document_lock_key(account: &Address)  -> LockKey;   // = (account, 2)
    /// The single principal-registry key. Load-bearing in `delegate`; defensive in create_new_document.
    pub fn principals_lock_key()                 -> LockKey;   // Space::Principals tag
    /// Coarse node-registry key — held by register_node so a concurrent duplicate surfaces NotFresh.
    pub fn node_lock_key()                       -> LockKey;   // Space::Nodes tag
}
```

### B. Entity operations — *transact-wrapped* (M3 drives the transaction; called by M10)

```rust
impl<W: WorldState + HasM3> Namespace<W> where W::Record: From<M3Rec> {
    /// Baptize a fresh empty document under `account`. Authorization by EFFECTIVE owner (ω).
    /// Registers d in the entity set; does NOT write M5's arrangement (lazy).
    /// Returns the address and its commit Seq only after commit (commit-before-acknowledge). [ASN-0103]
    pub fn create_new_document(&self, caller: PrincipalId, account: &Address)
        -> Result<(Address, Seq), TxnError<OpError>>;

    /// Delegation: O15 five-condition gate (with (iii) narrowed to zeros == 1) PLUS id-freshness
    /// PLUS P8 (parent registered) PLUS next-form — then baptize the new account prefix AND register
    /// the principal in ONE transaction. Returns the new account address and its commit Seq. [ASN-0042]
    pub fn delegate(&self, delegator: PrincipalId, new_prefix: Tumbler, new_id: PrincipalId)
        -> Result<(Address, Seq), TxnError<DelegateError>>;

    /// Admit an externally-originated node (NodeBaptism: validate freshness + n₀-lineage; address
    /// chosen by provisioning, not minted here). Returns the node address and its commit Seq. [ASN-0047]
    pub fn register_node(&self, addr: Tumbler) -> Result<(Address, Seq), TxnError<NodeError>>;

    /// Denial-as-fork, allocation half (O10, account-tier case): a fresh document in the caller's OWN
    /// account. Account-tier caller only — a node-tier caller gets Mint(NotAnAccount). Returns
    /// create_new_document's (Address, Seq).
    pub fn fork(&self, caller: PrincipalId) -> Result<(Address, Seq), TxnError<OpError>>;
}
```

### C. Queries — *pure methods* (read off any M2 `Snapshot`; write nothing)

```rust
impl M3State {
    pub fn is_allocated(&self, a: &Address) -> bool;            // any namespace incl. content/link
    pub fn entity_level(&self, a: &Address) -> Option<Level>;   // Some iff registered entity (zeros ≤ 2)
    pub fn is_registered_document(&self, d: &Address) -> bool;  // == entity_level == Some(Document)
    pub fn effective_owner(&self, a: &Address) -> Option<Principal>;  // ω(a), longest-prefix match;
                                                                     // valid even when a is not allocated
    /// Resolve a principal by its opaque id. Single-valued (delegate enforces id-freshness).
    pub fn principal_by_id(&self, id: PrincipalId) -> Option<Principal>;
    pub fn principal_prefix(&self, id: PrincipalId) -> Option<Address>;   // principal_by_id(id).map(|p| p.prefix)
    /// Peek the next delegable account-tier prefix under `parent` — the exact value delegate
    /// will demand as next-form. None if `parent` is neither node nor account, or the gate trips.
    pub fn next_account_prefix(&self, parent: &Address) -> Option<Address>;
    pub fn owns(prefix: &Address, a: &Address) -> bool; // O1; pure two-tumbler prefix test
}
```

### D. Genesis

```rust
impl M3State { pub fn genesis() -> M3State; }   // nodes={[1]}, frontiers={}, Π={ [1] → Principal{BOOTSTRAP_PRINCIPAL,[1]} }
```

## Caller contracts & obligations

**Frontier allocation (A) — pure mints:**
- Caller must hold the matching `*_lock_key(..)` (taken **before** opening the closure) for the transact `keys` arg; the mint runs **inside** the closure off `stg.working().m3()` and the caller stages the returned `M3Rec` via `stg.push(rec.into())`.
- `mint_content`/`mint_link`: `Err(MintError::HomeNotRegistered)` if `home` is not a registered document. On success the element-field subspace distinguishes content (`s_C`) from link (`s_L`) — disjoint by construction.
- `mint_version`: `Err(MintError::SourceNotRegistered)` if `source` is not a registered Document (covers both unregistered address and registered non-document).
- `mint_document`: `Err(MintError::NotAnAccount)` if `account` is not a registered Account.
- All mints: `Err(MintError::Gate(..))` only on a corrupted frontier. **Every returned Address is T4-valid.** Successive mints in one composite each see the prior mint (working state).
- The held lock key ≡ the advanced frontier key byte-for-byte; the three g=1 chains under one document (content, link, version) get distinct locks — caller must use the precise `*_lock_key`, never a coarser `(home_doc, g)` pair.

**Entity ops (B) — transact-wrapped:**
- Each returns `(Address, Seq)` **only after commit** (commit-before-acknowledge); `Seq` is the linearization coordinate. Each opens exactly one `transact`.
- `create_new_document(caller, account)`: `TxnError::Rejected(OpError::NotOwner)` if `effective_owner(account)` is absent or names another principal. Registers d only — **does NOT** write M5's arrangement. No idempotency key: a retried lost-ack yields a harmless orphan empty document.
- `delegate(delegator, new_prefix, new_id)`: rejections `NotValid` (T4-invalid prefix), `DelegatorUnknown`, `NotAccountTier` (zeros ≠ 1), `DuplicateId` (reused id), `NotAncestor`, `NotAuthorized`, `NotTopDown`, `NotFresh`, `ParentNotRegistered`, `NotNextForm`. Always produces an **account** (zeros=1) and one new principal. Caller obtains a valid `new_prefix` from `next_account_prefix(parent)` to avoid guess-and-retry. Caller must supply a fresh `new_id` (id uniqueness is now enforced in M3, not M10).
- `register_node(addr)`: caller supplies the address (minted externally by provisioning). Rejections `NotValid`, `NotNode`, `NotFresh`, `NotDescendantOfBootstrap` (requires `[1] ≼ addr`).
- `fork(caller)`: account-tier caller only — unknown id returns `Err(TxnError::Rejected(OpError::NotOwner))` opening **no** transaction; a node-tier caller gets `Mint(MintError::NotAnAccount)`. Mints a fresh document under the caller's own account-tier prefix; M5 wires shared content separately.

**Queries (C) — pure, read off any Snapshot:**
- `is_allocated` reflects *minting*, never byte-presence — a registered-empty document is `true` (a valid addressable ghost). Content existence is M4's separate axis.
- `effective_owner` is valid even when `a` is not yet allocated; `None` if no covering principal. **Authorization must use ω (longest match), never bare `owns`** — a node operator's prefix contains delegated accounts, so multiple principals' `owns` are simultaneously true; only ω arbitrates.
- `entity_level`: `None` for unregistered or for Element-level (content/link — use `is_allocated`).
- `principal_by_id`/`principal_prefix`: `None` for an unknown id; single-valued (delegate's id-freshness). Resolved prefix is value-stable across snapshots (prefixes immutable, principals persist).
- `next_account_prefix`: `None` if `parent` is neither node nor account, or the namespace gate trips; the returned prefix still faces delegate's full in-closure gate (racing peeks leave exactly one winner).

**Invariants a caller may rely on:** every minted/returned Address is T4-valid; registry is append-only (no delete API); allocations are contiguous/gap-free; one id ↦ at most one principal; ownership is exclusive under ω.

## Seams exposed downstream

Consumers reach `&self` methods via `HasM3::m3()` — `stg.working().m3()` inside a composite, `snapshot.world().m3()` for a read; `*_lock_key` are called on the type.
- **→ M5:** `is_registered_document(d)` (edit precondition); `effective_owner(d_src)` (VERSION owned-vs-cross-owner branch — owned ⇒ `mint_version` on `(d_src,1)`; cross-owner ⇒ `principal_prefix(forker_id)` → `mint_document(pfx(π))` on `(pfx(π),2)`); the pure mints `mint_content` (INSERT), `mint_version`/`mint_document` (VERSION), each with its matching `*_lock_key` taken before the closure; `is_allocated(a)` (content-side referential-integrity oracle for COPY). M5 must **pre-read `ω(d_src)` off a snapshot** before opening the closure (it is stable for an existing `d_src`), holds the single matching namespace lock, needs **no** `principals_lock_key`.
- **→ M7:** `mint_link` pure (inside MAKELINK; lock via `link_lock_key(d)` before the closure, then stage the returned `M3Rec`); `is_registered_document(d)` (link's home).
- **→ M6, M8:** `is_registered_document(d)` — they convert *registered-but-no-arrangement* → ⟨⟩ and *unregistered* → fail. M3 supplies the bool; the ⟨⟩-vs-fail query semantics are theirs.
- **→ M9:** `effective_owner`/`is_registered_document` (residence resolution); pred-def content allocated indirectly via M5 (M9→M5→M3).
- **→ M10:** dispatches `create_new_document`/`delegate`/`register_node`/`fork`; each returns `(Address, Seq)` surfaced as the linearization coordinate; binds the bootstrap session to `BOOTSTRAP_PRINCIPAL`; may resolve a session's prefix via `principal_prefix`; may peek the next delegable prefix via `next_account_prefix(node)`.

## Boundary — NOT provided here

- No byte storage (M4), no arrangements (M5), no link values (M7) — identity only.
- Does **not** materialize a new document's arrangement (lazy, M5) — `create_new_document` registers d and stops.
- Does **not** originate node addresses (provisioning/NodeBaptism mints them externally; M3 only validates via `register_node`).
- Does **not** run the request lifecycle or bind sessions to principals (M10).
- No delete/revoke API (registry is append-only, prefixes immutable).
- No node-tier `fork` and no per-node principals beyond bootstrap (delegation is account-tier only).
- No internal WAL/ordering/durability of its own — it rides M2's `transact`/`snapshot`.
