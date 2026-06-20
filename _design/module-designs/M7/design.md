# M7 — Link & Relation Store — Build-Spec Design

## Purpose & boundary

M7 owns the **authoritative, append-only store of links and typed relations** — every connection in the docuverse — keyed by the link's own permanent address, together with the recomputable **coverage indexes** that answer "which links touch this region." It does one thing: *be the single writer and the single source of truth for link values, and serve every read of structural relation state that does not require V-resolution.* It owns the write surfaces (MAKELINK, Emit/Nullify, assert_sup/editlink), the raw reads (READLINK, FOLLOWLINK), the typed-relation observers (Observe + the four behavior atoms BH1–BH4), the immutable type/shape registry, idempotent de-duplication, and the spanfilade.

It does **not** own: address minting or the home-existence/ownership facts (**M3** — M7 *calls* `mint_link`, reads `is_registered_document`); the V→I arrangement or the home seating mechanism (**M5** — M7 *calls* the semantics-blind `resolve_coverage`/`stage_seat_link`, never interpreting arrangement); ordering/durability/recovery (**M2**); the **provenance relation R** (M5 — link placement is deliberately *uncoupled* from R, ASN-0047 J-LV, so M7 touches no R); **non-transcludability** enforcement (M5's content-side referential-integrity check — M7's only duty is to keep links in `s_L`); and **indexed discovery *presentation*** — findlinks/count/windowed-pagination/projection/RETRIEVEENDSETS (**M8**, which executes over M7's spanfilade across the `M8→M7` edge). The split between M7 and M8 is *index ownership and matching* (M7) vs *cursoring/counting/projecting* (M8).

## Public interface

Types `Tumbler/Address/Span/SpanSet/CanonicalForm/Nat` are M1's; `Kernel/Snapshot/LockKey/Seq/TxnError/WorldState` are M2's; `M3Rec/HasM3/MintError`, `M5Rec/HasM5/VSpec` are M3/M5's. Pure reads are methods on `LinkState` over any `Snapshot`; transact-driving ops hang off `LinkStore<'k,W>` (holds `&'k Kernel<W>`) and are generic over `W` per the engine composition contract. Slots are 1-based: `FROM=1, TO=2, TYPE=3`.

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
    pub fn genesis(registry: TypeRegistry) -> LinkState;     // links = ∅; registry sealed
    pub fn apply_link(&self, r: &LinkRec) -> LinkState;       // pure/total/deterministic; maintains ALL hints
    pub fn rebuild_derived(self) -> LinkState;                // re-seeds every hint from `links`+`registry`
}
```

### B. Type registry (immutable, construction-time)

```rust
#[derive(Clone, Copy, PartialEq, Eq, Serialize, Deserialize)] pub enum Shape { Unary, Binary, Multi }
#[derive(Clone, Copy, PartialEq, Eq, Serialize, Deserialize)] pub enum Behavior { ReadFilter, Walk, ReverseLookup, Age } // BH1..4
pub struct Registration { pub shape: Shape, pub idem: bool, pub behaviors: im::OrdSet<Behavior> }

pub struct TypeDecl { pub key: Endset, pub reg: Registration }  // app-declared type; key names the coverage class
pub enum RegistryError { KeyCollision, EmptyKey, BadBehavior, ReservedClassClash }

