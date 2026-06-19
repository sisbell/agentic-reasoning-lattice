# M3 — Namespace: Allocation, Registry & Ownership

## Purpose & boundary

M3 owns the **authoritative permanent name space**: it mints every fresh, globally-unique, T4-valid address the system ever uses, records which organizational entities (nodes, accounts, documents) exist, and answers *"is this allocated?"* and *"who owns this?"* by prefix. It is the single minting authority and the single arbiter of the entity/principal sets. One thing well: **it owns identity, not content.** It does *not* store bytes (M4), arrangements (M5), or link values (M7); it does *not* materialize a new document's arrangement (lazy, in M5 — see [Conflicts resolved](#conflicts-resolved)); it does *not* originate node addresses (those arrive from the network-provisioning boundary, NodeBaptism); it does *not* run the request lifecycle or bind sessions to principals (M10). It hands every store a fresh owned address plus two cheap structural answers, and persists its registry + frontier through M2.

## Public interface

Indices 1-based (M1 convention). All types `Tumbler`/`Address`/`Level`/`Span`/`Nat` are M1's; `Kernel`/`Snapshot`/`LockKey`/`Seq`/`TxnError` are M2's. `M3State` is M3's slice of the engine's `WorldState` `W`, reached through a **named accessor trait** the engine implements (M3 is built before `W` exists, so it codes against this contract, not against `W` directly — with one addition for the *write* path, noted below):

```rust
pub trait HasM3 { fn m3(&self) -> &M3State; }   // engine: W: WorldState + HasM3 — M2's "read your store's slice off this"
// Write path: the engine's Record type must absorb M3's deltas, so the transact-driving B-ops are
// bound `where W::Record: From<M3Rec>` and stage via `stg.push(rec.into())`. `HasM3::m3()` is a
// READ accessor only; the `From<M3Rec>` bound is its write-side mirror (the engine wires both —
// `World::apply` dispatches the `Record::Ns` variant to `M3State::apply_ns`; the bound lifts M3Rec
// the other way).
```

A composite closure reads `stg.working().m3()` (frontier math) or `stg.base().m3()` (the txn-start root — where `delegate`'s race-prone gates are evaluated under the held locks; the other ops' authorizing ω is *stable*, read defensively in-closure or pre-read, §6/§8); a reader reads `snapshot.world().m3()`. The `impl M3State` methods below are reached through that accessor; the `*_lock_key` associated functions are called on the type (`M3State::content_lock_key(..)`), needing no instance.

```rust
#[derive(Clone, Copy, PartialEq, Eq, Hash, Debug, Serialize, Deserialize)]
pub struct PrincipalId(pub u64);                 // opaque external identity, supplied by M10/session;
                                                 // delegate enforces id-injectivity (DuplicateId) ⇒ one id ↦ one principal
#[derive(Clone, Serialize, Deserialize)]
pub struct Principal { pub id: PrincipalId, pub prefix: Address }  // prefix: T4-valid, zeros ≤ 1
pub const BOOTSTRAP_PRINCIPAL: PrincipalId = PrincipalId(0);  // π₀'s fixed id (genesis); the ω-auth gate keys on it

pub enum MintError    { HomeNotRegistered, SourceNotRegistered, NotAnAccount, Gate(GateViolation) }
// SourceNotRegistered (mint_version): source is NOT a registered Document — covers both an unregistered
//   address AND a registered non-document (entity_level(source) != Some(Document)).
pub enum OpError      { NotOwner, Mint(MintError) }   // create_new_document / fork. "not an account" and
                                                      // "not registered" BOTH surface via Mint(MintError::NotAnAccount).
pub enum DelegateError{ DelegatorUnknown, DuplicateId, NotAncestor, NotAuthorized, NotAccountTier,
                        NotTopDown, NotFresh, NotNextForm, NotValid, ParentNotRegistered }
// NotAccountTier now means zeros(new_prefix) != 1 — a node-tier (zeros=0) OR document-tier (zeros≥2)
//   prefix; (iii) is NARROWED from O15's ≤1 to ==1 (§6 / Conflicts §7).
pub enum NodeError    { NotValid, NotNode, NotFresh, NotDescendantOfBootstrap }
```

### A. Frontier allocation — *pure, composable* (folded into M5/M7 composites; M2 contract 3)

Each returns the minted address and the one journal delta the caller stages; the caller takes the matching namespace `LockKey` from the `*_lock_key` constructor (below) **before** opening the closure. They read the **working** state (so successive mints in one composite each see the prior mint), check only *structural* preconditions, and never touch ownership policy.

```rust
impl M3State {
    /// Next content address under d: namespace (b_C(d), 1), element field [s_C, m+1]. [M5: INSERT]
    pub fn mint_content(&self, home: &Address)    -> Result<(Address, M3Rec), MintError>;
    /// Next link address under d: namespace (b_L(d), 1), element field [s_L, m+1]. [M7: MAKELINK]
    pub fn mint_link(&self, home: &Address)        -> Result<(Address, M3Rec), MintError>;
    /// Next version identity: namespace (source, 1) — the version chain, kept SEPARATE
    /// from the document chain below (ASN-0123). [M5: owned CREATENEWVERSION]
    pub fn mint_version(&self, source: &Address)   -> Result<(Address, M3Rec), MintError>;
    /// Next document identity under an account: namespace (account, 2).
    /// [CREATENEWDOCUMENT; cross-owner VERSION; fork]
    pub fn mint_document(&self, account: &Address) -> Result<(Address, M3Rec), MintError>;

    // The caller locks with the matching `*_lock_key` constructor below, and the mint advances the
    // matching `*_ns` frontier — and BOTH route through the SAME private `*_ns` helper (→ the TRUE
    // NsKey: parent = b_C(d)/b_L(d)/source/account) and the SAME injective, space-tagged `ns_lock_key`
    // encoding (§1). So the lock key M5/M7 pass to transact and the frontier key the mint advances are
    // byte-identical BY CONSTRUCTION — one code path, NOTHING in the mint's return to drift (a divergence
    // would under-serialize a namespace and REUSE an address — the one fatal error). The three g=1 chains
    // that can sit under ONE document — content (b_C(d),1), link (b_L(d),1), version (d,1) — therefore
    // never share a key, and M5/M7 never reconstruct an anchor. (A bare `(home_doc, g)` cannot tell them
    // apart.) The constructor is called BEFORE the closure for transact's `keys` arg (M2 holds keys for
    // the txn's duration); the mint runs INSIDE the closure and hands back the matching `Allocate` to stage.

    /// Namespace LockKey for transact's `keys` arg (call before the closure; the mint advances the same key).
    pub fn content_lock_key(home: &Address)      -> LockKey;   // ns_lock_key(content_ns(home))   = (b_C(home), 1)
    pub fn link_lock_key(home: &Address)         -> LockKey;   // ns_lock_key(link_ns(home))      = (b_L(home), 1)
    pub fn version_lock_key(source: &Address)    -> LockKey;   // ns_lock_key(version_ns(source))  = (source, 1)
    pub fn document_lock_key(account: &Address)  -> LockKey;   // ns_lock_key(document_ns(account))= (account, 2)
    /// THE single global principal-registry key (NOT per-subtree — §8 / [Open decisions]).
    /// LOAD-BEARING in `delegate`: serializes its fresh-prefix top-down / next-form / authorization
    /// reads against concurrent same-namespace delegations AND its id-freshness read against
    /// concurrent same-ID delegations — and that id race is CROSS-namespace (same `new_id`, different
    /// `new_prefix`), so only a single global key serializes it. Held DEFENSIVELY by
    /// create_new_document (whose ω(account) read is stale-safe — ω of an *existing* account is
    /// stable, §6/§8). M5's cross-owner VERSION does NOT need it: it pre-reads the stable ω(d_src).
    /// Redundant under M2 v1's global applier lock.
    pub fn principals_lock_key()                 -> LockKey;   // Space::Principals tag
    /// Coarse node-registry key — held by register_node so a concurrent duplicate RegisterNode
    /// surfaces NotFresh instead of silently coalescing. Node admission needs NO lock for SAFETY
    /// (idempotent OrdSet insert, monotone freshness); this only preserves the typed rejection
    /// under per-key concurrency. Redundant under v1's global lock (exactly like principals_lock_key).
    pub fn node_lock_key()                       -> LockKey;   // Space::Nodes tag
}
```

### B. Entity operations — *transact-wrapped* (M3 drives the transaction; called by M10)

