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
pub struct Deletions { pub a_with_b: Vec<Address>, pub b_with_a: Vec<Address> }  // deleted-from-one ∧ current-in-other; the existing I-addresses (D-IDENT), deduped + Tumbler-ordered (D-ORD)

pub struct CorrPair { pub d1: Address, pub u1: VPos, pub d2: Address, pub u2: VPos, pub width: Nat }
pub struct CompareReport(pub Vec<CorrPair>);   // canonical order; slot i drawn from operand i

impl<'s, W: M6World> Query<'s, W> {
    /// SHOWDELETIONS (ASN-0075). Both documents must be registered (Err otherwise; allocated-empty is
    /// fine and yields empty halves). Each half is the deduped, Tumbler-ordered set of I-addresses
    /// deleted-from-one yet current-in-the-other — the existing I-addresses themselves (D-IDENT),
    /// never copies. Composed in M6 from M5's per-document `deletions`/`content_runs`; opens M4 for
    /// nothing. See the SHOWDELETIONS section.
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
pub enum SpecFault { NotOrdinalLevel, NotLevelUniform, StartNotZeroFree, StartNotDepth2 }
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
   - COMPARE's `Block { doc: Address, v_start: Tumbler, i_start: Address, width: Nat }` lists for P and Q, plus the intermediate `Vec<CorrPair>` before canonicalization; SHOWDELETIONS's enumerated `arranged_content(d)` address lists.
   - Dedup sets for origins, containers, and the two SHOWDELETIONS halves (`HashSet<Tumbler>` → sorted `Vec<Address>`, since `Address` is `Eq+Hash` but not `Ord`; `Tumbler` carries the `Ord`).

**Authoritative vs. recomputable, resolved explicitly for M6:** there is nothing to distinguish, because M6 holds neither. Three would-be hints all resolve away from M6:
- the **R reverse index** (`docs_containing`, FINDDOCSCONTAINING) belongs in M5, co-located with R's authoritative state (recomputable by replay only where R is folded), and is in M5's interface today; SHOWDELETIONS's **cross-document deletion comparison** stores nothing at all — it is a pure per-query read M6 composes from M5's *per-document* `deletions`/`content_runs` (membership-tested, no index, no fold);
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
    if span.start().len() != 2                                { return Err(SpecFault::StartNotDepth2); }    // m_S ≡ 2: depth-2 is the EXACT admissible V-position depth
    Ok(())
}

/// k-th address of a run. LOAD-BEARING ASSUMPTION (used directly here by RETRIEVEV and SHOWDELETIONS,
/// and mirrored by the element-level I-address arithmetic in SHOWORIGIN_V and COMPARE): every
/// content/link I-address has a 2-COMPONENT element field [subspace, ordinal] (zeros = 3), as M3 mints
/// them. `ElemPos` models exactly that 2-component field, so reconstructing i_start as
/// ElemPos{ doc, subspace, ordinal } and advancing the ordinal is faithful and dodges the raw-shift
/// subspace-crossing footgun — but a LONGER element field would be silently truncated here.
fn run_addr(i_start: &Address, k: &Nat) -> Address {
    let p = ElemPos { doc: document_of(i_start).unwrap(), subspace: i_start.subspace().unwrap(),
                      ordinal: ordinal(i_start.tumbler()).clone() };
    elem_addr(&shift_ordinal(&p, k)).unwrap()
}

