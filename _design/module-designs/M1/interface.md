# M1 — Interface (for dependents)

M1 owns the pure value-level calculus of the address space: tumbler identity and total order, T4 field-structure (validation/classification/projection/decidable containment), position arithmetic (`⊕`, `⊖`, `inc`, action-point/`sig`, ordinal shift), and the interval algebra over spans and span-sets — every function total within its preconditions, consulting no state, performing no I/O.

## Public interface

Indices are **1-based** (`#t`, `t₁..t_{#t}`, `actionPoint ∈ [1,#t]`).

```rust
// Error types referenced throughout:
pub struct EmptySequence;                                 // Tumbler::new on the empty sequence (T0)
pub struct T4Error { /* the violated T4Clause(s) */ }
pub struct AddPrecond;                                     // ⊕: ¬Pos(w) ∨ actionPoint(w) > #a
pub struct SubPrecond;                                     // ⊖: a < w  (requires a ≥ w)
pub struct GateViolation;                                  // checked_inc: inc_preserves_t4(t,k) = false (TA5a)
pub struct LevelMismatch;                                  // operands not mutually level-compatible (S6/WF)
pub enum   WfError    { NotIncreasing, LevelMismatch }     // from_endpoints: ¬(s<r) ; #s ≠ #r
pub enum   SplitError { NotInterior,  LevelMismatch }      // split: ¬(start<p<reach) ; level mismatch
```

### A. Tumbler value, identity, order

```rust
pub type Nat = num_bigint::BigUint;
pub type Pos = usize;                 // 1-based component index

#[derive(Clone, PartialEq, Eq, Hash)]
pub struct Tumbler(/* immutable sequence of Nat, len ≥ 1 */);

impl Tumbler {
    /// Carrier admission only (T0): rejects the empty sequence; admits zero/leading-zero
    /// sequences (legal carrier elements and span sentinels — NOT addresses).
    pub fn new(comps: impl IntoIterator<Item = Nat>) -> Result<Tumbler, EmptySequence>;
    pub fn len(&self) -> usize;                       // #t
    pub fn get(&self, i: Pos) -> &Nat;                // tᵢ
}

impl PartialOrd for Tumbler { /* delegates to `cmp` */ }
impl Ord for Tumbler { /* lexicographic, prefix-smaller (T1) */ }
pub fn is_prefix(p: &Tumbler, q: &Tumbler) -> bool;   // p ≼ q
```

### B. Validation, classification, field & containment projections

```rust
#[derive(Clone, Copy, PartialEq, Eq)] pub enum Level { Node, Account, Document, Element }
#[derive(Clone, Copy, PartialEq, Eq)] pub enum Class { Node, Account, Document, Element, Invalid }
pub enum T4Clause { LeadingZero, TrailingZero, AdjacentZeros, OverDepth }

pub fn zeros(t: &Tumbler) -> usize;                   // separator count — UNBOUNDED (T0(b)); usize
pub fn is_t4_valid(t: &Tumbler) -> bool;
pub fn classify(t: &Tumbler) -> Class;                 // total, never faults (ASN-0045)

/// Admission constructor: validate-and-classify front door. `T4Error` carries the
/// violated clause(s); `classify`'s `Class::Invalid` stays bare.
pub fn validate(t: Tumbler) -> Result<Address, T4Error>;

#[derive(Clone, PartialEq, Eq, Hash)]
pub struct Address { /* Tumbler */ , level: Level }

impl Address {
    pub fn tumbler(&self) -> &Tumbler;
    pub fn level(&self) -> Level;
    pub fn node_field(&self) -> &[Nat];
    pub fn account_field(&self) -> Option<&[Nat]>;    // Some iff zeros ≥ 1
    pub fn document_field(&self) -> Option<&[Nat]>;   // Some iff zeros ≥ 2
    pub fn element_field(&self) -> Option<&[Nat]>;    // Some iff zeros = 3
    pub fn subspace(&self) -> Option<Nat>;            // element_field[0] (T7): 1=text, 2=link
}

// Decidable containment (T6 a–d). Field-absence ⇒ NO.
pub fn same_node(a: &Address, b: &Address) -> bool;       // T6(a): N(a) = N(b)
pub fn same_account(a: &Address, b: &Address) -> bool;     // T6(b): zeros≥1 BOTH ∧ N,U equal
pub fn same_document(a: &Address, b: &Address) -> bool;    // T6(c): zeros≥2 BOTH ∧ N,U,D equal
pub fn under_document(a: &Address, b: &Address) -> bool;   // T6(d): zeros≥2 BOTH ∧ a under b's doc prefix
```

