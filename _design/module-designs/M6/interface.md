# M6 — Interface (for dependents)

M6 owns the system's **read-only observer surface over documents** — the seven content/provenance queries (RETRIEVEV, RETRIEVEDOCVSPAN, RETRIEVEDOCVSPANSET, SHOWORIGIN V-arity, SHOWDELETIONS, COMPARE, FINDDOCSCONTAINING), each a **pure function of one pinned M2 snapshot** that writes nothing, ever.

## Public interface

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
/// One document + one ordinal-level depth-2 V-span. RETRIEVEV's ordered, single-span idiom.
pub struct Spec  { pub doc: Address, pub span: Span }
/// One document + a finite V-region (set of spans). The SET-shaped idiom for COMPARE & FINDDOCSCONTAINING.
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
    /// SHOWORIGIN over a V-span (ASN-0077, V-arity). Deduplicated origin documents, in tumbler order.
    /// Inadmissible (Err) on an unallocated document, a foreign subspace (`NoSuchSubspace`) or empty
    /// real subspace (`EmptySubspace`), a depth-incompatible `#start ≥ 3` span (`DepthIncompatible`,
    /// WF_V(v)), or a depth-2 span whose positions are not all currently bound (`RangeNotPresent`,
    /// WF_V(vi); O13) — reject, never silently clamp. Only the V-arity ships; there is no I-arity method.
    pub fn show_origin_v(&self, doc: &Address, span: &Span) -> Result<Vec<Address>, OriginError>;
}
```

### D. Provenance comparison

```rust
pub struct Deletions { pub a_with_b: Vec<Address>, pub b_with_a: Vec<Address> }  // deleted-from-one ∧ current-in-other; the existing I-addresses (D-IDENT), deduped + Tumbler-ordered (D-ORD)

pub use m5::VPos;   // CorrPair/CompareReport carry M5's VPos; re-export so M10's marshaler names it through M6, not by reaching into M5's crate

pub struct CorrPair { pub d1: Address, pub u1: VPos, pub d2: Address, pub u2: VPos, pub width: Nat }
pub struct CompareReport(pub Vec<CorrPair>);   // canonical order; slot i drawn from operand i