impl TypeRegistry {
    /// Validate-once-or-fail (C0 + R-C0 + R-C1). Seeds the five shipped types BEFORE app decls;
    /// rejects any app key coverage-equal to another app key OR to a reserved shipped class.
    pub fn build(reserved: ReservedAddrs, decls: Vec<TypeDecl>) -> Result<TypeRegistry, RegistryError>;
    pub fn registration(&self, class: &CoverageClass) -> Option<&Registration>;
    pub fn reserved(&self, t: ShippedType) -> &Endset;   // the genesis-fixed type endset for a shipped class
}
pub enum ShippedType { Retired, Supersedes, Retraction, PredDef, PredStable }
```

`ReservedAddrs` carries the five reserved type addresses (the `pdef`/`pd_stable` pair coordinated with M9, the `[K_ret]/[K_sup]/[R]` triple) — parameters in the manner of `s_C`/`s_L`. Shipped registrations are fixed: `Retired = Unary/⊤/{ReadFilter}`, `Supersedes = Binary/⊤/{Walk}`, `Retraction = Binary/⊤/{}`, `PredDef = Unary/⊤/{}`, `PredStable = Unary/⊤/{}`.

### C. Write — open content links (ASN-0120 MAKELINK)

```rust
impl<'k,W> LinkStore<'k,W>
where W: WorldState + HasLinks + HasM3 + HasM5,
      W::Record: From<LinkRec> + From<M3Rec> + From<M5Rec>
{
    /// Resolve three V-spec-sets to content I-coverage endsets, require the type endset non-empty,
    /// mint a fresh home-scoped link, deposit the standard triple, seat it in `home`'s link subspace.
    /// ONE M2 composite. NO shape gate, NO idem dedup (distinct links always — ML0). NO provenance.
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
    /// (zero-step). Does NOT seat. `from` is a single address (|F|=1 forced); `to` cardinality is
    /// shape-checked. Used by M9 (pdef/pd_stable, rule fires) and managed app relations.
    pub fn emit(&self, home: &Address, ty: &Endset, from: &Address, to: &[Address])
        -> Result<(Address, Seq), TxnError<EmitError>>;

    /// Nullify_Binary: the SOLE retraction path. Emits an [R] tuple, canonical from-fill,
    /// unit-depth to-span at `target`. P-tgt enforced as a REJECTING precondition (target is a
    /// resident link OR the call's own fresh emitter) ⇒ sterilization unreachable through this surface.
    pub fn nullify(&self, home: &Address, target: &Address)
        -> Result<(Address, Seq), TxnError<NullifyError>>;

    /// assert_sup: emit "old is superseded by new" — F=enc({old}), G=enc({new}), type [K_sup]
    /// (slot convention per Conflicts §2). Idem⊤. Both endpoints must be resident links.
    pub fn assert_sup(&self, home: &Address, old: &Address, new: &Address)
        -> Result<(Address, Seq), TxnError<AssertSupError>>;

    /// editlink: allocate a fresh successor link (value supplied directly), then assert it
    /// supersedes `original` — ONE composite. Successor born UNSEATED. DC guard: reject a
    /// retraction-typed successor; schema-conform a claim-typed one.
    pub fn editlink(&self, original: &Address, successor: Link, d_s: &Address, d_a: &Address)
        -> Result<(Address /*successor*/, Address /*claim*/, Seq), TxnError<EditLinkError>>;

    /// BH4 batch tooling: nullify every stale tuple of `ty` (age > horizon), stale set snapshotted
    /// at entry. NOT atomic — a sequence of `nullify` transacts (ASN-0128 BH4).
    pub fn retract_stale(&self, d_retr: &Address, ty: &Endset, horizon: u64)
        -> Result<Vec<(Address, Seq)>, TxnError<NullifyError>>;
}
pub enum EmitError { HomeNotRegistered, NotRegistered, ShapeViolation, RetractionClass }
pub enum NullifyError { HomeNotRegistered, BadTarget }
```

### E. Raw reads (ASN-0111 / ASN-0114) — pure, arrangement-independent

```rust
impl LinkState {
    pub fn readlink(&self, a: &Address) -> Option<Link>;             // Σ.L(a) verbatim, or None (=⊥)
    /// Ok(spans) coverage-exact to slot `i`; Ok(SpanSet::empty()) = ⟨⟩ (valid-but-empty success);
    /// Err = ⊥ (link or slot absent). The Result/Ok-empty shape makes ⟨⟩ ≠ ⊥ unforgeable (F7).
    pub fn followlink(&self, a: &Address, i: usize) -> Result<SpanSet, Invalid>;
}
pub struct Invalid;
```

### F. Typed-relation reads & the PL surface for M9 (ASN-0086 / ASN-0128 / ASN-0125)

```rust
pub enum View { Audit, Active, Default }    // Default (active∖filtered) only on members/targets_of
pub struct Tuple { pub addr: Address, pub from: Endset, pub to: Endset }
pub enum Tip { Sink(Address), Indeterminate }   // ⊥ at branch or cycle

impl LinkState {
    // Observe + default predicates
    pub fn observe(&self, ty: &Endset, from_pat: &[Address], to_pat: &[Address], v: View) -> Vec<Tuple>;
    pub fn is_k(&self, ty: &Endset, a: &Address) -> bool;                 // D2 (coverage membership)
    pub fn members(&self, ty: &Endset, v: View) -> Vec<Address>;          // D1
    pub fn targets_of(&self, ty: &Endset, x: &Address, v: View) -> Vec<Address>;  // D3
    pub fn is_active(&self, a: &Address) -> bool;  pub fn is_nullified(&self, a: &Address) -> bool;
    // BH1 read-filter | BH2 walk | BH3 reverse | BH4 age — served entirely from M7's own indexes
    pub fn is_filtered(&self, a: &Address) -> bool;
    pub fn succs(&self, ty: &Endset, x: &Address) -> Vec<Address>;
    pub fn chain(&self, ty: &Endset, x: &Address) -> Vec<Address>;   pub fn tip(&self, ty: &Endset, x: &Address) -> Tip;
    pub fn sources_to(&self, ty: &Endset, target: &Address) -> Vec<Address>;
    pub fn target_of(&self, ty: &Endset, source: &Address) -> Option<Address>;
    pub fn age(&self, a: &Address) -> Option<u64>;   pub fn stale(&self, ty: &Endset, h: u64) -> Vec<Address>;
    // ASN-0125 currency (built on BH2 over the operative supersession graph)
    pub fn current(&self, y: &Address) -> Vec<CurrentMember>;        // set-valued; each member carries activity
}
```

### G. Discovery primitives for M8

```rust
impl LinkState {
    /// Spanfilade primitive: links whose slot-`i` coverage OVERLAPS `query`. The one shared index probe.
    pub fn stab(&self, i: usize, query: &SpanSet, v: View) -> im::OrdSet<Tumbler>;
    /// The AND-of-(per-slot overlap) combiner — findlinks' core, factored into M7 (Conflicts §6).
    pub fn match_links(&self, constraints: &[(usize, SpanSet)], v: View) -> im::OrdSet<Tumbler>;
    pub fn type_slice(&self, ty: &Endset, v: View) -> im::OrdSet<Tumbler>;    // L_K (Audit) / A_K (Active)
}
```

## Core data model

```rust
pub type Endset = SpanSet;                 // M1 SpanSet, stored VERBATIM — never normalized at rest
#[derive(Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Link { slots: im::Vector<Endset> }   // arity = slots.len() ≥ 3; positional accessors only

