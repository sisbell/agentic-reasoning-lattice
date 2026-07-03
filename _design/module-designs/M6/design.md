# M6 — Content Retrieval & Query — Detailed Design

## Purpose & boundary

M6 is the system's **read-only observer surface over documents**. It owns the seven content/provenance queries — RETRIEVEV, RETRIEVEDOCVSPAN, RETRIEVEDOCVSPANSET, SHOWORIGIN (V-arity), SHOWDELETIONS, COMPARE, FINDDOCSCONTAINING — and turns the authoritative state held below it (M3's registry, M4's content, M5's arrangements and provenance relation R) into delivered values, extents, origins, deletion sets, correspondence reports, and containment answers. Every operation is a **pure function of one consistent M2 snapshot**: it resolves through M5's arrangements, fetches bytes from M4, projects origin via M1, reads R through M5, and gates on M3's registry — and writes nothing, ever.

**One thing well:** *observe documents over a single pinned snapshot — resolve, fetch, project, classify, compose — never mutate.*

It does **not** own: any authoritative or derived-authoritative state (none — it has no `WorldState` slice, no journal record, no fold); the R relation or its reverse index (these belong in M5, co-located with R's authoritative state — `docs_containing` is M5's); content bytes (M4); arrangements (M5); link-side discovery (M8); the request lifecycle, dispatch, and marshaling (M10). It also does **not** deliver SHOWORIGIN's *I-span* arity: that arity needs an I-ordered enumeration of `dom(C)` over an interval, which M4's point-only interface (with `Ord` deliberately unused, range/prefix scans forbidden) and M3's point-only registry deliberately exclude; the I-arity is therefore **de-scoped from M6 and recorded as a decomposition amendment** (a new I-ordered content index over M4's append-only writes — see *Conflicts resolved* 2), and since M6 exposes only the V-arity, M10 has no I-arity surface to promise clients — the amendment is **settled, not conditional**. M6 delivers SHOWORIGIN's V-arity (preferring it is **M6's ruling** — ASN-0077 designates neither arity reader-facing).

**Build status:** all seven operations compile against M1–M5 *as given*. SHOWDELETIONS composes its cross-document combine **in M6** from M5's per-document `deletions`/`content_runs` and M1's `denotes` — membership-testing, not faulting set-algebra (see its section); no upstream amendment is needed. M6 owns no `WorldState` slice, journal record, or fold, so it trivially satisfies the engine composition contract.

## Public interface

All operations are methods on a stateless `Query` handle that binds one pinned snapshot; the caller (M10) takes the snapshot and constructs the handle, so every read in one logical query observes one consistent root. Reads never commit and have no commit-before-acknowledge obligation.

```rust
// M6 reads three upstream slices; it contributes none of its own.
pub trait M6World: WorldState + HasM3 + HasContent + HasM5 {}
impl<W: WorldState + HasM3 + HasContent + HasM5> M6World for W {}

/// Stateless reader over ONE pinned snapshot. Owns nothing; holds a borrow.
pub struct Query<'s, W: M6World>(&'s Snapshot<W>);

impl<'s, W: M6World> Query<'s, W> {
    pub fn new(snap: &'s Snapshot<W>) -> Self { Query(snap) }
    pub fn as_of(&self) -> Seq { self.0.seq() }   // the committed index this query reads (V1 retrospective)
}
```

**Derive policy (the marshaling seam M10 codes against — stated, not guessed).** Every M6-owned public request/result/error type is a plain all-`pub`-field value. The declared set: `Spec`, `Region`, `Delivery`, `DeliveryItem`, `Deletions`, and the six error enums derive **`Clone + PartialEq + Eq + Serialize`**; the payload-free `SpecFault`/`Operand` additionally derive **`Copy + Debug`**. Every leaf these carry (`Address`, `Span`, `Val`, `Nat`, `usize`) is itself `Serialize` per M1/M4, so the derives compile as stated. **No `Debug`** on any type carrying `Address`/`Span` — M1's `Tumbler`/`Address`/`Span` are not `Debug` (the same fact that forces `debug_assert!` over `debug_assert_eq!` in COMPARE). **No `Deserialize` anywhere** — M10 constructs requests through M1's validating front doors (`validate`, `Span::new`/`from_endpoints`), never by deserializing untrusted addresses. The two exceptions are **`CorrPair`/`CompareReport`**: they carry M5's `VPos`, whose as-given declaration names no derives, so M6 declares none on them — they are **move-only, destructure-only** values that M10 marshals **field-by-field** (every leaf still serializes individually, including `VPos`'s `pub Nat` fields).

### Shared request types

```rust
/// One document + one ordinal-level depth-2 V-span. RETRIEVEV's spec-set is the ORDERED `&[Spec]` —
/// per-spec order is denotational (R5) and each spec carries a single span. This is the single-span,
/// order-bearing idiom; the SET-shaped operations (COMPARE, FINDDOCSCONTAINING) use `Region` instead.
#[derive(Clone, PartialEq, Eq, Serialize)]
pub struct Spec  { pub doc: Address, pub span: Span }
/// One document + a finite V-region (set of spans) — the shared "(document, span-set)" idiom for the
/// two SET-shaped operations: COMPARE (content only; the unordered set ASN-0122's `ρ` is) and
/// FINDDOCSCONTAINING (FD-CONVEX wants multi-span). Both take `&[Region]`.
#[derive(Clone, PartialEq, Eq, Serialize)]
pub struct Region { pub doc: Address, pub spans: Vec<Span> }
```

### A. Content delivery

```rust
#[derive(Clone, PartialEq, Eq, Serialize)]
pub enum DeliveryItem { Content(Val), Ref(Address) }   // content position ⇒ value; link position ⇒ address-as-reference
#[derive(Clone, PartialEq, Eq, Serialize)]
pub struct Delivery(pub Vec<DeliveryItem>);            // per-spec concatenation, ascending-V within, no merge, no global sort

impl<'s, W: M6World> Query<'s, W> {
    /// RETRIEVEV (ASN-0115). Rejects the WHOLE request on any malformed spec (well-formedness
    /// precondition); gaps / depth-incompat / empty subspaces degrade to silent empty contributions,
    /// never an error (R6). Empty spec-set ⇒ Ok(empty).
    pub fn retrieve_v(&self, specs: &[Spec]) -> Result<Delivery, RetrieveError>;
}
```

### B. Document-extent queries

```rust
impl<'s, W: M6World> Query<'s, W> {
    /// RETRIEVEDOCVSPAN (ASN-0112). Whole-document bounding span: singleton `⟨σ_d⟩`, or `⟨⟩` for an
    /// allocated-empty document. Unallocated ⇒ Err. Degrades to a bounding box across subspaces.
    pub fn doc_vspan(&self, doc: &Address) -> Result<SpanSet, ExtentError>;

    /// RETRIEVEDOCVSPANSET (ASN-0113). Per-subspace exact extents: ≤2 members (content, link),
    /// already normalized; `⟨⟩` for allocated-empty. Unallocated ⇒ Err.
    pub fn doc_vspanset(&self, doc: &Address) -> Result<SpanSet, ExtentError>;
}
```

### C. Origin attribution

```rust
impl<'s, W: M6World> Query<'s, W> {
    /// SHOWORIGIN over a V-span (ASN-0077, V-arity). The I-arity is de-scoped to a decomposition
    /// amendment (M6's ruling — 0077 designates neither arity reader-facing); see *Conflicts resolved* 2.
    /// Deduplicated origin documents, in tumbler order. Inadmissible (Err) on an unallocated document,
    /// a foreign subspace (`NoSuchSubspace`) or empty real subspace (`EmptySubspace`), a depth-incompatible
    /// `#start ≥ 3` span (`DepthIncompatible`, WF_V(v)), or a depth-2 span whose positions are not all
    /// currently bound (`RangeNotPresent`, WF_V(vi); O13) — reject, never silently clamp.
    pub fn show_origin_v(&self, doc: &Address, span: &Span) -> Result<Vec<Address>, OriginError>;
}
```

### D. Provenance comparison

```rust
#[derive(Clone, PartialEq, Eq, Serialize)]
pub struct Deletions { pub a_with_b: Vec<Address>, pub b_with_a: Vec<Address> }  // deleted-from-one ∧ current-in-other; the existing I-addresses (D-IDENT), deduped + Tumbler-ordered (D-ORD)

pub use m5::VPos;   // CorrPair/CompareReport carry M5's VPos; re-export so M10's marshaler names it through M6, not by reaching into M5's crate

// NO DERIVES (deliberate): these two carry M5's VPos, whose as-given declaration names no derives —
// so they are move-only, destructure-only values; M10 marshals field-by-field (derive policy above).
pub struct CorrPair { pub d1: Address, pub u1: VPos, pub d2: Address, pub u2: VPos, pub width: Nat }
pub struct CompareReport(pub Vec<CorrPair>);   // canonical order; slot i drawn from operand i

impl<'s, W: M6World> Query<'s, W> {
    /// SHOWDELETIONS (ASN-0075). Both documents must be registered (Err otherwise; allocated-empty is
    /// fine and yields empty halves). Each half is the deduped, Tumbler-ordered set of I-addresses
    /// deleted-from-one yet current-in-the-other — the existing I-addresses themselves (D-IDENT),
    /// never copies. Composed in M6 from M5's per-document `deletions`/`content_runs`; opens M4 for
    /// nothing. See the SHOWDELETIONS section.
    pub fn show_deletions(&self, d_a: &Address, d_b: &Address) -> Result<Deletions, DeletionsError>;

