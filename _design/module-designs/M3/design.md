## Purpose & boundary

M3 owns the authoritative permanent name/entity space. It mints fresh, globally-unique, T4-valid addresses under a **gap-free monotone frontier** discipline that is *level-aware* (a document's chain under its account and a version's chain under its source document advance on separate frontiers and can never re-mint a colliding address); it records organizational existence in an **append-only entity registry** `E` (nodes, accounts, documents/versions); and it resolves authority by prefix — the stateless containment predicate `owns` and the longest-prefix **effective-owner** resolver `ω` over the **principal registry** `Π`. **One thing well: be the single source of truth for what organizational names exist, who may mint the next one, and who owns any address.**

It does *not*: store content or link bytes (M4/M7 — M3 lends only the pure frontier *arithmetic*, since `M3 → M4`/`M3 → M7` edges do not exist); materialize a document's arrangement `M(d)` (M5 — left lazy; M3 registers existence only, **diverging from ASN-0103's eager `M(d)=∅`** to avoid an `M3 → M5` cycle); own durability, journaling, the linearization counter, or recovery (M2 — M3 persists `E`/`Π` and commits each baptism *through* M2); or own the request lifecycle / typed-rejection surfacing to clients (M10). The frontier is **recomputed from the authoritative store, never held as a counter** (ASN-0040/0093/0123); there is no global allocation counter anywhere.

## Public interface

`Tumbler`, `Address`, `Level`, `Class`, `is_prefix`, `inc`, `inc_preserves_t4`, `classify`, field projections, `shift`, `subtree_of` are M1's. `Kernel<W>`, `Snapshot`, `Seq`, `LockKey`, `transact`, `WorldState` are M2's. M3 is generic over an engine `World` that carries M3's slice:

```rust
/// Engine-side accessor + record-wrapper (keeps M3 decoupled from W's full shape — the same
/// pattern M2 mandates for composable stores). The engine impls this for its `World`.
pub trait NamespaceWorld: WorldState {
    fn ns(&self) -> &Namespace;
    fn wrap(r: NsRecord) -> Self::Record;   // embed M3's record in the engine's Record enum
}
```

### A. Authority queries (no transaction)

```rust
/// O1 containment — PURE, STATELESS, no registry read; safe to push to the edge / any layer.
/// NOT an authorization decision on its own (see effective_owner / the §3 divergence note).
pub fn owns(principal_prefix: &Tumbler, a: &Tumbler) -> bool;   // = M1::is_prefix(prefix, a)

/// ω(a): the longest registered principal prefix that covers `a` (O2 exclusivity). The ONE
/// authority query that consults Π. None only if no principal covers `a` (uncovered ⇒ O4 says
/// unreachable for any registered a). This — never `owns` — arbitrates writes (§3).
pub fn effective_owner(ns: &Namespace, a: &Tumbler) -> Option<Tumbler>;

pub fn is_registered(ns: &Namespace, a: &Tumbler) -> bool;      // a ∈ E (ghost-tolerant: B3)
pub fn is_document(ns: &Namespace, d: &Tumbler) -> bool;        // d ∈ E ∧ classify(d)=Document
```

### B. Organizational allocation (M3-owned transactions)

Each returns the minted `Address` and the committed `Seq`; each commits exactly one record under one M2 transaction (atomic baptism, B4). `caller` is the acting principal's prefix, supplied by M10's session.

```rust
/// Admit an externally-minted node (NodeBaptism boundary; M3 mints no nodes). Registers it as
/// a node-principal. Gate: Node(n) ∧ n ∉ E ∧ n₀ ≼ n.
pub fn register_node<W: NamespaceWorld>(k: &Kernel<W>, n: Tumbler) -> Result<Seq, NsError>;

/// Delegation == account creation (ASN-0042 O18: a delegation IS a baptism). Mints the next
/// account at the frontier under a node-principal and registers it as a principal — one atomic
/// baptize+register. Gate: caller ∈ Π ∧ Node(caller) (tier floor O1a forces node→account).
pub fn create_account<W: NamespaceWorld>(k: &Kernel<W>, caller: &Tumbler)
    -> Result<(Address, Seq), NsError>;

/// CREATENEWDOCUMENT (ASN-0103). Mints the next DOCUMENT under `account` (level-aware: the
/// version chain is excluded — §Internal 1). Does NOT materialize M(d) (left lazy in M5).
/// Gate: Account(account) ∧ account ∈ E ∧ effective_owner(account) == Some(caller)  ← ω, not owns (§7).
pub fn create_document<W: NamespaceWorld>(k: &Kernel<W>, caller: &Tumbler, account: &Tumbler)
    -> Result<(Address, Seq), NsError>;

/// DenialAsFork (O10) / explicit fork: a fresh document under the caller's OWN account.
/// Allocation only — the content-sharing half is M5's COPY. (≡ create_document(caller, caller)
/// when caller is account-tier; O5 holds by construction.)
pub fn fork_address<W: NamespaceWorld>(k: &Kernel<W>, caller: &Tumbler)
    -> Result<(Address, Seq), NsError>;
```

