# M1 — Interface (for dependents)

M1 owns the pure, stateless value calculus of the address space: tumbler identity & total order, T4 field-structure (validation/classification/projection/containment), position arithmetic (`⊕`/`⊖`/`inc`/shift), and the interval algebra over spans & span-sets — every function total within its stated preconditions, consulting no state, performing no I/O, leaning on nothing below ℕ.

## Public interface

Indices are **1-based** (`#t`, `actionPoint ∈ [1,#t]`). `Nat = num_bigint::BigUint` (arbitrary precision, T0(a)). `Tumbler`, `Address`, `Span`, `SpanSet`, `Level` derive `Serialize + Deserialize` so stores can journal/checkpoint them — this requires `num-bigint` built with its **`serde` feature**.

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

### B. Validation, classification, field & containment projections

```rust
#[derive(Clone, Copy, PartialEq, Eq, Serialize, Deserialize)] pub enum Level { Node, Account, Document, Element }
#[derive(Clone, Copy, PartialEq, Eq, Serialize, Deserialize)] pub enum Class { Node, Account, Document, Element, Invalid }
pub enum T4Clause { LeadingZero, TrailingZero, AdjacentZeros, OverDepth }

pub fn zeros(t: &Tumbler) -> usize;                   // separator count — UNBOUNDED (T0(b)); usize, never u8
pub fn is_t4_valid(t: &Tumbler) -> bool;
pub fn classify(t: &Tumbler) -> Class;                 // total, never faults (ASN-0045)

/// Admission constructor: the validate-and-classify front door. `T4Error` carries the
/// violated clause(s); `classify`'s `Class::Invalid` stays bare.
pub fn validate(t: Tumbler) -> Result<Address, T4Error>;

/// INVARIANT: every `Address` is T4-valid; `level` is a derived constant (immutable ⇒ never stale).
#[derive(Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
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

// Decidable containment (T6 a–d). FIELD-ABSENCE ⇒ NO: if EITHER operand lacks the required
// field, the answer is `false` — never `None == None ⇒ true`.
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
/// Precondition `n ≥ 1`; `shift(v, 0) = v` is the total extension. PRIMITIVE — unsafe for an
/// element/subspace *base* `doc·0·subspace`: a raw shift there advances text→link.
pub fn shift(v: &Tumbler, n: &Nat) -> Tumbler;

// Subspace-safe packaging — closes the TA7a hazard for callers that use it:
pub struct ElemPos { pub doc: Address, pub subspace: Nat, pub ordinal: Nat }
pub enum ElemError { DocNotDocument, SubspaceZero, OrdinalZero }

/// Mints `doc·0·subspace·ordinal`. Requires `doc.level() == Document`, `subspace ≥ 1`,
/// `ordinal ≥ 1`; the constructed tumbler is routed through `validate` defensively.
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

/// Subtree-capture (the 1-position convention): the span denoting exactly prefix p's subtree —
/// every extension of p — for ANY prefix p. Total: returns `Span`, not `Result`.
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
/// Raw `PartialEq`/`Eq`/`Hash` on SpanSet are STRUCTURAL — NOT denotational identity. Use
/// `CanonicalForm` (the unique normalized form, S9) as a dedup/cache key, never a raw `SpanSet`.
#[derive(Clone, PartialEq, Eq, Hash, Serialize, Deserialize)] pub struct SpanSet(/* im::Vector<Span> (default) */);

/// The unique normalized form (S9) as a content-addressed identity. `Hash + Eq`.
#[derive(Clone, PartialEq, Eq, Hash)] pub struct CanonicalForm(SpanSet /* normalized */);

impl SpanSet {
    pub fn empty() -> SpanSet;                          // ⟨⟩ ≜ ∅ (distinct from any zero-width span)
    pub fn singleton(s: Span) -> SpanSet;
    pub fn normalize(&self) -> Result<SpanSet, LevelMismatch>;  // unique canonical form (N1∧N2); S8/S9
    pub fn is_normalized(&self) -> bool;
    pub fn denotes(&self, t: &Tumbler) -> bool;
}
pub fn union(a: &SpanSet, b: &SpanSet) -> SpanSet;          // ⊕-free join: CONCATENATION ONLY — never normalizes, never fails
pub fn intersect_sets(a: &SpanSet, b: &SpanSet) -> Result<SpanSet, LevelMismatch>;  // normalizes inputs internally
pub fn difference_sets(a: &SpanSet, b: &SpanSet) -> Result<SpanSet, LevelMismatch>; // normalizes inputs; no proven bound
pub fn equiv(a: &SpanSet, b: &SpanSet) -> Result<bool, LevelMismatch>;  // normalize both, compare (S9)
pub fn canonical_key(s: &SpanSet) -> Result<CanonicalForm, LevelMismatch>; // dedup/cache key (S9)

/// Single-span convex hull of a finite point set (S0). Precondition `#min P = #max P`; `None`
/// if P is empty or #min ≠ #max; else a COVER (⊇ P). No span-set denotes an arbitrary finite P
/// *exactly* (every span denotes an infinite set, S7).
pub fn hull(points: &[Tumbler]) -> Option<Span>;
```

## Caller contracts & obligations

**Global invariants a caller may rely on**
- Every `Address` M1 returns is **T4-valid and correctly classified**; `.level()` is a derived constant, never stale — callers need not re-validate an `Address` they received from M1.
- `Tumbler`'s `Ord`/`cmp` is a **total order over all of carrier T including zero tumblers**, lexicographic, prefix-smaller, with no special-casing of zero separators; a zero/all-zero tumbler sorts below everything and may serve as a span lower-bound sentinel.
- All functions are **pure and total within their stated preconditions** — no I/O, no state, no recovery; values are immutable, operations yield new values.
- `Tumbler`/`Address`/`Span`/`SpanSet`/`Level` are serializable as store keys/payloads (caller must enable `num-bigint`'s `serde` feature).

**Tumbler / order**
- `Tumbler::new` — admits any nonempty `Nat` sequence (including zeros/leading-zeros); returns `Err(EmptySequence)` **only** on the empty sequence. A constructed `Tumbler` is a carrier element, **not** necessarily an address.
- `is_prefix(p,q)` — total; `p ≼ q`.

**Validation / classification / projection / containment**
- `validate(t)` — consumes the `Tumbler`; `Ok(Address)` iff T4-valid, else `Err(T4Error)` carrying the violated clause(s). The front door for minting `Address`.
- `classify(t)` / `is_t4_valid(t)` / `zeros(t)` — total, never fault; garbage (incl. unbounded-zero input) classifies `Invalid` without overflow. Use on a bare `Tumbler` when you want a tag, not an error.
- Field projections — caller must handle `None`: `account_field` `Some` iff `zeros ≥ 1`, `document_field` iff `zeros ≥ 2`, `element_field` iff `zeros = 3`; `subspace` is `element_field[0]` (1=text, 2=link), `None` if not Element.
- **Containment predicates** — `same_node`/`same_account`/`same_document`/`under_document` return **`false` whenever either operand lacks the required field** (T6 b/c/d); do **not** reimplement as `a.field() == b.field()` (that makes two Node addresses report "same account"). `same_account` needs both `zeros ≥ 1`; `same_document`/`under_document` need both `zeros ≥ 2`.

**Decomposition**
- `parent(a)` — longest T4-valid proper prefix; a **single structural peel**, not a guaranteed level-coarsening (a full element peels to its subspace-base, still Element-class); `None` only for a 1-component node. It is the containment projection, **not** the derivation/version parent.
- `document_of(a)` — origin Document `Address` (zeros=2 prefix); `None` if `zeros(a) < 2`; a Document input returns itself. Records who allocated under whom (T6(d)), **not** what was copied from what.
- `ordinal(t)` / `depth(a)` — total; `depth(a) == a.level()`.

**Position arithmetic**
- `action_point(w)` — caller must handle `None` (the zero displacement, `Zero(w)`).
- `add(a,w)` — caller must discharge `Pos(w) ∧ actionPoint(w) ≤ #a`, else `Err(AddPrecond)`. **Many-to-one**: the start is not recoverable from result + displacement in general.
- `sub(a,w)` — caller must discharge `a ≥ w`, else `Err(SubPrecond)`; the result **may be a (non-address) zero tumbler** — legal here, not an `Address`.
- `inc(t,k)` — pure/total, `k ≥ 0`; `k=0` next sibling (length-preserving), `k=1` same-zeros-level peer/version, `k=2` descends one zeros-level, `k≥3` breaks T4. **Does not enforce the gate.**
- `inc_preserves_t4(t,k)` — the TA5a gate predicate (`k∈{0,1}` always, `k=2` iff `zeros ≤ 2`, `k≥3` never); a producer **must** consult it before minting (see M3 seam).
- `checked_inc(t,k)` — `inc` + gate + reclassify; `Err(GateViolation)` if the gate fails. Mint site preserving the `Address` invariant.
- `displacement(a,b)` — `Some(b⊖a)` only under D0–D2 (`a<b`, `divergence(a,b) ≤ #a`, `#a ≤ #b`); else `None` — the API forces "store endpoints, don't recompute" outside the safe window.

