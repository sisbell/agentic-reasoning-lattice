# M3 — Interface (for dependents)

M3 owns the **authoritative permanent name space**: it mints every fresh, globally-unique, T4-valid address, records which entities (nodes/accounts/documents) exist, and answers *"is this allocated?"* and *"who owns this?"* by prefix. **It owns identity, not content.**

## Public interface

All `Tumbler`/`Address`/`Level`/`Span`/`Nat` are M1's; `Kernel`/`Snapshot`/`LockKey`/`Seq`/`TxnError` (and `GateViolation`, surfaced by M1's `checked_inc`) are M2/M1's. `M3State` is M3's slice of the engine's `WorldState` `W`, opaque to dependents (its fields are not part of this interface) and reached through the accessor trait below. The engine implements `W: WorldState + HasM3`; consumers reach `&self` methods via `stg.working().m3()` / `stg.base().m3()` inside a composite and `snapshot.world().m3()` for a read. The `*_lock_key`/`genesis` associated functions are called on the type (`M3State::content_lock_key(..)`), needing no instance.

```rust
pub trait HasM3 { fn m3(&self) -> &M3State; }   // engine: W: WorldState + HasM3 — the read accessor
```

```rust
#[derive(Clone, Copy, PartialEq, Eq, Hash, Debug)]
pub struct PrincipalId(pub u64);                 // opaque external identity, supplied by M10/session
#[derive(Clone)] pub struct Principal { pub id: PrincipalId, pub prefix: Address }  // prefix: T4-valid, zeros ≤ 1
pub const BOOTSTRAP_PRINCIPAL: PrincipalId = PrincipalId(0);  // π₀'s fixed id (genesis); the ω-auth gate keys on it

pub enum MintError    { HomeNotRegistered, SourceNotRegistered, NotAnAccount, Gate(GateViolation) }
pub enum OpError      { NotOwner, Mint(MintError) }
pub enum DelegateError{ DelegatorUnknown, DuplicateId, NotAncestor, NotAuthorized, NotAccountTier,
                        NotTopDown, NotFresh, NotNextForm, NotValid, ParentNotRegistered }
pub enum NodeError    { NotValid, NotNode, NotFresh, NotDescendantOfBootstrap }
```

The journal-delta type returned by the mints; the engine's `W::Record` absorbs it via `From<M3Rec>` and the caller stages it with `stg.push(rec.into())` (the variants are M3-folded — a caller stages, never constructs or matches them):

```rust
pub enum M3Rec {
    Allocate          { addr: Tumbler },
    RegisterNode      { addr: Tumbler },
    RegisterPrincipal { prefix: Tumbler, id: PrincipalId },
}
```

### A. Frontier allocation — *pure, composable* (folded into M5/M7 composites)

```rust
impl M3State {
    /// Next content address under d: namespace (b_C(d), 1), element field [s_C, m+1]. [M5: INSERT]
    pub fn mint_content(&self, home: &Address)    -> Result<(Address, M3Rec), MintError>;
    /// Next link address under d: namespace (b_L(d), 1), element field [s_L, m+1]. [M7: MAKELINK]
    pub fn mint_link(&self, home: &Address)        -> Result<(Address, M3Rec), MintError>;
    /// Next version identity: namespace (source, 1) — version chain, SEPARATE from the document chain.
    pub fn mint_version(&self, source: &Address)   -> Result<(Address, M3Rec), MintError>;
    /// Next document identity under an account: namespace (account, 2). [CREATENEWDOCUMENT; cross-owner VERSION; fork]
    pub fn mint_document(&self, account: &Address) -> Result<(Address, M3Rec), MintError>;

    /// Namespace LockKey for transact's `keys` arg (call before the closure; the mint advances the same key).
    pub fn content_lock_key(home: &Address)      -> LockKey;   // = (b_C(home), 1)
    pub fn link_lock_key(home: &Address)         -> LockKey;   // = (b_L(home), 1)
    pub fn version_lock_key(source: &Address)    -> LockKey;   // = (source, 1)
    pub fn document_lock_key(account: &Address)  -> LockKey;   // = (account, 2)
    pub fn principals_lock_key()                 -> LockKey;   // Space::Principals tag
    pub fn node_lock_key()                       -> LockKey;   // Space::Nodes tag
}
```

### B. Entity operations — *transact-wrapped* (M3 drives the transaction; called by M10)

