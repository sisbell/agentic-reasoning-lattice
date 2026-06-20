# M6 — Content Retrieval & Query — Detailed Design

## Purpose & boundary

M6 is the system's **read-only observer surface over documents**. It owns the seven content/provenance queries — RETRIEVEV, RETRIEVEDOCVSPAN, RETRIEVEDOCVSPANSET, SHOWORIGIN (V-arity), SHOWDELETIONS, COMPARE, FINDDOCSCONTAINING — and turns the authoritative state held below it (M3's registry, M4's content, M5's arrangements and provenance relation R) into delivered values, extents, origins, deletion sets, correspondence reports, and containment answers. Every operation is a **pure function of one consistent M2 snapshot**: it resolves through M5's arrangements, fetches bytes from M4, projects origin via M1, reads R through M5, and gates on M3's registry — and writes nothing, ever.

**One thing well:** *observe documents over a single pinned snapshot — resolve, fetch, project, classify, compose — never mutate.*

It does **not** own: any authoritative or derived-authoritative state (none — it has no `WorldState` slice, no journal record, no fold); the R relation, its reverse index, or the cross-document deletion comparison (these belong in M5, co-located with R — `docs_containing` is M5's today; the SHOWDELETIONS combiner is **demanded** of M5 as `cross_deletions`, an amendment M5's interface does not yet provide); content bytes (M4); arrangements (M5); link-side discovery (M8); the request lifecycle, dispatch, and marshaling (M10). It also does **not** deliver SHOWORIGIN's *I-span* arity: that arity needs an I-ordered enumeration of `dom(C)` over an interval, which M4's point-only interface (with `Ord` deliberately unused, range/prefix scans forbidden) and M3's point-only registry deliberately exclude; the I-arity is therefore **de-scoped from M6 and recorded as a decomposition amendment** (a new I-ordered content index over M4's append-only writes — see *Conflicts resolved* 2), pending a builder's confirmation that M10's FEBE surface promises clients no SHOWORIGIN-over-I. M6 delivers SHOWORIGIN's V-arity (preferring it is **M6's ruling** — ASN-0077 designates neither arity reader-facing).

**Build status:** six of the seven operations compile against M1–M5 *as given*. **SHOWDELETIONS is blocked on a required M5 amendment** (`cross_deletions`, signature and output contract pinned in its section): the cross-document deletion combine is unbuildable from M5's published `deletions`/`ever_placed` surface (opaque, possibly mixed-length `SpanSet`s; M1 offers no SpanSet enumeration; `intersect_sets`/`normalize` fault on mixed-length input), and must be added beside R. M6's own design is complete; that one seam is a cross-module change M5's design must adopt.

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

### Shared request types

```rust
/// One document + one ordinal-level depth-2 V-span. A spec-set is `&[Spec]`. Used by RETRIEVEV
/// (content OR link) and COMPARE (content only).
pub struct Spec  { pub doc: Address, pub span: Span }
/// One document + a finite V-region (set of spans). FINDDOCSCONTAINING (FD-CONVEX wants multi-span).
pub struct Region { pub doc: Address, pub spans: Vec<Span> }
```

### A. Content delivery

```rust
pub enum DeliveryItem { Content(Val), Ref(Address) }   // content position ⇒ value; link position ⇒ address-as-reference
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
    /// Deduplicated origin documents, in tumbler order. Inadmissible (Err) on an empty/unallocated
    /// document or when the span's positions are not all currently bound (WF_V (iii)/(vi); O13) —
    /// reject, never silently clamp.
    pub fn show_origin_v(&self, doc: &Address, span: &Span) -> Result<Vec<Address>, OriginError>;
}
```

### D. Provenance comparison

```rust
pub struct Deletions { pub a_with_b: SpanSet, pub b_with_a: SpanSet }  // I-coverage of deleted-from-one ∧ current-in-other

pub struct CorrPair { pub d1: Address, pub u1: VPos, pub d2: Address, pub u2: VPos, pub width: Nat }
pub struct CompareReport(pub Vec<CorrPair>);   // canonical order; slot i drawn from operand i

impl<'s, W: M6World> Query<'s, W> {
    /// SHOWDELETIONS (ASN-0075). Both documents must be registered (Err otherwise; allocated-empty is
    /// fine and yields empty halves). Output is I-address coverage, not values. BLOCKED on a required
    /// M5 amendment: the cross-document comparison is M5's `cross_deletions` (not in M5's interface as
    /// given); M6 gates and wraps. See the SHOWDELETIONS section.
    pub fn show_deletions(&self, d_a: &Address, d_b: &Address) -> Result<Deletions, DeletionsError>;

    /// COMPARE / SHOWRELATIONOF2VERSIONS (ASN-0122). Content-subspace spec-sets; reports address-equal
    /// correspondences (NEVER opens M4). Complete under fan-out, deterministic canonical order.
    pub fn compare(&self, rho1: &[Spec], rho2: &[Spec]) -> Result<CompareReport, CompareError>;
}
```

### E. Document containment

```rust
impl<'s, W: M6World> Query<'s, W> {
    /// FINDDOCSCONTAINING (ASN-0124). Every named document must be registered (Err otherwise;
    /// allocated-empty contributes nothing). Returns the PRESENT-TENSE containers (filtered), tumbler-
    /// ordered, deduplicated — bare identities, no positions, no counts.
    pub fn find_docs_containing(&self, regions: &[Region]) -> Result<Vec<Address>, FindError>;
}
```

### Errors (all typed; M10 surfaces verbatim — never a silent skip)

```rust
pub enum SpecFault { NotOrdinalLevel, NotLevelUniform, StartNotZeroFree, StartTooShallow }
pub enum RetrieveError  { DocNotRegistered(Address), MalformedSpec { index: usize, fault: SpecFault } }
pub enum ExtentError    { DocNotRegistered }
pub enum OriginError    { DocNotRegistered, EmptySubspace, RangeNotPresent, MalformedSpan(SpecFault) }
pub enum DeletionsError { DocNotRegistered(Address) }
pub enum CompareError   { DocNotRegistered(Address), NotContentSubspace, MalformedSpan { index: usize, fault: SpecFault } }
pub enum FindError      { DocNotRegistered(Address) }
```

## Core data model

