# M7 — Link & Relation Store — Build-Spec Design

## Purpose & boundary

M7 owns the **authoritative, append-only store of links and typed relations** — every connection in the docuverse — keyed by the link's own permanent address, together with the recomputable **coverage indexes** that answer "which links touch this region." It does one thing: *be the single writer and the single source of truth for link values, and serve every read of structural relation state that does not require V-resolution.* It owns the write surfaces (MAKELINK, Emit/Nullify, assert_sup/editlink), the raw reads (READLINK, FOLLOWLINK), the typed-relation observers (Observe + the four behavior atoms BH1–BH4), the immutable type/shape registry, idempotent de-duplication, and the spanfilade.

It does **not** own: address minting or the home-existence/ownership facts (**M3** — M7 *calls* `mint_link`, reads `is_registered_document`); the V→I arrangement or the home seating mechanism (**M5** — M7 *calls* the semantics-blind `resolve`/`stage_seat_link`, never interpreting arrangement); ordering/durability/recovery (**M2**); the **provenance relation R** (M5 — link placement is deliberately *uncoupled* from R, ASN-0047 J-LV, so M7 touches no R); **non-transcludability** enforcement (M5's content-side referential-integrity check — M7's only duty is to keep links in `s_L`); and **indexed discovery *presentation*** — findlinks/count/windowed-pagination/projection/RETRIEVEENDSETS (**M8**, which executes over M7's spanfilade across the `M8→M7` edge). The split between M7 and M8 is *index ownership and matching* (M7) vs *cursoring/counting/projecting* (M8).

## Public interface

Types `Tumbler/Address/Span/SpanSet/CanonicalForm/Nat` are M1's; `Kernel/Snapshot/LockKey/Seq/TxnError/WorldState/Staging` are M2's; `M3Rec/HasM3/MintError`, `M5Rec/HasM5/VSpec/Run` are M3/M5's. Pure reads are methods on `LinkState` over any `Snapshot`; transact-driving ops hang off `LinkStore<'k,W>` (holds `&'k Kernel<W>` plus a construction-time `Arc<TypeRegistry>` cache of the genesis-immutable registry — constructed via `LinkStore::new`, §C; §3) and are generic over `W` per the engine composition contract. Slots are 1-based: `FROM=1, TO=2, TYPE=3`. Subspace constants are ASN-0093's `s_C = 1` (content), `s_L = 2` (link). `Endset` (M7's readable endset newtype, §Core data model) is the link-value carrier throughout.

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
    pub pred_def: Address, pub pred_stable: Address,            // M9-coordinated addresses; their Unary/⊤/{}
                                                               // registrations are the PredLayer registration
                                                               // agreement, the companion M9 coordination point (§B)
    pub retired: Address,  pub supersedes: Address, pub retraction: Address,  // [K_ret]/[K_sup]/[R]
}
pub enum RegistryError {
    KeyCollision, EmptyKey, BadBehavior, ReservedClassClash, ReservedSubspaceClash, NonAddressDenotingKey,
    UnservedWalk,          // v1 serving fence: app-declared BH2 Walk rejected — only the shipped Supersedes walk is served (§5)
    UnservedSecondFilter,  // v1 serving fence: app-declared BH1 ReadFilter rejected — the type-less is_filtered serves ONE filter (§7)
}

impl TypeRegistry {
    /// Validate-once-or-fail (C0 + R-C0 + R-C1 + reserved-isolation + key denotation + the v1 serving
    /// fence) — the registry's only write point. Seeds the five shipped types
    /// (each `key = enc({reserved.<addr>})`) BEFORE app decls.
    pub fn build(reserved: ReservedAddrs, decls: Vec<TypeDecl>) -> Result<TypeRegistry, RegistryError>;
    pub fn registration(&self, class: &CoverageClass) -> Option<&Registration>;  // internal lookup
    pub fn reserved(&self, t: ShippedType) -> &Endset;   // the genesis-fixed type endset for a shipped class
}
impl Default for TypeRegistry { /* the empty registry — serde seeds the #[serde(skip)] field with it;
                                  rebuild_derived replaces it from reserved+decls before replay */ }
pub enum ShippedType { Retired, Supersedes, Retraction, PredDef, PredStable }
```

`TypeRegistry::build` enforces **C0** (finite, key uniqueness → `KeyCollision`, non-empty representatives → `EmptyKey`); **R-C0**'s behavior↔shape compatibility → `BadBehavior` — **BH1 (ReadFilter) ⇒ Unary; BH2 (Walk) ⇒ Binary; BH3 (ReverseLookup) ⇒ Binary; BH4 (Age) ⇒ idem = ⊥** (any shape); **R-C1** (no app key coverage-equal to a reserved shipped class → `ReservedClassClash`); the **reserved-isolation** precondition (every `ReservedAddrs` entry is element-level with `subspace ∉ {s_C, s_L}` → `ReservedSubspaceClash`, §Core data model); the **key-denotation** precondition (every `TypeDecl.key` — idem⊤ or idem⊥, shipped or app — is address-denoting → `NonAddressDenotingKey`); and the **v1 serving fence** — an app `TypeDecl` declaring `Walk` is rejected (`UnservedWalk`: v1 serves the walk family only for the shipped `Supersedes` class, §5) and an app `TypeDecl` declaring `ReadFilter` is rejected (`UnservedSecondFilter`: the shipped `Retired` is the one BH1 filter the type-less `is_filtered` serves, §7). The fence makes **declared ⇒ served** a build-time property: the registry admits no behavior whose ASN-0128 semantics the v1 read surface would silently fail to serve; its converse — **served only where declared** — is enforced at the BH4 batch surface, where `stale`/`retract_stale` reject a `ty` not registered with BH4 (`NotBh4`, §7); both build rejections lift when the parameterized multi-BH1/multi-BH2 paths land (Open build decisions). The denotation clause keeps `coverage_class` on level-uniform keys during C0's uniqueness comparison *and* makes every idem⊤ dedup `LockKey` serialize an `Addrs` class (§3 / §Core data model totality). `genesis` wraps `build`, storing `reserved`+`decls` (each `Arc`-wrapped) as authoritative config and the built registry as a recomputable lookup (§Core data model); `TypeRegistry` also implements `Default` so serde can seed the `#[serde(skip)] registry` field on deserialize.

Shipped registrations come in two provenance classes. **Note-pinned** (settled — each is the registration a digested note fixes): `Retired = Unary/⊤/{ReadFilter}` (ASN-0128 S1), `Supersedes = Binary/⊤/{Walk}` (ASN-0128 S2), `Retraction = Binary/⊤/{}` (ASN-0128 S3). **The PredLayer registration agreement** — a *named* M7↔M9 coordination point, **not** a derived fact: `PredDef = Unary/⊤/{}` and `PredStable = Unary/⊤/{}`. No digested note pins these two; their shape/idem/behavior values are the registration-side companion to the `ReservedAddrs` addresses (themselves M9-coordinated parameters in the manner of `s_C`/`s_L`). A builder MUST treat the PredLayer registration agreement as an M9-negotiated constant — altering either registration is an M7↔M9 protocol change, not a local M7 edit — exactly as it treats `reserved.pred_def`/`reserved.pred_stable`.

### C. Write — open content links (ASN-0120 MAKELINK)

```rust
impl<'k,W> LinkStore<'k,W>
where W: WorldState + HasLinks
{
    /// Construct the store handle: takes ONE `kernel.snapshot()` and clones the `Arc<TypeRegistry>`
    /// off `snapshot.world().links()` (a refcount bump of the slice's rebuilt registry) as the
    /// construction-time registration cache §3's pre-transact reads consult. Sound because the
    /// registry is genesis-immutable (P1/P2, R1/R2) — the cache can never go stale.
    pub fn new(kernel: &'k Kernel<W>) -> LinkStore<'k, W>;
}

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
    /// Emit_K: gated typed-relation emission. REQUIRES `ty` address-denoting (else NonAddressDenotingType,
    /// rejected before any class computation — keeps `coverage_class(ty)` on the safe `Addrs` path, §Core
    /// data model) AND `ty ≁ [K_sup]` (else SupersessionClass — assert_sup/editlink are the sole
    /// [K_sup]-writers, the parallel of the [R] fence; Conflicts §10); both are PRE-TRANSACT rejections
    /// (Err(TxnError::Rejected(..)), NO transaction opened — §3). Shape-gated (registered ∧
    /// shape-conformant ∧ K≁R).
    /// idem(K)=⊤ ⇒ dedup against the ACTIVE view; a hit returns the incumbent and commits NOTHING
    /// (zero-step). Does NOT seat. value = Link[enc({from}), enc(to), ty.clone()] — `from` single
    /// (|F|=1 forced), `to` cardinality shape-checked, `ty` stored verbatim as e₃. Used by M9
    /// (pdef/pd_stable, rule fires) and managed app relations. The op acquires [dedup_key,
    /// link_lock_key(home)] (registered idem⊤) or [link_lock_key(home)] (idem⊥ or unregistered) before the transact (§3).
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

    /// editlink: ONE composite over [link_lock_key(d_s), link_lock_key(d_a)] (DEDUPED when d_s==d_a,
    /// §2) — allocate a fresh successor link (value supplied directly; M10 builds it via `Link::new`,
    /// arity 3), then assert it supersedes `original`. CANNOT call public assert_sup (M2 non-reentrant).
    /// Successor born UNSEATED. Rejects a successor of arity ≠ 3 (narrowing ASN-0125's N ≥ 3
    /// L3-conformance — Conflicts §11), empty type slot, or NON-LEVEL-UNIFORM type slot
    /// (IllFormedSuccessor — the last keeps the DC-guard `coverage_class` total, §2). DC guard:
    /// reject a retraction-typed successor; schema-conform a claim-typed one. Claim dedup is vacuous/lock-free
    /// (its key carries the fresh successor — §2/§3). M10 forms a content successor off any prior snapshot
    /// (recorded I-addresses are permanent — ML8/EL0; §2).
    pub fn editlink(&self, original: &Address, successor: Link, d_s: &Address, d_a: &Address)
        -> Result<(Address /*successor*/, Address /*claim*/, Seq), TxnError<EditLinkError>>;

    /// BH4 batch tooling. REQUIRES `ty` registered with BH4 (hence idem⊥, R-C0) — a non-BH4 `ty` is
    /// rejected up front (RetractStaleError::NotBh4, NO transaction opened; the served-only-where-
    /// declared fence — an unfenced call could mass-nullify an idem⊤ class, e.g. old Supersedes
    /// claims). v1 ships no BH4 type, so absent an app BH4 registration every call rejects — dormant
    /// by construction. On a BH4 `ty`: nullify every stale tuple of `ty` (age > horizon over the
    /// type-`ty` active slice), stale set snapshotted at entry. NOT atomic — a sequence of `nullify`
    /// transacts (constituent errors lift via RetractStaleError::Nullify). On full success returns the
    /// per-target (emitter, Seq) Vec (a target already nullified by a prior *same-`d_retr`* retraction
    /// dedups to a hit + base Seq; one nullified by a different `d_retr` deposits a redundant but
    /// harmless `[R]` tuple — the dedup key carries `d_retr`); on first TxnError returns Err, leaving
    /// earlier nullifies committed and durable — a re-run with the same `d_retr` is safe (§7).
    pub fn retract_stale(&self, d_retr: &Address, ty: &Endset, horizon: u64)
        -> Result<Vec<(Address, Seq)>, TxnError<RetractStaleError>>;
}
pub enum EmitError      { HomeNotRegistered, NotRegistered, ShapeViolation, RetractionClass, SupersessionClass,
                          NonAddressDenotingType, Mint(MintError) }
pub enum NullifyError   { HomeNotRegistered, BadTarget, Mint(MintError) }
pub enum AssertSupError { HomeNotRegistered, EndpointNotResident, SelfSupersession, Mint(MintError) }
pub enum EditLinkError  { OriginalNotResident, HomeNotRegistered, IllFormedSuccessor, DcViolation, Mint(MintError) }
pub enum RetractStaleError { NotBh4, Nullify(NullifyError) }   // NotBh4 is a pre-transact rejection (no txn opened)
impl From<NullifyError> for RetractStaleError { fn from(e: NullifyError) -> Self { RetractStaleError::Nullify(e) } }
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
pub enum View { Audit, Active, Default }    // Default (active∖filtered) meaningful only on members/targets_of; observe and the §G index primitives (stab/match_links/type_slice) coerce Default→Active
pub struct Tuple { pub addr: Address, pub from: Endset, pub to: Endset }   // endsets are M7's readable Endset
pub enum Tip { Sink(Address), Indeterminate }   // ⊥ at branch or cycle
pub struct NotBh4;   // `ty` not registered with BH4 — stale/retract_stale's served-only-where-declared rejection (§7)
/// EL14 disclosure-not-decision: the operative sink, its OWN activity, and `claims` = the FULL
/// operative out(sink) — EVERY operative [K_sup] claim whose `new` endpoint is this sink, INCLUDING
/// a claim asserted from a node outside reach_o(y); computed per sink via the match_links/type_slice
/// composition (§5), NOT by walk-side accumulation. Empty only when no operative claim targets the
/// sink (e.g. an unedited y that is its own sink and the target of no operative claim). Homes
/// recoverable by `document_of` (EL8b). The reader applies narrowing; M7 decides nothing.
pub struct CurrentMember { pub member: Address, pub active: bool, pub claims: Vec<Address> }

impl LinkState {
    // Observe + default predicates
    pub fn observe(&self, ty: &Endset, from_pat: &[Tumbler], to_pat: &[Tumbler], v: View) -> Vec<Tuple>; // exact ⊆-coverage; patterns T-wide (raw Tumblers — ghosts/non-T4 admitted, ASN-0086); Default→Active
    pub fn is_k(&self, ty: &Endset, a: &Tumbler) -> bool;                 // D2 (exact active coverage-membership; probe ranges over ALL of T; NOT a stab call)
    pub fn members(&self, ty: &Endset, v: View) -> Vec<Address>;          // D1
    pub fn targets_of(&self, ty: &Endset, x: &Address, v: View) -> Vec<Address>;  // D3
    pub fn is_active(&self, a: &Address) -> bool;  pub fn is_nullified(&self, a: &Address) -> bool;
    // BH1 read-filter | BH2 walk | BH3 reverse | BH4 age — served entirely from M7's own indexes
    pub fn is_filtered(&self, a: &Tumbler) -> bool;                       // v1: single shipped BH1 (Retired) — build-enforced (§B); probe ranges over ALL of T, as is_k (membership regime); see §7
    pub fn succs(&self, ty: &Endset, x: &Address) -> Vec<Address>;        // BH2 walk family — v1 serves only the shipped Supersedes class (§5; build-enforced, §B); empty for other ty
    pub fn chain(&self, ty: &Endset, x: &Address) -> Vec<Address>;   pub fn tip(&self, ty: &Endset, x: &Address) -> Tip;
    pub fn is_in_chain(&self, ty: &Endset, addr: &Address, target: &Address) -> bool;  // BH2: target ∈ chain(ty, addr) — membership in the walk's result list, never a coverage test
    pub fn sources_to(&self, ty: &Endset, target: &Address) -> Vec<Address>;     // BH3: active type-`ty` slice (A_K); stab(2,Audit) prefilter, exact G-coverage filter
    pub fn target_of(&self, ty: &Endset, source: &Address) -> Option<Address>;   // BH3: active type-`ty` slice; ⊥ unless exactly one active type-`ty` tuple denotes `source` with single-addr G
    pub fn targets_keyed(&self, source: &Address) -> im::HashMap<CoverageClass, Address>;  // BH3: target_of (active, per type) joined over all BH3 Binary types; key via public `coverage_class(ty)`
    pub fn age(&self, a: &Address) -> Option<u64>;
    pub fn stale(&self, ty: &Endset, h: u64) -> Result<Vec<Address>, NotBh4>;  // REQUIRES ty registered with BH4 (served-only-where-declared fence, §7)
    // ASN-0125 currency (BH2 over the operative supersession graph)
    pub fn current(&self, y: &Address) -> Vec<CurrentMember>;             // set-valued disclosure (EL14); hardwired to [K_sup]
    // shipped reserved-type endsets — M9 reads PredDef/PredStable here (registry lookup is internal)
    pub fn reserved_type(&self, t: ShippedType) -> &Endset;
}
```

### G. Discovery primitives for M8

```rust
impl LinkState {
    /// Spanfilade primitive: links whose slot-`i` coverage OVERLAPS `query` (overlap =
    /// ProperOverlap | Containment | Equal — NOT Adjacent, which abuts coverage-disjointly).
    /// The one shared index probe. `query` is M7's READABLE Endset (M8 builds it) so M7 can
    /// iterate its spans for `classify_spans` overlap. `v ∈ {Audit, Active}` ONLY (a `Default`
    /// is coerced to `Active` — result-side BH1 filtering is undefined for a raw index probe).
    /// Reads `self.hints.spanfilade` (or, in the v1 bootstrap, brute-scans `self.links`), then
    /// filters by `v` against `self.hints.nullified` — so it requires `&self`.
    pub fn stab(&self, i: usize, query: &Endset, v: View) -> im::OrdSet<Tumbler>;
    /// The AND-of-(per-slot overlap) combiner — findlinks' core, factored into M7 (Conflicts §6).
    /// `constraints` lists ONLY constrained slots (slot index, query endset); an unconstrained slot
    /// is OMITTED, never passed as an empty `Endset` (stab(i,&empty,_)=∅ would empty the AND). Empty
    /// `constraints` ⇒ the whole `v` slice (no constraint). `v ∈ {Audit, Active}` ONLY (`Default`
    /// coerced to `Active`, as `stab`).
    pub fn match_links(&self, constraints: &[(usize, Endset)], v: View) -> im::OrdSet<Tumbler>;
    pub fn type_slice(&self, ty: &Endset, v: View) -> im::OrdSet<Tumbler>;    // L_K (Audit) / A_K (Active); v ∈ {Audit, Active} (Default→Active)
}
```

**Return-type convention.** §G's discovery primitives return raw `im::OrdSet<Tumbler>` — the index's native key, which M8 cursors, counts, and paginates over directly without re-validation; they accept only `View::{Audit, Active}` (a `Default` is coerced to `Active` — result-side BH1 filtering is undefined for a raw index probe). Their **query inputs are M7's readable `Endset`** (M8 builds them via `enc`/`Endset::from_spans`), so M7 can iterate the query spans for overlap. §F's caller-facing reads return validated `Address` (and `Tuple`/`CurrentMember`, whose endsets are now readable), lifting M7's internal `Tumbler` keys to `Address` on the way *out* — infallible, every stored key being T4-valid by M3's mint. The handoff runs the other way too: when M8 feeds a §G result key into an address-taking §F read (e.g. `readlink` on a `match_links` hit), it is the **M8 caller** that lifts the `Tumbler` to `Address` via M1's `validate` (likewise infallible by M3's mint, since the key came from the store) before the §F call, whose arguments are `&Address` — the pattern-domain reads (`observe`'s patterns, `is_k`'s probe, and `is_filtered`'s probe) are the exception: they take raw `Tumbler`s (ASN-0086/0128's T-wide pattern/membership domain), so a result key feeds them directly, no lift.