    /// COMPARE / SHOWRELATIONOF2VERSIONS (ASN-0122). Two content-subspace spec-sets, each a set of
    /// `Region`s (the shared (document, span-set) idiom — ASN-0122's `ρ`); reports address-equal
    /// correspondences (NEVER opens M4). Complete under fan-out, deterministic canonical order.
    pub fn compare(&self, rho1: &[Region], rho2: &[Region]) -> Result<CompareReport, CompareError>;
}
```

### E. Document containment

```rust
impl<'s, W: M6World> Query<'s, W> {
    /// FINDDOCSCONTAINING (ASN-0124). Every named document must be registered and every region span
    /// well-formed (Err otherwise; allocated-empty contributes nothing). Returns the PRESENT-TENSE
    /// containers (filtered), tumbler-ordered, deduplicated — bare identities, no positions, no counts.
    pub fn find_docs_containing(&self, regions: &[Region]) -> Result<Vec<Address>, FindError>;
}
```

### Errors (all typed; M10 surfaces verbatim — never a silent skip)

```rust
#[derive(Clone, Copy, PartialEq, Eq, Debug, Serialize)]
pub enum SpecFault { NotOrdinalLevel, NotLevelUniform, StartNotZeroFree, StartTooShallow }  // StartTooShallow: #start < 2
#[derive(Clone, Copy, PartialEq, Eq, Debug, Serialize)]
pub enum Operand   { First, Second }   // which COMPARE spec-set (ρ₁/ρ₂) a fault came from — Copy, captured into the gate closure
// Every `DocNotRegistered` uniformly carries the offending document — one marshaling shape for M10
// (recoverable from the request for the single-document ops; carried anyway for uniformity).
// All six derive Clone + PartialEq + Eq + Serialize; NONE derives Debug (they carry Address — derive policy above).
#[derive(Clone, PartialEq, Eq, Serialize)]
pub enum RetrieveError  { DocNotRegistered(Address), MalformedSpec { index: usize, fault: SpecFault } }
#[derive(Clone, PartialEq, Eq, Serialize)]
pub enum ExtentError    { DocNotRegistered(Address) }
#[derive(Clone, PartialEq, Eq, Serialize)]
pub enum OriginError    { DocNotRegistered(Address), NoSuchSubspace, EmptySubspace, DepthIncompatible, RangeNotPresent, MalformedSpan(SpecFault) }
#[derive(Clone, PartialEq, Eq, Serialize)]
pub enum DeletionsError { DocNotRegistered(Address) }
#[derive(Clone, PartialEq, Eq, Serialize)]
pub enum CompareError   { DocNotRegistered(Address), NotContentSubspace { operand: Operand, region: usize, index: usize }, MalformedSpan { operand: Operand, region: usize, index: usize, fault: SpecFault } }
#[derive(Clone, PartialEq, Eq, Serialize)]
pub enum FindError      { DocNotRegistered(Address), MalformedSpan { region: usize, index: usize, fault: SpecFault } }
```

## Core data model

M6 owns **no persistent and no derived-authoritative state**. It declares no `WorldState` slice, no journal `Record` variant, no `apply`/`rebuild_derived` fold — it is not a store, and it does not appear in the engine's `World`/`Record`. Its "data model" is three things:

1. **The borrowed snapshot.** A `Query` holds one `&Snapshot<W>` and reads `s.world().m3()`, `s.world().content()`, `s.world().m5()` off it. M5/M4/M3's slices are `im`-backed (structurally shared, persistent), so the snapshot is an O(1), lock-free, immutable value; reading every constituent of one query off the *same* `&Snapshot` is what makes its `(M, R)` view consistent by construction (it is the discharge of M2's clause-6, ASN-0075/0122/0124 single-Σ requirement). M6 holds the borrow only for the query's duration.

2. **Result value types** (above) — `Delivery`, `SpanSet`, `Vec<Address>`, `Deletions`, `CompareReport`. All in-memory, returned by value. `DeliveryItem::Content(Val)` carries an `Arc<[u8]>` clone (an Arc bump, not a byte copy), so delivery is cheap even for large content.

3. **Transient per-query working structures**, all dropped at return:
   - COMPARE's `Block` lists for P and Q (the `Block` row type is fenced with the COMPARE helpers below), plus the intermediate `Vec<CorrPair>` before canonicalization; SHOWDELETIONS's enumerated `arranged_content(d)` address lists.
   - Dedup sets for origins, containers, and the two SHOWDELETIONS halves (`HashSet<Tumbler>` → sorted `Vec<Address>`, since `Address` is `Eq+Hash` but not `Ord`; `Tumbler` carries the `Ord`).

**Authoritative vs. recomputable, resolved explicitly for M6:** there is nothing to distinguish, because M6 holds neither. Three would-be hints all resolve away from M6:
- the **R reverse index** (`docs_containing`, FINDDOCSCONTAINING) belongs in M5, co-located with R's authoritative state (recomputable by replay only where R is folded), and is in M5's interface today; SHOWDELETIONS's **cross-document deletion comparison** stores nothing at all — it is a pure per-query read M6 composes from M5's *per-document* `deletions`/`content_runs` (membership-tested, no index, no fold);
- the **per-subspace common depth `m_S(d)`** that the source notes fret over (cache vs. recompute) is the **constant 2** — M5 fixes V-positions at depth 2, so `m_S(d) ≡ 2` and the depth-compatibility test is the static `#start == 2`;
- the **I-ordered content index** that SHOWORIGIN's de-scoped I-arity would need is **not placed here** at all (it would belong to M4 or a dedicated index; the I-arity is de-scoped — *Conflicts resolved* 2).

**Dense occupancy (D-CTG★) — a *theorem of ASN-0113 W4*, the one upstream structural fact M6 leans on.** Two M6 paths read M5's O(1) `content_count`/`link_count` *instead of* scanning positions, and one accumulates a V-cursor by run width rather than re-resolving each position: `doc_vspan`/`doc_vspanset` treat the counts *as* the extents (`n_S` ⇒ the span `([S,1],[0,n_S])`), and COMPARE's `resolve_blocks` starts its V-cursor at `span.start()` and advances by each run's width with no V-gap to skip. Both are correct because each subspace's occupied V-positions form a dense, origin-anchored, gap-free run — content at `[s_C, 1..n_C]`, links at `[s_L, 1..n_L]`, ordinals `1..n` with no hole — and that density is **proven, not merely promised**: **ASN-0113 W4 (ExactCoverage)** states `⟦ext(d,S)⟧ ∩ VSlice(S,m_S) = V_S(d)` with `ext(d,S) = ([S,1],[0,n_S])`, which *forces* the occupied set `V_S(d)` to be exactly the contiguous depth-`m_S` slice `[S, 1..n_S]` — no hole-admitting occupancy satisfies W4. So D-CTG★ is a **corollary of a note M6 already cites** for its extent synthesis, not an extra assumption: (a) **ASN-0113 W2/W4** supplies the slice equality just quoted (the formula `ext_span` literally builds, and the reason a count fixes an extent); (b) **ASN-0112 V8** (origin permanence) pins the content anchor at `[s_C,1]` while content is present, so the run always starts at ordinal 1; (c) **M5's contiguity/reseat maintenance** keeps live ordinals `1..n` dense across every DELETE (gap-close) and INSERT (reseat); (d) **append-only link seating** accretes links densely at `[s_L, 1..n_L]`, never sparsely. The catch is that W4 is a *claim of the source note*, not a named invariant of **M5's as-given interface** — and COMPARE's `u1`/`u2` soundness (load-bearing for X12-R1) rests on it. **Ask to M5:** surface D-CTG★ (the `[S, 1..n_S]` dense-slice occupancy that W4 proves) as a named M5 interface invariant, so this seam reliance is documented at the boundary rather than re-derived in M6. Meanwhile M6 **trusts** it (it is M5's write-path property, not M6's to enforce) and keeps it falsifiable: a debug build cross-checks `Σ content_runs(d).width == content_count(d)` with the first run anchored at `[s_C,1]` (and COMPARE `debug_assert`s the V-cursor against `point` per run); a release build reads the counts directly. Every site that depends on D-CTG★ is tagged with that name.

## Internal design

Every operation begins by reading its slices off the single bound snapshot, runs its gate (typed rejection), then composes upstream primitives. Shared helpers:

```rust
fn require_registered(m3: &M3State, d: &Address) -> bool { m3.is_registered_document(d) }

// content (s_C = 1) / link (s_L = 2) subspace constants (ASN-0047). `Nat = BigUint` cannot be `const`,
// so memoize each ONCE via `once_cell::sync::Lazy` instead of re-allocating a fresh `BigUint` on every
// reference. The hot per-position loop (`retrieve_v`) only COMPARES against them — `sub == *S_C` is a
// reference compare with no allocation — while the O(1)-per-query construction sites clone via
// `(*S_C).clone()`.
static S_C: Lazy<Nat> = Lazy::new(|| Nat::from(1u8));
static S_L: Lazy<Nat> = Lazy::new(|| Nat::from(2u8));

/// VSpec WELL-FORMEDNESS only (ASN-0115): zero-free, ordinal-level, level-uniform, depth #start ≥ 2.
/// It deliberately does NOT gate depth-COMPATIBILITY (#start == 2): ASN-0115 is explicit that
/// depth-compatibility is a consulting-state predicate, NOT a well-formedness condition, so a
/// well-formed #start ≥ 3 span passes here and resolves to ⟨⟩ downstream (R6 silent-empty).
fn gate_vspec(span: &Span) -> Result<(), SpecFault> {
    if !span.is_level_uniform()                               { return Err(SpecFault::NotLevelUniform); }   // #start == #width
    if action_point(span.width()) != Some(span.width().len()) { return Err(SpecFault::NotOrdinalLevel); }   // width acts at deepest
    if zeros(span.start()) != 0                               { return Err(SpecFault::StartNotZeroFree); }  // ⇒ all components > 0
    if span.start().len() < 2                                 { return Err(SpecFault::StartTooShallow); }   // ASN-0115 WF: #start ≥ 2; #start ≥ 3 is depth-INCOMPATIBLE (consulting-state), passes → ⟨⟩ (R6)
    Ok(())
}

/// k-th address of a run. LOAD-BEARING ASSUMPTION (used directly here by RETRIEVEV and SHOWDELETIONS,
/// and mirrored by the element-level I-address arithmetic in SHOWORIGIN_V and COMPARE): every
/// content/link I-address has a 2-COMPONENT element field [subspace, ordinal] (zeros = 3), as M3 mints
/// them. `ElemPos` models exactly that 2-component field, so reconstructing i_start as
/// ElemPos{ doc, subspace, ordinal } and advancing the ordinal is faithful and dodges the raw-shift
/// subspace-crossing footgun — but a LONGER element field would be silently truncated here, so a
/// debug tripwire fails loudly if one ever arrives (M3 makes it unreachable — a guard, not a path).
///
/// WHY THE ElemPos ROUND-TRIP, NOT A RAW `shift`: `run_addr` returns a validated **`Address`** (not the
/// bare `Tumbler` a raw `shift` would give) because two of its consumers are `Address`-typed and cannot
/// take a `Tumbler` — `DeliveryItem::Ref(Address)` (RETRIEVEV link references) and
/// `dedup_addrs(impl Iterator<Item = Address>)` (SHOWDELETIONS); the others (`value_at`/`denotes`) read
/// `.tumbler()`, but the `Ref`/dedup paths fix the return type. Do NOT "simplify" this to a raw shift.
/// COMPARE's `reach_i` *does* raw-`shift` an identical element-level i_start — deliberately — because it
/// needs only a `Tumbler` endpoint for the half-open I-interval compare (`lo < hi`), where no `Address`
/// invariant is consumed. Same i_start shape, two different lifts, because the consumers differ.
fn run_addr(i_start: &Address, k: &Nat) -> Address {
    debug_assert!(i_start.element_field().map_or(false, |e| e.len() == 2),
        "run_addr: I-address must carry a 2-component element field [subspace, ordinal] (else silent truncation)");
    let p = ElemPos { doc: document_of(i_start).unwrap(), subspace: i_start.subspace().unwrap(),
                      ordinal: ordinal(i_start.tumbler()).clone() };
    elem_addr(&shift_ordinal(&p, k)).unwrap()
}

/// Dedup a stream of addresses by their `Tumbler` and return them T1-sorted. `Address` is `Eq + Hash`
/// but not `Ord`, so the `Tumbler` carries the order. Used for origin DOCUMENTS (SHOWORIGIN_V) and
/// content I-ADDRESSES (SHOWDELETIONS) alike — both are `Address`, so one neutral helper serves either
/// (the name says "addrs", not "docs", because at the SHOWDELETIONS site the deduped elements are
/// content addresses, not documents).
fn dedup_addrs(it: impl Iterator<Item = Address>) -> Vec<Address> {
    let mut seen: HashSet<Tumbler> = HashSet::new();
    // first-insert-wins dedup, keyed on the Ord-bearing Tumbler (Address is Eq+Hash, not Ord)
    let mut out: Vec<Address> = it.filter(|a| seen.insert(a.tumbler().clone())).collect();
    out.sort_by(|a, b| a.tumbler().cmp(b.tumbler()));   // T1 order on Tumbler
    out
}

/// CURRENT(·, d) on the content side — every content I-address d's arrangement currently binds (the
/// math `content_image(d)`, realized in M6 by enumerating M5's V-ordered content runs per-position,
/// exactly as RETRIEVEV does; M5's own `content_image` is private and is NOT called here). May repeat
/// an address under intra-doc transclusion — callers dedup.
fn arranged_content(m5: &M5State, d: &Address) -> Vec<Address> {
    let mut out = Vec::new();
    for run in m5.content_runs(d) {
        let mut k = Nat::zero();
        while k < run.width { out.push(run_addr(&run.i_start, &k)); k += 1u8; }
    }
    out
}
```