M6 owns **no persistent and no derived-authoritative state**. It declares no `WorldState` slice, no journal `Record` variant, no `apply`/`rebuild_derived` fold — it is not a store, and it does not appear in the engine's `World`/`Record`. Its "data model" is three things:

1. **The borrowed snapshot.** A `Query` holds one `&Snapshot<W>` and reads `s.world().m3()`, `s.world().content()`, `s.world().m5()` off it. M5/M4/M3's slices are `im`-backed (structurally shared, persistent), so the snapshot is an O(1), lock-free, immutable value; reading every constituent of one query off the *same* `&Snapshot` is what makes its `(M, R)` view consistent by construction (it is the discharge of M2's clause-6, ASN-0075/0122/0124 single-Σ requirement). M6 holds the borrow only for the query's duration.

2. **Result value types** (above) — `Delivery`, `SpanSet`, `Vec<Address>`, `Deletions`, `CompareReport`. All in-memory, returned by value. `DeliveryItem::Content(Val)` carries an `Arc<[u8]>` clone (an Arc bump, not a byte copy), so delivery is cheap even for large content.

3. **Transient per-query working structures**, all dropped at return:
   - COMPARE's `Block { doc: Address, v_start: Tumbler, i_start: Address, width: Nat }` lists for P and Q, plus the intermediate `Vec<CorrPair>` before canonicalization.
   - Dedup sets for origins/containers (`HashSet<Tumbler>` → sorted `Vec<Address>`, since `Address` is `Eq+Hash` but not `Ord`; `Tumbler` carries the `Ord`).

**Authoritative vs. recomputable, resolved explicitly for M6:** there is nothing to distinguish, because M6 holds neither. Three would-be hints all resolve away from M6:
- the **R reverse index** (`docs_containing`, FINDDOCSCONTAINING) and the **cross-document deletion comparison** (SHOWDELETIONS) belong in M5, co-located with R's authoritative state (recomputable by replay only where R is folded) — `docs_containing` exists today; the deletion combiner is the demanded `cross_deletions` amendment;
- the **per-subspace common depth `m_S(d)`** that the source notes fret over (cache vs. recompute) is the **constant 2** — M5 fixes V-positions at depth 2, so `m_S(d) ≡ 2` and the depth-compatibility test is the static `#start == 2`;
- the **I-ordered content index** that SHOWORIGIN's de-scoped I-arity would need is **not placed here** at all (it would belong to M4 or a dedicated index; the I-arity is de-scoped — *Conflicts resolved* 2).

## Internal design

Every operation begins by reading its slices off the single bound snapshot, runs its gate (typed rejection), then composes upstream primitives. Shared helpers:

```rust
fn require_registered(m3: &M3State, d: &Address) -> bool { m3.is_registered_document(d) }

fn s_c() -> Nat { Nat::from(1u8) }   // content subspace (s_C = 1, ASN-0047) — Nat = BigUint, so a fn, not a const
fn s_l() -> Nat { Nat::from(2u8) }   // link subspace    (s_L = 2)

fn gate_vspec(span: &Span) -> Result<(), SpecFault> {
    if !span.is_level_uniform()                               { return Err(SpecFault::NotLevelUniform); }   // #start == #width
    if action_point(span.width()) != Some(span.width().len()) { return Err(SpecFault::NotOrdinalLevel); }   // width acts at deepest
    if zeros(span.start()) != 0                               { return Err(SpecFault::StartNotZeroFree); }  // ⇒ all components > 0
    if span.start().len() < 2                                 { return Err(SpecFault::StartTooShallow); }
    Ok(())
}

/// k-th address of a run. i_start is element-level (zeros=3, field [subspace, ordinal]) by M5 invariant,
/// so advancing the ordinal via ElemPos avoids the raw-shift subspace-crossing footgun.
fn run_addr(i_start: &Address, k: &Nat) -> Address {
    let p = ElemPos { doc: document_of(i_start).unwrap(), subspace: i_start.subspace().unwrap(),
                      ordinal: ordinal(i_start.tumbler()).clone() };
    elem_addr(&shift_ordinal(&p, k)).unwrap()
}

fn dedup_docs(it: impl Iterator<Item = Address>) -> Vec<Address> { /* HashSet<Tumbler> → sort by Tumbler */ }
```

### RETRIEVEV — resolve, then dereference, in order

Two phases, kept separate (the load-bearing factoring of ASN-0115): resolve V-spans to I-addresses (M5), then fetch values (M4 for content) or pass the address through (links).

```rust
pub fn retrieve_v(&self, specs: &[Spec]) -> Result<Delivery, RetrieveError> {
    let (m3, m5, c) = (self.0.world().m3(), self.0.world().m5(), self.0.world().content());
    // Gate the whole request first — well-formedness is the only in-model failure (ASN-0115).
    for (i, s) in specs.iter().enumerate() {
        if !require_registered(m3, &s.doc) { return Err(RetrieveError::DocNotRegistered(s.doc.clone())); }
        gate_vspec(&s.span).map_err(|f| RetrieveError::MalformedSpec { index: i, fault: f })?;
    }
    let mut out = Vec::new();
    for s in specs {                                   // concatenate per spec, IN ORDER (R5) — no global sort
        let sub = s.span.start().get(1).clone();       // 1=content, 2=link (gate_vspec ⇒ #start≥2, zero-free)
        for run in m5.resolve(&s.doc, &s.span) {       // V-ordered, clipped, gap-aligned; #start≠2 ⇒ ⟨⟩ (depth-incompat)
            let mut k = Nat::zero();
            while &k < &run.width {                     // per active position, ascending V (R3) — no dedup (R8)
                let a = run_addr(&run.i_start, &k);
                if sub == s_c() {
                    out.push(DeliveryItem::Content(
                        c.value_at(a.tumbler()).expect("S3★: content position ⇒ a∈dom(C)").clone()));
                } else if sub == s_l() {
                    out.push(DeliveryItem::Ref(a));     // link reference IS the address — never reads M4
                } else {
                    // UNREACHABLE for an ACTIVE position: S3★-aux confines every bound V-position to
                    // subspace ∈ {s_C, s_L}, and `resolve` yields NO runs for any other start subspace
                    // (M5 holds only content/link positions), so this branch never executes when a run
                    // exists. Documented silent-drop intent, not an oversight.
                    debug_assert!(false, "active V-position must be content or link subspace (S3★-aux)");
                }
                k += 1u8;
            }
        }
    }
    Ok(Delivery(out))                                   // empty spec-set ⇒ Ok(Delivery(vec![]))
}
```