impl<'s, W: M6World> Query<'s, W> {
    /// SHOWDELETIONS (ASN-0075). Both documents must be registered (Err otherwise; allocated-empty is
    /// fine and yields empty halves). Each half is the deduped, Tumbler-ordered set of I-addresses
    /// deleted-from-one yet current-in-the-other — the existing I-addresses themselves (D-IDENT),
    /// never copies. Composed in M6 from M5's per-document `deletions`/`content_runs`; opens M4 for nothing.
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
pub enum SpecFault { NotOrdinalLevel, NotLevelUniform, StartNotZeroFree, StartTooShallow }  // StartTooShallow: #start < 2
#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub enum Operand   { First, Second }   // which COMPARE spec-set (ρ₁/ρ₂) a fault came from — Copy, captured into the gate closure
pub enum RetrieveError  { DocNotRegistered(Address), MalformedSpec { index: usize, fault: SpecFault } }
pub enum ExtentError    { DocNotRegistered }
pub enum OriginError    { DocNotRegistered, NoSuchSubspace, EmptySubspace, DepthIncompatible, RangeNotPresent, MalformedSpan(SpecFault) }
pub enum DeletionsError { DocNotRegistered(Address) }
pub enum CompareError   { DocNotRegistered(Address), NotContentSubspace { operand: Operand, region: usize, index: usize }, MalformedSpan { operand: Operand, region: usize, index: usize, fault: SpecFault } }
pub enum FindError      { DocNotRegistered(Address), MalformedSpan { region: usize, index: usize, fault: SpecFault } }
```

## Caller contracts & obligations

**General (all seven operations):**
- The caller takes the snapshot (`M2::snapshot()`) and constructs the handle with `Query::new(&snap)`; build **one `Query` per logical query** so every read observes one consistent `(M, R)` root.
- Reads never commit and have **no commit-before-acknowledge** obligation; M6 returns owned values, never a live view.
- Every failure is a **typed `Err(_)`** the caller must surface verbatim as a precondition/well-formedness rejection — never a silent skip.
- A **registered-but-empty** document yields the operation's empty form (`⟨⟩` / empty `Delivery` / empty halves / `[]`); an **unallocated** one yields the op's `*NotRegistered` error. M6 owns this distinction via `m3.is_registered_document`.
- `Vec<Address>` results are already **deduped and Tumbler-ordered**; `Address` is `Eq + Hash` but **not `Ord`**, so order any returned addresses via `.tumbler()`, not directly.
- `VPos` reaches the caller **re-exported through M6** (`pub use m5::VPos`) — name it as M6's type, do not reach into M5's crate.
- `as_of()` returns the committed `Seq` index this query reads (V1 retrospective).

**`retrieve_v(specs)`:**
- Caller must submit specs whose spans are **well-formed**: zero-free, ordinal-level, level-uniform, `#start ≥ 2` (an open-ended "to the end" selection must be expressed ordinal-level by reading `content_count` first).
- A single malformed spec **rejects the whole request** (`MalformedSpec { index, fault }`); an unregistered `doc` ⇒ `DocNotRegistered(Address)`.
- Guarantee: **one `DeliveryItem` per active V-position**, per-spec concatenation in submitted order, ascending-V within, no merge, no dedup, no global sort (R5/R8/R3). `Content(Val)` for content (an `Arc` clone — cheap), `Ref(Address)` for links (never reads M4).
- Gaps, depth-incompatible (`#start ≥ 3`), and empty/foreign subspaces degrade to **silent empty contributions, never errors** (R6); empty spec-set ⇒ `Ok(Delivery(vec![]))`.

**`doc_vspan(doc)` / `doc_vspanset(doc)`:**
- `doc` must be registered, else `Err(ExtentError::DocNotRegistered)`; registered-empty ⇒ `Ok(SpanSet::empty())` (`⟨⟩`).
- `doc_vspan`: singleton whole-document **bounding box** across subspaces, insensitive to mid-document content edits (V9) — route fragmentation-sensitive callers to `doc_vspanset`.
- `doc_vspanset`: per-subspace **exact** extents, ≤2 members (content, then link), already W13-normalized.

**`show_origin_v(doc, span)`:**
- Precondition: `doc` registered (`DocNotRegistered`) and `span` well-formed (`MalformedSpan(SpecFault)`).
- Returns **deduplicated origin documents in tumbler order** (`document_of` projection; the original allocator, not the current holder).
- Reject-never-clamp error cases the caller must handle distinctly: `NoSuchSubspace` (foreign subspace ∉ {content, link}), `EmptySubspace` (real but empty subspace), `DepthIncompatible` (`#start ≥ 3`), `RangeNotPresent` (depth-2 span overrunning the bound prefix).

**`show_deletions(d_a, d_b)`:**
- Both documents must be registered, else `DeletionsError::DocNotRegistered(Address)`; allocated-empty is fine ⇒ empty halves.
- Returns `Deletions { a_with_b, b_with_a }`, each the deduped, Tumbler-ordered set of **the existing I-addresses themselves** (D-IDENT) deleted-from-one yet current-in-the-other — never copies. Never opens M4.

**`compare(rho1, rho2)`:**
- Each region `doc` must be registered (`DocNotRegistered`); each span must **start in the content subspace** (`NotContentSubspace { operand, region, index }`) and be well-formed (`MalformedSpan { operand, region, index, fault }`) — the `operand`/`region`/`index` fields localize the fault.
- Returns a `CompareReport` of **address-equal** correspondences (value-blind, **never opens M4**), **complete under fan-out**, in deterministic canonical order; in each `CorrPair`, **slot 1 ⇐ ρ₁ and slot 2 ⇐ ρ₂**.

**`find_docs_containing(regions)`:**
- Each region `doc` must be registered (`DocNotRegistered`) and each span well-formed (`MalformedSpan { region, index, fault }`); allocated-empty contributes nothing.
- Returns the **present-tense containers** (current holders, filtered), tumbler-ordered and deduplicated — bare identities, **no positions, no counts**. (Distinct from `show_origin_v`, which reports allocators.)

**Invariants a caller may rely on:**
- No mutation anywhere; the returned values are immutable snapshot reads, and all constituents of one query come from one `&Snapshot`.
- Delivered content is permanent and faithful (M4 has no delete; bytes returned verbatim).
- COMPARE/SHOWDELETIONS/FINDDOCSCONTAINING never fetch bytes; only RETRIEVEV reads M4 (content positions only).

## Seams exposed downstream

- **→ M10 (the only consumer):** the seven read methods on `Query<'s, W>`. M10 takes a snapshot, builds a `Query`, calls the op, **marshals the returned value, and surfaces any `Err(_)` as a typed rejection** (precondition/well-formedness failures, never silent skips); registered-empty ⇒ the op's empty form, unallocated ⇒ the op's `*NotRegistered`. M6 returns by value and never commits — **no commit-before-acknowledge** step for reads. The reader surface carries **no SHOWORIGIN-over-I** (only `show_origin_v` exists). `VPos` is marshaled through M6's re-export.
- **→ engine assembly:** M6 contributes **no slice, no `Record` variant, no accessor trait, no `apply`/`rebuild_derived` fold** — it is a pure consumer of `HasM3 + HasContent + HasM5` and is generic over `W`, naming no concrete `World`/`Record`, so it trivially satisfies the composition contract. Nothing in the engine's `World`/`Record` comes from M6.

## Boundary — NOT provided here

- Any authoritative or derived-authoritative state — no `WorldState` slice, no journal record, no fold.
- The R relation or its reverse index `docs_containing` (M5); content bytes (M4); arrangements (M5).
- SHOWORIGIN's **I-span arity** — de-scoped to a settled decomposition amendment; no I-arity method exists on `Query`.
- Authorization / owner resolution (`effective_owner`) — M10's concern; SHOWORIGIN reports origin **documents**, not owners.
- Link-side discovery (M8).
- The request lifecycle, dispatch, and marshaling (M10).
- Any write path — M6 never mutates and exposes no `transact`/`Kernel`.
