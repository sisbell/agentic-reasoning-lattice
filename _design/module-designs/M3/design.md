# M3 — Namespace: Allocation, Registry & Ownership

## Purpose & boundary

M3 owns the **authoritative permanent name space**: it mints every fresh, globally-unique, T4-valid address the system ever uses, records which organizational entities (nodes, accounts, documents) exist, and answers *"is this allocated?"* and *"who owns this?"* by prefix. It is the single minting authority and the single arbiter of the entity/principal sets. One thing well: **it owns identity, not content.** It does *not* store bytes (M4), arrangements (M5), or link values (M7); it does *not* materialize a new document's arrangement (lazy, in M5 — see [Conflicts resolved](#conflicts-resolved)); it does *not* originate node addresses (those arrive from the network-provisioning boundary, NodeBaptism); it does *not* run the request lifecycle or bind sessions to principals (M10). It hands every store a fresh owned address plus two cheap structural answers, and persists its registry + frontier through M2.

## Public interface

Indices 1-based (M1 convention). All types `Tumbler`/`Address`/`Level`/`Span`/`Nat` are M1's; `Kernel`/`Snapshot`/`LockKey`/`Seq`/`TxnError` are M2's.

```rust
#[derive(Clone, Copy, PartialEq, Eq, Hash, Debug)]
pub struct PrincipalId(pub u64);                 // opaque external identity, supplied by M10/session
#[derive(Clone)] pub struct Principal { pub id: PrincipalId, pub prefix: Address }  // prefix: T4-valid, zeros ≤ 1
pub const BOOTSTRAP_PRINCIPAL: PrincipalId = PrincipalId(0);  // π₀'s fixed id (genesis); the ω-auth gate keys on it

pub enum MintError    { HomeNotRegistered, SourceNotRegistered, NotAnAccount, Gate(GateViolation) }
pub enum OpError      { NotOwner, NotAnAccount, NotRegistered, Mint(MintError) }
pub enum DelegateError{ DelegatorUnknown, NotAncestor, NotAuthorized, NotAccountTier,
                        NotTopDown, NotFresh, NotNextForm, NotValid, ParentNotRegistered }
pub enum NodeError    { NotValid, NotNode, NotFresh, NotDescendantOfBootstrap }
```

### A. Frontier allocation — *pure, composable* (folded into M5/M7 composites; M2 contract 3)

Each returns the minted address, the one journal delta the caller stages, **and the namespace `LockKey` it advances under**. They read the **working** state (so successive mints in one composite each see the prior mint), check only *structural* preconditions, and never touch ownership policy.

```rust
impl M3State {
    /// Next content address under d: namespace (b_C(d), 1), element field [s_C, m+1]. [M5: INSERT]
    pub fn mint_content(&self, home: &Address)    -> Result<(Address, M3Rec, LockKey), MintError>;
    /// Next link address under d: namespace (b_L(d), 1), element field [s_L, m+1]. [M7: MAKELINK]
    pub fn mint_link(&self, home: &Address)        -> Result<(Address, M3Rec, LockKey), MintError>;
    /// Next version identity: namespace (source, 1) — the version chain, kept SEPARATE
    /// from the document chain below (ASN-0123). [M5: owned CREATENEWVERSION]
    pub fn mint_version(&self, source: &Address)   -> Result<(Address, M3Rec, LockKey), MintError>;
    /// Next document identity under an account: namespace (account, 2).
    /// [CREATENEWDOCUMENT; cross-owner VERSION; fork]
    pub fn mint_document(&self, account: &Address) -> Result<(Address, M3Rec, LockKey), MintError>;

    // Each mint returns its LockKey by CALLING the matching `*_lock_key` constructor below — one
    // code path, so the lock key M5/M7 pass to transact and the frontier key the mint advances are
    // byte-identical BY CONSTRUCTION (a divergence would under-serialize a namespace and REUSE an
    // address — the one fatal error). Both the constructor and the frontier route through the
    // private `*_ns` helper (→ the TRUE NsKey: parent = b_C(d)/b_L(d)/source/account) and the
    // injective, space-tagged `ns_lock_key` encoding (§1). So the three g=1 chains that can sit
    // under ONE document — content (b_C(d),1), link (b_L(d),1), version (d,1) — never share a key,
    // and M5/M7 never reconstruct an anchor. (A bare `(home_doc, g)` cannot tell them apart.) The
    // constructors below are called BEFORE the closure for transact's `keys` arg (M2 holds keys for
    // the txn's duration); the mint returns the identical bytes inside the closure.

    /// Namespace LockKey for transact's `keys` arg (call before the closure; mirrors the mint).
    pub fn content_lock_key(home: &Address)      -> LockKey;   // ns_lock_key(content_ns(home))   = (b_C(home), 1)
    pub fn link_lock_key(home: &Address)         -> LockKey;   // ns_lock_key(link_ns(home))      = (b_L(home), 1)
    pub fn version_lock_key(source: &Address)    -> LockKey;   // ns_lock_key(version_ns(source))  = (source, 1)
    pub fn document_lock_key(account: &Address)  -> LockKey;   // ns_lock_key(document_ns(account))= (account, 2)
    /// The single principal-registry key — held ADDITIONALLY by every op that authorizes or
    /// branches on ω (create_new_document, delegate, M5 cross-owner VERSION) so a concurrent
    /// delegation can't change ω(account) between a stale read and commit (O8). Redundant
    /// under M2 v1's global applier lock; required once per-key concurrency lands.
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
impl Namespace { // holds Arc<Kernel<W>>
    /// Baptize a fresh empty document under `account`. Authorization is by EFFECTIVE owner
    /// (ω), not bare containment. Registers d in the entity set; does NOT write M5's
    /// arrangement (lazy). Returns only after commit (commit-before-acknowledge). [ASN-0103]
    pub fn create_new_document(&self, caller: PrincipalId, account: &Address)
        -> Result<Address, TxnError<OpError>>;

    /// Delegation: the O15 five-condition gate PLUS P8 (parent registered) PLUS next-form,
    /// then baptize the new account prefix AND register the principal in ONE transaction. [ASN-0042]
    pub fn delegate(&self, delegator: PrincipalId, new_prefix: Tumbler, new_id: PrincipalId)
        -> Result<Address, TxnError<DelegateError>>;

    /// Admit an externally-originated node (NodeBaptism: validate freshness + n₀-lineage;
    /// the ADDRESS is chosen by provisioning, not minted here). [ASN-0047]
    pub fn register_node(&self, addr: Tumbler) -> Result<Address, TxnError<NodeError>>;

    /// Denial-as-fork, allocation half (O10, account-tier case): a fresh document in the
    /// caller's OWN account. Resolves pfx(caller) via `principal_prefix` (unknown id → NotOwner).
    /// Account-tier caller only — a node-tier caller gets NotAnAccount; the node-tier O10 case is
    /// DROPPED, not relocated to `delegate` (see Conflicts resolved §6). Reduces to
    /// create_new_document(caller, pfx(caller)); M5 wires the shared content.
    pub fn fork(&self, caller: PrincipalId) -> Result<Address, TxnError<OpError>>;
}
```