### C. Decomposition

```rust
pub fn parent(a: &Address) -> Option<Address>;       // longest T4-valid proper prefix; None for a 1-component node
pub fn document_of(a: &Address) -> Option<Address>;  // origin Document (zeros=2 prefix N·0·U·0·D); None if zeros(a)<2
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
/// a < b, divergence(a,b) ≤ #a, #a ≤ #b). Otherwise None.
pub fn displacement(a: &Tumbler, b: &Tumbler) -> Option<Tumbler>;
```

### E. Ordinal-only shift (element stream)

```rust
/// Ordinal-only shift: v ⊕ δ(n,#v) (TS1–TS5). Precondition `n ≥ 1`; `shift(v,0)=v`
/// is the total extension. PRIMITIVE — unsafe on a bare element/subspace base.
pub fn shift(v: &Tumbler, n: &Nat) -> Tumbler;

pub struct ElemPos { pub doc: Address, pub subspace: Nat, pub ordinal: Nat }
pub enum ElemError { DocNotDocument, SubspaceZero, OrdinalZero }

/// Mints `doc·0·subspace·ordinal`. Requires `doc.level()==Document`, `subspace≥1`,
/// `ordinal≥1`; constructed tumbler is routed through `validate`.
pub fn elem_addr(p: &ElemPos) -> Result<Address, ElemError>;
pub fn shift_ordinal(p: &ElemPos, n: &Nat) -> ElemPos;    // ordinal += n only (subspace untouched)
```

### F. Spans

```rust
#[derive(Clone, PartialEq, Eq, Hash)]
pub struct Span { start: Tumbler, width: Tumbler }        // reach derived; (start,width) authoritative
pub enum T12Clause { ZeroWidth, ActionPointTooDeep }

impl Span {
    pub fn new(start: Tumbler, width: Tumbler) -> Result<Span, T12Clause>;   // T12
    pub fn from_endpoints(s: Tumbler, r: Tumbler) -> Result<Span, WfError>;  // WF: s<r ∧ #s=#r
    pub fn start(&self) -> &Tumbler;
    pub fn width(&self) -> &Tumbler;
    pub fn reach(&self) -> Tumbler;            // start ⊕ width — recomputed/cached, never persisted
    pub fn contains(&self, t: &Tumbler) -> bool;        // start ≤ t < reach
    pub fn is_level_uniform(&self) -> bool;             // #start == #width
}

/// Subtree-capture (ASN-0034, 1-position convention): the span denoting exactly prefix
/// p's subtree, for ANY prefix p. Width is δ(1,#p). Total; returns `Span`, not `Result`.
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
/// Raw `PartialEq`/`Eq`/`Hash` are STRUCTURAL — NOT denotational identity. Use
/// `CanonicalForm` as a dedup/cache key, never a raw `SpanSet`.
#[derive(Clone, PartialEq, Eq, Hash)] pub struct SpanSet(/* im::Vector<Span> */);

/// The unique normalized form (S9) as content-addressed identity. `Hash + Eq`.
#[derive(Clone, PartialEq, Eq, Hash)] pub struct CanonicalForm(SpanSet /* normalized */);

impl SpanSet {
    pub fn empty() -> SpanSet;                          // ⟨⟩ ≜ ∅ (distinct from any zero-width span)
    pub fn singleton(s: Span) -> SpanSet;
    pub fn normalize(&self) -> Result<SpanSet, LevelMismatch>;  // unique canonical form (N1∧N2); S8/S9
    pub fn is_normalized(&self) -> bool;
    pub fn denotes(&self, t: &Tumbler) -> bool;
}
pub fn union(a: &SpanSet, b: &SpanSet) -> SpanSet;          // CONCATENATION ONLY — never normalizes, never fails
pub fn intersect_sets(a: &SpanSet, b: &SpanSet) -> Result<SpanSet, LevelMismatch>;  // normalizes inputs internally
pub fn difference_sets(a: &SpanSet, b: &SpanSet) -> Result<SpanSet, LevelMismatch>; // normalizes inputs; no proven bound
pub fn equiv(a: &SpanSet, b: &SpanSet) -> Result<bool, LevelMismatch>;  // normalize both, compare (S9)
pub fn canonical_key(s: &SpanSet) -> Result<CanonicalForm, LevelMismatch>; // dedup/cache key (S9)

/// Single-span convex hull of a finite point set (S0). Precondition #min P = #max P;
/// `None` if P empty or #min ≠ #max; else `Some(from_endpoints(min P, inc(max P, 0)))`.
pub fn hull(points: &[Tumbler]) -> Option<Span>;
```

