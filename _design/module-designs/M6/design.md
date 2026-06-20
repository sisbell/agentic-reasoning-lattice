# M6 — Content Retrieval & Query — Detailed Design

## Purpose & boundary

M6 is the system's **read-only observer surface over documents**. It owns the seven content/provenance queries — RETRIEVEV, RETRIEVEDOCVSPAN, RETRIEVEDOCVSPANSET, SHOWORIGIN, SHOWDELETIONS, COMPARE, FINDDOCSCONTAINING — and turns the authoritative state held below it (M3's registry, M4's content, M5's arrangements and provenance relation R) into delivered values, extents, origins, deletion sets, correspondence reports, and containment answers. Every operation is a **pure function of one consistent M2 snapshot**: it resolves through M5's arrangements, fetches bytes from M4, projects origin via M1, reads R through M5, and gates on M3's registry — and writes nothing, ever.

**One thing well:** *observe documents over a single pinned snapshot — resolve, fetch, project, classify, compose — never mutate.*

It does **not** own: any authoritative or derived-authoritative state (none — it has no `WorldState` slice, no journal record, no fold); the R relation or its reverse index (M5 — `docs_containing`/`deletions`/`ever_placed` are M5's, co-located with R); content bytes (M4); arrangements (M5); link-side discovery (M8); the request lifecycle, dispatch, and marshaling (M10). It also does **not** own the I-ordered content index that SHOWORIGIN's *I-span* arity would require — that index is absent from the upstream interfaces and is flagged to M4 (see *Conflicts resolved*).

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
    /// SHOWORIGIN over a V-span (ASN-0077, primary arity). Deduplicated origin documents, in tumbler
    /// order. Inadmissible (Err) on an empty/unallocated document or when the span's positions are not
    /// all currently bound (WF_V (iii)/(vi); O13) — reject, never silently clamp.
    pub fn show_origin_v(&self, doc: &Address, span: &Span) -> Result<Vec<Address>, OriginError>;

    /// SHOWORIGIN over an I-span (ASN-0077). CONDITIONAL: its one new primitive — "allocated content
    /// addresses in an I-interval" — is NOT in M4/M3's current point-only interfaces. Unbuildable as-is;
    /// see *Conflicts resolved*. Signature reserved.
    pub fn show_origin_i(&self, span: &Span) -> Result<Vec<Address>, OriginError>;
}
```

### D. Provenance comparison

```rust
pub struct Deletions { pub a_with_b: SpanSet, pub b_with_a: SpanSet }  // I-coverage of deleted-from-one ∧ current-in-other

pub struct CorrPair { pub d1: Address, pub u1: VPos, pub d2: Address, pub u2: VPos, pub width: Nat }
pub struct CompareReport(pub Vec<CorrPair>);   // canonical order; slot i drawn from operand i