### C. Queries — *pure methods* (read off any M2 `Snapshot`; write nothing)

```rust
impl M3State {
    pub fn is_allocated(&self, a: &Address) -> bool;            // any namespace incl. content/link
    pub fn entity_level(&self, a: &Address) -> Option<Level>;   // Some iff registered entity (zeros ≤ 2)
    pub fn is_registered_document(&self, d: &Address) -> bool;  // == entity_level == Some(Document)
    pub fn effective_owner(&self, a: &Address) -> Option<Principal>;  // ω(a), longest-prefix match; a pure
                                                                     // prefix query over Π — valid even when
                                                                     // a is not (yet) allocated
    /// Resolve a principal by its opaque id. O(|Π|) scan over `principals.values()` — Π is
    /// account/node-tier only (O1a), hence small per node. `principal_prefix` is the pfx(id)
    /// projection the id-centric ops (fork, delegate) and the M5→M3 cross-owner-VERSION seam
    /// need, since `principals` is keyed by PREFIX, not id (so this is NOT a point lookup).
    pub fn principal_by_id(&self, id: PrincipalId) -> Option<Principal>;
    pub fn principal_prefix(&self, id: PrincipalId) -> Option<Address>;   // principal_by_id(id).map(|p| p.prefix)
    pub fn owns(prefix: &Address, a: &Address) -> bool { is_prefix(prefix.tumbler(), a.tumbler()) } // O1
}
```

### D. Genesis

```rust
impl M3State { pub fn genesis() -> M3State; }   // nodes={[1]}, frontiers={}, Π={ [1] → Principal{BOOTSTRAP_PRINCIPAL,[1]} }  (Σ₀, O14)
```

## Core data model

M3's slice of M2's `WorldState`. All persistent (`im`) so each commit yields a cheap structurally-shared version — free MVCC snapshots for readers and free historical `ω_Σ` (retain old roots). **The journal is the sole authority** (M2); these three structures are the *recovered working representation*, folded by `apply`, and need no `rebuild_derived` override.

```rust
pub struct M3State {
    /// THE registry, in B1+B2 compressed form. A namespace's entire realized set
    /// {c₁..cₘ} IS the single count m — so a gap is literally unrepresentable (B1 free).
    /// Keyed by (parent, g) — which keeps the document chain (A,2) and the version chain
    /// (d,1) on SEPARATE frontiers (ASN-0123) by construction. Covers every chain:
    /// accounts, documents, versions, content, links. Values are big-ints (B9 unbounded).
    frontiers: im::HashMap<NsKey, Nat>,

    /// Node addresses (zeros = 0). Externally minted (ASN-0047 NodeBaptism — provisioning mints
    /// node addresses OUTSIDE the docuverse), so possibly non-contiguous → held explicitly, not
    /// frontier-encoded. ASN-0040 seeds roots in B₀ and otherwise baptizes only CHILDREN
    /// (baptize(p,d)); it has no node-admission mechanism, so the ongoing-admission rationale is
    /// NodeBaptism's, not ASN-0040's. Seeded {[1]}.
    nodes: im::OrdSet<Tumbler>,

    /// Principal registry Π, keyed by ownership prefix. Small (node/account tier only, O1a).
    /// Append-only with immutable prefixes (O12/O13). The ONLY authoritative ownership
    /// state — the delegation forest is recomputable (NestingByDelegation) and never stored.
    principals: im::OrdMap<Tumbler, Principal>,
}

#[derive(Clone, PartialEq, Eq, Hash)]
pub struct NsKey { parent: Tumbler, g: u8 /* 1 | 2 */ }   // == ASN-0040's namespace (p, d)

pub enum M3Rec {                                   // M3's journal deltas, folded by `apply`
    Allocate          { addr: Tumbler },           // mint: advance frontier[namespace(addr)]
    RegisterNode      { addr: Tumbler },           // external node admission
    RegisterPrincipal { prefix: Tumbler, id: PrincipalId },  // delegation's principal half
}
```

