# M7 — Interface (for dependents)

M7 owns the authoritative, append-only store of links and typed relations — the single writer and single source of truth for link values, plus every read of structural relation state that does not require V-resolution.

## Public interface

**Foreign types** (consumed, not defined here): `Tumbler/Address/Span/SpanSet/CanonicalForm/Nat` (M1); `Kernel/Snapshot/LockKey/Seq/TxnError/WorldState/Staging` (M2); `M3Rec/HasM3/MintError` (M3); `M5Rec/HasM5/VSpec/Run` (M5).

Pure reads are methods on the opaque read-carrier `LinkState` (over any `Snapshot`); transact-driving ops hang off `LinkStore<'k,W>` (holds `&'k Kernel<W>` plus a construction-time `Arc<TypeRegistry>` cache of the genesis-immutable registry), generic over `W`. Slots are 1-based: `FROM=1, TO=2, TYPE=3`. Subspace constants: `s_C = 1` (content), `s_L = 2` (link).

### Carrier types — Endset, Link, address encoding

```rust
#[derive(Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct Endset(im::Vector<Span>);   // M7-owned READABLE span sequence, held verbatim (NOT M1's SpanSet)

impl Endset {
    pub fn empty() -> Endset;                                          // ⟨⟩ (distinct from any zero-width span)
    pub fn from_spans(spans: impl IntoIterator<Item = Span>) -> Endset; // verbatim
    pub fn spans(&self) -> impl Iterator<Item = &Span>;               // the readable decomposition
    pub fn len(&self) -> usize;                                       // # spans
    pub fn is_empty(&self) -> bool;                                   // == ⟨⟩
    pub fn denotes(&self, t: &Tumbler) -> bool;                       // t ∈ coverage: ∃ s ∈ spans : s.contains(t)
    pub fn addrs(&self) -> impl Iterator<Item = &Tumbler>;            // start of each unit-depth span
}

#[derive(Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Link { slots: im::Vector<Endset> }   // arity = slots.len() ≥ 3; positional accessors only

impl Link {
    pub fn new(slots: impl IntoIterator<Item = Endset>) -> Option<Link>;  // None ⇔ arity < 3
    pub fn arity(&self) -> usize;                       // |L| ≥ 3
    pub fn slot(&self, i: usize) -> Option<&Endset>;    // 1-based; None iff i < 1 ∨ i > arity
    pub fn from_slot(&self) -> &Endset;                 // e₁ (FROM=1)
    pub fn to_slot(&self) -> &Endset;                   // e₂ (TO=2)
    pub fn type_slot(&self) -> &Endset;                 // e₃ (TYPE=3)
}

/// Canonical address-set encoding (AD): one unit-depth span per address; enc(X).addrs() = X.
pub fn enc(addrs: &[Address]) -> Endset;   // single-&Address callers pass slice::from_ref(addr)

#[derive(Clone, PartialEq, Eq, Hash)]      // NOT Serialize (Extents wraps M1's non-Serialize CanonicalForm)
pub enum CoverageClass {
    Addrs(im::OrdSet<Tumbler>),                // address-denoting (exact ≼-minimal antichain)
    Extents(im::OrdMap<usize, CanonicalForm>), // per-length canonical coverage — content extents
}

/// PURE coverage class of an endset (type / I0 identity by coverage equality, never decomposition).
/// PUBLIC so M9 can key targets_keyed's map via coverage_class(ty). Total on level-uniform input.
pub fn coverage_class(e: &Endset) -> CoverageClass;
```

### A. Engine-plug surface