fn dedup_docs(it: impl Iterator<Item = Address>) -> Vec<Address> { /* HashSet<Tumbler> → sort by Tumbler */ }

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
    // Gate the whole request first — well-formedness is the only in-model failure (ASN-0115).
    for (i, s) in specs.iter().enumerate() {
        if !require_registered(m3, &s.doc) { return Err(RetrieveError::DocNotRegistered(s.doc.clone())); }
        gate_vspec(&s.span).map_err(|f| RetrieveError::MalformedSpec { index: i, fault: f })?;
    }
    let mut out = Vec::new();
    for s in specs {                                   // concatenate per spec, IN ORDER (R5) — no global sort
        let sub = s.span.start().get(1).clone();       // 1=content, 2=link (gate_vspec ⇒ #start == 2, zero-free)
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
- **Gaps / depth-incompat / foreign subspaces** all funnel through M5's defensive `resolve` returning fewer-or-zero runs → silent empty contribution; the request still succeeds (R6). The `m_S ≡ 2` simplification means depth-incompatibility *is* `#start ≠ 2`, which `resolve` already force-empties (and `gate_vspec` now rejects up front). A start subspace ∉ {1,2} is likewise force-empted upstream (M5 holds no such positions), so the closed `else` arm is unreachable while a run exists — its `debug_assert` records that as intent.
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
- **The nominal count is read via `ordinal(span.width())`** (the last component), not a hard-coded `width.get(2)`. `gate_vspec` now pins `#start == 2`, rejecting every non-depth-2 span *at the gate* as `MalformedSpan(StartNotDepth2)`; level-uniformity then forces `#width == 2`, so this read *is* `width.get(2)`. Reading it positionally via `ordinal` keeps it free of a hard-coded index and consistent with the gate — there is no depth-3 span left to slip through and mis-read a `0` at index 2, and `RangeNotPresent` is now reserved for genuinely unbound positions (no longer misattributed to depth).
- For the link subspace, `document_of(link)` is the home `doc` (CL-OWN) — handled uniformly, no special case.

### SHOWORIGIN_I — de-scoped (ruling)

`origins_I(σ) = {document_of(a) : a ∈ ⟦σ⟧ ∩ dom(C)}` requires enumerating allocated content addresses across an I-interval. No upstream surface provides this: M4 is point-only with `Ord` **deliberately** unused and its boundary forbidding range/prefix scans, and M3's registry is point-only (`is_allocated`). Stateless M6 has no fold hook to grow its own index. The I-arity is therefore **de-scoped from M6 and recorded as a decomposition amendment** — were it ever needed, it belongs to a *new* I-ordered content index (a recomputable hint over M4's append-only writes, e.g. `allocated_content_in(span)`), which is a change to the module decomposition, not an M6 internal. Only `show_origin_v` ships, and `OriginError` carries no `ISpanIndexUnavailable` placeholder; the prior `show_origin_i` placeholder is removed.

Two flags travel with the ruling so it does not silently diverge from the system docs:
- **Preferring the V-arity is M6's call, not ASN-0077's.** The note designates *neither* arity "reader-facing"; M6 rules the V-arity the one it ships.
- **The de-scope is settled, not conditional.** It is settled **by construction**: M10 can marshal only what M6's `Query` exposes, and that is `show_origin_v` alone — there is no I-arity method *anywhere* for the FEBE surface to reach (the I-arity would need the forbidden M4 index, which no module provides). The client surface therefore promises no SHOWORIGIN-over-I. (Corroborated by M10's enumerated reader-marshaling sources — ASN-0111/0112/0113/0114/0115/0121/0122/0124/0131/0132 — which list no SHOWORIGIN-over-I command.) The recorded amendment stands as future work (the new I-ordered index is where the I-arity would land *if* ever surfaced), not a live capability hole.

### SHOWDELETIONS — gate, then membership-test the cross-document combine in M6

`DeletedFromAWithB = {a ∈ dom(C) : DELETED(a, d_A) ∧ CURRENT(a, d_B)}` and its symmetric twin are a **cross-document** filter: the addresses *current in one* document that are *deleted from the other*. Read as a **membership test** rather than a set intersection, it builds directly on the upstream interfaces *as given* — no M5 amendment:

> `a_with_b = { a ∈ content_image(d_B) : DELETED(a, d_A) }`

