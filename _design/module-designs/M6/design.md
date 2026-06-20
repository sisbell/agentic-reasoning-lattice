# M6 — Content Retrieval & Query — Detailed Design

## Purpose & boundary

M6 is the system's **read-only observer surface over documents**. It owns the seven content/provenance queries — RETRIEVEV, RETRIEVEDOCVSPAN, RETRIEVEDOCVSPANSET, SHOWORIGIN (V-arity), SHOWDELETIONS, COMPARE, FINDDOCSCONTAINING — and turns the authoritative state held below it (M3's registry, M4's content, M5's arrangements and provenance relation R) into delivered values, extents, origins, deletion sets, correspondence reports, and containment answers. Every operation is a **pure function of one consistent M2 snapshot**: it resolves through M5's arrangements, fetches bytes from M4, projects origin via M1, reads R through M5, and gates on M3's registry — and writes nothing, ever.

**One thing well:** *observe documents over a single pinned snapshot — resolve, fetch, project, classify, compose — never mutate.*

It does **not** own: any authoritative or derived-authoritative state (none — it has no `WorldState` slice, no journal record, no fold); the R relation, its reverse index, or the cross-document deletion comparison (M5 — `docs_containing`/`deletions`/`cross_deletions` are M5's, co-located with R); content bytes (M4); arrangements (M5); link-side discovery (M8); the request lifecycle, dispatch, and marshaling (M10). It also does **not** deliver SHOWORIGIN's *I-span* arity: that arity needs an I-ordered enumeration of `dom(C)` over an interval, which M4's point-only interface (with `Ord` deliberately unused, range/prefix scans forbidden) and M3's point-only registry deliberately exclude; the I-arity is therefore **formally de-scoped from M6** (see *Conflicts resolved* 2). M6 delivers SHOWORIGIN's V-arity — the reader-facing one.

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
    /// SHOWORIGIN over a V-span (ASN-0077, V-arity — the reader-facing arity; the I-arity is
    /// de-scoped, see *Conflicts resolved* 2). Deduplicated origin documents, in tumbler order.
    /// Inadmissible (Err) on an empty/unallocated document or when the span's positions are not all
    /// currently bound (WF_V (iii)/(vi); O13) — reject, never silently clamp.
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
    /// fine and yields empty halves). Output is I-address coverage, not values. The cross-document
    /// comparison itself is M5's (`cross_deletions`); M6 gates and wraps.
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
- the **R reverse index and the cross-document deletion comparison** (FINDDOCSCONTAINING, SHOWDELETIONS) live in M5, co-located with R's authoritative state (recomputable by replay only where R is folded);
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
        let sub = s.span.start().get(1).clone();       // 1=content, 2=link
        for run in m5.resolve(&s.doc, &s.span) {       // V-ordered, clipped, gap-aligned; #start≠2 ⇒ ⟨⟩ (depth-incompat)
            let mut k = Nat::zero();
            while &k < &run.width {                     // per active position, ascending V (R3) — no dedup (R8)
                let a = run_addr(&run.i_start, &k);
                if sub == s_c() { out.push(DeliveryItem::Content(
                                    c.value_at(a.tumbler()).expect("S3★: content position ⇒ a∈dom(C)").clone())); }
                else if sub == s_l() { out.push(DeliveryItem::Ref(a)); }  // link reference IS the address — never reads M4
                k += 1u8;
            }
        }
    }
    Ok(Delivery(out))                                   // empty spec-set ⇒ Ok(Delivery(vec![]))
}
```

- **Common case:** a single content spec over a contiguous run — one M5 range scan, *w* M4 point lookups (one `Val` per address, each an `Arc` clone). Links never touch M4.
- **Gaps / depth-incompat / foreign subspaces** all funnel through M5's defensive `resolve` returning fewer-or-zero runs → silent empty contribution; the request still succeeds (R6). The `m_S ≡ 2` simplification means depth-incompatibility *is* `#start ≠ 2`, which `resolve` already force-empties.
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
    Ok(result)   // disjoint, content-before-link, appended in order ⇒ already normal (W13); union is concat (never normalizes/faults)
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
- **No invented M1 surface:** `doc_vspanset` builds the ≤2-member set by **`union` of singletons** (concatenation preserves the already-disjoint, content-before-link W13 normal form), not a fabricated `from_normalized_ordered`.
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