```rust
#[derive(Clone, Serialize, Deserialize)]
pub struct LinkState { /* opaque: authoritative links map + genesis type config + recomputable hints */ }

pub trait HasLinks { fn links(&self) -> &LinkState; }

/// The ONE authoritative delta — every write is a deposit of an immutable link at a fresh address.
#[derive(Clone, Serialize, Deserialize)]
#[non_exhaustive]
pub enum LinkRec { Emit { addr: Tumbler, value: Link } }

impl LinkState {
    /// Validate decls against reserved, seal both as genesis config, start links = ∅.
    pub fn genesis(reserved: ReservedAddrs, decls: Vec<TypeDecl>) -> Result<LinkState, RegistryError>;
    /// Pure/total/deterministic M2 fold; applied exactly once per committed record.
    pub fn apply_link(&self, r: &LinkRec) -> LinkState;
    /// Runs once at load, BEFORE replay: rebuild registry from reserved+decls, then hints from links+registry.
    pub fn rebuild_derived(self) -> LinkState;
}
```

### B. Type registry (immutable, construction-time)

```rust
#[derive(Clone, Copy, PartialEq, Eq, Serialize, Deserialize)] pub enum Shape { Unary, Binary, Multi }
#[derive(Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub enum Behavior { ReadFilter, Walk, ReverseLookup, Age } // BH1..4
#[derive(Clone, Serialize, Deserialize)]
pub struct Registration { pub shape: Shape, pub idem: bool, pub behaviors: im::OrdSet<Behavior> }

#[derive(Clone, Serialize, Deserialize)]
pub struct TypeDecl { pub key: Endset, pub reg: Registration }  // app-declared type; key names the coverage class
#[derive(Clone, Serialize, Deserialize)]
pub struct ReservedAddrs {            // the five reserved type addresses — M9-coordinated parameters
    pub pred_def: Address, pub pred_stable: Address,
    pub retired: Address,  pub supersedes: Address, pub retraction: Address,
}
pub enum RegistryError {
    KeyCollision, EmptyKey, BadBehavior, ReservedClassClash, ReservedSubspaceClash, NonAddressDenotingKey,
}

impl TypeRegistry {
    /// Validate-once-or-fail; seeds the five shipped types before app decls.
    pub fn build(reserved: ReservedAddrs, decls: Vec<TypeDecl>) -> Result<TypeRegistry, RegistryError>;
    pub fn registration(&self, class: &CoverageClass) -> Option<&Registration>;  // internal lookup
    pub fn reserved(&self, t: ShippedType) -> &Endset;   // the genesis-fixed type endset for a shipped class
}
impl Default for TypeRegistry { /* the empty registry — serde-seeds the #[serde(skip)] field */ }
pub enum ShippedType { Retired, Supersedes, Retraction, PredDef, PredStable }
```

**Behavior↔shape compatibility** the registry enforces (`BadBehavior` on violation): BH1 (ReadFilter) ⇒ Unary; BH2 (Walk) ⇒ Binary; BH3 (ReverseLookup) ⇒ Binary; BH4 (Age) ⇒ idem = ⊥ (any shape). Shipped registrations: `Retired = Unary/⊤/{ReadFilter}`, `Supersedes = Binary/⊤/{Walk}`, `Retraction = Binary/⊤/{}`; **PredLayer registration agreement** (an M7↔M9 build-time constant, not a derived fact): `PredDef = Unary/⊤/{}`, `PredStable = Unary/⊤/{}`.

### C. Write — open content links (MAKELINK)

```rust
impl<'k,W> LinkStore<'k,W>
where W: WorldState + HasLinks + HasM3 + HasM5,
      W::Record: From<LinkRec> + From<M3Rec> + From<M5Rec>
{
    /// Resolve three V-spec-sets to content I-extent endsets, mint a fresh home-scoped link, deposit, seat.
    /// NO shape gate, NO idem dedup (distinct links always), NO provenance.
    pub fn makelink(&self, home: &Address, from: Vec<VSpec>, to: Vec<VSpec>, ty: Vec<VSpec>)
        -> Result<(Address, Seq), TxnError<MakeLinkError>>;
}
pub enum MakeLinkError { HomeNotRegistered, IllFormedSpec, EmptyTypeResolution, Mint(MintError), Seat(SeatError) }
```