### C. Pure composable surface (folded by neighbors — M2 contract 3)

Published up front so M5/M7/M9 fold them into *their* transaction closures (never as a nested `transact`).

```rust
/// THE allocator. Next address in sibling stream S(p,g) over ANY ordered address set
/// (E, dom(C), dom(L)). g ∈ {1,2}. Gap-free, monotone, level-aware, T4-by-construction.
/// Truncate-then-increment (§Internal 1). PRECONDITION: inc_preserves_t4(p, g) — discharge it
/// at the call site (the typed ops in B do; content/link anchors are gate-safe by construction).
pub fn next_in_namespace<S: AddressSet>(addrs: &S, p: &Tumbler, g: usize) -> Tumbler;

pub fn content_anchor(d: &Tumbler) -> Tumbler;   // b_C(d) = inc(d,2)        — gate-safe (zeros(d)=2)
pub fn link_anchor(d: &Tumbler) -> Tumbler;      // b_L(d) = inc(b_C(d),0)
// ⇒ next content addr under d = next_in_namespace(&dom_C, &content_anchor(d), 1)
//   next link    addr under d = next_in_namespace(&dom_L, &link_anchor(d),    1)

/// Version identity (ASN-0123 allocator obligation). Owned in-place fork vs account-tier
/// cross-owner fork; node-tier non-owner is out of domain (P-tier). M5's VERSION composite calls
/// this, then stages NsRecord::Register{v} (this variant) + its own arrangement/provenance records.
pub fn version_identity(ns: &Namespace, d_src: &Tumbler, forker: &Tumbler)
    -> Result<Tumbler, NsError>;

/// The serialization-key seam M2 keys composites on (1-byte central-enum SpaceTag + bytes).
pub fn ns_key(home: &Tumbler, discriminant: u8) -> LockKey;
```

### D. Registry reads & genesis

```rust
/// Owned versions of d = address range scan of E ∩ S(d,1), gap-free (VN-B1) so enumeration
/// terminates at the first absentee. CROSS-OWNER versions are severed from the address space
/// (V9) and are NOT returned here — that discovery is provenance-based (M5/M6), not M3's.
pub fn versions_of<'a>(ns: &'a Namespace, d: &Tumbler) -> impl Iterator<Item = Tumbler> + 'a;
pub fn documents_under<'a>(ns: &'a Namespace, account: &Tumbler) -> impl Iterator<Item=Tumbler> + 'a;

pub fn genesis() -> Namespace;   // E₀ = {[1]}, Π₀ = {[1]}  (Σ₀; O14; n₀ baptized at genesis)
```

### E. Records & errors

```rust
pub enum NsRecord {
    Register { addr: Tumbler },           // E ∪ {addr}             — document / version / fork (zeros=2)
    RegisterPrincipal { prefix: Tumbler },// E ∪ {prefix}, Π ∪ {prefix} — node / account (zeros ≤ 1)
}
pub enum NsError {                         // surfaced verbatim by M10 as typed rejections (never silent)
    NotRegistered(Tumbler),                // P8 / target absent (account, d_src)
    NotAuthorized,                         // ω / owns check failed — the divergence guard (§3, §7)
    WrongTier { addr: Tumbler, want: Level },// not Account / not Node / delegate prefix zeros > 1 (O1a)
    BadLineage(Tumbler),                   // n₀ ⋠ n (NodeBaptism b)
    AlreadyRegistered(Tumbler),            // freshness (v) — unreachable for frontier mints
    GateViolation,                         // inc_preserves_t4(p,g) = false (B6/TA5a)
    VersionOutOfDomain,                    // node-tier non-owner forking (P-tier)
}
```

## Core data model