#[derive(Clone, Serialize, Deserialize)]
pub struct LinkState {
    links: im::OrdMap<Tumbler, Link>,           // ── AUTHORITATIVE ──
    registry: Arc<TypeRegistry>,                // immutable, genesis-fixed
    #[serde(skip)] hints: Hints,                // ── RECOMPUTABLE ── rebuilt by rebuild_derived
}
```

**The authoritative state is one map.** `links : Tumbler ⇀ Link` is append-only and immutable: a `LinkRec::Emit` only ever *inserts* at a fresh key, never mutates or removes. This single decision makes **Permanence (L12/R2), append-only audit (R3), retraction stability (R6a)**, and lock-free MVCC reads *free* — every `Snapshot` pins an immutable root, and a reader is untouched by concurrent appends. `im::OrdMap` keyed by `Tumbler` (the `Ord`-bearing type; callers pass `&Address`, M7 converts) gives O(log n) point lookup *and* the prefix-range scans that home-set enumeration and the frontier want — the one structure serving readlink, allocation-adjacent scans, and the indexes. **Identity is the key, never the value:** the store is *never* content-addressed on the endset (NonInjectivity L11b — two byte-identical links are distinct objects); hashing the payload would collapse them, so this is forbidden.

**`Link` is a positional sequence of endsets.** `im::Vector` because slot index is a primitive (L6) and arity is read off the value (FOLLOWLINK's post-lookup bound). Each `Endset` is M1's `SpanSet` held **verbatim** — the as-created span decomposition is observable through raw read-back (ML2/RL1), so we never canonicalize at rest; coverage is a *query-time projection*. `Link::new(slots)` enforces only the type floor (arity ≥ 3); the store invariant `e₃ ≠ ∅` (L3) is enforced at the *write boundary*, not the type (Conflicts §3).

**Everything else is a recomputable hint** — a pure function of `links` (+ `registry`), maintained incrementally in `apply_link` and re-seeded by `rebuild_derived` from the checkpointed `links`. This is the Lampson spine: the journal (via M2) is truth; lose any hint and replay rebuilds it, never wrong.

```rust
#[derive(Clone, Default)]
struct Hints {
    spanfilade: [SlotIndex; 3],                            // per standard slot: covered-extent → link addrs (overlap)
    type_class: im::HashMap<CoverageClass, im::OrdSet<Tumbler>>,  // typed slices L_K (Observe, type-match)
    nullified:  im::OrdSet<Tumbler>,                       // resident retraction roots — the tombstone set (active = audit ∖ this)
    dedup:      im::HashMap<DedupKey, im::OrdSet<Tumbler>>, // I0-class → addrs (audit; active-filtered at the check)
    sup_fwd:    im::HashMap<Tumbler, im::OrdSet<(Tumbler /*new*/, Tumbler /*claim*/)>>, // BH2 old→{(new,claim)}
    home_count: im::HashMap<Tumbler, u64>,                 // BH4: home document → # homed links (the frontier index)
}
```

| Hint | Makes free | Common-case cost |
|---|---|---|
| `spanfilade` | overlap/stabbing for Observe (BH3), `match_links`, M8 | O(log n) insert per slot-span on apply |
| `type_class` | `L_K` slices, same-type grouping (L8) | one `CoverageClass` of `e₃` + set-insert on apply |
| `nullified` | active view = `links ∖ nullified`; resurrection (I2) | one root-insert when applying an `[R]` tuple |
| `dedup` | O(1) idempotent dedup on the write path (I1) | one `DedupKey` + set-insert on apply |
| `sup_fwd` | BH2 walk / `current` | insert only when applying a `[K_sup]` tuple |
| `home_count` | BH4 `age` in O(1) | `+1` per apply, keyed by `origin(addr)` |

**`CoverageClass` and the level-mismatch hazard.** Two endsets are the same type / the same I0-class iff their *coverage* is equal — never their span decomposition. For **address-denoting endsets** (the managed surface: canonical encodings of address sets — every span unit-depth `(x,δ(1,#x))`), coverage equality reduces to the **≼-minimal antichain of denoted addresses** (I0a): drop any address that extends another, compare as a set. This is exact and never faults — it is the dedup hot-path key. For **general content endsets** (MAKELINK's resolved I-extents, multi-span, mixed-length), M1's `canonical_key`/`normalize` *fault* on mixed-length input (`LevelMismatch`), so the class is computed **per endpoint-length partition** — `canonical_key` each level-uniform partition, assemble the map.

```rust
#[derive(Clone, PartialEq, Eq, Hash)]
pub enum CoverageClass {
    Addrs(im::OrdSet<Tumbler>),               // ≼-minimal antichain — address-denoting (exact)
    Extents(im::OrdMap<usize, CanonicalForm>),// per-length canonical coverage — content extents (safe, see below)
}
pub struct DedupKey { ty: CoverageClass, from: CoverageClass, to: CoverageClass }  // I0 = (cov(F),cov(G)) within [K]
```

The per-length partition is **conservative**: it can *over*-discriminate two content endsets whose equal coverage straddles lengths, never *merge* distinct ones. Over-discrimination is the safe direction for both type-matching (you under-match, never false-match) and dedup (you deposit a second tuple, never wrongly suppress). The managed surface always lands in `Addrs` (exact); only MAKELINK content-type grouping touches `Extents`. The exact cross-length class is left open (M1 provides no cross-length normal form) — see Open build decisions.

## Internal design

### 1. The store, recovery, and the engine plug

`apply_link(LinkRec::Emit{addr, value})` inserts `addr↦value` into `links` and folds **every** hint incrementally — O(log n) `im` operations throughout: each slot's spans into `spanfilade`; `CoverageClass(value.e₃)` into `type_class`; if that class is `[R]`, the to-root into `nullified`; the `DedupKey` into `dedup`; if `[K_sup]`, the old→(new,addr) edge into `sup_fwd`; `home_count[origin(addr)] += 1`. `apply_link` reads only `LinkState` + M1 arithmetic + `registry`, is deterministic and total, and is applied exactly once per committed record (M2 guarantees this — do **not** code it idempotent).

`rebuild_derived` runs once at load, before replay, and recomputes `hints` entirely from the checkpointed `links` + `registry` (which it must, per M2's contract: it seeds exactly the `apply`-fold of the `Seq ≤ S_load` prefix). Because **all** hints are pure functions of `links`+`registry`, this is a single pass. The `registry` is genesis-fixed and not journaled; it rides the checkpoint (tiny) or is re-seeded from the engine's genesis — either is correct (Open decisions). Recovery is therefore *pure replay*: no undo log, no compaction for correctness; the only knob is M2's checkpoint cadence (it bounds the rebuild pass).

The engine assembles `World{ …, links: LinkState, … }`, implements `HasLinks`, `From<LinkRec> for Record`, and dispatches `Record::Links(x) => world.links().apply_link(x)`. M7 names neither `World` nor `Record`; its transact-ops are `impl<W: WorldState + HasLinks + HasM3 [+ HasM5]> LinkStore<W> where W::Record: From<LinkRec> + From<M3Rec> [+ From<M5Rec>]`.

### 2. Two write surfaces, one store (the central architecture)

The store holds links from **two disciplines that never unify** (Conflicts §1):

- **MAKELINK — the open content-link surface** (ASN-0043/0120). Resolves V-specs, admits multi-span endsets, admits ghost/unregistered types, applies **no shape gate** and **no idem dedup** (distinct links always — ML0). Seats the link in its home.
- **Emit_K — the managed typed-relation surface** (ASN-0086/0126/0128). Address-level, **shape-gated**, **idem-deduped per type**, `K ≁ R` rejected; **never seats**.

They share `links`, the spanfilade, every read path, and one internal `emit_core`. They differ only in admission and in the seat step. A MAKELINK content link's type resolves to `s_C` I-addresses, whose coverage class can never collide with a reserved managed class (different subspace), so MAKELINK links never pollute the managed slices; and the behaviors degrade gracefully (`target_of` returns ⊥ on a non-single-address endset, BH2 reads single-address claims) if an app ever registers a managed type coverage-equal to a MAKELINK type.

**`emit_core` (shared)** — the single choke point, run inside one `transact`:

```text
emit_core(stg, home, value, seat: bool, gate: Gate):
  Gate::Open (MAKELINK):  require value.arity()==3 ∧ value.e₃ ≠ ∅            // wf + type-nonempty
  Gate::Managed (Emit_K): let K = CoverageClass(value.type_slot());
                          require registry.registration(K).is_some()         // (i) registered
                          require K ≠ [R]                                     // K ≁ R
                          require Sh-conf(reg.shape, |F|, |G|)                // (ii) span-count gate
                          if reg.idem: DEDUP (below) — hit ⇒ return incumbent, stage nothing
  let (addr, m3rec) = stg.working().m3().mint_link(home)?                     // K.λ via M3
  stg.push(m3rec.into()); stg.push(LinkRec::Emit{addr, value}.into())
  if seat: stg.push(stage_seat_link(stg.working().m5(), home, addr)?.into()) // K.μ⁺_L via M5 (no R — J-LV)
  return addr
```

`Sh-conf` reads `shape(K)` from the registry and tests *span counts* (Unary `|G|=0`, Binary `|G|=1`, Multi `|G|<∞`; all require `|F|=1`) — never inferring shape from the tuple (a `(1,0)` tuple conforms under Unary *and* Multi). The gate adds preconditions only and never alters `value` (**effect-identity** — the ASN-0126 `π` bridge): do not "normalize on the way in."

**MAKELINK** wraps `emit_core` with the resolver:

```text
makelink(home, R₁, R₂, R₃):
  require is_registered_document(home)                                       // M3
  for each Rᵢ, each (d_j, σ_j): require is_registered_document(d_j)          // wf
                                ∧ subspace(u_j)=s_C ∧ #u_j≥2 ∧ ordinal-disp  // wf via M1
  eᵢ = ⋃_j resolve_coverage(d_j, span(σ_j))    [M5 — V→I, content I-extents]  // ρ as coverage
  require e₃ ≠ ⟨⟩                                                            // ML6 type precondition
  transact([content/home alloc key], |stg| emit_core(stg, home, Link[e₁,e₂,e₃], seat=true, Open))
```

Recording `resolve_coverage`'s output *as* the endset makes the **coverage-exactness recovery equation** (ML1: `coverage(eᵢ) ∩ dom(C) = ρ`) hold by construction — M5's runs trace exactly allocated content and never over-reach the frontier, and cross-origin runs arrive un-coalesced (M16). The wf checks reject malformed specs (a *rejection*, not the silent ⟨⟩ that `resolve_coverage` returns for non-content spans). MAKELINK touches **no R** (J-LV), allocates content nowhere (J0 vacuous), and seats exactly one link V-position.

**editlink** is one composite: deposit the successor (`emit_core(successor_value, seat=false, Open)` — born unseated, its content type idem⊥ so it never dedups), guarded by **DC** (reject a successor whose type class is `[R]` — else step 1 would silently nullify its to-set; schema-conform a `[K_sup]` successor), then `assert_sup(d_a, old=original, new=successor)`. The two writes commit atomically (EL7); the original is untouched (L12). The DC guard is what keeps editlink *discipline-preserving* and therefore chainable.

### 3. De-duplication and the M2 keyed critical section

Idempotence is a **computed equivalence at the surface, never stored identity** (I1) — the store stays pluralistic underneath; a hit returns the incumbent's address and *commits nothing*. For an idem type, `emit_core` computes the `DedupKey = (CoverageClass(ty), Addrs({from}), Addrs(to))` and:

1. **Acquires the dedup lock.** M7 serializes `DedupKey` bytes into a `LockKey` (M7's space tag + the minimal antichains) and passes it to `transact` *alongside* the home alloc key: `transact(&[dedup_key, M3::link_lock_key(home)], …)`. Same I0-class ⇒ same `LockKey` ⇒ M2 serializes the check-and-deposit (I1a/I4); different I0-class ⇒ no contention. This is the only cross-home synchronization point, partitioned **by I0-class, never by home** — sharding dedup by home would let two same-class different-home emits both miss.
2. **Checks the ACTIVE view inside the txn:** `dedup[key]` filtered by `∉ nullified` (reads `stg.working().links()`). Several active matches (only off a raw path) → return the T1-least (deterministic). One → return it, stage nothing (zero-step; M2 returns the base `Seq`). None → fall through and deposit.

Reading the *active* view (I2) is what gives **resurrection**: a nullified tuple is invisible to dedup, so re-emitting lands at a fresh address — the audit trail keeps both. MAKELINK and idem⊥ app types skip steps 1–2 entirely (only the home key).

### 4. Retraction, the nullified set, and the active view

`nullify(d_retr, target)` is `emit_core` of an `[R]` tuple with canonical from-fill `(d_retr,δ(1,#d_retr))` and unit-depth to-span `(target,δ(1,#target))`, idem⊤ (so re-retracting the same target from the same document dedups). **P-tgt is a rejecting precondition** (ASN-0128's promotion): `target ∈ links ∨ target == <the fresh emitter addr>`. Public `emit` rejects `K ~ R`, so `nullify` is the *sole* `[R]`-writer.

`nullified` is a monotone tombstone set of **resident retraction roots**. Under the unit-depth + antichain discipline, R-Scope makes each retraction nullify exactly one resident link, so "is `a` nullified?" is a plain `nullified.contains(a)` (a prefix-trie variant covers the off-surface range case — Open decisions). The **active view of any slice is `audit ∖ nullified`**, derived at query time; the spanfilade and `type_class` index the *audit* slice (append-only, never delete on nullification), and `View::Active`/`Default` filters results by `nullified`. Only `dedup` consults active (above). This keeps every index a pure append-only hint.

**Sterilization is unreachable through M7's surface** (DR theorem): `nullify`-only-via-the-wrapper + unit-depth to-span + P-tgt-rejecting makes the wp's C3 conjunct vacuous — no pre-existing retraction can ever cover a later fresh emitter address (antichain + freshness). Born-nullified tuples arise only from a deliberate self-emit retraction, and that falls out of the ordinary `audit ∖ nullified` derivation with no special gate.

### 5. Supersession and the BH2 walk

`assert_sup(home, old, new)` emits a `[K_sup]` claim with **F = enc({old}), G = enc({new})** (slot convention resolved in Conflicts §2 — F holds the *old/superseded* link, edges run old→new), both endpoints required resident. `sup_fwd` maps `old → {(new, claim_addr)}` over the audit `[K_sup]` slice. `succs(old)` returns the `new`s whose `claim_addr ∉ nullified` (operative `succ_o`). `chain` is a bounded iterative walk over `succs` with a visited-set, halting at **sink** (no succ), **branch** (≥2 succs), or **cycle** (repeat) — the finite link set is the termination bound; `tip` returns `Sink(head)` or `Indeterminate` at branch/cycle. `current(y)` is BH2 generalized to sets: the operative sinks reachable from `y` via `succ_o`, returned **entire** (linear→1, forked→≥2, mutual-supersession standoff→0, all legitimate), each member tagged with its own activity (a member can be a current sink yet itself nullified — EL14e). M7 owns **disclosure, not decision**: never fabricate a single "latest." A *per-home* latest is recoverable (claims homed on one chain are T1-ordered, EL13); a cross-home latest is not a state function and M7 does not invent one.

### 6. The spanfilade and the matcher (the M7↔M8 seam)

The spanfilade answers the one primitive both Observe and M8 stand on: **`stab(i, Q)` = link addresses whose slot-`i` endset coverage overlaps `Q`** (interval-overlap / stabbing). Per slot (the three standard slots only — higher-slot search is deferred), it maps covered I-extents to the link addresses covering them; M1's `classify_spans`/`intersect` decide overlap. The baseline is a **brute-force scan** of `links` (trivially correct, O(n)); the scale structure is an interval/segment index keyed in tumbler order (concrete shape = Open decisions). It is rebuilt by replay — never persisted transactionally — so durability (the journal) is decoupled from query performance.

Two combiners sit on `stab`, and to remove the double-implementation noted as the design's softest seam, **both live in M7** (M8 becomes pure presentation):

- **`match_links(constraints, view)`** — findlinks' core: per constrained slot, OR (`stab`-union) over the slot's query spans (overlap), then AND (intersect by link identity) across slots. M8's findlinks = this + cursor/count/window.
- **`observe(K, F̂, Ĝ, view)`** — Observe's *subset* match (`F̂ ⊆ coverage(F)`, distinct from findlinks' overlap): start from `type_slice(K, view)`; for each query address `a ∈ F̂`, intersect with `stab(1,{a})`; same for Ĝ on slot 2; assemble `Tuple`s. Patterns range over all of `T` (ghost addresses welcome — `is_k`/`stab` test coverage-membership, total).

M8 reads `stab`/`match_links`/`type_slice`/`is_active`/the BH3 family across the existing `M8→M7` edge; M9 reads `observe` + BH1–BH4 — both served entirely from M7's own indexes, so **no `M7→M8` edge** and **no `M9→M8` edge** arise.

### 7. Behavior atoms BH1, BH3, BH4; default predicates; raw reads

- **BH1 read-filter** (Unary types): `is_filtered(a)` = `is_k` over the *filter* type's active slice (a prefix-containment test on its roots); rewrites *only* `members`/`targets_of` at assembly (result-side subtraction, computed lazily against the filter roots — never materialize the filtered subtree). Filter-vs-walk/reverse interaction (OQ1) is left at the active reading.
- **BH3 typed-reverse-lookup** (Binary): `sources_to(target)` = `stab` on the target slot matched by target-coverage (the spanfilade *is* the reverse index — no separate structure); `target_of(source, K)` returns the unique single-address denoted target or ⊥. ASN-0125's archival `in(y)/out(x)` (M8) compose these.
- **BH4 age-staleness** (idem⊥ types): `age(a) = home_count[origin(a)] − ordinal(a)` — the chain index off the address (`ordinal`), the frontier off M7's own homed count (equivalent to M3's frontier by construction, so no upward read — Conflicts §7). `stale(h)` scans the active slice; `retract_stale` is a *sequence* of `nullify` transacts over the entry-time stale set (idempotent on already-nullified targets). No global counter, no clock (ordinal time only).
- **Default predicates** `is_k`/`members`/`targets_of` read coverage-membership and denoted addresses, `members`/`targets_of` alone honoring `Default` (active∖filtered).
- **READLINK** = `links.get(a)` copied out, total, returns `None`(=⊥) on absence — *recorded, never resolved*, never dereferencing covered links (RL4/RL6). The structural screen and ⊥-permanence caching of ASN-0111 are optional pre-probe fast paths; the persistent map is already the positive cache (immutability ⇒ never stale). **FOLLOWLINK** = slot lookup with the post-lookup arity bound, emitting the recorded spans verbatim (F1 by construction), `Ok(empty)` vs `Err` keeping ⟨⟩≠⊥.

## Invariants & contracts

**By construction** (fall out of the append-only `links` map + M3's minting + M1's algebra):

- **Permanence / immutability** of every link value and address — L12 (ASN-0043), R2 (ASN-0086), C0/L12 (ASN-0093), ML7 (ASN-0120), RL5/RL6 (ASN-0111), F5 (ASN-0114), EL0 (ASN-0125). *Where:* no update/delete record exists; `apply_link` only inserts.
- **Uniqueness / freshness / flat prefix-antichain** — L11a (0043), R0/R0a/R1 (0086). *Where:* M3 mints monotone home-scoped siblings; M7 never chooses an address.
- **Ownership derivability** (home = address projection) — L2 (0043). *Where:* M1's `document_of`/`origin`.
- **Subspace disjointness** (links in `s_L`, never colliding with `s_C` content) — L1d/L14 (0043), SD/R4 (0093/0086). *Where:* M3 keeps links in `s_L`; M7 stores only what M3 mints there.
- **Type-by-coverage / ghost permission** — L8/L9 (0043), RL3 (0111). *Where:* matching computes `CoverageClass`, never dereferences a type address.
- **Endset order-independence & slot distinction** — L5/L6 (0043). *Where:* `Endset = SpanSet` (membership), `Link = im::Vector` (positional).
- **Audit monotonicity, retraction stability, resurrection** — R3/R6a (0086), I2 (0128). *Where:* `nullified` only grows; dedup reads active.
- **Registry & idem stability** — P1/P2 (0126), R1/R2 (0128). *Where:* registry sealed at genesis; no mutator exists.
- **No sterilization through the surface** (DR) — ASN-0128. *Where:* `nullify`-only wrapper + unit-depth + P-tgt-rejecting.
- **Effect-identity** (the gate deposits exactly what an ungated emit would) — ASN-0126 `π`. *Where:* `emit_core` never mutates `value`.
- **Coverage-exactness of MAKELINK endsets** (ML1) — *Where:* recording `resolve_coverage` verbatim.

**By active enforcement** (M7 must guard):

- **Home existence** (L1a/0043, ML0/0120, P0): `is_registered_document(home)` (and each `d_j`) before any emit — at `makelink`/`emit`/`nullify` entry.
- **Type-endset non-empty** (L3/0043, ML6/0120): `e₃ ≠ ∅` — MAKELINK rejects empty type resolution; managed `e₃ = K` is non-empty by `T_admissible`.
- **Shape conformance** (P3/0126, |F|=1, arity 3): `Sh-conf` in the Managed gate (Emit_K only — *not* MAKELINK).
- **Dedup identity = coverage** (I0/I1, 0128): the dedup key/index compare `CoverageClass`, never value; idem-uniqueness (I1a) needs surface-routing + the M2 dedup `LockKey`.
- **`[R]` / reserved-class reservation** (R-C1, registry): `TypeRegistry::build` rejects any app key coverage-equal to a shipped class or another app key.
- **Unit-depth retraction + P-tgt** (R-Scope/DR, 0128): `nullify` writes only `{(target,δ(1,#target))}` and rejects a non-resident/non-self target.
- **DC guard on editlink** (Df-DISC, 0125): reject `[R]`-typed successor; schema-conform `[K_sup]` successor.
- **Recovery** of all indexes: `rebuild_derived` from `links`+`registry`.

**Discharged elsewhere (flag at the seam):** **Non-transcludability** (L14a, ASN-0043) — M7's *only* duty is keeping links in `s_L`; the exclusion of link addresses from V-position images lives in **M5**'s content-side referential-integrity check. Provenance R is M5's; M7 appends none.

## Dependencies & seams

**Upstream calls:**

- **M1** — pervasive: `Tumbler/Address/Span/SpanSet`; `coverage`/`subtree_of` for endset denotation; `canonical_key`/`CanonicalForm` for the `Extents` coverage-class partition; `classify`/`subspace`/`#u`/`document_of` for wf checks and `origin`/home; `classify_spans`/`intersect` for the spanfilade overlap; `is_prefix` for antichain minimization and nullified-root tests.
- **M2** — `transact(keys, f)` for every write (one `transact` per op, composites staging M3+M7+M5 records); `snapshot` for every read; the dedup `LockKey` supplied to the keyed critical section; `apply_link` plugged via `WorldState`; index rebuild via `rebuild_derived`. M7 contributes its own `Space` tag for the dedup `LockKey`; namespace alloc keys come from M3's `link_lock_key`.
- **M3** — `mint_link(home) → (Address, M3Rec)` and `link_lock_key(home)` inside every emit composite (stage the `M3Rec`); `is_registered_document` (home/spec preconditions); `effective_owner` only if M7 ever needs to attribute a claim's home to a principal (it does not — attribution is the address projection). The frontier is M3's; M7 reads no M3 state for BH4.
- **M5** — `resolve_coverage(d_j, span) → SpanSet` (MAKELINK V→I endset construction, the centralized `iextent` lift — consume per level-class); `stage_seat_link(&M5State, doc, link) → M5Rec` (the semantics-blind home seating, folded into MAKELINK's composite — the `M7→M5` edge with no return). M7 never reads link semantics back from M5 and never resolves anything itself.

**Downstream seams (make these explicit so M8/M9 build against them):**

- **→ M8** (`M8→M7` edge): `stab(i, Q, view)`, `match_links(constraints, view)`, `type_slice(K, view)`, `is_active`/`is_nullified`, the BH3 reverse family, and `readlink` — M8 layers cursors, counting, windowed pagination, projection (via M5's `project`), RETRIEVEENDSETS, and archival `in/out` (composing BH3) on top. M8 owns no index and writes nothing.
- **→ M9** (`M9→M7` edge, including writes): the full PL read surface — `observe` + BH1–BH4 + `is_k`/`members`/`targets_of` — all from M7's own indexes (so M9 needs no M8 dependency); and the gated write path — `emit(home, reserved(PredDef|PredStable), …)` for `register_pred`/`certify_pd_stable`, and `emit`/`nullify` for reactive rule fires. The `pdef`/`pd_stable` reserved classes must already sit in the genesis registry (M9 coordinates their addresses via `ReservedAddrs`).
- **→ M10**: the transact-driving ops in §C/§D, each returning `(…, Seq)` post-commit; M10 surfaces `TxnError::Rejected(E)` as typed rejections.
- **→ engine**: `LinkState` slice, `LinkRec` record, `HasLinks` accessor, `apply_link` fold, `genesis(registry)`, `rebuild_derived`.

## Conflicts resolved

1. **MAKELINK's multi-span endsets vs the shape gate's `|F|=1` (ASN-0120 vs 0126/0128).** ASN-0126 OQ6 itself defers multi-span sources, and ASN-0120 admits them. **Resolution: two write surfaces, one store.** MAKELINK is the *open* content-link surface (wf + type-nonempty, multi-span, ghost types, no dedup, seats); Emit_K is the *managed* typed-relation surface (shape-gated, idem, `K≁R`, no seat). They share `links`, the indexes, and `emit_core`; only admission and the seat differ. Managed types reserve `s_L`/coordinated classes; MAKELINK types resolve into `s_C`, so the populations never collide, and behaviors degrade gracefully (`target_of`→⊥) if they ever did.

2. **Supersedes slot direction (ASN-0125 Df-DIR vs ASN-0128 S2).** ASN-0125 puts the *new* link in F ("F replaces G"); ASN-0128 puts the *old* in F ("F is superseded by G; edges old→new"). Both agree the *edge* runs old→new and the walk goes version→head; they disagree only on which slot holds old. **Resolution: adopt ASN-0128 (F = old/superseded, G = new/superseding)** — it is the note where BH2/the walk is defined, and the decomposition endorses old→new so that `succs(old)=new` is the natural forward step and `tip` is the head. `assert_sup(home, old, new)` keeps its caller-facing meaning ("old is superseded by new") and maps `old→F, new→G` internally. This overrides ASN-0125 Df-DIR's labels.

3. **`e₃ ≠ ∅`: store invariant vs link type (ASN-0043 L3 vs ASN-0111).** ASN-0111 notes the `Link` *type* admits `e₃=∅` (∅ is a valid endset); L3 is a *store* invariant. **Resolution:** `Link::new` enforces only arity ≥ 3 (the type floor); `e₃ ≠ ∅` is enforced at the *write boundary* (`emit_core`/MAKELINK's `ML6`), so READLINK's verbatim disclosure inherits a non-empty type for free without the type over-constraining.

4. **MAKELINK "distinct links always" (ML0) vs idempotent dedup (ASN-0128).** **Resolution:** dedup is *per type's idem flag*. The store never merges (NonInjectivity L11b — distinct addresses always); the idem *surface* returns an incumbent *without depositing*. Content-link types are idem⊥ (every MAKELINK deposits fresh — ML0 honored); only the shipped/registered idem⊤ types dedup. The two compose without contradiction.

5. **Raw read vs bundled resolution (ASN-0111/0114).** Green bundled V-resolution into its link reads; the spec de-bundles. **Resolution:** READLINK/FOLLOWLINK are *raw* reads off `links`, taking no document handle and consulting no arrangement; V-projection (and the silent-drop it entails) lives in M8/M5. This is the boundary that makes orphaned/ghost links readable.

6. **Spanfilade placement and the double-implemented combiner (the decomposition's softest seam).** **Resolution: the spanfilade *and* the matchers (`stab`, `match_links`, `observe`) live in M7**, co-located with the link writer; M8 is pure discovery presentation over them. This restores ASN-0086's indexed Observe on M9's hot polling path and removes the duplicated per-slot-match + combiner.

7. **Frontier ownership for BH4 (M3 mints, M7 needs the frontier).** **Resolution:** M7 computes the frontier from its *own* homed-link count (`home_count`), equal to M3's frontier index by construction (every minted link is stored). No `M7→M3` read on the BH4 path; M3 stays the authoritative minter.

8. **Dedup's state-dependent home validation (ASN-0128 I1: `home` read only on the miss branch).** **Resolution:** the *internal* check stays branch-local (a hit answers whatever `home` holds), but M7's *caller-facing contract* requires a registered `home` unconditionally — callers cannot evaluate the hit/miss branch, so portability demands it.

## Open build decisions

- **Spanfilade structure.** Brute-force scan of `links` (correct, O(n), the bootstrap default) vs an interval/segment index in tumbler order. Pick the index when stabbing latency under measured corpus size and query rate demands it; keep `stab`'s signature stable across the swap.
- **Hint persistence.** `#[serde(skip)] hints` + `rebuild_derived` (recommended — one authoritative map, cheap checkpoints) vs serializing the indexes (faster load, larger checkpoints, a second consistency surface). Default skip+rebuild; tune M2's checkpoint cadence to bound the rebuild pass.
- **Active vs audit indexing.** Index the audit slice and filter active at query (recommended — append-only hints) vs maintain active-only indexes (removal on nullification). Dedup is the exception (active-keyed); choose whether dedup stores all-matches-filter-active (simpler) or an active incumbent (one less filter).
- **Cross-length coverage-class exactness.** The conservative per-length `Extents` partition (buildable today, over-discriminates across lengths, safe) vs a future exact cross-length coverage normal form (M1 provides none). Ship the conservative form; revisit if content-type matching shows the imprecision biting.
- **Nullified representation.** A plain `OrdSet` of roots (sufficient under the unit-depth surface discipline) vs a prefix-trie over roots (needed only if a raw/off-surface range retraction is ever admitted). Default the set; gate any raw `[R]` path behind the trie.
- **Raw-deposit / import path.** Surface-only (recommended — gives idem-uniqueness, no sterilization, no born-nullified non-R tuples, full attribution, all by construction) vs an explicit import mode tolerating multiple dedup matches, non-denoting spans, and audit/active divergence (AD: non-unit spans omitted from address enumerations, visible to membership/`observe`).
- **READLINK fast paths.** Whether to run the structural screen as a pre-probe and whether to keep a ⊥-permanence negative cache (permitted only for provably-permanent absence; usually redundant against the in-memory map). Default: rely on the map, screen only untrusted boundary addresses.
- **Endset backing.** Store verbatim `SpanSet` (decided — decomposition is observable, ML2/RL1) but optionally back each by a canonical span order for cheap structural equality and deterministic serialization — a representation nicety that must never become a *contract* (order is not promised).
- **BH2 audit-view recovery (OQ6) and `current` reader policy.** Whether to offer an audit-view `chain`/`tip` reconstructing nullified-mid-chain history; and the default the client applies to set-valued `current` (per-home-latest, curator-trust, drop-retracted) — M7 discloses, the consumer decides.