### D. Write — managed typed relations

```rust
impl<'k,W> LinkStore<'k,W>
where W: WorldState + HasLinks + HasM3, W::Record: From<LinkRec> + From<M3Rec>
{
    /// Emit_K: gated typed-relation emission. REQUIRES ty address-denoting. Shape-gated (registered ∧
    /// shape-conformant ∧ K≁R). idem(K)=⊤ ⇒ dedup against ACTIVE view; hit returns incumbent, commits NOTHING.
    /// Does NOT seat. |F|=1 forced, to cardinality shape-checked, ty stored verbatim.
    pub fn emit(&self, home: &Address, ty: &Endset, from: &Address, to: &[Address])
        -> Result<(Address, Seq), TxnError<EmitError>>;

    /// Nullify_Binary: the SOLE retraction path. Emits an [R] tuple. P-tgt enforced (target a resident
    /// link OR the call's own fresh emitter). idem⊤.
    pub fn nullify(&self, home: &Address, target: &Address)
        -> Result<(Address, Seq), TxnError<NullifyError>>;

    /// assert_sup: emit "old is superseded by new". Idem⊤. Requires home registered, both endpoints
    /// resident links, and old ≠ new (irreflexive).
    pub fn assert_sup(&self, home: &Address, old: &Address, new: &Address)
        -> Result<(Address, Seq), TxnError<AssertSupError>>;

    /// editlink: ONE composite — allocate a fresh successor link (value supplied; M10 builds via Link::new,
    /// arity 3), then assert it supersedes original. Successor born UNSEATED. Rejects arity ≠ 3, empty or
    /// non-level-uniform type slot, retraction-typed successor; schema-conforms a claim-typed one.
    pub fn editlink(&self, original: &Address, successor: Link, d_s: &Address, d_a: &Address)
        -> Result<(Address /*successor*/, Address /*claim*/, Seq), TxnError<EditLinkError>>;

    /// BH4 batch tooling (app-registered idem⊥ BH4 ty — v1 ships none, so dormant): nullify every stale
    /// tuple. NOT atomic — a sequence of nullify transacts; on first TxnError leaves earlier nullifies committed.
    pub fn retract_stale(&self, d_retr: &Address, ty: &Endset, horizon: u64)
        -> Result<Vec<(Address, Seq)>, TxnError<NullifyError>>;
}
pub enum EmitError      { HomeNotRegistered, NotRegistered, ShapeViolation, RetractionClass, NonAddressDenotingType, Mint(MintError) }
pub enum NullifyError   { HomeNotRegistered, BadTarget, Mint(MintError) }
pub enum AssertSupError { HomeNotRegistered, EndpointNotResident, SelfSupersession, Mint(MintError) }
pub enum EditLinkError  { OriginalNotResident, HomeNotRegistered, IllFormedSuccessor, DcViolation, Mint(MintError) }
```

### E. Raw reads — pure, arrangement-independent

```rust
impl LinkState {
    pub fn readlink(&self, a: &Address) -> Option<Link>;             // Σ.L(a) verbatim (readable endsets), or None (=⊥)
    /// Ok(spans) coverage-exact to slot i; Ok(SpanSet::empty()) = ⟨⟩ (valid-but-empty); Err = ⊥ (link/slot absent).
    pub fn followlink(&self, a: &Address, i: usize) -> Result<SpanSet, Invalid>;
}
pub struct Invalid;
```

### F. Typed-relation reads & the PL surface for M9