## Core data model

```rust
/// M7-OWNED endset — a READABLE finite span sequence, the as-created decomposition held VERBATIM
/// (observable via raw read-back, ML2/RL1). NOT M1's `SpanSet`, which is read-opaque to M7 (it exposes
/// no span iterator and no field access). Iterate `spans()` directly; fold to a `SpanSet` ONLY at an
/// M1-call boundary (`canonical_key`/`normalize`/`equiv`). Coverage is a query-time projection.
/// Derived Eq/Hash are STRUCTURAL (decomposition- and span-order-sensitive) — serde/container
/// plumbing only, NEVER identity (see the structural-derives contract below).
#[derive(Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
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
pub struct Link { slots: im::Vector<Endset> }   // arity = slots.len() ≥ 3; positional accessors only;
                                                // derived Eq is STRUCTURAL — never link-value identity (identity = address; see below)

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
                                           // single-`&Address` callers pass `slice::from_ref(addr)` for the &[Address] slice
```

```rust
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

**Derived `PartialEq`/`Eq` on `Endset` and `Link` (and `Hash` on `Endset`) are structural, never semantic — a stated contract.** The derives compare the stored span sequence verbatim, so they are decomposition- and span-order-sensitive; that is *not* the model's equality — L5 reads an endset as an unordered set with no positional span accessor, and L6's link equality is componentwise over those *set-valued* endsets — so two coverage-equal (even set-equal) endsets with different decompositions or orderings compare unequal under the derived impls. The derives exist for serde/container plumbing only. **No seam may use them for link-value identity:** link identity is the *address* (the store key; the store is never content-addressed — L11b), and type/dedup identity is `coverage_class`. A consumer that keys on derived `Eq`/`Hash` is wrong by contract, not merely by convention (the Open-decisions "Endset backing" bullet is bound by this).

**Everything else is a recomputable hint** — a pure function of `links` (+ `registry`), maintained incrementally in `apply_link` and re-seeded by `rebuild_derived`. This is the Lampson spine: the journal (via M2) is truth; lose any hint and replay rebuilds it, never wrong.

```rust
#[derive(Clone, Default)]
struct SlotIndex;   // v1 UNIT PLACEHOLDER (Default + Clone so the `Hints` derives compile) — carries
                    // no state; the bootstrap `stab` brute-scans `links` and never reads it. The
                    // deferred interval/segment index replaces this type wholesale behind the same
                    // field (Open decisions).