### RETRIEVEV — resolve, then dereference, in order

Two phases, kept separate (the load-bearing factoring of ASN-0115): resolve V-spans to I-addresses (M5), then fetch values (M4 for content) or pass the address through (links).

```rust
pub fn retrieve_v(&self, specs: &[Spec]) -> Result<Delivery, RetrieveError> {
    let (m3, m5, c) = (self.0.world().m3(), self.0.world().m5(), self.0.world().content());
    // Gate the whole request first — VSpec WELL-FORMEDNESS is the only in-model failure (ASN-0115).
    // A well-formed but depth-incompatible (#start ≥ 3) spec is NOT rejected here (R6).
    for (i, s) in specs.iter().enumerate() {
        if !require_registered(m3, &s.doc) { return Err(RetrieveError::DocNotRegistered(s.doc.clone())); }
        gate_vspec(&s.span).map_err(|f| RetrieveError::MalformedSpec { index: i, fault: f })?;
    }
    let mut out = Vec::new();
    for s in specs {                                   // concatenate per spec, IN ORDER (R5) — no global sort
        let sub = s.span.start().get(1).clone();       // 1=content, 2=link (gate ⇒ #start ≥ 2, zero-free; get(1) is the subspace at any depth)
        for run in m5.resolve(&s.doc, &s.span) {       // V-ordered, clipped, gap-aligned; #start ≠ 2 ⇒ ⟨⟩ (depth-incompat)
            let mut k = Nat::zero();
            while &k < &run.width {                     // per active position, ascending V (R3) — no dedup (R8)
                let a = run_addr(&run.i_start, &k);
                if sub == *S_C {
                    out.push(DeliveryItem::Content(
                        c.value_at(a.tumbler()).expect("S3★: content position ⇒ a∈dom(C)").clone()));
                } else if sub == *S_L {
                    out.push(DeliveryItem::Ref(a));     // link reference IS the address — never reads M4
                } else {
                    // UNREACHABLE for an ACTIVE position: S3★-aux confines every bound V-position to
                    // subspace ∈ {s_C, s_L}, and `resolve` yields NO runs for any other start subspace
                    // (M5 holds only content/link positions), so executing here means upstream
                    // corruption. PANIC IN ALL PROFILES — one read-path policy with the S3★ `expect`
                    // above: observed referential-integrity corruption panics; silently dropping an
                    // active position would violate exactness (R3).
                    unreachable!("active V-position must be content or link subspace (S3★-aux)");
                }
                k += 1u8;
            }
        }
    }
    Ok(Delivery(out))                                   // empty spec-set ⇒ Ok(Delivery(vec![]))
}
```

- **Common case:** a single content spec over a contiguous run — one M5 range scan, *w* M4 point lookups (one `Val` per address, each an `Arc` clone). Links never touch M4.
- **Gaps / depth-incompat / foreign subspaces** all funnel through M5's defensive `resolve` returning fewer-or-zero runs → silent empty contribution; the request still succeeds (R6). The `m_S ≡ 2` simplification means depth-incompatibility *is* `#start ≥ 3`: such a start is **well-formed** (ASN-0115 admits `#s ≥ 2`), so `gate_vspec` *passes* it and `resolve` force-empties it — the R6 silent-empty contribution, never a rejection (depth-compatibility is consulting-state, *not* well-formedness). A start subspace ∉ {1,2} is likewise force-empted upstream (M5 holds no such positions), so the closed `else` arm cannot execute while a run exists — and if it ever does, it `unreachable!`-panics in **all profiles**, the same policy as the S3★ `expect` (observed corruption on the read path panics, never silently drops an active position).
- **Tradeoff:** I deliver **one item per active V-position** (one `Val` or one `Ref`), not coalesced segments. This is the exact, no-dedup form (R3/R8) and sidesteps byte-clipping entirely — at M4's granularity each address holds one opaque `Val`, so there is no intra-position byte boundary for M6 to realize. Streamed/segmented delivery is an open decision; M5's runs are already gap-aligned, so a segment form would also be safe.
- The `expect` trusts S3★ (M5's content-side referential integrity); a `None` there means upstream corruption, and panicking is the correct read-path response (silently skipping would violate exactness). The `unreachable!` else-arm applies the identical policy to S3★-aux — the read path has one broken-invariant response (panic in all profiles), not two.

### RETRIEVEDOCVSPAN & RETRIEVEDOCVSPANSET — synthesize from counts

Both read `content_count`/`link_count` (M5 O(1) hints) and synthesize spans. Occupied positions are the dense runs `[s_C, 1..n_C]` and `[s_L, 1..n_L]` (D-CTG★, the dense-slice occupancy ASN-0113 W4 proves), so the counts *are* the extents and no scan is needed.

```rust
pub fn doc_vspan(&self, doc: &Address) -> Result<SpanSet, ExtentError> {
    let (m3, m5) = (self.0.world().m3(), self.0.world().m5());
    if !require_registered(m3, doc) { return Err(ExtentError::DocNotRegistered(doc.clone())); }   // unallocated ⇒ fail
    let (nc, nl) = (m5.content_count(doc), m5.link_count(doc));
    if nc.is_zero() && nl.is_zero() { return Ok(SpanSet::empty()); }                 // registered-empty ⇒ ⟨⟩
    let min = vpos(if !nc.is_zero() { (*S_C).clone() } else { (*S_L).clone() }, &Nat::one());          // min O(d): anchor of lowest occupied subspace
    let max = vpos(if !nl.is_zero() { (*S_L).clone() } else { (*S_C).clone() }, if !nl.is_zero() { &nl } else { &nc });
    let reach = shift(&max, &Nat::one());                                            // one ordinal step past max
    // from_endpoints is INFALLIBLE here: #min == #reach == 2 (both depth-2 V-positions ⇒ no
    // LevelMismatch) and min ≤ max < reach ⇒ min < reach (no NotIncreasing). The stored width
    // reach⊖min round-trips exactly — divergence(min,reach) ≤ #min (=2) discharges D1, INCLUDING the
    // cross-subspace box (min=[s_C,1], reach=[s_L,n_L+1], diverging at position 1) — so Span::reach()
    // recovers reach and the singleton is faithfully ASN-0112's σ_d = (origin_d, extent_d).
    Ok(SpanSet::singleton(Span::from_endpoints(min, reach).unwrap()))                // origin=min; width=reach⊖min
}

pub fn doc_vspanset(&self, doc: &Address) -> Result<SpanSet, ExtentError> {
    let (m3, m5) = (self.0.world().m3(), self.0.world().m5());
    if !require_registered(m3, doc) { return Err(ExtentError::DocNotRegistered(doc.clone())); }
    let (nc, nl) = (m5.content_count(doc), m5.link_count(doc));
    let mut result = SpanSet::empty();
    if !nc.is_zero() { result = union(&result, &SpanSet::singleton(ext_span((*S_C).clone(), &nc))); }  // ext(d,s_C) = ([1,1],[0,n_C])
    if !nl.is_zero() { result = union(&result, &SpanSet::singleton(ext_span((*S_L).clone(), &nl))); }  // ext(d,s_L) = ([2,1],[0,n_L])
    debug_assert!(result.is_normalized(), "W13: content-before-link, subspace-separated ⇒ already normal");
    Ok(result)   // disjoint, content-before-link, appended in order ⇒ already W13-normal (union is concat, never normalizes/faults)
}
```
where
```rust
fn vpos(s: Nat, n: &Nat) -> Tumbler { Tumbler::new([s, n.clone()]).unwrap() }   // depth-2 V-position [subspace, ordinal]
fn ext_span(s: Nat, n: &Nat) -> Span {                                          // ext(d,S) = ([S,1], [0,n_S])
    Span::new(Tumbler::new([s, Nat::one()]).unwrap(),
              Tumbler::new([Nat::zero(), n.clone()]).unwrap()).unwrap()
}
```

- **`doc_vspan`** returns a single bounding span; across subspaces it is a bounding box bridging the inter-subspace void (`[1,1]..[2,n_L+1)`), insensitive to mid-document content edits (V9) — by design (route fragmentation-sensitive callers to `doc_vspanset`).
- **Negative-origin hazard (0112 OQ5) designed out:** because `min` is read as the subspace anchor `[s,1]` rather than absorbed into a confluent summary, the origin can never go negative.
- **No invented M1 surface:** `doc_vspanset` builds the ≤2-member set by **`union` of singletons** (concatenation preserves the already-disjoint, content-before-link W13 normal form, asserted in debug), not a fabricated `from_normalized_ordered`.
- **Tradeoff:** trusting `content_count`/`link_count` rests on D-CTG★, the dense-slice occupancy ASN-0113 W4 proves (M5's write-path property, not M6's). A debug-build cross-check (`Σ content_runs(d).width == content_count(d)` and first run anchored at `[s_C,1]`) is cheap defense-in-depth (open decision).

### SHOWORIGIN_V — block-decompose, project one origin per run

Origin is the pure address projection `document_of` (M1). Block uniformity (O2) means all addresses in one run share an origin, so M6 projects **one address per run** — O(runs), not O(positions).

```rust
pub fn show_origin_v(&self, doc: &Address, span: &Span) -> Result<Vec<Address>, OriginError> {
    let (m3, m5) = (self.0.world().m3(), self.0.world().m5());
    if !require_registered(m3, doc)        { return Err(OriginError::DocNotRegistered(doc.clone())); }   // WF_V (i)
    gate_vspec(span).map_err(OriginError::MalformedSpan)?;                                  // (ii),(iv): ordinal-level, level-uniform, #start ≥ 2 (well-formedness)
    let sub = span.start().get(1);                                                          // subspace at any depth
    let n_s = if *sub == *S_C { m5.content_count(doc) }
              else if *sub == *S_L { m5.link_count(doc) }
              else { return Err(OriginError::NoSuchSubspace); };                            // foreign subspace ∉ {s_C,s_L}: distinct from a real-but-empty subspace
    if n_s.is_zero() { return Err(OriginError::EmptySubspace); }                            // (iii) inadmissible on a real but empty subspace
    if span.start().len() != 2 { return Err(OriginError::DepthIncompatible); }              // (v): span depth must equal m_S ≡ 2; #start ≥ 3 is depth-incompatible — reject (O13), distinct from a range overrun
    let runs = m5.resolve(doc, span);                                                       // span now depth-2 (≥3 rejected above); may be partial if it overruns the bound prefix
    let resolved: Nat = runs.iter().map(|r| &r.width).sum();
    if &resolved < ordinal(span.width()) { return Err(OriginError::RangeNotPresent); }      // (vi): names depth-2 positions not all bound — reject, never clamp (O13)
    Ok(dedup_addrs(runs.iter().map(|r| document_of(&r.i_start).unwrap())))                  // link case ⇒ {doc} by CL-OWN
}
```

- The `(iii)`/`(v)`/`(vi)` checks are the deliberate strictness: SHOWORIGIN_V is **inadmissible on an empty document, a foreign or empty subspace, a span whose depth ≠ m_S, and a span overrunning the bound prefix** — reject-and-signal, never clamp to the surviving sub-span (the digest's explicit choice, O13). Each inadmissibility carries its **own** error: a start subspace ∉ {s_C, s_L} is `NoSuchSubspace` (kept distinct from `EmptySubspace`, a *real* subspace — s_C or s_L — with no occupied positions, WF_V(iii)); a depth-incompatible `#start ≥ 3` span is `DepthIncompatible` (WF_V(v): span depth must equal the subspace common depth `m_S ≡ 2`); a depth-2 span that names positions past the bound prefix is `RangeNotPresent` (WF_V(vi)). The depth and overrun cases are kept **separate** so M10/clients can localize the cause — "wrong-depth span" is not conflated with "named positions aren't all bound."
- **WF_V(v) and WF_V(vi) are discharged by two separate checks.** `gate_vspec` enforces only VSpec well-formedness (`#start ≥ 2`, ordinal-level, level-uniform, zero-free) — it does **not** pin `#start == 2` (*Conflicts resolved* 1/8). SHOWORIGIN_V's own depth requirement (WF_V(v): the span's depth must equal the subspace common depth `m_S ≡ 2`) is discharged by an explicit `span.start().len() != 2 ⇒ DepthIncompatible` check *before* resolving. The range condition (WF_V(vi): every named depth-2 position is bound) is then discharged by the `resolved < ordinal(span.width())` ⇒ `RangeNotPresent` test on the depth-2 span. **The nominal count is read via `ordinal(span.width())`** — the last component, which level-uniformity ties to `#start` — not a hard-coded `width.get(2)`; reading it positionally keeps the overrun test depth-agnostic. Splitting the depth case out into its own `DepthIncompatible` error (rather than letting a `#start ≥ 3` span fall through `resolve`-empties-it ⇒ `resolved = 0 < ordinal(width)` ⇒ `RangeNotPresent`) is what lets a client tell "wrong depth" from "unbound positions."
- For the link subspace, `document_of(link)` is the home `doc` (CL-OWN) — handled uniformly, no special case.

### SHOWORIGIN_I — de-scoped (ruling)

`origins_I(σ) = {document_of(a) : a ∈ ⟦σ⟧ ∩ dom(C)}` requires enumerating allocated content addresses across an I-interval. No upstream surface provides this: M4 is point-only with `Ord` **deliberately** unused and its boundary forbidding range/prefix scans, and M3's registry is point-only (`is_allocated`). Stateless M6 has no fold hook to grow its own index. The I-arity is therefore **de-scoped from M6 and recorded as a decomposition amendment** — were it ever needed, it belongs to a *new* I-ordered content index (a recomputable hint over M4's append-only writes, e.g. `allocated_content_in(span)`), which is a change to the module decomposition, not an M6 internal. Only `show_origin_v` ships, and `OriginError` carries no `ISpanIndexUnavailable` placeholder; the prior `show_origin_i` placeholder is removed.

