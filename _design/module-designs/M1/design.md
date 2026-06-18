# M1 — Address & Span Algebra: Detailed Design

## Purpose & boundary

M1 is the pure value-level calculus of the address space. It owns everything decidable about an address or a range **from the values alone**: tumbler identity and the total order, T4 field-structure (validation, the node/account/document/element classifier, field and subspace projection, decidable containment), the position arithmetic (`⊕`, `⊖`, `inc`, action-point/`sig`, the ordinal shift), and the interval algebra over spans and span-sets (classify, intersect, merge, split, difference, canonical normalization, coverage). Every function here is total within its stated preconditions, consults no state, performs no I/O, and leans on nothing below ℕ. **One thing well: decide everything about addresses and ranges that is a function of the bare values, and hand those values upward as the universal key/endpoint/classification types.**

It deliberately does **not** own: the **allocator** — the durable monotone frontier, the active-allocator set, journaling and crash recovery — which is M3 (M1 supplies only the pure `inc` and the T4-preservation *gate predicate*; enforcing the gate and persisting the frontier is M3's obligation); the **inverse coverage index** ("which spans cover address *t*", the spanfilade) and any scale-up interval index, which is M7; the **content↔byte mapping** (M4/M5); and **ownership resolution** (the `ω` longest-prefix owner over the principal registry, M3 — M1 gives only the per-address containment predicates `ω` is built from).

## Public interface

Indices are **1-based** to match the spec (`#t`, `t₁..t_{#t}`, `actionPoint ∈ [1,#t]`); implement over 0-based storage. `Nat = num_bigint::BigUint` (arbitrary precision — T0(a) is non-negotiable; see Open decisions for the alternatives).

Every value type that crosses a store's journal/checkpoint boundary — `Tumbler`, `Address`, `Span`, `SpanSet`, `Level` — derives **`Serialize + Deserialize`**. M2's `WorldState` slices and `Record`s are `Serialize + DeserializeOwned`, and these types are the stores' keys and payloads, so a store cannot journal or checkpoint without them (surfaced by M4, the thinnest store — it journals a bare `Tumbler` key). This requires `num-bigint` built with its **`serde` feature** so `Nat = BigUint` serializes; M1 (or the shared base crate owning `Tumbler`) carries that obligation.

```rust
// Error types referenced throughout (T4Clause/T12Clause/ElemError are declared with their ops below):
pub struct EmptySequence;                                 // Tumbler::new on the empty sequence (T0)
pub struct T4Error { /* the violated T4Clause(s); first-failure vs full-set = Open decision */ }
pub struct AddPrecond;                                     // ⊕: ¬Pos(w) ∨ actionPoint(w) > #a
pub struct SubPrecond;                                     // ⊖: a < w  (requires a ≥ w)
pub struct GateViolation;                                  // checked_inc: inc_preserves_t4(t,k) = false (TA5a)
pub struct LevelMismatch;                                  // operands not mutually level-compatible (S6/WF)
pub enum   WfError    { NotIncreasing, LevelMismatch }     // from_endpoints: ¬(s<r) ; #s ≠ #r
pub enum   SplitError { NotInterior,  LevelMismatch }      // split: ¬(start<p<reach) ; level mismatch
```

### A. Tumbler value, identity, order

```rust
pub type Nat = num_bigint::BigUint;   // num-bigint built with its `serde` feature ⇒ Nat serializes
pub type Pos = usize;                 // 1-based component index; see "unbounded length" below

#[derive(Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct Tumbler(/* immutable sequence of Nat, len ≥ 1 */);

impl Tumbler {
    /// Carrier admission only (T0): rejects the empty sequence; admits zero/leading-zero
    /// sequences (they are legal carrier elements and legal span sentinels — NOT addresses).
    pub fn new(comps: impl IntoIterator<Item = Nat>) -> Result<Tumbler, EmptySequence>;
    pub fn len(&self) -> usize;                       // #t
    pub fn get(&self, i: Pos) -> &Nat;                // tᵢ
}

impl PartialOrd for Tumbler { /* delegates to `cmp` — required for Ord/PartialOrd consistency */ }
impl Ord for Tumbler { /* lexicographic, prefix-smaller (T1) */ }
pub fn is_prefix(p: &Tumbler, q: &Tumbler) -> bool;   // p ≼ q
```

`Ord`/`compare` is the intrinsic lexicographic order (T1/T2): total over **all** of carrier T including zero tumblers, no special-casing of zero separators (load-bearing — see Invariants). `==` is sequence equality (T3). `PartialOrd` exists only to satisfy `Ord: PartialOrd + Eq` and must return `Some(self.cmp(other))`.

### B. Validation, classification, field & containment projections

```rust
#[derive(Clone, Copy, PartialEq, Eq, Serialize, Deserialize)] pub enum Level { Node, Account, Document, Element }
#[derive(Clone, Copy, PartialEq, Eq, Serialize, Deserialize)] pub enum Class { Node, Account, Document, Element, Invalid }
pub enum T4Clause { LeadingZero, TrailingZero, AdjacentZeros, OverDepth }

pub fn zeros(t: &Tumbler) -> usize;                   // separator count — UNBOUNDED (T0(b)); usize, never u8
pub fn is_t4_valid(t: &Tumbler) -> bool;
pub fn classify(t: &Tumbler) -> Class;                 // total, never faults (ASN-0045)

/// Admission constructor: the validate-and-classify front door. `T4Error` **carries the
/// violated clause(s)** (decided — an admission gate is far more usable with diagnostics);
/// `classify`'s `Class::Invalid` stays bare.
pub fn validate(t: Tumbler) -> Result<Address, T4Error>;

/// A T4-valid, classified tumbler. INVARIANT: every `Address` is T4-valid; that validity
/// is discharged at each mint site — *checked* by `validate` and `elem_addr`, *preserved*
/// by `parent`, `document_of`, and `checked_inc`. `level` is a derived constant (immutable ⇒
/// never stale; not a hint).
#[derive(Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct Address { /* Tumbler */ , level: Level }

impl Address {
    pub fn tumbler(&self) -> &Tumbler;
    pub fn level(&self) -> Level;
    // Field projection (T4b N/U/D/E), present per zero-count. NB: the `&[Nat]` slices assume the
    // inline contiguous tumbler storage (the recommended default); under the `im::Vector` storage
    // option these must return `impl Iterator<Item = &Nat>` instead — see Open decisions.
    pub fn node_field(&self) -> &[Nat];
    pub fn account_field(&self) -> Option<&[Nat]>;    // Some iff zeros ≥ 1
    pub fn document_field(&self) -> Option<&[Nat]>;   // Some iff zeros ≥ 2
    pub fn element_field(&self) -> Option<&[Nat]>;    // Some iff zeros = 3
    pub fn subspace(&self) -> Option<Nat>;            // element_field[0] (T7): 1=text, 2=link
}

// Decidable containment (T6 a–d): truncate-and-compare on parsed fields, no index, no state.
// FIELD-ABSENCE ⇒ NO (T6 b/c/d): if EITHER operand lacks the required field (the relevant
// projection is `None`), the answer is `false` — never `None == None ⇒ true`. So two Node
// addresses do NOT report "same account".
pub fn same_node(a: &Address, b: &Address) -> bool;       // T6(a): N(a) = N(b)
pub fn same_account(a: &Address, b: &Address) -> bool;     // T6(b): zeros≥1 BOTH ∧ N,U equal
pub fn same_document(a: &Address, b: &Address) -> bool;    // T6(c): zeros≥2 BOTH ∧ N,U,D equal
pub fn under_document(a: &Address, b: &Address) -> bool;   // T6(d): zeros≥2 BOTH ∧ a under b's doc prefix
```

### C. Decomposition

```rust
pub fn parent(a: &Address) -> Option<Address>;       // longest T4-valid proper prefix; None for a 1-component node
pub fn document_of(a: &Address) -> Option<Address>;  // origin Document (zeros=2 prefix N·0·U·0·D) as Address; None if zeros(a)<2
pub fn ordinal(t: &Tumbler) -> &Nat;                 // t_{#t}, the local index at the current field
pub fn depth(a: &Address) -> Level;                  // = a.level()
```

### D. Position arithmetic

```rust
pub fn action_point(w: &Tumbler) -> Option<Pos>; // first nonzero index; None iff Zero(w)
pub fn sig(t: &Tumbler) -> Pos;                  // last nonzero index, else #t if all-zero

pub fn add(a: &Tumbler, w: &Tumbler) -> Result<Tumbler, AddPrecond>;  // ⊕: Pos(w) ∧ actionPoint(w) ≤ #a
pub fn sub(a: &Tumbler, w: &Tumbler) -> Result<Tumbler, SubPrecond>;  // ⊖: a ≥ w (result may be Zero)

pub fn inc(t: &Tumbler, k: usize) -> Tumbler;            // pure; k ≥ 0
pub fn inc_preserves_t4(t: &Address, k: usize) -> bool;  // TA5a gate predicate (M3 must consult)
pub fn checked_inc(t: &Address, k: usize) -> Result<Address, GateViolation>; // inc + gate + reclassify

/// b ⊖ a, returned only when the round-trip a ⊕ (b⊖a) = b is guaranteed (D0–D2:
/// a < b, divergence(a,b) ≤ #a, #a ≤ #b). Otherwise None — store endpoints, don't recompute.
pub fn displacement(a: &Tumbler, b: &Tumbler) -> Option<Tumbler>;
```

### E. Ordinal-only shift (element stream)

```rust
/// Ordinal-only shift: v ⊕ δ(n,#v) — advance the last component by n (TS1–TS5).
/// Precondition `n ≥ 1` (OrdinalShift/OrdinalDisplacement); `shift(v, 0) = v` is the total
/// extension (identity displacement). PRIMITIVE — unsafe for an element/subspace *base*
/// `doc·0·subspace` (whose last component IS the subspace id): a raw shift there advances
/// text→link. Hold a verified full element position, or use `shift_ordinal` (below), which
/// makes that mis-shift unrepresentable for callers that go through it.
pub fn shift(v: &Tumbler, n: &Nat) -> Tumbler;

// Subspace-safe packaging — closes the TA7a hazard for callers that use it:
pub struct ElemPos { pub doc: Address, pub subspace: Nat, pub ordinal: Nat }
pub enum ElemError { DocNotDocument, SubspaceZero, OrdinalZero }

/// Mints `doc·0·subspace·ordinal`. Guards the Address-validity invariant at this mint site:
/// requires `doc.level() == Document`, `subspace ≥ 1` (else adjacent zeros after the
/// separator), `ordinal ≥ 1` (else trailing zero); the constructed tumbler is routed through
/// `validate` defensively.
pub fn elem_addr(p: &ElemPos) -> Result<Address, ElemError>;
pub fn shift_ordinal(p: &ElemPos, n: &Nat) -> ElemPos;    // ordinal += n only (subspace untouched)
```

### F. Spans

```rust
#[derive(Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct Span { start: Tumbler, width: Tumbler }        // reach derived; (start,width) authoritative
pub enum T12Clause { ZeroWidth, ActionPointTooDeep }

impl Span {
    pub fn new(start: Tumbler, width: Tumbler) -> Result<Span, T12Clause>;   // T12
    pub fn from_endpoints(s: Tumbler, r: Tumbler) -> Result<Span, WfError>;  // WF: s<r ∧ #s=#r
    pub fn start(&self) -> &Tumbler;
    pub fn width(&self) -> &Tumbler;
    pub fn reach(&self) -> Tumbler;            // start ⊕ width — recomputed/cached, never persisted
    pub fn contains(&self, t: &Tumbler) -> bool;        // start ≤ t < reach (2 comparisons)
    pub fn is_level_uniform(&self) -> bool;             // #start == #width
}

/// Subtree-capture (ASN-0034, the 1-position convention): the span denoting exactly prefix
/// p's subtree — every extension of p (T5 contiguity), for ANY prefix p including one with a
/// trailing zero. Width is δ(1,#p) — advance position #p, NOT sig(p) — so the reach is
/// shift(p,1) = p ⊕ δ(1,#p). Total: shift(p,1) > p (TS4) and is length-preserving (#shift=#v),
/// so WF always fires; returns `Span`, not `Result`.
pub fn subtree_of(p: &Tumbler) -> Span;                  // from_endpoints(p, shift(p, &1))

pub enum SpanRel { Separated, Adjacent, ProperOverlap, Containment, Equal }  // SC
pub fn classify_spans(a: &Span, b: &Span) -> SpanRel;                         // pure order — no level gate
pub fn intersect(a: &Span, b: &Span) -> Result<Option<Span>, LevelMismatch>; // ≤ 1
pub fn merge(a: &Span, b: &Span)     -> Result<Option<Span>, LevelMismatch>; // = 1 when overlap/adjacent
pub fn split(s: &Span, p: &Tumbler)  -> Result<(Span, Span), SplitError>;    // p strictly interior
pub fn difference(a: &Span, b: &Span)-> Result<SpanSet, LevelMismatch>;      // ≤ 2 (S11d)
```

### G. Span-sets

```rust
/// Raw `PartialEq`/`Eq`/`Hash` on SpanSet are STRUCTURAL — they distinguish un-normalized
/// forms and are NOT denotational identity. The denotational, content-addressed identity is
/// `CanonicalForm` (the unique normalized form, S9); use that as a dedup/cache key, never a
/// raw `SpanSet`.
#[derive(Clone, PartialEq, Eq, Hash, Serialize, Deserialize)] pub struct SpanSet(/* im::Vector<Span> (default) */);

/// The unique normalized form (S9) as a content-addressed identity. `Hash + Eq` so it serves
/// directly as M7's dedup/cache key. Invariant: the inner SpanSet is normalized.
#[derive(Clone, PartialEq, Eq, Hash)] pub struct CanonicalForm(SpanSet /* normalized */);

impl SpanSet {
    pub fn empty() -> SpanSet;                          // ⟨⟩ ≜ ∅ (distinct from any zero-width span)
    pub fn singleton(s: Span) -> SpanSet;
    pub fn normalize(&self) -> Result<SpanSet, LevelMismatch>;  // unique canonical form (N1∧N2); S8/S9
    pub fn is_normalized(&self) -> bool;
    pub fn denotes(&self, t: &Tumbler) -> bool;
}
pub fn union(a: &SpanSet, b: &SpanSet) -> SpanSet;          // ⊕-free join: CONCATENATION ONLY — never
                                                            // normalizes, never fails; caller normalizes
pub fn intersect_sets(a: &SpanSet, b: &SpanSet) -> Result<SpanSet, LevelMismatch>;  // normalizes inputs internally
pub fn difference_sets(a: &SpanSet, b: &SpanSet) -> Result<SpanSet, LevelMismatch>; // normalizes inputs; no proven bound
pub fn equiv(a: &SpanSet, b: &SpanSet) -> Result<bool, LevelMismatch>;  // normalize both, compare (S9)
pub fn canonical_key(s: &SpanSet) -> Result<CanonicalForm, LevelMismatch>; // dedup/cache key (S9)

/// Single-span convex hull of a finite point set (S0). The only real precondition is
/// #min P = #max P (by convexity the hull then covers even a MIXED-length P): `None` if P is
/// empty or #min ≠ #max (WF cannot fire); else `Some(from_endpoints(min P, inc(max P, 0)))` —
/// reach = inc(max,0) is the exclusive upper bound (> max ALWAYS, length-preserving), and a
/// COVER (⊇ P) is all that's needed, so inc(·,0) here is correct (unlike in subtree_of). The
/// general `|Σ| = |P|` unit-span cover for arbitrary (possibly non-uniform) finite P (S7) is
/// deliberately NOT packaged here — union per-point unit spans `from_endpoints(t, inc(t,0))`.
pub fn hull(points: &[Tumbler]) -> Option<Span>;
```

## Core data model

M1 holds **no persistent state**; "authoritative vs hint" collapses to "primary value vs derived value", and every value is immutable (operations yield new values — Xanadu permanence falls out for free).

**`Tumbler` — the literal component sequence.** Store the bare sequence of `Nat` components, zeros explicit. This is the single highest-leverage decision: it makes canonical identity (T3) hold **by construction** — no mantissa/exponent, no normalization map, no quotient — deleting the entire alias bug class (the reference design's leading-zero alias that broke transitivity). Components are `BigUint`: `⊕` has **no carry propagation** (it touches exactly one position), so arbitrary precision is paid at one component, not across the address — cheap in the common case while honoring T0(a)'s unbounded siblings. Sequence storage is an **inline small-sequence** (most addresses are short); reach for `im::Vector` only if profiling shows deep tumblers dominate. The `&[Nat]` field projections (§B) assume this contiguous inline form; choosing `im::Vector` backing would require them to return an iterator/view instead (Open decisions). Note the contrast with span-sets below: structural sharing buys a short flat tumbler nothing, so `im` does *not* belong on the tumbler value — the cheapest structure that meets the contract is a flat array. Length is `usize`; T0(b) makes length unbounded *in principle*, but 2⁶⁴ components is unreachable, so `usize` is safe without violating the spec (unlike a fixed *component-magnitude* width, which would).

**`Address` — the validated, classified value (the hybrid).** Past the front door, an address carries its flat `Tumbler` plus its `Level` as a **derived constant**. Because the tumbler is immutable, the level can never miss — it is a standing fact, not a stale-able cache (had addresses been mutable, level would demote to a recomputed hint). Storage keys and journal entries stay flat `Tumbler`; everything that *reads fields or tests containment* carries `Address`. This is a builder choice (flat-on-demand vs parse-once vs hybrid) — the hybrid is recommended. Validity is the type's standing invariant, discharged at every mint site (§2, §3, §4, §5).

**`Span` — `(start, width)` authoritative, `reach` derived.** `(start, width)` is the spec's form and aligns the edit primitive (insert/delete shift widths) with the storage primitive. `reach = start ⊕ width` is a pure function of immutable inputs — a *cache* of a recomputation, not a Lampson hint: recompute on demand, optionally memoize on the hot comparison path, **never persist as authoritative state**, never desynchronizable. The empty designation is `SpanSet::empty()` (`⟨⟩`), structurally distinct from any span — a zero-width span is an illegal state the constructor must reject, never the representation of "nothing."

**`SpanSet` — an unordered union-denoting collection.** Default backing is `im::Vector<Span>`: structural sharing makes each derived span-set (a difference, an edit) a new value cheaply sharing the old, which is exactly the cheap-versioned-immutable-value shape Xanadu wants. This is where `im` earns its keep (not on the tumbler). The incremental-maintenance alternative — back it with `im::OrdMap<Tumbler, Span>` keyed by `start`, holding N1/N2 on every coalescing insert — is an Open decision for large, long-lived, in-place-edited span-sets. **Identity is denotational, not structural:** raw `SpanSet` derives `Eq`/`Hash`, but those are structural (they distinguish un-normalized forms) and must not be used as a dedup key. `canonical_key(&SpanSet) -> Result<CanonicalForm, LevelMismatch>` returns the unique normalized form (S9) as the content-addressed denotational identity — `CanonicalForm` is `Hash + Eq`, and *that* is the dedup/cache-key primitive M7 builds its link-dedup coverage-class on.

## Internal design

**Recovery: none, anywhere.** M1 is pure and stateless; every function is total within its preconditions. The durability/replay/recovery story for the one piece of mutable persistent state in this corner of the system — the allocation frontier — lives in M3 over M2's journal, not here.

### 1. Tumbler value, identity, order
Comparison is a direct left-to-right component scan, "prefix is smaller" (T1), O(min(#a,#b)), consulting nothing external (T2). It is **already the simplest correct thing** — leave it alone; don't cache what is this cheap (#t is small). Equality is sequence equality (T3), free from the representation. The comparator is defined on **all** of carrier T, including zero tumblers (TA-PosDom: positive > zero) — this is *why* an all-zero sequence sorts below everything and can serve as a span lower-bound sentinel even though it is not an admissible address. **Key tradeoff:** keeping the order flat and zero-agnostic (no hierarchy awareness in the comparator) is what keeps containment, spans, and arithmetic simple — hierarchy is projected on top (§2), never baked into the order. Getting zero-handling wrong here silently corrupts every operation downstream.

### 2. Validation, classification, projection, containment
All four T4-valid clauses (`zeros ≤ 3`; no adjacent zeros; no leading zero; no trailing zero) plus the zero-count are decidable in **one left-to-right O(#t) scan** with O(1) carried state (saw-zero-last?, running zero-count, first/last component). The running zero-count — and `zeros(t)`'s return — is **`usize`, unbounded per T0(b)**: a garbage tumbler with hundreds of zeros (legal carrier input arriving at admission) classifies as **Invalid**, never overflowing a fixed-width counter (which would wrap a 259-zero count to 3 and mis-read it as Element) and never faulting. The scan may early-exit once `zeros > 3` (validity already decided), but `zeros(t)` itself returns the true count. **Fuse validate-and-classify into that single pass** — there is no reason to walk the address twice. The cost is a *scan, not a parse*, and is cheap because it streams, not because the input is bounded (a Node is *any* zero-free sequence, unbounded length). The result is the five-way sum `Class` (Node/Account/Document/Element/Invalid), **not** four independent booleans: with a single classifying function, Partition (exactly-one-level) and Off-Domain Vacuity (zero-levels-for-invalid) become true *by construction* — a function is single-valued and `Invalid` is a disjoint tag — leaving only "the scan computes `zeros` and the clauses correctly" to verify. Mutual exclusion needs no injectivity (the zero-count is single-valued and 0/1/2/3 are distinct numerals); *membership* in {0,1,2,3} comes from the arithmetic bound `zeros ≤ 3`, never from a level-name bijection (which would be circular). `validate` mints `Address` on success (its `T4Error` carrying the violated clause(s)); `classify` is the total never-faulting form for garbage input.

Field projection (`node_field`/`account_field`/…) carves at the separator positions located during the scan (T4b); present-or-absent is encoded by `Option`, never a sentinel. `subspace` reads `element_field[0]` (T7: 1=text, 2=link). Containment (`same_node`/`same_account`/`same_document`/`under_document`) is `tumbleraccounteq`-style: truncate to the scope's field and compare parsed fields (T6 a–d) — decidable from the two addresses alone, the basis of coordination-free operation. **Field-absence is decisive (T6 b/c/d):** the predicate returns **NO** whenever *either* operand lacks the required field — `same_account` requires both `account_field`s present (`zeros ≥ 1`), `same_document`/`under_document` both `document_field`s present (`zeros ≥ 2`). A builder must not implement these as `a.account_field() == b.account_field()`: that gives `None == None ⇒ true`, so two **Node** addresses would falsely report "same account." Test field-presence first, then compare. **Tradeoff:** placing the T4-validity check *only* at admission (`validate`) and trusting internal producers keeps the arithmetic layer (§4) flat and re-validation-free; this is the recommended posture. The depth ceiling and the `T6/T7` field-reads rest *entirely* on the `zeros ≤ 3` clause being checked here — the only thing stopping a four-separator tumbler from being read as a phantom fifth level.

### 3. Decomposition
`ordinal(t) = t_{#t}` (the local sibling index). `depth(a) = a.level()`. **`parent(a)` is the longest T4-valid proper prefix of `a`** — equivalently, drop the last component and, if that exposes a trailing separator (0), drop that too (at most a two-component peel, since a valid address has no adjacent zeros). This is a *single structural peel*, not a guaranteed level-coarsening: a full content element `[1,0,2,0,5,0,1,9]` peels to its **subspace-base** `[1,0,2,0,5,0,1]` (still Element-class, element field `[1]`), and *that* peels to the document `[1,0,2,0,5]` — two calls, not one; a versioned document `[1,0,2,0,5,3]` peels to its base document `[1,0,2,0,5]`; a document peels to its account, an account to its node. `parent` returns `None` only for a single-component node (no non-empty proper prefix exists). For the common *level*-coarsening that M6's SHOWORIGIN actually needs — an I-address to its origin **Document `Address`** — use **`document_of`**, which truncates to the zeros=2 document prefix (N·0·U·0·D) and returns it as a classified `Document` address in one call (`None` when `zeros(a) < 2`; a Document input returns itself); this keeps address *construction* in M1 rather than forcing M6 to reassemble an address out of raw `document_field()` components. Both `parent` and `document_of` are the *containment* projection, recoverable from the address; **neither is the derivation parent** — the document field records who allocated under whom, not what was copied from what (T6(d)), and you cannot read creation time or version lineage off the address. Derivation history is a separate version graph (M3/M5), explicitly not M1's.

### 4. Position arithmetic
Implement straight from the constructive definitions; do **not** port reference mantissa arithmetic (its add routine carried an operand-order asymmetry that discarded an argument).
- **`action_point(w)`** = first nonzero index (the level at which a displacement acts); the shared kernel of `⊕`, the ordinal shift, and the span-length convention — a named primitive, not inline recomputation. **`sig(t)`** = last nonzero index; for T4-valid `t` it is `#t` (TA5-SigValid), but it is its own operation precisely so `inc(·,0)` (which advances `sig`) is never conflated with the action-point-driven arithmetic.
- **`add` (`⊕`)**: `k = action_point(w)`; copy `a₁..a_{k-1}`, set `a_k + w_k`, take `w_{k+1..}` as the tail; result length `#w`. Common case touches one component (no carry). It is **many-to-one** (TA-MTO/TA-RC): the start's structure below `k` is discarded, so a start cannot be recovered from result-plus-displacement in general.
- **`sub` (`⊖`)**: zero-pad to `L = max(#a,#w)`, find the zero-padded divergence `zpd`, emit zeros before it, the difference at it, `a`'s padded tail after; if padded-equal, the all-zero tumbler of length `L`. Result may be a (non-address) zero tumbler — that is legal here.
- **`inc`**: `k=0` advances `sig(t)` (next peer, length-preserving); `k>0` appends `k-1` zeros then a `1` — extending the component sequence by `k` positions (`k=1` mints a *same-zeros-level* peer/version; `k=2` descends one hierarchy/zeros-level; `k≥3` always breaks T4, hence the gate). **`inc_preserves_t4`** is the TA5a gate: `k∈{0,1}` always, `k=2` iff `zeros(t) ≤ 2`, `k≥3` never. M1 supplies `inc` (pure) and the gate *predicate*; **the gate's enforcement and the frontier it guards are M3's** — an allocator that skips the gate emits T4-invalid addresses that break the level-determination GlobalUniqueness rests on, so M3 must call `inc_preserves_t4`/`checked_inc` before minting. `checked_inc` is the convenience that combines them and reclassifies, and (with `validate`/`elem_addr`/`parent`/`document_of`) is one of the `Address` mint sites that keep the validity invariant standing.
- **`displacement(a,b)`** returns `Some(b⊖a)` only under D0–D2 (`a<b`, `divergence(a,b)≤#a`, `#a≤#b`), where the round-trip `a⊕(b⊖a)=b` is guaranteed; otherwise `None`. The API thereby *forces* the "store endpoints rather than recompute them" discipline at the type level: outside the safe window, callers cannot get a displacement and must keep the endpoints.

### 5. Ordinal-only shift
`shift(v,n) = v ⊕ δ(n,#v)` advances `v`'s last component by `n` (TumblerAdd at the final position), under precondition `n ≥ 1` (OrdinalDisplacement requires a positive displacement; `δ(0,·)` is Zero and fails `Pos(w)`). The total extension `shift(v,0) = v` is defined explicitly so the function is total. It inherits `⊕`'s structure: order-preserving (TS1), injective (TS2), additively-composing (TS3), strict and amount-monotone (TS4/TS5) — exactly what lets the I-stream stay sorted and distinct under shift. The hazard (TA7a): the *last component is the ordinal only for a full element position* (`doc·0·subspace·ordinal`); shifting a bare subspace base (`doc·0·subspace`, whose last component **is** the subspace id) would silently advance text→link. The recommended packaging — `ElemPos { doc, subspace, ordinal }` with `shift_ordinal` touching only `ordinal` — strips and reattaches the subspace as structural context, making the bug unrepresentable *for callers that go through the wrapper*. `shift_ordinal` is a pure `ElemPos → ElemPos` step (subspace untouched, `ordinal += n`); validity is re-discharged when the position is materialized by `elem_addr`, which guards the `Address` invariant at that mint site (`doc.level() == Document`, `subspace ≥ 1` so no adjacent zero follows the separator, `ordinal ≥ 1` so no trailing zero), returning `Result<Address, ElemError>` and routing the constructed tumbler through `validate`. **Raw `shift` remains public** for callers already holding a verified full element position, and so the "un-violable" property is the *wrapper's*, not the whole API's — raw `shift` still bypasses the guard. Making `shift` crate-private behind `shift_ordinal` is an Open decision; either way the wrapper is the safe default. **Tradeoff:** the wrapper costs a reconstruct on each shift but removes an entire silent-corruption class for the callers that use it — take it.

### 6. Spans
The whole single-span engine collapses to **one comparator, one constructor (`WF`/`from_endpoints`: `s<r ∧ #s=#r ⇒ (s, r⊖s)`), and min/max under the order** — resist four independently-reasoned operations.
- **`Span::new`** enforces full T12 (`width>0` **and** `actionPoint(width) ≤ #start`); both are required for `reach > start`. Routes the empty designation to `⟨⟩`, never a zero-width span.
- **`subtree_of(p)`** = `from_endpoints(p, shift(p, &1))` = `from_endpoints(p, p ⊕ δ(1,#p))` packages ASN-0034's 1-position subtree-capture convention: the span denoting exactly `p`'s subtree (every extension of `p`), making the T5 contiguity guarantee directly exploitable without re-deriving it — for **any** prefix `p`, well-formed or not. The width must advance position **`#p`** (the displacement `δ(1,#p)`, i.e. `shift(p,1)`), **not** `sig(p)`: the two coincide only when `p`'s last component is nonzero, so using `inc(p,0)` (which advances `sig(p)`) would over-capture on a trailing-zero prefix — e.g. `inc([2,0],0)=[3,0]` admits `[2,1]`, which is *not* an extension of `[2,0]`. It is total — `shift(p,1) > p` (TS4) and is length-preserving (`#shift = #v`), so `WF` always fires.
- **`classify_spans` (SC)** is pure order (5 mutually-exclusive cases) — **no level gate** (the classifier doesn't construct).
- **`intersect`** = `(max start, min reach)`; **self-guarding** — disjoint inputs give `max start ≥ min reach`, failing `WF`'s `s<r`, correctly yielding `None`. Needs the level gate (for equal-length `WF`) but **not** SC.
- **`merge`** = `(min start, max reach)`, which is *not* self-guarding (two separated spans still satisfy `min start < max reach`). One comparison suffices: `separated ⟺ max start > min reach` → `None`; else `WF(min start, max reach)`. Cheaper than the full classifier — do the cheapest correct thing.
- **`split`** requires `start < p < reach` (strictly interior — `p=start` or `p=reach` yields a forbidden zero-width part) and `level_compat(start,p)`; returns `(start, p⊖start)`, `(p, reach⊖p)`, adjacent by construction.
- **`difference`** is the only op needing **full SC** (S11d dispatch):

  | SC case | `⟦α⟧ \ ⟦β⟧` | spans |
  |---|---|---|
  | Separated / Adjacent | `⟦α⟧` | 1 |
  | Proper overlap | left- or right-complement | 1 |
  | Containment (`β⊂α`) | left + right complements | 2 |
  | Containment (`α⊂β`) / Equal | `∅` | 0 |

The **level gate** (level-uniform operands, mutually level-compatible — all endpoints share length L) sits *after* classification, *before* construction, on `intersect`/`merge`/`split`/`difference`. It is what makes `WF`/width-recovery sound: outside level-uniformity the start↔reach interconversion breaks silently (`[1,5] ⊖ [1,3,5] = [0,2,0] ≠ [0,2]`).

### 7. Span-sets
**`normalize`** is the central primitive: sort by `start`, linear left-to-right sweep coalescing any pair with `reach_i ≥ start_{i+1}` (overlap or adjacency), producing the unique N1∧N2 canonical form — O(n log n), dominated by the sort. It is fallible (`Result<SpanSet, LevelMismatch>`): a span-set whose components are not mutually level-compatible cannot be normalized. Uniqueness (S9) makes the canonical form an **equality oracle and cache key**: `equiv` = normalize both, compare — and so `equiv -> Result<bool, LevelMismatch>`, inheriting `normalize`'s fallibility. `canonical_key -> Result<CanonicalForm, LevelMismatch>` returns the unique normalized form wrapped as `CanonicalForm` (`Hash + Eq`), content-addressable for dedup/memoization — the seam M7's coverage-class dedup key rides; raw `SpanSet` `Eq`/`Hash` are structural and must not substitute for it. **`union`** is **concatenation only** — it never normalizes and never fails, so it stays total (`-> SpanSet`); normalization is the caller's separate (eager or lazy) step. Because union is commutative and associative (S10) — with idempotence following as a *derived corollary* — span-sets form a join-semilattice (within one tumbler length); workers can accumulate and merge in any order to a deterministic canonical result, coordination-free. **`intersect_sets`/`difference_sets`** are one parametrized sweep-line; each **normalizes its two inputs internally** (so the `Result<_, LevelMismatch>` is honest — `LevelMismatch` fires when a set is not internally level-uniform *or* the two sets are not mutually level-compatible) and emits a normalized result; set-level difference has **no proven output bound** (open), so its result is not size-promised. **`hull`** gives the single-span convex hull of a finite point set (convexity, S0); its only real precondition is **`#min P = #max P`** (by convexity the hull then covers even a *mixed-length* P) — `None` for empty P or `#min ≠ #max` (so `WF` cannot fire), else `from_endpoints(min P, inc(max P, 0))`. Here `inc(max,0)` is correct (unlike in `subtree_of`): the hull need only **cover** (⊇ P), and `inc(max,0) > max` always holds, so over-capture is harmless. The general `|Σ|=|P|` unit-span cover for arbitrary (possibly non-uniform) finite P (S7) is deliberately not packaged here — a caller wanting it unions per-point unit spans `from_endpoints(t, inc(t,0))`. Note the binding S7 fact — *no* span-set denotes an arbitrary finite P *exactly*, because every span denotes an infinite set (deeper sub-extensions fill every interval). The algebra is interval arithmetic over a hierarchical ordered space — not finite-set manipulation, not byte counting. **Default to eager normalization for stored/handed-off span-sets, lazy in-flight**; default to batch sort-sweep, graduate to the `im::OrdMap` incremental form only for large long-lived edited sets. Keep the commutative merge path **union-only** — difference is not order-free.

## Invariants & contracts

**By construction** (fall out of the data model / a single-valued function):
- *Canonical identity* (T3, ASN-0034) — free from literal-sequence storage; no normalization exists to get wrong.
- *Total order, intrinsic comparison* (T1/T2, ASN-0034) — free from the lexicographic scan; no external read.
- *Contiguous subtrees* (T5, ASN-0034) — every prefix's subtree is a contiguous interval; holds from the order alone, no field parse, so spans capture subtrees for free (`subtree_of`, width `δ(1,#p)`).
- *Exactly-one-level / off-domain vacuity / never-faults* (Partition, OffDomainVacuity, ASN-0045) — from the five-way sum classifier: a function is single-valued and `Invalid` is disjoint. The zero-count is unbounded `usize`, so arbitrarily-many-zeros input lands in `Invalid`, never a wrapped level and never a fault.
- *Level stability* (ASN-0045) — `Address.level` is a derived constant on an immutable value.
- *Subspace disjointness* (T7, ASN-0034) — text<link by `1<2` at the subspace position; no enforcement.
- *Span non-emptiness in results* (S2, ASN-0053) — every algebra result is built through `WF` (`s<r ⇒ width>0`); `⟨⟩` carries "nothing", never a zero-width span.
- *Bounded fan-out* (S1/S11, ASN-0053) — intersect ≤1, merge =1, difference ≤2, by formula shape.
- *Immutability/permanence* — values never mutate; operations yield new values.
- *Order-independent union* (S10, ASN-0053) — held by keeping the merge path union-only.

**By active enforcement** (a named function must guard):
- *Unbounded component magnitude* (T0(a), ASN-0034) — **`Nat = BigUint`** in every component op; fixed-width is a spec violation absent a discharged finite-model proof. *Where:* the value type and all of §4.
- *Carrier nonemptiness* (T0, ASN-0034) — `Tumbler::new` rejects the empty sequence. *Where:* the constructor. (This resolves ASN-0045's empty-tumbler question — see Conflicts.)
- *T4 well-formedness* (T4/ASN-0045) — the single scan in `validate`/`classify`; the depth ceiling and every `T6/T7` field-read rest on the `zeros ≤ 3` check, with `zeros` returning `usize` so unbounded-zero garbage is classified `Invalid` without overflow or fault. **Every `Address` mint site discharges this:** `validate` and `elem_addr` *check* it (the latter additionally guards `doc=Document ∧ subspace≥1 ∧ ordinal≥1`), and `parent`, `document_of`, and `checked_inc` *preserve* it. *Where:* §2, §3, §4, §5.
- *Field-absence ⇒ NO* (T6 b/c/d) — the containment predicates test field-presence before comparing fields; `None`-vs-`None` is `false`, never `true`. *Where:* §2.
- *Allocator-discipline gate* (T10a/TA5a, ASN-0034) — `inc_preserves_t4` must be **correct here**; its *enforcement* is M3's obligation (the producer's, not the caller's). *Where:* §4; flag the seam to M3.
- *T12 span well-formedness* (T12, ASN-0034/0053) — `width>0 ∧ actionPoint(width)≤#start`. *Where:* `Span::new`.
- *Level-compatibility* (S6/WF, ASN-0053) — gate before all span/span-set construction (`intersect`/`merge`/`split`/`difference`/`normalize`/`canonical_key`/`equiv`/`intersect_sets`/`difference_sets`). *Where:* §6/§7.
- *Zero-agnostic total order* (S0/Q11, ASN-0053) — the comparator special-cases nothing; the easiest invariant to break silently. *Where:* §1.
- *Arithmetic preconditions* — `⊕`: `Pos(w)∧actionPoint(w)≤#a`; `⊖`: `a≥w`; `shift`: `n≥1` (with `shift(v,0)=v` the total extension). *Where:* `add`/`sub`/`shift`.
- *Zero-sentinel quarantine* (TA6, ASN-0034) — the address validator is **not** reused at the span boundary; an all-zero tumbler is rejected as an address but legal as a span endpoint. *Where:* span constructors keep out of `validate`.

## Dependencies & seams

**Upstream:** none. M1 is the foundation; it leans only on ℕ → `num-bigint`. (It carries no edge to M2, which is generic over opaque keys and needs no address algebra.)

**Downstream seams (what M1 hands up, and to whom):**
- **`Tumbler`/`Address`** — the universal key/endpoint/classification type for every module (M3–M10). Flat `Tumbler` is the storage/journal key; `Address` is the past-the-door carried value, T4-valid by its standing invariant.
- **`inc` + `inc_preserves_t4`/`checked_inc` → M3.** M3's per-(home,subspace) frontier allocator *calls* these; M1 owns neither the frontier, the active-allocator set, nor durability/recovery. The seam contract M3 codes against: `inc(t,0)` = next sibling (length-preserving), `inc(t,k>0)` = extend by `k` components (`k=1` same-zeros-level version, `k=2` descends one zeros-level), and `inc_preserves_t4` is the gate it **must** pass before minting. Over-shooting (gaps/ghosts) is harmless to M1's algebra; reuse is fatal — that durability invariant is M3's.
- **`classify`/`Level`/field projections/containment → M3, M5, M6, M8.** M3's `ω` longest-prefix owner resolver composes `same_account`/`under_document` over its principal registry (M1 gives the per-address predicates, including the field-absence⇒NO rule; the resolver is M3's). M6/M8's registered-empty-vs-unallocated query distinctions, and M5's S3★ content-vs-link V-position routing, all key on `classify`/`subspace`.
- **`subspace` → M5/M7/M8.** Drives content-subspace (M4-targeted) vs link-subspace (M7-targeted) referential-integrity routing.
- **`Span`/`SpanSet`/`normalize`/`classify_spans`/`intersect`/`difference`/`canonical_key` → M5, M6, M7, M8.** M7's endsets/link values are span-sets; its link-dedup **coverage-class key** is derived from `canonical_key` (M1 computes the canonical form — `Result<CanonicalForm,_>` on level-uniform inputs; M7 decides the class *policy* and supplies it to M2's keyed critical section — M2 never computes it). M8's coverage/discovery and M6's extent queries consume `classify_spans`/`intersect`/`difference`/membership/`subtree_of`.
- **`shift`/`ElemPos` → M3/M5.** I-stream element allocation and V-enfilade traversal are driven by the ordinal shift; M1 supplies the pure value tool and the subspace-safe wrapper, the stateful allocation/traversal is upstream.
- **Field/origin projectors → M6.** SHOWORIGIN's *pointwise* origin attribution is the pure field/document-prefix projection here — in particular **`document_of`** maps an I-address straight to its origin **Document `Address`** (no reassembly from raw `document_field()` components on M6's side); the SHOWORIGIN *operation* (whose I-span/V-span resolvers read arrangement state) is M6.

**Explicitly NOT a seam M1 provides:** the inverse "which spans cover *t*" index / spanfilade (M7); any scale-up interval/segment index (M7/M8); content/byte mapping (M4/M5). M1 hands up span *values*; the indexing that makes the inverse query fast at docuverse scale is downstream.

## Conflicts resolved

- **Allocator material (ASN-0034) is M3, not M1 — the boundary.** ASN-0034 devotes most of its prose to the frontier, durability strategies, journaling, and crash recovery. None of that is M1: it is the one piece of *mutable persistent state* in the namespace, and it belongs to M3 over M2's journal. M1 keeps only the pure value pieces the allocator *uses* — `inc`, `action_point`/`sig`, and the TA5a gate *predicate*. This is the single biggest scoping resolution; the seam is `inc_preserves_t4` as a producer obligation M3 enforces.
- **Empty-tumbler open question (ASN-0045) — resolved upstream by T0.** ASN-0045 flags `T4-valid([])` as under-specified and says to escalate to T0/T4. T0's carrier is *nonempty* finite sequences (`#a ≥ 1`), so the empty sequence is not a tumbler at all. `Tumbler::new` rejects it; the boundary clauses `t₁≠0`/`t_{#t}≠0` never index a non-existent element, and the classifier never sees `[]`. Resolved by construction, not papered over in the classifier.
- **Zero-sentinel at the span boundary (ASN-0034 open) vs ASN-0053's T12 spans.** The all-zero tumbler is rejected *as an address* (T4 leading-zero) but is a legitimate *span endpoint* (unbounded lower bound, TA6). Resolution: the address validator stays out of the span layer; `Span::new` enforces T12 (no zero-width) but does not re-run `validate` on endpoints. How containment/intersection behave when an endpoint is the zero sentinel is left genuinely open (see Open decisions) — not silently resolved.
- **"coverage-class computed in M1" (decomposition) vs the canonical-form/policy split (here) — a deliberate refinement.** The decomposition's M7 seam says the link-dedup key is "keyed by a coverage-class computed in M1." This design refines that boundary: M1 owns only the **canonical normalization** — `canonical_key` *is* the dedup primitive (the unique normalized form, S9) — while the **coverage-class *policy*** (which classes are equivalent for de-duplication) lives in M7, which supplies the resulting key to M2's keyed critical section. The apparent contradiction is intentional: keeping policy out of the pure value layer is the cleaner placement (mechanism in M1, policy in M7), so this is a sharpening of the decomposition's wording, not a gap against it.
- **`(start,length)` (ASN-0034) vs `(start,width)`/`(start,reach)` (ASN-0053).** Resolution: `(start, width)` authoritative (aligns edit and storage primitives), `reach` a recomputed/cached derivation. For level-uniform spans the two endpoint forms are interchangeable; outside level-uniformity they are not, so the level gate guards every interconversion.
- **"account" vs "user" (ASN-0045).** `account` is canonical for the zeros=1 level everywhere in M1 (the level vocabulary, classifier, containment). `user` is confined to M3's ownership layer (session-slot index / ownership predicates) and never crosses into M1's level names. The field-projection symbol `U` is retained unrenamed.
- **"origin" projector scoping.** No source note defines an `origin` operation; M1 provides the *pure pointwise* field/document-prefix projectors (`document_of`, `document_field`, `under_document`; plus the generic `parent` peel), and the SHOWORIGIN *operation* — which resolves I-spans/V-spans against arrangement state — is M6. M1 hands up the value-level piece only.

## Open build decisions

- **Component representation:** `BigUint` (recommended) vs varint-only vs fixed-width-with-bignum-fallback — the last *only* with a discharged finite-model obligation; the fixed-width fast path is acceptable solely as a measured cache, never the system of record.
- **Sequence storage:** inline small-sequence (default) vs `im::Vector` — decided by whether deep tumblers actually dominate the workload. **Coupling:** the `&[Nat]`-returning field projections (§B) assume the inline contiguous form; selecting `im::Vector` requires them to return an iterator/view instead.
- **Address-representation strategy:** flat-on-demand vs parse-once vs the hybrid `Address` (recommended); whether to attach a recomputable parsed field-view as a hint (only if a containment-query path proves hot — measure first, `#t` is small).
- **Level-uniformity as a type invariant** (`LeveledSpan<L>`, mismatches unrepresentable) vs the runtime `LevelMismatch` gate — recommend the runtime gate now, type-encode once cross-level policy settles.
- **Span-set backing:** flat `im::Vector<Span>` + batch sort-sweep (default) vs `im::OrdMap<Tumbler,Span>` incremental coalescing (large, long-lived, in-place-edited sets — a coalescing insert is O(log n) but absorbing k spans is O(k log n)).
- **Eager vs lazy normalization**, and whether "always normalized" is a stored invariant.
- **Whether to content-address span-sets** (hash the `CanonicalForm`) for dedup/memoization — directly feeds the shape of M7's coverage-class policy keyed on `canonical_key`.
- **Pairwise return shape:** uniform `SpanSet` vs a `None | One | Two` sum, given the proven fan-outs.
- **`T4Error` diagnostic granularity:** `validate`'s `T4Error` **carries the violated clause(s)** (decided — admission gates want diagnostics) and `classify`'s `Class::Invalid` stays **bare** (the total form needs only the tag). The remaining sub-decision is *within* `T4Error`: first-failure-found vs the full set of violated clauses — they co-occur (`[0]` violates leading *and* trailing; `[0,0]` adds adjacent).
- **Subspace-context plumbing & raw `shift` visibility:** the `ElemPos` strip/reattach wrapper (recommended — makes TA7a un-violable *for callers that use it*) vs carrying the subspace id alongside ordinals everywhere. Because raw `shift` still bypasses the wrapper's guard (it will advance a `doc·0·subspace` base text→link), a paired sub-decision: keep `shift` public-but-annotated (current) vs make it crate-private behind `shift_ordinal`. The "un-violable" property is the wrapper's, not the whole API's.
- **Within-tumbler at-rest/wire encoding** (humber varint vs length-prefixed bignum) — a serialization-boundary choice deferable to M2's journal format, not M1's in-memory form.
- **Zero-sentinel span semantics** — how `contains`/`intersect`/`classify_spans` treat an unbounded (all-zero) endpoint. The note leaves this open; pick a convention when a consumer (M6/M8 unbounded-range queries) first needs one, and keep it out of the address validator.