**Why these shapes.** A `HashMap` for `frontiers` because the hot operations — mint and membership — are *point* lookups on one namespace; we never iterate namespaces, so we don't pay for order. `BigUint` values are non-negotiable (B9: "each integer has no upper limit"; a fixed-width counter silently violates it). The principal map is `OrdMap` because delegation's top-down check needs a descendant *range* scan, and ordering lets a builder upgrade ω to a range walk. **Authoritative vs hint:** `frontiers`/`nodes`/`principals` are authoritative working state (the compressed allocation journal). The delegation forest, any `address → owner` ω-cache, and any `id → prefix` reverse index are *hints* — recomputable from `principals` alone — and are deliberately **not** stored.

`apply` (M3's fold) is deterministic, total, side-effect-free. A bare journal `Tumbler` must be lifted to an `Address` before `parent`/projection (M1 types those over `&Address`/`&Tumbler` respectively); minted and journaled addresses are always T4-valid, so the lift cannot fail:

```rust
fn apply(&self, r: &M3Rec) -> M3State {
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

/// Recover (parent, g, ordinal) from a minted address — pure M1. `parent` takes `&Address`, so the
/// bare `Tumbler` is `validate`-lifted first (total here — minted addresses are T4-valid); `zeros`
/// and `ordinal` take `&Tumbler`, so they read `.tumbler()` projections.
fn decompose(addr: &Tumbler) -> (Tumbler, u8, Nat) {
    let ad  = validate(addr.clone()).expect("minted addresses are T4-valid");
    let par = parent(&ad).expect("a minted address is never a 1-component node");
    let g   = if zeros(addr) == zeros(par.tumbler()) { 1 } else { 2 };
    (par.tumbler().clone(), g, ordinal(addr).clone())
}
```

One `Allocate` variant suffices for every minted address (entity, content, link) because the frontier map is uniform; the level distinction is recovered at *query* time from `zeros`. The `(parent, g)` of an `Allocate` is exactly the `NsKey` of the `LockKey` the minting op held — frontier key and lock key are the same key (pinned at the byte level in §1).

## Internal design

### 1. The frontier allocator (the heart)

For namespace `(p, g)`, ASN-0040's `next(B,p,g)` has a closed form once you store the count `m`: the chain `S(p,g)` is `c₁ = inc(p,g)`, `cₙ₊₁ = inc(cₙ,0)`, so `cₙ = p ++ [0]*(g−1) ++ [n]`. Therefore **the next address is `c_{m+1}` = `p ++ [0]*(g−1) ++ [m+1]`** — read the count, advance the trailing ordinal.

```rust
fn next_in(&self, key: &NsKey) -> Result<Address, GateViolation> {
    let m = self.frontiers.get(key).cloned().unwrap_or_else(Nat::zero);
    let parent = validate(key.parent.clone()).expect("registered parents are T4-valid"); // standing inv
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
// `Space` is the engine's SINGLE CENTRAL tag enum (M2's LockKey contract — a 1-byte space tag,
// never chosen per-store). Namespace, Principals, Nodes are three DISTINCT tags, so the three key
// spaces never alias. The byte image is what M2 Eq/Hash/Ord-s; injectivity is what guarantees
// distinct namespaces map to distinct locks (an alias would under-serialize → REUSE an address).
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
fn principals_lock_key() -> LockKey { LockKey(vec![Space::Principals as u8]) }
fn node_lock_key()       -> LockKey { LockKey(vec![Space::Nodes as u8]) }

// The four namespace helpers — the ONE code path each mint and each *_lock_key reuses:
fn content_ns (d: &Address) -> NsKey { NsKey{ parent: inc(d.tumbler(), 2), g: 1 } }            // b_C(d)=inc(d,2)
fn link_ns    (d: &Address) -> NsKey { NsKey{ parent: inc(&inc(d.tumbler(), 2), 0), g: 1 } }   // b_L(d)=inc(b_C(d),0)
fn version_ns (s: &Address) -> NsKey { NsKey{ parent: s.tumbler().clone(), g: 1 } }            // (source,1)
fn document_ns(a: &Address) -> NsKey { NsKey{ parent: a.tumbler().clone(), g: 2 } }            // (account,2)

pub fn content_lock_key (home:    &Address) -> LockKey { ns_lock_key(&content_ns(home)) }
pub fn link_lock_key    (home:    &Address) -> LockKey { ns_lock_key(&link_ns(home)) }
pub fn version_lock_key (source:  &Address) -> LockKey { ns_lock_key(&version_ns(source)) }
pub fn document_lock_key(account: &Address) -> LockKey { ns_lock_key(&document_ns(account)) }

// Every mint advances `next_in(*_ns(..))` and RETURNS `Self::*_lock_key(..)` — and since
// `*_lock_key(..) = ns_lock_key(*_ns(..))`, the staged frontier key and the held lock key are the
// SAME BYTES. The pattern, once (the other three differ only in the *_ns/*_lock_key pair and the
// structural precondition: SourceNotRegistered=Document / NotAnAccount=Account):
pub fn mint_content(&self, home: &Address) -> Result<(Address, M3Rec, LockKey), MintError> {
    if !self.is_registered_document(home) { return Err(MintError::HomeNotRegistered); }     // P6/C2
    let a = self.next_in(&content_ns(home)).map_err(MintError::Gate)?;
    Ok((a.clone(), M3Rec::Allocate{ addr: a.tumbler().clone() }, Self::content_lock_key(home)))
}
```

- **Common case** is a single `HashMap::get`, one M1 `checked_inc`, and (past the first emission) one ordinal-only `shift` — no scan. (The reference's stateless "find-max-under-prefix-and-increment" is the same answer without the cached count; caching the count *is* the O(log n)→O(1) optimization, and we cache it because we keep the registry anyway.)
- **Level-awareness** (ASN-0123, the load-bearing gotcha): we key by `(p, g)`, never by the predicate "next document under A." A document under account A lives in `(A, 2)`; a version of document d lives in `(d, 1)`. Both classify as `Document`, both have `parent == A`-or-a-document, but their namespace keys differ, so their frontiers advance independently and **never re-mint a colliding address**. This is the entire fix for ASN-0103's version/document collision and ASN-0123's VD obligation — it falls out of the key, requiring no length filter. And because the per-namespace `LockKey` is built from this very `(p, g)` key through `ns_lock_key` (above) — *not* from `(home_doc, g)` — the *lock* granularity mirrors the *frontier* granularity **byte-for-byte**: the three g=1 chains under one document (content `(b_C(d),1)`, link `(b_L(d),1)`, version `(d,1)`) receive three **distinct** locks, so same-namespace serializes (B8) while they run free of each other (B7).
- **Determinism (B2):** `next_in` is a pure function of `frontiers` — memoizable, replayable, and the natural property-test oracle.
- **Tradeoff:** the counter representation makes B1 contiguity *free* (a gap is unrepresentable) and registry size O(active namespaces) not O(addresses), at the cost of decomposition on membership (cheap — `parent`/`zeros`/`ordinal`). The alternative (explicit address set/trie) buys fast arbitrary-`t` membership but reintroduces contiguity as something to *enforce*; deferred to [Open decisions](#open-build-decisions).

### 2. The entity registry (membership without a second structure)

The entity set E is *encoded* by the entity-namespace frontiers plus the node root set — no separate `Set<Address>`. Membership is decompose-and-compare (ASN-0040 counter membership); `zeros`/`ordinal` are M1 functions over `&Tumbler`, so they read `.tumbler()`:

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

`is_allocated` is the same probe without the `zeros ≤ 2` restriction, so it answers for content/link too (the referential-integrity oracle M5 needs). Consistency is automatic: a content frontier `(b_C(d),1)` only advances if d is registered (P6 gate), and E is append-only, so a `true` answer is permanent (B0/P1). **Ghost principle:** `is_allocated` reflects *minting*, never byte-presence — a registered-empty document is a valid, addressable ghost (B3); content existence is M4's separate axis.

### 3. Content & link sub-allocators (why the frontier lives here, not in M4/M7)

`mint_content(d)`: anchor `b_C(d) = inc(d, 2) = [d.0.s_C]` (zeros(d)=2 ⇒ B6-safe), chain `(b_C(d), 1)`, emitting `[d.0.s_C.{m+1}]` with element field `[s_C, m+1]`. `mint_link(d)`: `b_L(d) = inc(b_C(d), 0) = [d.0.s_L]`, chain `(b_L(d), 1)`. The subspace identifier is the element-field's **first component** (`s_C=1`, `s_L=2`), read via M1's `subspace()` — *not* the `.0.` separator (a corpus-wide misread to guard against). `s_C ≠ s_L` is exactly what makes content and link address spaces disjoint by construction (SD/L14, T7). `mint_content`/`mint_link` each return their namespace `LockKey` (`content_lock_key(d)` / `link_lock_key(d)`), so the lock M5/M7 take is the exact `(b_C(d),1)` / `(b_L(d),1)` frontier they advance — never a coarser `(d, g)` key that could not separate content from a version chain — and **byte-identically**, because both the returned key and the advanced frontier go through the single `content_ns`/`link_ns` helper and the injective `ns_lock_key` encoding (§1).

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

The account-tier floor (O1a) is the win: we never probe document/element prefixes, so ω is O(depth) lookups, not O(addresses). **Critical discipline** (the ownership-divergence trap): a node operator's prefix *contains* every delegated account, so `owns` is true for several principals at once — only ω (longest match) arbitrates. Authorization must use ω, never bare `owns`, or the node operator falsely appears to own delegated subdomains. O2 exclusivity (exactly one ω) is a *theorem* given prefix-injectivity, which delegation's freshness check (below) enforces — no runtime uniqueness check.

**Id→prefix resolution.** `create_new_document`/`fork`/`delegate` and the M5→M3 cross-owner-VERSION seam all hold a principal as a `PrincipalId` (the id is what M10 binds to a session), but `principals` is keyed by *prefix*, so id→prefix is **not** a point lookup. `principal_by_id(id)` is an O(|Π|) scan over `principals.values()` — sound because Π is account/node-tier only (O1a), hence small per node — and `principal_prefix(id) = principal_by_id(id).map(|p| p.prefix)`. Because prefixes are immutable (O13) and principals persist (O12), the resolved prefix is value-stable regardless of which snapshot it is read from. A hot/retried caller can fold a recomputable `PrincipalId → Tumbler` reverse-index *hint* (never authoritative — `principals` is the source of truth); deferred to [Open decisions](#open-build-decisions).

- **Recovery/tradeoff:** Π is replay-recovered like everything else. ASN-0042's recommendation stands: default to a linear scan keeping the longest match (Π is small, per-node); upgrade to a radix trie only when |Π| or query rate demands ([Open decisions](#open-build-decisions)). An `address → owner` cache is a sound hint (a stale entry can only under-resolve to an ancestor, never over-claim, by monotonic refinement).

### 6. Delegation gate

`delegate` first resolves the delegator by id — `dp := principal_prefix(delegator)`, `DelegatorUnknown` if the id names no principal (the §5 `principal_by_id` scan) — then runs O15's five conditions **plus P8 plus next-form** against the snapshot, then — in **one transaction** (atomicity is the crux; M2's `transact` gives it; a two-phase baptize-then-register could half-fail) — baptizes the new account prefix (`Allocate{new_prefix}`, advancing its account-chain frontier) and registers the principal (`RegisterPrincipal`). The supplied `new_prefix` is `validate`-lifted to an `Address` first (`NotValid` otherwise — the T4-valid half of condition (v)):

```
(i)   ancestry      dp = pfx(delegator) ≺ new_prefix                       is_prefix + strict
(ii)  authorization effective_owner(new_prefix).id = delegator   (the longest existing coverer; ω is a
                                                                 pure prefix query, valid on a fresh prefix)
(iii) account-tier  zeros(new_prefix) ≤ 1                                  O1a
(iv)  top-down      no existing principal strictly under new_prefix        OrdMap range scan
(v)   fresh-valid   T4-valid(new_prefix) ∧ !is_allocated(new_prefix)       O1b prefix-injectivity
      parent-reg    entity_level(parent(new_prefix)).is_some()             P8   → ParentNotRegistered
      next-form     new_prefix == next_in(namespace(new_prefix))           O17c — MANDATORY (see below)
```

Condition (ii) reuses ω directly. **`parent-reg` (P8) is the fix for the ASN‑0040/0042-vs-ASN‑0047 conflict** ([Conflicts resolved](#conflicts-resolved) §5): B6 alone would let a node-tier delegator baptize an account under a node that was never registered — e.g. delegator π₀ at `[1]` passing every other condition for `new_prefix = [1.5.0.1]` while node `[1.5]` is *not* in `nodes`. The explicit `entity_level(parent(new_prefix)).is_some()` check (the new account's parent node — or, when delegating a sub-account, the parent account — must be a registered entity) enforces `parent(e) ∈ E`. **Next-form is MANDATORY under the counter representation**, not relaxable: the frontier stores only the count `m`, so accepting a non-next supplied prefix (e.g. setting `frontiers[(N,2)] := 5` from `[N.0.5]` while the frontier is 1) would make `is_allocated` report phantom, never-baptized entities `[N.0.2..4]` — breaking B1/B3 and the registry's correctness. Relaxing it requires switching the frontier to an explicit allocated-set ([Open decisions](#open-build-decisions)).

Delegation always produces an **account** (zeros=1: (i)+(iii) force it — internal baptism never mints a zeros=0 node; nodes arrive only via `register_node`), advancing an account-chain frontier and adding one principal; it is the *only* non-bootstrap entry for principals. `delegate`'s transact locks the new account's namespace key `namespace(new_prefix)` (to serialize the `Allocate`) **and** `principals_lock_key()` (to serialize the principal mutation against every ω-reader — §8).

### 7. CREATENEWDOCUMENT, fork, node baptism, genesis

- **`create_new_document`** locks `[document_lock_key(account), principals_lock_key()]`, checks `effective_owner(account).id == caller`, mints via `mint_document`, stages one `Allocate`, returns post-commit. It registers d and **stops** — no `M(d)=∅` write into M5. This is the deliberate divergence from ASN-0103's eager recommendation ([Conflicts resolved](#conflicts-resolved)). No idempotency key (identity is the address, ASN-0103): a retried lost-ack yields a harmless orphan empty document; exactly-once lives at M10's session layer if wanted.
- **`fork`** implements **O10 (DenialAsFork), account-tier case only**: it resolves `pfx(caller)` via `principal_prefix(caller)` (an unknown id → `OpError::NotOwner` — an unregistered caller owns nothing) and reduces to `create_new_document(caller, pfx(caller))`, minting a fresh document one structural tier below an *account-tier* caller's prefix (O10's `zeros(a')=zeros(pfx)+1` ⇒ a document, zeros=2), with M5 wiring the shared content separately (mechanism/policy split). `fork` opens no transaction of its own — the `principal_prefix` read is value-stable because prefixes are immutable (O13) — and lets `create_new_document` drive the commit (`ω(pfx(caller))=caller` by SelfOwnershipAtPrefix, so the ω-auth passes by construction). O10 itself is *not* account-scoped — it would also let a node-tier `π` mint a self-owned *account* one tier below its node prefix — but M3 scopes `fork` to the document case: a node-tier caller (whose `pfx(caller)` is a node, not an account) is rejected with the typed `OpError::NotAnAccount` (raised by `mint_document`'s `Account(account)` check, never a silent skip). That rejection is **not** "go delegate instead": delegation mints a *new* principal and moves effective ownership to it (O7), so it does not deliver O10's self-owned account under the *same* node principal — the node-tier O10 case is genuinely **dropped** (see [Conflicts resolved](#conflicts-resolved) §6). Cite **O10** here, *not* ASN‑0123 V9 — V9 governs cross-owner VERSION, a different operation.
- **`register_node`** is the provisioning seam: the address is *supplied* (NodeBaptism mints outside the docuverse), M3 only validates freshness, `Level::Node`, and bootstrap lineage `[1] ≼ addr`, then adds to `nodes`. Its transact holds `node_lock_key()` — a single coarse node-registry key: node admission needs no namespace lock for *safety* (the `OrdSet` insert is idempotent and freshness is monotone), but holding the coarse key makes a concurrent duplicate `RegisterNode` surface `NotFresh` rather than silently coalesce under per-key concurrency (redundant under M2 v1's global lock, exactly like `principals_lock_key`). This is the one validate-not-mint path (see conflict 1).
- **`genesis`** = `nodes={[1]}`, `frontiers={}`, `Π={[1] → Principal{BOOTSTRAP_PRINCIPAL,[1]}}` (Σ₀ + O14). `BOOTSTRAP_PRINCIPAL` is a fixed `PrincipalId` constant — the `effective_owner(account).id == caller` auth gate keys on it, so M10 must bind the bootstrap session to it. "Load empty journal" and "fresh genesis" are the same code path.

### 8. Durability, serialization, recovery

M3 **rides M2** — it builds no WAL of its own. Its three structures are part of `WorldState`, recovered by M2's checkpoint-load + replay; B4 atomicity (frontier advance and record durable *together*) is exactly M2's `transact` commit. The one invariant the durability protects — **never mint an address twice** — holds because the frontier only advances, `apply` is deterministic, and same-namespace commits are serialized by handing M2 the **true-namespace** `LockKey` (`content`/`link`/`version`/`document_lock_key`, each computed from the actual `NsKey` parent — *not* a `(home_doc, g)` pair, which cannot tell the three g=1 chains under a document apart). Distinct namespaces carry distinct keys, so independent owners/documents allocate concurrently (B7); only same-namespace serializes (B8/B-Seq).

**Correctness must not lean on M2 v1's global applier lock.** That lock currently masks any lock-key defect; per-key concurrency would expose a same-namespace key collision as address reuse — the one fatal error. So the lock keys mirror the frontier keys exactly, **by construction**: each `mint_*` advances `next_in(*_ns(..))` and returns `Self::*_lock_key(..)`, and `*_lock_key(..) = ns_lock_key(*_ns(..))` — one `*_ns` helper, one injective space-tagged `ns_lock_key` encoding (§1) — so the held lock key and the staged frontier key are the *same bytes*. There is no second code path to drift, and the distinct `Space::Namespace`/`Space::Principals`/`Space::Nodes` tags keep the three key spaces from aliasing each other.

Two ops additionally hold `principals_lock_key()` — `create_new_document` and `delegate` (and, by the same discipline, M5's cross-owner VERSION, which *branches* on ω): under per-key concurrency a concurrent `delegate` could otherwise change `ω(account)` between a stale-base auth/branch read and commit, slipping a now-unauthorized write past O8. Holding the one principal-registry key on both the ω-reader and every ω-mutator serializes them; it is redundant (harmless) under v1's global lock. `register_node` holds the coarse `node_lock_key()` for the analogous reason — to keep its `NotFresh` rejection under per-key concurrency, not for safety (the insert is idempotent).

The minted address is returned only after M2 commits (commit-before-acknowledge), so a crash never loses a handed-out address — over-shooting (a gap) is safe (permanent ghost), reuse is fatal, and we never reuse.

## Invariants & contracts

### By construction (fall out of the data model)
- **Permanence / irrevocability** — `frontiers`/`nodes`/`principals` only grow; there is *no* delete API. [ASN-0040 B0/B0★, ASN-0047 P1/P3, ASN-0042 O12/O13]
- **Contiguity / gap-free** — the count representation makes a gap unrepresentable. [ASN-0040 B1]
- **Determinism & finiteness** — `next_in` is a pure function of the frontier; growth is one-at-a-time. [ASN-0040 B2/B_fin]
- **Unbounded extent** — `Nat = BigUint` for every ordinal and count. [ASN-0040 B9]
- **T4-validity of every minted address** — valid parents + `checked_inc`. [ASN-0040 B10, ASN-0093 StoreT4Validity]
- **Cross-namespace uniqueness; document↔version separation; content↔link disjointness** — distinct `(p,g)` keys, `s_C ≠ s_L`. [ASN-0040 B7/B8-cross, ASN-0093 SD/Cross-doc, ASN-0123 V0/VD, ASN-0034 T10]
- **Content-independence (ghosts)** — registry is M3, content is M4; allocated ≠ has-bytes. [ASN-0040 B3]
- **Ownership exclusivity, refinement, node-locality** — longest-prefix match over an append-only immutable-prefix Π. [ASN-0042 O2/O3/O8/O9]

### By active enforcement (M3 must guard)
- **Same-namespace uniqueness** — serialize commits per namespace via the **true-namespace** `LockKey` (`content`/`link`/`version`/`document_lock_key`, computed from the actual `NsKey` parent through the injective, space-tagged `ns_lock_key` encoding — one code path shared with the frontier, so the lock key ≡ the frontier key byte-for-byte; never a `(home_doc, g)` pair) to M2. [ASN-0040 B8/B-Seq] → *the allocator + M2 transact, §1/§8*
- **Atomicity (frontier advance + record durable together)** — M2's `transact`/commit marker. [ASN-0040 B4]
- **Parent/origin registered (P8/P6/C2/L1a)** — `entity_level`/`is_registered_document` before minting (`mint_document`/`mint_version`/`mint_content`/`mint_link`) *and* `entity_level(parent(new_prefix))` in `delegate` (P8 for delegated accounts — [Conflicts resolved](#conflicts-resolved) §5). [ASN-0047 P8/P6, ASN-0093 C2/L1a] → *§4, §6*
- **Prefix-injectivity & account-floor** — delegation (v) freshness + (iii) tier. [ASN-0042 O1b/O1a]
- **Delegation gate (5 conditions + P8 + next-form)** — `delegate`. [ASN-0042 O15] → *§6*
- **Authorization by ω (never bare `owns`)** — `create_new_document`/`fork`/`delegate`. [ASN-0042 O5, ownership-divergence] → *§5/§7*
- **Node freshness + bootstrap lineage** — `register_node`. [ASN-0047 NodeBaptism] → *§7*
- **Commit-before-return** — address returned only post-commit. [ASN-0040 finality, ASN-0103 commit point]

## Dependencies & seams

**Upstream — M1 (calls):** `checked_inc`/`inc_preserves_t4` (B6 gate on every mint), `inc` (anchors `b_C = inc(d,2)`/`b_L`), `shift` (ordinal-only — mints `cₘ₊₁` from the gated `c₁`, §1), `parent`/`zeros`/`ordinal`/`document_of` (decomposition & membership — `zeros`/`ordinal` over `&Tumbler`, `parent`/`document_of` over `&Address`, so call sites project via `.tumbler()`/`validate`), `classify`/`Level`/field projections (entity-level + acct/node prefixes for ω), `is_prefix`/`validate`, `subspace` (content vs link). M3 holds **no** address algebra of its own.

**Upstream — M2 (calls):** `transact(&[<namespace LockKey>], …)` — the namespace key from `content`/`link`/`version`/`document_lock_key` (plus `principals_lock_key()` for the ω-authorizing/branching ops and `node_lock_key()` for `register_node`, §8) — for every mutating op (atomic + serialized + durable); `snapshot()` for query reads; M3 implements its slice of `WorldState::apply` (and the default `rebuild_derived`). M3 stages `M3Rec`; M2 owns ordering/durability/recovery. The 1-byte space tags (`Space::Namespace`/`Principals`/`Nodes`) are drawn from the engine's single central `Space` enum (M2's `LockKey` contract).

**Downstream seams M3 exposes (build neighbors against these):**
- **M5 → M3:** `is_registered_document(d)` (edit precondition); `effective_owner(d_src)` (CREATENEWVERSION's owned-vs-cross-owner branch — ASN‑0123 V8/V9: owned ⇒ `mint_version` on `(d_src,1)`; cross-owner ⇒ `principal_prefix(forker_id)` → the forker's account-tier prefix `pfx(π)`, then `mint_document(pfx(π))` on `(pfx(π),2)` — M5 holds the forker as a `PrincipalId`, consistent with M3's id-centric ops, and `principal_prefix` is the §5 id→prefix query); the *pure* mints — `mint_content` (INSERT), `mint_version`/`mint_document` (VERSION) — each returning the namespace `LockKey` it advances (M5 takes that key from the matching `*_lock_key` constructor for transact's `keys` arg *before* the closure); `is_allocated(a)` (content-side referential-integrity oracle for COPY transclusion — COPY mints no content, it only checks this). M5 never reads M4 for this — allocation status is M3's. (Cross-owner VERSION branches on ω, so it also holds `principals_lock_key()` under per-key concurrency — §8.)
- **M7 → M3:** `mint_link` *pure* (inside MAKELINK, returning the link namespace `LockKey`; M7 locks via `link_lock_key(d)`); `is_registered_document(d)` (link's home).
- **M6, M8 → M3:** `is_registered_document(d)` — they convert *registered-but-no-arrangement* → ⟨⟩ and *unregistered* → fail. M3 supplies the bool; the ⟨⟩-vs-fail *query semantics* are theirs.
- **M9 → M3:** `effective_owner`/`is_registered_document` (residence resolution); pred-def content is allocated indirectly via M5's composite (M9→M5→M3).
- **M10 → M3:** dispatches `create_new_document`/`delegate`/`register_node`/`fork`; binds the bootstrap session to `BOOTSTRAP_PRINCIPAL`; may resolve a bound session's prefix via `principal_prefix` for echo/validation (same prefix-keyed registry, so M10 reuses the §5 query rather than re-deriving it).

## Conflicts resolved

1. **Mint vs validate document addresses (ASN-0093 K.σ vs ASN-0047 K.δ / ASN-0103).** ASN-0093's `K.σ` *validates* a caller-supplied document address; ASN-0047/0103 *mint* it. ASN-0093 itself defers "document-address origination to the entity-allocation layer" — **which is M3**. Resolution: M3 **mints** accounts/documents/versions/content/links via the frontier; the validate-not-mint path survives only for **nodes** (NodeBaptism originates them externally, M3 validates).

2. **"Recompute the cursor from the store" (ASN-0093/0047) vs the module DAG.** Those notes treat C/L/registry as one substrate and recompute the frontier from `dom(C)`/`dom(L)`. Our split forbids `M3 → M4/M7`, so M3 cannot read those stores. Resolution: **M3 owns and persists the frontier for all chains, including content/link**, advanced by `Allocate` records that M5/M7 co-stage with their value-writes in one M2 composite. Same Lampson hint discipline (recomputable by replay), different source-of-truth boundary (M3's own allocation journal, not M4/M7).

3. **Eager `M(d)=∅` (ASN-0103) vs lazy arrangement (decomposition).** ASN-0103 recommends writing the empty arrangement at creation — which would write M5 from M3 and close an `M3 → M5` cycle. Resolution: `create_new_document` **registers d only**; the arrangement is implicit/lazy in M5. M6/M8 read *registered-with-no-arrangement* as ⟨⟩. The DAG stays acyclic (`M5 → M3` only).

4. **`owns` (containment) vs `ω` (longest-match) for authorization.** ASN-0103's literal `pfx(π) ≼ A` precondition is bare containment, but in the multi-tier model a node operator contains delegated accounts. Resolution: every authorization gate uses **`ω`** (the delegate, not the ancestor), per O5 and the ownership-divergence finding.

5. **Baptism under an unbaptized parent (ASN‑0040/0042) vs P8 (ASN‑0047).** B6 (ValidDepth) does *not* require the parent `p ∈ B`, so ASN‑0040/0042's delegation would let a node-tier delegator baptize an account under a node that was never registered. ASN‑0047 P8 forbids it (`parent(e) ∈ E` for every non-node entity), and this design commits to P8 (it lists P8 under active enforcement). Resolution: **P8 wins for delegated accounts** — `delegate` adds the `entity_level(parent(new_prefix)).is_some()` gate (`ParentNotRegistered` otherwise). `mint_document`/`mint_version` already discharged P8 via their `entity_level` checks; `delegate` was the one account-minting path that skipped it.

6. **O10 node-tier fork (ASN‑0042 O10) vs the account ≡ principal model.** O10 (DenialAsFork) lets *any* principal fork a self-owned address one structural tier below its prefix — including a **node-tier** principal minting a self-owned *account* (zeros=1) with **no** new principal. M3 deliberately scopes `fork` to the **account-tier** case only: a fork mints a *document* (zeros=2) under an account-tier caller's prefix. This makes M3 treat an account-tier prefix as the unit of principal identity — coherent with, and assumed by, `create_new_document`'s ω-authorization (the authorizing principal sits at an account, and `fork` relies on `ω(pfx(caller))=caller`). **Resolution / consequence:** the node-tier O10 case is **dropped, not relocated.** A node-tier caller is rejected `NotAnAccount`; this is *not* silently equivalent to "delegate an account first," because `delegate` mints a **new** principal and moves effective ownership to it (O7), whereas O10's node-tier fork would leave the new account owned by the *same* node principal. We accept the narrowing — in the multi-tier model an account is the natural home of a principal, and a node operator provisioning accounts *via delegation* (new principals) is the intended path — and flag re-admitting node-tier `fork` under [Open decisions](#open-build-decisions).

## Open build decisions

- **Frontier representation:** counter map (recommended; B1 free) vs. explicit allocated-set/trie (fast arbitrary-`t` membership, contiguity becomes enforced — **and the only representation under which a gap-creating supplied delegate-prefix is admissible**; see Delegate-prefix policy) vs. hierarchical tree (only if subtree/range queries are needed elsewhere).
- **ω resolver structure & caching:** linear scan over Π (default, ASN-0042) vs. `OrdMap` descending range-walk vs. radix/PATRICIA trie — sized to |Π| and query rate; plus an optional `address → owner` hint cache.
- **Id→prefix resolution:** default O(|Π|) `principal_by_id` scan over `principals` (Π small, O1a); fold a recomputable `im::HashMap<PrincipalId, Tumbler>` reverse-index *hint* (and maintain it in `apply` alongside `RegisterPrincipal`) only if id-keyed lookups get hot — never authoritative, `principals` stays the source of truth.
- **Delegate-prefix policy** (under the counter rep, next-form is *mandatory* — §6; the open choice is *who picks the address*, not whether to check it): (a) keep `delegate(new_prefix)` and *validate* the supplied prefix is next-form (current design, O17c-faithful); or (b) drop `new_prefix` from the signature and have `delegate` *mint* the next account slot (next-by-construction, no check) — Green-faithful, but the caller no longer names the prefix. Admitting an *arbitrary* (gap-creating) supplied prefix is unsound here — it writes phantom entities into the count-compressed registry — and would require switching the frontier to an explicit allocated-set; reaching a chosen non-next prefix under the counter rep instead means baptizing the intervening slots (filling the gap, at the cost of extra allocations).
- **Node-tier `fork` (O10):** dropped today ([Conflicts resolved](#conflicts-resolved) §6); re-admit a node-principal forking a *self-owned* account (no new principal, ownership stays at the node) only if that provisioning path is needed — it requires a node-tier "mint a self-owned account" branch distinct from `delegate`, which moves ownership to a new principal.
- **Serialization granularity:** the per-namespace `LockKey` (recommended — concurrency by B7) vs. a single global writer. **Resolved default:** `create_new_document`/`delegate` (and any ω-branching composite, incl. M5's cross-owner VERSION) additionally hold `principals_lock_key()`, so a concurrent delegation cannot change `ω(account)` between a stale-base read and commit (O8); `register_node` holds `node_lock_key()` to preserve `NotFresh`; both harmless-redundant under v1's global lock. The remaining open question is only their *granularity* — one global principal key (safe, coarse) vs. a finer per-account-subtree key.
- **Record delegator identity vs. recompute the forest** (NestingByDelegation): recompute suffices while refinement stays monotonic (no ownership transfer); store it only if transfer is later introduced.
- **Node tracking:** explicit `OrdSet` for all nodes (recommended — tolerates non-contiguous external minting) vs. a node-frontier if provisioning guarantees contiguity.
- **`PrincipalId` shape & session binding:** opaque here; the session→principal binding and idempotency/exactly-once for retried `create_new_document` live at M10.