Two flags travel with the ruling so it does not silently diverge from the system docs:
- **Preferring the V-arity is M6's call, not ASN-0077's.** The note designates *neither* arity "reader-facing"; M6 rules the V-arity the one it ships.
- **The de-scope is settled, not conditional.** It is settled **by construction**: M10 can marshal only what M6's `Query` exposes, and that is `show_origin_v` alone — there is no I-arity method *anywhere* for the FEBE surface to reach (the I-arity would need the forbidden M4 index, which no module provides). The client surface therefore promises no SHOWORIGIN-over-I. This by-construction argument is the load-bearing one; M10's enumerated reader-marshaling sources (ASN-0111/0112/0113/0114/0115/0121/0122/0124/0131/0132) corroborate it only **vacuously**, since that list omits ASN-0077 **and** ASN-0075 *entirely* — its silence on a SHOWORIGIN-over-I command therefore says nothing positive. (That same omission is itself an **M10-side reader-marshaling reconciliation item, not an M6 defect**: 0077 and 0075 are exactly the two M6 readers M6 *does* ship — `show_origin_v` and `show_deletions` — so M10's source list should name them.) The recorded amendment stands as future work (the new I-ordered index is where the I-arity would land *if* ever surfaced), not a live capability hole.

### SHOWDELETIONS — gate, then membership-test the cross-document combine in M6

`DeletedFromAWithB = {a ∈ dom(C) : DELETED(a, d_A) ∧ CURRENT(a, d_B)}` and its symmetric twin are a **cross-document** filter: the addresses *current in one* document that are *deleted from the other*. Read as a **membership test** rather than a set intersection, it builds directly on the upstream interfaces *as given* — no M5 amendment:

> `a_with_b = { a ∈ content_image(d_B) : DELETED(a, d_A) }`

- enumerate `content_image(d_B)` exactly as RETRIEVEV enumerates content — `m5.content_runs(d_b)` per-position through `run_addr` (this *is* CURRENT(·, d_B) for content addresses, by definition of `ran`; realized by the `arranged_content` helper);
- test `DELETED(a, d_A)` by membership in M5's per-document deleted cover: `m5.deletions(d_a).denotes(a.tumbler())`. `deletions(d) = ever_placed(d) ∖ content_image(d) = { a : DELETED(a, d) }` (M5 computes it per level-class, fault-free); `denotes` (M1) faults on nothing and is **exact** here by `difference_sets`' denotational contract — `⟦deletions(d)⟧ = ⟦ever_placed(d)⟧ ∖ ⟦content_image(d)⟧ = {x : DELETED(x,d)}` exactly, whatever the cover's internal span packing (detailed below) — so the membership test recovers `DELETED` with no false positives;
- symmetric for `b_with_a`: `content_image(d_A)` filtered by `deletions(d_b).denotes(·)`.

```rust
pub fn show_deletions(&self, d_a: &Address, d_b: &Address) -> Result<Deletions, DeletionsError> {
    let (m3, m5) = (self.0.world().m3(), self.0.world().m5());
    for d in [d_a, d_b] {
        if !require_registered(m3, d) { return Err(DeletionsError::DocNotRegistered(d.clone())); }
    }
    let del_a = m5.deletions(d_a);   // { a : DELETED(a, d_a) } as a per-level-class cover
    let del_b = m5.deletions(d_b);   // { a : DELETED(a, d_b) }
    // a_with_b = current-in-B ∧ deleted-from-A;  b_with_a = current-in-A ∧ deleted-from-B
    let a_with_b = dedup_addrs(arranged_content(m5, d_b).into_iter()
        .filter(|a| del_a.denotes(a.tumbler())));
    let b_with_a = dedup_addrs(arranged_content(m5, d_a).into_iter()
        .filter(|a| del_b.denotes(a.tumbler())));
    Ok(Deletions { a_with_b, b_with_a })
}
```

- **Output is address sets** — each half is the deduped, Tumbler-ordered `Vec<Address>` of the *existing* I-addresses (D-IDENT: "the returned reference is precisely the I-address `a`," never a copy; D-ORD: T1-orderable). No SpanSet re-encoding, so no exactness/lossless caveat applies.
- **No M4 access** — DELETED/CURRENT are arrangement + R facts; bytes are never fetched. Both documents registered-but-empty ⇒ `deletions` and `content_runs` both empty ⇒ empty halves.
- **`denotes` exactness, by `difference_sets`' denotational contract.** Testing `denotes(a)` recovers `DELETED(a, d_A)` exactly — *unconditionally*, with no chain-confinement reasoning needed. M5's `deletions(d) = ever_placed(d) ∖ content_image(d)` is a **set difference**, and M1's `difference_sets` is denotational: `⟦difference_sets(A, B)⟧ = ⟦A⟧ ∖ ⟦B⟧` by definition. A span coalesced *across* a non-deleted ordinal would change the cover's denotation — it would denote a still-live address as deleted — so it **cannot occur** in a correct `difference_sets`: the two unit spans straddling a live ordinal are non-adjacent and stay separate (`merge`, M1, coalesces only *adjacent* spans). Hence `⟦deletions(d)⟧ = {x : DELETED(x, d)}` *exactly*, whatever the internal span packing, and `deletions(d_a).denotes(a.tumbler())` is the exact membership test — the test inputs from `arranged_content` happen to be real content addresses, but the exactness does not even lean on that. (A purely defensive, exactness-independent restatement `DELETED(a, d_A) ≡ ever_placed(d_a).denotes(a) ∧ a ∉ arranged_content(d_a)` — `ever_placed` + `content_runs`, both M5 as given — is available as a *test cross-check*, but v1 needs nothing beyond the denotational contract and ships the `deletions` form on M5's stated fault-free, read-straight-off seam.)
- **Single consistent `(M, R)`** — every read is off the one bound `&Snapshot`; M2 commits composites atomically, so the digest's "R-ahead-of-M phantom deletion" cannot arise (no torn read).
- **D-DISJ guard (optional, M6-local)** — when `deletions(d_a)` is empty, `a_with_b` is empty without enumerating `arranged_content(d_b)` (symmetrically for `b_with_a`): a cheap sufficient case of D-DISJ's R-disjointness, folded into M6 since the combine now lives here.

### COMPARE — interval equi-join on I-address, complete under fan-out

The contract is a relational join keyed on **address equality, never value** — so COMPARE **never opens M4**. Three phases: resolve regions to blocks, interval-join on the I-axis with cross-product on overlap, coalesce-and-canonicalize.

```rust
pub fn compare(&self, rho1: &[Region], rho2: &[Region]) -> Result<CompareReport, CompareError> {
    let (m3, m5) = (self.0.world().m3(), self.0.world().m5());
    // Gate per operand so a MalformedSpan/NotContentSubspace fault carries an unambiguous
    // (operand, region, span-index) — FINDDOCSCONTAINING's (region, index) plus the operand tag.
    for (operand, regions) in [(Operand::First, rho1), (Operand::Second, rho2)] {
        for (ri, r) in regions.iter().enumerate() {
            if !require_registered(m3, &r.doc) { return Err(CompareError::DocNotRegistered(r.doc.clone())); }
            for (si, span) in r.spans.iter().enumerate() {
                if *span.start().get(1) != *S_C {                                            // start in content subspace
                    return Err(CompareError::NotContentSubspace { operand, region: ri, index: si });
                }
                gate_vspec(span).map_err(|f| CompareError::MalformedSpan { operand, region: ri, index: si, fault: f })?;
            }
        }
    }
    let (p, q) = (resolve_blocks(m5, rho1), resolve_blocks(m5, rho2));   // Vec<Block>; reads ONLY M5
    let pairs  = interval_join(&p, &q);                                  // cross-product per overlap (X8 completeness)
    Ok(CompareReport(canonicalize(pairs)))                              // R1–R3 conforming, deterministic order (X12)
}

// Transient per-query working row for COMPARE: built by `resolve_blocks`, consumed by `overlap_pair`/
// `interval_join`/`reach_i`; dropped at return. One block per resolved I-run of one region span.
struct Block { doc: Address, v_start: Tumbler, i_start: Address, width: Nat }

fn resolve_blocks(m5: &M5State, regions: &[Region]) -> Vec<Block> {
    let mut out = Vec::new();
    for r in regions {
        for span in &r.spans {
            // V-RECONSTRUCTION LEMMA (load-bearing for X12-R1 soundness, correct ONLY under D-CTG★):
            // content is gap-free, so the FIRST bound V-position of a content span IS span.start(), and
            // resolve's runs tile the bound prefix CONTIGUOUSLY in V. Hence the V-cursor starts at
            // span.start() and advances by each run's width — there are no V-gaps to skip. A depth-
            // incompatible (#start ≥ 3) content span resolves to ⟨⟩, so produces no blocks (empty region).
            let mut v = span.start().clone();
            for run in m5.resolve(&r.doc, span) {
                // Assert the lemma on EVERY run: M(d)(v-cursor) == this run's i_start. Firing per run
                // (not first-run-only) localizes a future M5 density regression to the EXACT mis-aligning
                // run, instead of letting a mid-document V-gap slip past a first-run check and silently
                // mis-set a later block's v_start. (`vpos_of(&v)` is depth-2-safe each iteration — a run
                // exists only for a depth-2 span.) NB: `debug_assert!` with `==`, not `debug_assert_eq!`
                // — Address/Tumbler are PartialEq but NOT Debug, so the *_eq! form (which {:?}-formats on
                // failure) would fail to typecheck in every profile; `==` needs only PartialEq.
                debug_assert!(m5.point(&r.doc, &vpos_of(&v)).as_ref() == Some(&run.i_start),
                    "D-CTG★: each content run must begin at the V-cursor (gap-free tiling)");
                out.push(Block { doc: r.doc.clone(), v_start: v.clone(),
                                 i_start: run.i_start.clone(), width: run.width.clone() });
                v = shift(&v, &run.width);                                  // accumulate V offset by run width (no V-gaps in content)
            }
        }
    }
    out
}

// ── COMPARE helpers — ALL operate on `Tumbler` (thread `.tumbler()` off any `Address`) ──
// CO-CHAIN PRECONDITION: `overlap_pair` calls `ordinal_gap` only AFTER the `lo < hi` overlap guard,
// i.e. only on runs whose I-intervals overlap. Overlapping content runs lie on ONE content chain
// (shared origin sub-allocator ⇒ equal-length, equal prefix below the action point), so a bare
// ordinal subtraction is a TOTAL `Nat` op — no borrow, no underflow. Different-chain pairs have
// disjoint I-intervals and are rejected by the guard before any ordinal arithmetic runs.
fn reach_i(b: &Block) -> Tumbler { shift(b.i_start.tumbler(), &b.width) }   // i_start ⊕ δ(width,#): one I-step past the run; raw shift SAFE (i_start element-level, last comp = ordinal) — a bare `Tumbler` endpoint is all the `lo < hi` compare needs; cf. `run_addr`'s `Address` round-trip
fn ordinal_gap(hi: &Tumbler, lo: &Tumbler) -> Nat { ordinal(hi).clone() - ordinal(lo).clone() }  // co-chain ⇒ ordinal(hi) ≥ ordinal(lo)
fn max_tumbler(a: &Tumbler, b: &Tumbler) -> Tumbler { if a >= b { a.clone() } else { b.clone() } }
fn min_tumbler(a: &Tumbler, b: &Tumbler) -> Tumbler { if a <= b { a.clone() } else { b.clone() } }
fn vpos_of(t: &Tumbler) -> VPos { VPos { subspace: t.get(1).clone(), ordinal: t.get(2).clone() } }                // depth-2 V-pos → VPos
fn vpos_shift(v: &Tumbler, k: &Nat) -> VPos { VPos { subspace: v.get(1).clone(), ordinal: v.get(2).clone() + k } } // advance ordinal by k

fn overlap_pair(pb: &Block, qb: &Block) -> Option<CorrPair> {
    let lo = max_tumbler(pb.i_start.tumbler(), qb.i_start.tumbler());   // I-interval overlap, on Tumblers
    let hi = min_tumbler(&reach_i(pb), &reach_i(qb));
    if !(lo < hi) { return None; }                                     // disjoint I-intervals ⇒ no correspondence
    // lo < hi now discharges the co-chain precondition: every ordinal_gap below is total.
    Some(CorrPair {
        d1: pb.doc.clone(),
        u1: vpos_shift(&pb.v_start, &ordinal_gap(&lo, pb.i_start.tumbler())),  // slot 1 ⇐ operand 1; lo's offset WITHIN P
        d2: qb.doc.clone(),
        u2: vpos_shift(&qb.v_start, &ordinal_gap(&lo, qb.i_start.tumbler())),  // slot 2 ⇐ operand 2; lo's offset WITHIN Q
        width: ordinal_gap(&hi, &lo),                                         // overlap width
    })
}

fn interval_join(p: &[Block], q: &[Block]) -> Vec<CorrPair> {
    // v1 REFERENCE IMPLEMENTATION: exhaustive O(|P|·|Q|) double-loop block join — emit EVERY
    // I-overlap (X8 fan-out completeness). Sort-by-i_start + sweep (or an interval tree) is a
    // drop-in optimization of this SAME join (same pair multiset); the independent TEST ORACLE is
    // a per-position hash join on address. One vocabulary — see Open build decisions (canonical).
    let mut out = Vec::new();
    for pb in p { for qb in q { if let Some(c) = overlap_pair(pb, qb) { out.push(c); } } }
    out
}

fn canonicalize(mut pairs: Vec<CorrPair>) -> Vec<CorrPair> {
    // Deterministic presentation (X12 R3) of the complete+sound relation (R1/R2); NOT claimed maximal
    // (R4 optional). Sort lexicographically by (d1, u1, d2, u2). `sort_by_cached_key` computes each
    // four-`Tumbler` key ONCE per element — not twice per *comparison* as a bare
    // `sort_by(|x,y| corr_key(x).cmp(&corr_key(y)))` would, which clones O(n log n) keys — and stays a
    // STABLE sort, so duplicate overlaps keep a deterministic listed order (R3). The adjacent-pair fold
    // is the IDENTITY in v1 (a finer-than-maximal, per-overlap report conforms — see `fold_adjacent`).
    pairs.sort_by_cached_key(corr_key);
    fold_adjacent(pairs)
}
fn corr_key(c: &CorrPair) -> (Tumbler, Tumbler, Tumbler, Tumbler) {
    (c.d1.tumbler().clone(), vpos_tumbler(&c.u1), c.d2.tumbler().clone(), vpos_tumbler(&c.u2))
}
fn vpos_tumbler(v: &VPos) -> Tumbler { Tumbler::new([v.subspace.clone(), v.ordinal.clone()]).unwrap() }

/// Adjacent-pair folding is OPTIONAL — X12 R4 (maximal pairs) is NOT required, and a per-overlap,
/// finer-than-maximal report already satisfies R1–R3. v1 ships the IDENTITY (no fold); the reference
/// is therefore complete, not an unimplemented stub. A builder wanting the X11 maximal form merges
/// feet-successor-adjacent pairs here (pair₂'s two feet are the unit-successors of pair₁'s last
/// positions AND their I-addresses are consecutive) into one wider pair — a pure presentation
/// post-pass that never changes ⟦Γ⟧.
fn fold_adjacent(pairs: Vec<CorrPair>) -> Vec<CorrPair> { pairs }   // identity — conforming (R4 optional)
```

- **The second foot is computed within its own block.** `u2` offsets `qb.v_start` by `lo ⊖ qb.i_start` (lo's position *inside the Q-block*), not `lo ⊖ pb.i_start`. In the normal cross-document case `lo = max(pb.i_start, qb.i_start)` is one operand's start, so the inter-block gap would otherwise shift `u2` and make `res_Σ(d2, u2) ≠ a` — a violation of X12 **R1 (soundness)**. With the per-block offset, both feet resolve to the shared address `lo`.
- **Co-chain totality of the ordinal arithmetic.** Every `ordinal_gap` in `overlap_pair` runs only after the `lo < hi` overlap guard, hence only on addresses sharing one content chain (equal-length, equal prefix below the action point) — so the bare `ordinal(·) − ordinal(·)` subtractions are total `Nat` operations. Different-chain block pairs have disjoint I-intervals and are rejected by the guard before any subtraction. The helpers (`reach_i`/`ordinal_gap`/`max_tumbler`/`min_tumbler`/`vpos_shift`/`vpos_of`) all operate on `Tumbler` (callers thread `.tumbler()` off the `Address`), so the I-axis comparison typechecks uniformly (no `Address`/`Tumbler` mixing).
- **V-reconstruction lemma (load-bearing for X12-R1 soundness).** `resolve_blocks` sets the first run's `v_start = span.start()` and accumulates `v_start` by each run's width. This is correct **only because content is gap-free** (D-CTG★, the dense-slice occupancy ASN-0113 W4 proves): the first bound V-position of a content span *is* `span.start()`, and `resolve`'s runs tile the bound prefix contiguously in V, so there are no V-gaps to skip. The code states this as the lemma it is and **`debug_assert`s it on *every* run** (`M(d)(v-cursor) == this run's i_start`, via `m5.point`), so a future M5 regression to V-gapped content runs fails loudly **at the exact mis-aligning run** rather than silently mis-aligning `u1`/`u2` (it would then need per-position `point` resolution or a V-carrying run type). Asserting per-run, not first-run-only, is what localizes the failure: under D-CTG★ a first-run check would transitively cover the rest, but a per-run check pins a regression to the precise run that broke density. The tripwire is a `debug_assert!` with `==` (not `debug_assert_eq!`) precisely because `Address`/`Tumbler` are `PartialEq` but not `Debug` — the `*_eq!` form's failure-path `{:?}` formatting would fail to compile in every profile.
- **Report granularity is deterministic because M5's block decomposition is canonical (the second determinism reliance, beside D-CTG★).** X12 R3 demands the emitted report be a function of `(ρ₁, ρ₂, res_Σ|P, res_Σ|Q)` — "no hidden input and no nondeterminism." M6 emits finer-than-maximal pairs, one per I-overlap of resolved runs, so the pair *granularity* inherits `resolve`'s run splits. That is R3-conforming only because M5's POOM block decomposition is **canonical** — unique maximal runs (ASN-0058 split/merge/canonicalize) — which makes the run splits a pure function of the arrangement restriction `res_Σ|P` / `res_Σ|Q`, never of the edit history that built it. A future M5 relaxation of run canonicality would leave `⟦Γ⟧` correct (R1/R2 are denotational) but make the *listed* pairs history-dependent — an R3 violation. Named here and in the *Delegated* list so it is caught at the seam, not silently.
- **Fan-out completeness is the whole game** (the place a naïve implementation goes wrong): when an address occurs in multiple P-blocks and/or Q-blocks, `interval_join` must emit the **full cross-product** over each I-overlap, not a lockstep merge. v1 ships the exhaustive double-loop block join as the **reference implementation**; sort-by-`i_start` + sweep (or an interval tree) is a drop-in optimization of the *same* join, and the independent **test oracle** is a per-position hash join on address (*Open build decisions* carries the one canonical statement of this vocabulary). All three consume blocks/addresses only and never read bytes — simultaneously the correctness property (value-matching over-reports) and the perf property (no content fault).
- **Overlapping windows within one operand are redundant, not wrong.** ASN-0122 X12 permits a spec-set to name overlapping (or repeated) windows; `resolve_blocks` then double-covers the shared V-positions, and `interval_join` emits the overlap pair more than once. This is **denotationally conforming** — `⟦Γ⟧` is a set-union, so duplicates collapse in the denotation (R1/R2 hold), and the *stable* `sort_by_cached_key` in `canonicalize` keeps the listed order deterministic (R3) regardless of duplicate count. A builder may pre-dedupe each operand's regions to shrink the cross-product; correctness does not require it.
- **`canonicalize`** sorts the pairs lexicographically by `(d1, u1, d2, u2)`, then applies `fold_adjacent`. This is a **deterministic** presentation (X12 R3) of the **complete and sound** relation (R1/R2); it is **not** claimed to be the X11 **maximal** form — X12 **R4 (maximal pairs) is explicitly not required for conformance**. In v1 `fold_adjacent` is the **identity** (a finer-than-maximal, per-overlap report fully conforms under R1–R3); a builder wanting maximal output merges feet-successor-adjacent pairs (pair₂'s feet are the unit-successors of pair₁'s last positions *and* their I-addresses are consecutive) into one wider pair — a pure presentation post-pass that never changes `⟦Γ⟧`. The second-foot tie-break in the sort key is load-bearing under fan-out.

### FINDDOCSCONTAINING — resolve, then a present-tense filter over M5's R⁻¹ superset

This is the digest's recommended "monotone index + present-tense filter," with **M5 owning the monotone R⁻¹ index** and M6 owning only the resolve-union and the filter.

```rust
pub fn find_docs_containing(&self, regions: &[Region]) -> Result<Vec<Address>, FindError> {
    let (m3, m5) = (self.0.world().m3(), self.0.world().m5());
    // Gate each region span for WELL-FORMEDNESS (gate_vspec: zero-free, #start≥2, ordinal-level,
    // level-uniform) — a malformed / non-ordinal-level span (e.g. [s_C,3] width [1,0]) would otherwise
    // silently UNDER-resolve through `resolve_coverage` and drop containers (FD-COMPLETE), inconsistent
    // with M6's typed-rejection-over-silent-empty rule elsewhere. The gate does NOT restrict subspace:
    // a link/foreign-subspace span [s_L,·] passes and stays inert downstream — FD's image_C content-
    // restriction is realized by M5's R⁻¹ (`docs_containing` indexes content provenance only; link
    // placement is R-uncoupled, J-LV) and the content-only `project` filter, so it can add no spurious
    // container. A depth-incompatible (#start≥3) span passes the gate and `resolve_coverage` empties it
    // (consulting-state, exactly like RETRIEVEV's R6) — contributing nothing, never a rejection.
    let mut coverage = SpanSet::empty();                                // Phase 1: resolve to content I-coverage
    for (ri, r) in regions.iter().enumerate() {
        if !require_registered(m3, &r.doc) { return Err(FindError::DocNotRegistered(r.doc.clone())); }
        for (si, span) in r.spans.iter().enumerate() {
            gate_vspec(span).map_err(|f| FindError::MalformedSpan { region: ri, index: si, fault: f })?;
            coverage = union(&coverage, &m5.resolve_coverage(&r.doc, span));   // raw mixed-length; concat
        }
    }
    let candidates = m5.docs_containing(&coverage);                     // Phase 2: R⁻¹ superset, tumbler-ordered (handles level-classes internally)
    Ok(candidates.into_iter()
        .filter(|d| m5.project(d, &coverage) != SpanSet::empty())      // present-tense soundness filter (FD-SOUND) — one project/candidate
        .collect())
}
```

- The filter is the only difference between the live answer and the historical "ever-contained" answer (`docs_containing` alone) — exactly the step the reference omits. `project(d, coverage)` is an I→V lookup, not a re-search; cost is proportional to the candidate set. Emptiness is tested with **`!= SpanSet::empty()`** (derived structural `PartialEq`), not a fabricated `.is_empty()` — and this structural test is a valid *denotational* emptiness check **only** because of M1's span-set guarantee that **no algebra result ever carries a zero-width member**. Every span member therefore denotes at least one position, so a denotationally-empty `project` result must have *zero* members — i.e. it is exactly the length-0 `SpanSet::empty()`, never a structurally-non-empty vector with an empty denotation. The check rests on that named M1 invariant; the ask for exactly this — a `SpanSet`-level, `denotes`-free emptiness predicate (`is_empty`) — is **recorded on the M1 seam** (*Dependencies & seams*), and switching to it when it lands would be strictly more robust, since it would not lean on the canonical-structural-form argument at all.
- **Each region span is well-formedness-gated** (`gate_vspec`), so a malformed or non-ordinal-level span is a typed `MalformedSpan { region, index, fault }` rejection rather than a silent under-resolution that drops containers (FD-COMPLETE). The gate checks *well-formedness only*, never subspace — a link/foreign-subspace span passes and stays inert downstream (it adds nothing to the content-only R⁻¹/`project` machinery), and a depth-incompatible (`#start ≥ 3`) span passes and resolves to empty coverage (consulting-state, contributing nothing — never a rejection).
- `resolve_coverage` returns raw, possibly mixed-length covers; `docs_containing`/`project` apply the level-class discipline **internally** (M5 contract), so M6 passes the raw union straight through — M6 owns no level-class discipline anywhere.
- Bare deduplicated identities, no positions/counts (FD codomain), tumbler-ordered (deterministic).

## Invariants & contracts

**By construction** (fall out of the read-only/one-snapshot model and leaning on upstream):
- *No mutation; snapshot value, not live view* — M6 has no write path and returns owned values; the `im` slices it reads are immutable. (R-frame 0115; V-frame/V16 0112; W8 0113; O10 0077; D-OBS 0075; X12 frame 0122; FD-FRAME 0124.)
- *Single consistent `(M, R)` snapshot* — every constituent of a query is read off one `&Snapshot` (M2 clause 6). (0075 consistent-snapshot; 0124 composite-boundary; 0122 single-Σ.)
- *Permanence / faithfulness of delivered content* — M4 has no delete and `value_at` returns the stored bytes verbatim. (R11/R2 0115.)
- *Arrangement relativity / locality* — each spec resolves only through its named document's `M(d)` via M5. (R4 0115; X5 0122; FD-LOCAL 0124.)
- *No-dedup, multiplicity, order fidelity* — per-spec concatenation, ascending-V within, no global sort. (R5/R8 0115.)
- *Origin by projection, unstrippable* — `document_of` reads the address only; one origin per run by block uniformity. (O2/O3/O5 0077.)
- *Correspondence by address equality, value-blind* — COMPARE joins on I-address and never opens M4. (X1/X2 0122; FD-IDENT 0124.)
- *Deletion sets are the existing I-addresses* — SHOWDELETIONS returns the addresses themselves, never copies, T1-orderable. (D-IDENT/D-ORD 0075.)
- *Two-kinds-only, disjoint, pre-normalized extents* — fixed two-subspace iteration. (W9/W11/W13 0113.)

**By active enforcement** (M6 must guard, with the site named):
- *Well-formedness gates → typed rejection* — `gate_vspec` + `require_registered` at each operation's entry; the chief in-model failures. `gate_vspec` enforces VSpec *well-formedness only* — zero-free, ordinal-level, level-uniform, depth `#start ≥ 2` (`StartTooShallow` for `#start < 2`) — and does **not** gate depth-*compatibility*: a `#start ≥ 3` span is well-formed (ASN-0115 admits `#s ≥ 2`) and passes, resolving to ⟨⟩ downstream (R6 silent-empty for RETRIEVEV; empty region for COMPARE; `DepthIncompatible` for SHOWORIGIN_V). Folding `#start == 2` into the gate would be an over-reach — ASN-0115 makes depth-compatibility a consulting-state predicate, not well-formedness. (0115 well-formedness; WF_V 0077; W-pre 0112/0113; precondition 0122.)
- *Registered-empty → result vs. unallocated → fail* — **M6's owned distinction**, via `m3.is_registered_document`, applied per-operation (and tightened for SHOWORIGIN_V, which additionally rejects an empty *real* subspace as `EmptySubspace` and a *foreign* subspace as `NoSuchSubspace`). (Decomposition; W-pre 0113; WF_V(iii) 0077.)
- *Single-subspace at the gate* — the ordinal-level check in `gate_vspec` makes a straddle unrepresentable for RETRIEVEV. (R10 0115.)
- *Partial-delivery never fails* — gaps/depth-incompat/foreign-subspace become empty contributions, never errors. (R6 0115.)
- *SHOWORIGIN_V admissibility* — reject empty document, foreign subspace (`NoSuchSubspace`), empty real subspace (`EmptySubspace`), depth-incompatible span (`DepthIncompatible`, WF_V(v): explicit `#start != 2` check), and a depth-2 span that overruns the bound prefix (`RangeNotPresent`, WF_V(vi): the depth-agnostic `resolved < ordinal(width)` test), never clamp. (WF_V(iii,v,vi)/O13 0077.)
- *SHOWDELETIONS cross-document combine* — `arranged_content(d_X)` filtered by `deletions(d_Y).denotes(·)`, both halves off one snapshot. (DeletedFromAWithB/BWithA 0075.)
- *Completeness under fan-out; deterministic canonical order* — cross-product `interval_join` + `canonicalize`. (X8/R1/R2/R3 0122; X11 maximal / R4 not required.)
- *Present-tense soundness filter* — `project`-narrowing of `docs_containing`. (FD-SOUND 0124.)

**Delegated (M6 relies on, does not enforce):** contiguity D-CTG★ (the dense-occupancy reliance — a theorem of ASN-0113 W4 — stated once under *Core data model*); **run canonicality** — M5's POOM block decomposition is the unique maximal-run form (ASN-0058 split/merge/canonicalize), which makes `resolve`'s run splits, and with them COMPARE's finer-than-maximal report granularity, a pure function of the arrangement restriction (X12 R3's "no hidden input"), never of edit history — a future M5 relaxation would silently make COMPARE's *listed* pairs history-dependent; and referential integrity S3★ (M5 write path); R permanence/monotonicity, the J-couplings, the **level-class discipline on every coverage set-op**, the R⁻¹ index `docs_containing`, and the per-document `deletions`/`content_runs` covers from which M6 composes the cross-document SHOWDELETIONS combine (M5); durability/recovery (M2). M6 trusts these and panics (not silently skips) if S3★ or S3★-aux is observed broken on the read path — a content position with no stored value (RETRIEVEV's `expect`) or an active position outside both subspaces (RETRIEVEV's `unreachable!` arm) — one policy in all build profiles. Every primitive M6 calls is in M1–M5's interface as given — no upstream amendment is required.

## Dependencies & seams

**Upstream calls (concrete):**
- **M1** — `document_of` (origin projection, SHOWORIGIN_V; I-address → origin Document in `run_addr`); `shift`/`shift_ordinal`+`ElemPos`/`elem_addr` (run-address enumeration, V-cursor advance, COMPARE `reach_i`); `from_endpoints`/`Span::new` (extent synthesis); `action_point`/`zeros`/`ordinal`/`Tumbler::get`/`Tumbler::new`/`is_level_uniform`/`element_field` (gates, the depth-agnostic count read, the `run_addr` element-field tripwire, COMPARE ordinal arithmetic); `union`/`SpanSet::singleton`/`SpanSet::empty`/`SpanSet::is_normalized`/`SpanSet::denotes`/`SpanSet` `PartialEq` and tumbler `Ord` (set algebra, COMPARE overlaps, the FINDDOCSCONTAINING filter test, the **SHOWDELETIONS membership test**, dedup ordering, normal-form assert). The FINDDOCSCONTAINING `!= SpanSet::empty()` test leans on M1's *no-zero-width-member* span-set boundary (denotation-empty ⇒ structurally `empty()`). **One ask rides this seam** (M6's third upstream ask, beside the two on M5 below): that M1 surface a denotational, `denotes`-free **`SpanSet::is_empty()`** (zero members ⇔ empty denotation, which no-zero-width-member already forces), so the FINDDOCSCONTAINING emptiness test can stop leaning on the structural-`PartialEq` argument; until then `!= SpanSet::empty()` stands on the named invariant.
- **M2** — `snapshot()` (one per logical query; M10 takes it), `Snapshot::world()`/`seq()`. No `transact`, no `Kernel` — M6 never writes.
- **M3** — `is_registered_document` (the universal allocation gate). Not `effective_owner` (authorization is M10's; SHOWORIGIN reports origin *documents*, not owners).
- **M4** — `value_at` (RETRIEVEV content only). `contains` available as a defensive S3★ check but not needed (M5 guarantees it). Never touched by COMPARE/extent/containment/deletions.
- **M5** — the workhorse: `resolve` (RETRIEVEV, SHOWORIGIN_V, COMPARE), `resolve_coverage` (FINDDOCSCONTAINING phase 1), `content_count`/`link_count` (extent queries, SHOWORIGIN_V subspace gate), `point` (COMPARE's per-run debug-assert of the V-reconstruction lemma), `project` (FINDDOCSCONTAINING present-tense filter), `docs_containing` (FINDDOCSCONTAINING phase 2), `content_runs` + `deletions` (SHOWDELETIONS: enumerate `content_image` and membership-test the per-document deleted cover; `ever_placed` is the defensive exactness-independent cross-check). M6's public `CompareReport`/`CorrPair` also carry M5's `VPos`, re-exported (`pub use m5::VPos;`) so M10 marshals it through M6's surface. All of these are in M5's interface **as given** — no amendment; **two documentation asks ride this seam** (M6's third ask — the denotational `SpanSet::is_empty` — rides the M1 bullet above): (a) that M5 surface **D-CTG★** as a named interface invariant (the dense-slice occupancy ASN-0113 W4 proves), since COMPARE's `u1`/`u2` soundness rests on it; (b) that M5 state explicitly that **`resolve` serves link-subspace V-spans** — its defensive conditions name no subspace (unlike `project`, which is explicitly content-only), and M6 leans on that reading: RETRIEVEV's `DeliveryItem::Ref` items and SHOWORIGIN_V's `s_L` arity are correct only if a link-subspace depth-2 span resolves to its runs; a content-only `resolve` would silently violate R3 exactness for link specs.

**Downstream seam (what M6 exposes — only M10 consumes it):** the seven read methods on `Query<'s, W>`. The contract M10 codes against: take a snapshot, build a `Query`, call the op, **marshal the returned value** (per the derive policy stated in *Public interface*: serde-derived except `CorrPair`/`CompareReport`, which M10 destructures field-by-field), **and surface any `Err(_)` as a typed rejection** (these are precondition/well-formedness failures, never silent skips); a registered-empty document yields the operation's empty form (`⟨⟩`/empty `Delivery`/empty halves/`[]`), an unallocated one yields the op's `DocNotRegistered(Address)` error (uniform payload across all seven error enums). M6 returns by value and never commits, so there is no commit-before-acknowledge step for reads. All seven operations ship against the upstream interfaces as given; M10's reader surface carries no SHOWORIGIN-over-I (it cannot — M6 exposes only the V-arity), so the V-arity-only origin path is settled (Conflicts resolved 2).

**Engine assembly:** M6 contributes **no slice, no record variant, no accessor trait, no fold** — it is a pure consumer of `HasM3 + HasContent + HasM5`. Nothing in the engine's `World`/`Record` comes from M6, and no `apply`/`rebuild_derived` obligation attaches to it. (It therefore trivially satisfies the composition contract by being generic over `W` and naming no concrete `World`/`Record`.)

## Conflicts resolved

1. **Where the R index and coverage set-ops live; how the SHOWDELETIONS combine is built.** The decomposition lists M6 as owning the "reverse-index hint over R" and "deletion classification (SHOWDELETIONS)." M5's *as-built interface* exposes `docs_containing`, `deletions`, and `ever_placed` as **M5 methods**, co-locating the R index with R's authoritative state (Lampson: a hint belongs with the store that recomputes it on replay — only M5 folds R). **Resolution:** M6 owns **no index and no coverage set-op**. FINDDOCSCONTAINING contributes only the phase-1 resolve-union and the present-tense `project` filter over M5's `docs_containing` superset. SHOWDELETIONS's cross-document `DELETED(·,d_A) ∧ CURRENT(·,d_B)` is a **pure per-query read** M6 composes from M5's *per-document* primitives — `content_runs(d_B)` enumerates CURRENT(·,d_B), and `deletions(d_A).denotes(a)` (with M1's `denotes`) tests DELETED(·,d_A) by **membership**, not set intersection. This sidesteps the two dead ends the design must reject: the SpanSet-*intersection* route faults (`intersect_sets`/`normalize` choke on mixed-length covers), and the in-M6-*authoritative-state* route is misplaced (stateless M6 cannot recover a fold). Membership-testing needs neither — `denotes` faults on nothing and is exact by `difference_sets`' denotational contract (`⟦deletions(d)⟧ = {x : DELETED(x,d)}` exactly; see the SHOWDELETIONS section) — so the combine lives where the decomposition puts it (M6), on the seam M5 already advertises (`deletions`: "SHOWDELETIONS primitive… **M6 reads it straight off**"). **No M5 amendment is required; all seven operations build against the interfaces as given.**

2. **SHOWORIGIN_I de-scoped — a settled decomposition amendment.** `origins_I(σ) = {document_of(a) : a ∈ ⟦σ⟧ ∩ dom(C)}` needs an *enumeration of allocated content addresses across an I-interval*. M4 is point-only with `Ord` **deliberately** unused (its boundary forbids range/prefix/ordered scans) and M3 is point-only (`is_allocated`); neither exposes — and M4 by its stated design *excludes* — the I-ordered index this arity requires. Adding such a scan to M4 would itself be an upstream-overreach defect, and stateless M6 (no slice, no fold hook) cannot grow its own index. **Resolution:** M6 ships `show_origin_v` only. The I-arity is **de-scoped to a recorded decomposition amendment** — it belongs to a *new* I-ordered content index (a recomputable hint over M4's append-only writes, e.g. `allocated_content_in(span)`), a change to the module decomposition, not an M6 internal. Two caveats made explicit: (i) ASN-0077 designates *neither* arity "reader-facing" — preferring the V-arity is **M6's ruling**, not the note's; (ii) the de-scope is **settled by construction** — M10 can marshal only what M6's `Query` exposes (`show_origin_v` alone), so no I-arity surface exists for the FEBE layer to reach. (M10's enumerated reader sources omit ASN-0077 and ASN-0075 *entirely*, so their silence on a SHOWORIGIN-over-I command corroborates this only **vacuously** — the by-construction argument carries it; and that omission of 0077/0075, the two readers M6 actually ships, is an **M10-side reconciliation item, not an M6 defect**.) The amendment is future work, not a live capability hole. The prior `show_origin_i`/`ISpanIndexUnavailable` placeholders are removed.

3. **`m_S(d)` depth hint collapses to a constant.** ASN-0115/0112/0113 all weigh caching vs. recomputing the per-subspace common depth `m_S(d)`. **Resolution:** M5 fixes V-positions at depth 2, so `m_S(d) ≡ 2`; the depth-compatibility test is the static `#start == 2`, enforced by M5's defensive `resolve` (which returns ⟨⟩ for any non-depth-2 span). `gate_vspec` does **not** fold depth-compatibility into well-formedness — it admits any well-formed `#start ≥ 2` start and lets a depth-incompatible (`#start ≥ 3`) span resolve to ⟨⟩ (ASN-0115: depth-compatibility is consulting-state, not a well-formedness condition; see *Conflicts resolved* 8 and the gate revision). No hint, no per-document scalar.

4. **RETRIEVEDOCVSPAN: count-read vs. confluent summary, and the negative-origin hazard (0112 OQ5).** The note offers a min/max read or a maintained summary tree whose relative displacement can drive the **origin negative** (violating S8a). **Resolution:** M6 synthesizes from M5's authoritative `content_count`/`link_count`, reading `min` as the subspace anchor `[s,1]` — never negative. The hazard is exclusive to the summary-tree path and is designed out. (This also resolves "trust counts vs. scan": trust M5's counts; D-CTG★ is the dense-slice occupancy ASN-0113 W4 proves; debug-assert optionally.)

5. **Byte-clipping / run-coalescing / width≠count (0115).** The digest's elaborate boundary-clipping presumes a byte-granular store. **Resolution:** M4 stores opaque `Val`s keyed per address and M5's arrangement is per-address, so M6 delivers **one item per active V-position** — exact, no dedup, no byte clip. "Never coalesce across a gap" is satisfied trivially by per-position delivery (and remains safe if a builder chooses segment/streaming delivery, since M5's runs are gap-aligned). Byte-boundary semantics are a property of how content was chunked into `Val`s *below* M6.

6. **0112 vs. 0113 overlap.** Both are "document extent." **Resolution:** complementary, not conflicting — they share the same count-read core; `doc_vspan` is the whole-document bounding span (a bounding box across subspaces), `doc_vspanset` is the per-subspace exact span-set. Fragmentation-sensitive callers use the latter; M10 routes accordingly.

7. **SHOWORIGIN vs. FINDDOCSCONTAINING (a distinction to *preserve*, not a conflict).** SHOWORIGIN reports the **original allocator** (`document_of`), FINDDOCSCONTAINING the **current holders** (R⁻¹ filtered to present). Different questions; M6 keeps them on different machinery (M1 projection vs. M5's R index + filter) so neither is mistaken for the other.

8. **`gate_vspec`'s ordinal-level requirement is a deliberate domain-narrowing surfaced as a typed rejection; depth-compatibility is *not* gated.** ASN-0077 WF_V(iv) requires only `actionPoint(ℓ) ≤ #u`, and ASN-0122 X12 requires only T12-well-formedness + a content-subspace start — *not* strict ordinal-level. M6 nonetheless gates all four resolve-based ops (RETRIEVEV, SHOWORIGIN_V, COMPARE, FINDDOCSCONTAINING) to **ordinal-level, level-uniform** spans. **Resolution:** for RETRIEVEV this is exactly ASN-0115 VSpec well-formedness (which *does* require ordinal-level + level-uniform), so rejecting is faithful by the note's own definition. For SHOWORIGIN_V, COMPARE, and FINDDOCSCONTAINING it is a genuine **domain-narrowing**, and the honest framing is that M6 accepts a *strictly smaller* domain than these notes specify: X12 (T12-well-formed + content-subspace start) and WF_V(iv) admit non-ordinal-level spans that M6 rejects. Rejection is **not forced** — a non-ordinal-level content span like `([s_C,3],[w₁,w₂])` denotes exactly the content positions `{[s_C,k] : k ≥ 3}`, which M6 *could* (after reading `content_count`) normalize to the ordinal-level `([s_C,3],[0, n_C−2])` and then resolve faithfully. M6 deliberately **chooses not to build that normalization machinery**: supporting the wider T12 domain would mean a per-span count-read-and-renormalize step before every resolve, and the simpler contract is "ordinal-level only." The narrowing is honest — and a builder is not misled — because it is **surfaced as a typed rejection** (`MalformedSpec`/`MalformedSpan`), never a silent under-resolution: M5's only resolution primitives, `resolve`/`resolve_coverage`, **force-empty** a non-ordinal-level span, so the *alternative* (accept-and-push-through) would silently drop the span's real contribution and return an **under-complete** answer (violating COMPARE **R2-completeness** / FINDDOCSCONTAINING **FD-COMPLETE**, and the analogous origin-set completeness for SHOWORIGIN_V). The gate therefore converts M5's silent upstream empty into an explicit rejection — the *behavior* is sound either way, and the rejection is the one that does not lie about the answer. (The narrowing does cost reach: an **open-ended** selection like "content position 3 to the end" is naturally a non-ordinal-level span and needs the count to express as ordinal-level, so a caller wanting it must read `content_count` itself and submit `([s_C,3],[0,n_C−2])`. The *closed* selections these notes exhibit are already ordinal-level in the `m_S ≡ 2` model, so they survive the gate unchanged.) **What `gate_vspec` does *not* do is gate the depth:** it admits any well-formed `#start ≥ 2` start and lets a depth-incompatible (`#start ≥ 3`) span pass to M5's `resolve`, which force-empties it. The distinction from the non-ordinal-level case is *what the contract says the answer should be*: a depth-incompatible span is **contractually empty** — ASN-0115 R6 mandates a depth-incompatible spec yield `act = ∅` *without failure*, and X12 reports a depth-incompatible content span's empty region as success — so force-emptying it is the *correct, complete* answer, whereas a non-ordinal-level span has real results M5 cannot produce (without the normalization M6 declines to build). Gating depth-2 *as well-formedness* would be an over-reach — ASN-0115 is explicit that depth-compatibility is a consulting-state predicate, **not** a well-formedness condition. So depth-incompatibility stays a silent ⟨⟩ (RETRIEVEV R6 / COMPARE empty region), surfacing as a typed rejection only where the operation's *own* precondition demands the common depth — SHOWORIGIN_V's WF_V(v), discharged via its dedicated `DepthIncompatible` error. Recorded here as the deliberate split: ordinal-level/level-uniform gated (a domain-narrowing, surfaced as a typed rejection); depth-compatibility *not* gated (consulting-state).

## Open build decisions

- **COMPARE matcher structure** *(the one canonical statement — the `interval_join` comment and the fan-out bullet defer here)*. v1's **reference implementation** is the exhaustive O(|P|·|Q|) double-loop block join, shipped as `interval_join`. **Sort-by-`i_start` + sweep** (or an interval tree) is a drop-in *optimization of the same join* — same pair multiset — to adopt when profiles demand it (an optimization path, not the shipped form). The **independent test oracle** is a per-position hash join on address (obviously fan-out-complete), used to validate whichever join ships. One vocabulary throughout: "reference implementation" = the shipped double loop; "optimization" = sweep/interval tree; "oracle" = the hash join, and only the hash join.
- **COMPARE maximal output.** Ship `fold_adjacent` as the identity (per-overlap, finer-than-maximal — fully conforming, R4 not required) vs. the feet-successor-adjacency merge for literal X11 maximal pairs. Default to identity; add the merge only if a consumer demands maximal form (it changes presentation, never `⟦Γ⟧`).
- **RETRIEVEV delivery shape.** Per-position items (chosen default — exact, simplest) vs. coalesced gap-aligned segments vs. lazy streaming for large spec-sets. If streaming, decide how back-pressure interacts with partial-delivery (a stream still "succeeds" while emitting nothing for gaps), and whether `DeliveryItem::Content` borrows through the snapshot (zero-copy) instead of cloning the `Arc`.
- **Snapshot ownership.** M6 methods take `&Snapshot` so M10 controls the consistency scope (recommended); a convenience that snapshots per call is possible but couples M6 to `&Kernel`.
- **Extent contiguity check.** Trust `content_count`/`link_count` (O(1)) vs. debug-build cross-check against `content_runs` (catches a broken D-CTG★ from upstream). Trust in release, assert in debug.
- **SHOWDELETIONS exactness source.** Use `deletions(d).denotes(·)` (the default and the only path the design depends on — M5's stated fault-free, read-straight-off seam; exact *unconditionally* by `difference_sets`' denotational contract, §SHOWDELETIONS). The exactness-independent `ever_placed(d).denotes(·) ∧ a ∉ arranged_content(d)` form is retained only as a **defensive test cross-check**, not a fallback the design leans on — the denotational argument leaves no coalescing hazard to guard against, so there is nothing for it to recover.
- **SHOWDELETIONS D-DISJ short-circuit.** M6-local: skip enumerating one document's `arranged_content` when the other's `deletions` cover is empty (its half is then empty) — a cheap guard in the spirit of D-DISJ's R-disjointness. Optional; default computes both halves directly.
- **COMPARE link-start spans.** Reject loudly (recommended — `NotContentSubspace`) vs. leniently strip via a content-subspace front-filter. (Spans that merely *denote* link positions from a content start are always legal — `resolve` clips them — so this is only about a span whose *start* is in the link subspace.)
- **COMPARE overlapping-region dedup.** Leave overlapping/repeated windows within an operand to collapse denotationally (default — conforming, deterministic via the stable sort) vs. pre-dedupe each operand's regions to shrink the cross-product. Perf-only; pick per profile.
- **Result caching.** Recompute by default (cheap, local, lock-free). If COMPARE/SHOWDELETIONS profile hot, memoize as a *hint* keyed on `(Snapshot::seq, args)` — and for any RETRIEVEV delivery cache, key on the consulted *restriction* (`M(d)|⟦σ⟧`), never on output byte-identity (R7 is sufficiency, not biconditional). Never authoritative; always recompute on a miss.
- **FINDDOCSCONTAINING resolve timing.** Re-resolve per query (tracks present-tense drift) vs. cache the frozen resolved I-coverage at an earlier snapshot for stable "find more like this" (legitimate because content is permanently grounded). Different products want different answers; expose the choice at M10.
