# M3 — Interface (for dependents)

M3 owns the **authoritative permanent name space**: it mints every fresh, globally-unique, T4-valid address, records which entities (nodes, accounts, documents) exist, and answers *"is this allocated?"* and *"who owns this?"* by prefix. It owns identity, not content.

## Public interface

Indices 1-based (M1 convention). `Tumbler`/`Address`/`Level`/`Span`/`Nat`/`GateViolation` are M1's; `Kernel`/`Snapshot`/`LockKey`/`Seq`/`TxnError` are M2's. `&self` methods are reached through the `HasM3::m3()` accessor — `stg.working().m3()` inside a composite (mints read **working** state so successive mints see prior mints), `snapshot.world().m3()` for a read (queries read **any** snapshot); the `*_lock_key` associated functions are called on the type (`M3State::content_lock_key(..)`), no instance. Mints hand back an `M3Rec` the caller stages via `stg.push(rec.into())` (the `W::Record: From<M3Rec>` bound). `M3State` (M3's `WorldState` slice) and `M3Rec` (M3's journal delta) are otherwise opaque to dependents.

```rust
pub trait HasM3 { fn m3(&self) -> &M3State; }   // engine: W: WorldState + HasM3 — read your store's slice off this

#[derive(Clone, Copy, PartialEq, Eq, Hash, Debug, Serialize, Deserialize)]
pub struct PrincipalId(pub u64);                 // opaque external identity, supplied by M10/session
#[derive(Clone, Serialize, Deserialize)]
pub struct Principal { pub id: PrincipalId, pub prefix: Address }  // prefix: T4-valid, zeros ≤ 1
pub const BOOTSTRAP_PRINCIPAL: PrincipalId = PrincipalId(0);  // π₀'s fixed id (genesis); the ω-auth gate keys on it

pub enum MintError    { HomeNotRegistered, SourceNotRegistered, NotAnAccount, Gate(GateViolation) }
pub enum OpError      { NotOwner, Mint(MintError) }
pub enum DelegateError{ DelegatorUnknown, DuplicateId, NotAncestor, NotAuthorized, NotAccountTier,
                        NotTopDown, NotFresh, NotNextForm, NotValid, ParentNotRegistered }
pub enum NodeError    { NotValid, NotNode, NotFresh, NotDescendantOfBootstrap }
```

### A. Frontier allocation — *pure, composable* (folded into M5/M7 composites)

Each returns the minted address and the one `M3Rec` to stage; the caller takes the matching `LockKey` from the `*_lock_key` constructor **before** opening the closure.

```rust
impl M3State {
    /// Next content address under d: namespace (b_C(d), 1), element field [s_C, m+1]. [M5: INSERT]
    pub fn mint_content(&self, home: &Address)     -> Result<(Address, M3Rec), MintError>;
    /// Next link address under d: namespace (b_L(d), 1), element field [s_L, m+1]. [M7: MAKELINK]
    pub fn mint_link(&self, home: &Address)        -> Result<(Address, M3Rec), MintError>;
    /// Next version identity: namespace (source, 1) — the version chain, kept SEPARATE from the
    /// document chain. [M5: owned CREATENEWVERSION]
    pub fn mint_version(&self, source: &Address)   -> Result<(Address, M3Rec), MintError>;
    /// Next document identity under an account: namespace (account, 2). [CREATENEWDOCUMENT; cross-owner VERSION; fork]
    pub fn mint_document(&self, account: &Address) -> Result<(Address, M3Rec), MintError>;

    /// Namespace LockKey for transact's `keys` arg (call before the closure; the mint advances the same key).
    pub fn content_lock_key(home: &Address)      -> LockKey;   // (b_C(home), 1)
    pub fn link_lock_key(home: &Address)         -> LockKey;   // (b_L(home), 1)
    pub fn version_lock_key(source: &Address)    -> LockKey;   // (source, 1)
    pub fn document_lock_key(account: &Address)  -> LockKey;   // (account, 2)
    /// THE single global principal-registry key (NOT per-subtree). Load-bearing in `delegate`,
    /// defensive in `create_new_document`.
    pub fn principals_lock_key()                 -> LockKey;   // Space::Principals tag
    /// Coarse node-registry key — held by `register_node` so a duplicate surfaces NotFresh.
    pub fn node_lock_key()                       -> LockKey;   // Space::Nodes tag
}
```

### B. Entity operations — *transact-wrapped* (M3 drives the transaction; called by M10)