`origins_I(σ) = {document_of(a) : a ∈ ⟦σ⟧ ∩ dom(C)}` requires enumerating allocated content addresses across an I-interval. No upstream surface provides this: M4 is point-only with `Ord` **deliberately** unused and its boundary forbidding range/prefix scans, and M3's registry is point-only (`is_allocated`). Stateless M6 has no fold hook to grow its own index. Per *Conflicts resolved* 2 the I-arity is **formally de-scoped from M6**; only `show_origin_v` ships, and `OriginError` carries no `ISpanIndexUnavailable` placeholder. (Were the I-arity ever needed, it belongs to a new I-ordered content index over M4's append-only writes — a decomposition amendment, not an M6 internal.)

### SHOWDELETIONS — gate, then delegate the cross-document comparison to M5

`DeletedFromAWithB = {a : DELETED(a, d_A) ∧ CURRENT(a, d_B)}` and its symmetric twin are a **cross-document** intersection of one document's DELETED set with the other's current content image. M6 **cannot** perform it: M5 hands `deletions(d)` back only as an **opaque `SpanSet`**, M1 exposes no SpanSet enumeration/partition, and the mixed-length covers (from transcluded origins) fault `intersect_sets`/`normalize`. The combiner therefore lives in M5 — beside R, with run-level access to both documents and the level-class machinery already used by `project`/`deletions` — and M6 only gates and wraps.

```rust
pub fn show_deletions(&self, d_a: &Address, d_b: &Address) -> Result<Deletions, DeletionsError> {
    let m3 = self.0.world().m3();
    let m5 = self.0.world().m5();
    for d in [d_a, d_b] {
        if !require_registered(m3, d) { return Err(DeletionsError::DocNotRegistered(d.clone())); }
    }
    // The cross-document DELETED∧CURRENT comparison is M5's `cross_deletions`: it reads BOTH documents'
    // (M,R) off one slice and applies the level-class discipline internally, returning each half as a
    // per-level-class-correct SpanSet. M6 owns no level-class discipline and no coverage set-op.
    let (a_with_b, b_with_a) = m5.cross_deletions(d_a, d_b);
    Ok(Deletions { a_with_b, b_with_a })
}
```

- **Output is I-coverage**, the compact span form feeding an identity-preserving restore (the addresses *are* the existing I-addresses, D-IDENT). Because M5 returns coverage and M1 offers no SpanSet enumeration, the individual `dom(C)` members are not recoverable above M5 — accepted as the coverage-consuming restore contract (*Conflicts resolved* 9).
- **No torn read:** `cross_deletions` reads one `&M5State` off one snapshot, so `(M, R)` is a single boundary — the digest's "R-ahead-of-M phantom deletion" cannot occur (M2 commits composites atomically).
- **D-DISJ short-circuit** (skip R-disjoint pairs) is now M5's to apply inside `cross_deletions`, since M6 no longer touches `ever_placed`.

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
        let mut v = s.span.start().clone();                             // first bound V-pos = span start (content is gap-free)
        for run in m5.resolve(&s.doc, &s.span) {
            out.push(Block { doc: s.doc.clone(), v_start: v.clone(), i_start: run.i_start.clone(), width: run.width.clone() });
            v = shift(&v, &run.width);                                  // accumulate V offset by run width (no V-gaps in content)
        }
    }
    out
}