## Caller contracts & obligations

- **`Tumbler::new`** — `Err(EmptySequence)` on the empty input; admits zero/leading-zero sequences (carrier elements/sentinels, not addresses).
- **`Ord`/`cmp` on `Tumbler`** — total over **all** of carrier T including zero tumblers; lexicographic, prefix-smaller, special-cases nothing. An all-zero sequence sorts below everything (legal span lower-bound sentinel, not an admissible address).
- **`validate`** — caller hands a `Tumbler`; on success gets an `Address`, on failure `T4Error` carrying the violated clause(s). **Invariant a caller may rely on: every `Address` returned anywhere in M1 is T4-valid and correctly classified.**
- **`classify`** — total, never faults; returns `Class::Invalid` (bare) for garbage including unbounded-zero input — never wraps or overflows.
- **`zeros`** — returns the true unbounded count (`usize`); a caller must not assume ≤ 3.
- **Field projections** (`account_field`/`document_field`/`element_field`/`subspace`) — `None` when the field is absent at that address's zero-count; caller must handle absence, not assume presence.
- **Containment predicates** (`same_account`/`same_document`/`under_document`) — **field-absence ⇒ `false`**. Caller must NOT reimplement as `a.field()==b.field()` (that yields `None==None ⇒ true`, falsely equating two Node addresses). They decide from the two addresses alone — no state, coordination-free.
- **`parent`** — a single structural peel (longest T4-valid proper prefix), NOT a guaranteed level-coarsening; may take two calls to cross a level. `None` only for a single-component node. It is the *containment* projection, never derivation/version lineage.
- **`document_of`** — level-coarsening to the origin Document `Address` in one call; `None` when `zeros(a) < 2`; a Document input returns itself. Use this (not `parent`) for I-address → origin Document.
- **`add` (`⊕`)** — caller must discharge `Pos(w) ∧ actionPoint(w) ≤ #a`, else `AddPrecond`. Many-to-one: start structure below the action point is discarded (not recoverable from result + displacement).
- **`sub` (`⊖`)** — requires `a ≥ w`, else `SubPrecond`; result may be a (non-address) zero tumbler — legal here.
- **`inc`** — pure, `k ≥ 0`; `k=0` next sibling (length-preserving), `k=1` same-zeros-level version, `k=2` descends one zeros-level, `k≥3` always breaks T4. Caller must NOT mint addresses from raw `inc` without passing the gate.
- **`inc_preserves_t4` / `checked_inc`** — the TA5a gate predicate; **M3 must consult it before minting**. `checked_inc` returns `GateViolation` when the gate fails. M1 does not enforce the gate or persist any frontier.
- **`displacement`** — `Some(b⊖a)` only inside the safe window D0–D2; `None` otherwise. The `None` *forces* "store endpoints, don't recompute" — caller keeps the endpoints when it gets `None`.
- **`shift`** — precondition `n ≥ 1` (`shift(v,0)=v` total extension). **PRIMITIVE and unsafe** on a bare `doc·0·subspace` base (advances text→link silently). Caller must hold a verified full element position, or use `shift_ordinal`.
- **`ElemPos` / `shift_ordinal` / `elem_addr`** — the subspace-safe path: `shift_ordinal` advances only `ordinal`; `elem_addr` mints the `Address` guarding `doc.level()==Document`, `subspace≥1`, `ordinal≥1`, returning `ElemError` otherwise. Going through this wrapper makes the TA7a text→link mis-shift unrepresentable.
- **`Span::new`** — enforces T12 (`width>0 ∧ actionPoint(width)≤#start`), `T12Clause` otherwise; never represents "nothing" as a zero-width span.
- **`from_endpoints`** — requires `s<r ∧ #s=#r`, else `WfError`.
- **`subtree_of`** — total, returns `Span` (not `Result`); the span of every extension of `p`, for any prefix `p`.
- **`classify_spans`** — pure order, no level gate, always succeeds.
- **`intersect` / `merge` / `split` / `difference`** — require **level-uniform, mutually level-compatible operands** (all endpoints share length L), else `LevelMismatch`/`SplitError::LevelMismatch`. `intersect` → `Ok(None)` for disjoint; `merge` → `Ok(None)` for separated; `split` requires `p` strictly interior (`NotInterior` otherwise); `difference` returns a `SpanSet` of ≤ 2 spans.
- **`SpanSet::empty`** — `⟨⟩`, structurally distinct from any span; the only representation of "nothing".
- **`normalize` / `canonical_key` / `equiv` / `intersect_sets` / `difference_sets`** — fallible with `LevelMismatch` when a set is not internally level-uniform or the two are not mutually compatible. `difference_sets` has **no proven output size bound**.
- **`union`** — concatenation only: never normalizes, never fails; caller must normalize separately. Commutative/associative → coordination-free accumulate-and-merge.
- **Identity of span-sets is denotational, not structural.** Use `canonical_key` → `CanonicalForm` (`Hash + Eq`) as the dedup/cache key; never a raw `SpanSet`'s derived `Eq`/`Hash`.
- **`hull`** — precondition `#min P = #max P`; `None` for empty or mixed-length-extreme P; the result *covers* P (⊇), it does not denote P exactly. No span-set denotes an arbitrary finite point set exactly (S7) — this is interval arithmetic, not finite-set manipulation.