```rust
impl<W: WorldState + HasM3> Namespace<W> where W::Record: From<M3Rec> {
    /// Baptize a fresh empty document under `account`; authorization by effective owner (ω), not bare
    /// containment. Registers d in the entity set; does NOT write M5's arrangement (lazy). [ASN-0103]
    pub fn create_new_document(&self, caller: PrincipalId, account: &Address)
        -> Result<(Address, Seq), TxnError<OpError>>;

    /// O15 five-condition gate — (iii) NARROWED to zeros==1 — PLUS id-freshness PLUS P8 (parent
    /// registered) PLUS next-form; baptize the new account prefix AND register the principal in ONE txn. [ASN-0042]
    pub fn delegate(&self, delegator: PrincipalId, new_prefix: Tumbler, new_id: PrincipalId)
        -> Result<(Address, Seq), TxnError<DelegateError>>;

    /// Admit an externally-originated node (validate freshness + n₀-lineage; address chosen by provisioning). [ASN-0047]
    pub fn register_node(&self, addr: Tumbler) -> Result<(Address, Seq), TxnError<NodeError>>;

    /// Denial-as-fork, allocation half (O10, account-tier): a fresh document in the caller's OWN account.
    /// Account-tier caller only; a node-tier caller gets Mint(NotAnAccount). Reduces to create_new_document(caller, pfx(caller)).
    pub fn fork(&self, caller: PrincipalId) -> Result<(Address, Seq), TxnError<OpError>>;
}
```

### C. Queries — *pure methods* (read off any M2 `Snapshot`; write nothing)

```rust
impl M3State {
    pub fn is_allocated(&self, a: &Address) -> bool;            // any namespace incl. content/link
    pub fn entity_level(&self, a: &Address) -> Option<Level>;   // Some iff registered entity (zeros ≤ 2)
    pub fn is_registered_document(&self, d: &Address) -> bool;  // == entity_level == Some(Document)
    pub fn effective_owner(&self, a: &Address) -> Option<Principal>;  // ω(a), longest-prefix match; valid even if a unallocated
    pub fn principal_by_id(&self, id: PrincipalId) -> Option<Principal>;        // O(|Π|) scan; single-valued
    pub fn principal_prefix(&self, id: PrincipalId) -> Option<Address>;         // principal_by_id(id).map(|p| p.prefix)
    pub fn next_account_prefix(&self, parent: &Address) -> Option<Address>;     // peek delegate's next-form value
    pub fn owns(prefix: &Address, a: &Address) -> bool { is_prefix(prefix.tumbler(), a.tumbler()) } // O1
}
```

### D. Genesis

```rust
impl M3State { pub fn genesis() -> M3State; }   // Σ₀: nodes={[1]}, frontiers={}, Π={[1] → Principal{BOOTSTRAP_PRINCIPAL,[1]}} (O14)
```

## Caller contracts & obligations

**Engine wiring (the integrator must provide):**
- Implement `HasM3` for `W` (`W: WorldState + HasM3`); dependents then reach M3 only through `m3()`.
- `W::Record` must satisfy `From<M3Rec>`; each entity op lifts its deltas via `stg.push(rec.into())`, and the engine dispatches the `W::Record` M3 variant into `M3State::apply`.
- The 1-byte `Space` tags (`Namespace`/`Principals`/`Nodes`) come from the engine's single central `Space` enum.

**Pure mints (`mint_content`/`mint_link`/`mint_version`/`mint_document`):**
- Caller must take the matching `*_lock_key(..)` **before** opening the `transact` closure (pass it in `keys`), then run the mint **inside** the closure off `stg.working().m3()` so successive mints each see the prior one.
- Caller stages the returned `M3Rec` via `stg.push(rec.into())`; the mint advances the byte-identical key the caller locked.
- Precondition each enforces (structural only — never ownership): `mint_content`/`mint_link` need `is_registered_document(home)` → else `HomeNotRegistered`; `mint_document` needs a registered `Account` → else `NotAnAccount`; `mint_version` needs a registered `Document` `source` → else `SourceNotRegistered` (covers both an unregistered address **and** a registered non-document).
- `Gate(GateViolation)` indicates a corrupted frontier (defensive; not a normal caller error).
- Guarantee: the returned `Address` is always T4-valid and never previously minted.

**Lock keys (`*_lock_key`):** associated functions, no instance. The three g=1 chains under one document — content `(b_C(d),1)`, link `(b_L(d),1)`, version `(d,1)` — receive **distinct** keys; never substitute a coarser `(home_doc, g)` key.

**Queries (read off any `Snapshot`, write nothing):**
- `is_allocated(a)` → true iff `a` is minted in *any* namespace (incl. content/link element). Reflects **minting, not byte-presence** — a registered-empty document is an allocated ghost. A `true` answer is permanent.
- `entity_level(a)` → `Some(level)` iff `a` is a registered node/account/document; `None` for an element address (use `is_allocated`) or an unregistered address.
- `effective_owner(a)` → ω(a) by longest-prefix match; `None` if no covering principal. **Authorization must use this, never bare `owns`** — a node operator's prefix contains delegated accounts, so only ω arbitrates.
- `owns(prefix, a)` → pure containment test; coordination-free, but **not** an authorization gate.
- `principal_by_id(id)` / `principal_prefix(id)` → single-valued (delegation enforces id-freshness); `None` if `id` names no principal. Value-stable across snapshots (prefixes immutable, principals persist).
- `next_account_prefix(parent)` → the exact next-form value `delegate` will demand; `None` if `parent` is neither node nor account. The peeked prefix still faces `delegate`'s full in-closure gate (racing peeks → exactly one winner).