#[derive(Clone, Default)]
struct Hints {
    spanfilade: [SlotIndex; 3],                            // per standard slot: covered-extent → link addrs (overlap).
                                                           // v1: unit placeholders (above) — `stab` scans `links`
                                                           // directly (reading each endset's spans); the deferred
                                                           // interval/segment index swaps in behind the same field.
    type_class: im::HashMap<CoverageClass, im::OrdSet<Tumbler>>,  // typed slices L_K (Observe, type-match)
    nullified:  im::OrdSet<Tumbler>,                       // resident retraction roots — the tombstone set (active = audit ∖ this)
    dedup:      im::HashMap<DedupKey, im::OrdSet<Tumbler>>, // I0-class → addrs (audit; active-filtered at the check) — idem⊤ classes only
    sup_fwd:    im::HashMap<Tumbler, im::OrdSet<(Tumbler /*new*/, Tumbler /*claim*/)>>, // BH2 old→{(new,claim)}; [K_sup] only (v1)
    home_count: im::HashMap<Tumbler, u64>,                 // BH4: home document → # homed links (the frontier index)
}
```

| Hint | Makes free | Common-case cost |
|---|---|---|
| `spanfilade` | overlap/stabbing for Observe (BH3), `match_links`, M8 | O(log n) insert per slot-span on apply — **target only**; the v1 unit `SlotIndex` holds nothing (no insert; `stab` does an O(n) scan of `links`) |
| `type_class` | `L_K` slices, same-type grouping (L8) | one `coverage_class` of `e₃` + set-insert on apply |
| `nullified` | active view = `links ∖ nullified`; resurrection (I2) | one root-insert when applying an `[R]` tuple |
| `dedup` | O(1) idempotent dedup on the write path (I1) | one `DedupKey` + set-insert on apply (**registered idem⊤ classes only**) |
| `sup_fwd` | BH2 walk / `current` | insert only when applying a `[K_sup]` tuple |
| `home_count` | BH4 `age` in O(1) | `+1` per apply, keyed by `origin(addr)` |

**`CoverageClass` and the level-mismatch hazard.** Two endsets are the same type / the same I0-class iff their *coverage* is equal — never their span decomposition. M7 computes the class via the pure `coverage_class(e)` (below), iterating the readable endset spans. For **address-denoting endsets** (the managed surface: canonical encodings of address sets — every span unit-depth `(x,δ(1,#x))`, detected by `s == subtree_of(s.start())`), coverage equality reduces to the **≼-minimal antichain of denoted addresses** (I0a): iterate `addrs()`, drop any `x` for which some other denoted `y` has `is_prefix(y, x)`, compare as a set. This is exact and never faults — it is the dedup hot-path key. For **general content endsets** (MAKELINK's resolved I-extents, whose spans may differ in length across the endset — element-level and coarser), M1's `canonical_key`/`normalize` *fault* on cross-length input (`LevelMismatch`), so the class is computed **per endpoint-length partition** — partition `spans()` by `#start`, fold each partition to a `SpanSet` (`to_spanset`), `canonical_key` it, assemble the per-length map.

**`coverage_class` is total on the input it actually sees** — every endset reaching it has `#reach == #start` on each span (so within each `#start`-partition all endpoints are equal-length), and `to_spanset`/`canonical_key` therefore never `LevelMismatch`. The earlier draft tried to derive this from a length law of `⊕` (*`⊕` never extends its left operand*); that law is **false and unstated in M1** (M1's `displacement` round-trip holds for `#a ≤ #b`, and T12 admits `Span::new([5,3],[0,2,7])` with `reach = [5,5,7]` *longer* than its start). The real basis is **construction, not arithmetic:** every endset is built through M1's length-preserving primitives, so `#reach == #start` holds *by the primitive it was built from*, with no appeal to any `⊕` output-length property — `subtree_of(p) = from_endpoints(p, shift(p,1))` (`from_endpoints` requires `#s == #r`, and `shift(·,1)` preserves length per ASN-0034 OrdinalShift, so `#start == #reach == #p`); `enc(X)` as unit-depth `subtree_of` spans (same); and `Run::iextent()`, whose reach endpoint is `shift(i_start, width)` (length `#i_start` by shift's length-preservation, M5-guaranteed level-uniform element-level) against start `i_start`. This covers every endset that reaches `coverage_class`: address-denoting on every managed path (emit's `ty` is validated address-denoting before the call, every `TypeDecl.key` is validated address-denoting at `build`, and `enc`/the reserved types/all stored managed from/to/type slots are encodings) and `iextent`-lifted on every content path (MAKELINK and editlink-successor type slots). The only paths that could present a *hand-built* span are an externally-supplied `editlink` successor type slot and a read-side `ty` argument; both are fenced separately — the editlink successor's type slot is **additionally** checked `is_level_uniform()` at the write boundary (`IllFormedSuccessor`), and read-side `ty` is registered/reserved (hence address-denoting), or, for a content-type query, an `iextent`-built endset, by caller contract (M8/M9 never hand `coverage_class` a length-mismatched span). So `is_level_uniform()` is a **belt-and-suspenders backstop** against an adversarial `Span::new`, *not* the safety basis — which is the by-construction `#reach == #start` above. This is what lets the total `apply_link` call `coverage_class` unconditionally without a builder having to reconstruct an `⊕`-length proof. **Off-contract behavior is pinned:** on a non-level-uniform span, `coverage_class` **panics** — the internal `canonical_key` `LevelMismatch` is `.expect()`ed with a message naming the level-uniformity precondition — never skipping the span and never returning a coarser class (either would silently merge distinct classes and corrupt type/dedup identity); since every internal call site is guarded above, the panic can only mark an off-contract external caller of the `pub` function.

```rust
#[derive(Clone, PartialEq, Eq, Hash)]                  // NOT Serialize: Extents wraps M1's non-Serialize CanonicalForm
pub enum CoverageClass {                                // (lives only in the skip registry/hints, so this is fine)
    Addrs(im::OrdSet<Tumbler>),               // ≼-minimal antichain — address-denoting (exact)
    Extents(im::OrdMap<usize, CanonicalForm>),// per-length canonical coverage — content extents (safe, see below)
}
#[derive(Clone, PartialEq, Eq, Hash)]
pub struct DedupKey { ty: CoverageClass, from: CoverageClass, to: CoverageClass }  // I0 = (cov(F),cov(G)) within [K]

/// PURE coverage CLASS of an endset (type / I0 identity — coverage equality, NEVER decomposition).
/// No store state, so no `&self`. Address-denoting endset (every span unit-depth) ⇒ `Addrs` = its
/// ≼-minimal denoted antichain (I0a, exact); general (level-uniform) content endset ⇒ `Extents` = per-`#start`
/// partition, each folded `to_spanset` then `canonical_key`d (safe, over-discriminates across lengths
/// — see below). The lone place an endset folds to a `SpanSet`. PUBLIC so M9 can key `targets_keyed`'s
/// map via `coverage_class(ty)`; M7 itself calls it by name from `apply_link`, `emit_core`, the dedup
/// key, the DC guard, and the walk-class checks. TOTAL ON LEVEL-UNIFORM INPUT — which is all it ever
/// receives (managed paths validate address-denoting; content paths are `iextent`-level-uniform; read
/// `ty` args are registered address-denoting types by contract). OFF-CONTRACT INPUT PANICS: a
/// hand-built non-level-uniform span (`#width > #start`, e.g. T12-valid `([5,3],[0,2,7])`) hits M1's
/// `LevelMismatch` inside `canonical_key`, surfaced as a PANIC (`.expect()` naming the level-uniformity
/// precondition) — NEVER a skipped span or a coarser class, either of which would silently corrupt
/// type/dedup identity. Guarded at every internal entry — see the totality argument above.
pub fn coverage_class(e: &Endset) -> CoverageClass;
```

The per-length partition is **conservative**: it can *over*-discriminate two content endsets whose equal coverage straddles lengths, never *merge* distinct ones. Over-discrimination is the safe direction for both type-matching (you under-match, never false-match) and dedup (you deposit a second tuple, never wrongly suppress). **Address-denoting endsets land in `Addrs` (exact)** — the entire managed surface *and* any MAKELINK type that resolves to a single content address; **only a multi-span or mixed-length content extent reaches `Extents`** (a MAKELINK type spanning content). **Reserved-class isolation:** `TypeRegistry::build` requires every `ReservedAddrs` entry to be element-level with `subspace ∉ {s_C, s_L}` (`ReservedSubspaceClash`), so a content link's type class (always within `s_C`) and a link-store address (within `s_L`) can never coverage-equal a reserved class — the no-collision guarantee Conflict §1 leans on (e.g. a content-typed link can never be misread into the `[R]` class and spuriously inserted into `nullified`). The exact cross-length class is left open (M1 provides no cross-length normal form) — see Open build decisions.

**One `coverage_class`, everywhere — class coherence under over-discrimination.** Every class-sensitive *guard* — `emit`'s `[R]` and `[K_sup]` fences, `editlink`'s DC check, `nullify`'s Retraction gate — and every class *recognition* in `apply_link` — `[R]` → `nullified`, `[K_sup]` → `sup_fwd`, idem⊤ → `dedup` — evaluate the **same** pure `coverage_class` function; no second classifier exists anywhere in M7. This is what extends the safe-direction claim from type-matching and dedup to the fences: a hand-built endset whose *coverage* equals a reserved class but whose *class* differs — e.g. mixing the unit span at `r_addr` with a deeper non-unit span under it, which adds nothing to coverage but lands the endset in `Extents` rather than `Addrs` — is admitted by the DC guard (its class ≠ `[R]`'s `Addrs` class) *and* treated as non-`[R]` by the fold (the same inequality, evaluated by the same function on the same stored slot). The engine therefore never half-recognizes a tuple — fence-admitted yet fold-recognized (a spurious `nullified` insert), or fence-rejected yet fold-ignored — because guard and fold cannot disagree when they are one function.

Because the dedup **`LockKey`** serializes `DedupKey.ty = coverage_class(ty)` and the `Extents` variant wraps M1's non-`Serialize` `CanonicalForm`, `TypeRegistry::build` constrains **every** type key to be address-denoting (`NonAddressDenotingKey`) — doing double duty: it keeps `coverage_class` on level-uniform input (totality, above) *and* makes every idem⊤ type's serialized class the `Serialize`-able `Addrs`. `DedupKey.from`/`.to` on the emit path are always `Addrs` (single source address / `enc`'d to-set), and MAKELINK/idem⊥ types never take a dedup lock — on the **emit/lock path** no dedup key is computed for them at all (§3); the lone fold-side exception is the degenerate coincidence class (a MAKELINK deposit whose resolved type class equals a registered idem⊤ app class — §1, Conflicts §1), whose in-memory `DedupKey` — possibly with `Extents` from/to — lives only in the `dedup` hint and never reaches a `LockKey` — so no `Extents` class is ever serialized into a `LockKey`.

## Internal design

### 1. The store, recovery, and the engine plug

`apply_link(LinkRec::Emit{addr, value})` inserts `addr↦value` into `links` and folds **every** hint incrementally — O(log n) `im` operations throughout, all reading the endsets through `spans()`/`addrs()`: each slot's spans into `spanfilade` (a no-op in the v1 bootstrap — `SlotIndex` is the unit placeholder and `stab` scans `links`, §6); `coverage_class(value.type_slot())` into `type_class`; if that class is `[R]`, **every** denoted to-root (`value.to_slot().addrs()`) into `nullified`; **for a tuple whose type class is registered idem⊤ only**, the `DedupKey` into `dedup` (an unregistered or idem⊥ class — every ordinary MAKELINK content link, and any idem⊥ app relation — skips the dedup key entirely, since no dedup check ever reads it, sparing the multi-span `Extents` partition the key would otherwise force; the fold keys on the *class registration*, so the one exception is a MAKELINK deposit whose resolved type class coincidentally equals a registered idem⊤ app class — Conflicts §1's degenerate case — which does fold an in-memory `DedupKey`, possibly with `Extents` from/to: harmless, it never reaches a `LockKey`, and over-discrimination is the safe direction); if `[K_sup]`, the `old→(new,addr)` edge (both via `addrs()`) into `sup_fwd`; `home_count[origin(addr)] += 1`. The `[R]` fold is **pinned off the surface discipline** — this is the replay-critical fold M2 requires total and deterministic: it inserts *every* denoted to-root — zero denoted roots ⇒ no insert, several ⇒ all inserted — the faithful address-denoting generalization of ASN-0086's coverage-based `nullified`; a non-unit-depth `[R]` to-span contributes no root (its coverage-*range* effect is admitted only with the prefix-trie — Open decisions, Nullified representation). Every v1 path yields exactly one root (`nullify` writes the unit-depth `enc({target})`; `emit`/MAKELINK/`editlink` are `[R]`-fenced), so the general rule degenerates to the single-root insert in practice — but a builder never invents behavior at the fold. `apply_link` carries the genesis config — `reserved`, `decls` (`Arc`-shared, so "carrying forward" is a refcount bump, not a copy), and the rebuilt `registry` — forward unchanged (they are not records and never change). It reads only `LinkState` + M1 arithmetic + `registry`, is deterministic and total, and is applied exactly once per committed record (M2 guarantees this — do **not** code it idempotent).

`rebuild_derived` runs once at load, before replay (serde having seeded the two `#[serde(skip)]` fields with their `Default`s on deserialize — an empty `TypeRegistry` and empty `Hints`, both immediately overwritten here): it first reconstructs `registry = TypeRegistry::build(reserved, decls)` from the deserialized authoritative config (a `.expect()` — the inputs passed validation at genesis), then recomputes `hints` entirely from the checkpointed `links` + `registry`. Because **all** hints are pure functions of `links`+`registry`, this is a single pass; and because the registry is reconstructed before replay, the post-checkpoint `apply_link` folds see it. Recovery is therefore *pure replay*: no undo log, no compaction for correctness; the only knob is M2's checkpoint cadence (it bounds the rebuild pass).

The engine assembles `World{ …, links: LinkState, … }`, implements `HasLinks`, `From<LinkRec> for Record`, and dispatches `Record::Links(x) => world.links().apply_link(x)`. M7 names neither `World` nor `Record`; its transact-ops are `impl<W: WorldState + HasLinks + HasM3 [+ HasM5]> LinkStore<W> where W::Record: From<LinkRec> + From<M3Rec> [+ From<M5Rec>]`.

### 2. Two write surfaces, one store (the central architecture)

The store holds links from **two disciplines that never unify** (Conflicts §1):

- **MAKELINK — the open content-link surface** (ASN-0043/0120). Resolves V-specs, admits multi-span endsets, admits ghost/unregistered types, applies **no shape gate** and **no idem dedup** (distinct links always — ML0). Seats the link in its home.
- **Emit_K — the managed typed-relation surface** (ASN-0086/0126/0128). Address-level, **shape-gated**, **idem-deduped per type**, `K ≁ R` rejected; **never seats**.

They share `links`, the spanfilade, every read path, and one internal `emit_core`. They differ only in admission (the gate) and in whether the *op* seats afterward (MAKELINK does; Emit_K/Nullify/assert_sup/editlink do not). A MAKELINK content link's type resolves to `s_C` I-addresses, whose coverage class can never collide with a reserved managed class (reserved type addresses lie outside `s_C`/`s_L`, §Core data model), so MAKELINK links never pollute the managed slices; and the behaviors degrade gracefully (`target_of` returns ⊥ on a non-single-address endset, BH2 reads single-address claims) if an app ever registered a managed type coverage-equal to a MAKELINK type.

**`emit_core` (shared)** — the single choke point, run inside one `transact`. Its bounds are `W: WorldState + HasLinks + HasM3` only (gate + `mint_link` + deposit `LinkRec`); it has **no `seat` step** and so needs neither `HasM5` nor `From<M5Rec>` — the seat is staged by MAKELINK itself, the lone `HasM5` caller, after `emit_core` returns. Any dedup **lock** is acquired by the public op *before* this transact (§3 step 1); `emit_core` does the **hoisted home check** and the in-txn active-view dedup **check** (§3 step 2). `|F|`/`|G|` below are `value.from_slot().len()`/`value.to_slot().len()`. Its concrete signature, gate selector, and internal error:

```rust
enum Gate { Open, Managed, Retraction }   // selects the admission DISCIPLINE, never the value (effect-identity)
enum EmitCoreError { HomeNotRegistered, NotRegistered, ShapeViolation, RetractionClass, EmptyType, Mint(MintError) }
impl From<MintError> for EmitCoreError { fn from(e: MintError) -> Self { EmitCoreError::Mint(e) } }  // backs `mint_link(home)?`

fn emit_core<W>(stg: &mut Staging<W>, home: &Address, value: Link, gate: Gate)
    -> Result<Address, EmitCoreError>
where W: WorldState + HasLinks + HasM3, W::Record: From<LinkRec> + From<M3Rec>;
```

The body:

```text
emit_core(stg, home, value, gate) -> Result<Address, EmitCoreError>:
  assert value.arity() == 3                                                   // STORE-INVARIANT BACKSTOP — defensive; every caller
                                                                             // builds arity 3 (MAKELINK/Emit_K/assert_sup/claim/editlink),
                                                                             // so this is never tripped, but it guarantees type_class /
                                                                             // the 3-slot spanfilade / ASN-0086's |Σ.L|=3 hold locally
  require stg.working().m3().is_registered_document(home)                     // HomeNotRegistered — HOISTED ahead of every
                                                                             // gate/dedup short-circuit (enforced on a hit too, Conflicts §8)
  match gate:
    Open (MAKELINK / editlink successor):
        require !value.type_slot().is_empty()                                 // EmptyType (arity 3 guaranteed by caller)
    Managed (Emit_K / assert_sup / editlink claim):
        let K = coverage_class(value.type_slot())                            // total: value.type_slot() level-uniform (validated upstream)
        require registry.registration(&K).is_some()                          // (i) registered (NotRegistered)
        require K ≠ coverage_class(reserved(Retraction))                     // K ≁ R (RetractionClass)
        require Sh-conf(reg.shape, |F|, |G|)                                 // (ii) span-count gate (ShapeViolation)
        if reg.idem: DEDUP-CHECK (§3 step 2, vs stg.working() active) — hit ⇒ return incumbent, stage NOTHING
    Retraction (Nullify):
        require registry.registration(&coverage_class(reserved(Retraction))).shape == Binary  // defensive (genesis-fixed)
        require Sh-conf(Binary, |F|, |G|)                                    // |F|=1, |G|=1
        DEDUP-CHECK (§3 step 2, idem⊤) — hit ⇒ return incumbent, stage NOTHING
  let (addr, m3rec) = stg.working().m3().mint_link(home)?                     // K.λ via M3 (home already known-registered; other MintError → Mint)
  stg.push(m3rec.into())
  stg.push(LinkRec::Emit{ addr: addr.tumbler().clone(), value }.into())       // addr: Address → Tumbler key (LinkRec.addr is Tumbler); deposit; NO seat, NO R
  return addr
```

`Sh-conf` reads `shape(K)` from the registry and tests *span counts* (Unary `|G|=0`, Binary `|G|=1`, Multi `|G|<∞`; all require `|F|=1`) — never inferring shape from the tuple (a `(1,0)` tuple conforms under Unary *and* Multi). The gate adds preconditions only and never alters `value` (**effect-identity** — the ASN-0126 `π` bridge): do not "normalize on the way in." Both `Open` callers supply an arity-3 value (MAKELINK builds `[e₁,e₂,e₃]`; `editlink` pre-checks `successor.arity()==3`), and `emit_core` *defensively asserts* `value.arity() == 3` — a store-invariant backstop these callers never trip — so the store holds only arity-3 links. The Managed gate's `coverage_class(value.type_slot())` is total because the type slot is level-uniform by upstream validation (emit's `ty` is address-denoting; the supersession claim's type is reserved; §Core data model totality).

**`emit_core` error mapping.** It returns `EmitCoreError`. `HomeNotRegistered` originates at the **hoisted home check** alone; `mint_link`'s own `MintError::HomeNotRegistered` would lift through the `From<MintError>` impl into `EmitCoreError::Mint(..)`, not `EmitCoreError::HomeNotRegistered` — but the hoist makes `home` known-registered before the mint, so that `mint_link` branch is unreachable. Every other `MintError` rides `Mint`. Each public op maps it:

- **MAKELINK** (`Open`): maps `emit_core`'s `EmptyType→EmptyTypeResolution`, `Mint→Mint`, `HomeNotRegistered→HomeNotRegistered` (the `Managed`/`Retraction` branches are unreachable); and — since MAKELINK, not `emit_core`, stages the seat — maps `stage_seat_link`'s `SeatError→Seat` directly.
- **emit** (`Managed`, no seat): `HomeNotRegistered/NotRegistered/ShapeViolation/RetractionClass/Mint` pass through to the like-named `EmitError` variants; `EmptyType` unreachable (managed `e₃ = ty` non-empty by `T_admissible`). The address-denoting `ty` precondition (`NonAddressDenotingType`) and the supersession-class fence (`SupersessionClass`) are enforced in the public op before `emit_core`, never raised here.
- **nullify** (`Retraction`): `HomeNotRegistered→HomeNotRegistered`, `Mint→Mint`; the gate variants are defensive (the `[R]` type is genesis-fixed Binary); P-tgt is checked in `nullify` itself (`BadTarget`).
- **assert_sup / editlink-claim** (`Managed`, K_sup): `HomeNotRegistered→HomeNotRegistered`, `Mint→Mint`; `NotRegistered/ShapeViolation/RetractionClass` are unreachable for the registry-fixed K_sup. editlink's successor (`Open`): `EmptyType→IllFormedSuccessor`, `Mint→Mint`.

As `From` impls (each op's `?` on `emit_core(…)` lifts through these; MAKELINK additionally lifts `stage_seat_link`'s `SeatError`; the `_ => unreachable!()` arms are the paths the prose above proves cannot fire):

```rust
impl From<EmitCoreError> for MakeLinkError {            // Open: only EmptyType/HomeNotRegistered/Mint reachable
    fn from(e: EmitCoreError) -> Self { match e {
        EmitCoreError::EmptyType         => MakeLinkError::EmptyTypeResolution,
        EmitCoreError::HomeNotRegistered => MakeLinkError::HomeNotRegistered,
        EmitCoreError::Mint(m)           => MakeLinkError::Mint(m),
        _ => unreachable!("Open gate raises no Managed/Retraction rejection"),
    }}
}
impl From<SeatError> for MakeLinkError { fn from(e: SeatError) -> Self { MakeLinkError::Seat(e) } }

impl From<EmitCoreError> for EmitError {                // Managed: EmptyType unreachable (e₃ = ty non-empty)
    fn from(e: EmitCoreError) -> Self { match e {
        EmitCoreError::HomeNotRegistered => EmitError::HomeNotRegistered,
        EmitCoreError::NotRegistered     => EmitError::NotRegistered,
        EmitCoreError::ShapeViolation    => EmitError::ShapeViolation,
        EmitCoreError::RetractionClass   => EmitError::RetractionClass,
        EmitCoreError::Mint(m)           => EmitError::Mint(m),
        EmitCoreError::EmptyType         => unreachable!("managed e₃ = ty ∈ T_admissible"),
    }}
}
impl From<EmitCoreError> for NullifyError {             // Retraction: gate variants defensive (genesis-fixed [R] Binary)
    fn from(e: EmitCoreError) -> Self { match e {
        EmitCoreError::HomeNotRegistered => NullifyError::HomeNotRegistered,
        EmitCoreError::Mint(m)           => NullifyError::Mint(m),
        _ => unreachable!("[R] type is genesis-fixed Binary; P-tgt checked in nullify"),
    }}
}
impl From<EmitCoreError> for AssertSupError {           // Managed/K_sup: registry-fixed ⇒ gate variants unreachable
    fn from(e: EmitCoreError) -> Self { match e {
        EmitCoreError::HomeNotRegistered => AssertSupError::HomeNotRegistered,
        EmitCoreError::Mint(m)           => AssertSupError::Mint(m),
        _ => unreachable!("K_sup registry-fixed Binary/idem⊤; endpoints/irreflexivity pre-checked in assert_sup"),
    }}
}
impl From<EmitCoreError> for EditLinkError {            // successor (Open): EmptyType→IllFormedSuccessor; claim (Managed/K_sup)
    fn from(e: EmitCoreError) -> Self { match e {
        EmitCoreError::EmptyType         => EditLinkError::IllFormedSuccessor,
        EmitCoreError::HomeNotRegistered => EditLinkError::HomeNotRegistered,
        EmitCoreError::Mint(m)           => EditLinkError::Mint(m),
        _ => unreachable!("editlink pre-checks DC/arity/residence; K_sup claim registry-fixed"),
    }}
}
```

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

Recording M5's `resolve` runs lifted through the public, total `Run::iextent()` *as* the endset spans makes the **coverage-exactness recovery equation** (ML1: `coverage(eᵢ) ∩ dom(C) = ρ`) hold by construction — M5's runs trace exactly allocated content and never over-reach the frontier, cross-origin runs arrive un-coalesced (M16), and `iextent` is the level-uniform element-level I-extent (so every MAKELINK endset, type included, is level-uniform — its later `coverage_class` fold cannot fault). The `wf` checks are *concrete component tests* on the V-span — `subspace(u_j)=s_C` of ASN-0120 is the V-position's first component `start.get(1)`, **not** M1's `Address::subspace()` (which needs `zeros=3` and returns `None` for a depth-2 V-position, so a naïve builder would reject every spec); the length checks `#start==2`/`#width==2` precede the `get(1)` indexing so the 1-based `Tumbler::get` never panics. These mirror M5's `resolve` precondition — deliberately **narrowing** ASN-0120's `wf` (`#u_j ≥ 2`) to exactly depth 2, since M5's POOM keys and `resolve` are depth-2 as given and a deeper spec could only ever resolve to ∅ (Conflicts §12) — and produce `IllFormedSpec` *rejections*, distinct from the silent ⟨⟩ that `resolve` returns for a non-content/malformed span. The held key is `link_lock_key(home)` — `emit_core`'s `mint_link(home)` advances the link frontier, so the held lock and the advanced frontier are byte-identical (M3's contract); a content key would not serialize MAKELINK against `emit`/`assert_sup`/`nullify` at the same home (colliding link addresses) under a multi-applier realization. MAKELINK touches **no R** (J-LV), allocates content nowhere (J0 vacuous), and seats exactly one link V-position.

**Emit_K** first **validates `ty` is address-denoting** (else `EmitError::NonAddressDenotingType`, before any `coverage_class(ty)` — this is what keeps the class computation on the safe `Addrs` path, §Core data model totality), then **fences the supersession class**: `coverage_class(ty) == coverage_class(reserved(Supersedes))` is rejected (`SupersessionClass`) — the exact parallel of the `[R]` fence, making `assert_sup`/`editlink` the sole `[K_sup]`-writers; the fence lives in the **public op only**, so those two ops' internal `emit_core` `Managed` path is untouched (Conflicts §10). Both rejections are pre-transact — no transaction opened (§3). It then wraps `emit_core` with the value construction: `value = Link::new([enc(slice::from_ref(from)), enc(to), ty.clone()]).unwrap()` (F single-address, G the to-set encoding, e₃ = `ty` verbatim), then `emit_core(stg, home, value, Managed)`. The public op computes the `dedup_key` from its args **before** the transact and supplies `[dedup_key, link_lock_key(home)]` (registered idem⊤) or `[link_lock_key(home)]` (idem⊥ or unregistered) to `transact` (§3).

**editlink** is one M2 composite over **two home alloc keys** — `transact([M3State::link_lock_key(d_s), M3State::link_lock_key(d_a)], …)`, the key vec **deduped before the transact** (a same-home edit `d_s == d_a` collapses `[k, k]` to `[k]`; M7 does the dedup rather than relying on M2 deduping, since M2's `transact(keys)` contract makes no duplicate-key promise) — inlining two `emit_core` calls; it **cannot** call the public `assert_sup` (itself a `transact`: M2 is non-reentrant — a nested write deadlocks — and a second `transact` would forfeit EL7 atomicity). The residence/arity preconditions and the **DC** guard run *inside* the closure against `stg.base()` (DC's `[K_sup]`-witness check is a base-state read):

```text
editlink(original, successor, d_s, d_a):                      // successor : Link, supplied (M10 built it via Link::new)
  let keys = dedup([link_lock_key(d_s), link_lock_key(d_a)]); // d_s == d_a ⇒ one key (M2 makes no dedup promise — §2)
  transact(keys, |stg| {                                      // two home alloc keys only — no dedup key (claim key carries fresh a')
     let base = stg.base();
     require base.m3().is_registered_document(d_s) ∧ base.m3().is_registered_document(d_a)  // HomeNotRegistered
     require original ∈ base.links()                                                        // OriginalNotResident
     require successor.arity() == 3 ∧ !successor.type_slot().is_empty()                     // IllFormedSuccessor (arity-3 store,
            ∧ successor.type_slot().spans().all(|s| s.is_level_uniform())                   //   Conflicts §11; type slot level-uniform ⇒ DC-guard coverage_class total)
     require DC(successor):  coverage_class(successor.type_slot()) ≠ coverage_class(reserved(Retraction))  // DcViolation (coverage_class total: type slot level-uniform)
                          ∧ (coverage_class(successor.type_slot()) == coverage_class(reserved(Supersedes)) ⟹
                               schema-conforming witnesses ∈ base.links())                  // unit-depth single-addr F/G, endpoints resident, irreflexive
     let a' = emit_core(stg, d_s, successor, Open)?           // born unseated; content type idem⊥ ⇒ no dedup deposit
     let b  = emit_core(stg, d_a,                             // claim: "original superseded by a'"
                        Link::new([enc(slice::from_ref(original)), enc(slice::from_ref(&a')), reserved(Supersedes).clone()]).unwrap(),
                        Managed)?                             // claim dedup-CHECK is a guaranteed miss (fresh a') ⇒ lock-free (§3)
     Ok((a', b))
  })
```

The claim's dedup is **vacuous and lock-free** here: its `DedupKey` carries the freshly minted successor `a'` (unknowable before the closure, and M2 takes `keys` up front), so the active check is a guaranteed miss — no claim dedup `LockKey` is needed, only the two (deduped) home alloc keys. Both writes commit atomically (EL7); the original is untouched (L12). The DC guard is what keeps editlink discipline-preserving and therefore chainable; rejecting an `[R]`-typed successor stops step 1 from silently nullifying its to-set, and schema-conforming a `[K_sup]`-typed successor keeps the supersession discipline. The level-uniformity check on the successor's type slot (folded into `IllFormedSuccessor`) is what makes the DC-guard `coverage_class(successor.type_slot())` total — M10's documented content-successor construction (`iextent`/`enc`) satisfies it by construction.

**M10 builds the `successor: Link` itself** (ASN-0125 takes a pre-formed `ℓ'`). For a content successor it resolves V-specs through M5's `resolve`, lifts each run with `Run::iextent` to a readable `Span` (level-uniform), forms the endsets with `Endset::from_spans` (any address-denoting slot — e.g. a type address — via `enc`), and assembles the three slots with `Link::new` (arity 3). The resolution may be taken off **any prior snapshot**, since recorded I-addresses are permanent (ML8/EL0) and need not be re-resolved at edit time — so the builder is never left guessing how to form a content successor.

### 3. De-duplication and the M2 keyed critical section

Idempotence is a **computed equivalence at the surface, never stored identity** (I1) — the store stays pluralistic underneath; a hit returns the incumbent's address and *commits nothing*. The dedup **lock** and the dedup **check** are split across the transact boundary, because `emit_core` runs *inside* an already-open `transact` and cannot itself acquire keys:

1. **The public op validates `ty` (denotation + class fences), reads the registration, then acquires the dedup lock — *before* the transact.** `emit` first **rejects a non-address-denoting `ty`** (`NonAddressDenotingType`, ahead of any `coverage_class(ty)`, so the class computation stays on the safe `Addrs` path — §Core data model totality), then **rejects `ty ~ [K_sup]`** (`SupersessionClass` — the supersession class writes only through `assert_sup`/`editlink`, Conflicts §10). Both are **pre-transact rejections**: the call returns `Err(TxnError::Rejected(..))` with **no transaction opened** — the same plumbing as `retract_stale`'s `NotBh4` (§7) and M3 `fork`'s no-txn rejection — so M10 sees one uniform typed-rejection contract. (`assert_sup`/`nullify` have no pre-transact rejections of their own: their key computations are total — genesis-fixed reserved classes plus `enc`'d addresses — and cannot fail.) Which lock set to hold then turns on the type's registration, so the op reads its `Registration` *before* opening the transact: `emit` looks it up by `coverage_class(ty)` in `LinkStore`'s **construction-time registration cache** — an `Arc<TypeRegistry>` cloned once at `LinkStore` creation; concretely, `LinkStore::new` (§C) takes one `kernel.snapshot()` and clones the `Arc` off `snapshot.world().links()` (a refcount bump of the slice's rebuilt registry). The registry is genesis-immutable, so taking a fresh `Snapshot` per write purely to read invariant config is wasteful, and the cache is the default (an equivalent `self.k.snapshot().world().links().registry` read is the fallback where no cache is wired). `assert_sup`/`nullify` need no read (their fixed `[K_sup]`/`[R]` types are genesis-idem⊤, so they always take the dedup lock). The registration is **immutable across all reachable states** (P1/P2 of ASN-0126, R1/R2 of ASN-0128 — the registry is sealed at genesis and never drifts), so the cache (or fallback read) is race-free against any concurrent write and agrees with what `emit_core` consults inside the txn. **Lock by case:** a **registered idem⊤** type computes `DedupKey = (coverage_class(ty), Addrs({from}), Addrs(to))` from the op's *arguments* (the from/to addresses are in hand; `coverage_class(ty)` reads `ty`'s spans, address-denoting by the just-checked precondition ⇒ `Addrs`), serializes it into a `LockKey` (M7's space tag + the minimal antichains), and supplies it alongside the home alloc key: `transact(&[dedup_key, M3State::link_lock_key(home)], …)`. A **registered idem⊥** type *or* an **unregistered** type takes **only** `[link_lock_key(home)]` (no dedup key, none computed) — an idem⊥ type always deposits fresh, and an unregistered type cannot be a dedup hit at all: `emit_core` rejects it with `NotRegistered` after the hoisted home check. Same I0-class ⇒ same `LockKey` ⇒ M2 serializes the check-and-deposit (I1a/I4); different I0-class ⇒ no contention. This is the only cross-home synchronization point, partitioned **by I0-class, never by home** — sharding dedup by home would let two same-class different-home emits both miss.
2. **`emit_core` performs the active-view check — *inside* the txn** (after the hoisted home check). It recomputes the same `DedupKey` from `value` (identical to the op's, by construction — `value.type_slot()` is the validated address-denoting `ty`, from/to are `enc`'d) and looks up `dedup[key]` filtered by `∉ nullified` off `stg.working().links()`. Several active matches (only off a raw path) → return the T1-least (deterministic). One → return it, stage nothing (zero-step; M2 returns the base `Seq`). None → fall through and deposit.

Reading the *active* view (I2) is what gives **resurrection**: a nullified tuple is invisible to dedup, so re-emitting lands at a fresh address — the audit trail keeps both. MAKELINK and idem⊥ app types skip both the lock and the check (only the home key) and compute no `DedupKey` on the write path (§1's fold-side degenerate-coincidence exception is apply-time, in-memory only); the editlink claim skips the dedup **lock** too — its `DedupKey` carries the freshly minted successor `a'` (unobtainable as a `transact` key before the closure), and the in-txn check is a guaranteed miss, so editlink supplies only the two (deduped) home alloc keys (§2).

### 4. Retraction, the nullified set, and the active view

`nullify(d_retr, target)` is `emit_core` of an `[R]` tuple with canonical from-fill `enc({d_retr})` and unit-depth to-span `enc({target})`, run through the **Retraction** gate (which requires the genesis-fixed `[R]` Binary type and the `|F|=|G|=1` span counts), idem⊤ — so re-retracting the same target from the same document dedups. The public op computes `dedup_key` (the `[R]` class via `coverage_class(reserved(Retraction))`, from=`{d_retr}`, to=`{target}` — all address-denoting) before the transact and supplies `[dedup_key, M3State::link_lock_key(d_retr)]`. It checks **P0** (`is_registered_document(d_retr)` → `HomeNotRegistered`) and **P-tgt** as a rejecting precondition in `nullify`'s closure against `stg.base()`: `target` is a resident link (`target ∈ stg.base().links()`) **or** `target` equals nullify's own would-be fresh emitter. M7 computes that would-be emitter in O(1) without reading M3's frontier: since each sibling-advance `inc(·,0)` only bumps the terminal ordinal, the emitter is `elem_addr(ElemPos{ doc: d_retr, subspace: s_L, ordinal: 1 + home_count[d_retr] })` — the next link-chain **I-address**, the element-level link-store address `d_retr·0·s_L·(1 + home_count[d_retr])` (*not* an M5 depth-2 V-position; no iterated `inc` scan), equal to `mint_link(d_retr)`'s output by construction (FrontierUnification; §Conflicts 7; `home_count[d_retr] == 0` ⇒ ordinal 1, the first emission itself). The `elem_addr` `Result` is infallible here: P0's `is_registered_document(d_retr)` check precedes it, so `d_retr.level() == Document` holds, and `s_L ≥ 1`, ordinal ≥ 1 discharge the other two clauses. Else `BadTarget`. Public `emit` rejects `K ~ R` (the Managed gate's `K ≠ [R]`), so `nullify` is the *sole* `[R]`-writer (the parallel public-op fence on `[K_sup]` makes `assert_sup`/`editlink` the sole `[K_sup]`-writers — §5, Conflicts §10).

`nullified` is a monotone tombstone set of **resident retraction roots**. Under the unit-depth + antichain discipline, R-Scope makes each retraction nullify exactly one resident link, so "is `a` nullified?" is a plain `nullified.contains(a)` (a prefix-trie variant covers the off-surface range case — Open decisions). The **active view of any slice is `audit ∖ nullified`**, derived at query time; the spanfilade and `type_class` index the *audit* slice (append-only, never delete on nullification), and `View::Active`/`Default` filters results by `nullified`. Only `dedup` consults active (above). This keeps every index a pure append-only hint.

**Sterilization is unreachable through M7's surface** (DR theorem): `nullify`-only-via-the-wrapper + unit-depth to-span + P-tgt-rejecting makes the wp's C3 conjunct vacuous — no pre-existing retraction can ever cover a later fresh emitter address (antichain + freshness). Born-nullified tuples arise only from a deliberate self-emit retraction, and that falls out of the ordinary `audit ∖ nullified` derivation with no special gate.

### 5. Supersession and the BH2 walk

`assert_sup(home, old, new)` emits a `[K_sup]` claim with **F = enc({old}), G = enc({new})** (slot convention resolved in Conflicts §2 — F holds the *old/superseded* link, edges run old→new) through the Managed gate (idem⊤). Like `emit`, it computes `dedup_key` from (`[K_sup]`, {old}, {new}) before the transact and supplies `[dedup_key, link_lock_key(home)]` — so two identical bare assertions of the same `(old, new)`, even from different homes, dedup to the first claim (Conflicts §9). It requires `is_registered_document(home)` (P0 → `HomeNotRegistered`), both endpoints resident (`old, new ∈ links` → `EndpointNotResident`), and `old ≠ new` (→ `SelfSupersession`, Df-DISC(ii) irreflexivity). Public `emit` rejects `ty ~ [K_sup]` at the surface (`SupersessionClass`, §2/§3, Conflicts §10), so **every `[K_sup]` deposit routes through `assert_sup`, `editlink`'s claim, or a DC-schema-checked `[K_sup]`-typed `editlink` successor** — ASN-0125 Df-LAY's routing commitment discharged at the surface, every stored claim schema-conformant (Df-DISC(ii)), and every `sup_fwd` edge therefore between resident, distinct links (what EL-DM's induction and EL4's `addr`/`new`/`old` accessors assume). `sup_fwd` maps `old → {(new, claim_addr)}` over the audit `[K_sup]` slice. `succs(old)` returns the `new`s whose `claim_addr ∉ nullified` (operative `succ_o`). `chain` is a bounded iterative walk over `succs` with a visited-set, halting at **sink** (no succ), **branch** (≥2 succs), or **cycle** (repeat) — the finite link set is the termination bound; `tip` returns `Sink(head)` or `Indeterminate` at branch/cycle. `is_in_chain(ty, addr, target)` is the method form of `chain(ty, addr).contains(target)` — membership in the walk's **result list** (exact denoted vertices), never a coverage test (ASN-0128 BH2).

v1's `sup_fwd` (and the whole `succs`/`chain`/`tip`/`is_in_chain`/`current` walk family) serve **only** the shipped `Supersedes` class: `succs(ty, x)`/`chain(ty, x)`/`tip(ty, x)`/`is_in_chain(ty, …)` validate `coverage_class(ty) == coverage_class(reserved(Supersedes))` and return empty (resp. `false`) for any other `ty` — and `TypeRegistry::build`'s v1 serving fence (`UnservedWalk`, §B) rejects any app `Walk` declaration, so no *registered* type's declared walk can go unserved; the class check remains as the service-scope guard on arbitrary `ty` arguments. (The general multi-BH2 path — a class-keyed `sup_fwd`, or a `type_class[ty]`-active scan with `sup_fwd` as the `[K_sup]` accelerator — lands together with lifting the fence: Open build decisions.) `current(y)` is hardwired to `[K_sup]`.

`current(y)` is BH2 generalized to sets: the operative sinks reachable from `y` via `succ_o`, returned **entire** as `Vec<CurrentMember>` — linear→1, forked→≥2, mutual-supersession standoff→0, all legitimate. **Mechanism:** `current` runs the `reach_o(y)` closure — iterating `succs` (= `sup_fwd[old]` filtered to `claim ∉ nullified`) from `y` to a fixpoint within the finite `dom(L)`; the sinks are the reached nodes with empty `succs`. Each sink's `claims` is then the **full operative `out(sink)`** — every operative `[K_sup]` claim whose `new` endpoint is that sink, *including one asserted from a node outside `reach_o(y)`* — computed per sink as `match_links([(TO, enc(slice::from_ref(sink)))], Active) ∩ type_slice(reserved(Supersedes), Active)` (the same composition M8 uses for archival `out`, §7; the R0a antichain makes the overlap an exact address match), **not** by accumulating only walk-traversed edges (which would drop an operative claim targeting the sink from outside the closure). Each `CurrentMember` carries the sink address, its **own** activity status (a member can be a current sink yet itself nullified — EL14e), and that **supporting claim set** — the inbound supersession edges that establish it as a current reading (their homes recoverable by `document_of` — EL8b; the set is empty only when no operative claim targets the sink, e.g. a `y` that is its own sink and the target of no operative claim). This discharges EL14d's *disclosure, not decision* contract: M7 hands the reader the entire set with attribution so the reader applies its own narrowing policy. M7 never fabricates a single "latest." A *per-home* latest is recoverable (claims homed on one chain are T1-ordered, EL13); a cross-home latest is not a state function and M7 does not invent one.

### 6. The spanfilade and the matcher (the M7↔M8 seam)

The spanfilade answers the one primitive both Observe and M8 stand on: **`self.stab(i, Q, v)` = link addresses whose slot-`i` endset coverage overlaps `Q`** (interval-overlap / stabbing), `Q` an M7-readable `Endset`. Per slot (the three standard slots — **exhaustive**, since the store holds only arity-3 links, §Core data model), it maps covered I-extents to the link addresses covering them; M1's **`classify_spans`** decides overlap — **overlap is `ProperOverlap | Containment | Equal`, excluding both `Separated` *and* `Adjacent`**: `Adjacent` spans abut without sharing a tumbler (`coverage([a,b)) ∩ coverage([b,c)) = ∅` — exactly the contiguous pair M1's `merge` fuses and `intersect` returns `Ok(None)` for), so an abutting region is *no* overlap and yields no match (matching it would false-positive every link whose slot coverage merely abuts the query); the decision is **never** `intersect`, which gates on level and `Err(LevelMismatch)`es on the mixed-length endpoints that M5's `resolve` runs (lifted via `iextent`) routinely produce. The baseline is a **brute-force scan** of `self.links` (trivially correct, O(n) — the bootstrap default, with the unit `SlotIndex` placeholder carrying no state, reading each endset's spans through `spans()`); the deferred interval/segment index keyed in tumbler order applies the **same** `ProperOverlap | Containment | Equal` predicate (concrete shape = Open decisions). It is rebuilt by replay — never persisted transactionally — so durability (the journal) is decoupled from query performance.

Two combiners sit on `stab`, and to remove the double-implementation noted as the design's softest seam, **both live in M7** (M8 becomes pure presentation):

- **`match_links(constraints, view)`** — findlinks' core: per constrained slot, OR (`stab`-union, which already unions overlap across the constraint endset's spans) over the slot's query spans, then AND (intersect by link identity) across slots. `constraints` carries **only the constrained slots** — an unconstrained slot is *omitted*, never supplied as an empty `Endset` (`stab(i, &empty, _) = ∅` would collapse the AND to ∅); an empty `constraints` list is *no constraint* and yields the whole `view` slice. M8's findlinks = this + cursor/count/window. (Each slot's `stab` excludes `Adjacent`, so findlinks never returns an abutment-only false positive.) `view ∈ {Audit, Active}` (a `Default` is coerced to `Active`).
- **`observe(K, F̂, Ĝ, view)`** — Observe's *subset* match (`F̂ ⊆ coverage(F) ∧ Ĝ ⊆ coverage(G)`, distinct from findlinks' overlap): start from candidates `type_slice(K, view)`, optionally prefiltered by `self.stab(1, &Endset::from_spans(F̂.iter().map(subtree_of)), Audit)` — likewise `Ĝ` on slot 2 — (`subtree_of` is total on any tumbler, so the prefilter admits the T-wide pattern domain; it is `enc`'s tumbler-level analogue, the patterns being raw `Tumbler`s; overlap is a sound *superset* of membership; `Audit` is the largest view, so any later `Active` filtering by `type_slice(K, view)` and the exact membership test stays correct) — **but a slot's prefilter is applied only when that pattern is non-empty**: an empty pattern's query endset is the empty endset and `stab(i, &empty, _)` returns `∅`, so prefiltering the common enumerate-a-type query `observe(K, [], [], Active)` (which must return all of `A_K`) would wrongly empty it; an empty `F̂` or `Ĝ` is *no constraint*, so its prefilter is skipped. Then **exact-filter** each candidate tuple by testing every pattern tumbler — `tuple.from.denotes(t)` for all `t ∈ F̂` and `tuple.to.denotes(t)` for all `t ∈ Ĝ` (`Endset::denotes` decides `t ∈ coverage(·)` as `∃ s ∈ spans : s.contains(t)`; for address-denoting endsets this is the `∃ x ∈ addrs(F): x ≼ t` prefix test; an empty pattern's clause is vacuously true — no constraint). `stab` overlap **alone over-matches** — a pattern that is a proper *ancestor* of a stored endset address overlaps it while `t ∈ coverage(F)` is false (e.g. `F̂ = {[d.0.s_L]}` would wrongly return every tuple homed at `d`), so `stab` is **only** a prefilter and the membership test is authoritative. Assemble surviving `Tuple`s. Patterns range over all of `T` — the arguments are raw `&[Tumbler]`, admitting ghost and even non-T4-valid tumblers (ASN-0086's pattern domain; `denotes` is total over `Tumbler`). `View::Default` is coerced to `Active` (raw Observe never filters — ASN-0128).

M8 reads `stab`/`match_links`/`type_slice`/`is_active`/the BH3 family across the existing `M8→M7` edge; M9 reads `observe` + BH1–BH4 — both served entirely from M7's own indexes, so **no `M7→M8` edge** and **no `M9→M8` edge** arise.

### 7. Behavior atoms BH1, BH3, BH4; default predicates; raw reads

- **BH1 read-filter** (Unary types): v1 ships exactly one BH1 type (`Retired`). `is_filtered(a)` tests membership in its active filter slice (prefix-containment over its roots); its probe `a` ranges over **all of `T`** (a raw `&Tumbler` — the same membership-predicate regime as `is_k`, ASN-0128 AD); `View::Default` rewrites `members(K')`/`targets_of` for any `K' ≠ Retired` by subtracting the filtered results — result-side only, computed lazily against the filter roots (never materialize the filtered subtree). The general multi-BH1 form unions over the BH1 set `Φ` *excluding the queried* `K'` (ASN-0128's `J ≠ K'`); with a single shipped filter that reduces to the single subtraction. **Restriction, build-enforced:** exactly one BH1 type is registered in v1 — the shipped `Retired`; `TypeRegistry::build` rejects any app `ReadFilter` declaration (`UnservedSecondFilter`, §B), so the type-less `is_filtered` is correct *by construction*, not by assumption. Lifting the rejection requires `is_filtered` to take the queried `K'` to honor the `J ≠ K'` exclusion (deferred — Open decisions). Filter-vs-walk/reverse interaction (OQ1) is left at the active reading.
- **BH3 typed-reverse-lookup** (Binary): the spanfilade *is* the reverse index — no separate structure — and the family reads the **active typed slice** `type_slice(ty, Active)` (ASN-0128's `A_K`), with `stab(·, Audit)` used *only* as an overlap prefilter and an exact-membership test authoritative (a coarse document-level or ghost argument over-matches). `sources_to(ty, target)`: candidates `self.stab(2, &enc(slice::from_ref(target)), Audit) ∩ type_slice(ty, Active)` (to-slot prefilter, restricted to active type-`ty` tuples), exact-filtered by `G.denotes(target)` (coverage match, per AM's reverse-lookup rule), collecting each survivor's `F.addrs()`. `target_of(ty, source)`: candidates `self.stab(1, &enc(slice::from_ref(source)), Audit) ∩ type_slice(ty, Active)` (from-slot prefilter, active type-`ty`), exact-filtered by `source ∈ F.addrs()` (denotation match, per AM's source-vertex rule), returning the unique survivor's single denoted target `G.addrs()` — ⊥ on none or several active type-`ty` matches, or on a unique candidate whose G is not single-address-denoting; restricting to the active type-`ty` slice is what makes "exactly one **active** K-tuple" exact. `targets_keyed(source)` joins `target_of` across *every* BH3-registered Binary type into a `CoverageClass→addr` map keyed by the public `coverage_class` (M9 indexes it via `coverage_class(ty)` — e.g. `coverage_class(reserved_type(t))` for a reserved BH3 type; M9 cannot enumerate the BH3 types itself, the registry being private to `LinkState`, which is why M7 composes the join). ASN-0125's archival `in(y)/out(x)` (M8) compose the **claim-tuple** enumeration over `[K_sup]`, *not* these endpoint projections: a claim's endpoints sit in F/G as `old`/`new`, so M8 builds `in(y) = match_links([(FROM, enc(&[y]))], view) ∩ type_slice(reserved(Supersedes), view)` (claims whose `old`/F = y) and `out(x) = match_links([(TO, enc(&[x]))], view) ∩ type_slice(reserved(Supersedes), view)` (claims whose `new`/G = x), then `readlink`s each survivor (the antichain R0a makes each `enc` overlap an exact link-address match, so no false positives). BH3's `sources_to`/`target_of` serve the **endpoint-projection** variant, which `in/out` compose only when the caller wants endpoints rather than claim tuples.
- **BH4 age-staleness** — for **app-registered idem⊥ BH4 types** (v1 ships none, so absent an app BH4 registration the family is dormant). **Domain fence — served only where declared:** `stale` and `retract_stale` REQUIRE `ty` registered with BH4 (hence idem⊥ by R-C0) — `stale` rejects with `Err(NotBh4)` (a registry lookup by `coverage_class(ty)` requiring `Behavior::Age` in the registration), and `retract_stale` rejects with `Err(TxnError::Rejected(RetractStaleError::NotBh4))` *without opening any transaction* (M3 `fork`'s no-txn-rejection precedent) — closing the foot-gun of aiming the batch nullifier at an idem⊤ class (an unfenced `retract_stale` against `[K_sup]` would mass-nullify old supersession claims). This is the converse of §B's declared ⇒ served fence. ASN-0128 R-C0 forces BH4 ⇒ idem⊥ precisely so renewal resets age: under idem⊤ a re-asserted pair returns the incumbent (the dedup hit), pinning the address to its first emission, so `age` would count from the original deposit and never reset; an idem⊥ renewal instead deposits at the frontier and restarts age at zero. For `a ∈ links`, `age(a) = home_count[origin(a)] − ordinal(a).to_u64()` — the chain index off the address (`ordinal`, M1's `&Nat`, narrowed via `to_u64()`; a homed link's ordinal is `≤ home_count[origin(a)]`, itself a `u64`, so the narrowing never overflows), the frontier off M7's own homed count (`home_count`, equal to M3's frontier index by construction, so no upward read — Conflicts §7); `age` returns `None` for a non-homed `a`. `age(a)` is a raw home-relative chain-distance — *meaningful as staleness only for an idem⊥ type*; the method itself takes no type (the fence lives on the two type-taking entries, `stale`/`retract_stale`), so a caller reads it only for tuples of a BH4 idem⊥ type. `stale(ty, h)` (post-fence) scans the **type-`ty` active slice** (`type_slice(ty, Active)`, per ASN-0128's "stale unions over every active K-tuple") for `age(a) > h`; `retract_stale(d_retr, ty, h)` (post-fence) snapshots `stale(ty, h)` at entry and issues one `nullify(d_retr, target)` per stale target — **not** one atomic transaction; each constituent's `TxnError<NullifyError>` lifts into `TxnError<RetractStaleError>` via `Nullify` (`Rejected(e) → Rejected(Nullify(e))`; `Durability`/`Poisoned` pass through). On full success it returns the `Vec<(Address, Seq)>` of emitter addresses and commit seqs (a target already nullified by a prior retraction *from this same `d_retr`* dedups to a zero-step hit, contributing its incumbent address and the base `Seq`; a target nullified by a *different* `d_retr` instead deposits a redundant but harmless `[R]` tuple, since the dedup key carries `d_retr` in its from-set); on the first `TxnError` it returns `Err`, leaving earlier nullifies **committed and durable** (no rollback — the store is append-only) — a re-run is safe, since the batch holds `d_retr` constant, so already-nullified targets from this same `d_retr` dedup to no-ops. No global counter, no clock (ordinal time only).
- **Default predicates** `is_k`/`members`/`targets_of`: `is_k(a)` is exact coverage-*membership* over the **active** K-slice — `∃ x ∈ members(ty, Active): x ≼ a` for address-denoting types (the D2 bridge), `∃ active tuple: tuple.from.denotes(a)` in general — its probe `a` ranges over **all of `T`** (a raw `&Tumbler`, per ASN-0128's membership-predicate domain; `denotes`/`is_prefix` are total over `Tumbler`) — and is **never** a `stab` overlap call (an ancestor pattern would over-match). `members`/`targets_of` return denoted addresses (`F.addrs()`/`G.addrs()`) and alone honor `View::Default` (active ∖ filtered); `is_k` is never filtered (BH1 Rewrite scope).
- **READLINK** = `links.get(a)` copied out, total, returns `None`(=⊥) on absence — *recorded, never resolved*, never dereferencing covered links (RL4/RL6); the returned `Link` carries readable endsets (RL1/RL2). The structural screen and ⊥-permanence caching of ASN-0111 are optional pre-probe fast paths; the persistent map is already the positive cache (immutability ⇒ never stale). **FOLLOWLINK** = slot lookup with the post-lookup arity bound, returning the recorded slot's coverage as a `SpanSet` (`to_spanset` of the verbatim endset — F1/F3 by construction), `Ok(empty)` vs `Err` keeping ⟨⟩≠⊥.

## Invariants & contracts

**By construction** (fall out of the append-only `links` map + M3's minting + M1's algebra):

- **Permanence / immutability** of every link value and address — L12 (ASN-0043), R2 (ASN-0086), C0/L12 (ASN-0093), ML7 (ASN-0120), RL5/RL6 (ASN-0111), F5 (ASN-0114), EL0 (ASN-0125). *Where:* no update/delete record exists; `apply_link` only inserts.
- **Uniqueness / freshness / flat prefix-antichain** — L11a (0043), R0/R0a/R1 (0086). *Where:* M3 mints monotone home-scoped siblings; M7 never chooses an address.
- **Arity-3 store** — every creation op realizes arity exactly 3 (MAKELINK standard triple, Emit_K, supersession claims; `editlink` rejects a non-arity-3 successor — a deliberate narrowing of ASN-0125 EDITop's N ≥ 3 `L3-conforming` precondition, Conflicts §11). ASN-0043 L3's N≥3 is a *type capacity* `Link::new` admits but no op exceeds; the spanfilade's three slots are exhaustive, and `type_class`/`type_slice`/`observe` satisfy ASN-0086's `|Σ.L(a)|=3` restriction without an explicit filter. *Where:* every creation op builds arity 3, and `emit_core` *defensively asserts* `value.arity() == 3` as the local store-invariant backstop.
- **Ownership derivability** (home = address projection) — L2 (0043). *Where:* M1's `document_of`/`origin`.
- **Subspace disjointness** (links in `s_L`, never colliding with `s_C` content) — L1d/L14 (0043), SD/R4 (0093/0086). *Where:* M3 keeps links in `s_L`; M7 stores only what M3 mints there.
- **Type-by-coverage / ghost permission** — L8/L9 (0043), RL3 (0111). *Where:* matching computes `coverage_class` over the readable endset spans, never dereferences a type address.
- **Class coherence (one `coverage_class`)** — every class-sensitive guard (`emit`'s `[R]`/`[K_sup]` fences, `editlink`'s DC, `nullify`'s gate) and every `apply_link` recognition (`[R]`→`nullified`, `[K_sup]`→`sup_fwd`, idem⊤→`dedup`) evaluate the one pure `coverage_class` — a coverage-equal-but-class-distinct endset is admitted and folded consistently as non-reserved, never half-recognized (§Core data model). *Where:* single function; no second classifier exists.
- **Endset order-independence & slot distinction** — L5/L6 (0043). *Where:* `Endset` is read by membership (`denotes`/`addrs`, no positional span accessor), `Link = im::Vector` is positional. Derived `Eq`/`Hash` are structural, never the L6 equality — no seam keys on them (§Core data model structural-derives contract).
- **Audit monotonicity, retraction stability, resurrection** — R3/R6a (0086), I2 (0128). *Where:* `nullified` only grows; dedup reads active.
- **Registry & idem stability** — P1/P2 (0126), R1/R2 (0128). *Where:* registry sealed at genesis; no mutator exists.
- **No sterilization through the surface** (DR) — ASN-0128. *Where:* `nullify`-only wrapper + unit-depth + P-tgt-rejecting.
- **Effect-identity** (the gate deposits exactly what an ungated emit would) — ASN-0126 `π`. *Where:* `emit_core` never mutates `value`.
- **Coverage-exactness of MAKELINK endsets** (ML1) — *Where:* recording M5's `resolve` runs' `iextent` spans verbatim, inside the txn (and `iextent`-level-uniform, so the later `coverage_class` fold cannot fault).

**By active enforcement** (M7 must guard):

- **Home existence** (L1a/0043, ML0/0120, P0): `is_registered_document(home)` (and each `d_j`) before any emit — at `makelink`/`emit`/`nullify`/`assert_sup`/`editlink` entry (the latter against `stg.base()`).
- **Home-registration even on a dedup hit** (deliberate divergence from ASN-0128 I1): `emit_core` checks `is_registered_document(home)` **ahead of the dedup short-circuit**, so an unregistered-home emit is rejected on every path — miss *and* hit. Callers cannot observe the hit/miss branch, so this unconditional check is what makes the contract portable; it strengthens I1's branch-local precondition into an M7-enforced guard (Conflict §8).
- **Type-endset non-empty** (L3/0043, ML6/0120): `e₃ ≠ ∅` (`!type_slot().is_empty()`) — MAKELINK rejects empty type resolution; managed `e₃ = K` is non-empty by `T_admissible`.
- **Shape conformance** (P3/0126, |F|=1, arity 3): `Sh-conf` in the Managed/Retraction gates (Emit_K/Nullify — *not* MAKELINK).
- **Store arity floor** (the arity-3 store invariant): `emit_core` asserts `value.arity() == 3` as the local backstop, so a misbuilt N>3 value can never land in `type_class`/`type_slice`/the 3-slot spanfilade.
- **Dedup identity = coverage** (I0/I1, 0128): the dedup key/index compare `CoverageClass` (via `coverage_class`), never value; idem-uniqueness (I1a) needs surface-routing + the M2 dedup `LockKey` (acquired by the public op pre-transact, §3).
- **`[R]` / reserved-class reservation** (R-C1, registry): `TypeRegistry::build` rejects any app key coverage-equal to a shipped class or another app key.
- **Reserved-class isolation** (Conflict §1): `build` requires every `ReservedAddrs` entry element-level with `subspace ∉ {s_C, s_L}` (`ReservedSubspaceClash`), so content-link type classes (in `s_C`) and link addresses (in `s_L`) never coverage-collide with a reserved class.
- **Declared ⇒ served (v1 serving fence)**: `TypeRegistry::build` rejects app-declared `Walk` (`UnservedWalk`) and any app `ReadFilter` (`UnservedSecondFilter`), so every registered behavior's ASN-0128 semantics are actually served by the v1 read surface (§5 walk family, §7 `is_filtered`); the rejections lift together with the parameterized multi-BH1/multi-BH2 paths (Open build decisions). The converse — **served only where declared** — is enforced at the BH4 batch surface: `stale`/`retract_stale` reject a `ty` not registered with BH4 (`NotBh4`/`RetractStaleError::NotBh4`, the latter pre-transact), so the batch nullifier can never be aimed at an idem⊤ class (§7).
- **Type-endset level-uniformity & key denotation** (`coverage_class` totality + dedup serializability): every endset reaching `coverage_class` is level-uniform — `build` requires **every** type key address-denoting (`NonAddressDenotingKey`); `emit` requires its `ty` address-denoting (`NonAddressDenotingType`, checked before any class computation); `editlink` requires its successor's type slot level-uniform (`IllFormedSuccessor`); and `enc`/`iextent` endsets plus the registered-type read contract supply the rest — so each `#start`-partition has `#reach == #start`, `canonical_key` never `LevelMismatch`es (`coverage_class` total; off-contract input **panics**, never a skipped span — §Core data model), and every idem⊤ dedup `LockKey` serializes the `Serialize`-able `Addrs` class, never the non-`Serialize` `Extents`.
- **Unit-depth retraction + P-tgt** (R-Scope/DR, 0128): `nullify` writes only `{(target,δ(1,#target))}` and rejects a non-resident/non-self target (the would-be self emitter computed via M7's own `home_count` + M1 arithmetic).
- **Supersession schema** (Df-DISC, ASN-0125): `assert_sup` rejects `old == new` (`SelfSupersession`) and a non-resident endpoint (`EndpointNotResident`); `editlink`'s DC guard rejects a `[R]`-typed successor and a schema-non-conforming `[K_sup]` successor (`DcViolation`), and rejects a non-arity-3 / empty-type / non-level-uniform-type successor (`IllFormedSuccessor`); and the public `emit` fences the class itself (`ty ~ [K_sup]` → `SupersessionClass`, Conflicts §10) — so `assert_sup`/`editlink` are the sole `[K_sup]`-writers and no write path bypasses these checks (Df-LAY's routing commitment discharged at the surface).
- **Observe is exact membership over the active typed slice** (ASN-0086): `observe`/`is_k` and the BH3 reverse family (`sources_to`/`target_of`/`targets_keyed`) match over `type_slice(ty, Active)` — testing `⊆ coverage(·)` / exact denotation via `denotes`/`addrs`/prefix, using `stab` overlap (always probed `Audit`) only as a prefilter, never as the match; an empty pattern is no constraint and its prefilter is skipped. BH3 reading the **active typed** slice (not audit, not cross-type) is what makes `target_of`'s "exactly one active K-tuple" hold.
- **Recovery** of all indexes: `rebuild_derived` rebuilds `registry` from `reserved`+`decls`, then every hint from `links`+`registry`.

**Discharged elsewhere (flag at the seam):** **Non-transcludability** (L14a, ASN-0043) — M7's *only* duty is keeping links in `s_L`; the exclusion of link addresses from V-position images lives in **M5**'s content-side referential-integrity check. Provenance R is M5's; M7 appends none.

## Dependencies & seams

**Upstream calls:**

- **M1** — pervasive: `Tumbler/Address/Span/SpanSet/CanonicalForm`. M7's `Endset` is a newtype over M1's **readable** `Span` (`start()/width()/reach()/contains()/is_level_uniform()`), so all endset reads (`spans`/`addrs`/`denotes`/overlap) are M7-local span iteration — **M1's `SpanSet` is never *stored* as an endset** (it is read-opaque). M7 uses: `subtree_of`/`from_endpoints` to build unit-depth and I-extent spans, to test address-denotation (`s == subtree_of(s.start())`), and to lift T-wide observe patterns into prefilter queries (§6); `is_level_uniform` for the editlink-successor type-slot check (`coverage_class` totality backstop); `Span::contains` for `denotes` (`∃ s : s.contains(t)`); `classify_spans` for spanfilade overlap — overlap = `ProperOverlap | Containment | Equal`, excluding both `Separated` *and* `Adjacent` (adjacent spans abut but share no tumbler) — never `intersect` (it faults on the mixed-length endpoints M5's runs routinely yield); `is_prefix` for the ≼-minimal antichain, nullified-root tests, and `is_k`/`observe`/BH3 membership; `canonical_key`/`CanonicalForm` for the `Extents` coverage-class partition (the **only** place an endset is folded to a `SpanSet`, per level-class, inside `coverage_class`, and only ever on level-uniform input); `classify`/`subspace`/`elem_addr`/`inc`/`document_of` for wf checks, `origin`/home, the reserved-isolation `subspace` test, and the BH4/P-tgt frontier arithmetic (`elem_addr(ElemPos{ doc, subspace: s_L, ordinal: 1 + home_count })` — the O(1) self-emitter, §4). (M1 exposes no `coverage` function — coverage is the query-time `denotes` projection.)
- **M2** — `transact(keys, f)` for every write (one `transact` per op, composites staging M3+M7+M5 records); `snapshot` for every read; the dedup `LockKey` supplied by the *public op* to the keyed critical section; `apply_link` plugged via `WorldState`; index rebuild via `rebuild_derived`. M7 contributes its own `Space` tag for the dedup `LockKey`; namespace alloc keys come from M3's `link_lock_key`. M7 dedupes any multi-key vec that can collide (editlink's `[d_s, d_a]`) **before** the transact — M2's `transact(keys)` makes no duplicate-key promise.
- **M3** — `mint_link(home) → (Address, M3Rec)` and `M3State::link_lock_key(home)` inside every emit composite (stage the `M3Rec`); `is_registered_document` (home/spec preconditions). The frontier is M3's; M7 reads no M3 state for BH4 (it derives the frontier from its own `home_count`).
- **M5** — `resolve(d_j, span) → Vec<Run>` for MAKELINK's V→I endset construction: M7 lifts each run with the public, total `Run::iextent()` to a **readable** (level-uniform) `Span` and forms the endset via `Endset::from_spans` (read off the txn base; the resulting content-extent class is computed per level-class). (M7 does **not** use M5's `resolve_coverage`, whose `SpanSet` result M7 could not read.) Also `stage_seat_link(&M5State, doc, link) → M5Rec` (the semantics-blind home seating, staged by MAKELINK *after* `emit_core` — the `M7→M5` edge with no return). M7 never reads link semantics back from M5 and never resolves anything itself.

**Build precondition** — `LinkState` checkpointing needs the `im` crate's `serde` feature (for `OrdMap`/`Vector`/`OrdSet`) and serde's `rc` feature (for the `Arc<ReservedAddrs>`/`Arc<Vec<TypeDecl>>` config); `Link`/`Endset`(newtype over `im::Vector<Span>`)/`Tumbler` are all `Serialize`/`DeserializeOwned`. `TypeRegistry` and `Hints` impl `Default` so serde can seed the `#[serde(skip)]` fields (replaced by `rebuild_derived` before replay).

**Downstream seams (make these explicit so M8/M9 build against them):**

- **→ M8** (`M8→M7` edge): `stab(i, Q, view)` and `match_links(constraints, view)` — both `&self` methods M8 calls as `link_state.stab(…)`/`link_state.match_links(…)`; both accept only `View::{Audit, Active}` (`Default` coerced to `Active`); the query `Q`/constraint regions are M7's readable `Endset` (M8 builds them via `enc` over resolved I-addresses, or `Endset::from_spans`), so M7 can iterate the query spans for overlap (`ProperOverlap | Containment | Equal`, never abutment); `match_links` takes **only constrained slots** (an unconstrained slot omitted, never an empty `Endset`); plus `type_slice(K, view)` (same view domain), `is_active`/`is_nullified`, the BH3 reverse family, and `readlink` — M8 layers cursors, counting, windowed pagination, projection (via M5's `project`), RETRIEVEENDSETS, and archival `in/out` on top. **When M8 feeds a §G result `Tumbler` into an address-taking §F read** (e.g. `readlink` on a `match_links` hit), the **M8 caller** lifts it to `Address` via M1's `validate` (infallible by M3's mint) before the call (§G Return-type convention; `observe`'s patterns and the `is_k`/`is_filtered` probes take raw `Tumbler`s and need no lift). **`in(y)`/`out(x)` are claim-tuple enumerations** built as `match_links([(FROM|TO, enc(&[y|x]))], view) ∩ type_slice(reserved(Supersedes), view)` + `readlink` (BH3 serves only the endpoint-projection variant — §7). **EL11(a) contextual (arrangement-gated) discovery** — `project(slot endset, d) ≠ ∅ ⟺ listed(endpoint, d)` — must follow this design's *flipped* slot convention (Conflict §2: **F = old/superseded, G = new/superseding — opposite to ASN-0125's labels**): M8 projects the **FROM** slot (e₁) through M5's `project` to test `listed(old)`, and the **TO** slot (e₂) to test `listed(new)` — *not* ASN-0125 EL11(a)'s original `e₂`-for-`old`/`e₁`-for-`new` mapping, which this design inverts. M8 owns no index and writes nothing.
- **→ M9** (`M9→M7` edge, including writes): the full PL read surface — `observe` + BH1–BH4 + `is_k`/`members`/`targets_of` — all from M7's own indexes (so M9 needs no M8 dependency). ASN-0128's BH2 atom set is complete **as methods** — `succs`/`chain`/`tip`/`is_in_chain(ty, addr, target)` (the last = membership in `chain`'s result list — exact denoted vertices, never a coverage test). M9 also passes only **registered/reserved (address-denoting) type endsets** to the typed reads (`observe`/`type_slice`/`is_k`/`members`/`targets_of`/BH3/`stale`), so each read's internal `coverage_class(ty)` stays total (§Core data model); `observe`'s patterns and the `is_k`/`is_filtered` probes are raw `&[Tumbler]`/`&Tumbler` — ASN-0086's T-wide pattern domain, ghosts and non-T4 tumblers admitted (M9 passes `addr.tumbler()` for an `Address`-valued probe). The gated write path — `emit(home, ty, …)` for `register_pred`/`certify_pd_stable`, and `emit`/`nullify` for reactive rule fires — takes an address-denoting `ty` (the reserved/registered endset), satisfying `emit`'s `NonAddressDenotingType` precondition by construction (and never the `[K_sup]` class, so the `SupersessionClass` fence never fires on M9's paths). M9 obtains the type endset via `LinkState::reserved_type(ShippedType::PredDef|PredStable)` read off a snapshot (the registry lookup is internal; `reserved_type` is the public read). When M9 consumes `targets_keyed`'s `CoverageClass→addr` map it indexes by the public `coverage_class(ty)`. The `pdef`/`pd_stable` reserved classes sit in the genesis registry: M9 coordinates their **addresses** via `ReservedAddrs` *and* their `Unary/⊤/{}` registrations via **the PredLayer registration agreement** (§B) — both are *named* M7↔M9 build-time coordination points, not pinned by any digested note, and a builder treats each as an M9-negotiated constant rather than a derived fact.
- **→ M10**: the transact-driving ops in §C/§D, each returning `(…, Seq)` post-commit; M10 surfaces `TxnError::Rejected(E)` as typed rejections. M10 forms an editlink content successor via M5's `resolve` + `Run::iextent` + `Endset::from_spans`/`enc` + `Link::new` (off any prior snapshot — ML8/EL0; §2), keeping the successor's slots level-uniform/address-denoting by construction (so `editlink`'s `IllFormedSuccessor` type-slot check passes).
- **→ engine**: `LinkState` slice, `LinkRec` record, `HasLinks` accessor, `apply_link` fold, `genesis(reserved, decls)`, `rebuild_derived`.

## Conflicts resolved

1. **MAKELINK's multi-span endsets vs the shape gate's `|F|=1` (ASN-0120 vs 0126/0128).** ASN-0126 OQ6 itself defers multi-span sources, and ASN-0120 admits them. **Resolution: two write surfaces, one store.** MAKELINK is the *open* content-link surface (wf + type-nonempty, multi-span, ghost types, no dedup, seats); Emit_K is the *managed* typed-relation surface (shape-gated, idem, `K≁R` — and, at the public op, `K≁K_sup` (§10) — no seat, **address-denoting type**). They share `links`, the indexes, and `emit_core`; only admission and (for MAKELINK) the seat differ. **Managed types occupy reserved coverage classes whose type addresses lie outside `s_C`/`s_L`** (a `build` precondition, `ReservedSubspaceClash`); **MAKELINK types resolve into `s_C`**; so the populations never coverage-collide, and behaviors degrade gracefully (`target_of`→⊥) if an app ever registered a managed type coverage-equal to a MAKELINK type (such a coincidence-class MAKELINK deposit also folds an in-memory `DedupKey` into the `dedup` hint — §1 — never serialized into a `LockKey`).

2. **Supersedes slot direction (ASN-0125 Df-DIR vs ASN-0128 S2).** ASN-0125 puts the *new* link in F ("F replaces G"); ASN-0128 puts the *old* in F ("F is superseded by G; edges run old→new"). Both agree the *edge* runs old→new and the walk goes version→head; they disagree only on which slot holds old. **Resolution: adopt ASN-0128 (F = old/superseded, G = new/superseding)** — it is the note where BH2/the walk is defined, and the decomposition endorses old→new so that `succs(old)=new` is the natural forward step and `tip` is the head. `assert_sup(home, old, new)` keeps its caller-facing meaning ("old is superseded by new") and maps `old→F, new→G` internally. This overrides ASN-0125 Df-DIR's labels — including for EL11(a) contextual discovery, where the FROM slot now carries `old` and the TO slot `new` (flagged at the M8 seam so M8 projects FROM for `listed(old)`, TO for `listed(new)`).

3. **`e₃ ≠ ∅`: store invariant vs endset type (ASN-0043 L3 vs ASN-0043 Endset).** ASN-0043's `Endset` definition (`Endset = 𝒫_fin(Span)`) admits `∅` as a valid endset, so the `Link` *type* admits `e₃=∅`; ASN-0111 in fact **affirms** L3's non-empty type slot for the read (RL1(a)/(c) — a usable type endset is always returned). L3 is a *store* invariant. **Resolution:** `Link::new` enforces only the arity floor (≥ 3 — ASN-0043 L3's *capacity*, of which creation realizes only 3, §Core data model); `e₃ ≠ ∅` is enforced at the *write boundary* (`emit_core`'s `Open`/`Managed` gate, MAKELINK's `ML6`), so READLINK's verbatim disclosure inherits a non-empty type for free without the type over-constraining.

4. **MAKELINK "distinct links always" (ML0) vs idempotent dedup (ASN-0128).** **Resolution:** dedup is *per type's idem flag*. The store never merges (NonInjectivity L11b — distinct addresses always); the idem *surface* returns an incumbent *without depositing*. Content-link types are idem⊥ (every MAKELINK deposits fresh — ML0 honored, and the emit path computes no dedup key for them at all, §1/§3); only the shipped/registered idem⊤ types dedup. The two compose without contradiction.

5. **Raw read vs bundled resolution (ASN-0111/0114).** Green bundled V-resolution into its link reads; the spec de-bundles. **Resolution:** READLINK/FOLLOWLINK are *raw* reads off `links`, taking no document handle and consulting no arrangement; V-projection (and the silent-drop it entails) lives in M8/M5. This is the boundary that makes orphaned/ghost links readable.

6. **Spanfilade placement and the double-implemented combiner (the decomposition's softest seam).** **Resolution: the spanfilade *and* the matchers (`stab`, `match_links`, `observe`) live in M7**, co-located with the link writer; M8 is pure discovery presentation over them. This restores ASN-0086's indexed Observe on M9's hot polling path and removes the duplicated per-slot-match + combiner.

7. **Frontier ownership for BH4 (M3 mints, M7 needs the frontier).** **Resolution:** M7 computes the frontier from its *own* homed-link count (`home_count`), equal to M3's frontier index by construction (every minted link is stored). No `M7→M3` read on the BH4 path (nor on `nullify`'s P-tgt self-emit computation, which builds the would-be emitter directly via `elem_addr` + `home_count`, §4); M3 stays the authoritative minter.

8. **Dedup's state-dependent home validation (ASN-0128 I1: `home` read only on the miss branch).** **Resolution:** M7 **hoists** `is_registered_document(home)` to the top of `emit_core`, ahead of every gate and dedup short-circuit, so a registered `home` is enforced on *every* emit — including a dedup hit. This is a deliberate divergence from I1's miss-only read: callers cannot evaluate the hit/miss branch, so the unconditional check is what makes M7's caller-facing contract portable (surfaced in §Invariants active enforcement). The strengthening is **provably invisible**: no M9/M10 caller relies on a hit succeeding regardless of home — `register_pred`/`certify_pd_stable` and reactive rule fires (M9) always emit at a registered residence, `assert_sup`/`editlink` and every managed app relation home at a document M10 dispatched against (already registered), and a MAKELINK/editlink content op homes at the operating document — so the unconditional check rejects no legitimate call that I1's branch-local check would have admitted.

9. **Duplicate supersession claims dedup (ASN-0125 EL6/EL8b vs ASN-0128 S2 idem⊤).** ASN-0125's `assert_sup` is a raw `Emit_{K_sup}` — EL6(i) gives "exactly one fresh address" per assertion and EL8(b) attributes each asserter by the claim's home — while ASN-0128 S2 registers `[K_sup]` **idem⊤**. **Resolution: idem⊤ governs** (S2 is where the supersession class's idempotence is declared). A duplicate identical bare `assert_sup(home, old, new)` — including one from a *different* home with the same `(old, new)`, since `DedupKey = (coverage_class([K_sup]), Addrs({old}), Addrs({new}))` excludes home (§3) — is a dedup **hit** that returns the incumbent claim and deposits nothing, refining EL6(i)'s fresh-address guarantee into "one canonical claim per `(old, new)`" and subsuming the second asserter's EL8(b) attribution into the first. `editlink` forks are **unaffected**: each `editlink` mints a fresh successor `a'`, so its claim's `new = a'` is never-before-seen, its `DedupKey` always misses, and two edits of one original yield distinct successors and distinct, co-visible claims (EL12 ForkPermanence preserved).

10. **Public Emit_K vs the supersession routing commitment (ASN-0128 I6 vs ASN-0125 Df-LAY).** ASN-0128's exposed `Emit_K` fences only the retraction class (the `K ≁ R` precondition); ASN-0125's editing layer commits that **every `[K_sup]` emission routes through `assert_sup` or `editlink`** (under DC) — the Df-DISC(ii) schema (unit-depth single-address endsets, resident endpoints, irreflexive) that EL-DM's induction, EL4's `addr`/`new`/`old` accessors, and this design's walk family (`sup_fwd`/`succs`/`chain`/`tip`/`current`) all lean on. An unfenced `emit(home, reserved(Supersedes), x, [y])` would pass the Managed gate (registered, Binary, `K ≁ R`) with no residence or irreflexivity check and deposit a schema-violating claim — `sup_fwd` would then carry edges to non-resident or self-referential endpoints, and `chain`/`tip`/`current` could report non-link "sinks." **Resolution: the public `emit` rejects `ty ~ [K_sup]` (`SupersessionClass`), the exact parallel of the `[R]` fence.** The fence lives in the public op only, so `assert_sup`/`editlink`'s internal `emit_core` `Managed` path is untouched; `assert_sup`/`editlink` are the sole `[K_sup]`-writers, every `[K_sup]` deposit (bare claim, editlink claim, or DC-schema-checked `[K_sup]`-typed successor) passes the residence/irreflexivity/DC checks, and Df-LAY's routing commitment is discharged at the surface. (MAKELINK cannot reach the class at all: its types resolve into `s_C`, and reserved addresses lie outside `s_C`/`s_L` — reserved-class isolation, §Core data model.)

11. **editlink successor arity: ASN-0125 EDITop (`ℓ' L3-conforming`, N ≥ 3) vs the arity-3 store.** ASN-0125's precondition admits any L3-conforming successor — arity ≥ 3 — while this design rejects `successor.arity() ≠ 3` (`IllFormedSuccessor`). **Resolution: a deliberate narrowing**, the editlink face of the arity-3-store commitment (§Core data model): no creation op realizes arity > 3, so the spanfilade's three slots stay exhaustive, RL2's N > 3 branch stays vacuous, and `type_class`/`type_slice`/`observe` meet ASN-0086's `|Σ.L(a)| = 3` restriction with no filter. Listed here beside §8/§9 so every deliberate note-divergence is traceable in one place; admitting an arity-N successor is a store-wide revisit, not an editlink-local relaxation.

12. **MAKELINK wf depth: ASN-0120's `#u_j ≥ 2` vs the exact depth-2 check.** ASN-0120's `wf` admits V-specs of any element-field depth ≥ 2; this design's spec test requires `#σ.start() == 2 ∧ #σ.width() == 2` exactly (§2). **Resolution: a deliberate narrowing forced by M5 as given** — M5's POOM keys and `resolve` precondition are depth-2 (`resolve` returns ⟨⟩ unless `#start == 2 ∧ #width == 2 ∧ width.get(1) == 0`), so a deeper V-spec could only ever resolve to ∅; rejecting it up front as `IllFormedSpec` is a typed rejection where accepting would only ever manufacture a silent empty endset (or a spurious `EmptyTypeResolution` on the type slot). Listed beside §8/§9/§11 so every deliberate note-divergence stays traceable in one place; admitting deeper V-positions is an M5 POOM change first, not a MAKELINK-local relaxation.

## Open build decisions

- **Spanfilade structure.** Brute-force scan of `links` (correct, O(n), the bootstrap default — `SlotIndex` the unit placeholder, §Core data model) vs an interval/segment index in tumbler order (which replaces the `SlotIndex` type behind the same field). Either way the overlap predicate is `ProperOverlap | Containment | Equal` (never `Adjacent`). Pick the index when stabbing latency under measured corpus size and query rate demands it; keep `stab`'s signature (`&self, i, query, v`) and overlap predicate stable across the swap.
- **Hint persistence.** `#[serde(skip)] hints`/`registry` + `rebuild_derived` (recommended — authoritative `links`+config, cheap checkpoints) vs serializing the indexes (faster load, larger checkpoints, a second consistency surface — and the registry cannot serialize as keyed on `CoverageClass`). Default skip+rebuild; tune M2's checkpoint cadence to bound the rebuild pass.
- **Active vs audit indexing.** Index the audit slice and filter active at query (recommended — append-only hints) vs maintain active-only indexes (removal on nullification). Dedup is the exception (active-keyed); choose whether dedup stores all-matches-filter-active (simpler) or an active incumbent (one less filter).
- **Cross-length coverage-class exactness.** The conservative per-length `Extents` partition (buildable today, over-discriminates across lengths, safe) vs a future exact cross-length coverage normal form (M1 provides none). Ship the conservative form; revisit if content-type matching shows the imprecision biting. (Note: this concerns level-uniform content extents only — managed and `enc` endsets land in the exact `Addrs` path, and a non-level-uniform span never reaches `coverage_class` by the §Core data model totality guards.)
- **Nullified representation.** A plain `OrdSet` of roots (sufficient under the unit-depth surface discipline) vs a prefix-trie over roots (needed only if a raw/off-surface range retraction is ever admitted). Default the set; gate any raw `[R]` path behind the trie.
- **Raw-deposit / import path.** Surface-only (recommended — gives idem-uniqueness, no sterilization, no born-nullified non-R tuples, schema-conformant `[K_sup]` claims (§10), full attribution, all by construction) vs an explicit import mode tolerating multiple dedup matches, non-denoting spans, and audit/active divergence (AD: non-unit spans omitted from address enumerations, visible to membership/`observe`).
- **READLINK fast paths.** Whether to run the structural screen as a pre-probe and whether to keep a ⊥-permanence negative cache (permitted only for provably-permanent absence; usually redundant against the in-memory map). Default: rely on the map, screen only untrusted boundary addresses.
- **Endset backing.** Store verbatim as M7's `Endset` newtype over `im::Vector<Span>` (decided — decomposition must be readable for the hint fold and observable per ML2/RL1) but optionally back each by a canonical span order for cheap structural equality and deterministic serialization — a representation nicety that must never become a *contract* (span order is not promised; the structural-derives contract in §Core data model makes this binding: equality is by coverage, never decomposition, and no seam keys on the derived impls).
- **Registry handle for `emit`.** §3 reads the type's registration before the transact (default: `LinkStore`'s construction-time `Arc<TypeRegistry>` cache, cloned off `kernel.snapshot().world().links()` at construction — `LinkStore::new`, §C). A stronger alternative — `emit` taking a registered **type handle** rather than a raw `&Endset` (closer to ASN-0128's K-indexed `Emit_K`) — would close the runtime-`ty` validity surface entirely (no `NonAddressDenotingType`/`NotRegistered`/`SupersessionClass` rejection possible) at the cost of an M9/M10-facing API change. Default the raw-`&Endset`+validate form; adopt the handle if the validity rejections prove burdensome.
- **Multi-BH1 `is_filtered`.** The v1 type-less `is_filtered` assumes — and `TypeRegistry::build` enforces (`UnservedSecondFilter`, §B) — the single shipped `Retired` filter. Lifting the build rejection and parameterizing `is_filtered` by the queried `K'` (to honor ASN-0128's `J ≠ K'` exclusion) land together as one change.
- **Multi-BH2 walk family.** v1's `sup_fwd` accelerates only the shipped `Supersedes` class, `succs`/`chain`/`tip`/`is_in_chain`/`current` serve the walk only for it, and `TypeRegistry::build` rejects any app `Walk` declaration (`UnservedWalk`, §B) so the gap is unreachable through the registry. Lifting that rejection lands together with either a class-keyed `sup_fwd` or the general scan path (`succs(ty,x)` over `type_class[ty]` active, `sup_fwd` as the `[K_sup]` accelerator) — symmetric to the multi-BH1 decision.
- **BH2 audit-view recovery (OQ6) and `current` reader policy.** Whether to offer an audit-view `chain`/`tip` reconstructing nullified-mid-chain history; and the default the client applies to set-valued `current` (per-home-latest, curator-trust, drop-retracted) — M7 discloses, the consumer decides.