```rust
pub enum View { Audit, Active, Default }    // Default meaningful only on members/targets_of; coerced to Active elsewhere
pub struct Tuple { pub addr: Address, pub from: Endset, pub to: Endset }
pub enum Tip { Sink(Address), Indeterminate }   // ⊥ at branch or cycle
/// EL14 disclosure-not-decision: member, its OWN activity, and the operative [K_sup] claims establishing it.
pub struct CurrentMember { pub member: Address, pub active: bool, pub claims: Vec<Address> }

impl LinkState {
    pub fn observe(&self, ty: &Endset, from_pat: &[Address], to_pat: &[Address], v: View) -> Vec<Tuple>; // exact ⊆-coverage; Default→Active
    pub fn is_k(&self, ty: &Endset, a: &Address) -> bool;                 // D2 (exact active coverage-membership)
    pub fn members(&self, ty: &Endset, v: View) -> Vec<Address>;          // D1
    pub fn targets_of(&self, ty: &Endset, x: &Address, v: View) -> Vec<Address>;  // D3
    pub fn is_active(&self, a: &Address) -> bool;  pub fn is_nullified(&self, a: &Address) -> bool;
    pub fn is_filtered(&self, a: &Address) -> bool;                       // v1: single shipped BH1 (Retired)
    pub fn succs(&self, ty: &Endset, x: &Address) -> Vec<Address>;        // BH2 walk — v1 serves only shipped Supersedes; empty for other ty
    pub fn chain(&self, ty: &Endset, x: &Address) -> Vec<Address>;   pub fn tip(&self, ty: &Endset, x: &Address) -> Tip;
    pub fn sources_to(&self, ty: &Endset, target: &Address) -> Vec<Address>;     // BH3: active type-ty slice
    pub fn target_of(&self, ty: &Endset, source: &Address) -> Option<Address>;   // BH3: ⊥ unless exactly one active type-ty tuple, single-addr G
    pub fn targets_keyed(&self, source: &Address) -> im::HashMap<CoverageClass, Address>;  // BH3: joined over all BH3 Binary types; key via coverage_class(ty)
    pub fn age(&self, a: &Address) -> Option<u64>;   pub fn stale(&self, ty: &Endset, h: u64) -> Vec<Address>;
    pub fn current(&self, y: &Address) -> Vec<CurrentMember>;             // set-valued disclosure (EL14); hardwired to [K_sup]
    pub fn reserved_type(&self, t: ShippedType) -> &Endset;              // M9 reads PredDef/PredStable here
}
```

`is_in_chain(ty, addr, target)` is **not** a method — caller-derive: `chain(ty, addr).contains(target)`.

### G. Discovery primitives for M8

```rust
impl LinkState {
    /// Links whose slot-i coverage OVERLAPS query (overlap = ProperOverlap | Containment | Equal — NOT Adjacent).
    /// query is M7's READABLE Endset. v ∈ {Audit, Active} ONLY (Default coerced to Active).
    pub fn stab(&self, i: usize, query: &Endset, v: View) -> im::OrdSet<Tumbler>;
    /// AND-of-(per-slot overlap). constraints lists ONLY constrained slots (omit unconstrained; never an empty
    /// Endset); empty constraints ⇒ whole v slice. v ∈ {Audit, Active} ONLY (Default coerced).
    pub fn match_links(&self, constraints: &[(usize, Endset)], v: View) -> im::OrdSet<Tumbler>;
    pub fn type_slice(&self, ty: &Endset, v: View) -> im::OrdSet<Tumbler>;    // L_K (Audit) / A_K (Active); v ∈ {Audit, Active}
}
```

**Return-type convention.** §G returns raw `im::OrdSet<Tumbler>` (the index's native key) and accepts only `View::{Audit, Active}` (a `Default` is coerced to `Active`). Query inputs are M7's readable `Endset` (build via `enc`/`Endset::from_spans`). §F caller-facing reads return validated `Address` (and `Tuple`/`CurrentMember`). When feeding a §G result key into a §F read, the **caller** lifts the `Tumbler → Address` via M1's `validate` (infallible by M3's mint) before the §F call.

## Caller contracts & obligations

**Writes** (`LinkStore<'k,W>` — return `(…, Seq)` post-commit; M10 surfaces `TxnError::Rejected(E)` as typed rejections):