impl<'s, W: M6World> Query<'s, W> {
    /// SHOWDELETIONS (ASN-0075). Both documents must be registered (Err otherwise; allocated-empty is
    /// fine and yields empty halves). Output is I-address coverage, not values.
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
pub enum OriginError    { DocNotRegistered, EmptySubspace, RangeNotPresent, MalformedSpan(SpecFault),
                          ISpanIndexUnavailable /* show_origin_i, until the M4 seam exists */ }
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
   - SHOWDELETIONS's per-level-class grouping maps (`BTreeMap<usize, SpanSet>` keyed by endpoint length).
   - Dedup sets for origins/containers (`HashSet<Tumbler>` → sorted `Vec<Address>`, since `Address` is `Eq+Hash` but not `Ord`; `Tumbler` carries the `Ord`).

**Authoritative vs. recomputable, resolved explicitly for M6:** there is nothing to distinguish, because M6 holds neither. Three would-be hints all resolve away from M6:
- the **R reverse index** (FINDDOCSCONTAINING) lives in M5, co-located with R's authoritative state (recomputable by replay only where R is folded);
- the **per-subspace common depth `m_S(d)`** that the source notes fret over (cache vs. recompute) is the **constant 2** — M5 fixes V-positions at depth 2, so `m_S(d) ≡ 2` and the depth-compatibility test is the static `#start == 2`;
- the **I-ordered content index** for SHOWORIGIN_I belongs in M4 (the store whose append-only writes determine it), not in stateless M6.

## Internal design

Every operation begins by reading its slices off the single bound snapshot, runs its gate (typed rejection), then composes upstream primitives. Shared helpers:

```rust
fn require_registered(m3: &M3State, d: &Address) -> bool { m3.is_registered_document(d) }

fn gate_vspec(span: &Span) -> Result<(), SpecFault> {
    if !span.is_level_uniform()                            { return Err(SpecFault::NotLevelUniform); }   // #start == #width
    if action_point(span.width()) != Some(span.width().len()) { return Err(SpecFault::NotOrdinalLevel); }// acts at deepest
    if zeros(span.start()) != 0                           { return Err(SpecFault::StartNotZeroFree); }  // ⇒ all components > 0
    if span.start().len() < 2                             { return Err(SpecFault::StartTooShallow); }
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
                if sub == S_C { out.push(DeliveryItem::Content(
                                    c.value_at(a.tumbler()).expect("S3★: content position ⇒ a∈dom(C)").clone())); }
                else if sub == S_L { out.push(DeliveryItem::Ref(a)); }  // link reference IS the address — never reads M4
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
    let min = vpos(if !nc.is_zero() { S_C } else { S_L }, &Nat::one());              // min O(d): anchor of lowest occupied subspace
    let max = vpos(if !nl.is_zero() { S_L } else { S_C }, if !nl.is_zero() { &nl } else { &nc });
    let reach = shift(&max, &Nat::one());                                            // one ordinal step past max
    Ok(SpanSet::singleton(Span::from_endpoints(min, reach).unwrap()))                // origin=min; width=reach⊖min
}

pub fn doc_vspanset(&self, doc: &Address) -> Result<SpanSet, ExtentError> {
    let (m3, m5) = (self.0.world().m3(), self.0.world().m5());
    if !require_registered(m3, doc) { return Err(ExtentError::DocNotRegistered); }
    let (nc, nl) = (m5.content_count(doc), m5.link_count(doc));
    let mut members = Vec::new();
    if !nc.is_zero() { members.push(ext_span(S_C, &nc)); }   // ext(d,s_C) = ([1,1], [0,n_C])
    if !nl.is_zero() { members.push(ext_span(S_L, &nl)); }   // ext(d,s_L) = ([2,1], [0,n_L])
    Ok(SpanSet::from_normalized_ordered(members))            // disjoint, subspace-ordered ⇒ already normal (W13)
}
```
where `vpos(s,n)=Tumbler[s,n]`, `ext_span(s,n)=Span::new([s,1],[0,n])`.

- **`doc_vspan`** returns a single bounding span; across subspaces it is a bounding box bridging the inter-subspace void (`[1,1]..[2,n_L+1)`), insensitive to mid-document content edits (V9) — by design (route fragmentation-sensitive callers to `doc_vspanset`).
- **Negative-origin hazard (0112 OQ5) designed out:** because `min` is read as the subspace anchor `[s,1]` rather than absorbed into a confluent summary, the origin can never go negative.
- **Tradeoff:** trusting `content_count`/`link_count` rests on D-CTG★, which is M5's write-path obligation, not M6's. A debug-build cross-check (`Σ content_runs(d).width == content_count(d)` and first run anchored at `[s_C,1]`) is cheap defense-in-depth (open decision).

### SHOWORIGIN_V — block-decompose, project one origin per run

Origin is the pure address projection `document_of` (M1). Block uniformity (O2) means all addresses in one run share an origin, so M6 projects **one address per run** — O(runs), not O(positions).

```rust
pub fn show_origin_v(&self, doc: &Address, span: &Span) -> Result<Vec<Address>, OriginError> {
    let (m3, m5) = (self.0.world().m3(), self.0.world().m5());
    if !require_registered(m3, doc)        { return Err(OriginError::DocNotRegistered); }   // WF_V (i)
    gate_vspec(span).map_err(OriginError::MalformedSpan)?;                                  // (ii),(iv),(v): depth-2, ordinal-level
    let sub = span.start().get(1);
    let n_s = if *sub == S_C { m5.content_count(doc) }
              else if *sub == S_L { m5.link_count(doc) } else { Nat::zero() };
    if n_s.is_zero() { return Err(OriginError::EmptySubspace); }                            // (iii) inadmissible on empty subspace
    let runs = m5.resolve(doc, span);
    let resolved: Nat = runs.iter().map(|r| &r.width).sum();
    if &resolved < span.width().get(2) { return Err(OriginError::RangeNotPresent); }        // (vi) some position unbound — reject (O13)
    Ok(dedup_docs(runs.iter().map(|r| document_of(&r.i_start).unwrap())))                   // link case ⇒ {doc} by CL-OWN
}
```

- The `(iii)`/`(vi)` checks are the deliberate strictness: SHOWORIGIN_V is **inadmissible on an empty document and on a span overrunning the bound prefix** — reject-and-signal, never clamp to the surviving sub-span (the digest's explicit choice, O13).
- For the link subspace, `document_of(link)` is the home `doc` (CL-OWN) — handled uniformly, no special case.

### SHOWORIGIN_I — conditional on an absent seam

`origins_I(σ) = {document_of(a) : a ∈ ⟦σ⟧ ∩ dom(C)}` needs to **enumerate allocated content addresses in an I-interval**. M4 is point-only (`contains`/`value_at`; `Ord` deliberately unused, no range scan) and M3 exposes no frontier/range query. So this arity is **not buildable against the given interfaces.** The method returns `Err(ISpanIndexUnavailable)` until an upstream seam exists. Given one (`m4.allocated_content_in(span) -> impl Iterator<Address>`, a recomputable I-ordered hint over M4's append-only writes), the body is a boundary-walk: collect distinct `document_of(a)` over the enumerated addresses, plus the single-origin fast path (`document_of(start)==document_of(last)` gated on a non-empty existence check → `{that doc}`). See *Conflicts resolved* for the recommended placement.

### SHOWDELETIONS — cross-document intersection with the level-class discipline

M5 gives `deletions(d)` = `Rproj(d) \ ran(M(d))` (the DELETED set, computed per-level-class internally). The witness condition `CURRENT(a, partner)` is partner's current content image, reconstructed from `content_runs`. The set identity `(X\Y)∩Z = (X∩Z)\Y` makes `deletions(d_A) ∩ content_image(d_B)` exactly `DeletedFromAWithB`.

```rust
pub fn show_deletions(&self, d_a: &Address, d_b: &Address) -> Result<Deletions, DeletionsError> {
    let (m3, m5) = (self.0.world().m3(), self.0.world().m5());
    for d in [d_a, d_b] { if !require_registered(m3, d) { return Err(DeletionsError::DocNotRegistered(d.clone())); } }
    // Optional D-DISJ short-circuit: if level-class-disjoint(ever_placed(d_a), ever_placed(d_b)) ⇒ both halves ∅.
    let (del_a, del_b) = (m5.deletions(d_a), m5.deletions(d_b));        // per-level-class internally; possibly mixed-length
    let (cur_a, cur_b) = (content_image(m5, d_a), content_image(m5, d_b));
    Ok(Deletions {
        a_with_b: intersect_by_level_class(&del_a, &cur_b),            // DELETED from A ∧ CURRENT in B
        b_with_a: intersect_by_level_class(&del_b, &cur_a),
    })
}

fn content_image(m5: &M5State, d: &Address) -> SpanSet {               // ran_C(d); mixed-length (transcluded origins)
    m5.content_runs(d).iter().fold(SpanSet::empty(), |s, r| union(&s, &SpanSet::singleton(r.iextent())))
}

/// M6 owns the level-class discipline HERE (it intersects two raw mixed-length covers itself, unlike
/// FINDDOCSCONTAINING where M5 partitions internally). Cross-length spans never intersect (disjoint
/// document prefixes), so grouping by #start and intersecting matching classes is exact and dodges M1's
/// LevelMismatch.
fn intersect_by_level_class(a: &SpanSet, b: &SpanSet) -> SpanSet {
    let (ga, gb) = (group_by_start_len(a), group_by_start_len(b));     // BTreeMap<usize, SpanSet>
    ga.iter().filter_map(|(len, sa)| gb.get(len).map(|sb| intersect_sets(sa, sb).unwrap()))
             .fold(SpanSet::empty(), |s, part| union(&s, &part))
}
```

- **Output is I-coverage**, the compact span form the digest recommends, feeding an identity-preserving restore (the addresses *are* the existing I-addresses, D-IDENT).
- **The torn-read hazard is gone:** all of `deletions`/`content_runs` read off one `&M5State` from one snapshot, so `(M, R)` is a single boundary — the digest's "R-ahead-of-M phantom deletion" cannot occur (M2 commits composites atomically).

### COMPARE — interval equi-join on I-address, complete under fan-out

The contract is a relational join keyed on **address equality, never value** — so COMPARE **never opens M4**. Three phases: resolve regions to blocks, interval-join on the I-axis with cross-product on overlap, coalesce-and-canonicalize.

```rust
pub fn compare(&self, rho1: &[Spec], rho2: &[Spec]) -> Result<CompareReport, CompareError> {
    let (m3, m5) = (self.0.world().m3(), self.0.world().m5());
    for (i, s) in rho1.iter().chain(rho2).enumerate() {
        if !require_registered(m3, &s.doc) { return Err(CompareError::DocNotRegistered(s.doc.clone())); }
        if *s.span.start().get(1) != S_C  { return Err(CompareError::NotContentSubspace); }   // start in content subspace
        gate_vspec(&s.span).map_err(|f| CompareError::MalformedSpan { index: i, fault: f })?;
    }
    let (p, q) = (resolve_blocks(m5, rho1), resolve_blocks(m5, rho2));   // Vec<Block>; reads ONLY M5
    let pairs  = interval_join(&p, &q);                                  // cross-product per overlap (X8 completeness)
    Ok(CompareReport(canonicalize(pairs)))                              // maximal succ-runs, lex order (X11)
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
        d1: pb.doc.clone(), u1: vpos_shift(&pb.v_start, &ordinal_gap(&lo, &pb.i_start)),  // slot 1 ⇐ operand 1 (X3)
        d2: qb.doc.clone(), u2: vpos_shift(&qb.v_start, &ordinal_gap(&lo, &qb.i_start)),
        width: w,
    })
}
```

- **Reconstructing V-positions** from `resolve`'s `Vec<Run>` relies on content arrangements being **gap-free** (D-CTG★): the first run starts at the span start and runs tile the bound prefix contiguously in V, so `v_start` accumulates by width. (If M5 ever returned V-gapped content runs — it must not — COMPARE would need per-position resolution via `point` or a richer run type; flagged as an assumption.)
- **Fan-out completeness is the whole game** (the place the reference implementation is wrong): when an address occurs in multiple P-blocks and/or Q-blocks, `interval_join` must emit the **full cross-product** over each I-overlap, not a lockstep merge. The recommended structure is sort-by-`i_start` + sweep (or interval tree); the O(|P|·|Q|) double loop is the simplicity oracle. Either consumes blocks directly and reads only addresses (never bytes) — simultaneously the correctness property (value-matching over-reports) and the perf property (no content fault).
- **`canonicalize`** merges succ-adjacent pairs (both feet advance by one, addresses contiguous) into maximal runs, then sorts lexicographically by `(d1, u1, d2, u2)` — the determinism contract R3/X11. The second-foot tie-break is load-bearing under fan-out.

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
        .filter(|d| !m5.project(d, &coverage).is_empty())              // present-tense soundness filter (FD-SOUND) — one project/candidate
        .collect())
}
```

- **The filter is the only difference between the live answer and the historical "ever-contained" answer** (`docs_containing` alone) — exactly the step the reference omits. `project(d, coverage)` is an I→V lookup, not a re-search; cost is proportional to the candidate set.
- `resolve_coverage` returns raw, possibly mixed-length covers; `docs_containing`/`project` apply the level-class discipline **internally** (M5 contract), so M6 passes the raw union straight through — the level-class helper is needed only in SHOWDELETIONS.
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
- *SHOWORIGIN_V admissibility* — reject empty document and unbound-range spans (the `resolved < nominal` test), never clamp. (WF_V(iii,vi)/O13 0077.)
- *Completeness under fan-out; deterministic canonical order* — cross-product `interval_join` + `canonicalize`. (X8/R2/R3/X11 0122.)
- *Present-tense soundness filter* — `project`-narrowing of `docs_containing`. (FD-SOUND 0124.)
- *Level-class discipline on cross-document intersection* — `intersect_by_level_class` partitions before intersecting (SHOWDELETIONS only). (M5 interface contract.)

**Delegated (M6 relies on, does not enforce):** contiguity D-CTG★ and referential integrity S3★ (M5 write path); R permanence/monotonicity and the J-couplings (M5/M2); durability/recovery (M2). M6 trusts these and panics (not silently skips) if S3★ is observed broken on the content side.

## Dependencies & seams

**Upstream calls (concrete):**
- **M1** — `document_of` (origin projection, SHOWORIGIN); `shift`/`shift_ordinal`+`ElemPos`/`elem_addr` (run-address enumeration, V-cursor advance); `sub`/`from_endpoints`/`Span::new` (extent synthesis); `action_point`/`zeros`/`Tumbler::get`/`is_level_uniform` (gates); `union`/`intersect_sets`/`SpanSet::singleton`/`empty` and tumbler `Ord` (set algebra, COMPARE overlaps, dedup ordering); `Run::iextent` (content-image lift).
- **M2** — `snapshot()` (one per logical query; M10 takes it), `Snapshot::world()`/`seq()`. No `transact`, no `Kernel` — M6 never writes.
- **M3** — `is_registered_document` (the universal allocation gate). Not `effective_owner` (authorization is M10's; SHOWORIGIN reports origin *documents*, not owners).
- **M4** — `value_at` (RETRIEVEV content only). `contains` available as a defensive S3★ check but not needed (M5 guarantees it). Never touched by COMPARE/extent/containment/deletions.
- **M5** — the workhorse: `resolve` (RETRIEVEV, SHOWORIGIN_V, COMPARE), `resolve_coverage` (FINDDOCSCONTAINING phase 1), `content_runs` (SHOWDELETIONS content-image, COMPARE), `content_count`/`link_count` (extent queries, SHOWORIGIN_V subspace gate), `project` (FINDDOCSCONTAINING filter), `deletions` (SHOWDELETIONS), `docs_containing` (FINDDOCSCONTAINING phase 2), optionally `ever_placed` (D-DISJ short-circuit).

**Downstream seam (what M6 exposes — only M10 consumes it):** the seven read methods on `Query<'s, W>`. The contract M10 codes against: take a snapshot, build a `Query`, call the op, **marshal the returned value, and surface any `Err(_)` as a typed rejection** (these are precondition/well-formedness failures, never silent skips); a registered-empty document yields the operation's empty form (`⟨⟩`/empty `Delivery`/empty halves/`[]`), an unallocated one yields the op's `*NotRegistered` error. M6 returns by value and never commits, so there is no commit-before-acknowledge step for reads.

**Engine assembly:** M6 contributes **no slice, no record variant, no accessor trait, no fold** — it is a pure consumer of `HasM3 + HasContent + HasM5`. Nothing in the engine's `World`/`Record` comes from M6, and no `apply`/`rebuild_derived` obligation attaches to it. (It therefore trivially satisfies the composition contract by being generic over `W` and naming no concrete `World`/`Record`.)

## Conflicts resolved

1. **Where the R indexes live (the biggest scope narrowing).** The decomposition lists M6 as owning the "reverse-index hint over R" and implies M6 computes the deletion set-algebra. M5's *as-built interface* instead exposes `docs_containing`, `deletions`, and `ever_placed` as **M5 methods**, co-locating the R index with R's authoritative state (Lampson: a hint belongs with the store that recomputes it on replay — only M5 folds R). **Resolution:** M6 owns **no index**. SHOWDELETIONS contributes only the cross-document intersection + level-class discipline; FINDDOCSCONTAINING contributes only the phase-1 union + the present-tense `project` filter. Putting either index in stateless M6 would be authoritative duplicate state M6 cannot recover. I honor the M5 interface.

2. **SHOWORIGIN_I has no enumeration seam.** The operation needs allocated content addresses in an I-interval, but M4 is point-only with `Ord` *deliberately* unused (no range scan) and M3 exposes no frontier/range query. **Resolution:** SHOWORIGIN_V is fully built; **SHOWORIGIN_I is deferred behind a named upstream seam** that, by Lampson, belongs in **M4** — a recomputable I-ordered content index over M4's append-only writes (rebuilt by replay, exposed as e.g. `allocated_content_in(span)`). M6 must *not* grow its own I-range index (it has no fold hook and owns no state). Until that seam exists, `show_origin_i` returns `ISpanIndexUnavailable`. Adding it to M4 is the recommended path; scoping the I-arity out entirely is the cheaper alternative (the digest notes the V-arity is the reader-facing one).

3. **`m_S(d)` depth hint collapses to a constant.** ASN-0115/0112/0113 all weigh caching vs. recomputing the per-subspace common depth `m_S(d)`. **Resolution:** M5 fixes V-positions at depth 2, so `m_S(d) ≡ 2`; the depth-compatibility test is the static `#start == 2`, which M5's defensive `resolve` already enforces. No hint, no per-document scalar.

4. **RETRIEVEDOCVSPAN: count-read vs. confluent summary, and the negative-origin hazard (0112 OQ5).** The note offers a min/max read or a maintained summary tree whose relative displacement can drive the **origin negative** (violating S8a). **Resolution:** M6 synthesizes from M5's authoritative `content_count`/`link_count`, reading `min` as the subspace anchor `[s,1]` — never negative. The hazard is exclusive to the summary-tree path and is designed out. (This also resolves "trust counts vs. scan": trust M5's counts; D-CTG★ is M5's write-path obligation; debug-assert optionally.)

5. **Byte-clipping / run-coalescing / width≠count (0115).** The digest's elaborate boundary-clipping presumes a byte-granular store. **Resolution:** M4 stores opaque `Val`s keyed per address and M5's arrangement is per-address, so M6 delivers **one item per active V-position** — exact, no dedup, no byte clip. "Never coalesce across a gap" is satisfied trivially by per-position delivery (and remains safe if a builder chooses segment/streaming delivery, since M5's runs are gap-aligned). Byte-boundary semantics are a property of how content was chunked into `Val`s *below* M6.

6. **0112 vs. 0113 overlap.** Both are "document extent." **Resolution:** complementary, not conflicting — they share the same count-read core; `doc_vspan` is the whole-document bounding span (a bounding box across subspaces), `doc_vspanset` is the per-subspace exact span-set. Fragmentation-sensitive callers use the latter; M10 routes accordingly.

7. **SHOWORIGIN vs. FINDDOCSCONTAINING (a distinction to *preserve*, not a conflict).** SHOWORIGIN reports the **original allocator** (`document_of`), FINDDOCSCONTAINING the **current holders** (R⁻¹ filtered to present). Different questions; M6 keeps them on different machinery (M1 projection vs. M5's R index + filter) so neither is mistaken for the other.

## Open build decisions

- **COMPARE matcher structure.** Sort-by-`i_start` + sweep (or interval tree) for the cross-product join — the production default, consumes M5's blocks directly — vs. a per-position hash join on address (obviously fan-out-complete; the simplicity oracle to validate against). Pick the block interval join; keep the hash join as the test oracle.
- **RETRIEVEV delivery shape.** Per-position items (chosen default — exact, simplest) vs. coalesced gap-aligned segments vs. lazy streaming for large spec-sets. If streaming, decide how back-pressure interacts with partial-delivery (a stream still "succeeds" while emitting nothing for gaps), and whether `DeliveryItem::Content` borrows through the snapshot (zero-copy) instead of cloning the `Arc`.
- **Snapshot ownership.** M6 methods take `&Snapshot` so M10 controls the consistency scope (recommended); a convenience that snapshots per call is possible but couples M6 to `&Kernel`.
- **Extent contiguity check.** Trust `content_count`/`link_count` (O(1)) vs. debug-build cross-check against `content_runs` (catches a broken D-CTG★ from upstream). Trust in release, assert in debug.
- **SHOWDELETIONS D-DISJ short-circuit.** Pre-check level-class disjointness of `ever_placed(d_A)`/`ever_placed(d_B)` to rule out unrelated documents before reading arrangements — worth it under unrelated-pair workloads.
- **SHOWORIGIN_I.** Add the M4 I-ordered content index seam and build the boundary-walk + single-origin fast path, or scope the I-arity out and ship only the V-arity.
- **COMPARE link-start spans.** Reject loudly (recommended — `NotContentSubspace`) vs. leniently strip via a content-subspace front-filter. (Spans that merely *denote* link positions from a content start are always legal — `resolve` clips them — so this is only about a span whose *start* is in the link subspace.)
- **Result caching.** Recompute by default (cheap, local, lock-free). If COMPARE/SHOWDELETIONS profile hot, memoize as a *hint* keyed on `(Snapshot::seq, args)` — and for any RETRIEVEV delivery cache, key on the consulted *restriction* (`M(d)|⟦σ⟧`), never on output byte-identity (R7 is sufficiency, not biconditional). Never authoritative; always recompute on a miss.
- **FINDDOCSCONTAINING resolve timing.** Re-resolve per query (tracks present-tense drift) vs. cache the frozen resolved I-coverage at an earlier snapshot for stable "find more like this" (legitimate because content is permanently grounded). Different products want different answers; expose the choice at M10.