fn overlap_pair(pb: &Block, qb: &Block) -> Option<CorrPair> {
    let lo = max_tumbler(&pb.i_start, &qb.i_start);                     // I-interval overlap
    let hi = min_tumbler(&reach_i(pb), &reach_i(qb));
    if !(lo < hi) { return None; }
    let w = ordinal_gap(&hi, &lo);                                      // overlap width (Nat)
    Some(CorrPair {
        d1: pb.doc.clone(), u1: vpos_shift(&pb.v_start, &ordinal_gap(&lo, &pb.i_start)),  // slot 1 ⇐ operand 1; lo's offset within P (X3)
        d2: qb.doc.clone(), u2: vpos_shift(&qb.v_start, &ordinal_gap(&lo, &qb.i_start)),  // slot 2 ⇐ operand 2; lo's offset within Q
        width: w,
    })
}
```

- **The second foot is computed within its own block.** `u2` offsets `qb.v_start` by `lo ⊖ qb.i_start` (lo's position *inside the Q-block*), not `lo ⊖ pb.i_start`. In the normal cross-document case `lo = max(pb.i_start, qb.i_start)` is one operand's start, so the inter-block gap would otherwise shift `u2` and make `res_Σ(d2, u2) ≠ a` — a violation of X12 **R1 (soundness)**. With the per-block offset, both feet resolve to the shared address `lo`.
- **Reconstructing V-positions** from `resolve`'s `Vec<Run>` relies on content arrangements being **gap-free** (D-CTG★): the first run starts at the span start and runs tile the bound prefix contiguously in V, so `v_start` accumulates by width. (If M5 ever returned V-gapped content runs — it must not — COMPARE would need per-position resolution via `point` or a richer run type; flagged as an assumption.)
- **Fan-out completeness is the whole game** (the place a naïve implementation goes wrong): when an address occurs in multiple P-blocks and/or Q-blocks, `interval_join` must emit the **full cross-product** over each I-overlap, not a lockstep merge. The recommended structure is sort-by-`i_start` + sweep (or interval tree); the O(|P|·|Q|) double loop is the simplicity oracle. Either consumes blocks directly and reads only addresses (never bytes) — simultaneously the correctness property (value-matching over-reports) and the perf property (no content fault).
- **`canonicalize`** merges address-contiguous succ-adjacent pairs (both feet advance by one *and* their addresses are consecutive) into runs, then sorts lexicographically by `(d1, u1, d2, u2)`. This is a **deterministic** presentation (X12 R3) of the **complete and sound** relation (R1/R2). It is *not* claimed to be the X11 **maximal** form — X12 **R4 (maximal pairs) is explicitly not required for conformance**, and the address-contiguity merge yields a possibly-finer-than-maximal but fully conforming report (X10(c) permits a correspondence over a non-contiguous address sequence, which this merge would split — harmless under R1–R3). If literally-maximal output were wanted, merge instead on **feet-successor-adjacency** (the successor pair is itself in `corr`), independent of address contiguity. The second-foot tie-break is load-bearing under fan-out.

### FINDDOCSCONTAINING — resolve, then a present-tense filter over M5's R⁻¹ superset

This is the digest's recommended "monotone index + present-tense filter," with **M5 owning the monotone R⁻¹ index** and M6 owning only the resolve-union and the filter.

```rust
pub fn find_docs_containing(&self, regions: &[Region]) -> Result<Vec<Address>, FindError> {
    let (m3, m5) = (self.0.world().m3(), self.0.world().m5());
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

**Delegated (M6 relies on, does not enforce):** contiguity D-CTG★ and referential integrity S3★ (M5 write path); R permanence/monotonicity, the J-couplings, the **level-class discipline on every coverage set-op**, and the **whole cross-document deletion comparison `cross_deletions`** (M5); durability/recovery (M2). M6 trusts these and panics (not silently skips) if S3★ is observed broken on the content side.

## Dependencies & seams

**Upstream calls (concrete):**
- **M1** — `document_of` (origin projection, SHOWORIGIN_V; I-address → origin Document in `run_addr`); `shift`/`shift_ordinal`+`ElemPos`/`elem_addr` (run-address enumeration, V-cursor advance); `from_endpoints`/`Span::new` (extent synthesis); `action_point`/`zeros`/`ordinal`/`Tumbler::get`/`is_level_uniform` (gates and the depth-agnostic count read); `union`/`SpanSet::singleton`/`SpanSet::empty`/`SpanSet` `PartialEq` and tumbler `Ord` (set algebra, COMPARE overlaps, the FINDDOCSCONTAINING filter test, dedup ordering).
- **M2** — `snapshot()` (one per logical query; M10 takes it), `Snapshot::world()`/`seq()`. No `transact`, no `Kernel` — M6 never writes.
- **M3** — `is_registered_document` (the universal allocation gate). Not `effective_owner` (authorization is M10's; SHOWORIGIN reports origin *documents*, not owners).
- **M4** — `value_at` (RETRIEVEV content only). `contains` available as a defensive S3★ check but not needed (M5 guarantees it). Never touched by COMPARE/extent/containment/deletions.
- **M5** — the workhorse: `resolve` (RETRIEVEV, SHOWORIGIN_V, COMPARE), `resolve_coverage` (FINDDOCSCONTAINING phase 1), `content_count`/`link_count` (extent queries, SHOWORIGIN_V subspace gate), `project` (FINDDOCSCONTAINING present-tense filter), `docs_containing` (FINDDOCSCONTAINING phase 2), `cross_deletions` (SHOWDELETIONS — the entire cross-document DELETED∧CURRENT comparison, computed per-level-class inside M5). M6 calls **no** `content_runs`/`deletions`/`ever_placed` directly — the deletion comparison moved wholesale into M5 (defect-1 fix: the DELETED operand is an opaque `SpanSet` M6 cannot decompose).

**Downstream seam (what M6 exposes — only M10 consumes it):** the seven read methods on `Query<'s, W>`. The contract M10 codes against: take a snapshot, build a `Query`, call the op, **marshal the returned value, and surface any `Err(_)` as a typed rejection** (these are precondition/well-formedness failures, never silent skips); a registered-empty document yields the operation's empty form (`⟨⟩`/empty `Delivery`/empty halves/`[]`), an unallocated one yields the op's `*NotRegistered` error. M6 returns by value and never commits, so there is no commit-before-acknowledge step for reads.

**Engine assembly:** M6 contributes **no slice, no record variant, no accessor trait, no fold** — it is a pure consumer of `HasM3 + HasContent + HasM5`. Nothing in the engine's `World`/`Record` comes from M6, and no `apply`/`rebuild_derived` obligation attaches to it. (It therefore trivially satisfies the composition contract by being generic over `W` and naming no concrete `World`/`Record`.)

## Conflicts resolved

1. **Where the R indexes and coverage set-ops live (the biggest scope narrowing).** The decomposition lists M6 as owning the "reverse-index hint over R" and implies M6 computes the deletion set-algebra. M5's *as-built interface* instead exposes `docs_containing`, `deletions`, and `ever_placed` as **M5 methods**, co-locating the R index with R's authoritative state (Lampson: a hint belongs with the store that recomputes it on replay — only M5 folds R). **Resolution:** M6 owns **no index and no coverage set-op**. FINDDOCSCONTAINING contributes only the phase-1 resolve-union and the present-tense `project` filter; SHOWDELETIONS contributes only the registration gate and result wrapping — the cross-document DELETED∧CURRENT intersection is **M5's `cross_deletions`**. The earlier draft had M6 partition and intersect the mixed-length covers itself (`intersect_by_level_class`/`group_by_start_len`/`content_image`); that is **unbuildable** — `deletions(d)`/`ever_placed(d)` arrive only as opaque `SpanSet`s, and M1 exposes no SpanSet enumeration/partition (only `empty`/`singleton`/`normalize`/`is_normalized`/`denotes`), while `intersect_sets`/`normalize` fault on the mixed-length input. The cross-document combiner must therefore live where the runs and the level-class machinery already are — in M5, beside R — extending this conflict's own co-location principle (the `cross_deletions` seam is requested of M5 on exactly that ground). Putting any index or cross-doc combiner in stateless M6 would be authoritative-shaped state M6 cannot recover. I honor the M5 interface.

2. **SHOWORIGIN_I de-scoped (a ruling, not a stub).** `origins_I(σ) = {document_of(a) : a ∈ ⟦σ⟧ ∩ dom(C)}` needs an *enumeration of allocated content addresses across an I-interval*. M4 is point-only with `Ord` **deliberately** unused (its boundary forbids range/prefix/ordered scans) and M3 is point-only (`is_allocated`); neither exposes — and M4 by its stated design *excludes* — the I-ordered index this arity requires. Adding such an index would contradict M4's interface boundary, and M6, holding no state and no fold hook, cannot grow its own. **Ruling:** the SHOWORIGIN *I-arity is formally de-scoped from M6's mandate* — the V-arity is the reader-facing one (ASN-0077's V-span resolver) and is fully built. If the I-arity is ever required, it belongs to a new I-ordered content index (a recomputable hint over M4's append-only writes, e.g. `allocated_content_in(span)`), which is a **decomposition amendment**, not an M6 internal. M6's interface therefore offers `show_origin_v` only; the prior `show_origin_i`/`ISpanIndexUnavailable` placeholders are removed.

3. **`m_S(d)` depth hint collapses to a constant.** ASN-0115/0112/0113 all weigh caching vs. recomputing the per-subspace common depth `m_S(d)`. **Resolution:** M5 fixes V-positions at depth 2, so `m_S(d) ≡ 2`; the depth-compatibility test is the static `#start == 2`, which M5's defensive `resolve` already enforces. No hint, no per-document scalar.

4. **RETRIEVEDOCVSPAN: count-read vs. confluent summary, and the negative-origin hazard (0112 OQ5).** The note offers a min/max read or a maintained summary tree whose relative displacement can drive the **origin negative** (violating S8a). **Resolution:** M6 synthesizes from M5's authoritative `content_count`/`link_count`, reading `min` as the subspace anchor `[s,1]` — never negative. The hazard is exclusive to the summary-tree path and is designed out. (This also resolves "trust counts vs. scan": trust M5's counts; D-CTG★ is M5's write-path obligation; debug-assert optionally.)

5. **Byte-clipping / run-coalescing / width≠count (0115).** The digest's elaborate boundary-clipping presumes a byte-granular store. **Resolution:** M4 stores opaque `Val`s keyed per address and M5's arrangement is per-address, so M6 delivers **one item per active V-position** — exact, no dedup, no byte clip. "Never coalesce across a gap" is satisfied trivially by per-position delivery (and remains safe if a builder chooses segment/streaming delivery, since M5's runs are gap-aligned). Byte-boundary semantics are a property of how content was chunked into `Val`s *below* M6.

6. **0112 vs. 0113 overlap.** Both are "document extent." **Resolution:** complementary, not conflicting — they share the same count-read core; `doc_vspan` is the whole-document bounding span (a bounding box across subspaces), `doc_vspanset` is the per-subspace exact span-set. Fragmentation-sensitive callers use the latter; M10 routes accordingly.

7. **SHOWORIGIN vs. FINDDOCSCONTAINING (a distinction to *preserve*, not a conflict).** SHOWORIGIN reports the **original allocator** (`document_of`), FINDDOCSCONTAINING the **current holders** (R⁻¹ filtered to present). Different questions; M6 keeps them on different machinery (M1 projection vs. M5's R index + filter) so neither is mistaken for the other.

8. **`gate_vspec`'s ordinal-level requirement is an upstream-forced narrowing, recorded deliberately.** ASN-0077 WF_V(iv) requires only `actionPoint(ℓ) ≤ #u`, and ASN-0122 X12 requires only T12-well-formedness + a content-subspace start — *not* strict ordinal-level. M6 nonetheless gates all three resolve-based ops (RETRIEVEV, SHOWORIGIN_V, COMPARE) to **ordinal-level** spans. **Resolution:** the narrowing is forced by M5's `resolve`, which is defensive and yields ⟨⟩ for any span that is not `#start == 2 ∧ #width == 2 ∧ width.get(1) == 0` (ordinal-level depth-2). A non-ordinal-level span would therefore resolve to nothing upstream regardless, and every selection these notes name is expressible as an ordinal-level span in the depth-2 model — so gating ordinally up front turns a silent upstream empty into an explicit, typed rejection (`MalformedSpec`/`MalformedSpan`) without losing any admissible query. Recorded here as a deliberate, M5-driven restriction rather than an implicit one.

9. **SHOWDELETIONS returns coverage, not an address set (confirmed acceptable).** ASN-0075 speaks of `dom(C)` *address sets*, and D-IDENT/D-ORD reason about each individual returned I-address `a`. M6's `Deletions { a_with_b: SpanSet, b_with_a: SpanSet }` is a **lossless re-encoding** of those sets as I-coverage — but because `cross_deletions` returns `SpanSet` and M1 exposes no SpanSet enumeration, a downstream consumer cannot recover the individual `a`s from the result. **Resolution:** this is inherited from the M5/M1 surfaces (not an M6 choice), and is accepted as the contract for the **coverage-consuming restore path** — the identity-preserving restore reads coverage directly, and the addresses *are* the existing I-addresses, never copies (D-IDENT holds of the encoded set). A consumer that genuinely needs the enumerated `dom(C)` members would require a SpanSet-enumeration seam on M1 (or an address-list variant of M5's `cross_deletions`); flagged, not built, since no current consumer needs it.

## Open build decisions

- **COMPARE matcher structure.** Sort-by-`i_start` + sweep (or interval tree) for the cross-product join — the production default, consumes M5's blocks directly — vs. a per-position hash join on address (obviously fan-out-complete; the simplicity oracle to validate against). Pick the block interval join; keep the hash join as the test oracle.
- **RETRIEVEV delivery shape.** Per-position items (chosen default — exact, simplest) vs. coalesced gap-aligned segments vs. lazy streaming for large spec-sets. If streaming, decide how back-pressure interacts with partial-delivery (a stream still "succeeds" while emitting nothing for gaps), and whether `DeliveryItem::Content` borrows through the snapshot (zero-copy) instead of cloning the `Arc`.
- **Snapshot ownership.** M6 methods take `&Snapshot` so M10 controls the consistency scope (recommended); a convenience that snapshots per call is possible but couples M6 to `&Kernel`.
- **Extent contiguity check.** Trust `content_count`/`link_count` (O(1)) vs. debug-build cross-check against `content_runs` (catches a broken D-CTG★ from upstream). Trust in release, assert in debug.
- **SHOWDELETIONS D-DISJ short-circuit.** Now delegated: since the cross-document comparison is `cross_deletions` (M5), any D-DISJ pre-check (rule out R-disjoint document pairs before the per-class intersection) is M5's optimization to make, not M6's — M6 simply calls `cross_deletions`.
- **COMPARE link-start spans.** Reject loudly (recommended — `NotContentSubspace`) vs. leniently strip via a content-subspace front-filter. (Spans that merely *denote* link positions from a content start are always legal — `resolve` clips them — so this is only about a span whose *start* is in the link subspace.)
- **Result caching.** Recompute by default (cheap, local, lock-free). If COMPARE/SHOWDELETIONS profile hot, memoize as a *hint* keyed on `(Snapshot::seq, args)` — and for any RETRIEVEV delivery cache, key on the consulted *restriction* (`M(d)|⟦σ⟧`), never on output byte-identity (R7 is sufficiency, not biconditional). Never authoritative; always recompute on a miss.
- **FINDDOCSCONTAINING resolve timing.** Re-resolve per query (tracks present-tense drift) vs. cache the frozen resolved I-coverage at an earlier snapshot for stable "find more like this" (legitimate because content is permanently grounded). Different products want different answers; expose the choice at M10.