M3's authoritative state is two **append-only persistent sets**, folded from the journal by `apply` and serialized into M2 checkpoints. Both are non-recomputable from any other store (a ghost document, an empty account, a node leave no trace in C/L/M/R — B3 content-independence), so neither is a hint.

```rust
pub struct Namespace {
    pub entities:   im::OrdSet<Tumbler>,   // E  — nodes(zeros=0)/accounts(zeros=1)/docs+versions(zeros=2)
    pub principals: im::OrdSet<Tumbler>,   // Π  — principal prefixes (zeros ≤ 1); Π ⊆ E by construction
}
```

- **`im::OrdSet<Tumbler>`** (M1's `Ord`) is the load-bearing choice. Ordering buys, in *one* structure: O(log n) membership (`is_registered`); the predecessor/max-under-prefix query the frontier needs; prefix-range scans for `versions_of`/`documents_under` (T5 contiguity) and for ω's reverse direction; and cheap structurally-shared snapshots — each baptism is a new `OrdSet` sharing the old, so every `Σ` is a cheap immutable value (MVCC-style consistent reads while a writer advances a namespace). This is exactly the granfilade shape ASN-0093 recommends, and matches M2's persistent-map substrate.
- **Principal identity *is* its prefix.** `pfx` is injective and immutable (O1b/O13), so `Tumbler` is the principal id; the kind (Node/Account) is `classify`-derivable and the delegation parent is recomputable as the most-specific coverer (NestingByDelegation) — none of it is authoritative, so `Π` is a bare `OrdSet`, not a record map. `Π ⊆ E` (PrefixBaptismCoupling) falls out of `RegisterPrincipal` adding to both.

**Authoritative vs hint.** `E` and `Π` are authoritative. There is **no stored frontier** — it is recomputed from `E`/`dom(C)`/`dom(L)` on every mint (ASN-0093 "the cursor is a hint, not authoritative state"; ASN-0040 "no session-local counter"). Two *optional* hints (default off, §Open decisions): a per-`(home,g)` next-address cache, and an `address → owner` ω cache — both recomputable, maintained in `apply` and seeded by `rebuild_derived` only if added. With neither, M3's `rebuild_derived` is the identity and recovery is pure M2 replay.

```rust
/// The minimal ordered-set capability the allocator needs, so next_in_namespace works
/// uniformly over E (OrdSet) and M4/M7's stores (OrdMap keys) without M3 knowing W's shape.
pub trait AddressSet {
    fn max_with_prefix(&self, p: &Tumbler) -> Option<Tumbler>; // lex-greatest e with p ≼ e
    fn contains_addr(&self, a: &Tumbler) -> bool;
}
// impl AddressSet for im::OrdSet<Tumbler>            { max_with_prefix = range(p..subtree_of(p).reach()).next_back() }
// impl<V> AddressSet for im::OrdMap<Tumbler, V>      { … over keys … }
```

## Internal design

### 1. The frontier allocator — `next_in_namespace` (the centerpiece)

ASN-0040/0093/0123 all reduce allocation to `next(addrs, p, g)`: the first absentee of the sibling stream `S(p,g)`. The mechanism is **truncate-then-increment** over a single max-under-prefix query — robust precisely because it tolerates a *deeper* address (a version) being the lexical maximum, normalizing it back to the target level before stepping (udanax-green's verified method; ASN-0103 prefers it over a bare level filter exactly to kill that bug class).

```rust
pub fn next_in_namespace<S: AddressSet>(addrs: &S, p: &Tumbler, g: usize) -> Tumbler {
    let first   = inc(p, g);                       // first emission: inc(p,1)=p·k₁ or inc(p,2)=p·0·1
    let sib_len = first.len();                      // every sibling of S(p,g) has exactly this length
    let sib_pfx = truncate(&first, sib_len - 1);    // common prefix: p (g=1) or p·0 (g=2)
    match addrs.max_with_prefix(&sib_pfx) {
        None                              => first,                       // empty stream
        Some(m) if m.len() < sib_len      => first,                       // only the parent present (g=1)
        Some(m) => inc(&truncate(&m, sib_len), 0),  // truncate a deeper descendant to sibling level, advance
    }
}
```

`max_with_prefix(p)` is `range(p .. M1::subtree_of(p).reach())` then `.next_back()` — O(log n), exploiting T5 (a prefix's subtree is the contiguous interval `[p, shift(p,1))`).

**Level-awareness (the ASN-0123 obligation), worked.** A document under account `A=[1,0,1]` is `S(A,2)`; a version of `d₁=[1,0,1,0,1]` is `S(d₁,1)`. Both satisfy `Document(·)`; the naïve "max document under A, +1" collides because a version `[1,0,1,0,1,1]` is `Document`-class with `parent = A`. The truncate isolates the frontiers:

| `E` contains | `create_document(A)` → `next(E, [1,0,1], 2)` | `version(d₁)` → `next(E, [1,0,1,0,1], 1)` |
|---|---|---|
| `{[1,0,1,0,1], [1,0,1,0,2], [1,0,1,0,1,1]}` | max-under-`[1,0,1,0]` = `[1,0,1,0,2]` → trunc(·,5) → inc(·,0) = **`[1,0,1,0,3]`** | max-under-`[1,0,1,0,1]` = `[1,0,1,0,1,1]` → trunc(·,6) → inc(·,0) = **`[1,0,1,0,1,2]`** |

The document frontier *steps past* the version `[1,0,1,0,1,1]` (it never re-mints `[1,0,1,0,3]`'s slot for a version), and the two chains advance independently — V0/V5/VN-B1 hold. **Common-case cost:** one O(log n) range query + one carry-free `inc` (M1: `inc` touches one component). **Gate:** the typed ops in §B check `inc_preserves_t4(p, g)` before calling (B6/TA5a — the producer obligation M1 hands M3); content/link anchors are gate-safe by construction (`inc(d,2)` needs `zeros(d)≤2`, true for any document; the `g=1` chain off a `zeros=3` anchor always preserves T4).

### 2. Entity registry & the typed organizational ops

Every organizational allocation is one pipeline inside one `transact`:

```rust
pub fn create_document<W: NamespaceWorld>(k, caller, account) -> Result<(Address, Seq), NsError> {
    let (addr, seq) = k.transact(&[ns_key(account, 2)], |stg| {
        let ns = stg.working().ns();                                   // base == working (one record)
        if classify(account) != Class::Account        { return Err(NsError::WrongTier{..}); }
        if !ns.entities.contains(account)              { return Err(NsError::NotRegistered(account.clone())); } // P8
        if ns.effective_owner_eq(account, caller)==false { return Err(NsError::NotAuthorized); }                // O5/ω — §7
        if !inc_preserves_t4(account_as_address, 2)    { return Err(NsError::GateViolation); }                  // B6
        let d = next_in_namespace(&ns.entities, account, 2);           // level-aware document frontier
        stg.push(W::wrap(NsRecord::Register { addr: d.clone() }));     // single atomic baptism (B4)
        Ok(validate(d)?)                                              // T4-classified Address
    })?;
    Ok((addr, seq))
}
```

`apply` arms (M3's, dispatched by the engine's `WorldState::apply`):

```rust
impl Namespace {
    pub fn apply_ns(&self, r: &NsRecord) -> Namespace { match r {
        NsRecord::Register{addr}            => Namespace{ entities: self.entities.update(addr.clone()), ..self.clone() },
        NsRecord::RegisterPrincipal{prefix} => Namespace{ entities:   self.entities.update(prefix.clone()),
                                                          principals: self.principals.update(prefix.clone()) },
    }}
}
```

**Permanence is structural:** there is no delete/overwrite arm, so B0/P1/O12 hold by construction (the append-only journal + this `apply` enforce it). **Atomicity (B4):** one record under one `transact` — M2 commits it durably-before-visibly; a torn baptism never becomes visible and never replays (M2 §1/§7). **Same-namespace uniqueness (B8):** the only uniqueness *not* free — `ns_key(parent, mode)` serializes same-namespace mints through M2's keyed critical section (under M2 v1's single applier this is subsumed by the global lock; the key remains the documented seam). **Recovery:** none of M3's own — `E`/`Π` are rebuilt by M2 replaying `Register`/`RegisterPrincipal` into the `OrdSet`s; the frontier, being recomputed, has nothing to recover.

`register_node` / `create_account` differ only in their gate (lineage `n₀ ≼ n` and `Node(n)` for the former; `caller ∈ Π ∧ Node(caller)` for the latter) and in staging `RegisterPrincipal` (both create principals).

### 3. Ownership resolution

`owns(prefix, a)` is M1's `is_prefix` — pure, stateless, edge-pushable. `ω(a) = effective_owner` is the **longest-prefix match** over `Π`, the one resolver that consults state. Because the account tier is the ownership floor (`zeros(pfx(π)) ≤ 1`, O1a) and delegation is always node→account (the tier floor makes account→account ancestry impossible), the *only* candidate covering prefixes of any `a` are its **account prefix** (`zeros=1`) and its **node-field prefixes** (`zeros=0`). So ω is an **ancestor-walk longest-first**, bounded by `1 + #N(a)` set lookups — effectively O(1):

```rust
pub fn effective_owner(ns, a) -> Option<Tumbler> {
    let acct = account_prefix(a);                       // N·0·U  (M1 node_field ++ [0] ++ account_field)
    if let Some(acct) = acct { if ns.principals.contains_addr(&acct) { return Some(acct); } } // longest possible
    for node_pfx in node_field_truncations(a).rev() {   // [1,5,3], [1,5], [1] — longest node first
        if ns.principals.contains_addr(&node_pfx) { return Some(node_pfx); }
    }
    None                                                // uncovered ⇒ O4 unreachable for registered a
}
```

**This is the divergence guard.** Using *containment* (`owns`) where the contract means *exclusive ownership* (`ω`) is the known bug: a node operator `[1]` contains every delegated account `[1,0,5]`, so `owns([1], [1,0,5,…])` is `true` and a containment-based authorizer hands the node operator write access to delegated accounts — violating O2/O3/O8. The ancestor-walk returns the **account** (longest) over the **node**, so authorizing on `ω(target) == caller` (never on `owns`) refuses that — the node operator does *not* own a delegated account. Default to this walk; the radix-trie / linear-scan / `address→owner` cache are sized-up alternatives (§Open decisions). ω's exclusivity (O2) holds by construction given longest-match + prefix-injectivity; refinement-only / irrevocability / node-locality (O3/O8/O9) hold from append-only `Π` + immutable prefixes + prefix geometry.

### 4. Delegation = account creation

`create_account(caller)` mints `next(E, caller, 2)` under a node-principal and stages `RegisterPrincipal`. Minting **at the frontier under one's own node** discharges ASN-0042's five delegation conditions structurally: (i) ancestry `node ≺ account` ✓ (frontier extends node); (ii) authorization `caller` is the most-specific coverer ✓ (minting directly under itself into a fresh slot); (iii) tier `zeros(account)=1 ≤ 1` ✓; (iv) top-down-order ✓ (a fresh frontier slot has nothing below it); (v) fresh-valid ✓ (`next` is fresh + T4 by the gate). Restricting to the frontier slot is O17c-faithful (you cannot delegate account #5 while #1–4 are unbaptized). Atomicity (`O15` ≤ 1 principal per transition) is free — one `RegisterPrincipal` record per `transact`.

### 5. CREATENEWDOCUMENT specifics

Beyond §2: `M(d)` is **not** written — M3 only registers `d` in `E_doc` and returns it. This is the deliberate divergence from ASN-0103's `CND.empty` (`M'(d)=∅`): writing the empty arrangement would make M3 write M5's state and close an `M3 → M5` cycle. The empty arrangement is left implicit; M5 treats "`d ∈ E_doc`, no materialized arrangement" as `⟨⟩`. The coupling constraints J0/J1★ hold *vacuously* (no content/placement/provenance work — CND.atomicity), so creation is the easy member of the composite family. Immediate referability (a link may target `d` before any bytes — CND.refer) falls out of identity-by-address + B3.

### 6. Version identity & fork

```rust
pub fn version_identity(ns, d_src, forker) -> Result<Tumbler, NsError> {
    if !ns.entities.contains(d_src) || classify(d_src) != Class::Document { return Err(NotRegistered(..)); }
    match ns.effective_owner(d_src) {
        Some(o) if &o == forker => Ok(next_in_namespace(&ns.entities, d_src, 1)),     // V4 owned: S(d_src,1)
        _ if classify(forker) == Class::Account
                                => Ok(next_in_namespace(&ns.entities, forker, 2)),    // V9 cross-owner: S(pfx,2)
        _                       => Err(NsError::VersionOutOfDomain),                  // P-tier: node non-owner
    }
}
```

M5's VERSION composite folds this into its closure: compute `v`, stage `W::wrap(NsRecord::Register{v})` (M3's record) + M5's arrangement-snapshot and provenance records, commit as one `transact`. M3 owns the *identity allocation*; M5 owns the *composite*. **Unification:** the cross-owner version branch, `fork_address`, and `create_document(caller, own-account)` are all `next(E, pfx(π), 2)` — one frontier serves explicit creation, denial-as-fork, and cross-owner versioning; O5 holds by construction for all three (the caller is the most-specific coverer of its own fresh slot). The content-sharing half of fork/version is always M5's.

### 7. The pure composable surface (how M5/M7/M9 use M3)

M3 mints *content/link* addresses without depending on M4/M7 by publishing the math and letting the owning store supply the witness — exactly M2's contract-3 pattern. Inside M5's placement composite, each content `K.α` mints by folding M3's pure allocator against `stg.working()` (so a multi-atom run advances atom-by-atom; reading `base()` would recompute one address *m* times and collide):

```rust
// inside M5's single transact([ns_key(d, s_C)], |stg| { … }) :
let dom_c = stg.working().content();                     // M4's OrdMap — M5's slice, not M3's
let a = next_in_namespace(&dom_c, &content_anchor(&d), 1);// M3's pure math + M1's inc
// (precondition is_registered(stg.working().ns(), &d)  ← P6/C2: home document registered)
stg.push(W::wrap_content(K_α{ a, bytes }));              // M4's record — NOT folded as a nested transact
```

M7's MAKELINK folds `next_in_namespace(&dom_l, &link_anchor(&d), 1)` the same way (L1a origin check via `is_registered`). M9 resolves residence via `is_registered`/`ω`. None of these is a nested `transact` (that deadlocks on M2's applier lock); they reuse M3's *pure bodies*. **Edit authorization** for those composites (`ω(d) == caller`) is the caller's (M5/M10) — M3 supplies `owns`/`ω`, the policy lives at the consumer; M3's minting math is auth-free mechanism (Lampson separation).

### 8. Genesis & recovery

`genesis()` returns `E₀ = {[1]}`, `Π₀ = {[1]}` (Σ₀; n₀ baptized at genesis; O14 coverage). The ordered-set registry needs **no auxiliary seed-root set** — `[1]` is just a member, dissolving the special case ASN-0040's counter representation required for non-child roots. Recovery is entirely M2's: replay `Register`/`RegisterPrincipal` into the `OrdSet`s; with no stored frontier and no mandatory hints, `rebuild_derived` is the identity.

## Invariants & contracts

**By construction** (from the data model / a pure `next`):
- *Permanence / irrevocability* — B0/B0★ (ASN-0040), P1/P3 (ASN-0047), O12/O13 (ASN-0042): no delete/overwrite arm exists; `E`/`Π` only grow.
- *Determinism, finiteness, no global counter* — B2/B_fin (ASN-0040), V5b (ASN-0123): `next` is a pure function of the store; no entropy, clock, or authoritative counter.
- *Gap-free contiguity* — B1/B2 (ASN-0040), VN-B1 (ASN-0123): `next` returns `c_{hwm+1}`; registration is the sole growth path.
- *Cross-namespace uniqueness* — B7/B8-cross (ASN-0040), T10/GlobalUniqueness (ASN-0034), CrossDocumentDisjointness (ASN-0093): distinct namespaces are prefix-incomparable or level-distinct.
- *Level-aware non-collision of document vs version chains* — V0/V5 (ASN-0123): the truncate-then-increment isolates `S(A,2)` from `S(d,1)` (§Internal 1).
- *T4 validity of every minted address* — B10/M0 (ASN-0040/0093): the B6 gate + conforming seed.
- *Unbounded extent* — B9 (ASN-0040): M1's `BigUint` tumblers, no fixed cap.
- *Content-independence / ghosts* — B3 (ASN-0040), existence = `E` membership not `M(d)=∅` (ASN-0047): `E` is disjoint from C/L/M.
- *Ownership is a theorem, exclusive ω* — O1/O2 (ASN-0042): `owns` is a pure prefix test; ω = longest-match + injectivity.
- *Refinement-only / irrevocable delegation / node-locality* — O3/O8/O9 (ASN-0042): append-only `Π` + immutable prefixes + prefix geometry.

**By active enforcement** (M3 must guard, named):
- *Same-namespace uniqueness* — B8-same (ASN-0040): `ns_key(home, g)` serializes via M2's keyed critical section (§Internal 2).
- *Atomic baptize+register* — B4 (ASN-0040), O15/delegation atomicity (ASN-0042): one record per `transact` (§Internal 2/4).
- *B6/T4 gate* — B6/TA5a (ASN-0040/0034): `inc_preserves_t4(p, g)` checked before each organizational mint (§B).
- *Parent-exists* — P8 (ASN-0047): `parent(e) ∈ E` for non-nodes, checked in each registration op. **This resolves the ASN-0040-vs-0047 tension** — see Conflicts.
- *Origin-registered for content/link* — P6/C2/L1a (ASN-0047/0093): M3 supplies `is_registered`; M5/M7 enforce before folding the content/link mint.
- *Tier floor* — O1a (ASN-0042): delegate prefix `zeros ≤ 1`, checked in `create_account`.
- *ω-based write authorization (O5 SubdivisionAuthority)* — O5 (ASN-0042): `ω(target) == caller`, never `owns` (§Internal 3/7). **This resolves the ASN-0103-vs-0042 tension** — see Conflicts.
- *Prefix-injectivity* — O1b (ASN-0042): frontier mints are fresh, keeping ω single-valued.
- *Node freshness + lineage* — NodeBaptism (ASN-0047): `Node(n) ∧ n ∉ E ∧ n₀ ≼ n` in `register_node`.

## Dependencies & seams

**Uses M1:** `inc` + `inc_preserves_t4` (frontier mint + B6 gate); `classify`/`Level`/`Class`, `validate`, field projections (`node_field`/`account_field` to build account/node prefixes for ω), `is_prefix` (`owns`), `parent`/`document_of`, `subtree_of`/`shift` (the `max_with_prefix` range bound), `Ord` (the `OrdSet`). No allocator state lives in M1 — M3 enforces the gate M1 only *predicates*.

**Uses M2:** `transact` (commits each organizational baptism, keyed `ns_key(home, g)`); `snapshot` (reads of `E`/`Π` for queries and for folding the pure surface); the `WorldState`/`apply` seam (M3 contributes `NsRecord` variants + apply arms via `NamespaceWorld::wrap`); `genesis` (the seed `Σ₀`). M3 holds no journal and no recovery of its own.

**Exposes downstream (seam contracts neighbors build against):**
- **→ M5:** `is_registered` (edit precondition "is d registered?"); `next_in_namespace` + `content_anchor` (content minting, folded into M5's placement composite against its `dom(C)` slice); `version_identity` + `NsRecord::Register` (VERSION composite); `fork_address` (denial-as-fork / cross-owner base). M3 never reads or writes `M(d)`.
- **→ M7:** `is_registered` (link origin check L1a); `next_in_namespace` + `link_anchor` (link minting, folded into MAKELINK).
- **→ M6, M8:** `is_registered`/`is_document` — the **registered-empty (`⟨⟩`) vs unallocated (fail)** distinction is built *by them* on top of this membership answer (M3 owns existence; M5/M6/M8 own the emptiness/result interpretation).
- **→ M9:** `is_registered`/`effective_owner` for residence resolution (predicate-def *content* creation rides M5's placement composite, not M3 directly).
- **→ M10:** the transact-wrapped ops (`create_document`/`create_account`/`register_node`/`fork_address`) for dispatch; `owns`/`ω` for session authorization; `NsError` for typed rejection surfacing.
- **→ everyone:** `owns` (stateless, edge), `effective_owner` (central).

**Explicitly not a seam M3 provides:** content/link *storage* (M4/M7); the arrangement `M(d)` (M5, lazy); the frontier as durable state (recomputed); any raw `baptize(p,g)` (only the typed, precondition-gated ops mint into `E`).

## Conflicts resolved

1. **ASN-0040 "no parent-baptized precondition" vs ASN-0047 P8 "parent ∈ E."** ASN-0040's `Bop` requires only B6 (a position may be baptized beneath an unbaptized virtual parent) — it explicitly *defers* whether ordering needs a baptized parent to the ownership/transition layer. M3 *is* that integrated layer, so its organizational ops **enforce P8** (`parent(e) ∈ E` for non-nodes; lineage for nodes). The permissive baptism is the lower stratum; M3 layers P8 on top. Not a contradiction — a deferral M3 settles.

2. **ASN-0103 `CND.pre` (containment) vs ASN-0042 O5/exclusive-ω.** ASN-0103 gives `pfx(π) ≼ A` (containment) as CREATENEWDOCUMENT's precondition — sound only in a flat, account-only hierarchy (Green's reality, where `owns ≈ ω`). In M3's multi-tier model with delegation, containment lets a node operator create documents inside a *delegated* account (`owns([1],[1,0,5])` is true), the exact ownership-divergence O2/O3/O8 forbid. M3 **upgrades the gate to O5 SubdivisionAuthority — `ω(account) == caller`** (the caller must be the *exclusive* owner, the longest coverer), which refuses the ancestor. ASN-0103's containment is the flat-model simplification; the multi-tier integration uses ω.

3. **Counter representation (ASN-0040) vs ordered map (ASN-0093 / M2).** ASN-0040 recommends per-namespace high-water counters + an auxiliary set for non-child roots "for baptism *alone*"; it also says pick the hierarchical/ordered structure "when the broader system needs subtree/range queries." M3 *does* — longest-prefix ownership, level-aware version enumeration, the truncate-then-increment frontier, and the registered-empty range scans. So M3 picks the **ordered set** (recompute-always frontier, matching M2's persistent substrate), with the counter demoted to an optional O(1) frontier *hint*. This dissolves the auxiliary-seed-root set (`[1]` is just a member) and gives the version/document level-separation a clean predecessor query.

4. **"Mints content/link addresses via M3" vs `M3 ↛ M4/M7`.** M3 cannot read `dom(C)`/`dom(L)`. Resolution: M3 owns the frontier *algorithm* (`next_in_namespace`, pure); M4/M7 hold the authoritative store; M5's composite / M7's MAKELINK apply M3's math to their own slice inside their own transaction. "Via M3" = via M3's pure minting function, never a held content/link frontier (which would be authoritative-duplicate state — the anti-pattern). Consistent with M2's "M5 reuses M3's pure `recompute_max`/`inc` math."

5. **Naming.** `account` is M3's level name (matching M1); `acct(a)`/`U` (ASN-0042's account-prefix projection / user field) map to M3's `account_prefix`/M1's `account_field`. Delegation (ASN-0042 policy) and K.δ account creation (ASN-0047 mechanism) are one operation (`create_account`), folded because "a delegation is a baptism" (O18).

## Open build decisions

- **Registry representation.** Ordered set (chosen) vs ASN-0040 counters+aux-set vs hierarchical tree. The optional per-`(home,g)` next-address cache (recompute-on-miss) is the O(1) hint over the chosen set — add only under measured allocation-latency pressure; never persist it as truth.
- **Frontier strategy.** Recompute-always (default; matches Green's stateless query-and-increment) vs cached frontier hint — pick on write rate.
- **ω resolver.** Ancestor-walk longest-match (recommended; exploits the `zeros ≤ 1` floor to bound candidates) vs linear scan over `Π` vs radix/PATRICIA trie vs an `address → owner` cache (rebuilt from `Π`) — sized to `|Π|`, query rate, and whether historical `ω_Σ` snapshots are wanted (free from retained persistent roots).
- **Version/document level separation.** Truncate-then-increment (recommended — robust to a version being the lexical max) vs an explicit length/level filter (clean only if the index already keys on level).
- **Delegate-prefix policy.** Frontier-only (default, O17c) vs baptize-intermediates to reach a chosen prefix (the ASN-0042 worked-example path).
- **Principal metadata.** Bare `OrdSet<Tumbler>` of prefixes (recommended — kind is `classify`-derivable, delegator is recomputable as most-specific coverer) vs an `OrdMap` recording delegator/seq. The recompute shortcut breaks if ownership *transfer* is ever added (an out-of-model open question) — be explicit it holds only while refinement stays monotone.
- **Fork/create/version unification.** Expose `fork_address` as a distinct entry point (intent-clarifying) vs collapse into `create_document(self, own-account)`; the underlying `next(E, pfx(π), 2)` is shared regardless.
- **Idempotency / retry.** M3's mints are non-idempotent by the identity-is-address lock (CND, no idempotency key); under M2's lost-ack case a committed-but-unacked `create_document` replays and a client retry mints a *second* (harmless orphan empty document, B3). Exactly-once must live at M10's session layer (a request key) — decide there, not here.
- **Genesis configuration.** Single node operator (`E₀={[1]}`, `Π₀={[1]}`) vs a multi-node bootstrap seed (still O14-conforming: nonempty, finite, account-tier, injective, pairwise non-nesting, covering, baptized).
- **`LockKey` byte layout.** The `ns_key` discriminant encoding (`(home, mode)` for organizational vs `(doc, subspace)` for content/link) — must align with M5/M7's `key(d, s_C)` shape and draw its 1-byte space tag from the engine's central enum.