```rust
impl<W: WorldState + HasM3> Namespace<W> where W::Record: From<M3Rec> {  // holds Arc<Kernel<W>>
    /// Baptize a fresh empty document under `account`; authorization by effective owner ω (not bare
    /// containment). Registers d only — does NOT write M5's arrangement (lazy). Returns (Address, Seq)
    /// post-commit (commit-before-acknowledge).
    pub fn create_new_document(&self, caller: PrincipalId, account: &Address)
        -> Result<(Address, Seq), TxnError<OpError>>;

    /// O15 five-condition gate (with (iii) narrowed to zeros==1) + id-freshness + P8 + next-form;
    /// baptizes the new account prefix AND registers the principal in ONE transaction.
    /// Returns the new account address and its commit Seq.
    pub fn delegate(&self, delegator: PrincipalId, new_prefix: Tumbler, new_id: PrincipalId)
        -> Result<(Address, Seq), TxnError<DelegateError>>;

    /// Admit an externally-originated node (validate freshness + bootstrap lineage; the ADDRESS is
    /// chosen by provisioning, not minted here). Returns the node address and its commit Seq.
    pub fn register_node(&self, addr: Tumbler) -> Result<(Address, Seq), TxnError<NodeError>>;

    /// Denial-as-fork (O10, account-tier case): a fresh document in the caller's OWN account. An
    /// unknown id opens NO transaction and returns Err(TxnError::Rejected(OpError::NotOwner)) directly.
    /// Reduces to create_new_document(caller, pfx(caller)); returns its (Address, Seq).
    pub fn fork(&self, caller: PrincipalId) -> Result<(Address, Seq), TxnError<OpError>>;
}
```

### C. Queries — *pure methods* (read off any M2 `Snapshot`; write nothing)

```rust
impl M3State {
    pub fn is_allocated(&self, a: &Address) -> bool;            // any namespace incl. content/link
    pub fn entity_level(&self, a: &Address) -> Option<Level>;   // Some iff registered entity (zeros ≤ 2)
    pub fn is_registered_document(&self, d: &Address) -> bool;  // == entity_level == Some(Document)
    pub fn effective_owner(&self, a: &Address) -> Option<Principal>;  // ω(a), longest-prefix match; valid
                                                                     // even when a is not (yet) allocated
    pub fn principal_by_id(&self, id: PrincipalId) -> Option<Principal>;  // single-valued (id-injective)
    pub fn principal_prefix(&self, id: PrincipalId) -> Option<Address>;   // principal_by_id(id).map(|p| p.prefix)
    /// Peek the next delegable account-tier prefix under `parent` — the exact value `delegate` will
    /// demand as next-form. None if `parent` is neither node nor account, or the gate trips.
    pub fn next_account_prefix(&self, parent: &Address) -> Option<Address>;
    pub fn owns(prefix: &Address, a: &Address) -> bool { is_prefix(prefix.tumbler(), a.tumbler()) } // O1
}
```

### D. Genesis

```rust
impl M3State { pub fn genesis() -> M3State; }   // nodes={[1]}, frontiers={}, Π={ [1] → Principal{BOOTSTRAP_PRINCIPAL,[1]} }
```

## Caller contracts & obligations

**Frontier mints (M5/M7, inside a composite):**
- `mint_content(home)` / `mint_link(home)`: caller must pass a **registered document** `home` (else `Err(MintError::HomeNotRegistered)`); hold `content_lock_key(home)` / `link_lock_key(home)` before the closure.
- `mint_version(source)`: `source` must be a **registered `Document`** (else `MintError::SourceNotRegistered` — covers both an unregistered address AND a registered non-document); hold `version_lock_key(source)`.
- `mint_document(account)`: `account` must be a **registered `Account`** (else `MintError::NotAnAccount` — covers both unregistered AND non-account); hold `document_lock_key(account)`.
- All mints: `MintError::Gate(GateViolation)` is the M1 inc-gate (B6), defensive — fires only on a corrupted frontier. Take the matching `*_lock_key` **before** the closure (M2 holds keys for the txn); run the mint inside off `stg.working().m3()`; stage the returned `M3Rec` via `stg.push(rec.into())`.
- Guarantee: the held lock key and the advanced frontier key are byte-identical **by construction** — never reconstruct an anchor or pass a coarser `(home_doc, g)` key. The three g=1 chains under one document (content/link/version) get **distinct** locks.

**Entity ops (M10):** each returns `(Address, Seq)` only **after commit**; `Seq` is M2's committed `last_seq` (the linearization coordinate). Op-specific `E` surfaces as `TxnError::Rejected(E)`; other `TxnError` variants are M2's.
- `create_new_document(caller, account)`: caller must be the **effective owner** of `account` (`ω(account).id == caller`); `OpError::NotOwner` if ω is `None` or names another principal. Registers d only (no arrangement). No idempotency key — a retried lost-ack yields a harmless orphan empty document.
- `delegate(delegator, new_prefix, new_id)`: caller must supply a `new_prefix` that is T4-valid (`NotValid`), **account-tier `zeros == 1`** (`NotAccountTier` — a node- or document-tier prefix is rejected), unallocated/fresh (`NotFresh`), in **next-form** `== next_in(namespace(new_prefix))` (`NotNextForm` — obtain via `next_account_prefix(parent)` to avoid guess-and-retry), strictly under the delegator's prefix (`NotAncestor`), with the delegator as ω of `new_prefix` (`NotAuthorized`), no principal strictly beneath it (`NotTopDown`), and a registered parent (`ParentNotRegistered`); `new_id` must be unused (`DuplicateId`); `delegator` must name a known principal (`DelegatorUnknown`). Produces an account + one principal atomically.
- `register_node(addr)`: `addr` is **supplied** by provisioning; must be T4-valid (`NotValid`), `Level::Node` (`NotNode`), unregistered (`NotFresh`), and a descendant of bootstrap `[1] ≼ addr` (`NotDescendantOfBootstrap`). Validate-not-mint.
- `fork(caller)`: `caller` must be a **known account-tier** principal. Unknown id → `Err(TxnError::Rejected(OpError::NotOwner))`, **no transaction opened**. A node-tier caller → `OpError::Mint(MintError::NotAnAccount)` (the node-tier O10 case is dropped). M5 wires the shared content separately.