- enumerate `content_image(d_B)` exactly as RETRIEVEV enumerates content — `m5.content_runs(d_b)` per-position through `run_addr` (this *is* CURRENT(·, d_B) for content addresses, by definition of `ran`; realized by the `arranged_content` helper);
- test `DELETED(a, d_A)` by membership in M5's per-document deleted cover: `m5.deletions(d_a).denotes(a.tumbler())`. `deletions(d) = ever_placed(d) ∖ content_image(d) = { a : DELETED(a, d) }` (M5 computes it per level-class, fault-free); `denotes` (M1) faults on nothing and is **exact** on real content addresses — no content address is a strict prefix of another (each is an element-level `zeros=3` tumbler `doc·0·s·ord` under a distinct `zeros=2` origin document), so the cover denotes exactly its address set with no subtree phantom;
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
    let a_with_b = dedup_docs(arranged_content(m5, d_b).into_iter()
        .filter(|a| del_a.denotes(a.tumbler())));
    let b_with_a = dedup_docs(arranged_content(m5, d_a).into_iter()
        .filter(|a| del_b.denotes(a.tumbler())));
    Ok(Deletions { a_with_b, b_with_a })
}
```

- **Output is address sets** — each half is the deduped, Tumbler-ordered `Vec<Address>` of the *existing* I-addresses (D-IDENT: "the returned reference is precisely the I-address `a`," never a copy; D-ORD: T1-orderable). No SpanSet re-encoding, so no exactness/lossless caveat applies.
- **No M4 access** — DELETED/CURRENT are arrangement + R facts; bytes are never fetched. Both documents registered-but-empty ⇒ `deletions` and `content_runs` both empty ⇒ empty halves.
- **`denotes` exactness, with a fallback.** Testing `denotes(a)` recovers membership exactly because content I-addresses are prefix-free (above). If M5's cover should ever *coalesce* spans (admitting an interval phantom between two real deleted addresses), the **exactness-independent** test `DELETED(a, d_A) ≡ ever_placed(d_a).denotes(a) ∧ a ∉ arranged_content(d_a)` uses only `ever_placed` (raw, unit-cover) + `content_runs` — both M5 as given. v1 uses the `deletions` form on M5's stated fault-free, read-straight-off seam.
- **Single consistent `(M, R)`** — every read is off the one bound `&Snapshot`; M2 commits composites atomically, so the digest's "R-ahead-of-M phantom deletion" cannot arise (no torn read).
- **D-DISJ guard (optional, M6-local)** — when `deletions(d_a)` is empty, `a_with_b` is empty without enumerating `arranged_content(d_b)` (symmetrically for `b_with_a`): a cheap sufficient case of D-DISJ's R-disjointness, folded into M6 since the combine now lives here.

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
    // (R4 optional). Sort lexicographically by (d1, u1, d2, u2); the adjacent-pair fold is the
    // IDENTITY in v1 (a finer-than-maximal, per-overlap report conforms — see `fold_adjacent`).
    pairs.sort_by(|x, y| corr_key(x).cmp(&corr_key(y)));
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
- **V-reconstruction lemma (load-bearing for X12-R1 soundness).** `resolve_blocks` sets the first run's `v_start = span.start()` and accumulates `v_start` by each run's width. This is correct **only because content is gap-free** (D-CTG★): the first bound V-position of a content span *is* `span.start()`, and `resolve`'s runs tile the bound prefix contiguously in V, so there are no V-gaps to skip. The code states this as the lemma it is and **`debug_assert`s it** (`M(d)(span.start()) == first_run.i_start`, via `m5.point`), so a future M5 regression to V-gapped content runs fails loudly rather than silently mis-aligning `u1`/`u2` (it would then need per-position `point` resolution or a V-carrying run type).
- **Fan-out completeness is the whole game** (the place a naïve implementation goes wrong): when an address occurs in multiple P-blocks and/or Q-blocks, `interval_join` must emit the **full cross-product** over each I-overlap, not a lockstep merge. The recommended structure is sort-by-`i_start` + sweep (or interval tree); the O(|P|·|Q|) double loop is the simplicity oracle. Either consumes blocks directly and reads only addresses (never bytes) — simultaneously the correctness property (value-matching over-reports) and the perf property (no content fault).
- **Overlapping windows within one operand are redundant, not wrong.** ASN-0122 X12 permits a spec-set to name overlapping (or repeated) windows; `resolve_blocks` then double-covers the shared V-positions, and `interval_join` emits the overlap pair more than once. This is **denotationally conforming** — `⟦Γ⟧` is a set-union, so duplicates collapse in the denotation (R1/R2 hold), and the *stable* `sort_by` in `canonicalize` keeps the listed order deterministic (R3) regardless of duplicate count. A builder may pre-dedupe each operand's regions to shrink the cross-product; correctness does not require it.
- **`canonicalize`** sorts the pairs lexicographically by `(d1, u1, d2, u2)`, then applies `fold_adjacent`. This is a **deterministic** presentation (X12 R3) of the **complete and sound** relation (R1/R2); it is **not** claimed to be the X11 **maximal** form — X12 **R4 (maximal pairs) is explicitly not required for conformance**. In v1 `fold_adjacent` is the **identity** (a finer-than-maximal, per-overlap report fully conforms under R1–R3); a builder wanting maximal output merges feet-successor-adjacent pairs (pair₂'s feet are the unit-successors of pair₁'s last positions *and* their I-addresses are consecutive) into one wider pair — a pure presentation post-pass that never changes `⟦Γ⟧`. The second-foot tie-break in the sort key is load-bearing under fan-out.

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
- *Deletion sets are the existing I-addresses* — SHOWDELETIONS returns the addresses themselves, never copies, T1-orderable. (D-IDENT/D-ORD 0075.)
- *Two-kinds-only, disjoint, pre-normalized extents* — fixed two-subspace iteration. (W9/W11/W13 0113.)

**By active enforcement** (M6 must guard, with the site named):
- *Well-formedness gates → typed rejection* — `gate_vspec` + `require_registered` at each operation's entry; the only in-model failures. The depth check is `#start == 2` (the exact admissible depth under `m_S ≡ 2`), so a non-depth-2 span is rejected uniformly at the gate as `StartNotDepth2` across RETRIEVEV / SHOWORIGIN_V / COMPARE. (0115 well-formedness; WF_V 0077; W-pre 0112/0113; precondition 0122.)
- *Registered-empty → result vs. unallocated → fail* — **M6's owned distinction**, via `m3.is_registered_document`, applied per-operation (and tightened for SHOWORIGIN_V, which also rejects an empty *subspace*). (Decomposition; W-pre 0113; WF_V(iii) 0077.)
- *Single-subspace at the gate* — the ordinal-level check in `gate_vspec` makes a straddle unrepresentable for RETRIEVEV. (R10 0115.)
- *Partial-delivery never fails* — gaps/depth-incompat/foreign-subspace become empty contributions, never errors. (R6 0115.)
- *SHOWORIGIN_V admissibility* — reject empty document and unbound-range spans (the depth-agnostic `resolved < ordinal(width)` test), never clamp. (WF_V(iii,vi)/O13 0077.)
- *SHOWDELETIONS cross-document combine* — `arranged_content(d_X)` filtered by `deletions(d_Y).denotes(·)`, both halves off one snapshot. (DeletedFromAWithB/BWithA 0075.)
- *Completeness under fan-out; deterministic canonical order* — cross-product `interval_join` + `canonicalize`. (X8/R1/R2/R3 0122; X11 maximal / R4 not required.)
- *Present-tense soundness filter* — `project`-narrowing of `docs_containing`. (FD-SOUND 0124.)