- **Common case:** a single content spec over a contiguous run — one M5 range scan, *w* M4 point lookups (one `Val` per address, each an `Arc` clone). Links never touch M4.
- **Gaps / depth-incompat / foreign subspaces** all funnel through M5's defensive `resolve` returning fewer-or-zero runs → silent empty contribution; the request still succeeds (R6). The `m_S ≡ 2` simplification means depth-incompatibility *is* `#start ≠ 2`, which `resolve` already force-empties. A start subspace ∉ {1,2} is likewise force-empted upstream (M5 holds no such positions), so the closed `else` arm is unreachable while a run exists — its `debug_assert` records that as intent.
- **Tradeoff:** I deliver **one item per active V-position** (one `Val` or one `Ref`), not coalesced segments. This is the exact, no-dedup form (R3/R8) and sidesteps byte-clipping entirely — at M4's granularity each address holds one opaque `Val`, so there is no intra-position byte boundary for M6 to realize. Streamed/segmented delivery is an open decision; M5's runs are already gap-aligned, so a segment form would also be safe.
- The `expect` trusts S3★ (M5's content-side referential integrity); a `None` there means upstream corruption, and panicking is the correct read-path response (silently skipping would violate exactness).

### RETRIEVEDOCVSPAN & RETRIEVEDOCVSPANSET — synthesize from counts

Both read `content_count`/`link_count` (M5 O(1) hints) and synthesize spans. Occupied positions are the dense runs `[s_C, 1..n_C]` and `[s_L, 1..n_L]` (D-CTG★, M5's write-path invariant), so the counts *are* the extents and no scan is needed.

```rust
pub fn doc_vspan(&self, doc: &Address) -> Result<SpanSet, ExtentError> {
    let (m3, m5) = (self.0.world().m3(), self.0.world().m5());
    if !require_registered(m3, doc) { return Err(ExtentError::DocNotRegistered); }   // unallocated ⇒ fail
    let (nc, nl) = (m5.content_count(doc), m5.link_count(doc));
    if nc.is_zero() && nl.is_zero() { return Ok(SpanSet::empty()); }                 // registered-empty ⇒ ⟨⟩
    let min = vpos(if !nc.is_zero() { s_c() } else { s_l() }, &Nat::one());          // min O(d): anchor of lowest occupied subspace
    let max = vpos(if !nl.is_zero() { s_l() } else { s_c() }, if !nl.is_zero() { &nl } else { &nc });
    let reach = shift(&max, &Nat::one());                                            // one ordinal step past max
    Ok(SpanSet::singleton(Span::from_endpoints(min, reach).unwrap()))                // origin=min; width=reach⊖min
}

pub fn doc_vspanset(&self, doc: &Address) -> Result<SpanSet, ExtentError> {
    let (m3, m5) = (self.0.world().m3(), self.0.world().m5());
    if !require_registered(m3, doc) { return Err(ExtentError::DocNotRegistered); }
    let (nc, nl) = (m5.content_count(doc), m5.link_count(doc));
    let mut result = SpanSet::empty();
    if !nc.is_zero() { result = union(&result, &SpanSet::singleton(ext_span(s_c(), &nc))); }  // ext(d,s_C) = ([1,1],[0,n_C])
    if !nl.is_zero() { result = union(&result, &SpanSet::singleton(ext_span(s_l(), &nl))); }  // ext(d,s_L) = ([2,1],[0,n_L])
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
- **Tradeoff:** trusting `content_count`/`link_count` rests on D-CTG★, which is M5's write-path obligation, not M6's. A debug-build cross-check (`Σ content_runs(d).width == content_count(d)` and first run anchored at `[s_C,1]`) is cheap defense-in-depth (open decision).

### SHOWORIGIN_V — block-decompose, project one origin per run

Origin is the pure address projection `document_of` (M1). Block uniformity (O2) means all addresses in one run share an origin, so M6 projects **one address per run** — O(runs), not O(positions).

```rust
pub fn show_origin_v(&self, doc: &Address, span: &Span) -> Result<Vec<Address>, OriginError> {
    let (m3, m5) = (self.0.world().m3(), self.0.world().m5());
    if !require_registered(m3, doc)        { return Err(OriginError::DocNotRegistered); }   // WF_V (i)
    gate_vspec(span).map_err(OriginError::MalformedSpan)?;                                  // (ii),(iv),(v): depth-2, ordinal-level
    let sub = span.start().get(1);
    let n_s = if *sub == s_c() { m5.content_count(doc) }
              else if *sub == s_l() { m5.link_count(doc) } else { Nat::zero() };
    if n_s.is_zero() { return Err(OriginError::EmptySubspace); }                            // (iii) inadmissible on empty subspace
    let runs = m5.resolve(doc, span);
    let resolved: Nat = runs.iter().map(|r| &r.width).sum();
    if &resolved < ordinal(span.width()) { return Err(OriginError::RangeNotPresent); }      // (vi) some position unbound — reject (O13)
    Ok(dedup_docs(runs.iter().map(|r| document_of(&r.i_start).unwrap())))                   // link case ⇒ {doc} by CL-OWN
}
```

- The `(iii)`/`(vi)` checks are the deliberate strictness: SHOWORIGIN_V is **inadmissible on an empty document and on a span overrunning the bound prefix** — reject-and-signal, never clamp to the surviving sub-span (the digest's explicit choice, O13).
- **The nominal count is read depth-agnostically** via `ordinal(span.width())` (the last component), *not* a hard-coded `width.get(2)`: `gate_vspec` admits `#start ≥ 2`, so a (degenerate) deeper span no longer slips the gate and then mis-reads a `0` at index 2 — it is rejected correctly. Non-load-bearing in the depth-2 model, but it removes the latent gate/count-read inconsistency.
- For the link subspace, `document_of(link)` is the home `doc` (CL-OWN) — handled uniformly, no special case.

### SHOWORIGIN_I — de-scoped (ruling)

`origins_I(σ) = {document_of(a) : a ∈ ⟦σ⟧ ∩ dom(C)}` requires enumerating allocated content addresses across an I-interval. No upstream surface provides this: M4 is point-only with `Ord` **deliberately** unused and its boundary forbidding range/prefix scans, and M3's registry is point-only (`is_allocated`). Stateless M6 has no fold hook to grow its own index. The I-arity is therefore **de-scoped from M6 and recorded as a decomposition amendment** — were it ever needed, it belongs to a *new* I-ordered content index (a recomputable hint over M4's append-only writes, e.g. `allocated_content_in(span)`), which is a change to the module decomposition, not an M6 internal. Only `show_origin_v` ships, and `OriginError` carries no `ISpanIndexUnavailable` placeholder; the prior `show_origin_i` placeholder is removed.

Two flags travel with the ruling so it does not silently diverge from the system docs:
- **Preferring the V-arity is M6's call, not ASN-0077's.** The note designates *neither* arity "reader-facing"; M6 rules the V-arity the one it ships.
- **The de-scope is sound only if M10 promises clients no SHOWORIGIN-over-I.** M10 sources ASN-0077; a builder **must confirm** M10's FEBE command surface exposes only the V-arity. If M10 does promise the I-arity to external clients, this de-scope is no longer an internal ruling but a genuine capability hole — a **DEFECT** that escalates to the decomposition (it forces the new I-ordered index above), not something M6 can absorb.

### SHOWDELETIONS — gate, then delegate the cross-document comparison to a demanded M5 method

`DeletedFromAWithB = {a : DELETED(a, d_A) ∧ CURRENT(a, d_B)}` and its symmetric twin are a **cross-document** intersection of one document's DELETED set with the other's current content image. M6 **cannot** perform it: M5 hands `deletions(d)` back only as an **opaque `SpanSet`**, M1 exposes no SpanSet enumeration/partition, and the mixed-length covers (from transcluded origins) fault `intersect_sets`/`normalize`. M5's published `deletions` seam computes only a *single* document's difference, not the cross-document combine SHOWDELETIONS requires. The combiner therefore must live in M5 — beside R, with run-level access to both documents and the level-class machinery already used by `project`/`deletions` — **but M5's interface as given does not expose it.** SHOWDELETIONS is consequently **blocked on a required M5 amendment**; M6's contribution is only the registration gate and the result wrapping.

```rust
pub fn show_deletions(&self, d_a: &Address, d_b: &Address) -> Result<Deletions, DeletionsError> {
    let m3 = self.0.world().m3();
    let m5 = self.0.world().m5();
    for d in [d_a, d_b] {
        if !require_registered(m3, d) { return Err(DeletionsError::DocNotRegistered(d.clone())); }
    }
    // ⚠ BLOCKED — the call below is the DEMANDED M5 amendment `cross_deletions`, NOT a method M5's
    // interface provides as given. The cross-document DELETED(·,d_A) ∧ CURRENT(·,d_B) intersection is
    // unbuildable from M5's published surface (opaque, possibly mixed-length SpanSets; no M1 SpanSet
    // enumeration/partition; intersect_sets/normalize fault on mixed-length input), so it MUST be added
    // to M5, beside R and the level-class discipline. The gate above is M6's entire contribution until
    // M5's design adopts the method specified next.
    let (a_with_b, b_with_a) = m5.cross_deletions(d_a, d_b);   // ← REQUIRES the M5 amendment below
    Ok(Deletions { a_with_b, b_with_a })
}
```

```rust
// ════════ REQUIRED M5 INTERFACE AMENDMENT (cross-module change; M5's design must adopt it) ════════
// NOT present in M5's interface as given. Demanded signature + pinned output contract:
impl M5State {
    /// Both halves of SHOWDELETIONS, computed beside R: reads BOTH documents' (M, R) off one slice
    /// and applies the level-class discipline internally —
    ///     a_with_b = { a ∈ dom(C) : DELETED(a, d_a) ∧ CURRENT(a, d_b) }
    ///     b_with_a = { a ∈ dom(C) : DELETED(a, d_b) ∧ CURRENT(a, d_a) }
    /// OUTPUT CONTRACT (PINNED — load-bearing): each returned SpanSet MUST be an *exact* cover of its
    /// dom(C) address set — a unit-span cover per level-class denoting EXACTLY that set, with NO
    /// coalesced-over phantom address. A coarser (merged-span) return makes the I-coverage
    /// over-approximate dom(C) and breaks the lossless re-encoding M6 relies on (Conflicts resolved 9).
    pub fn cross_deletions(&self, d_a: &Address, d_b: &Address) -> (SpanSet, SpanSet);
}
// ═══════════════════════════════════════════════════════════════════════════════════════════════════
```

- **Status: blocked on the M5 amendment above.** SHOWDELETIONS is the *only* M6 operation not buildable against the upstream interfaces as given; the other six compile today. M6's design contribution is final (the registration gate + result wrapping + the pinned demand on M5); the missing piece is a cross-module change M5 must accept.
- **Output is I-coverage**, the compact span form feeding an identity-preserving restore (the addresses *are* the existing I-addresses, D-IDENT). Lossless **only under the pinned exact-cover contract** above; because the result is a `SpanSet` and M1 offers no SpanSet enumeration, the individual `dom(C)` members are not recoverable above M5 — accepted as the coverage-consuming restore contract (*Conflicts resolved* 9).
- **No torn read:** `cross_deletions` reads one `&M5State` off one snapshot, so `(M, R)` is a single boundary — the digest's "R-ahead-of-M phantom deletion" cannot occur (M2 commits composites atomically).
- **D-DISJ short-circuit** (skip R-disjoint pairs) belongs inside the demanded `cross_deletions` (M5), since M6 no longer touches `ever_placed`.

### COMPARE — interval equi-join on I-address, complete under fan-out

The contract is a relational join keyed on **address equality, never value** — so COMPARE **never opens M4**. Three phases: resolve regions to blocks, interval-join on the I-axis with cross-product on overlap, coalesce-and-canonicalize.

```rust
pub fn compare(&self, rho1: &[Spec], rho2: &[Spec]) -> Result<CompareReport, CompareError> {
    let (m3, m5) = (self.0.world().m3(), self.0.world().m5());
    for (i, s) in rho1.iter().chain(rho2).enumerate() {
        if !require_registered(m3, &s.doc) { return Err(CompareError::DocNotRegistered(s.doc.clone())); }
        if *s.span.start().get(1) != s_c()  { return Err(CompareError::NotContentSubspace); }   // start in content subspace
        gate_vspec(&s.span).map_err(|f| CompareError::MalformedSpan { index: i, fault: f })?;
    }
    let (p, q) = (resolve_blocks(m5, rho1), resolve_blocks(m5, rho2));   // Vec<Block>; reads ONLY M5
    let pairs  = interval_join(&p, &q);                                  // cross-product per overlap (X8 completeness)
    Ok(CompareReport(canonicalize(pairs)))                              // R1–R3 conforming, deterministic order (X12)
}

fn resolve_blocks(m5: &M5State, specs: &[Spec]) -> Vec<Block> {
    let mut out = Vec::new();
    for s in specs {
        // V-RECONSTRUCTION LEMMA (load-bearing for X12-R1 soundness, correct ONLY under D-CTG★):
        // content is gap-free, so the FIRST bound V-position of a content span IS span.start(), and
        // resolve's runs tile the bound prefix CONTIGUOUSLY in V. Hence the V-cursor starts at
        // span.start() and advances by each run's width — there are no V-gaps to skip.
        let mut v = s.span.start().clone();
        let mut first = true;
        for run in m5.resolve(&s.doc, &s.span) {
            if first {
                // Assert the lemma in debug: M(d)(span.start()) == first run's i_start. A future M5
                // regression to V-gapped content runs then fails LOUDLY rather than mis-aligning u1/u2.
                debug_assert_eq!(m5.point(&s.doc, &vpos_of(&v)).as_ref(), Some(&run.i_start),
                    "D-CTG★: first content run must begin at span.start()");
                first = false;
            }
            out.push(Block { doc: s.doc.clone(), v_start: v.clone(),
                             i_start: run.i_start.clone(), width: run.width.clone() });
            v = shift(&v, &run.width);                                  // accumulate V offset by run width (no V-gaps in content)
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
fn reach_i(b: &Block) -> Tumbler { shift(b.i_start.tumbler(), &b.width) }   // i_start ⊕ δ(width,#): one I-step past the run; raw shift SAFE — i_start is element-level (last component = ordinal)
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
    // Simplicity-oracle form: full O(|P|·|Q|) cross-product, emit EVERY I-overlap (X8 fan-out
    // completeness). Production may sort both sides by i_start and sweep / interval-tree for the
    // same pair multiset.
    let mut out = Vec::new();
    for pb in p { for qb in q { if let Some(c) = overlap_pair(pb, qb) { out.push(c); } } }
    out
}

fn canonicalize(mut pairs: Vec<CorrPair>) -> Vec<CorrPair> {
    // Deterministic presentation (X12 R3) of the complete+sound relation (R1/R2); NOT claimed maximal
    // (R4 optional). 1) sort lexicographically by (d1, u1, d2, u2); 2) fold neighbours where BOTH feet
    // advance by one AND the two i-addresses are consecutive into single wider pairs (finer-than-maximal
    // residue is conforming).
    pairs.sort_by(|x, y| corr_key(x).cmp(&corr_key(y)));
    fold_adjacent(pairs)
}
fn corr_key(c: &CorrPair) -> (Tumbler, Tumbler, Tumbler, Tumbler) {
    (c.d1.tumbler().clone(), vpos_tumbler(&c.u1), c.d2.tumbler().clone(), vpos_tumbler(&c.u2))
}
fn vpos_tumbler(v: &VPos) -> Tumbler { Tumbler::new([v.subspace.clone(), v.ordinal.clone()]).unwrap() }
```

- **The second foot is computed within its own block.** `u2` offsets `qb.v_start` by `lo ⊖ qb.i_start` (lo's position *inside the Q-block*), not `lo ⊖ pb.i_start`. In the normal cross-document case `lo = max(pb.i_start, qb.i_start)` is one operand's start, so the inter-block gap would otherwise shift `u2` and make `res_Σ(d2, u2) ≠ a` — a violation of X12 **R1 (soundness)**. With the per-block offset, both feet resolve to the shared address `lo`.
- **Co-chain totality of the ordinal arithmetic.** Every `ordinal_gap` in `overlap_pair` runs only after the `lo < hi` overlap guard, hence only on addresses sharing one content chain (equal-length, equal prefix below the action point) — so the bare `ordinal(·) − ordinal(·)` subtractions are total `Nat` operations. Different-chain block pairs have disjoint I-intervals and are rejected by the guard before any subtraction. The helpers (`reach_i`/`ordinal_gap`/`max_tumbler`/`min_tumbler`/`vpos_shift`/`vpos_of`) all operate on `Tumbler` (callers thread `.tumbler()` off the `Address`), so the I-axis comparison typechecks uniformly (no `Address`/`Tumbler` mixing).
- **V-reconstruction lemma (load-bearing for X12-R1 soundness).** `resolve_blocks` sets the first run's `v_start = span.start()` and accumulates `v_start` by each run's width. This is correct **only because content is gap-free** (D-CTG★): the first bound V-position of a content span *is* `span.start()`, and `resolve`'s runs tile the bound prefix contiguously in V, so there are no V-gaps to skip. The code states this as the lemma it is and **`debug_assert`s it** (`M(d)(span.start()) == first_run.i_start`, via `m5.point`), so a future M5 regression to V-gapped content runs fails loudly rather than silently mis-aligning `u1`/`u2` (it would then need per-position `point` resolution or a V-carrying run type).
- **Fan-out completeness is the whole game** (the place a naïve implementation goes wrong): when an address occurs in multiple P-blocks and/or Q-blocks, `interval_join` must emit the **full cross-product** over each I-overlap, not a lockstep merge. The recommended structure is sort-by-`i_start` + sweep (or interval tree); the O(|P|·|Q|) double loop is the simplicity oracle. Either consumes blocks directly and reads only addresses (never bytes) — simultaneously the correctness property (value-matching over-reports) and the perf property (no content fault).
- **`canonicalize`** merges address-contiguous succ-adjacent pairs (both feet advance by one *and* their addresses are consecutive) into runs via `fold_adjacent`, then sorts lexicographically by `(d1, u1, d2, u2)`. This is a **deterministic** presentation (X12 R3) of the **complete and sound** relation (R1/R2). It is *not* claimed to be the X11 **maximal** form — X12 **R4 (maximal pairs) is explicitly not required for conformance**, and the address-contiguity merge yields a possibly-finer-than-maximal but fully conforming report (X10(c) permits a correspondence over a non-contiguous address sequence, which this merge would split — harmless under R1–R3). If literally-maximal output were wanted, merge instead on **feet-successor-adjacency** (the successor pair is itself in `corr`), independent of address contiguity. The second-foot tie-break is load-bearing under fan-out.

### FINDDOCSCONTAINING — resolve, then a present-tense filter over M5's R⁻¹ superset

This is the digest's recommended "monotone index + present-tense filter," with **M5 owning the monotone R⁻¹ index** and M6 owning only the resolve-union and the filter.

```rust
pub fn find_docs_containing(&self, regions: &[Region]) -> Result<Vec<Address>, FindError> {
    let (m3, m5) = (self.0.world().m3(), self.0.world().m5());
    // NOTE: Region spans are NOT gated to the content subspace, and that is CORRECT — FD's image_C
    // content-restriction is realized DOWNSTREAM: a link/foreign-subspace coverage contribution is inert
    // against M5's R⁻¹ (`docs_containing`, which indexes content provenance only — link placement is
    // R-uncoupled, J-LV) and against the content-only `project` filter, so it can add no spurious
    // container. A content-subspace gate here would be redundant and FD-unfaithful.
    let mut coverage = SpanSet::empty();                                // Phase 1: resolve to content I-coverage
    for r in regions {
        if !require_registered(m3, &r.doc) { return Err(FindError::DocNotRegistered(r.doc.clone())); }
        for span in &r.spans { coverage = union(&coverage, &m5.resolve_coverage(&r.doc, span)); }  // raw mixed-length; concat
    }
    let candidates = m5.docs_containing(&coverage);                     // Phase 2: R⁻¹ superset, tumbler-ordered (handles level-classes internally)
    Ok(candidates.into_iter()
        .filter(|d| m5.project(d, &coverage) != SpanSet::empty())      // present-tense soundness filter (FD-SOUND) — one project/candidate
        .collect())
}
```

- **The filter is the only difference between the live answer and the historical "ever-contained" answer** (`docs_containing` alone) — exactly the step the reference omits. `project(d, coverage)` is an I→V lookup, not a re-search; cost is proportional to the candidate set. Emptiness is tested with **`!= SpanSet::empty()`** (derived structural `PartialEq`; a non-empty result is structurally distinct from the empty vector and never carries a zero-width member) — not a fabricated `.is_empty()`.
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
- *Two-kinds-only, disjoint, pre-normalized extents* — fixed two-subspace iteration. (W9/W11/W13 0113.)

**By active enforcement** (M6 must guard, with the site named):
- *Well-formedness gates → typed rejection* — `gate_vspec` + `require_registered` at each operation's entry; the only in-model failures. (0115 well-formedness; WF_V 0077; W-pre 0112/0113; precondition 0122.)
- *Registered-empty → result vs. unallocated → fail* — **M6's owned distinction**, via `m3.is_registered_document`, applied per-operation (and tightened for SHOWORIGIN_V, which also rejects an empty *subspace*). (Decomposition; W-pre 0113; WF_V(iii) 0077.)
- *Single-subspace at the gate* — the ordinal-level check in `gate_vspec` makes a straddle unrepresentable for RETRIEVEV. (R10 0115.)
- *Partial-delivery never fails* — gaps/depth-incompat/foreign-subspace become empty contributions, never errors. (R6 0115.)
- *SHOWORIGIN_V admissibility* — reject empty document and unbound-range spans (the depth-agnostic `resolved < ordinal(width)` test), never clamp. (WF_V(iii,vi)/O13 0077.)
- *Completeness under fan-out; deterministic canonical order* — cross-product `interval_join` + `canonicalize`. (X8/R1/R2/R3 0122; X11 maximal / R4 not required.)
- *Present-tense soundness filter* — `project`-narrowing of `docs_containing`. (FD-SOUND 0124.)

**Delegated (M6 relies on, does not enforce):** contiguity D-CTG★ and referential integrity S3★ (M5 write path); R permanence/monotonicity, the J-couplings, the **level-class discipline on every coverage set-op**, the R⁻¹ index `docs_containing`, and — **once M5 adopts the demanded amendment** — the **whole cross-document deletion comparison `cross_deletions`** (M5); durability/recovery (M2). M6 trusts these and panics (not silently skips) if S3★ is observed broken on the content side. **SHOWDELETIONS is the one operation whose delegate does not yet exist in M5's interface — it is blocked on that amendment** (Conflicts resolved 1).

## Dependencies & seams

**Upstream calls (concrete):**
- **M1** — `document_of` (origin projection, SHOWORIGIN_V; I-address → origin Document in `run_addr`); `shift`/`shift_ordinal`+`ElemPos`/`elem_addr` (run-address enumeration, V-cursor advance, COMPARE `reach_i`); `from_endpoints`/`Span::new` (extent synthesis); `action_point`/`zeros`/`ordinal`/`Tumbler::get`/`Tumbler::new`/`is_level_uniform` (gates, the depth-agnostic count read, COMPARE ordinal arithmetic); `union`/`SpanSet::singleton`/`SpanSet::empty`/`SpanSet::is_normalized`/`SpanSet` `PartialEq` and tumbler `Ord` (set algebra, COMPARE overlaps, the FINDDOCSCONTAINING filter test, dedup ordering, normal-form assert).
- **M2** — `snapshot()` (one per logical query; M10 takes it), `Snapshot::world()`/`seq()`. No `transact`, no `Kernel` — M6 never writes.
- **M3** — `is_registered_document` (the universal allocation gate). Not `effective_owner` (authorization is M10's; SHOWORIGIN reports origin *documents*, not owners).
- **M4** — `value_at` (RETRIEVEV content only). `contains` available as a defensive S3★ check but not needed (M5 guarantees it). Never touched by COMPARE/extent/containment/deletions.
- **M5** — the workhorse: `resolve` (RETRIEVEV, SHOWORIGIN_V, COMPARE), `resolve_coverage` (FINDDOCSCONTAINING phase 1), `content_count`/`link_count` (extent queries, SHOWORIGIN_V subspace gate), `point` (COMPARE's debug-assert of the V-reconstruction lemma), `project` (FINDDOCSCONTAINING present-tense filter), `docs_containing` (FINDDOCSCONTAINING phase 2). **SHOWDELETIONS additionally requires the not-yet-published `cross_deletions` amendment** (the entire cross-document DELETED∧CURRENT comparison, per-level-class, beside R — see the SHOWDELETIONS section and Conflicts resolved 1); pending that amendment, M6 calls **no** `content_runs`/`deletions`/`ever_placed` directly — the DELETED operand is an opaque `SpanSet` M6 cannot decompose, so the combine cannot live in M6.

**Downstream seam (what M6 exposes — only M10 consumes it):** the seven read methods on `Query<'s, W>`. The contract M10 codes against: take a snapshot, build a `Query`, call the op, **marshal the returned value, and surface any `Err(_)` as a typed rejection** (these are precondition/well-formedness failures, never silent skips); a registered-empty document yields the operation's empty form (`⟨⟩`/empty `Delivery`/empty halves/`[]`), an unallocated one yields the op's `*NotRegistered` error. M6 returns by value and never commits, so there is no commit-before-acknowledge step for reads. **One M10-facing caveat:** `show_deletions` is not yet implementable (it depends on the demanded M5 `cross_deletions`), and M10 must not promise clients SHOWORIGIN-over-I (the V-arity only ships) — see Conflicts resolved 1 and 2.

**Engine assembly:** M6 contributes **no slice, no record variant, no accessor trait, no fold** — it is a pure consumer of `HasM3 + HasContent + HasM5`. Nothing in the engine's `World`/`Record` comes from M6, and no `apply`/`rebuild_derived` obligation attaches to it. (It therefore trivially satisfies the composition contract by being generic over `W` and naming no concrete `World`/`Record`.)

## Conflicts resolved

1. **Where the R indexes and coverage set-ops live — and the one place M5's interface falls short.** The decomposition lists M6 as owning the "reverse-index hint over R" and implies M6 computes the deletion set-algebra. M5's *as-built interface* instead exposes `docs_containing`, `deletions`, and `ever_placed` as **M5 methods**, co-locating the R index with R's authoritative state (Lampson: a hint belongs with the store that recomputes it on replay — only M5 folds R). **Resolution — mostly clean, one *blocked* seam:** M6 owns **no index and no coverage set-op**. FINDDOCSCONTAINING contributes only the phase-1 resolve-union and the present-tense `project` filter — **fully buildable** on `docs_containing` + `project`. SHOWDELETIONS, however, is **not** buildable on M5's published surface: the cross-document `DELETED(·,d_A) ∧ CURRENT(·,d_B)` intersection needs run-level access to both documents and the level-class machinery, but `deletions(d)`/`ever_placed(d)` arrive only as opaque, possibly mixed-length `SpanSet`s, M1 exposes no SpanSet enumeration/partition (only `empty`/`singleton`/`normalize`/`is_normalized`/`denotes`), and `intersect_sets`/`normalize` fault on mixed-length input — so M6 *cannot* perform the combine, and M5's published `deletions` seam ("read straight off it; M5 does the per-level-class difference") is **insufficient** (it yields a single document's difference, not the cross-document one SHOWDELETIONS requires). **The honest conclusion is a cross-module defect: M5's interface must grow a `cross_deletions(&self, d_a, d_b) -> (SpanSet, SpanSet)` method** (signature + pinned exact-cover output contract in the SHOWDELETIONS section), beside R where the runs and level-class discipline already are — a change M5's design must actually adopt. M6's design is final and correct; SHOWDELETIONS stays **blocked** until M5 adopts that method. The earlier draft's own `intersect_by_level_class`/`group_by_start_len`/`content_image` *inside M6* was doubly wrong — unbuildable (opaque SpanSets, faulting set-ops) *and* misplaced (authoritative-shaped state stateless M6 cannot recover). Putting the combiner in M5 is the right home; the gap is that M5 does not yet expose it.

2. **SHOWORIGIN_I de-scoped — recorded as a decomposition amendment.** `origins_I(σ) = {document_of(a) : a ∈ ⟦σ⟧ ∩ dom(C)}` needs an *enumeration of allocated content addresses across an I-interval*. M4 is point-only with `Ord` **deliberately** unused (its boundary forbids range/prefix/ordered scans) and M3 is point-only (`is_allocated`); neither exposes — and M4 by its stated design *excludes* — the I-ordered index this arity requires. Adding such a scan to M4 would itself be an upstream-overreach defect, and stateless M6 (no slice, no fold hook) cannot grow its own index. **Resolution:** M6 ships `show_origin_v` only. The I-arity is **de-scoped to a recorded decomposition amendment** — it belongs to a *new* I-ordered content index (a recomputable hint over M4's append-only writes, e.g. `allocated_content_in(span)`), a change to the module decomposition, not an M6 internal. Two caveats made explicit: (i) ASN-0077 designates *neither* arity "reader-facing" — preferring the V-arity is **M6's ruling**, not the note's; (ii) the de-scope is sound **only if** M10's FEBE command surface promises clients no SHOWORIGIN-over-I. M10 sources ASN-0077, so **a builder must confirm M10 exposes only the V-arity** — if M10 does promise the I-arity to external clients, this is a genuine capability hole and escalates from a recorded amendment to a **DEFECT** blocking the decomposition. The prior `show_origin_i`/`ISpanIndexUnavailable` placeholders are removed.

3. **`m_S(d)` depth hint collapses to a constant.** ASN-0115/0112/0113 all weigh caching vs. recomputing the per-subspace common depth `m_S(d)`. **Resolution:** M5 fixes V-positions at depth 2, so `m_S(d) ≡ 2`; the depth-compatibility test is the static `#start == 2`, which M5's defensive `resolve` already enforces. No hint, no per-document scalar.

4. **RETRIEVEDOCVSPAN: count-read vs. confluent summary, and the negative-origin hazard (0112 OQ5).** The note offers a min/max read or a maintained summary tree whose relative displacement can drive the **origin negative** (violating S8a). **Resolution:** M6 synthesizes from M5's authoritative `content_count`/`link_count`, reading `min` as the subspace anchor `[s,1]` — never negative. The hazard is exclusive to the summary-tree path and is designed out. (This also resolves "trust counts vs. scan": trust M5's counts; D-CTG★ is M5's write-path obligation; debug-assert optionally.)

5. **Byte-clipping / run-coalescing / width≠count (0115).** The digest's elaborate boundary-clipping presumes a byte-granular store. **Resolution:** M4 stores opaque `Val`s keyed per address and M5's arrangement is per-address, so M6 delivers **one item per active V-position** — exact, no dedup, no byte clip. "Never coalesce across a gap" is satisfied trivially by per-position delivery (and remains safe if a builder chooses segment/streaming delivery, since M5's runs are gap-aligned). Byte-boundary semantics are a property of how content was chunked into `Val`s *below* M6.

6. **0112 vs. 0113 overlap.** Both are "document extent." **Resolution:** complementary, not conflicting — they share the same count-read core; `doc_vspan` is the whole-document bounding span (a bounding box across subspaces), `doc_vspanset` is the per-subspace exact span-set. Fragmentation-sensitive callers use the latter; M10 routes accordingly.

7. **SHOWORIGIN vs. FINDDOCSCONTAINING (a distinction to *preserve*, not a conflict).** SHOWORIGIN reports the **original allocator** (`document_of`), FINDDOCSCONTAINING the **current holders** (R⁻¹ filtered to present). Different questions; M6 keeps them on different machinery (M1 projection vs. M5's R index + filter) so neither is mistaken for the other.

8. **`gate_vspec`'s ordinal-level requirement is an upstream-forced narrowing, recorded deliberately.** ASN-0077 WF_V(iv) requires only `actionPoint(ℓ) ≤ #u`, and ASN-0122 X12 requires only T12-well-formedness + a content-subspace start — *not* strict ordinal-level. M6 nonetheless gates all three resolve-based ops (RETRIEVEV, SHOWORIGIN_V, COMPARE) to **ordinal-level** spans. **Resolution:** the narrowing is forced by M5's `resolve`, which is defensive and yields ⟨⟩ for any span that is not `#start == 2 ∧ #width == 2 ∧ width.get(1) == 0` (ordinal-level depth-2). A non-ordinal-level span would therefore resolve to nothing upstream regardless, and every selection these notes name is expressible as an ordinal-level span in the depth-2 model — so gating ordinally up front turns a silent upstream empty into an explicit, typed rejection (`MalformedSpec`/`MalformedSpan`) without losing any admissible query. Recorded here as a deliberate, M5-driven restriction rather than an implicit one.

9. **SHOWDELETIONS returns coverage, not an address set — lossless only under the pinned exact-cover contract.** ASN-0075 speaks of `dom(C)` *address sets*, and D-IDENT/D-ORD reason about each individual returned I-address `a`. M6's `Deletions { a_with_b: SpanSet, b_with_a: SpanSet }` re-encodes those sets as I-coverage. This is a **lossless** re-encoding **iff** the demanded `cross_deletions` honors its pinned output contract — an *exact* unit-span cover per level-class, denoting exactly the `dom(C)` member set with no coalesced-over phantom address. A coarser (merged-span) return would make the coverage *over-approximate* `dom(C)`, silently admitting never-deleted addresses — which is why the exact-cover contract is **pinned on the amendment**, not left to M5's discretion. Given that contract: because the result is a `SpanSet` and M1 exposes no SpanSet enumeration, a downstream consumer cannot recover the individual `a`s from the result — accepted as the contract for the **coverage-consuming restore path** (the identity-preserving restore reads coverage directly; the addresses *are* the existing I-addresses, never copies, D-IDENT holds of the encoded set). A consumer that genuinely needs the enumerated `dom(C)` members would require a SpanSet-enumeration seam on M1 (or an address-list variant of `cross_deletions`); flagged, not built, since no current consumer needs it.

## Open build decisions

- **COMPARE matcher structure.** Sort-by-`i_start` + sweep (or interval tree) for the cross-product join — the production default, consumes M5's blocks directly — vs. a per-position hash join on address (obviously fan-out-complete; the simplicity oracle to validate against). Pick the block interval join; keep the hash join as the test oracle.
- **RETRIEVEV delivery shape.** Per-position items (chosen default — exact, simplest) vs. coalesced gap-aligned segments vs. lazy streaming for large spec-sets. If streaming, decide how back-pressure interacts with partial-delivery (a stream still "succeeds" while emitting nothing for gaps), and whether `DeliveryItem::Content` borrows through the snapshot (zero-copy) instead of cloning the `Arc`.
- **Snapshot ownership.** M6 methods take `&Snapshot` so M10 controls the consistency scope (recommended); a convenience that snapshots per call is possible but couples M6 to `&Kernel`.
- **Extent contiguity check.** Trust `content_count`/`link_count` (O(1)) vs. debug-build cross-check against `content_runs` (catches a broken D-CTG★ from upstream). Trust in release, assert in debug.
- **SHOWDELETIONS D-DISJ short-circuit.** Belongs to the demanded `cross_deletions` (M5), not M6: any D-DISJ pre-check (rule out R-disjoint document pairs before the per-class intersection) is M5's optimization to fold into that method — once M5 adopts it, M6 simply calls it.
- **COMPARE link-start spans.** Reject loudly (recommended — `NotContentSubspace`) vs. leniently strip via a content-subspace front-filter. (Spans that merely *denote* link positions from a content start are always legal — `resolve` clips them — so this is only about a span whose *start* is in the link subspace.)
- **Result caching.** Recompute by default (cheap, local, lock-free). If COMPARE/SHOWDELETIONS profile hot, memoize as a *hint* keyed on `(Snapshot::seq, args)` — and for any RETRIEVEV delivery cache, key on the consulted *restriction* (`M(d)|⟦σ⟧`), never on output byte-identity (R7 is sufficiency, not biconditional). Never authoritative; always recompute on a miss.
- **FINDDOCSCONTAINING resolve timing.** Re-resolve per query (tracks present-tense drift) vs. cache the frozen resolved I-coverage at an earlier snapshot for stable "find more like this" (legitimate because content is permanently grounded). Different products want different answers; expose the choice at M10.