```rust
impl<W: WorldState + HasM3> Namespace<W> where W::Record: From<M3Rec> { // holds Arc<Kernel<W>>; the
                 // From bound lets each op LIFT its M3Rec deltas to W::Record and stage them via
                 // stg.push(rec.into()) (the write-path mirror of HasM3's read accessor). Each op opens
                 // ONE `transact`. `delegate`'s race-prone gates (freshness, top-down, id-freshness,
                 // next-form, authorization) are evaluated INSIDE the closure against stg.base().m3()
                 // under the held locks (a pre-transaction snapshot() read is at most a fail-fast, NEVER
                 // authoritative for those — §6/§8); STALE-SAFE reads (ω of an existing account/document;
                 // monotone conditions; pfx) may equally be pre-read off a snapshot. The closure mints
                 // off stg.working().m3() and stages the lifted deltas. Each op returns (Address, Seq) —
                 // the new address plus transact's committed last_seq (the linearization coordinate).
    /// Baptize a fresh empty document under `account`. Authorization is by EFFECTIVE owner (ω), not
    /// bare containment. ω of an *existing* account is STABLE (no concurrent delegation can introduce
    /// a longer coverer — §6/§8), so the in-closure ω re-read is stale-safe and its held principals
    /// lock is defensive. Registers d in the entity set; does NOT write M5's arrangement (lazy).
    /// Returns the address and its commit Seq only after commit (commit-before-acknowledge). [ASN-0103]
    pub fn create_new_document(&self, caller: PrincipalId, account: &Address)
        -> Result<(Address, Seq), TxnError<OpError>>;

    /// Delegation: the O15 five-condition gate — with (iii) NARROWED to `zeros == 1` (account-tier
    /// only; §6 / Conflicts §7) — PLUS id-freshness PLUS P8 (parent registered) PLUS next-form, every
    /// race-prone condition evaluated in-closure under the held principals+namespace locks (§6) — then
    /// baptize the new account prefix AND register the principal in ONE transaction. A reused `new_id`
    /// → DuplicateId; a node-tier (or document-tier) `new_prefix` → NotAccountTier. Returns the new
    /// account address and its commit Seq. [ASN-0042]
    pub fn delegate(&self, delegator: PrincipalId, new_prefix: Tumbler, new_id: PrincipalId)
        -> Result<(Address, Seq), TxnError<DelegateError>>;

    /// Admit an externally-originated node (NodeBaptism: validate freshness + n₀-lineage; the ADDRESS
    /// is chosen by provisioning, not minted here). Returns the node address and its commit Seq. [ASN-0047]
    pub fn register_node(&self, addr: Tumbler) -> Result<(Address, Seq), TxnError<NodeError>>;

    /// Denial-as-fork, allocation half (O10, account-tier case): a fresh document in the caller's OWN
    /// account. Resolves pfx(caller) via `principal_prefix` (value-stable, O13); an unknown id opens NO
    /// transaction and returns Err(TxnError::Rejected(OpError::NotOwner)) directly. Account-tier caller
    /// only — a node-tier caller gets Mint(NotAnAccount); the node-tier O10 case is DROPPED, not
    /// relocated to `delegate` (see Conflicts resolved §6). Reduces to create_new_document(caller,
    /// pfx(caller)) — whose ω-auth passes by construction (ω(pfx(caller)) = caller is stable,
    /// SelfOwnershipAtPrefix); M5 wires the shared content. Returns create_new_document's (Address, Seq).
    pub fn fork(&self, caller: PrincipalId) -> Result<(Address, Seq), TxnError<OpError>>;
}
```

### C. Queries — *pure methods* (read off any M2 `Snapshot`; write nothing)

```rust
impl M3State {
    pub fn is_allocated(&self, a: &Address) -> bool;            // any namespace incl. content/link (body in §2)
    pub fn entity_level(&self, a: &Address) -> Option<Level>;   // Some iff registered entity (zeros ≤ 2)
    pub fn is_registered_document(&self, d: &Address) -> bool;  // == entity_level == Some(Document)
    pub fn effective_owner(&self, a: &Address) -> Option<Principal>;  // ω(a), longest-prefix match; a pure
                                                                     // prefix query over Π — valid even when
                                                                     // a is not (yet) allocated
    /// Resolve a principal by its opaque id. O(|Π|) scan over `principals.values()` — Π is
    /// account/node-tier only (O1a), hence small per node. SINGLE-VALUED because `delegate`
    /// enforces id-freshness (DuplicateId), so at most one principal carries any id. `principal_prefix`
    /// is the pfx(id) projection the id-centric ops (fork, delegate) and the M5→M3 cross-owner-VERSION
    /// seam need, since `principals` is keyed by PREFIX, not id (so this is NOT a point lookup).
    pub fn principal_by_id(&self, id: PrincipalId) -> Option<Principal>;
    pub fn principal_prefix(&self, id: PrincipalId) -> Option<Address>;   // principal_by_id(id).map(|p| p.prefix)
    /// Peek the next delegable account-tier prefix under `parent` — the exact value `delegate`
    /// will demand as next-form, so a caller obtains a valid `new_prefix` instead of
    /// guess-and-retry on NotNextForm. g follows `parent`'s level: a node ⇒ the (parent, 2)
    /// account chain; an account ⇒ the (parent, 1) sub-account chain. Both yield zeros=1 (account-tier,
    /// consistent with (iii)==1). Pure frontier read off any snapshot; `None` if `parent` is neither
    /// node nor account, or the namespace gate trips. The returned prefix still faces delegate's full
    /// in-closure gate, so two racing peeks of the same value still leave exactly one winner.
    pub fn next_account_prefix(&self, parent: &Address) -> Option<Address>;
    pub fn owns(prefix: &Address, a: &Address) -> bool { is_prefix(prefix.tumbler(), a.tumbler()) } // O1
}
```

### D. Genesis

```rust
impl M3State { pub fn genesis() -> M3State; }   // nodes={[1]}, frontiers={}, Π={ [1] → Principal{BOOTSTRAP_PRINCIPAL,[1]} }  (Σ₀, O14)
```

## Core data model