- `makelink`: caller passes a registered `home` and well-formed V-specs — each a depth-2 content V-position (`#start==2 ∧ start.get(1)==s_C ∧ #width==2 ∧ width.get(1)==0`, else `IllFormedSpec`); type resolution must be non-empty (`EmptyTypeResolution`). No dedup — every call deposits a fresh distinct link and seats it in `home`. Errors: `HomeNotRegistered/IllFormedSpec/EmptyTypeResolution/Mint/Seat`.
- `emit`: `home` registered; `ty` **address-denoting** (else `NonAddressDenotingType`), registered, shape-conformant (`|from|=1` always; `to` cardinality per shape), `K≁R`. On an idem⊤ type a dedup hit returns the incumbent address with the base `Seq` and commits nothing. Does NOT seat. Errors: `HomeNotRegistered/NotRegistered/ShapeViolation/RetractionClass/NonAddressDenotingType/Mint`.
- `nullify`: sole retraction path. `home` registered; `target` is a resident link OR this call's own fresh emitter (else `BadTarget`). idem⊤ — re-retracting the same target from the same home dedups. Errors: `HomeNotRegistered/BadTarget/Mint`.
- `assert_sup`: `home` registered; both `old`,`new` resident links; `old ≠ new` (`SelfSupersession`). idem⊤ keyed on `(coverage_class([K_sup]), {old}, {new})` — a duplicate `(old,new)` *even from a different home* dedups to the first claim. Errors: `HomeNotRegistered/EndpointNotResident/SelfSupersession/Mint`.
- `editlink`: caller supplies `successor: Link` pre-formed (arity 3, type slot non-empty and level-uniform — else `IllFormedSuccessor`); `original` resident; `d_s`/`d_a` registered. DC guard rejects a retraction-typed successor and a schema-non-conforming `[K_sup]`-typed one (`DcViolation`). Returns `(successor, claim, Seq)` atomically; `original` untouched. Build the content successor via M5 `resolve` + `Run::iextent` + `Endset::from_spans`/`enc` + `Link::new`, off any prior snapshot (recorded I-addresses are permanent). Errors: `OriginalNotResident/HomeNotRegistered/IllFormedSuccessor/DcViolation/Mint`.
- `retract_stale`: dormant in v1 (no BH4 idem⊥ type shipped). **NOT atomic** — a sequence of `nullify` transacts. Full success → `Vec<(Address, Seq)>`; first `TxnError` → `Err`, with earlier nullifies committed and durable; a re-run with the same `d_retr` is safe.
- Across all writes: the caller never chooses an address; M3 mints fresh home-scoped siblings, so every returned `Address` is **T4-valid** and the link value is **permanent/immutable** (no update or delete exists).

**Raw reads** (`LinkState`, `&self` over any Snapshot):

- `readlink(a)`: `Some(Link)` with readable endsets, or `None` (=⊥) on absence. Total; recorded, never V-resolved; never dereferences covered links.
- `followlink(a, i)`: `Ok(SpanSet)` coverage-exact to slot `i`; `Ok(SpanSet::empty())` is a valid-but-empty endset ⟨⟩; `Err(Invalid)` means link or slot absent (⊥). ⟨⟩ ≠ ⊥ is unforgeable.

**Typed reads / PL surface** (`LinkState`):