**Ordinal-only shift**
- `shift(v,n)` — precondition `n ≥ 1` (`shift(v,0)=v` is the total extension). **PRIMITIVE and unguarded**: applied to a bare subspace base `doc·0·subspace` it silently advances text→link. Use only when holding a verified full element position.
- `elem_addr(p)` — mints `doc·0·subspace·ordinal`; `Err(DocNotDocument)` unless `doc.level()==Document`, `Err(SubspaceZero)` if `subspace < 1`, `Err(OrdinalZero)` if `ordinal < 1`; routes through `validate`. Mint site.
- `shift_ordinal(p,n)` — subspace-safe: advances `ordinal` by `n` only, subspace untouched; makes the text→link mis-shift unrepresentable for callers that go through it; validity is re-discharged at `elem_addr`.

**Spans**
- `Span::new(start,width)` — caller must satisfy T12 (`width>0 ∧ actionPoint(width) ≤ #start`), else `Err(T12Clause)`. Use `SpanSet::empty()` for "nothing" — a zero-width span is rejected.
- `Span::from_endpoints(s,r)` — caller must satisfy WF (`s<r ∧ #s=#r`), else `Err(WfError::{NotIncreasing|LevelMismatch})`.
- `reach()` — derived, never authoritative/persisted; `contains(t)` is `start ≤ t < reach`; `is_level_uniform()` is `#start==#width`.
- `subtree_of(p)` — **total** (returns `Span`, not `Result`); the span of exactly `p`'s subtree, for any prefix `p` (incl. trailing-zero).
- `classify_spans(a,b)` — pure order, **no level gate**, total; 5 mutually-exclusive `SpanRel`.
- `intersect`/`merge`/`split`/`difference` — all require **mutually level-compatible (level-uniform) operands**; `Err(LevelMismatch)` otherwise. `intersect` returns `Ok(None)` when disjoint; `merge` returns `Ok(None)` when separated; `split` needs `start < p < reach` strictly interior (else `Err(SplitError::NotInterior)`); fan-outs are bounded (`intersect ≤1`, `merge =1`, `difference ≤2`).