**Queries (any snapshot, write nothing):**
- `is_allocated(a)`: `true` iff `a` is minted in any namespace (incl. content/link). Reflects **minting, never byte-presence** (a registered-empty document is an addressable ghost). Append-only ⇒ a `true` answer is permanent.
- `entity_level(a)`: `Some(level)` iff `a` is a registered entity (`zeros ≤ 2`); `None` for an element or unregistered address.
- `is_registered_document(d)`: `entity_level(d) == Some(Document)`.
- `effective_owner(a)`: `Some(Principal)` longest-prefix match over Π, or `None` if uncovered; valid even when `a` is not allocated. **Authorize with ω, never bare `owns`** — a node operator's prefix contains every delegated account, so `owns` is true for several principals at once; only ω (longest match) arbitrates. ω is unique (O2).
- `principal_by_id(id)` / `principal_prefix(id)`: `Some(..)` / `None`; **single-valued** (delegate's id-freshness gate). `principal_prefix` is **value-stable** across snapshots (prefixes immutable).
- `next_account_prefix(parent)`: `Some(prefix)` to feed `delegate`, or `None` if `parent` is neither node nor account; the returned prefix still faces delegate's full in-closure gate.
- `owns(prefix, a)`: pure two-tumbler prefix test, coordination-free; **not for authorization**.

**Invariants a caller may rely on:**
- Every `Address` returned by a mint or op is **T4-valid**.
- Allocations, nodes, and principals are **permanent and contiguous** (no delete/revoke API; a gap is unrepresentable).
- Distinct namespaces never collide; content↔link spaces are disjoint; the content/link/version/document chains under one document never share an address.
- **Commit-before-acknowledge**: the address (and `Seq`) is returned only after M2 commits — a crash never loses a handed-out address, and an address is never reused.

## Seams exposed downstream

- **→ M5:** `is_registered_document(d)` (edit precondition); `effective_owner(d_src)` for CREATENEWVERSION's owned-vs-cross-owner branch (owned ⇒ `mint_version` on `(d_src,1)`; cross-owner ⇒ `principal_prefix(forker_id)` → `pfx(π)`, then `mint_document(pfx(π))` on `(pfx(π),2)` — M5 holds the forker as a `PrincipalId`); the pure mints `mint_content`/`mint_version`/`mint_document` (take the matching `*_lock_key` before the closure, stage the returned `M3Rec`); `is_allocated(a)` (content-side referential-integrity oracle for COPY). **ω(d_src) is stable for an existing d_src**, so M5 **pre-reads it off a snapshot** to pick the branch-dependent namespace lock, and needs **no** `principals_lock_key()`.
- **→ M7:** `mint_link` (inside MAKELINK; lock via `link_lock_key(d)` before the closure, stage the returned `M3Rec`); `is_registered_document(d)`.
- **→ M6, M8:** `is_registered_document(d)` — M3 supplies the bool; converting *registered-but-no-arrangement* → ⟨⟩ and *unregistered* → fail is theirs.
- **→ M9:** `effective_owner` / `is_registered_document` (residence resolution); pred-def content is allocated indirectly via M5 (M9→M5→M3).
- **→ M10:** dispatches `create_new_document` / `delegate` / `register_node` / `fork` (each returns `(Address, Seq)`); binds the bootstrap session to `BOOTSTRAP_PRINCIPAL`; may resolve a bound session's prefix via `principal_prefix`; may peek the next delegable account prefix via `next_account_prefix(node)`.
- **→ engine:** implements `HasM3` for `W` (`W: WorldState + HasM3`) with `W::Record: From<M3Rec>`; `World::apply` dispatches the `Record::Ns` variant into M3's fold `M3State::apply_ns`; M3 relies on M2's **default `rebuild_derived`** (its slice is fully serialized — nothing to re-seed).

## Boundary — NOT provided here

- Does **not** store content bytes (M4), arrangements (M5), or link values (M7).
- Does **not** materialize a new document's arrangement — `create_new_document` registers d only; the empty arrangement is lazy in M5.
- Does **not** originate node addresses — provisioning (NodeBaptism) mints them externally; `register_node` only validates.
- Does **not** run the request lifecycle or bind sessions to principals (M10); the session→`PrincipalId` binding and exactly-once/idempotency for retried `create_new_document` are M10's.
- No delete/revoke API; no node-tier `fork` and no per-node principals beyond bootstrap.
- The ⟨⟩-vs-fail query semantics for registered-but-no-arrangement belong to M6/M8; `fork`'s shared-content wiring belongs to M5.
- Holds **no** address algebra of its own (M1) and does **not** own ordering/durability/recovery (rides M2).