- `observe`: exact ⊆-coverage match over the active typed slice; `Default→Active`; an empty `from_pat`/`to_pat` is no constraint; patterns range over all of T (ghosts welcome); caller passes a registered/reserved (address-denoting) `ty`.
- `is_k`/`members`/`targets_of` (D2/D1/D3): `members`/`targets_of` alone honor `View::Default` (active ∖ filtered); `is_k` is never filtered. Caller passes an address-denoting `ty`.
- `is_active`/`is_nullified`: tuple status by address. `is_filtered(a)`: correct only while exactly one BH1 type (`Retired`) is registered (v1).
- `succs`/`chain`/`tip`: BH2 walk; v1 serves only the shipped `Supersedes` class — empty/trivial for any other `ty`. `tip` is `Sink(head)` or `Indeterminate` (branch/cycle). Derive is_in_chain as `chain(ty, addr).contains(target)`.
- `sources_to`/`target_of`/`targets_keyed`: BH3 over the active type-`ty` slice. `target_of` returns `None` unless exactly one active type-`ty` tuple denotes `source` with a single-address G. `targets_keyed` is keyed by `coverage_class(ty)` over all BH3 Binary types — consumer indexes with `coverage_class(reserved_type(t))` etc.
- `age(a)`: `Some(u64)` home-relative chain-distance, or `None` for a non-homed `a`; meaningful as staleness only for an idem⊥ BH4 type. `stale(ty, h)`: active type-`ty` tuples with age > h. (Both dormant in v1.)
- `current(y)`: set-valued disclosure (EL14), hardwired to `[K_sup]` — linear→1, fork→≥2, mutual standoff→0. Each `CurrentMember` carries the sink address, its own activity (a sink may itself be nullified), and the operative inbound `[K_sup]` claims (homes recoverable via M1's `document_of`). M7 discloses; the consumer narrows — M7 invents no single "latest."
- `reserved_type(t)`: the genesis-fixed endset for a shipped class (M9 reads `PredDef`/`PredStable`).
- `coverage_class(e)`: **total only on level-uniform input** — caller passes registered/reserved address-denoting types or `iextent`-built content endsets; it is the lone public way to key a `CoverageClass` map.

**Discovery primitives** (`LinkState`, for M8):

- `stab`/`match_links`/`type_slice`: return raw `im::OrdSet<Tumbler>`; accept only `View::{Audit, Active}` (Default coerced). Query/constraint regions are M7's readable `Endset` (build via `enc`/`Endset::from_spans`). `match_links` carries ONLY constrained slots (omit an unconstrained slot — never an empty `Endset`, which empties the AND); empty `constraints` ⇒ whole `v` slice. Overlap excludes `Adjacent` (abutment is not a match). Lift a result `Tumbler → Address` via `validate` before any §F read.

**Engine plug:**

- `genesis(reserved, decls)`: validate-once-or-fail → `Err(RegistryError)` on `KeyCollision/EmptyKey/BadBehavior/ReservedClassClash/ReservedSubspaceClash/NonAddressDenotingKey`. Each `ReservedAddrs` entry must be element-level with `subspace ∉ {s_C, s_L}`; every `TypeDecl.key` must be address-denoting and not coverage-equal to a reserved/other app class. Starts `links = ∅`. (`TypeRegistry::build` is the same validation standalone; the normal entry is `genesis`.)
- `apply_link(r)`: pure/total/deterministic — engine dispatches `Record::Links(x) => world.links().apply_link(x)`; applied exactly once per committed record — do **not** code it idempotent.
- `rebuild_derived(self)`: call once at load, before replay.
- The PredLayer registration agreement (`PredDef`/`PredStable` each `Unary/⊤/{}`) and the `reserved.pred_def`/`reserved.pred_stable` addresses are M7↔M9 build-time constants — treat as M9-negotiated, not local edits.

**Carrier-type constructors/accessors:**

- `Endset`: `empty`/`from_spans` build; `spans`/`addrs`/`denotes`/`len`/`is_empty` read. Equality is by the verbatim span sequence; coverage is a query-time projection via `denotes`.
- `Link::new(slots)`: `None` iff arity < 3. `slot(i)` 1-based, `None` iff `i < 1 ∨ i > arity`. `from_slot/to_slot/type_slot` = e₁/e₂/e₃.
- `enc(addrs)`: canonical address-set encoding; `enc(X).addrs() = X`; single-`&Address` callers pass `slice::from_ref(addr)`.

## Seams exposed downstream

- **→ M8** (`M8→M7` edge): `stab(i, Q, view)`, `match_links(constraints, view)`, `type_slice(K, view)` (all `&self`; only `View::{Audit, Active}`, Default coerced), `is_active`/`is_nullified`, the BH3 reverse family, and `readlink`. Query/constraint regions are M7's readable `Endset` (M8 builds via `enc`/`from_spans`); `match_links` takes only constrained slots. M8 layers cursors, counting, windowed pagination, projection (via M5's `project`), RETRIEVEENDSETS, and archival `in/out` on top — owning no index, writing nothing. M8 lifts a §G `Tumbler` to `Address` via `validate` before a §F read. Archival `in(y)/out(x)` are claim-tuple enumerations: `match_links([(FROM|TO, enc(&[y|x]))], view) ∩ type_slice(reserved(Supersedes), view)` + `readlink`. **EL11(a) contextual discovery uses this design's FLIPPED slot convention (F = old/superseded, G = new/superseding):** M8 projects the **FROM** slot (e₁) for `listed(old)` and the **TO** slot (e₂) for `listed(new)`.
- **→ M9** (`M9→M7` edge, incl. writes): the full PL read surface — `observe` + BH1–BH4 + `is_k`/`members`/`targets_of` — served entirely from M7's own indexes (no M8 dependency). Derive `is_in_chain(ty, addr, target)` as `chain(ty, addr).contains(target)`. M9 passes only registered/reserved (address-denoting) type endsets to every typed read (keeping each internal `coverage_class(ty)` total). Gated writes `emit`/`nullify` take an address-denoting `ty`. M9 obtains type endsets via `reserved_type(ShippedType::PredDef|PredStable)`; indexes `targets_keyed`'s map by `coverage_class(ty)`. The `pdef`/`pd_stable` classes are M7↔M9 build-time coordination points — addresses via `ReservedAddrs`, `Unary/⊤/{}` registrations via the PredLayer registration agreement.
- **→ M10**: the transact-driving ops in §C/§D, each returning `(…, Seq)` post-commit; M10 surfaces `TxnError::Rejected(E)` as typed rejections. M10 forms an editlink content successor via M5 `resolve` + `Run::iextent` + `Endset::from_spans`/`enc` + `Link::new` (off any prior snapshot — recorded I-addresses are permanent).
- **→ engine**: the `LinkState` slice, `LinkRec` record, `HasLinks` accessor, `apply_link` fold, `genesis(reserved, decls)`, and `rebuild_derived`. The engine implements `HasLinks`, `From<LinkRec> for Record`, and dispatches the fold; M7 names neither `World` nor `Record`. Build precondition: the `im` crate's `serde` feature + serde's `rc` feature; `Link`/`Endset`/`Tumbler` are `Serialize`/`DeserializeOwned`; `TypeRegistry` and `Hints` impl `Default` for the `#[serde(skip)]` fields.
- **→ everyone**: every `Address` M7 returns is **T4-valid**; link values are **permanent and immutable**; `View::Default` is meaningful only on `members`/`targets_of`, coerced to `Active` everywhere else.

## Boundary — NOT provided here

- Address minting and home-existence/ownership facts — **M3** (M7 *calls* `mint_link`, reads `is_registered_document`).
- The V→I arrangement and home seating mechanism — **M5** (M7 *calls* the semantics-blind `resolve`/`stage_seat_link`; never interprets arrangement, never reads link semantics back).
- Ordering, durability, recovery — **M2**.
- The provenance relation R — **M5** (link placement is deliberately uncoupled from R; M7 appends no R).
- Non-transcludability enforcement — **M5**'s content-side referential-integrity check (M7's only duty is to keep links in `s_L`).
- Indexed discovery *presentation* — findlinks/count/windowed-pagination/projection/RETRIEVEENDSETS and archival `in/out` — **M8** (executes over M7's spanfilade across the `M8→M7` edge; no `M7→M8` or `M9→M8` edge exists).
- No `coverage` function — coverage is the query-time `denotes` projection, not a stored value.