**Span-sets**
- **Identity**: raw `SpanSet` `Eq`/`Hash` are **structural** (they distinguish un-normalized forms) — never use them as a dedup/cache key. Use `CanonicalForm` from `canonical_key` for denotational identity.
- `SpanSet::empty()` — `⟨⟩`, structurally distinct from any span; `singleton(s)`.
- `normalize` / `equiv` / `canonical_key` / `intersect_sets` / `difference_sets` — all return `Err(LevelMismatch)` when a set is not internally level-uniform or the two sets are not mutually level-compatible. `difference_sets` carries **no proven size bound**.
- `union(a,b)` — **concatenation only**: never normalizes, never fails, total; the **caller** must normalize. Commutative/associative ⇒ workers may accumulate and merge in any order to a deterministic canonical result.
- `canonical_key(s)` — the unique normalized form (S9) as `CanonicalForm`; this is the dedup/cache-key primitive (e.g. M7's coverage-class key is derived from it).
- `hull(points)` — precondition `#min P = #max P`; `None` if `P` empty or `#min ≠ #max`; else a single-span **cover** (⊇ P), not an exact denotation. No span-set denotes an arbitrary finite `P` exactly.

## Seams exposed downstream

- **`Tumbler`/`Address` → everyone (M3–M10).** The universal key/endpoint/classification type. Flat `Tumbler` is the storage/journal key; `Address` is the past-the-door carried value, T4-valid by its standing invariant.
- **`inc` + `inc_preserves_t4`/`checked_inc` → M3.** M3's per-(home,subspace) frontier allocator *calls* these; it **must** pass `inc_preserves_t4`/`checked_inc` before minting. M1 owns neither the frontier, the active-allocator set, nor durability/recovery. Over-shooting (gaps/ghosts) is harmless to the algebra; reuse is fatal — that durability invariant is M3's.
- **`classify`/`Level`/field projections/containment → M3, M5, M6, M8.** M3's `ω` longest-prefix owner resolver composes `same_account`/`under_document` over its principal registry (M1 gives the per-address predicates incl. field-absence⇒NO; the resolver is M3's). M6/M8 registered-empty-vs-unallocated distinctions and M5's content-vs-link V-position routing key on `classify`/`subspace`.
- **`subspace` → M5/M7/M8.** Drives content-subspace (M4-targeted) vs link-subspace (M7-targeted) referential-integrity routing.
- **`Span`/`SpanSet`/`normalize`/`classify_spans`/`intersect`/`difference`/`canonical_key`/`subtree_of` → M5, M6, M7, M8.** M7's endsets/link values are span-sets; its link-dedup coverage-class key is derived from `canonical_key` (M1 computes the canonical form on level-uniform inputs; **M7 decides the class policy** and supplies the key to M2 — M2 never computes it). M8's coverage/discovery and M6's extent queries consume `classify_spans`/`intersect`/`difference`/membership/`subtree_of`.
- **`shift`/`ElemPos`/`shift_ordinal`/`elem_addr` → M3/M5.** I-stream element allocation and V-enfilade traversal are driven by the ordinal shift; M1 supplies the pure value tool and the subspace-safe wrapper, the stateful allocation/traversal is upstream.
- **Field/origin projectors (`document_of`, `document_field`, `under_document`, `parent`) → M6.** SHOWORIGIN's *pointwise* origin attribution is the pure projection here — `document_of` maps an I-address straight to its origin Document `Address` (no reassembly from raw components on M6's side); the SHOWORIGIN *operation* is M6.

## Boundary — NOT provided here

- **Allocator** — durable monotone frontier, active-allocator set, journaling, crash recovery (**M3**); M1 gives only pure `inc` and the `inc_preserves_t4` gate *predicate*.
- **Ownership resolution** — the `ω` longest-prefix owner over the principal registry (**M3**); M1 gives only the per-address containment predicates `ω` is built from.
- **Inverse coverage index** — "which spans cover address *t*" / the spanfilade, and any scale-up interval/segment index (**M7/M8**); M1 hands up span *values*, not the index.
- **Content↔byte mapping** (**M4/M5**).
- **SHOWORIGIN operation** — the I-span/V-span resolution against arrangement state (**M6**); M1 gives only the pointwise field/document-prefix projectors.
- **Derivation/version lineage** — `parent`/`document_of` are containment projections, not creation-time/version history (separate version graph, **M3/M5**).
- **Zero-sentinel span semantics** — how `contains`/`intersect`/`classify_spans` treat an unbounded (all-zero) endpoint is **left genuinely open**; do not build against a settled convention here.