## Seams exposed downstream

- **`Tumbler`/`Address` → everyone (M3–M10).** Flat `Tumbler` is the storage/journal key; `Address` is the past-the-door carried value, T4-valid by standing invariant.
- **`inc` + `inc_preserves_t4`/`checked_inc` → M3.** M3's per-(home,subspace) frontier allocator calls these; M1 owns neither frontier, active-allocator set, nor durability/recovery. Contract: `inc(t,0)`=next sibling, `inc(t,k>0)`=extend by k (k=1 same-zeros-level version, k=2 descends one level); M3 must pass the gate before minting. Reuse is fatal and is M3's invariant.
- **`classify`/`Level`/field projections/containment → M3, M5, M6, M8.** M3's `ω` longest-prefix owner resolver composes `same_account`/`under_document` over its own principal registry (M1 supplies the per-address predicates incl. field-absence⇒NO; the resolver is M3's). M6/M8 registered-empty-vs-unallocated distinctions and M5's content-vs-link V-routing key on `classify`/`subspace`.
- **`subspace` → M5/M7/M8.** Content-subspace (M4) vs link-subspace (M7) referential-integrity routing.
- **`Span`/`SpanSet`/`normalize`/`classify_spans`/`intersect`/`difference`/`canonical_key` → M5, M6, M7, M8.** M7's endsets/link values are span-sets; its link-dedup coverage-class key is derived from `canonical_key` (M1 computes the canonical form; **M7 owns the class *policy*** and supplies the key to M2 — M2 never computes it). M8/M6 extent and coverage queries consume `classify_spans`/`intersect`/`difference`/membership/`subtree_of`.
- **`shift`/`ElemPos` → M3/M5.** I-stream element allocation and V-enfilade traversal driven by the ordinal shift; M1 supplies the pure value tool + subspace-safe wrapper, the stateful allocation/traversal is upstream.
- **Field/origin projectors → M6.** SHOWORIGIN's pointwise origin attribution is the pure projection here — `document_of` maps an I-address straight to its origin Document `Address` (no reassembly on M6's side); the SHOWORIGIN *operation* is M6.

## Boundary — NOT provided here

- The **allocator** — durable monotone frontier, active-allocator set, journaling, crash recovery (M3). M1 gives only pure `inc` and the gate *predicate*.
- **Ownership resolution** — the `ω` longest-prefix owner over the principal registry (M3). M1 gives only the per-address containment predicates.
- The inverse **"which spans cover address *t*"** index / spanfilade, and any scale-up interval/segment index (M7/M8). M1 hands up span *values*, not the inverse-query index.
- **Content↔byte mapping** (M4/M5).
- **Coverage-class *policy*** — which classes are equivalent for de-dup (M7). M1 owns only `canonical_key` mechanism.
- **Derivation/version lineage** — `parent`/`document_of` are containment projections, not the derivation parent; creation time and version history are a separate version graph (M3/M5).
- **No persistent state and no recovery story** of any kind in M1.