**`create_new_document(caller, account)`:**
- Caller supplies its session-bound `caller: PrincipalId` and the target `account`.
- Authorization: requires `effective_owner(account).id == caller` → else `OpError::NotOwner` (ω absent or names another principal); a non-account `account` → `OpError::Mint(MintError::NotAnAccount)`.
- Registers d **only** — no M5 arrangement is written. No idempotency key: a retried lost-ack yields a harmless orphan empty document.
- Returns `(Address, Seq)` **only after commit** (commit-before-acknowledge); `Seq` is the linearization coordinate.

**`delegate(delegator, new_prefix, new_id)`:**
- Caller supplies a candidate `new_prefix: Tumbler` (obtain it from `next_account_prefix(parent)` to avoid guess-and-retry), and a fresh `new_id`.
- `new_prefix` obligations: T4-valid (`NotValid`); account-tier `zeros == 1` (`NotAccountTier` — node-tier *and* document-tier both rejected); unallocated (`NotFresh`); the next-form under its namespace (`NotNextForm`); its parent registered (`ParentNotRegistered`).
- `delegator` obligations: a known principal (`DelegatorUnknown`); the effective owner of `new_prefix` (`NotAuthorized`); a strict ancestor (`NotAncestor`); no existing principal strictly under `new_prefix` (`NotTopDown`).
- `new_id` must be unused (`DuplicateId`).
- Produces an **account** (zeros=1) plus one new principal in one transaction. Returns `(Address, Seq)` post-commit.

**`register_node(addr)`:**
- The address is **supplied** (minted externally by provisioning), not minted here. Validates T4-validity (`NotValid`), `Level::Node` (`NotNode`), freshness (`NotFresh`), bootstrap lineage `[1] ≼ addr` (`NotDescendantOfBootstrap`). Returns `(Address, Seq)` post-commit.

**`fork(caller)`:**
- Account-tier caller only; reduces to `create_new_document(caller, pfx(caller))`. An unknown `caller` opens **no** transaction and returns `Err(TxnError::Rejected(OpError::NotOwner))` directly; a node-tier caller gets `OpError::Mint(MintError::NotAnAccount)`. M5 wires the shared content separately. Returns `create_new_document`'s `(Address, Seq)`.

**Cross-cutting guarantees a caller may rely on:**
- Every returned `Address` is T4-valid; no address is ever minted twice; gaps are unrepresentable.
- All registrations are permanent and irrevocable — there is **no delete/revoke API**; a `true`/`Some` answer never regresses.
- `BOOTSTRAP_PRINCIPAL = PrincipalId(0)` is the genesis (sole node-tier) principal; M10 must bind the bootstrap session to it.

## Seams exposed downstream

- **→ M5:** `is_registered_document(d)` (edit precondition); `effective_owner(d_src)` for CREATENEWVERSION's owned-vs-cross-owner branch (owned ⇒ `mint_version` on `(d_src,1)`; cross-owner ⇒ `principal_prefix(forker_id)` → `pfx(π)`, then `mint_document(pfx(π))` on `(pfx(π),2)`); the pure mints `mint_content` (INSERT) and `mint_version`/`mint_document` (VERSION), each locked via the matching `*_lock_key` before the closure and the returned `M3Rec` staged; `is_allocated(a)` (content-side referential-integrity oracle for COPY transclusion). Because the VERSION lock is branch-dependent and the branch *is* `ω(d_src)`, M5 **pre-reads** the stable `ω(d_src)` off a snapshot, holds the single matching namespace lock, and needs **no** `principals_lock_key()`.
- **→ M7:** `mint_link` *pure* (inside MAKELINK; M7 locks via `link_lock_key(d)` before the closure, then stages the returned `M3Rec`); `is_registered_document(d)` (link's home).
- **→ M6, M8:** `is_registered_document(d)` — they convert *registered-but-no-arrangement* → ⟨⟩ and *unregistered* → fail. M3 supplies the bool; the ⟨⟩-vs-fail query semantics are theirs.
- **→ M9:** `effective_owner`/`is_registered_document` (residence resolution); pred-def content is allocated indirectly via M5's composite (M9→M5→M3).
- **→ M10:** dispatches `create_new_document`/`delegate`/`register_node`/`fork`, each returning `(Address, Seq)` so M10 surfaces the commit `Seq` as the linearization coordinate; binds the bootstrap session to `BOOTSTRAP_PRINCIPAL`; may resolve a bound session's prefix via `principal_prefix`; may peek the next delegable account prefix via `next_account_prefix(node)` to construct `delegate`'s `new_prefix`.

## Boundary — NOT provided here

- **Bytes / content storage** (M4) — `is_allocated` reflects minting, never byte-presence; content existence is M4's separate axis.
- **Arrangements** (M5) — including a new document's empty arrangement, which is lazy/implicit in M5; `create_new_document` registers the document and stops.
- **Link values** (M7).
- **Node address origination** — nodes arrive pre-minted from the network-provisioning boundary (NodeBaptism); M3 only *validates* them via `register_node`.
- **Request lifecycle, session→principal binding, exactly-once** (M10).
- **Delete / revoke / ownership-transfer** — no such API exists (permanence/irrevocability).
