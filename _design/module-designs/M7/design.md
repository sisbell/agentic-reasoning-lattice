# M7 — Link & Relation Store — Build-Spec Design

## Purpose & boundary

M7 owns the **authoritative, append-only store of links and typed relations** — every connection in the docuverse — keyed by the link's own permanent address, together with the recomputable **coverage indexes** that answer "which links touch this region." It does one thing: *be the single writer and the single source of truth for link values, and serve every read of structural relation state that does not require V-resolution.* It owns the write surfaces (MAKELINK, Emit/Nullify, assert_sup/editlink), the raw reads (READLINK, FOLLOWLINK), the typed-relation observers (Observe + the four behavior atoms BH1–BH4), the immutable type/shape registry, idempotent de-duplication, and the spanfilade.

It does **not** own: address minting or the home-existence/ownership facts (**M3** — M7 *calls* `mint_link`, reads `is_registered_document`); the V→I arrangement or the home seating mechanism (**M5** — M7 *calls* the semantics-blind `resolve`/`stage_seat_link`, never interpreting arrangement); ordering/durability/recovery (**M2**); the **provenance relation R** (M5 — link placement is deliberately *uncoupled* from R, ASN-0047 J-LV, so M7 touches no R); **non-transcludability** enforcement (M5's content-side referential-integrity check — M7's only duty is to keep links in `s_L`); and **indexed discovery *presentation*** — findlinks/count/windowed-pagination/projection/RETRIEVEENDSETS (**M8**, which executes over M7's spanfilade across the `M8→M7` edge). The split between M7 and M8 is *index ownership and matching* (M7) vs *cursoring/counting/projecting* (M8).

## Public interface

Types `Tumbler/Address/Span/SpanSet/CanonicalForm/Nat` are M1's; `Kernel/Snapshot/LockKey/Seq/TxnError/WorldState` are M2's; `M3Rec/HasM3/MintError`, `M5Rec/HasM5/VSpec/Run` are M3/M5's. Pure reads are methods on `LinkState` over any `Snapshot`; transact-driving ops hang off `LinkStore<'k,W>` (holds `&'k Kernel<W>`) and are generic over `W` per the engine composition contract. Slots are 1-based: `FROM=1, TO=2, TYPE=3`. Subspace constants are ASN-0093's `s_C = 1` (content), `s_L = 2` (link). `Endset` (M7's readable endset newtype, §Core data model) is the link-value carrier throughout.

### A. Engine-plug surface

```rust
pub trait HasLinks { fn links(&self) -> &LinkState; }

/// The ONE authoritative delta. Every write — MAKELINK link, Emit_K tuple, retraction emitter,
/// supersession claim, editlink successor, pdef/pd_stable classifier — is a deposit of an immutable
/// link at a fresh address. There is no update, no delete, no tombstone record.
#[derive(Clone, Serialize, Deserialize)]
#[non_exhaustive]
pub enum LinkRec { Emit { addr: Tumbler, value: Link } }

impl LinkState {
    /// Validate `decls` against `reserved` (TypeRegistry::build), seal BOTH as authoritative genesis
    /// config, start from links = ∅. The built lookup registry and EVERY hint are RECOMPUTABLE
    /// (rebuild_derived); only `reserved` + `decls` (Serialize, `Arc`-wrapped) are checkpointed. The
    /// engine builds the genesis slice here at assembly, propagating RegistryError.
    pub fn genesis(reserved: ReservedAddrs, decls: Vec<TypeDecl>) -> Result<LinkState, RegistryError>;
    /// Pure/total/deterministic M2 fold; maintains ALL hints incrementally and carries the genesis
    /// config (`reserved`/`decls`/`registry`) forward unchanged. Applied exactly once per record.
    pub fn apply_link(&self, r: &LinkRec) -> LinkState;
    /// Runs once at load, BEFORE replay: rebuilds the (skip) lookup `registry` from the deserialized
    /// `reserved`+`decls`, THEN every (skip) hint from `links`+`registry`. Required because both are
    /// `#[serde(skip)]` — M2's default identity would leave them empty (and replay needs the registry).
    pub fn rebuild_derived(self) -> LinkState;
}
```

### B. Type registry (immutable, construction-time)

```rust
#[derive(Clone, Copy, PartialEq, Eq, Serialize, Deserialize)] pub enum Shape { Unary, Binary, Multi }
#[derive(Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub enum Behavior { ReadFilter, Walk, ReverseLookup, Age } // BH1..4 (Ord so it backs im::OrdSet)
#[derive(Clone, Serialize, Deserialize)]
pub struct Registration { pub shape: Shape, pub idem: bool, pub behaviors: im::OrdSet<Behavior> }

#[derive(Clone, Serialize, Deserialize)]
pub struct TypeDecl { pub key: Endset, pub reg: Registration }  // app-declared type; key names the coverage class
#[derive(Clone, Serialize, Deserialize)]
pub struct ReservedAddrs {            // the five reserved type addresses — parameters in the manner of s_C/s_L
    pub pred_def: Address, pub pred_stable: Address,            // coordinated with M9
    pub retired: Address,  pub supersedes: Address, pub retraction: Address,  // [K_ret]/[K_sup]/[R]
}
pub enum RegistryError {
    KeyCollision, EmptyKey, BadBehavior, ReservedClassClash, ReservedSubspaceClash, NonAddressDenotingKey,
}

impl TypeRegistry {
    /// Validate-once-or-fail (C0 + R-C0 + R-C1 + reserved-isolation + idem-key denotation) — the
    /// registry's only write point. Seeds the five shipped types (each `key = enc({reserved.<addr>})`)
    /// BEFORE app decls.
    pub fn build(reserved: ReservedAddrs, decls: Vec<TypeDecl>) -> Result<TypeRegistry, RegistryError>;
    pub fn registration(&self, class: &CoverageClass) -> Option<&Registration>;  // internal lookup
    pub fn reserved(&self, t: ShippedType) -> &Endset;   // the genesis-fixed type endset for a shipped class
}
impl Default for TypeRegistry { /* the empty registry — serde seeds the #[serde(skip)] field with it;
                                  rebuild_derived replaces it from reserved+decls before replay */ }
pub enum ShippedType { Retired, Supersedes, Retraction, PredDef, PredStable }
```

`TypeRegistry::build` enforces **C0** (finite, key uniqueness → `KeyCollision`, non-empty representatives → `EmptyKey`); **R-C0**'s behavior↔shape compatibility → `BadBehavior` — **BH1 (ReadFilter) ⇒ Unary; BH2 (Walk) ⇒ Binary; BH3 (ReverseLookup) ⇒ Binary; BH4 (Age) ⇒ idem = ⊥** (any shape); **R-C1** (no app key coverage-equal to a reserved shipped class → `ReservedClassClash`); the **reserved-isolation** precondition (every `ReservedAddrs` entry is element-level with `subspace ∉ {s_C, s_L}` → `ReservedSubspaceClash`, §Core data model); and the **idem-key denotation** precondition (every idem⊤ `TypeDecl.key` is address-denoting → `NonAddressDenotingKey`, §3). `genesis` wraps `build`, storing `reserved`+`decls` (each `Arc`-wrapped) as authoritative config and the built registry as a recomputable lookup (§Core data model); `TypeRegistry` also implements `Default` so serde can seed the `#[serde(skip)] registry` field on deserialize. Shipped registrations are fixed: `Retired = Unary/⊤/{ReadFilter}`, `Supersedes = Binary/⊤/{Walk}`, `Retraction = Binary/⊤/{}`, `PredDef = Unary/⊤/{}`, `PredStable = Unary/⊤/{}` — the `PredDef`/`PredStable` shape/idem/behavior values are **M9-coordination assumptions** (no digested note pins them; they are M7↔M9 build-time agreements, alongside the `ReservedAddrs` addresses).

### C. Write — open content links (ASN-0120 MAKELINK)

```rust
impl<'k,W> LinkStore<'k,W>
where W: WorldState + HasLinks + HasM3 + HasM5,
      W::Record: From<LinkRec> + From<M3Rec> + From<M5Rec>
{
    /// Resolve three V-spec-sets to content I-extent endsets (via M5's `resolve` + `Run::iextent`),
    /// require the type endset non-empty, mint a fresh home-scoped link, deposit the standard triple,
    /// then seat it in `home`'s link subspace. ONE M2 composite under `link_lock_key(home)`. NO shape
    /// gate, NO idem dedup (distinct links always — ML0). NO provenance. Resolution reads off the txn
    /// base (single linearization, §2).
    pub fn makelink(&self, home: &Address, from: Vec<VSpec>, to: Vec<VSpec>, ty: Vec<VSpec>)
        -> Result<(Address, Seq), TxnError<MakeLinkError>>;
}
pub enum MakeLinkError { HomeNotRegistered, IllFormedSpec, EmptyTypeResolution, Mint(MintError), Seat(SeatError) }
```

### D. Write — managed typed relations (ASN-0086/0126/0128/0125)

```rust
impl<'k,W> LinkStore<'k,W>
where W: WorldState + HasLinks + HasM3, W::Record: From<LinkRec> + From<M3Rec>
{
    /// Emit_K: gated typed-relation emission. Shape-gated (registered ∧ shape-conformant ∧ K≁R).
    /// idem(K)=⊤ ⇒ dedup against the ACTIVE view; a hit returns the incumbent and commits NOTHING
    /// (zero-step). Does NOT seat. value = Link[enc({from}), enc(to), ty.clone()] — `from` single
    /// (|F|=1 forced), `to` cardinality shape-checked, `ty` stored verbatim as e₃. Used by M9
    /// (pdef/pd_stable, rule fires) and managed app relations. The op acquires [dedup_key,
    /// link_lock_key(home)] (idem⊤) or [link_lock_key(home)] (idem⊥) before the transact (§3).
    pub fn emit(&self, home: &Address, ty: &Endset, from: &Address, to: &[Address])
        -> Result<(Address, Seq), TxnError<EmitError>>;

    /// Nullify_Binary: the SOLE retraction path. Emits an [R] tuple, canonical from-fill enc({home}),
    /// unit-depth to-span enc({target}); Retraction gate (idem⊤). P-tgt enforced as a REJECTING
    /// precondition (target a resident link OR the call's own fresh emitter) ⇒ sterilization
    /// unreachable through this surface. Lock set [dedup_key, link_lock_key(home)].
    pub fn nullify(&self, home: &Address, target: &Address)
        -> Result<(Address, Seq), TxnError<NullifyError>>;

    /// assert_sup: emit "old is superseded by new" — F=enc({old}), G=enc({new}), type [K_sup]
    /// (slot convention per Conflicts §2). Idem⊤; lock set [dedup_key, link_lock_key(home)]. Requires
    /// home registered, both endpoints resident links, and old ≠ new (irreflexive, Df-DISC(ii)).
    pub fn assert_sup(&self, home: &Address, old: &Address, new: &Address)
        -> Result<(Address, Seq), TxnError<AssertSupError>>;

    /// editlink: ONE composite over [link_lock_key(d_s), link_lock_key(d_a)] — allocate a fresh
    /// successor link (value supplied directly; M10 builds it via `Link::new`, arity 3), then assert it
    /// supersedes `original`. CANNOT call public assert_sup (M2 non-reentrant). Successor born
    /// UNSEATED. DC guard: reject a retraction-typed successor; schema-conform a claim-typed one. Claim
    /// dedup is vacuous/lock-free (its key carries the fresh successor — §2/§3). M10 forms a content
    /// successor off any prior snapshot (recorded I-addresses are permanent — ML8/EL0; §2).
    pub fn editlink(&self, original: &Address, successor: Link, d_s: &Address, d_a: &Address)
        -> Result<(Address /*successor*/, Address /*claim*/, Seq), TxnError<EditLinkError>>;

    /// BH4 batch tooling: nullify every stale tuple of `ty` (age > horizon), stale set snapshotted
    /// at entry. NOT atomic — a sequence of `nullify` transacts. On full success returns the per-target
    /// (emitter, Seq) Vec (an already-nullified target dedups to a hit + base Seq); on first TxnError
    /// returns Err, leaving earlier nullifies committed and durable — a re-run is safe (§7).
    pub fn retract_stale(&self, d_retr: &Address, ty: &Endset, horizon: u64)
        -> Result<Vec<(Address, Seq)>, TxnError<NullifyError>>;
}
pub enum EmitError      { HomeNotRegistered, NotRegistered, ShapeViolation, RetractionClass, Mint(MintError) }
pub enum NullifyError   { HomeNotRegistered, BadTarget, Mint(MintError) }
pub enum AssertSupError { HomeNotRegistered, EndpointNotResident, SelfSupersession, Mint(MintError) }
pub enum EditLinkError  { OriginalNotResident, HomeNotRegistered, IllFormedSuccessor, DcViolation, Mint(MintError) }
```

### E. Raw reads (ASN-0111 / ASN-0114) — pure, arrangement-independent

```rust
impl LinkState {
    pub fn readlink(&self, a: &Address) -> Option<Link>;             // Σ.L(a) verbatim (readable endsets), or None (=⊥)
    /// Ok(spans) coverage-exact to slot `i`; Ok(SpanSet::empty()) = ⟨⟩ (valid-but-empty success);
    /// Err = ⊥ (link or slot absent). The Result/Ok-empty shape makes ⟨⟩ ≠ ⊥ unforgeable (F7).
    /// Returns M1's SpanSet (coverage-exact, F1/F3 — the consumer does span-set algebra); the
    /// boundary fold `Endset → SpanSet` is the lone M1-call use of `to_spanset`.
    pub fn followlink(&self, a: &Address, i: usize) -> Result<SpanSet, Invalid>;
}
pub struct Invalid;
```

### F. Typed-relation reads & the PL surface for M9 (ASN-0086 / ASN-0128 / ASN-0125)

```rust
pub enum View { Audit, Active, Default }    // Default (active∖filtered) only on members/targets_of; observe coerces Default→Active
pub struct Tuple { pub addr: Address, pub from: Endset, pub to: Endset }   // endsets are M7's readable Endset
pub enum Tip { Sink(Address), Indeterminate }   // ⊥ at branch or cycle
/// EL14 disclosure-not-decision: the operative sink, its OWN activity, and `claims` = the operative
/// [K_sup] claims whose `new` endpoint IS this sink (the inbound supersession edges that establish it;
/// empty for a self-sink) — their homes recoverable by `document_of` (EL8b). The reader applies
/// narrowing; M7 decides nothing.
pub struct CurrentMember { pub member: Address, pub active: bool, pub claims: Vec<Address> }

impl LinkState {
    // Observe + default predicates
    pub fn observe(&self, ty: &Endset, from_pat: &[Address], to_pat: &[Address], v: View) -> Vec<Tuple>; // exact ⊆-coverage; Default→Active
    pub fn is_k(&self, ty: &Endset, a: &Address) -> bool;                 // D2 (exact active coverage-membership; NOT a stab call)
    pub fn members(&self, ty: &Endset, v: View) -> Vec<Address>;          // D1
    pub fn targets_of(&self, ty: &Endset, x: &Address, v: View) -> Vec<Address>;  // D3
    pub fn is_active(&self, a: &Address) -> bool;  pub fn is_nullified(&self, a: &Address) -> bool;
    // BH1 read-filter | BH2 walk | BH3 reverse | BH4 age — served entirely from M7's own indexes
    pub fn is_filtered(&self, a: &Address) -> bool;                       // v1: single shipped BH1 (Retired) — see §7
    pub fn succs(&self, ty: &Endset, x: &Address) -> Vec<Address>;        // BH2 walk family — v1 serves only the shipped Supersedes class (§5); empty for other ty
    pub fn chain(&self, ty: &Endset, x: &Address) -> Vec<Address>;   pub fn tip(&self, ty: &Endset, x: &Address) -> Tip;
    pub fn sources_to(&self, ty: &Endset, target: &Address) -> Vec<Address>;
    pub fn target_of(&self, ty: &Endset, source: &Address) -> Option<Address>;
    pub fn targets_keyed(&self, source: &Address) -> im::HashMap<CoverageClass, Address>;  // BH3: target_of joined over all BH3 Binary types
    pub fn age(&self, a: &Address) -> Option<u64>;   pub fn stale(&self, ty: &Endset, h: u64) -> Vec<Address>;
    // ASN-0125 currency (BH2 over the operative supersession graph)
    pub fn current(&self, y: &Address) -> Vec<CurrentMember>;             // set-valued disclosure (EL14); hardwired to [K_sup]
    // shipped reserved-type endsets — M9 reads PredDef/PredStable here (registry lookup is internal)
    pub fn reserved_type(&self, t: ShippedType) -> &Endset;
}
```

### G. Discovery primitives for M8

```rust
impl LinkState {
    /// Spanfilade primitive: links whose slot-`i` coverage OVERLAPS `query`. The one shared index probe.
    /// `query` is M7's READABLE Endset (M8 builds it) so M7 can iterate its spans for `classify_spans` overlap.
    pub fn stab(&self, i: usize, query: &Endset, v: View) -> im::OrdSet<Tumbler>;
    /// The AND-of-(per-slot overlap) combiner — findlinks' core, factored into M7 (Conflicts §6).
    pub fn match_links(&self, constraints: &[(usize, Endset)], v: View) -> im::OrdSet<Tumbler>;
    pub fn type_slice(&self, ty: &Endset, v: View) -> im::OrdSet<Tumbler>;    // L_K (Audit) / A_K (Active)
}
```

**Return-type convention.** §G's discovery primitives return raw `im::OrdSet<Tumbler>` — the index's native key, which M8 cursors, counts, and paginates over directly without re-validation; their **query inputs are M7's readable `Endset`** (M8 builds them via `enc`/`Endset::from_spans`), so M7 can iterate the query spans for overlap. §F's caller-facing reads return validated `Address` (and `Tuple`/`CurrentMember`, whose endsets are now readable). M7 lifts `Tumbler → Address` at the §F boundary; every stored key is T4-valid by M3's mint, so the lift is infallible.

## Core data model

```rust
/// M7-OWNED endset — a READABLE finite span sequence, the as-created decomposition held VERBATIM
/// (observable via raw read-back, ML2/RL1). NOT M1's `SpanSet`, which is read-opaque to M7 (it exposes
/// no span iterator and no field access). Iterate `spans()` directly; fold to a `SpanSet` ONLY at an
/// M1-call boundary (`canonical_key`/`normalize`/`equiv`). Coverage is a query-time projection.
#[derive(Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Endset(im::Vector<Span>);

impl Endset {
    pub fn empty() -> Endset;                                          // ⟨⟩ (distinct from any zero-width span)
    pub fn from_spans(spans: impl IntoIterator<Item = Span>) -> Endset; // verbatim; MAKELINK & M10 content successors build here
    pub fn spans(&self) -> impl Iterator<Item = &Span>;               // the readable decomposition (L5: membership, not position)
    pub fn len(&self) -> usize;                                       // # spans
    pub fn is_empty(&self) -> bool;                                   // == ⟨⟩  (the e₃ ≠ ∅ write-boundary check reads this)
    pub fn denotes(&self, t: &Tumbler) -> bool;                       // t ∈ coverage:  ∃ s ∈ spans : s.contains(t)
    pub fn addrs(&self) -> impl Iterator<Item = &Tumbler>;            // AD readback: start of each unit-depth span (s == subtree_of(s.start()))
    fn   to_spanset(&self) -> SpanSet;                                // INTERNAL — fold singleton+union (M1 union = concatenation, order-preserving)
}

#[derive(Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Link { slots: im::Vector<Endset> }   // arity = slots.len() ≥ 3; positional accessors only

impl Link {
    pub fn new(slots: impl IntoIterator<Item = Endset>) -> Option<Link>;  // None ⇔ arity < 3 (the type floor /
                                                                          // ASN-0043 L3 capacity; e₃ ≠ ∅ is a
                                                                          // WRITE-boundary check, not here)
    pub fn arity(&self) -> usize;                       // |L| ≥ 3
    pub fn slot(&self, i: usize) -> Option<&Endset>;    // 1-based; None iff i < 1 ∨ i > arity
    pub fn from_slot(&self) -> &Endset;                 // e₁ (FROM=1)
    pub fn to_slot(&self) -> &Endset;                   // e₂ (TO=2)
    pub fn type_slot(&self) -> &Endset;                 // e₃ (TYPE=3)
}

/// Canonical address-set encoding (AD): one unit-depth span per address, `{subtree_of(x) : x ∈ X}`
/// — exactly what the managed surface (Emit_K/Nullify/assert_sup/claims) emits, with `enc(X).addrs() = X`.
/// M9 builds reserved-type endsets the same way (or reads them via `LinkState::reserved_type`); M10
/// builds an editlink content successor via M5's `resolve` + `Run::iextent` + `Endset::from_spans`
/// (address slots via `enc`) + `Link::new`; M8 reads structure via `readlink` + the Link/Endset accessors.
pub fn enc(addrs: &[Address]) -> Endset;   // Endset::from_spans(addrs.iter().map(|a| subtree_of(a.tumbler())))

#[derive(Clone, Serialize, Deserialize)]
pub struct LinkState {
    links:    im::OrdMap<Tumbler, Link>,         // ── AUTHORITATIVE ── append-only, immutable values
    reserved: Arc<ReservedAddrs>,                 // ── AUTHORITATIVE ── genesis type config; Arc ⇒ O(1) per-fold clone (serde `rc`)
    decls:    Arc<Vec<TypeDecl>>,                 // ── AUTHORITATIVE ── genesis type config; Arc ⇒ O(1) per-fold clone (serde `rc`)
    #[serde(skip)] registry: Arc<TypeRegistry>,   // ── RECOMPUTABLE ── lookup map; rebuilt from reserved+decls (TypeRegistry: Default seeds the skip)
    #[serde(skip)] hints:    Hints,               // ── RECOMPUTABLE ── rebuilt from links+registry (Hints: Default seeds the skip)
}
```

**The authoritative state is one map plus the genesis type config.** `links : Tumbler ⇀ Link` is append-only and immutable: a `LinkRec::Emit` only ever *inserts* at a fresh key, never mutates or removes. This single decision makes **Permanence (L12/R2), append-only audit (R3), retraction stability (R6a)**, and lock-free MVCC reads *free* — every `Snapshot` pins an immutable root, and a reader is untouched by concurrent appends. `im::OrdMap` keyed by `Tumbler` (the `Ord`-bearing type; callers pass `&Address`, M7 converts) gives O(log n) point lookup *and* the prefix-range scans that home-set enumeration and the frontier want — the one structure serving readlink, allocation-adjacent scans, and the indexes. `reserved`/`decls` are `Arc`-wrapped so the clone-and-modify `apply_link`/`World::apply` bumps a refcount rather than copying the declaration vector on every record. **Identity is the key, never the value:** the store is *never* content-addressed on the endset (NonInjectivity L11b — two byte-identical links are distinct objects); hashing the payload would collapse them, so this is forbidden.

**The registry is genesis config, not a fold of records**, yet `apply_link` must consult it *during replay* (to recognize the `[R]`/`[K_sup]` coverage classes that drive `nullified`/`sup_fwd`). The lookup `registry` is keyed by `CoverageClass`, which is *not* `Serialize` (its `Extents` variant wraps M1's non-`Serialize` `CanonicalForm`), so the registry cannot itself ride a checkpoint. M7 therefore persists the *serializable build inputs* — `reserved: Arc<ReservedAddrs>` and `decls: Arc<Vec<TypeDecl>>` (both `Serialize` under serde's `rc` feature) — as **authoritative** state, and treats the lookup `registry` as `#[serde(skip)]` recomputable. On deserialize, serde seeds the two `#[serde(skip)]` fields via `Default` — `TypeRegistry: Default` (the empty registry) and `Hints: Default` (derived) — placeholders that `rebuild_derived` replaces *before* replay: it reconstructs `registry = TypeRegistry::build(reserved, decls).expect("validated at genesis")` (the inputs are already-validated authoritative state, so the rebuild cannot fail), then recomputes every hint. This is load-bearing because M2 recovers from the deserialized checkpoint whenever a retained one exists — genesis `W` is consulted only on full fallback — so a skip-the-registry-and-reseed-from-engine-genesis scheme would deserialize an empty registry and silently mis-replay. That option is rejected.

**`Link` is a positional sequence of endsets.** `im::Vector` because slot index is a primitive (L6) and arity is read off the value (FOLLOWLINK's post-lookup bound). Each `Endset` is **M7's own readable newtype over `im::Vector<Span>`**, held **verbatim** (the as-created span decomposition is observable through raw read-back — ML2/RL1 — so we never canonicalize at rest; coverage is a *query-time projection* computed by iterating the spans). M7 owns this type *because M1's `SpanSet` is read-opaque* — it exposes no span iterator and no field access, so a stored `SpanSet` endset could feed neither an incremental hint fold nor an enumerated read (`members`/`addrs`/`sources_to`). M7 reads its endsets through `spans()`/`addrs()`/`denotes()` (each span's `start()/width()/reach()/contains()` is M1-public) and folds to a `SpanSet` *only* at an M1-call boundary (`canonical_key` for the `Extents` class). `Link::new(slots)` enforces only the type floor — arity ≥ 3, ASN-0043 L3's *capacity*; the store invariant `e₃ ≠ ∅` (L3) is enforced at the *write boundary*, not the type (Conflicts §3). **No creation op realizes arity > 3:** MAKELINK builds the standard triple `[e₁,e₂,e₃]`, Emit_K/`assert_sup`/the editlink claim build arity-3, and `editlink` rejects a successor whose `arity() ≠ 3` (`IllFormedSuccessor`). So the store holds only arity-3 links — the spanfilade's three slots are exhaustive, RL2's "N > 3" read branch is vacuous over this store, and `type_class`/`type_slice`/`observe` meet ASN-0086's `|Σ.L(a)| = 3` restriction with no explicit arity filter.

**Everything else is a recomputable hint** — a pure function of `links` (+ `registry`), maintained incrementally in `apply_link` and re-seeded by `rebuild_derived`. This is the Lampson spine: the journal (via M2) is truth; lose any hint and replay rebuilds it, never wrong.

```rust
#[derive(Clone, Default)]
struct Hints {
    spanfilade: [SlotIndex; 3],                            // per standard slot: covered-extent → link addrs (overlap).
                                                           // SlotIndex = the deferred interval/segment index (Open
                                                           // decisions); the brute-force bootstrap leaves it empty and
                                                           // `stab` scans `links` directly (reading each endset's spans).
    type_class: im::HashMap<CoverageClass, im::OrdSet<Tumbler>>,  // typed slices L_K (Observe, type-match)
    nullified:  im::OrdSet<Tumbler>,                       // resident retraction roots — the tombstone set (active = audit ∖ this)
    dedup:      im::HashMap<DedupKey, im::OrdSet<Tumbler>>, // I0-class → addrs (audit; active-filtered at the check) — idem⊤ types only
    sup_fwd:    im::HashMap<Tumbler, im::OrdSet<(Tumbler /*new*/, Tumbler /*claim*/)>>, // BH2 old→{(new,claim)}; [K_sup] only (v1)
    home_count: im::HashMap<Tumbler, u64>,                 // BH4: home document → # homed links (the frontier index)
}
```

| Hint | Makes free | Common-case cost |
|---|---|---|
| `spanfilade` | overlap/stabbing for Observe (BH3), `match_links`, M8 | O(log n) insert per slot-span on apply |
| `type_class` | `L_K` slices, same-type grouping (L8) | one `CoverageClass` of `e₃` + set-insert on apply |
| `nullified` | active view = `links ∖ nullified`; resurrection (I2) | one root-insert when applying an `[R]` tuple |
| `dedup` | O(1) idempotent dedup on the write path (I1) | one `DedupKey` + set-insert on apply (**idem⊤ types only**) |
| `sup_fwd` | BH2 walk / `current` | insert only when applying a `[K_sup]` tuple |
| `home_count` | BH4 `age` in O(1) | `+1` per apply, keyed by `origin(addr)` |

**`CoverageClass` and the level-mismatch hazard.** Two endsets are the same type / the same I0-class iff their *coverage* is equal — never their span decomposition. M7 computes the class by iterating the readable endset spans. For **address-denoting endsets** (the managed surface: canonical encodings of address sets — every span unit-depth `(x,δ(1,#x))`, detected by `s == subtree_of(s.start())`), coverage equality reduces to the **≼-minimal antichain of denoted addresses** (I0a): iterate `addrs()`, drop any `x` for which some other denoted `y` has `is_prefix(y, x)`, compare as a set. This is exact and never faults — it is the dedup hot-path key. For **general content endsets** (MAKELINK's resolved I-extents, multi-span, mixed-length), M1's `canonical_key`/`normalize` *fault* on mixed-length input (`LevelMismatch`), so the class is computed **per endpoint-length partition** — partition `spans()` by `#start`, fold each level-uniform partition to a `SpanSet` (`to_spanset`), `canonical_key` it, assemble the per-length map.

```rust
#[derive(Clone, PartialEq, Eq, Hash)]                  // NOT Serialize: Extents wraps M1's non-Serialize CanonicalForm
pub enum CoverageClass {                                // (lives only in the skip registry/hints, so this is fine)
    Addrs(im::OrdSet<Tumbler>),               // ≼-minimal antichain — address-denoting (exact)
    Extents(im::OrdMap<usize, CanonicalForm>),// per-length canonical coverage — content extents (safe, see below)
}
#[derive(Clone, PartialEq, Eq, Hash)]
pub struct DedupKey { ty: CoverageClass, from: CoverageClass, to: CoverageClass }  // I0 = (cov(F),cov(G)) within [K]
```

The per-length partition is **conservative**: it can *over*-discriminate two content endsets whose equal coverage straddles lengths, never *merge* distinct ones. Over-discrimination is the safe direction for both type-matching (you under-match, never false-match) and dedup (you deposit a second tuple, never wrongly suppress). **Address-denoting endsets land in `Addrs` (exact)** — the entire managed surface *and* any MAKELINK type that resolves to a single content address; **only a multi-span or mixed-length content extent reaches `Extents`** (a MAKELINK type spanning content). **Reserved-class isolation:** `TypeRegistry::build` requires every `ReservedAddrs` entry to be element-level with `subspace ∉ {s_C, s_L}` (`ReservedSubspaceClash`), so a content link's type class (always within `s_C`) and a link-store address (within `s_L`) can never coverage-equal a reserved class — the no-collision guarantee Conflict §1 leans on (e.g. a content-typed link can never be misread into the `[R]` class and spuriously inserted into `nullified`). The exact cross-length class is left open (M1 provides no cross-length normal form) — see Open build decisions.

Because the dedup **`LockKey`** serializes `DedupKey.ty = CoverageClass(ty)` and the `Extents` variant wraps M1's non-`Serialize` `CanonicalForm`, `TypeRegistry::build` constrains every **idem⊤** type key to be address-denoting (`NonAddressDenotingKey`), so its class is the serializable `Addrs`. `DedupKey.from`/`.to` are always `Addrs` (single source address / `enc`'d to-set), and MAKELINK/idem⊥ types never take a dedup lock *and never compute a dedup key at all* (§1) — so no `Extents` class is ever serialized into a `LockKey`.

## Internal design

### 1. The store, recovery, and the engine plug

`apply_link(LinkRec::Emit{addr, value})` inserts `addr↦value` into `links` and folds **every** hint incrementally — O(log n) `im` operations throughout, all reading the endsets through `spans()`/`addrs()`: each slot's spans into `spanfilade`; `CoverageClass(value.type_slot())` into `type_class`; if that class is `[R]`, the to-root (`value.to_slot().addrs()` single) into `nullified`; **for an idem⊤ type only**, the `DedupKey` into `dedup` (an idem⊥ type — every MAKELINK content link, and any idem⊥ app relation — skips the dedup key entirely, since no dedup check ever reads it, sparing the multi-span `Extents` partition the key would otherwise force); if `[K_sup]`, the `old→(new,addr)` edge (both via `addrs()`) into `sup_fwd`; `home_count[origin(addr)] += 1`. It carries the genesis config — `reserved`, `decls` (`Arc`-shared, so "carrying forward" is a refcount bump, not a copy), and the rebuilt `registry` — forward unchanged (they are not records and never change). `apply_link` reads only `LinkState` + M1 arithmetic + `registry`, is deterministic and total, and is applied exactly once per committed record (M2 guarantees this — do **not** code it idempotent).

`rebuild_derived` runs once at load, before replay (serde having seeded the two `#[serde(skip)]` fields with their `Default`s on deserialize — an empty `TypeRegistry` and empty `Hints`, both immediately overwritten here): it first reconstructs `registry = TypeRegistry::build(reserved, decls)` from the deserialized authoritative config (a `.expect()` — the inputs passed validation at genesis), then recomputes `hints` entirely from the checkpointed `links` + `registry`. Because **all** hints are pure functions of `links`+`registry`, this is a single pass; and because the registry is reconstructed before replay, the post-checkpoint `apply_link` folds see it. Recovery is therefore *pure replay*: no undo log, no compaction for correctness; the only knob is M2's checkpoint cadence (it bounds the rebuild pass).

The engine assembles `World{ …, links: LinkState, … }`, implements `HasLinks`, `From<LinkRec> for Record`, and dispatches `Record::Links(x) => world.links().apply_link(x)`. M7 names neither `World` nor `Record`; its transact-ops are `impl<W: WorldState + HasLinks + HasM3 [+ HasM5]> LinkStore<W> where W::Record: From<LinkRec> + From<M3Rec> [+ From<M5Rec>]`.

### 2. Two write surfaces, one store (the central architecture)

The store holds links from **two disciplines that never unify** (Conflicts §1):

- **MAKELINK — the open content-link surface** (ASN-0043/0120). Resolves V-specs, admits multi-span endsets, admits ghost/unregistered types, applies **no shape gate** and **no idem dedup** (distinct links always — ML0). Seats the link in its home.
- **Emit_K — the managed typed-relation surface** (ASN-0086/0126/0128). Address-level, **shape-gated**, **idem-deduped per type**, `K ≁ R` rejected; **never seats**.

They share `links`, the spanfilade, every read path, and one internal `emit_core`. They differ only in admission (the gate) and in whether the *op* seats afterward (MAKELINK does; Emit_K/Nullify/assert_sup/editlink do not). A MAKELINK content link's type resolves to `s_C` I-addresses, whose coverage class can never collide with a reserved managed class (reserved type addresses lie outside `s_C`/`s_L`, §Core data model), so MAKELINK links never pollute the managed slices; and the behaviors degrade gracefully (`target_of` returns ⊥ on a non-single-address endset, BH2 reads single-address claims) if an app ever registered a managed type coverage-equal to a MAKELINK type.

**`emit_core` (shared)** — the single choke point, run inside one `transact`. Its bounds are `W: WorldState + HasLinks + HasM3` only (gate + `mint_link` + deposit `LinkRec`); it has **no `seat` step** and so needs neither `HasM5` nor `From<M5Rec>` — the seat is staged by MAKELINK itself, the lone `HasM5` caller, after `emit_core` returns. Any dedup **lock** is acquired by the public op *before* this transact (§3 step 1); `emit_core` does the **hoisted home check** and the in-txn active-view dedup **check** (§3 step 2). `|F|`/`|G|` below are `value.from_slot().len()`/`value.to_slot().len()`:

```text
emit_core(stg, home, value, gate) -> Result<Address, EmitCoreError>:
  require stg.working().m3().is_registered_document(home)                     // HomeNotRegistered — HOISTED ahead of every
                                                                             // gate/dedup short-circuit (enforced on a hit too, Conflicts §8)
  match gate:
    Open (MAKELINK / editlink successor):
        require !value.type_slot().is_empty()                                 // EmptyType (arity 3 guaranteed by caller)
    Managed (Emit_K / assert_sup / editlink claim):
        let K = CoverageClass(value.type_slot())
        require registry.registration(K).is_some()                           // (i) registered (NotRegistered)
        require K ≠ CoverageClass(reserved(Retraction))                      // K ≁ R (RetractionClass)
        require Sh-conf(reg.shape, |F|, |G|)                                 // (ii) span-count gate (ShapeViolation)
        if reg.idem: DEDUP-CHECK (§3 step 2, vs stg.working() active) — hit ⇒ return incumbent, stage NOTHING
    Retraction (Nullify):
        require registry.registration(CoverageClass(reserved(Retraction))).shape == Binary  // defensive (genesis-fixed)
        require Sh-conf(Binary, |F|, |G|)                                    // |F|=1, |G|=1
        DEDUP-CHECK (§3 step 2, idem⊤) — hit ⇒ return incumbent, stage NOTHING
  let (addr, m3rec) = stg.working().m3().mint_link(home)?                     // K.λ via M3 (home already known-registered; other MintError → Mint)
  stg.push(m3rec.into()); stg.push(LinkRec::Emit{addr, value}.into())        // deposit; NO seat, NO R here
  return addr
```

`Sh-conf` reads `shape(K)` from the registry and tests *span counts* (Unary `|G|=0`, Binary `|G|=1`, Multi `|G|<∞`; all require `|F|=1`) — never inferring shape from the tuple (a `(1,0)` tuple conforms under Unary *and* Multi). The gate adds preconditions only and never alters `value` (**effect-identity** — the ASN-0126 `π` bridge): do not "normalize on the way in." Both `Open` callers supply an arity-3 value (MAKELINK builds `[e₁,e₂,e₃]`; `editlink` pre-checks `successor.arity()==3`), so `emit_core` carries no arity guard and the store holds only arity-3 links.

**`emit_core` error mapping.** It returns `EmitCoreError { HomeNotRegistered, NotRegistered, ShapeViolation, RetractionClass, EmptyType, Mint(MintError) }`. `HomeNotRegistered` originates at the **hoisted home check** (and, defensively, at `mint_link`); every other `MintError` rides `Mint`. Each public op maps it:

- **MAKELINK** (`Open`): maps `emit_core`'s `EmptyType→EmptyTypeResolution`, `Mint→Mint`, `HomeNotRegistered→HomeNotRegistered` (the `Managed`/`Retraction` branches are unreachable); and — since MAKELINK, not `emit_core`, stages the seat — maps `stage_seat_link`'s `SeatError→Seat` directly.
- **emit** (`Managed`, no seat): `HomeNotRegistered/NotRegistered/ShapeViolation/RetractionClass/Mint` pass through to the like-named `EmitError` variants; `EmptyType` unreachable (managed `e₃ = ty` non-empty by `T_admissible`).
- **nullify** (`Retraction`): `HomeNotRegistered→HomeNotRegistered`, `Mint→Mint`; the gate variants are defensive (the `[R]` type is genesis-fixed Binary); P-tgt is checked in `nullify` itself (`BadTarget`).
- **assert_sup / editlink-claim** (`Managed`, K_sup): `HomeNotRegistered→HomeNotRegistered`, `Mint→Mint`; `NotRegistered/ShapeViolation/RetractionClass` are unreachable for the registry-fixed K_sup. editlink's successor (`Open`): `EmptyType→IllFormedSuccessor`, `Mint→Mint`.

**MAKELINK** wraps `emit_core` with the resolver, resolving `ρ` **inside** the transact off the txn base (so the whole operation linearizes at its commit — ASN-0134's single linearization point; ML8 keeps the endsets valid either way, but this removes the read-write gap), and **stages the seat itself** after `emit_core` returns the address:

```text
makelink(home, R₁, R₂, R₃):                                  // Rᵢ : Vec<VSpec>, VSpec{ source, span:(start,width) }
  transact([M3State::link_lock_key(home)], |stg| {           // home minted on the LINK frontier ⇒ link_lock_key (Conflicts §7)
     let m3 = stg.base().m3(); let m5 = stg.base().m5();
     require m3.is_registered_document(home)                                   // HomeNotRegistered
     for each Rᵢ, each VSpec{source: d_j, span: σ_j}:                          // wf(R,Σ) by CONCRETE component tests:
        require m3.is_registered_document(d_j)                                 //   d_j ∈ dom(M)
              ∧ #σ_j.start() == 2 ∧ σ_j.start().get(1) == s_C                  //   depth-2 CONTENT V-position
              ∧ #σ_j.width() == 2 ∧ σ_j.width().get(1) == 0                    //   ordinal displacement δ(n,2)   → else IllFormedSpec
     eᵢ = Endset::from_spans(⋃_j { run.iextent() : run ∈ m5.resolve(d_j, σ_j) })  // ρ as content I-extents — readable spans off the txn BASE
     require !e₃.is_empty()                                                    // EmptyTypeResolution (ML6)
     let addr = emit_core(stg, home, Link::new([e₁,e₂,e₃]).unwrap(), Open)?    // arity 3 by construction; deposits, no seat
     stg.push(stage_seat_link(stg.working().m5(), home, addr)?.into())         // K.μ⁺_L via M5 — the seat (no R, J-LV)
     Ok(addr)
  })
```

Recording M5's `resolve` runs lifted through the public, total `Run::iextent()` *as* the endset spans makes the **coverage-exactness recovery equation** (ML1: `coverage(eᵢ) ∩ dom(C) = ρ`) hold by construction — M5's runs trace exactly allocated content and never over-reach the frontier, cross-origin runs arrive un-coalesced (M16), and `iextent` is the level-uniform element-level I-extent. The `wf` checks are *concrete component tests* on the V-span — `subspace(u_j)=s_C` of ASN-0120 is the V-position's first component `start.get(1)`, **not** M1's `Address::subspace()` (which needs `zeros=3` and returns `None` for a depth-2 V-position, so a naïve builder would reject every spec); the length checks `#start==2`/`#width==2` precede the `get(1)` indexing so the 1-based `Tumbler::get` never panics. These mirror M5's `resolve` precondition and produce `IllFormedSpec` *rejections*, distinct from the silent ⟨⟩ that `resolve` returns for a non-content/malformed span. The held key is `link_lock_key(home)` — `emit_core`'s `mint_link(home)` advances the link frontier, so the held lock and the advanced frontier are byte-identical (M3's contract); a content key would not serialize MAKELINK against `emit`/`assert_sup`/`nullify` at the same home (colliding link addresses) under a multi-applier realization. MAKELINK touches **no R** (J-LV), allocates content nowhere (J0 vacuous), and seats exactly one link V-position.

**Emit_K** wraps `emit_core` with the value construction: `value = Link::new([enc(&[from]), enc(to), ty.clone()]).unwrap()` (F single-address, G the to-set encoding, e₃ = `ty` verbatim), then `emit_core(stg, home, value, Managed)`. The public op computes the `dedup_key` from its args **before** the transact and supplies `[dedup_key, link_lock_key(home)]` (idem⊤) or `[link_lock_key(home)]` (idem⊥) to `transact` (§3).

**editlink** is one M2 composite over **two home alloc keys** — `transact([M3State::link_lock_key(d_s), M3State::link_lock_key(d_a)], …)` — inlining two `emit_core` calls; it **cannot** call the public `assert_sup` (itself a `transact`: M2 is non-reentrant — a nested write deadlocks — and a second `transact` would forfeit EL7 atomicity). The residence/arity preconditions and the **DC** guard run *inside* the closure against `stg.base()` (DC's `[K_sup]`-witness check is a base-state read):

```text
editlink(original, successor, d_s, d_a):                      // successor : Link, supplied (M10 built it via Link::new)
  transact([link_lock_key(d_s), link_lock_key(d_a)], |stg| {  // two home alloc keys only — no dedup key (claim key carries fresh a')
     let base = stg.base();
     require base.m3().is_registered_document(d_s) ∧ base.m3().is_registered_document(d_a)  // HomeNotRegistered
     require original ∈ base.links()                                                        // OriginalNotResident
     require successor.arity() == 3 ∧ !successor.type_slot().is_empty()                     // IllFormedSuccessor (arity-3 store)
     require DC(successor):  CoverageClass(successor.e₃) ≠ CoverageClass(reserved(Retraction))  // DcViolation
                          ∧ (CoverageClass(successor.e₃) == CoverageClass(reserved(Supersedes)) ⟹
                               schema-conforming witnesses ∈ base.links())                  // unit-depth single-addr F/G, endpoints resident, irreflexive
     let a' = emit_core(stg, d_s, successor, Open)?           // born unseated; content type idem⊥ ⇒ no dedup deposit
     let b  = emit_core(stg, d_a,                             // claim: "original superseded by a'"
                        Link::new([enc(&[original]), enc(&[a']), reserved(Supersedes)]).unwrap(),
                        Managed)?                             // claim dedup-CHECK is a guaranteed miss (fresh a') ⇒ lock-free (§3)
     Ok((a', b))
  })
```

The claim's dedup is **vacuous and lock-free** here: its `DedupKey` carries the freshly minted successor `a'` (unknowable before the closure, and M2 takes `keys` up front), so the active check is a guaranteed miss — no claim dedup `LockKey` is needed, only the two home alloc keys. Both writes commit atomically (EL7); the original is untouched (L12). The DC guard is what keeps editlink discipline-preserving and therefore chainable; rejecting an `[R]`-typed successor stops step 1 from silently nullifying its to-set, and schema-conforming a `[K_sup]`-typed successor keeps the supersession discipline.

**M10 builds the `successor: Link` itself** (ASN-0125 takes a pre-formed `ℓ'`). For a content successor it resolves V-specs through M5's `resolve`, lifts each run with `Run::iextent` to a readable `Span`, forms the endsets with `Endset::from_spans` (any address-denoting slot — e.g. a type address — via `enc`), and assembles the three slots with `Link::new` (arity 3). The resolution may be taken off **any prior snapshot**, since recorded I-addresses are permanent (ML8/EL0) and need not be re-resolved at edit time — so the builder is never left guessing how to form a content successor.

### 3. De-duplication and the M2 keyed critical section

Idempotence is a **computed equivalence at the surface, never stored identity** (I1) — the store stays pluralistic underneath; a hit returns the incumbent's address and *commits nothing*. The dedup **lock** and the dedup **check** are split across the transact boundary, because `emit_core` runs *inside* an already-open `transact` and cannot itself acquire keys:

1. **The public op acquires the dedup lock — *before* the transact.** For an idem type, the op computes `DedupKey = (CoverageClass(ty), Addrs({from}), Addrs(to))` from its *arguments* (the from/to addresses are in hand; `CoverageClass(ty)` reads `ty`'s spans, address-denoting by the idem⊤ build precondition ⇒ `Addrs`), serializes it into a `LockKey` (M7's space tag + the minimal antichains), and supplies it alongside the home alloc key: `transact(&[dedup_key, M3State::link_lock_key(home)], …)`. Same I0-class ⇒ same `LockKey` ⇒ M2 serializes the check-and-deposit (I1a/I4); different I0-class ⇒ no contention. This is the only cross-home synchronization point, partitioned **by I0-class, never by home** — sharding dedup by home would let two same-class different-home emits both miss.
2. **`emit_core` performs the active-view check — *inside* the txn** (after the hoisted home check). It recomputes the same `DedupKey` from `value` (identical to the op's, by construction) and looks up `dedup[key]` filtered by `∉ nullified` off `stg.working().links()`. Several active matches (only off a raw path) → return the T1-least (deterministic). One → return it, stage nothing (zero-step; M2 returns the base `Seq`). None → fall through and deposit.

Reading the *active* view (I2) is what gives **resurrection**: a nullified tuple is invisible to dedup, so re-emitting lands at a fresh address — the audit trail keeps both. MAKELINK and idem⊥ app types skip both the lock and the check (only the home key) and never compute a `DedupKey` at all (§1); the editlink claim skips the dedup **lock** too — its `DedupKey` carries the freshly minted successor `a'` (unobtainable as a `transact` key before the closure), and the in-txn check is a guaranteed miss, so editlink supplies only the two home alloc keys (§2).

### 4. Retraction, the nullified set, and the active view

`nullify(d_retr, target)` is `emit_core` of an `[R]` tuple with canonical from-fill `enc({d_retr})` and unit-depth to-span `enc({target})`, run through the **Retraction** gate (which requires the genesis-fixed `[R]` Binary type and the `|F|=|G|=1` span counts), idem⊤ — so re-retracting the same target from the same document dedups. The public op computes `dedup_key` (the `[R]` class, from=`{d_retr}`, to=`{target}`) before the transact and supplies `[dedup_key, M3State::link_lock_key(d_retr)]`. It checks **P0** (`is_registered_document(d_retr)` → `HomeNotRegistered`) and **P-tgt** as a rejecting precondition in `nullify`'s closure against `stg.base()`: `target` is a resident link (`target ∈ stg.base().links()`) **or** `target` equals nullify's own would-be fresh emitter. M7 computes that would-be emitter without reading M3's frontier: `inc^{home_count[d_retr]}([d_retr.0.s_L.1], 0)` — the first link V-position `[d_retr.0.s_L.1]` (= `elem_addr(ElemPos{doc: d_retr, subspace: s_L, ordinal: 1})`) sibling-advanced `home_count[d_retr]` times via M1's `inc`, equal to `mint_link(d_retr)`'s output by construction (FrontierUnification; §Conflicts 7; `home_count[d_retr] == 0` ⇒ the first emission itself). Else `BadTarget`. Public `emit` rejects `K ~ R` (the Managed gate's `K ≠ [R]`), so `nullify` is the *sole* `[R]`-writer.

`nullified` is a monotone tombstone set of **resident retraction roots**. Under the unit-depth + antichain discipline, R-Scope makes each retraction nullify exactly one resident link, so "is `a` nullified?" is a plain `nullified.contains(a)` (a prefix-trie variant covers the off-surface range case — Open decisions). The **active view of any slice is `audit ∖ nullified`**, derived at query time; the spanfilade and `type_class` index the *audit* slice (append-only, never delete on nullification), and `View::Active`/`Default` filters results by `nullified`. Only `dedup` consults active (above). This keeps every index a pure append-only hint.

**Sterilization is unreachable through M7's surface** (DR theorem): `nullify`-only-via-the-wrapper + unit-depth to-span + P-tgt-rejecting makes the wp's C3 conjunct vacuous — no pre-existing retraction can ever cover a later fresh emitter address (antichain + freshness). Born-nullified tuples arise only from a deliberate self-emit retraction, and that falls out of the ordinary `audit ∖ nullified` derivation with no special gate.

### 5. Supersession and the BH2 walk

`assert_sup(home, old, new)` emits a `[K_sup]` claim with **F = enc({old}), G = enc({new})** (slot convention resolved in Conflicts §2 — F holds the *old/superseded* link, edges run old→new) through the Managed gate (idem⊤). Like `emit`, it computes `dedup_key` from (`[K_sup]`, {old}, {new}) before the transact and supplies `[dedup_key, link_lock_key(home)]`. It requires `is_registered_document(home)` (P0 → `HomeNotRegistered`), both endpoints resident (`old, new ∈ links` → `EndpointNotResident`), and `old ≠ new` (→ `SelfSupersession`, Df-DISC(ii) irreflexivity). `sup_fwd` maps `old → {(new, claim_addr)}` over the audit `[K_sup]` slice. `succs(old)` returns the `new`s whose `claim_addr ∉ nullified` (operative `succ_o`). `chain` is a bounded iterative walk over `succs` with a visited-set, halting at **sink** (no succ), **branch** (≥2 succs), or **cycle** (repeat) — the finite link set is the termination bound; `tip` returns `Sink(head)` or `Indeterminate` at branch/cycle.

v1's `sup_fwd` (and the whole `succs`/`chain`/`tip`/`current` walk family) serve **only** the shipped `Supersedes` class: `succs(ty, x)`/`chain(ty, x)`/`tip(ty, x)` validate `CoverageClass(ty) == CoverageClass(reserved(Supersedes))` and return empty for any other `ty` (a second registered BH2 Binary type's walk is a deferred Open decision — the general path would scan `type_class[ty]` active with `sup_fwd` as the `[K_sup]` accelerator). `current(y)` is hardwired to `[K_sup]`.

`current(y)` is BH2 generalized to sets: the operative sinks reachable from `y` via `succ_o`, returned **entire** as `Vec<CurrentMember>` — linear→1, forked→≥2, mutual-supersession standoff→0, all legitimate. Each `CurrentMember` carries the sink address, its **own** activity status (a member can be a current sink yet itself nullified — EL14e), and its **supporting claim set**: the addresses of the operative `[K_sup]` claims whose `new` endpoint **is this sink** — the inbound supersession edges that establish it as a current reading (their homes recoverable by `document_of` — EL8b; for a `y`-is-its-own-sink member with no inbound operative edge, the set is empty). This discharges EL14d's *disclosure, not decision* contract: M7 hands the reader the entire set with attribution so the reader applies its own narrowing policy. M7 never fabricates a single "latest." A *per-home* latest is recoverable (claims homed on one chain are T1-ordered, EL13); a cross-home latest is not a state function and M7 does not invent one.

### 6. The spanfilade and the matcher (the M7↔M8 seam)

The spanfilade answers the one primitive both Observe and M8 stand on: **`stab(i, Q)` = link addresses whose slot-`i` endset coverage overlaps `Q`** (interval-overlap / stabbing), `Q` an M7-readable `Endset`. Per slot (the three standard slots — **exhaustive**, since the store holds only arity-3 links, §Core data model), it maps covered I-extents to the link addresses covering them; M1's **`classify_spans`** decides overlap (`Separated` ⟹ none) — never `intersect`, which gates on level and `Err(LevelMismatch)`es on the mixed-length endpoints that M5's `resolve` runs (lifted via `iextent`) routinely produce. The baseline is a **brute-force scan** of `links` (trivially correct, O(n) — the bootstrap default, with the `SlotIndex` hint empty, reading each endset's spans through `spans()`); the scale structure is an interval/segment index keyed in tumbler order (concrete shape = Open decisions). It is rebuilt by replay — never persisted transactionally — so durability (the journal) is decoupled from query performance.

Two combiners sit on `stab`, and to remove the double-implementation noted as the design's softest seam, **both live in M7** (M8 becomes pure presentation):

- **`match_links(constraints, view)`** — findlinks' core: per constrained slot, OR (`stab`-union, which already unions overlap across the constraint endset's spans) over the slot's query spans, then AND (intersect by link identity) across slots. M8's findlinks = this + cursor/count/window.
- **`observe(K, F̂, Ĝ, view)`** — Observe's *subset* match (`F̂ ⊆ coverage(F) ∧ Ĝ ⊆ coverage(G)`, distinct from findlinks' overlap): start from candidates `type_slice(K, view)`, optionally prefiltered by `stab(1, &enc(F̂))` / `stab(2, &enc(Ĝ))` (overlap is a sound *superset* of membership); then **exact-filter** each candidate tuple by testing every pattern address — `tuple.from.denotes(a)` for all `a ∈ F̂` and `tuple.to.denotes(a)` for all `a ∈ Ĝ` (`Endset::denotes` decides `a ∈ coverage(·)` as `∃ s ∈ spans : s.contains(a)`; for address-denoting endsets this is the `∃ x ∈ addrs(F): x ≼ a` prefix test). `stab` overlap **alone over-matches** — a pattern that is a proper *ancestor* of a stored endset address overlaps it while `a ∈ coverage(F)` is false (e.g. `F̂ = {[d.0.s_L]}` would wrongly return every tuple homed at `d`), so `stab` is **only** a prefilter and the membership test is authoritative. Assemble surviving `Tuple`s. Patterns range over all of `T` (ghost addresses welcome — the `denotes` membership test is total). `View::Default` is coerced to `Active` (raw Observe never filters — ASN-0128).

M8 reads `stab`/`match_links`/`type_slice`/`is_active`/the BH3 family across the existing `M8→M7` edge; M9 reads `observe` + BH1–BH4 — both served entirely from M7's own indexes, so **no `M7→M8` edge** and **no `M9→M8` edge** arise.

### 7. Behavior atoms BH1, BH3, BH4; default predicates; raw reads

- **BH1 read-filter** (Unary types): v1 ships exactly one BH1 type (`Retired`). `is_filtered(a)` tests membership in its active filter slice (prefix-containment over its roots); `View::Default` rewrites `members(K')`/`targets_of` for any `K' ≠ Retired` by subtracting the filtered results — result-side only, computed lazily against the filter roots (never materialize the filtered subtree). The general multi-BH1 form unions over the BH1 set `Φ` *excluding the queried* `K'` (ASN-0128's `J ≠ K'`); with a single shipped filter that reduces to the single subtraction. **Restriction:** the type-less `is_filtered` is correct only while exactly one BH1 type is registered; a second BH1 registration requires `is_filtered` to take the queried `K'` to honor the `J ≠ K'` exclusion (deferred — Open decisions). Filter-vs-walk/reverse interaction (OQ1) is left at the active reading.
- **BH3 typed-reverse-lookup** (Binary): the spanfilade *is* the reverse index — no separate structure — but, exactly as `observe` (§6), `stab` overlap is only a **prefilter** and an exact-membership test is authoritative (a coarse document-level or ghost argument over-matches). `sources_to(target)` = `stab` on the **to**-slot for `enc(&[target])` (prefilter), then exact-filter the candidates by `G.denotes(target)` (coverage match, per AM's reverse-lookup rule), collecting each survivor's `F.addrs()`; `target_of(source, K)` = `stab` on the **from**-slot for `enc(&[source])` (prefilter), then exact-filter by `source ∈ F.addrs()` (denotation match, per AM's source-vertex rule), returning the unique surviving candidate's single denoted target `G.addrs()` (⊥ on none/several, or on a unique candidate whose G is not single-address-denoting); `targets_keyed(source)` joins `target_of` across *every* BH3-registered Binary type into a `CoverageClass→addr` map (M9 cannot compose this itself — the registry is private to `LinkState`, so M9 cannot enumerate the BH3 types). ASN-0125's archival `in(y)/out(x)` (M8) compose these.
- **BH4 age-staleness** (idem⊥ types): `age(a) = home_count[origin(a)] − ordinal(a)` — the chain index off the address (`ordinal`), the frontier off M7's own homed count (equivalent to M3's frontier by construction, so no upward read — Conflicts §7). `stale(h)` scans the active slice; `retract_stale(d_retr, ty, h)` snapshots `stale(h)` at entry and issues one `nullify(d_retr, target)` per stale target — **not** one atomic transaction. On full success it returns the `Vec<(Address, Seq)>` of emitter addresses and commit seqs (an already-nullified target dedups to a zero-step hit, contributing its incumbent address and the base `Seq`); on the first `TxnError` it returns `Err`, leaving earlier nullifies **committed and durable** (no rollback — the store is append-only) — a re-run is safe, since already-nullified targets dedup to no-ops. No global counter, no clock (ordinal time only).
- **Default predicates** `is_k`/`members`/`targets_of`: `is_k(a)` is exact coverage-*membership* over the **active** K-slice — `∃ x ∈ members(ty, Active): x ≼ a` for address-denoting types (the D2 bridge), `∃ active tuple: tuple.from.denotes(a)` in general — **never** a `stab` overlap call (an ancestor pattern would over-match). `members`/`targets_of` return denoted addresses (`F.addrs()`/`G.addrs()`) and alone honor `View::Default` (active ∖ filtered); `is_k` is never filtered (BH1 Rewrite scope).
- **READLINK** = `links.get(a)` copied out, total, returns `None`(=⊥) on absence — *recorded, never resolved*, never dereferencing covered links (RL4/RL6); the returned `Link` carries readable endsets (RL1/RL2). The structural screen and ⊥-permanence caching of ASN-0111 are optional pre-probe fast paths; the persistent map is already the positive cache (immutability ⇒ never stale). **FOLLOWLINK** = slot lookup with the post-lookup arity bound, returning the recorded slot's coverage as a `SpanSet` (`to_spanset` of the verbatim endset — F1/F3 by construction), `Ok(empty)` vs `Err` keeping ⟨⟩≠⊥.

## Invariants & contracts

**By construction** (fall out of the append-only `links` map + M3's minting + M1's algebra):

- **Permanence / immutability** of every link value and address — L12 (ASN-0043), R2 (ASN-0086), C0/L12 (ASN-0093), ML7 (ASN-0120), RL5/RL6 (ASN-0111), F5 (ASN-0114), EL0 (ASN-0125). *Where:* no update/delete record exists; `apply_link` only inserts.
- **Uniqueness / freshness / flat prefix-antichain** — L11a (0043), R0/R0a/R1 (0086). *Where:* M3 mints monotone home-scoped siblings; M7 never chooses an address.
- **Arity-3 store** — every creation op realizes arity exactly 3 (MAKELINK standard triple, Emit_K, supersession claims; `editlink` rejects a non-arity-3 successor). ASN-0043 L3's N≥3 is a *type capacity* `Link::new` admits but no op exceeds; the spanfilade's three slots are exhaustive, and `type_class`/`type_slice`/`observe` satisfy ASN-0086's `|Σ.L(a)|=3` restriction without an explicit filter.
- **Ownership derivability** (home = address projection) — L2 (0043). *Where:* M1's `document_of`/`origin`.
- **Subspace disjointness** (links in `s_L`, never colliding with `s_C` content) — L1d/L14 (0043), SD/R4 (0093/0086). *Where:* M3 keeps links in `s_L`; M7 stores only what M3 mints there.
- **Type-by-coverage / ghost permission** — L8/L9 (0043), RL3 (0111). *Where:* matching computes `CoverageClass` over the readable endset spans, never dereferences a type address.
- **Endset order-independence & slot distinction** — L5/L6 (0043). *Where:* `Endset` is read by membership (`denotes`/`addrs`, no positional span accessor), `Link = im::Vector` is positional.
- **Audit monotonicity, retraction stability, resurrection** — R3/R6a (0086), I2 (0128). *Where:* `nullified` only grows; dedup reads active.
- **Registry & idem stability** — P1/P2 (0126), R1/R2 (0128). *Where:* registry sealed at genesis; no mutator exists.
- **No sterilization through the surface** (DR) — ASN-0128. *Where:* `nullify`-only wrapper + unit-depth + P-tgt-rejecting.
- **Effect-identity** (the gate deposits exactly what an ungated emit would) — ASN-0126 `π`. *Where:* `emit_core` never mutates `value`.
- **Coverage-exactness of MAKELINK endsets** (ML1) — *Where:* recording M5's `resolve` runs' `iextent` spans verbatim, inside the txn.

**By active enforcement** (M7 must guard):

- **Home existence** (L1a/0043, ML0/0120, P0): `is_registered_document(home)` (and each `d_j`) before any emit — at `makelink`/`emit`/`nullify`/`assert_sup`/`editlink` entry (the latter against `stg.base()`).
- **Home-registration even on a dedup hit** (deliberate divergence from ASN-0128 I1): `emit_core` checks `is_registered_document(home)` **ahead of the dedup short-circuit**, so an unregistered-home emit is rejected on every path — miss *and* hit. Callers cannot observe the hit/miss branch, so this unconditional check is what makes the contract portable; it strengthens I1's branch-local precondition into an M7-enforced guard (Conflict §8).
- **Type-endset non-empty** (L3/0043, ML6/0120): `e₃ ≠ ∅` (`!type_slot().is_empty()`) — MAKELINK rejects empty type resolution; managed `e₃ = K` is non-empty by `T_admissible`.
- **Shape conformance** (P3/0126, |F|=1, arity 3): `Sh-conf` in the Managed/Retraction gates (Emit_K/Nullify — *not* MAKELINK).
- **Dedup identity = coverage** (I0/I1, 0128): the dedup key/index compare `CoverageClass`, never value; idem-uniqueness (I1a) needs surface-routing + the M2 dedup `LockKey` (acquired by the public op pre-transact, §3).
- **`[R]` / reserved-class reservation** (R-C1, registry): `TypeRegistry::build` rejects any app key coverage-equal to a shipped class or another app key.
- **Reserved-class isolation** (Conflict §1): `build` requires every `ReservedAddrs` entry element-level with `subspace ∉ {s_C, s_L}` (`ReservedSubspaceClash`), so content-link type classes (in `s_C`) and link addresses (in `s_L`) never coverage-collide with a reserved class.
- **Idem-key denotation** (dedup serializability): `build` requires every idem⊤ type key address-denoting (`NonAddressDenotingKey`), so the dedup `LockKey` (serializing `CoverageClass(ty)`) has bytes (`Addrs`, not the non-`Serialize` `Extents`).
- **Unit-depth retraction + P-tgt** (R-Scope/DR, 0128): `nullify` writes only `{(target,δ(1,#target))}` and rejects a non-resident/non-self target (the would-be self emitter computed via M7's own `home_count` + M1 arithmetic).
- **Supersession schema** (Df-DISC, ASN-0125): `assert_sup` rejects `old == new` (`SelfSupersession`) and a non-resident endpoint (`EndpointNotResident`); `editlink`'s DC guard rejects a `[R]`-typed successor and a schema-non-conforming `[K_sup]` successor (`DcViolation`), and rejects a non-arity-3 successor (`IllFormedSuccessor`).
- **Observe is exact membership** (ASN-0086): `observe`/`is_k`, and the BH3 reverse family, test `⊆ coverage(·)` / exact denotation via `denotes`/`addrs`/prefix, using `stab` overlap only as a prefilter — never as the match.
- **Recovery** of all indexes: `rebuild_derived` rebuilds `registry` from `reserved`+`decls`, then every hint from `links`+`registry`.

**Discharged elsewhere (flag at the seam):** **Non-transcludability** (L14a, ASN-0043) — M7's *only* duty is keeping links in `s_L`; the exclusion of link addresses from V-position images lives in **M5**'s content-side referential-integrity check. Provenance R is M5's; M7 appends none.

## Dependencies & seams

**Upstream calls:**

- **M1** — pervasive: `Tumbler/Address/Span/SpanSet/CanonicalForm`. M7's `Endset` is a newtype over M1's **readable** `Span` (`start()/width()/reach()/contains()`), so all endset reads (`spans`/`addrs`/`denotes`/overlap) are M7-local span iteration — **M1's `SpanSet` is never *stored* as an endset** (it is read-opaque). M7 uses: `subtree_of`/`from_endpoints` to build unit-depth and I-extent spans and to test address-denotation (`s == subtree_of(s.start())`); `Span::contains` for `denotes` (`∃ s : s.contains(t)`); `classify_spans` for spanfilade overlap (never `intersect` — it faults on the mixed-length endpoints M5's runs routinely yield); `is_prefix` for the ≼-minimal antichain, nullified-root tests, and `is_k`/`observe`/BH3 membership; `canonical_key`/`CanonicalForm` for the `Extents` coverage-class partition (the **only** place an endset is folded to a `SpanSet`, per level-class); `classify`/`subspace`/`elem_addr`/`inc`/`document_of` for wf checks, `origin`/home, the reserved-isolation `subspace` test, and the BH4/P-tgt frontier arithmetic. (M1 exposes no `coverage` function — coverage is the query-time `denotes` projection.)
- **M2** — `transact(keys, f)` for every write (one `transact` per op, composites staging M3+M7+M5 records); `snapshot` for every read; the dedup `LockKey` supplied by the *public op* to the keyed critical section; `apply_link` plugged via `WorldState`; index rebuild via `rebuild_derived`. M7 contributes its own `Space` tag for the dedup `LockKey`; namespace alloc keys come from M3's `link_lock_key`.
- **M3** — `mint_link(home) → (Address, M3Rec)` and `M3State::link_lock_key(home)` inside every emit composite (stage the `M3Rec`); `is_registered_document` (home/spec preconditions). The frontier is M3's; M7 reads no M3 state for BH4 (it derives the frontier from its own `home_count`).
- **M5** — `resolve(d_j, span) → Vec<Run>` for MAKELINK's V→I endset construction: M7 lifts each run with the public, total `Run::iextent()` to a **readable** `Span` and forms the endset via `Endset::from_spans` (read off the txn base; the resulting content-extent class is computed per level-class). (M7 does **not** use M5's `resolve_coverage`, whose `SpanSet` result M7 could not read.) Also `stage_seat_link(&M5State, doc, link) → M5Rec` (the semantics-blind home seating, staged by MAKELINK *after* `emit_core` — the `M7→M5` edge with no return). M7 never reads link semantics back from M5 and never resolves anything itself.

**Build precondition** — `LinkState` checkpointing needs the `im` crate's `serde` feature (for `OrdMap`/`Vector`/`OrdSet`) and serde's `rc` feature (for the `Arc<ReservedAddrs>`/`Arc<Vec<TypeDecl>>` config); `Link`/`Endset`(newtype over `im::Vector<Span>`)/`Tumbler` are all `Serialize`/`DeserializeOwned`. `TypeRegistry` and `Hints` impl `Default` so serde can seed the `#[serde(skip)]` fields (replaced by `rebuild_derived` before replay).

**Downstream seams (make these explicit so M8/M9 build against them):**

- **→ M8** (`M8→M7` edge): `stab(i, Q, view)` and `match_links(constraints, view)` — **the query `Q`/constraint regions are M7's readable `Endset`** (M8 builds them via `enc` over resolved I-addresses, or `Endset::from_spans`), so M7 can iterate the query spans for overlap; plus `type_slice(K, view)`, `is_active`/`is_nullified`, the BH3 reverse family, and `readlink` — M8 layers cursors, counting, windowed pagination, projection (via M5's `project`), RETRIEVEENDSETS, and archival `in/out` (composing BH3) on top. M8 owns no index and writes nothing.
- **→ M9** (`M9→M7` edge, including writes): the full PL read surface — `observe` + BH1–BH4 + `is_k`/`members`/`targets_of` — all from M7's own indexes (so M9 needs no M8 dependency); and the gated write path — `emit(home, ty, …)` for `register_pred`/`certify_pd_stable`, and `emit`/`nullify` for reactive rule fires. M9 obtains the type endset via `LinkState::reserved_type(ShippedType::PredDef|PredStable)` read off a snapshot (the registry lookup is internal; `reserved_type` is the public read). The `pdef`/`pd_stable` reserved classes sit in the genesis registry: M9 coordinates their **addresses** via `ReservedAddrs` *and* their `Unary/⊤/{}` registrations — both are M7↔M9 build-time agreements, not pinned by any digested note.
- **→ M10**: the transact-driving ops in §C/§D, each returning `(…, Seq)` post-commit; M10 surfaces `TxnError::Rejected(E)` as typed rejections. M10 forms an editlink content successor via M5's `resolve` + `Run::iextent` + `Endset::from_spans`/`enc` + `Link::new` (off any prior snapshot — ML8/EL0; §2).
- **→ engine**: `LinkState` slice, `LinkRec` record, `HasLinks` accessor, `apply_link` fold, `genesis(reserved, decls)`, `rebuild_derived`.

## Conflicts resolved

1. **MAKELINK's multi-span endsets vs the shape gate's `|F|=1` (ASN-0120 vs 0126/0128).** ASN-0126 OQ6 itself defers multi-span sources, and ASN-0120 admits them. **Resolution: two write surfaces, one store.** MAKELINK is the *open* content-link surface (wf + type-nonempty, multi-span, ghost types, no dedup, seats); Emit_K is the *managed* typed-relation surface (shape-gated, idem, `K≁R`, no seat). They share `links`, the indexes, and `emit_core`; only admission and (for MAKELINK) the seat differ. **Managed types occupy reserved coverage classes whose type addresses lie outside `s_C`/`s_L`** (a `build` precondition, `ReservedSubspaceClash`); **MAKELINK types resolve into `s_C`**; so the populations never coverage-collide, and behaviors degrade gracefully (`target_of`→⊥) if an app ever registered a managed type coverage-equal to a MAKELINK type.

2. **Supersedes slot direction (ASN-0125 Df-DIR vs ASN-0128 S2).** ASN-0125 puts the *new* link in F ("F replaces G"); ASN-0128 puts the *old* in F ("F is superseded by G; edges old→new"). Both agree the *edge* runs old→new and the walk goes version→head; they disagree only on which slot holds old. **Resolution: adopt ASN-0128 (F = old/superseded, G = new/superseding)** — it is the note where BH2/the walk is defined, and the decomposition endorses old→new so that `succs(old)=new` is the natural forward step and `tip` is the head. `assert_sup(home, old, new)` keeps its caller-facing meaning ("old is superseded by new") and maps `old→F, new→G` internally. This overrides ASN-0125 Df-DIR's labels.

3. **`e₃ ≠ ∅`: store invariant vs endset type (ASN-0043 L3 vs ASN-0043 Endset).** ASN-0043's `Endset` definition (`Endset = 𝒫_fin(Span)`) admits `∅` as a valid endset, so the `Link` *type* admits `e₃=∅`; ASN-0111 in fact **affirms** L3's non-empty type slot for the read (RL1(a)/(c) — a usable type endset is always returned). L3 is a *store* invariant. **Resolution:** `Link::new` enforces only the arity floor (≥ 3 — ASN-0043 L3's *capacity*, of which creation realizes only 3, §Core data model); `e₃ ≠ ∅` is enforced at the *write boundary* (`emit_core`'s `Open`/`Managed` gate, MAKELINK's `ML6`), so READLINK's verbatim disclosure inherits a non-empty type for free without the type over-constraining.

4. **MAKELINK "distinct links always" (ML0) vs idempotent dedup (ASN-0128).** **Resolution:** dedup is *per type's idem flag*. The store never merges (NonInjectivity L11b — distinct addresses always); the idem *surface* returns an incumbent *without depositing*. Content-link types are idem⊥ (every MAKELINK deposits fresh — ML0 honored, and `apply_link` computes no dedup key for them at all, §1); only the shipped/registered idem⊤ types dedup. The two compose without contradiction.

5. **Raw read vs bundled resolution (ASN-0111/0114).** Green bundled V-resolution into its link reads; the spec de-bundles. **Resolution:** READLINK/FOLLOWLINK are *raw* reads off `links`, taking no document handle and consulting no arrangement; V-projection (and the silent-drop it entails) lives in M8/M5. This is the boundary that makes orphaned/ghost links readable.

6. **Spanfilade placement and the double-implemented combiner (the decomposition's softest seam).** **Resolution: the spanfilade *and* the matchers (`stab`, `match_links`, `observe`) live in M7**, co-located with the link writer; M8 is pure discovery presentation over them. This restores ASN-0086's indexed Observe on M9's hot polling path and removes the duplicated per-slot-match + combiner.

7. **Frontier ownership for BH4 (M3 mints, M7 needs the frontier).** **Resolution:** M7 computes the frontier from its *own* homed-link count (`home_count`), equal to M3's frontier index by construction (every minted link is stored). No `M7→M3` read on the BH4 path (nor on `nullify`'s P-tgt self-emit computation); M3 stays the authoritative minter.

8. **Dedup's state-dependent home validation (ASN-0128 I1: `home` read only on the miss branch).** **Resolution:** M7 **hoists** `is_registered_document(home)` to the top of `emit_core`, ahead of every gate and dedup short-circuit, so a registered `home` is enforced on *every* emit — including a dedup hit. This is a deliberate divergence from I1's miss-only read: callers cannot evaluate the hit/miss branch, so the unconditional check is what makes M7's caller-facing contract portable (surfaced in §Invariants active enforcement).

## Open build decisions

- **Spanfilade structure.** Brute-force scan of `links` (correct, O(n), the bootstrap default — `SlotIndex` left empty) vs an interval/segment index in tumbler order. Pick the index when stabbing latency under measured corpus size and query rate demands it; keep `stab`'s signature stable across the swap.
- **Hint persistence.** `#[serde(skip)] hints`/`registry` + `rebuild_derived` (recommended — authoritative `links`+config, cheap checkpoints) vs serializing the indexes (faster load, larger checkpoints, a second consistency surface — and the registry cannot serialize as keyed on `CoverageClass`). Default skip+rebuild; tune M2's checkpoint cadence to bound the rebuild pass.
- **Active vs audit indexing.** Index the audit slice and filter active at query (recommended — append-only hints) vs maintain active-only indexes (removal on nullification). Dedup is the exception (active-keyed); choose whether dedup stores all-matches-filter-active (simpler) or an active incumbent (one less filter).
- **Cross-length coverage-class exactness.** The conservative per-length `Extents` partition (buildable today, over-discriminates across lengths, safe) vs a future exact cross-length coverage normal form (M1 provides none). Ship the conservative form; revisit if content-type matching shows the imprecision biting.
- **Nullified representation.** A plain `OrdSet` of roots (sufficient under the unit-depth surface discipline) vs a prefix-trie over roots (needed only if a raw/off-surface range retraction is ever admitted). Default the set; gate any raw `[R]` path behind the trie.
- **Raw-deposit / import path.** Surface-only (recommended — gives idem-uniqueness, no sterilization, no born-nullified non-R tuples, full attribution, all by construction) vs an explicit import mode tolerating multiple dedup matches, non-denoting spans, and audit/active divergence (AD: non-unit spans omitted from address enumerations, visible to membership/`observe`).
- **READLINK fast paths.** Whether to run the structural screen as a pre-probe and whether to keep a ⊥-permanence negative cache (permitted only for provably-permanent absence; usually redundant against the in-memory map). Default: rely on the map, screen only untrusted boundary addresses.
- **Endset backing.** Store verbatim as M7's `Endset` newtype over `im::Vector<Span>` (decided — decomposition must be readable for the hint fold and observable per ML2/RL1) but optionally back each by a canonical span order for cheap structural equality and deterministic serialization — a representation nicety that must never become a *contract* (span order is not promised; equality is by coverage, not decomposition).
- **Multi-BH1 `is_filtered`.** The v1 type-less `is_filtered` assumes the single shipped `Retired` filter; a second registered BH1 type requires `is_filtered` to take the queried `K'` to honor ASN-0128's `J ≠ K'` exclusion. Parameterize when a second filter type is registered.
- **Multi-BH2 walk family.** v1's `sup_fwd` accelerates only the shipped `Supersedes` class, and `succs`/`chain`/`tip`/`current` serve the walk only for it (empty for any other `ty`). A second registered BH2 Binary type needs either a class-keyed `sup_fwd` or the general scan path (`succs(ty,x)` over `type_class[ty]` active, `sup_fwd` as the `[K_sup]` accelerator). Parameterize when a second BH2 type is registered — symmetric to the multi-BH1 decision.
- **BH2 audit-view recovery (OQ6) and `current` reader policy.** Whether to offer an audit-view `chain`/`tip` reconstructing nullified-mid-chain history; and the default the client applies to set-valued `current` (per-home-latest, curator-trust, drop-retracted) — M7 discloses, the consumer decides.