M3's slice of M2's `WorldState` (reached via `HasM3::m3()` — Public interface). All persistent (`im`) so each commit yields a cheap structurally-shared version — free MVCC snapshots for readers and free historical `ω_Σ` (retain old roots). **The journal is the sole authority** (M2); these three structures are the *recovered working representation*, folded by `apply_ns`. `frontiers`, `nodes`, and `principals` are all ordinary `Serialize`/`Deserialize` fields — **none** is `#[serde(skip)]` (the `im` collections serialize under `im`'s `serde` feature, exactly as M1's `Nat` needs `num-bigint`'s) — so they are restored verbatim from the loaded checkpoint and then advanced by replaying the post-checkpoint `M3Rec`s. They are authoritative working state, not derived hints, so M3 takes M2's **default `rebuild_derived`** (identity): there is nothing to re-seed before replay.

```rust
#[derive(Clone, Serialize, Deserialize)]
pub struct M3State {
    /// THE registry, in B1+B2 compressed form. A namespace's entire realized set
    /// {c₁..cₘ} IS the single count m — so a gap is literally unrepresentable (B1 free).
    /// Keyed by (parent, g) — which keeps the document chain (A,2) and the version chain
    /// (d,1) on SEPARATE frontiers (ASN-0123) by construction. Covers every chain:
    /// accounts, documents, versions, content, links. Values are big-ints (B9 unbounded).
    frontiers: im::HashMap<NsKey, Nat>,

    /// Node addresses (zeros = 0). Externally minted (ASN-0047 NodeBaptism — provisioning mints
    /// node addresses OUTSIDE the docuverse), so possibly non-contiguous → held explicitly, not
    /// frontier-encoded. ASN-0040 seeds roots in B₀, and its baptize(p,1) with a NODE parent CAN
    /// mint a child node ([1] → [1,1], still zeros=0) — but M3 SUPPRESSES that capability (forced
    /// by NodeBaptism: no docuverse transition mints a node — Conflicts §7), so internal minting
    /// never yields a zeros=0 address and the ongoing-admission path is register_node, not ASN-0040
    /// baptism. Seeded {[1]}.
    nodes: im::OrdSet<Tumbler>,

    /// Principal registry Π, keyed by ownership prefix. Small (node/account tier only, O1a).
    /// Append-only with immutable prefixes (O12/O13), prefix-injective (O1b, by (v)) AND
    /// id-injective (delegate's DuplicateId gate, §6) — so BOTH the by-prefix key and the by-id
    /// scan are single-valued. The ONLY authoritative ownership state — the delegation forest is
    /// recomputable (NestingByDelegation) and never stored.
    principals: im::OrdMap<Tumbler, Principal>,
}

#[derive(Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct NsKey { parent: Tumbler, g: u8 /* 1 | 2 */ }   // == ASN-0040's namespace (p, d)

#[derive(Clone, Serialize, Deserialize)]
pub enum M3Rec {                                   // M3's journal deltas, lifted to W::Record (From) and folded by `apply_ns`
    Allocate          { addr: Tumbler },           // mint: advance frontier[namespace(addr)]
    RegisterNode      { addr: Tumbler },           // external node admission
    RegisterPrincipal { prefix: Tumbler, id: PrincipalId },  // delegation's principal half
}
```

**Why these shapes.** A `HashMap` for `frontiers` because the hot operations — mint and membership — are *point* lookups on one namespace; we never iterate namespaces, so we don't pay for order. `BigUint` values are non-negotiable (B9: "each integer has no upper limit"; a fixed-width counter silently violates it). The principal map is `OrdMap` because delegation's top-down check needs a descendant *range* scan, and ordering lets a builder upgrade ω to a range walk. **Authoritative vs hint:** `frontiers`/`nodes`/`principals` are authoritative working state (the compressed allocation journal). The delegation forest, any `address → owner` ω-cache, and any `id → prefix` reverse index are *hints* — recomputable from `principals` alone — and are deliberately **not** stored.

`apply_ns` (M3's fold) is deterministic, total, side-effect-free. A bare journal `Tumbler` must be lifted to an `Address` before `parent`/projection (M1 types those over `&Address`/`&Tumbler` respectively); minted and journaled addresses are always T4-valid, so the lift cannot fail. The engine's `World::apply` routes the `Record::Ns` variant (M3's lifted `M3Rec`, M3 being the engine's namespace slice) into this fold:

```rust
fn apply_ns(&self, r: &M3Rec) -> M3State {
    let mut s = self.clone();
    match r {
        M3Rec::Allocate{ addr }            => { let (p, g, n) = decompose(addr); s.frontiers.insert(NsKey{ parent: p, g }, n); }
        M3Rec::RegisterNode{ addr }        => { s.nodes.insert(addr.clone()); }
        M3Rec::RegisterPrincipal{ prefix, id } => {
            let ad = validate(prefix.clone()).expect("a registered principal prefix is T4-valid");
            s.principals.insert(prefix.clone(), Principal{ id: *id, prefix: ad });
        }
    }
    s
}

/// Recover (parent, g, ordinal) from a T4-valid address — pure M1. The address is a mint OR
/// `delegate`'s validated `new_prefix` (this is NOT a mint-only path — §6). `parent` takes
/// `&Address`, so the bare `Tumbler` is `validate`-lifted first (total — the caller passes a
/// T4-valid tumbler); `zeros` and `ordinal` take `&Tumbler`, so they read `.tumbler()` projections.
fn decompose(addr: &Tumbler) -> (Tumbler, u8, Nat) {
    let ad  = validate(addr.clone()).expect("T4-valid by caller contract");
    let par = parent(&ad).expect("a decomposed address is never a 1-component node");
    let g   = if zeros(addr) == zeros(par.tumbler()) { 1 } else { 2 };
    (par.tumbler().clone(), g, ordinal(addr).clone())
}

/// The NsKey a minted address advances under — its namespace. Pure M1 via `decompose`.
/// `delegate` uses it for BOTH the next-form check and the held namespace LockKey, so the checked
/// key, the locked key, and the key the staged `Allocate` advances are one and the same key.
/// Safe only on a T4-valid address (decompose's lift); `delegate` calls it after the validate-lift.
fn namespace(addr: &Tumbler) -> NsKey { let (p, g, _) = decompose(addr); NsKey{ parent: p, g } }
```

One `Allocate` variant suffices for every minted address (entity, content, link) because the frontier map is uniform; the level distinction is recovered at *query* time from `zeros`. The `(parent, g)` of an `Allocate` is exactly the `NsKey` of the `LockKey` the minting op held — frontier key and lock key are the same key (pinned at the byte level in §1).

## Internal design

### 1. The frontier allocator (the heart)

For namespace `(p, g)`, ASN-0040's `next(B,p,g)` has a closed form once you store the count `m`: the chain `S(p,g)` is `c₁ = inc(p,g)`, `cₙ₊₁ = inc(cₙ,0)`, so `cₙ = p ++ [0]*(g−1) ++ [n]`. Therefore **the next address is `c_{m+1}` = `p ++ [0]*(g−1) ++ [m+1]`** — read the count, advance the trailing ordinal.

```rust
fn next_in(&self, key: &NsKey) -> Result<Address, GateViolation> {
    let m = self.frontiers.get(key).cloned().unwrap_or_else(Nat::zero);
    let parent = validate(key.parent.clone()).expect("namespace parents are T4-valid by construction"); // anchors b_C/b_L (#E=1) and registered entities alike
    let c1 = checked_inc(&parent, key.g as usize)?;   // M1 gate ⇒ B6(ii)/(iii) (TA5a); c1 = inc(parent,g), trailing ordinal 1
    Ok(if m.is_zero() {
        c1                                            // first emission
    } else {
        // cₘ₊₁ = c1 with its trailing ordinal 1 → m+1. M1's `shift` (ordinal-only, n=m≥1) does
        // exactly this and is SAFE here: c1 is a FULL address carrying its ordinal in the last
        // position, not a bare doc·0·subspace base. Re-`validate` is total — cₘ₊₁ is the same
        // namespace as the gated c1, differing only in a positive ordinal.
        validate(shift(c1.tumbler(), &m)).expect("differs from gated c1 only in a positive ordinal")
    })
}
```

**Namespace keys and their lock-key mirror (single-sourced).** The `(p, g)` key the frontier advances under and the `LockKey` the op holds are produced from *one* `NsKey` through *one* injective encoding, so they can never drift:

```rust
// `Space` is M2's SINGLE CENTRAL tag enum (the LockKey contract's 1-byte space tag, never chosen
// per-store). It lives in `skep-kernel`, BELOW every store — NOT in the engine assembler crate
// (naming it there would cycle). M3's THREE variants — `Space::Namespace`, `Space::Principals`,
// `Space::Nodes` — are DECLARED in that central `Space` enum in skep-kernel (where every tag lives);
// they are NOT "reserved" by the assembler — skep-engine assembles `World`/`Record` and does not
// own `Space`. Drawing three tags deviates from the contract's one-tag-*per-store* GUIDANCE, but the
// contract's HARD rule is tag UNIQUENESS (distinct key spaces never collide), which three distinct
// central-enum variants satisfy exactly. (Stricter-conformance equivalent, if one-tag-per-store is
// to be honored literally: a single `Space::M3` tag plus a second sub-tag byte selecting
// namespace/principals/nodes — same byte-level disjointness, one tag.) The three distinct tags are
// what keep the three key spaces from aliasing; the byte image is what M2 Eq/Hash/Ord-s; injectivity
// is what guarantees distinct namespaces map to distinct locks (an alias would under-serialize →
// REUSE an address).
fn ns_lock_key(k: &NsKey) -> LockKey {
    let mut b = vec![Space::Namespace as u8];
    b.extend((k.parent.len() as u32).to_be_bytes());          // component count
    for i in 1..=k.parent.len() {
        let c = k.parent.get(i).to_bytes_be();                // BigUint → minimal big-endian bytes
        b.extend((c.len() as u32).to_be_bytes());             // length-delimit each component (injective)
        b.extend(c);
    }
    b.push(k.g);                                              // g ∈ {1,2}
    LockKey(b)
}

// The four namespace helpers — the ONE code path each mint and each *_lock_key reuses:
fn content_ns (d: &Address) -> NsKey { NsKey{ parent: inc(d.tumbler(), 2), g: 1 } }            // b_C(d)=inc(d,2)
fn link_ns    (d: &Address) -> NsKey { NsKey{ parent: inc(&inc(d.tumbler(), 2), 0), g: 1 } }   // b_L(d)=inc(b_C(d),0)
fn version_ns (s: &Address) -> NsKey { NsKey{ parent: s.tumbler().clone(), g: 1 } }            // (source,1)
fn document_ns(a: &Address) -> NsKey { NsKey{ parent: a.tumbler().clone(), g: 2 } }            // (account,2)

// The six LockKey constructors are `impl M3State` ASSOCIATED functions (Public interface §A) —
// called on the type (`M3State::content_lock_key(..)`), no instance needed:
impl M3State {
    pub fn content_lock_key (home:    &Address) -> LockKey { ns_lock_key(&content_ns(home)) }
    pub fn link_lock_key    (home:    &Address) -> LockKey { ns_lock_key(&link_ns(home)) }
    pub fn version_lock_key (source:  &Address) -> LockKey { ns_lock_key(&version_ns(source)) }
    pub fn document_lock_key(account: &Address) -> LockKey { ns_lock_key(&document_ns(account)) }
    pub fn principals_lock_key() -> LockKey { LockKey(vec![Space::Principals as u8]) }
    pub fn node_lock_key()       -> LockKey { LockKey(vec![Space::Nodes as u8]) }
}

// Every mint advances `next_in(*_ns(..))`; the caller locks with `Self::*_lock_key(..)`. Since BOTH
// `*_lock_key(..) = ns_lock_key(*_ns(..))` and the frontier advance route through the SAME `*_ns`
// helper, the staged frontier key and the held lock key are the SAME BYTES — by one code path, with
// nothing in the return to drift. All four mints share one shape; they differ only in the *_ns helper
// and the structural precondition (HomeNotRegistered / SourceNotRegistered=Document / NotAnAccount=Account):
impl M3State {
    pub fn mint_content(&self, home: &Address) -> Result<(Address, M3Rec), MintError> {
        if !self.is_registered_document(home) { return Err(MintError::HomeNotRegistered); }   // P6/C2
        let a = self.next_in(&content_ns(home)).map_err(MintError::Gate)?;
        Ok((a.clone(), M3Rec::Allocate{ addr: a.tumbler().clone() }))
    }
    pub fn mint_link(&self, home: &Address) -> Result<(Address, M3Rec), MintError> {
        if !self.is_registered_document(home) { return Err(MintError::HomeNotRegistered); }   // L1a
        let a = self.next_in(&link_ns(home)).map_err(MintError::Gate)?;
        Ok((a.clone(), M3Rec::Allocate{ addr: a.tumbler().clone() }))
    }
    pub fn mint_version(&self, source: &Address) -> Result<(Address, M3Rec), MintError> {
        if self.entity_level(source) != Some(Level::Document) {                                // V-WF: registered Document
            return Err(MintError::SourceNotRegistered);                                        //   (covers unregistered AND non-document)
        }
        let a = self.next_in(&version_ns(source)).map_err(MintError::Gate)?;
        Ok((a.clone(), M3Rec::Allocate{ addr: a.tumbler().clone() }))
    }
    pub fn mint_document(&self, account: &Address) -> Result<(Address, M3Rec), MintError> {
        if self.entity_level(account) != Some(Level::Account) {                                // P8/CND.pre
            return Err(MintError::NotAnAccount);                                               //   (covers unregistered AND non-account)
        }
        let a = self.next_in(&document_ns(account)).map_err(MintError::Gate)?;
        Ok((a.clone(), M3Rec::Allocate{ addr: a.tumbler().clone() }))
    }
}
```

- **Common case** is a single `HashMap::get`, one M1 `checked_inc`, and (past the first emission) one ordinal-only `shift` — no scan. (The reference's stateless "find-max-under-prefix-and-increment" is the same answer without the cached count; caching the count *is* the O(log n)→O(1) optimization, and we cache it because we keep the registry anyway.)
- **Level-awareness** (ASN-0123, the load-bearing gotcha): we key by `(p, g)`, never by the predicate "next document under A." A document under account A lives in `(A, 2)`; a version of document d lives in `(d, 1)`. Both classify as `Document`, both have `parent == A`-or-a-document, but their namespace keys differ, so their frontiers advance independently and **never re-mint a colliding address**. This is the entire fix for ASN-0103's version/document collision and ASN-0123's VD obligation — it falls out of the key, requiring no length filter. And because the per-namespace `LockKey` is built from this very `(p, g)` key through `ns_lock_key` (above) — *not* from `(home_doc, g)` — the *lock* granularity mirrors the *frontier* granularity **byte-for-byte**: the three g=1 chains under one document (content `(b_C(d),1)`, link `(b_L(d),1)`, version `(d,1)`) receive three **distinct** locks, so same-namespace serializes (B8) while they run free of each other (B7).
- **Determinism (B2):** `next_in` is a pure function of `frontiers` — memoizable, replayable, and the natural property-test oracle.
- **Tradeoff:** the counter representation makes B1 contiguity *free* (a gap is unrepresentable) and registry size O(active namespaces) not O(addresses), at the cost of decomposition on membership (cheap — `parent`/`zeros`/`ordinal`). The alternative (explicit address set/trie) buys fast arbitrary-`t` membership but reintroduces contiguity as something to *enforce*; deferred to [Open decisions](#open-build-decisions).

### 2. The entity registry (membership without a second structure)

The entity set E is *encoded* by the entity-namespace frontiers plus the node root set — no separate `Set<Address>`. Membership is decompose-and-compare (ASN-0040 counter membership); `zeros`/`ordinal` are M1 functions over `&Tumbler`, so they read `.tumbler()`.

**Membership-correctness invariant (decompose-and-range *is* chain membership).** For any T4-valid `a`, let `p = parent(a)` (M1's longest T4-valid proper prefix) and `g = (zeros(a) == zeros(p) ? 1 : 2)` — equivalently `g = 1` iff `a` with its last component dropped is itself T4-valid (the `g = 2` form `p ++ [0, n]` has a trailing-zero penultimate, so its longest valid prefix is `p`, not `p ++ [0]`). Then `a` is *exactly* `c_{ordinal(a)}` of namespace `(p, g)` — `a = p ++ [0]^{g−1} ++ [ordinal(a)]` — by ASN-0040's `S(p, g)` canonical form, and distinct T4-valid addresses decompose to distinct `(namespace, ordinal)` pairs (T4b unique-parse). So `a ∈ {c₁..cₘ}` iff `1 ≤ ordinal(a) ≤ m`: the range checks below are genuine chain membership with **no false positives**, not an approximation.

```rust
fn entity_level(&self, a: &Address) -> Option<Level> {
    match a.level() {
        Level::Node => self.nodes.contains(a.tumbler()).then_some(Level::Node),
        Level::Account | Level::Document => {
            let p = parent(a)?;                                    // M1 longest-valid-prefix (takes &Address)
            let key = NsKey{ parent: p.tumbler().clone(),
                             g: if zeros(a.tumbler())==zeros(p.tumbler()) {1} else {2} };
            let m = self.frontiers.get(&key).cloned().unwrap_or_else(Nat::zero);
            (Nat::one() <= *ordinal(a.tumbler()) && *ordinal(a.tumbler()) <= m).then_some(a.level())
        }
        Level::Element => None,   // content/link are not entities — use is_allocated
    }
}
```

`is_allocated` shares `entity_level`'s decompose-and-compare but drops the entity restriction — the `Level::Element => None` arm becomes the same general branch, so content/link element addresses resolve against their own `(b_C(d),1)`/`(b_L(d),1)` frontiers. This is the referential-integrity oracle M5 (COPY transclusion) depends on — its uniform Element branch answers content- and link-subspace addresses alike, though M5's content-side check is the only current caller:

```rust
fn is_allocated(&self, a: &Address) -> bool {
    match a.level() {
        Level::Node => self.nodes.contains(a.tumbler()),       // node case, exactly as entity_level
        // The general decompose-and-compare, now over ALL non-node levels (incl. Element):
        // a content/link element [d.0.s.{n}] has parent b_C(d)/b_L(d) at the SAME zeros, so g=1 and
        // the key is its TRUE content/link namespace; n is in range iff 1 ≤ n ≤ m.
        Level::Account | Level::Document | Level::Element => {
            let Some(p) = parent(a) else { return false };     // None only for a 1-component node (handled above)
            let key = NsKey{ parent: p.tumbler().clone(),
                             g: if zeros(a.tumbler())==zeros(p.tumbler()) {1} else {2} };
            let m = self.frontiers.get(&key).cloned().unwrap_or_else(Nat::zero);
            Nat::one() <= *ordinal(a.tumbler()) && *ordinal(a.tumbler()) <= m
        }
    }
}
```

Consistency is automatic: a content frontier `(b_C(d),1)` only advances if d is registered (P6 gate), and E is append-only, so a `true` answer is permanent (B0/P1). **Ghost principle:** `is_allocated` reflects *minting*, never byte-presence — a registered-empty document is a valid, addressable ghost (B3); content existence is M4's separate axis.

### 3. Content & link sub-allocators (why the frontier lives here, not in M4/M7)

`mint_content(d)`: anchor `b_C(d) = inc(d, 2) = [d.0.s_C]` (zeros(d)=2 ⇒ B6-safe), chain `(b_C(d), 1)`, emitting `[d.0.s_C.{m+1}]` with element field `[s_C, m+1]`. `mint_link(d)`: `b_L(d) = inc(b_C(d), 0) = [d.0.s_L]`, chain `(b_L(d), 1)`. The subspace identifier is the element-field's **first component** (`s_C=1`, `s_L=2`), read via M1's `subspace()` — *not* the `.0.` separator (a corpus-wide misread to guard against). `s_C ≠ s_L` is exactly what makes content and link address spaces disjoint by construction (SD/L14, T7). `mint_content`/`mint_link` advance the exact `(b_C(d),1)`/`(b_L(d),1)` frontier; the caller locks with `content_lock_key(d)`/`link_lock_key(d)` — never a coarser `(d, g)` key that could not separate content from a version chain — **byte-identically** to the advanced frontier, because both the constructor and the frontier go through the single `content_ns`/`link_ns` helper and the injective `ns_lock_key` encoding (§1).

The deep point: M3 cannot read M4's `dom(C)` or M7's `dom(L)` (the DAG forbids `M3 → M4/M7`), so the content/link frontier **is M3's own state**, advanced by the `Allocate` record M5/M7 co-stage with their value-write in one M2 composite. Allocation⇒placement⇒value-write are atomic (J0); M3's frontier and M4's `dom(C)` therefore advance together and can never diverge.

### 4. Admission gate (B6 + P8/P6 + freshness)

- **B6 (well-formedness)** — by construction: minting only ever applies `inc(parent, g)` for B6-valid `(parent, g)` (valid registered parent, g∈{1,2}, zeros budget). M1's `checked_inc` is the TA5a gate; routing every first emission through it is the defensive guard (it can only fire on a corrupted frontier).
- **P8 / P6 (parent/origin registered)** — actively enforced: `mint_document` requires `entity_level(account) == Some(Account)` and `mint_version` requires a registered source `Document` (else `NotAnAccount`/`SourceNotRegistered`); `mint_content`/`mint_link` check the home document via `is_registered_document`. `delegate` enforces the same P8 obligation for the new account's *parent* (§6). These are the *only* active structural gates — everything else about a minted address is structural.
- **Freshness (B8/V0)** — by construction from monotone frontier advance under serialized commit (below); never a runtime "is it taken?" check, because we mint rather than validate.

### 5. Principal registry & the `ω` resolver

`owns(prefix, a)` is a pure two-tumbler prefix test (O1) — coordination-free, pushable to the edge, consulting no state. **`effective_owner` (ω) is the one operation that consults Π**: longest-prefix match.

```rust
fn effective_owner(&self, a: &Address) -> Option<Principal> {
    // Only zeros ≤ 1 prefixes of `a` can be principal prefixes (O1a). Enumerate them
    // longest-first: account-tier prefixes (N·0·U[..j]) then node-tier (N[..i]).
    self.principal_tier_prefixes(a)             // ≤ depth candidates, longest first
        .find_map(|p| self.principals.get(&p).cloned())
}

fn principal_tier_prefixes(&self, a: &Address) -> impl Iterator<Item = Tumbler> + '_ {
    // a's T4-valid, zeros ≤ 1 prefixes, LONGEST FIRST (O1a). For each prefix length L from #a
    // down to 1, reconstruct a[..L] (via M1 Tumbler::new over a's first L components) and keep it
    // iff T4-valid ∧ zeros ≤ 1. validate drops the single trailing-zero length (N·0, non-T4) and
    // the zeros ≤ 1 filter caps the walk at the account field — leaving exactly the account-tier
    // (N·0·U[..j]) then node-tier (N[..i]) prefixes. Every account-tier prefix is strictly longer
    // than every node-tier one, so descending L is globally longest-first; ≤ #a (= depth)
    // candidates, never O(#allocated).
    (1..=a.tumbler().len()).rev().filter_map(move |L| {
        let p = Tumbler::new((1..=L).map(|i| a.tumbler().get(i).clone())).ok()?;
        validate(p).ok().filter(|ad| zeros(ad.tumbler()) <= 1).map(|ad| ad.tumbler().clone())
    })
}
```

The account-tier floor (O1a) is the win: we never probe document/element prefixes, so ω is O(depth) lookups, not O(addresses). The narrowing of delegation to account-tier (§6) does **not** narrow ω's candidate set — ω still considers the bootstrap node-tier principal (zeros=0) as a coverer; it only means no *new* node-tier principal can be created. **Critical discipline** (the ownership-divergence trap): a node operator's prefix *contains* every delegated account, so `owns` is true for several principals at once — only ω (longest match) arbitrates. Authorization must use ω, never bare `owns`, or the node operator falsely appears to own delegated subdomains. O2 exclusivity (exactly one ω) is a *theorem* given prefix-injectivity, which delegation's freshness check (below) enforces — no runtime uniqueness check.

The default walk above point-`get`s at most `#a` tier-prefixes. The optional `OrdMap` descending-range *upgrade* ([Open decisions](#open-build-decisions)) reads the longest coverer in one walk: `principals.range(..=a.tumbler().clone()).rev().find(|(k, _)| is_prefix(k, a.tumbler()))` — the *largest* in-map key that is a prefix of `a`, which is the *longest* prefix because a proper prefix sorts *before* its extensions (T1), so the first prefix hit walking down from `a` is the longest. Same result as the tier-prefix walk; the choice is purely |Π|/query-rate.

**Id→prefix resolution.** `create_new_document`/`fork`/`delegate` and the M5→M3 cross-owner-VERSION seam all hold a principal as a `PrincipalId` (the id is what M10 binds to a session), but `principals` is keyed by *prefix*, so id→prefix is **not** a point lookup. `principal_by_id(id)` is an O(|Π|) scan over `principals.values()` — sound because Π is account/node-tier only (O1a), hence small per node — and `principal_prefix(id) = principal_by_id(id).map(|p| p.prefix)`. The scan is *single-valued* because `delegate` enforces id-freshness (`DuplicateId`, §6) — at most one principal carries any id; without that gate `PrincipalId` would be an unconstrained second identity axis and the scan could return an arbitrary match. Because prefixes are immutable (O13) and principals persist (O12), the resolved prefix is value-stable regardless of which snapshot it is read from. A hot/retried caller can fold a recomputable `PrincipalId → Tumbler` reverse-index *hint* (never authoritative — `principals` is the source of truth); deferred to [Open decisions](#open-build-decisions).

- **Recovery/tradeoff:** Π is replay-recovered like everything else. ASN-0042's recommendation stands: default to a linear scan keeping the longest match (Π is small, per-node); upgrade to a radix trie only when |Π| or query rate demands ([Open decisions](#open-build-decisions)). An `address → owner` cache is a sound hint (a stale entry can only under-resolve to an ancestor, never over-claim, by monotonic refinement).

### 6. Delegation gate

`delegate` does its **pure** work first, before opening `transact`: it `validate`-lifts the supplied `new_prefix` to an `Address` (`NotValid` otherwise — the T4-valid half of condition (v)), which both yields that typed rejection and makes `namespace(new_prefix)`/`parent(new_prefix)`/`zeros(new_prefix)` safe to compute. From the lifted address it builds the two `LockKey`s it will hold — the new account's namespace key `ns_lock_key(namespace(new_prefix))` (to serialize the `Allocate`) **and** `principals_lock_key()` (to serialize the principal mutation and the ω/id reads, §8) — and hands both to `transact`.

**Every race-prone gate condition is then evaluated *inside* the closure, against `stg.base().m3()`, under those held locks** — not on a pre-transaction `snapshot()`. A pre-transaction snapshot read is admissible only as an optional fail-fast (to avoid opening a doomed transaction); it is never authoritative. The closure resolves the delegator (`dp := principal_prefix(delegator)`, `DelegatorUnknown` if the id names no principal — the §5 scan), evaluates O15's five conditions **plus id-freshness plus P8 plus next-form**, and — iff all pass — baptizes the new account prefix (`Allocate{new_prefix}`, advancing its account-chain frontier) and registers the principal (`RegisterPrincipal`) in that **one transaction** (atomicity is the crux; M2's `transact` gives it; a two-phase baptize-then-register could half-fail). All conditions read the lifted address:

```
(i)   ancestry      dp = pfx(delegator) ≺ new_prefix                 is_prefix + strict      [monotone — pfx immutable O13]
(ii)  authorization matches!(effective_owner(new_prefix), Some(p) if p.id == delegator)   longest coverer  [NON-MONOTONE → in-closure]
(iii) account-tier  zeros(new_prefix) == 1                           O1a (narrowed ≤1→==1)   [monotone — pure; ⇒ NotAccountTier]
(iv)  top-down      no existing principal strictly under new_prefix  OrdMap single probe (below) [NON-MONOTONE → in-closure]
(v)   fresh-valid   T4-valid(new_prefix) ∧ !is_allocated(new_prefix) O1b prefix-injectivity  [T4 monotone; !is_allocated NON-MONOTONE → in-closure]
      id-fresh      principal_by_id(new_id).is_none()                id-injectivity → DuplicateId  [NON-MONOTONE → in-closure]
      parent-reg    entity_level(parent(new_prefix)).is_some()       P8 → ParentNotRegistered  [monotone — E append-only P1]
      next-form     new_prefix == next_in(namespace(new_prefix))     O17c → NotNextForm      [NON-MONOTONE → in-closure]
```

**(iv), concretely.** Because `principals` is an `OrdMap` under tumbler order and the extensions of `new_prefix` form a contiguous block (T5), a *single* probe settles top-down: `principals.range(new_prefix.tumbler().clone()..)`, take the first key `k`, and reject `NotTopDown` iff `is_prefix(new_prefix.tumbler(), k) && k != new_prefix.tumbler()` — a registered principal sits strictly under `new_prefix`. If that first key ≥ `new_prefix` is *not* an extension of `new_prefix`, none is (the block is empty). No full scan.

**Why (iii) is `== 1`, not O15(iii)'s `≤ 1` (the fix for internal node minting — [Conflicts resolved](#conflicts-resolved) §7).** O15(iii) reads `zeros(pfx(π')) ≤ 1`, which also admits a *node-tier* delegate (zeros=0). Composed with ASN‑0040's `baptize(node,1)` — which mints a *child node* (`baptize([1],1) = [1,1]`, still zeros=0) — the `≤ 1` form would let `delegate` mint a node: the bootstrap `[1]` supplying `new_prefix = [1,1]` passes (i) `[1] ≺ [1,1]`, (ii) `ω([1,1]) = bootstrap`, (iv) nothing below, (v) `[1,1] ∉ nodes`, id-fresh, parent-reg `entity_level([1]) = Some(Node)`, and next-form (`next_in(([1],1)) = inc([1],1) = [1,1]`) — registering a principal at a freshly **minted node**. That violates ASN‑0047 NodeBaptism (*no docuverse transition mints a node address*) and this design's own guarantee that nodes arrive only via `register_node`. We therefore **narrow O15(iii) `≤1 → ==1`** and **suppress ASN‑0040's `baptize(node,1)` child-node capability**: a node-tier `new_prefix` (zeros=0) — and equally a document-tier one (zeros≥2) — is rejected `NotAccountTier`. **Consequence:** beyond bootstrap, principals exist only at accounts; no per-node principal can be created by delegation, so every provisioned node stays bootstrap-owned via ω until an account is delegated beneath it — re-admitting node-tier principals is flagged under [Open decisions](#open-build-decisions).

**Why in-closure is mandatory (the fix for the pre-snapshot race).** The non-monotone conditions — (ii), (iv), the `!is_allocated` half of (v), id-fresh, next-form — each read state a concurrent `delegate` can advance. Evaluated on a pre-transaction snapshot and then committed blindly, two delegations under the same parent both pass `next-form`/`fresh`/`id-fresh` on that stale view and commit in turn; the second's `RegisterPrincipal{new_prefix, …}` **overwrites** the first at the identical prefix, handing one address to two principals — an O1b/O13 violation and address reuse, the one fatal error. This is harmful **even under M2 v1's global applier lock**: that lock serializes the *commits*, but a pre-snapshot pre-check has already passed *outside* it, and the closure that follows does not re-check. Evaluating the gate in-closure under the held `principals_lock_key()` + namespace key makes the `base()` reads authoritative — no concurrent ω-mutator or same-namespace allocation can commit between the read and our commit — so the losing delegation re-reads the winner's advance and is cleanly rejected (`NotNextForm`/`NotFresh`/`DuplicateId`). The monotone conditions (i, iii, parent-reg) are stale-safe — `pfx` is immutable (O13), `zeros` is pure, and E is append-only (P1) so a registered parent stays registered — so a pre-snapshot fail-fast on them is sound (only their *acceptance* direction matters, and it cannot regress).

Condition (ii) reuses ω directly. **`id-fresh` actively enforces `PrincipalId` injectivity** — the id-axis mirror of (v)'s prefix-freshness. `principals` keys by prefix, but carries a second identity axis, `PrincipalId`, on which `principal_by_id`/`principal_prefix` and the `effective_owner(account).id == caller` auth gate all resolve; (v) guarantees *prefix* uniqueness but says nothing about ids. Without `id-fresh`, a reused id — a fixed "admin" id, `id = hash(user)`, or simply `PrincipalId(0) = BOOTSTRAP_PRINCIPAL` — would make `principal_by_id(new_id)` return an arbitrary match, so `fork`/cross-owner VERSION would mint under the wrong account and `create_new_document`'s ω-gate would mis-authorize (an O8/O5 violation). Rejecting `principal_by_id(new_id).is_some()` with `DuplicateId` makes one id ↦ at most one principal, so all three id-keyed paths are well-defined. Note the id race differs in *shape* from the prefix-collision race: prefix-collision is **same-namespace** (two delegations at the *same* `new_prefix`, serialized by the namespace lock `delegate` also holds), whereas id-collision is **cross-namespace** (two delegations with *different* `new_prefix` but the same `new_id`). Only the *single global* `principals_lock_key()` serializes the latter — a per-subtree principal lock would not (§8, [Open decisions](#open-build-decisions)).

**`parent-reg` (P8) is the fix for the ASN‑0040/0042-vs-ASN‑0047 conflict** ([Conflicts resolved](#conflicts-resolved) §5): B6 alone would let an account-tier delegator baptize a sub-account under an account that was never registered. The explicit `entity_level(parent(new_prefix)).is_some()` check (the new account's parent node — or, when delegating a sub-account, the parent account — must be a registered entity) enforces `parent(e) ∈ E`. It is stale-safe (E only grows), so its position relative to the lock is immaterial; it is grouped with the in-closure gate purely to keep one evaluation site.

**The next-form check** computes `next_in(namespace(new_prefix))` — `namespace` (Core data model) being the very `(parent, g)` key the staged `Allocate` advances and the namespace lock is held on — and maps its `GateViolation` (a malformed namespace that cannot produce a next address) to `NotNextForm`. **Next-form is MANDATORY under the counter representation**, not relaxable: the frontier stores only the count `m`, so accepting a non-next supplied prefix (e.g. setting `frontiers[(N,2)] := 5` from `[N.0.5]` while the frontier is 1) would make `is_allocated` report phantom, never-baptized entities `[N.0.2..4]` — breaking B1/B3 and the registry's correctness. Relaxing it requires switching the frontier to an explicit allocated-set ([Open decisions](#open-build-decisions)). A caller obtains the required next-form value from the `next_account_prefix(parent)` peek (§ Public interface C), rather than guess-and-retry on `NotNextForm`.

Delegation always produces an **account** (zeros=1: condition (iii)'s strict `== 1` forces it directly — see the narrowing above; internal baptism never mints a zeros=0 node, and nodes arrive only via `register_node`), advancing an account-chain frontier and adding one principal; it is the *only* non-bootstrap entry for principals. Because both `LockKey`s are computed from the validate-lifted prefix *before* `transact` opens (M2 holds `keys` for the txn's duration), the held namespace lock and the in-closure `next_in(namespace(new_prefix))` advance the **same** `(parent, g)` key, and the held `principals_lock_key()` covers the in-closure `id-fresh`/`top-down`/authorization reads against every concurrent delegation (§8).

### 7. CREATENEWDOCUMENT, fork, node baptism, genesis

- **`create_new_document`** locks `[document_lock_key(account), principals_lock_key()]`; inside the closure, against `stg.base().m3()`, it evaluates `matches!(stg.base().m3().effective_owner(account), Some(p) if p.id == caller)` (`NotOwner` if ω is absent — `None` — or names another principal), then mints via `mint_document` off `stg.working().m3()`, stages one `Allocate` (lifted `rec.into()`), and returns the address with its commit `Seq` post-commit. **ω(account) is stable** for an existing account: the only `zeros ≤ 1` prefixes covering `account` are its node ancestors and `account` itself, all already allocated, so no concurrent `delegate` (which requires a *fresh* target) can introduce a longer coverer — a sub-account sits *below* `account` and never covers it. The read is therefore stale-safe; it is evaluated in-closure for uniformity with the rest of the op (and could equally be a pre-read), and the held `principals_lock_key()` is **defensive/harmless-redundant, not load-bearing** (§8). It registers d and **stops** — no `M(d)=∅` write into M5. This is the deliberate divergence from ASN-0103's eager recommendation ([Conflicts resolved](#conflicts-resolved)). No idempotency key (identity is the address, ASN-0103): a retried lost-ack yields a harmless orphan empty document; exactly-once lives at M10's session layer if wanted.
- **`fork`** implements **O10 (DenialAsFork), account-tier case only**: it resolves `pfx(caller)` via `principal_prefix(caller)` (an unknown id → it returns `Err(TxnError::Rejected(OpError::NotOwner))` **directly, opening no transaction** — an unregistered caller owns nothing) and reduces to `create_new_document(caller, pfx(caller))`, minting a fresh document one structural tier below an *account-tier* caller's prefix (O10's `zeros(a')=zeros(pfx)+1` ⇒ a document, zeros=2), with M5 wiring the shared content separately (mechanism/policy split). `fork` opens no transaction of its own — the `principal_prefix` read is value-stable because prefixes are immutable (O13) — and lets `create_new_document` drive the commit (returning its `(Address, Seq)`), whose ω-auth passes by construction (`ω(pfx(caller))=caller` is stable in every reachable state by SelfOwnershipAtPrefix — nothing can sit at a longer prefix ≼ pfx(caller)). O10 itself is *not* account-scoped — it would also let a node-tier `π` mint a self-owned *account* one tier below its node prefix — but M3 scopes `fork` to the document case: a node-tier caller (whose `pfx(caller)` is a node, not an account) is rejected with the typed `OpError::Mint(MintError::NotAnAccount)` (raised by `mint_document`'s `Account(account)` check, never a silent skip). That rejection is **not** "go delegate instead": delegation mints a *new* principal and moves effective ownership to it (O7), so it does not deliver O10's self-owned account under the *same* node principal — the node-tier O10 case is genuinely **dropped** (see [Conflicts resolved](#conflicts-resolved) §6). Cite **O10** here, *not* ASN‑0123 V9 — V9 governs cross-owner VERSION, a different operation.
- **`register_node`** is the provisioning seam: the address is *supplied* (NodeBaptism mints outside the docuverse), M3 only validates freshness, `Level::Node`, and bootstrap lineage `[1] ≼ addr`, then adds to `nodes`, returning the node address with its commit `Seq`. Its transact holds `node_lock_key()` — a single coarse node-registry key: node admission needs no namespace lock for *safety* (the `OrdSet` insert is idempotent and freshness is monotone), but holding the coarse key makes a concurrent duplicate `RegisterNode` surface `NotFresh` rather than silently coalesce under per-key concurrency (redundant under M2 v1's global lock, exactly like `principals_lock_key`). This is the one validate-not-mint path (see conflict 1).
- **`genesis`** = `nodes={[1]}`, `frontiers={}`, `Π={[1] → Principal{BOOTSTRAP_PRINCIPAL,[1]}}` (Σ₀ + O14). `BOOTSTRAP_PRINCIPAL` is a fixed `PrincipalId` constant — the `effective_owner(account).id == caller` auth gate keys on it, so M10 must bind the bootstrap session to it; `delegate`'s `id-fresh` gate then prevents any later principal from re-claiming id 0. The bootstrap principal is the system's *only* node-tier principal (zeros=0), since delegation is now account-tier only (§6). "Load empty journal" and "fresh genesis" are the same code path.

### 8. Durability, serialization, recovery

M3 **rides M2** — it builds no WAL of its own. Its three structures are part of `WorldState`, recovered by M2's checkpoint-load + replay; B4 atomicity (frontier advance and record durable *together*) is exactly M2's `transact` commit. The one invariant the durability protects — **never mint an address twice** — holds because the frontier only advances, `apply_ns` is deterministic, and same-namespace commits are serialized by handing M2 the **true-namespace** `LockKey` (`content`/`link`/`version`/`document_lock_key`, each computed from the actual `NsKey` parent — *not* a `(home_doc, g)` pair, which cannot tell the three g=1 chains under a document apart). Distinct namespaces carry distinct keys, so independent owners/documents allocate concurrently (B7); only same-namespace serializes (B8/B-Seq).

**Correctness must not lean on M2 v1's global applier lock.** That lock currently masks any lock-key defect; per-key concurrency would expose a same-namespace key collision as address reuse — the one fatal error. So the lock keys mirror the frontier keys exactly, **by construction**: each `mint_*` advances `next_in(*_ns(..))` and the caller locks with `Self::*_lock_key(..)`, and `*_lock_key(..) = ns_lock_key(*_ns(..))` — one `*_ns` helper, one injective space-tagged `ns_lock_key` encoding (§1) — so the held lock key and the staged frontier key are the *same bytes*, with nothing in the mint's return to drift. The distinct `Space::Namespace`/`Space::Principals`/`Space::Nodes` tags keep the three key spaces from aliasing each other.

**`delegate`'s race-prone gates are read *inside* the `transact` closure** (off `stg.base().m3()`), within the held-lock region — a pre-transaction `snapshot()` read sits outside every lock and so can only ever be a fail-fast, never authoritative for those. `delegate` therefore holds `principals_lock_key()` **load-bearingly**: its `new_prefix` is *fresh*, and the top-down / next-form / authorization reads race against concurrent **same-namespace** delegations while the id-freshness read races against concurrent **same-id** delegations — which may target a *different* namespace (a different `new_prefix` carrying the same `new_id`). Because that id race is **cross-namespace**, only the *single global* principal-registry key serializes it (alongside the same-namespace reads and the `RegisterPrincipal` insert); a per-subtree principal key would let two same-id delegations in different subtrees both pass id-freshness off stale `base()` and both commit `RegisterPrincipal{_, new_id}` — a duplicate id, the O1b-mirror violation. (The prefix-collision race is already covered by the namespace lock `delegate` also holds; see [Open decisions](#open-build-decisions).) `create_new_document` holds the same key only **defensively**: its `ω(account)` read is *stale-safe* (ω of an existing account is stable — no concurrent delegation can introduce a longer coverer, a sub-account sitting *below* the account and never covering it), so the lock is harmless-redundant, not load-bearing. **M5's cross-owner VERSION needs no principal lock at all** — it **pre-reads** the stable `ω(d_src)` off a snapshot, resolves the owned-vs-cross-owner branch, and holds only the single matching namespace lock (`version_lock_key`/`document_lock_key`). `register_node` holds the coarse `node_lock_key()` to keep its `NotFresh` rejection under per-key concurrency, not for safety (the insert is idempotent). All three principal/node locks are redundant under v1's global applier lock.

The minted address (and its commit `Seq`) is returned only after M2 commits (commit-before-acknowledge), so a crash never loses a handed-out address — over-shooting (a gap) is safe (permanent ghost), reuse is fatal, and we never reuse.

## Invariants & contracts

### By construction (fall out of the data model)
- **Permanence / irrevocability** — `frontiers`/`nodes`/`principals` only grow; there is *no* delete API. [ASN-0040 B0/B0★, ASN-0047 P1/P3, ASN-0042 O12/O13]
- **Contiguity / gap-free** — the count representation makes a gap unrepresentable. [ASN-0040 B1]
- **Determinism & finiteness** — `next_in` is a pure function of the frontier; growth is one-at-a-time. [ASN-0040 B2/B_fin]
- **Unbounded extent** — `Nat = BigUint` for every ordinal and count. [ASN-0040 B9]
- **T4-validity of every minted address** — valid parents + `checked_inc`. [ASN-0040 B10, ASN-0093 StoreT4Validity]
- **Membership correctness (no false positives)** — every T4-valid `a` is *exactly* the `ordinal(a)`-th member `c_{ordinal(a)}` of its decomposed `(parent, g)` namespace, so the `entity_level`/`is_allocated` decompose-and-range check is exact chain membership, not an approximation. [ASN-0040 `S(p,d)` canonical form, ASN-0034 T4b unique-parse → *§2*]
- **Cross-namespace uniqueness; document↔version separation; content↔link disjointness** — distinct `(p,g)` keys, `s_C ≠ s_L`. [ASN-0040 B7/B8-cross, ASN-0093 SD/Cross-doc, ASN-0123 V0/VD, ASN-0034 T10]
- **Content-independence (ghosts)** — registry is M3, content is M4; allocated ≠ has-bytes. [ASN-0040 B3]
- **No internal node minting** — internal baptism applies only `inc(parent, g)` for a non-node result ((iii) `== 1`); a zeros=0 address never arises from a mint or `delegate`. [ASN-0047 NodeBaptism → *§6, Conflicts §7*]
- **Ownership exclusivity, refinement, node-locality** — longest-prefix match over an append-only immutable-prefix Π. [ASN-0042 O2/O3/O8/O9]

### By active enforcement (M3 must guard)
- **Same-namespace uniqueness** — serialize commits per namespace via the **true-namespace** `LockKey` (`content`/`link`/`version`/`document_lock_key`, computed from the actual `NsKey` parent through the injective, space-tagged `ns_lock_key` encoding — one code path shared with the frontier, so the lock key ≡ the frontier key byte-for-byte; never a `(home_doc, g)` pair) to M2. [ASN-0040 B8/B-Seq] → *the allocator + M2 transact, §1/§8*
- **Atomicity (frontier advance + record durable together)** — M2's `transact`/commit marker. [ASN-0040 B4]
- **Parent/origin registered (P8/P6/C2/L1a)** — `entity_level`/`is_registered_document` before minting (`mint_document`/`mint_version`/`mint_content`/`mint_link`) *and* `entity_level(parent(new_prefix))` in `delegate` (P8 for delegated accounts — [Conflicts resolved](#conflicts-resolved) §5). [ASN-0047 P8/P6, ASN-0093 C2/L1a] → *§4, §6*
- **Account-tier delegation (no node minting)** — `delegate` condition (iii) narrowed `≤1 → ==1`; a zeros≠1 `new_prefix` → `NotAccountTier`. [ASN-0047 NodeBaptism, narrowing ASN-0042 O15(iii)] → *§6, Conflicts §7*
- **Prefix-injectivity & account-floor** — delegation (v) freshness + (iii) tier (`==1`). [ASN-0042 O1b/O1a]
- **PrincipalId injectivity** — `delegate` rejects a reused id (`principal_by_id(new_id).is_some()` → `DuplicateId`), so `principal_by_id`/`principal_prefix`/the ω-auth gate are single-valued (one id ↦ at most one principal). Enforced under the **single global** `principals_lock_key()`, since the id-freshness race is cross-namespace (a per-subtree lock would not serialize it — §8). [id-axis mirror of ASN-0042 O1b] → *§6, §8*
- **Delegation gate (5 conditions + id-fresh + P8 + next-form)** — `delegate`; the non-monotone conditions (ii/iv/v-freshness/id-fresh/next-form) evaluated in-closure under the held locks. [ASN-0042 O15] → *§6*
- **Authorization by ω (never bare `owns`)** — `create_new_document`/`fork`/`delegate`/M5-VERSION; ω resolves the authorizing/branching principal. For `delegate` the in-closure reads under `principals_lock_key()` are **load-bearing** (fresh prefix); `create_new_document`/`fork`/M5-VERSION authorize/branch on a *stable* ω (defensive lock / pre-read, §8). [ASN-0042 O5, ownership-divergence] → *§5/§7/§8*
- **Node freshness + bootstrap lineage** — `register_node`. [ASN-0047 NodeBaptism] → *§7*
- **Commit-before-return** — address (and `Seq`) returned only post-commit. [ASN-0040 finality, ASN-0103 commit point]

## Dependencies & seams

**Upstream — M1 (calls):** `checked_inc`/`inc_preserves_t4` (B6 gate on every mint), `inc` (anchors `b_C = inc(d,2)`/`b_L`), `shift` (ordinal-only — mints `cₘ₊₁` from the gated `c₁`, §1), `parent`/`zeros`/`ordinal` (decomposition & membership — `zeros`/`ordinal` over `&Tumbler`, `parent` over `&Address`, so call sites project via `.tumbler()`/`validate`), `classify`/`Level`/field projections (entity-level + acct/node prefixes for ω), `is_prefix`/`validate`, `subspace` (content vs link). M3 holds **no** address algebra of its own.

**Upstream — M2 (calls):** `transact(&[<namespace LockKey>], …)` — the namespace key from `content`/`link`/`version`/`document_lock_key` (plus `principals_lock_key()` for `delegate` (load-bearing) and `create_new_document` (defensive), and `node_lock_key()` for `register_node`, §8) — for every mutating op (atomic + serialized + durable), receiving each op's commit `Seq` from `transact`'s `(T, Seq)` return; `snapshot()` for query reads; M3 provides its fold `M3State::apply_ns` — which the engine's `World::apply` dispatches via the `Record::Ns` variant — and relies on M2's **default `rebuild_derived`** (its slice is fully `Serialize`d, nothing to re-seed). M3 stages `M3Rec` **lifted to `W::Record` via the `W::Record: From<M3Rec>` bound** (`stg.push(rec.into())` — Public interface B); M2 owns ordering/durability/recovery. The 1-byte space tags (`Space::Namespace`/`Principals`/`Nodes`) are **declared in** M2's single central `Space` enum, which lives in `skep-kernel` below every store (not the engine assembler crate — that would cycle); M3 is the one store drawing *three* tags from it (three serialization domains). The contract's one-tag-*per-store* line is *guidance*; its hard rule is tag **uniqueness**, which three distinct `Space` variants satisfy — and those variants live in skep-kernel's enum, not "reserved" by skep-engine (which only assembles `World`/`Record`).

**Downstream seams M3 exposes (build neighbors against these):**
Consumers reach M3's `&self` methods through the `HasM3::m3()` accessor — `stg.working().m3()` inside a composite, `snapshot.world().m3()` for a read (M2's `Staging::working`/`Snapshot::world` hand back `&W: HasM3`, not `&M3State`); the `*_lock_key` associated functions are called on the type. So e.g. M5's INSERT does `stg.working().m3().mint_content(d)` and takes its key from `M3State::content_lock_key(d)` before the closure; the mint hands back an `M3Rec` the caller stages via the same `W::Record: From<M3Rec>` lift.
- **M5 → M3:** `is_registered_document(d)` (edit precondition); `effective_owner(d_src)` (CREATENEWVERSION's owned-vs-cross-owner branch — ASN‑0123 V8/V9: owned ⇒ `mint_version` on `(d_src,1)`; cross-owner ⇒ `principal_prefix(forker_id)` → the forker's account-tier prefix `pfx(π)`, then `mint_document(pfx(π))` on `(pfx(π),2)` — M5 holds the forker as a `PrincipalId`, consistent with M3's id-centric ops, and `principal_prefix` is the §5 id→prefix query); the *pure* mints — `mint_content` (INSERT), `mint_version`/`mint_document` (VERSION) — each advancing a namespace frontier (M5 takes the matching key from the `*_lock_key` constructor for transact's `keys` arg *before* the closure, then stages the returned `M3Rec`); `is_allocated(a)` (content-side referential-integrity oracle for COPY transclusion — COPY mints no content, it only checks this). M5 never reads M4 for this — allocation status is M3's. **Because the VERSION namespace lock is branch-dependent (`version_lock_key(d_src)` vs `document_lock_key(pfx(π))`) and the branch *is* `ω(d_src)`, M5 must resolve ω *before* opening the closure** — which is sound because `ω(d_src)` is **stable** for an existing `d_src`: its account, and any node ancestor, are already allocated, so no concurrent `delegate` (which needs a *fresh* target) can introduce a longer coverer, and a sub-account sits *below* `d_src`'s account and never covers it. M5 therefore **pre-reads** `ω(d_src)` (and, cross-owner, `principal_prefix(forker_id)`) off a snapshot — exactly as `fork` pre-reads the stable `principal_prefix(caller)` — resolves the branch, holds the single matching namespace lock, and needs **no** `principals_lock_key()`. (This is the buildable form: M5 cannot pick a branch-dependent lock before the closure while reading the branch only inside it; the stable pre-read removes the contradiction.)
- **M7 → M3:** `mint_link` *pure* (inside MAKELINK; M7 locks via `link_lock_key(d)` before the closure, then stages the returned `M3Rec`); `is_registered_document(d)` (link's home).
- **M6, M8 → M3:** `is_registered_document(d)` — they convert *registered-but-no-arrangement* → ⟨⟩ and *unregistered* → fail. M3 supplies the bool; the ⟨⟩-vs-fail *query semantics* are theirs.
- **M9 → M3:** `effective_owner`/`is_registered_document` (residence resolution); pred-def content is allocated indirectly via M5's composite (M9→M5→M3).
- **M10 → M3:** dispatches `create_new_document`/`delegate`/`register_node`/`fork`; each returns `(Address, Seq)`, so M10 surfaces the commit `Seq` as the operation's linearization coordinate uniformly with the store-driven ops; binds the bootstrap session to `BOOTSTRAP_PRINCIPAL`; may resolve a bound session's prefix via `principal_prefix` for echo/validation (same prefix-keyed registry, so M10 reuses the §5 query rather than re-deriving it); and may peek the next delegable account prefix via `next_account_prefix(node)` to construct `delegate`'s `new_prefix` instead of guess-and-retry on `NotNextForm`.

## Conflicts resolved

1. **Mint vs validate document addresses (ASN-0093 K.σ vs ASN-0047 K.δ / ASN-0103).** ASN-0093's `K.σ` *validates* a caller-supplied document address; ASN-0047/0103 *mint* it. ASN-0093 itself defers "document-address origination to the entity-allocation layer" — **which is M3**. Resolution: M3 **mints** accounts/documents/versions/content/links via the frontier; the validate-not-mint path survives only for **nodes** (NodeBaptism originates them externally, M3 validates).

2. **"Recompute the cursor from the store" (ASN-0093/0047) vs the module DAG.** Those notes treat C/L/registry as one substrate and recompute the frontier from `dom(C)`/`dom(L)`. Our split forbids `M3 → M4/M7`, so M3 cannot read those stores. Resolution: **M3 owns and persists the frontier for all chains, including content/link**, advanced by `Allocate` records that M5/M7 co-stage with their value-writes in one M2 composite. Same Lampson hint discipline (recomputable by replay), different source-of-truth boundary (M3's own allocation journal, not M4/M7).

3. **Eager `M(d)=∅` (ASN-0103) vs lazy arrangement (decomposition).** ASN-0103 recommends writing the empty arrangement at creation — which would write M5 from M3 and close an `M3 → M5` cycle. Resolution: `create_new_document` **registers d only**; the arrangement is implicit/lazy in M5. M6/M8 read *registered-with-no-arrangement* as ⟨⟩. The DAG stays acyclic (`M5 → M3` only).

4. **`owns` (containment) vs `ω` (longest-match) for authorization.** ASN-0103's literal `pfx(π) ≼ A` precondition is bare containment, but in the multi-tier model a node operator contains delegated accounts. Resolution: every authorization gate uses **`ω`** (the delegate, not the ancestor), per O5 and the ownership-divergence finding.

5. **Baptism under an unbaptized parent (ASN‑0040/0042) vs P8 (ASN‑0047).** B6 (ValidDepth) does *not* require the parent `p ∈ B`, so ASN‑0040/0042's delegation would let a delegator baptize an account under a node/account that was never registered. ASN‑0047 P8 forbids it (`parent(e) ∈ E` for every non-node entity), and this design commits to P8 (it lists P8 under active enforcement). Resolution: **P8 wins for delegated accounts** — `delegate` adds the `entity_level(parent(new_prefix)).is_some()` gate (`ParentNotRegistered` otherwise). `mint_document`/`mint_version` already discharged P8 via their `entity_level` checks; `delegate` was the one account-minting path that skipped it.

6. **O10 node-tier fork (ASN‑0042 O10) vs the account ≡ principal model.** O10 (DenialAsFork) lets *any* principal fork a self-owned address one structural tier below its prefix — including a **node-tier** principal minting a self-owned *account* (zeros=1) with **no** new principal. M3 deliberately scopes `fork` to the **account-tier** case only: a fork mints a *document* (zeros=2) under an account-tier caller's prefix. This makes M3 treat an account-tier prefix as the unit of principal identity — coherent with, and assumed by, `create_new_document`'s ω-authorization (the authorizing principal sits at an account, and `fork` relies on `ω(pfx(caller))=caller`). **Resolution / consequence:** the node-tier O10 case is **dropped, not relocated.** A node-tier caller is rejected `Mint(NotAnAccount)`; this is *not* silently equivalent to "delegate an account first," because `delegate` mints a **new** principal and moves effective ownership to it (O7), whereas O10's node-tier fork would leave the new account owned by the *same* node principal. **The load-bearing reason for the drop** (not mere taste): a node-tier fork would register an *account* (zeros=1) with **no account principal of its own** — covered only by the node principal via ω — which breaks the implicit invariant that *every registered account carries its own account principal*. `create_new_document`'s ω-authorization leans on exactly that invariant: it reads `ω(account)` as the account's *own* principal (`p.id == caller`), never an ancestor, and its stale-safety argument (§7) holds *because* an account never exists without a principal sitting at its prefix. Manufacturing principal-less accounts would defeat both. We accept the narrowing — an account is the natural home of a principal, and a node operator provisioning accounts *via delegation* (new principals) is the intended path — and flag re-admitting node-tier `fork` under [Open decisions](#open-build-decisions).

7. **Internal node minting via delegation (ASN‑0040 `baptize(node,1)` + ASN‑0042 O15(iii) `≤1`) vs NodeBaptism (ASN‑0047).** O15(iii) admits a delegate prefix with `zeros ≤ 1`, and ASN‑0040's `baptize(p,1)` with a *node* parent `p` mints a **child node** (`baptize([1],1) = [1,1]`, still zeros=0) — ASN‑0040 *does* have a node-admission mechanism, contrary to a naive reading. Composed, `delegate` would mint a child node and register a principal there: a node-tier delegator `[1]` supplying `[1,1]` passes every condition (§6). But ASN‑0047 NodeBaptism states *no docuverse transition mints a node address*, and this design originates nodes only via `register_node`. Resolution: **narrow O15(iii) `≤1 → ==1`** and **suppress ASN‑0040's `baptize(node,1)` child-node capability** — `delegate` produces an *account* (zeros=1) only; a node-tier (or document-tier) `new_prefix` is rejected `NotAccountTier`. **Consequence:** beyond bootstrap, principals exist only at accounts (no per-node principals); every provisioned node is bootstrap-owned via ω until an account is delegated beneath it — re-admitting node-tier principals is flagged under [Open decisions](#open-build-decisions).

## Open build decisions

- **Frontier representation:** counter map (recommended; B1 free) vs. explicit allocated-set/trie (fast arbitrary-`t` membership, contiguity becomes enforced — **and the only representation under which a gap-creating supplied delegate-prefix is admissible**; see Delegate-prefix policy) vs. hierarchical tree (only if subtree/range queries are needed elsewhere).
- **`Space`-tag encoding:** three distinct top-level variants (`Space::Namespace`/`Principals`/`Nodes`) in skep-kernel's central enum (recommended — satisfies the contract's tag-uniqueness hard rule directly) vs. one `Space::M3` tag plus a sub-tag byte distinguishing the three domains (literal one-tag-per-store conformance, byte-equivalent). Either way the variants live in `skep-kernel`, never the engine assembler.
- **ω resolver structure & caching:** linear scan over Π (default, ASN-0042) vs. `OrdMap` descending range-walk (`principals.range(..=a.tumbler().clone()).rev().find(|(k, _)| is_prefix(k, a.tumbler()))`, §5) vs. radix/PATRICIA trie — sized to |Π| and query rate; plus an optional `address → owner` hint cache.
- **Id→prefix resolution:** default O(|Π|) `principal_by_id` scan over `principals` (Π small, O1a; single-valued by `delegate`'s id-freshness gate); fold a recomputable `im::HashMap<PrincipalId, Tumbler>` reverse-index *hint* (and maintain it in `apply_ns` alongside `RegisterPrincipal`) only if id-keyed lookups get hot — never authoritative, `principals` stays the source of truth.
- **Delegate-prefix policy** (under the counter rep, next-form is *mandatory* — §6; the open choice is *who picks the address*, not whether to check it): (a) keep `delegate(new_prefix)` and *validate* the supplied prefix is next-form (current design, O17c-faithful) — a caller obtains the required next-form value from the `next_account_prefix` peek (§ Public interface C), so this path is callable without guess-and-retry; or (b) drop `new_prefix` from the signature and have `delegate` *mint* the next account slot (next-by-construction, no check) — Green-faithful, but the caller no longer names the prefix. Admitting an *arbitrary* (gap-creating) supplied prefix is unsound here — it writes phantom entities into the count-compressed registry — and would require switching the frontier to an explicit allocated-set; reaching a chosen non-next prefix under the counter rep instead means baptizing the intervening slots (filling the gap, at the cost of extra allocations).
- **Per-node principals:** delegation is now account-tier only ((iii) `== 1`, §6 / [Conflicts resolved](#conflicts-resolved) §7), so beyond bootstrap no principal sits at a node — every provisioned node is bootstrap-owned via ω until an account is delegated beneath it. Admit a node-tier principal — a registration variant that registers a principal at a `zeros=0` prefix *without* minting the node (the node still arriving via `register_node`) — only if multiple independent node operators each need to own their own subtree. This is distinct from the dropped node-tier `fork` (below): one is about *who owns a node*, the other about *forking a self-owned account under a node*.
- **Node-tier `fork` (O10):** dropped today ([Conflicts resolved](#conflicts-resolved) §6); re-admit a node-principal forking a *self-owned* account (no new principal, ownership stays at the node) only if that provisioning path is needed — it requires a node-tier "mint a self-owned account" branch distinct from `delegate` (which moves ownership to a new principal), **and relaxing the "every registered account carries its own account principal" invariant that `create_new_document`'s ω-authorization leans on** (Conflicts §6).
- **Serialization granularity:** the per-namespace `LockKey` (recommended — concurrency by B7) vs. a single global writer. **Resolved default:** `delegate` holds `principals_lock_key()` **load-bearingly** (its fresh-prefix top-down / next-form / authorization reads race against concurrent same-namespace delegations, and its id-freshness read against concurrent same-id delegations — which can target a *different* namespace, §8); `create_new_document` holds it **defensively** (its `ω(account)` read is stale-safe — ω of an existing account is stable, §8); M5's cross-owner VERSION holds **no** principal lock, pre-reading the stable `ω(d_src)`; `register_node` holds `node_lock_key()` to preserve `NotFresh`. All are redundant under v1's global lock. The remaining question is `delegate`'s principal-lock *granularity*, and it is **constrained**: a per-account-subtree key is **unsafe** — id-freshness races *across* subtrees (same `new_id`, different `new_prefix`), which a per-subtree lock would not serialize → duplicate id. The only sound finer granularity than the single global `principals_lock_key()` is a per-***id*** key (`Space::Principals` tag + `new_id` bytes), which serializes exactly the same-id delegations id-freshness needs, with the *prefix*-collision (same-namespace) race covered separately by the namespace lock `delegate` already holds. Default to the single global key.
- **Record delegator identity vs. recompute the forest** (NestingByDelegation): recompute suffices while refinement stays monotonic (no ownership transfer); store it only if transfer is later introduced.
- **Node tracking:** explicit `OrdSet` for all nodes (recommended — tolerates non-contiguous external minting) vs. a node-frontier if provisioning guarantees contiguity.
- **`PrincipalId` shape & session binding:** opaque here; id *uniqueness* is now enforced inside M3 by `delegate`'s `DuplicateId` gate (§6), so M10 need not guarantee it — what remains M10's is the session→id binding and idempotency/exactly-once for retried `create_new_document`.