**Delegated (M6 relies on, does not enforce):** contiguity D-CTG★ and referential integrity S3★ (M5 write path); R permanence/monotonicity, the J-couplings, the **level-class discipline on every coverage set-op**, the R⁻¹ index `docs_containing`, and the per-document `deletions`/`content_runs` covers from which M6 composes the cross-document SHOWDELETIONS combine (M5); durability/recovery (M2). M6 trusts these and panics (not silently skips) if S3★ is observed broken on the content side. Every primitive M6 calls is in M1–M5's interface as given — no upstream amendment is required.

## Dependencies & seams

**Upstream calls (concrete):**
- **M1** — `document_of` (origin projection, SHOWORIGIN_V; I-address → origin Document in `run_addr`); `shift`/`shift_ordinal`+`ElemPos`/`elem_addr` (run-address enumeration, V-cursor advance, COMPARE `reach_i`); `from_endpoints`/`Span::new` (extent synthesis); `action_point`/`zeros`/`ordinal`/`Tumbler::get`/`Tumbler::new`/`is_level_uniform` (gates, the depth-agnostic count read, COMPARE ordinal arithmetic); `union`/`SpanSet::singleton`/`SpanSet::empty`/`SpanSet::is_normalized`/`SpanSet::denotes`/`SpanSet` `PartialEq` and tumbler `Ord` (set algebra, COMPARE overlaps, the FINDDOCSCONTAINING filter test, the **SHOWDELETIONS membership test**, dedup ordering, normal-form assert).
- **M2** — `snapshot()` (one per logical query; M10 takes it), `Snapshot::world()`/`seq()`. No `transact`, no `Kernel` — M6 never writes.
- **M3** — `is_registered_document` (the universal allocation gate). Not `effective_owner` (authorization is M10's; SHOWORIGIN reports origin *documents*, not owners).
- **M4** — `value_at` (RETRIEVEV content only). `contains` available as a defensive S3★ check but not needed (M5 guarantees it). Never touched by COMPARE/extent/containment/deletions.
- **M5** — the workhorse: `resolve` (RETRIEVEV, SHOWORIGIN_V, COMPARE), `resolve_coverage` (FINDDOCSCONTAINING phase 1), `content_count`/`link_count` (extent queries, SHOWORIGIN_V subspace gate), `point` (COMPARE's debug-assert of the V-reconstruction lemma), `project` (FINDDOCSCONTAINING present-tense filter), `docs_containing` (FINDDOCSCONTAINING phase 2), `content_runs` + `deletions` (SHOWDELETIONS: enumerate `content_image` and membership-test the per-document deleted cover; `ever_placed` is the exactness-independent fallback). All of these are in M5's interface **as given** — no amendment.

**Downstream seam (what M6 exposes — only M10 consumes it):** the seven read methods on `Query<'s, W>`. The contract M10 codes against: take a snapshot, build a `Query`, call the op, **marshal the returned value, and surface any `Err(_)` as a typed rejection** (these are precondition/well-formedness failures, never silent skips); a registered-empty document yields the operation's empty form (`⟨⟩`/empty `Delivery`/empty halves/`[]`), an unallocated one yields the op's `*NotRegistered` error. M6 returns by value and never commits, so there is no commit-before-acknowledge step for reads. All seven operations ship against the upstream interfaces as given; M10's reader surface carries no SHOWORIGIN-over-I (it cannot — M6 exposes only the V-arity), so the V-arity-only origin path is settled (Conflicts resolved 2).

**Engine assembly:** M6 contributes **no slice, no record variant, no accessor trait, no fold** — it is a pure consumer of `HasM3 + HasContent + HasM5`. Nothing in the engine's `World`/`Record` comes from M6, and no `apply`/`rebuild_derived` obligation attaches to it. (It therefore trivially satisfies the composition contract by being generic over `W` and naming no concrete `World`/`Record`.)

## Conflicts resolved

1. **Where the R index and coverage set-ops live; how the SHOWDELETIONS combine is built.** The decomposition lists M6 as owning the "reverse-index hint over R" and "deletion classification (SHOWDELETIONS)." M5's *as-built interface* exposes `docs_containing`, `deletions`, and `ever_placed` as **M5 methods**, co-locating the R index with R's authoritative state (Lampson: a hint belongs with the store that recomputes it on replay — only M5 folds R). **Resolution:** M6 owns **no index and no coverage set-op**. FINDDOCSCONTAINING contributes only the phase-1 resolve-union and the present-tense `project` filter over M5's `docs_containing` superset. SHOWDELETIONS's cross-document `DELETED(·,d_A) ∧ CURRENT(·,d_B)` is a **pure per-query read** M6 composes from M5's *per-document* primitives — `content_runs(d_B)` enumerates CURRENT(·,d_B), and `deletions(d_A).denotes(a)` (with M1's `denotes`) tests DELETED(·,d_A) by **membership**, not set intersection. This sidesteps the two dead ends the design must reject: the SpanSet-*intersection* route faults (`intersect_sets`/`normalize` choke on mixed-length covers), and the in-M6-*authoritative-state* route is misplaced (stateless M6 cannot recover a fold). Membership-testing needs neither — `denotes` faults on nothing and is exact on prefix-free content addresses — so the combine lives where the decomposition puts it (M6), on the seam M5 already advertises (`deletions`: "SHOWDELETIONS primitive… **M6 reads it straight off**"). **No M5 amendment is required; all seven operations build against the interfaces as given.**

2. **SHOWORIGIN_I de-scoped — a settled decomposition amendment.** `origins_I(σ) = {document_of(a) : a ∈ ⟦σ⟧ ∩ dom(C)}` needs an *enumeration of allocated content addresses across an I-interval*. M4 is point-only with `Ord` **deliberately** unused (its boundary forbids range/prefix/ordered scans) and M3 is point-only (`is_allocated`); neither exposes — and M4 by its stated design *excludes* — the I-ordered index this arity requires. Adding such a scan to M4 would itself be an upstream-overreach defect, and stateless M6 (no slice, no fold hook) cannot grow its own index. **Resolution:** M6 ships `show_origin_v` only. The I-arity is **de-scoped to a recorded decomposition amendment** — it belongs to a *new* I-ordered content index (a recomputable hint over M4's append-only writes, e.g. `allocated_content_in(span)`), a change to the module decomposition, not an M6 internal. Two caveats made explicit: (i) ASN-0077 designates *neither* arity "reader-facing" — preferring the V-arity is **M6's ruling**, not the note's; (ii) the de-scope is **settled by construction** — M10 can marshal only what M6's `Query` exposes (`show_origin_v` alone), so no I-arity surface exists for the FEBE layer to reach (corroborated by M10's enumerated reader sources, which list no SHOWORIGIN-over-I). The amendment is future work, not a live capability hole. The prior `show_origin_i`/`ISpanIndexUnavailable` placeholders are removed.

3. **`m_S(d)` depth hint collapses to a constant.** ASN-0115/0112/0113 all weigh caching vs. recomputing the per-subspace common depth `m_S(d)`. **Resolution:** M5 fixes V-positions at depth 2, so `m_S(d) ≡ 2`; the depth-compatibility test is the static `#start == 2`, which both `gate_vspec` (rejecting `#start != 2` as `StartNotDepth2`) and M5's defensive `resolve` enforce. No hint, no per-document scalar.

4. **RETRIEVEDOCVSPAN: count-read vs. confluent summary, and the negative-origin hazard (0112 OQ5).** The note offers a min/max read or a maintained summary tree whose relative displacement can drive the **origin negative** (violating S8a). **Resolution:** M6 synthesizes from M5's authoritative `content_count`/`link_count`, reading `min` as the subspace anchor `[s,1]` — never negative. The hazard is exclusive to the summary-tree path and is designed out. (This also resolves "trust counts vs. scan": trust M5's counts; D-CTG★ is M5's write-path obligation; debug-assert optionally.)

5. **Byte-clipping / run-coalescing / width≠count (0115).** The digest's elaborate boundary-clipping presumes a byte-granular store. **Resolution:** M4 stores opaque `Val`s keyed per address and M5's arrangement is per-address, so M6 delivers **one item per active V-position** — exact, no dedup, no byte clip. "Never coalesce across a gap" is satisfied trivially by per-position delivery (and remains safe if a builder chooses segment/streaming delivery, since M5's runs are gap-aligned). Byte-boundary semantics are a property of how content was chunked into `Val`s *below* M6.

6. **0112 vs. 0113 overlap.** Both are "document extent." **Resolution:** complementary, not conflicting — they share the same count-read core; `doc_vspan` is the whole-document bounding span (a bounding box across subspaces), `doc_vspanset` is the per-subspace exact span-set. Fragmentation-sensitive callers use the latter; M10 routes accordingly.

7. **SHOWORIGIN vs. FINDDOCSCONTAINING (a distinction to *preserve*, not a conflict).** SHOWORIGIN reports the **original allocator** (`document_of`), FINDDOCSCONTAINING the **current holders** (R⁻¹ filtered to present). Different questions; M6 keeps them on different machinery (M1 projection vs. M5's R index + filter) so neither is mistaken for the other.

8. **`gate_vspec`'s ordinal-level requirement is an upstream-forced narrowing, recorded deliberately.** ASN-0077 WF_V(iv) requires only `actionPoint(ℓ) ≤ #u`, and ASN-0122 X12 requires only T12-well-formedness + a content-subspace start — *not* strict ordinal-level. M6 nonetheless gates all three resolve-based ops (RETRIEVEV, SHOWORIGIN_V, COMPARE) to **ordinal-level, depth-2** spans. **Resolution:** the narrowing is forced by M5's `resolve`, which is defensive and yields ⟨⟩ for any span that is not `#start == 2 ∧ #width == 2 ∧ width.get(1) == 0` (ordinal-level depth-2). A non-ordinal-level (or non-depth-2) span would therefore resolve to nothing upstream regardless, and every selection these notes name is expressible as an ordinal-level depth-2 span in the `m_S ≡ 2` model — so gating up front turns a silent upstream empty into an explicit, typed rejection (`MalformedSpec`/`MalformedSpan`) without losing any admissible query. Recorded here as a deliberate, M5-driven restriction rather than an implicit one.

## Open build decisions

- **COMPARE matcher structure.** Sort-by-`i_start` + sweep (or interval tree) for the cross-product join — the production default, consumes M5's blocks directly — vs. a per-position hash join on address (obviously fan-out-complete; the simplicity oracle to validate against). Pick the block interval join; keep the hash join as the test oracle.
- **COMPARE maximal output.** Ship `fold_adjacent` as the identity (per-overlap, finer-than-maximal — fully conforming, R4 not required) vs. the feet-successor-adjacency merge for literal X11 maximal pairs. Default to identity; add the merge only if a consumer demands maximal form (it changes presentation, never `⟦Γ⟧`).
- **RETRIEVEV delivery shape.** Per-position items (chosen default — exact, simplest) vs. coalesced gap-aligned segments vs. lazy streaming for large spec-sets. If streaming, decide how back-pressure interacts with partial-delivery (a stream still "succeeds" while emitting nothing for gaps), and whether `DeliveryItem::Content` borrows through the snapshot (zero-copy) instead of cloning the `Arc`.
- **Snapshot ownership.** M6 methods take `&Snapshot` so M10 controls the consistency scope (recommended); a convenience that snapshots per call is possible but couples M6 to `&Kernel`.
- **Extent contiguity check.** Trust `content_count`/`link_count` (O(1)) vs. debug-build cross-check against `content_runs` (catches a broken D-CTG★ from upstream). Trust in release, assert in debug.
- **SHOWDELETIONS exactness source.** Use `deletions(d).denotes(·)` (default — M5's stated fault-free, read-straight-off seam, exact on prefix-free content addresses) vs. the exactness-independent `ever_placed(d).denotes(·) ∧ a ∉ arranged_content(d)` (robust even if M5's cover should ever coalesce spans). Default to `deletions`; switch only if M5's cover is shown to coalesce.
- **SHOWDELETIONS D-DISJ short-circuit.** M6-local: skip enumerating one document's `arranged_content` when the other's `deletions` cover is empty (its half is then empty) — a cheap guard in the spirit of D-DISJ's R-disjointness. Optional; default computes both halves directly.
- **COMPARE link-start spans.** Reject loudly (recommended — `NotContentSubspace`) vs. leniently strip via a content-subspace front-filter. (Spans that merely *denote* link positions from a content start are always legal — `resolve` clips them — so this is only about a span whose *start* is in the link subspace.)
- **COMPARE overlapping-region dedup.** Leave overlapping/repeated windows within an operand to collapse denotationally (default — conforming, deterministic via the stable sort) vs. pre-dedupe each operand's regions to shrink the cross-product. Perf-only; pick per profile.
- **Result caching.** Recompute by default (cheap, local, lock-free). If COMPARE/SHOWDELETIONS profile hot, memoize as a *hint* keyed on `(Snapshot::seq, args)` — and for any RETRIEVEV delivery cache, key on the consulted *restriction* (`M(d)|⟦σ⟧`), never on output byte-identity (R7 is sufficiency, not biconditional). Never authoritative; always recompute on a miss.
- **FINDDOCSCONTAINING resolve timing.** Re-resolve per query (tracks present-tense drift) vs. cache the frozen resolved I-coverage at an earlier snapshot for stable "find more like this" (legitimate because content is permanently grounded). Different products want different answers; expose the choice at M10.
