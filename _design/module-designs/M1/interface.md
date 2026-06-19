# M1 — Interface (for dependents)

M1 owns the pure, stateless value-level calculus of the address space: tumbler identity and total order, T4 field-structure (validation/classification/projection/containment), position arithmetic (`⊕`/`⊖`/`inc`/`sig`/ordinal shift), and the interval algebra over spans and span-sets. Every function is total within its stated preconditions, consults no state, performs no I/O, and leans on nothing below ℕ.

## Public interface

Indices are **1-based** (to match the spec); implement over 0-based storage. `Nat = num_bigint::BigUint` (arbitrary precision). `Tumbler`, `Address`, `Span`, `SpanSet`, `Level` derive **`Serialize + Deserialize`** (a store cannot journal/checkpoint them otherwise); this requires `num-bigint` built with its **`serde` feature**.

```rust
// Error types referenced throughout (T4Clause/T12Clause/ElemError declared with their ops below):
pub struct EmptySequence;                                 // Tumbler::new on the empty sequence (T0)
pub struct T4Error { /* the violated T4Clause(s) ONLY — does NOT carry the rejected Tumbler */ }
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
pub type Pos = usize;                 // 1-based component index

#[derive(Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct Tumbler(/* immutable sequence of Nat, len ≥ 1 */);

impl Tumbler {
    /// Carrier admission only (T0): rejects the empty sequence; admits zero/leading-zero
    /// sequences (legal carrier elements and span sentinels — NOT addresses).
    pub fn new(comps: impl IntoIterator<Item = Nat>) -> Result<Tumbler, EmptySequence>;
    pub fn len(&self) -> usize;                       // #t
    pub fn get(&self, i: Pos) -> &Nat;                // tᵢ — 1-based; PANICS on i = 0 or i > #t
}

impl PartialOrd for Tumbler { /* delegates to `cmp` */ }
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
pub fn classify(t: &Tumbler) -> Class;                // total, never faults (ASN-0045)

/// validate-and-classify front door. CONSUMES `t`; T4Error carries the violated clause(s) only.
pub fn validate(t: Tumbler) -> Result<Address, T4Error>;

/// A T4-valid, classified tumbler. INVARIANT: every `Address` is T4-valid; `level` is a derived constant.
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

// Decidable containment (T6 a–d). FIELD-ABSENCE ⇒ NO: if EITHER operand lacks the required field, false.
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
pub fn depth(a: &Address) -> Level;                  // ALIAS of a.level(), NOT a numeric nesting count
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

/// b ⊖ a only when the round-trip a ⊕ (b⊖a) = b is guaranteed (D0–D2: a<b, divergence(a,b)≤#a, #a≤#b).
/// Otherwise None — store endpoints, don't recompute.
pub fn displacement(a: &Tumbler, b: &Tumbler) -> Option<Tumbler>;
```

### E. Ordinal-only shift (element stream)

```rust
/// Ordinal-only shift: v ⊕ δ(n,#v). Precond `n ≥ 1`; `shift(v,0)=v` is the total extension.
/// PRIMITIVE — unsafe for a `doc·0·subspace` base (advances text→link); prefer `shift_ordinal`.
pub fn shift(v: &Tumbler, n: &Nat) -> Tumbler;

pub struct ElemPos { pub doc: Address, pub subspace: Nat, pub ordinal: Nat }
pub enum ElemError { DocNotDocument, SubspaceZero, OrdinalZero }

/// Mints `doc·0·subspace·ordinal`; requires doc.level()==Document, subspace≥1, ordinal≥1.
pub fn elem_addr(p: &ElemPos) -> Result<Address, ElemError>;
pub fn shift_ordinal(p: &ElemPos, n: &Nat) -> ElemPos;    // ordinal += n only (subspace untouched)
```

### F. Spans

```rust
#[derive(Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct Span { start: Tumbler, width: Tumbler }        // reach derived; (start,width) authoritative
pub enum T12Clause { ZeroWidth, ActionPointTooDeep }

impl Span {
    pub fn new(start: Tumbler, width: Tumbler) -> Result<Span, T12Clause>;   // T12: width>0 ∧ actionPoint(width)≤#start
    pub fn from_endpoints(s: Tumbler, r: Tumbler) -> Result<Span, WfError>;  // WF: s<r ∧ #s=#r
    pub fn start(&self) -> &Tumbler;
    pub fn width(&self) -> &Tumbler;
    pub fn reach(&self) -> Tumbler;            // start ⊕ width — recomputed/cached, never persisted
    pub fn contains(&self, t: &Tumbler) -> bool;        // start ≤ t < reach
    pub fn is_level_uniform(&self) -> bool;             // #start == #width
}

/// The span denoting exactly prefix p's subtree (every extension of p, T5), for ANY prefix p. Total.
pub fn subtree_of(p: &Tumbler) -> Span;                  // from_endpoints(p, shift(p, &1))

pub enum SpanRel { Separated, Adjacent, ProperOverlap, Containment, Equal }  // SC
pub fn classify_spans(a: &Span, b: &Span) -> SpanRel;                         // pure order — no level gate
pub fn intersect(a: &Span, b: &Span) -> Result<Option<Span>, LevelMismatch>; // ≤ 1
pub fn merge(a: &Span, b: &Span)     -> Result<Option<Span>, LevelMismatch>; // = 1 when overlap/adjacent
pub fn split(s: &Span, p: &Tumbler)  -> Result<(Span, Span), SplitError>;    // p strictly interior, σ level-uniform
pub fn difference(a: &Span, b: &Span)-> Result<SpanSet, LevelMismatch>;      // ≤ 2 (S11d)
```

### G. Span-sets

```rust
/// Raw PartialEq/Eq/Hash are STRUCTURAL (distinguish un-normalized forms), NOT denotational identity.
#[derive(Clone, PartialEq, Eq, Hash, Serialize, Deserialize)] pub struct SpanSet(/* im::Vector<Span> (default) */);

/// The unique normalized form (S9) as content-addressed identity. NOT Serialize/Deserialize (in-memory key).
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

/// Single-span convex hull of a finite point set (S0). Precond #min P = #max P; None if empty or #min≠#max.
pub fn hull(points: &[Tumbler]) -> Option<Span>;

/// S7 unit-span cover: one unit span per point, |Σ|=|P|, ⟦Σ⟧⊇P (a COVER, not exact). NOT normalized. cover(&[])=empty().
pub fn cover(points: &[Tumbler]) -> SpanSet;
```

## Caller contracts & obligations

**Tumbler / order**
- `Tumbler::new` — handle `Err(EmptySequence)`; it admits zero/leading-zero sequences (legal as span sentinels, **not** addresses — they are not T4-valid).
- `Tumbler::get(i)` — 1-based; you must ensure `1 ≤ i ≤ len`, else it **PANICS**.
- `Ord`/`cmp` is total over **all** of carrier T including zero tumblers (prefix-smaller; positive > zero); consults nothing external. `==` is sequence equality.

**Validation / classification / Address invariant**
- `validate` **consumes `t`**; on `Err(T4Error)` the input is dropped (`T4Error` carries only the violated clause(s), not the tumbler) — `clone` before calling if you need it back.
- `classify` is total and never faults; garbage yields `Class::Invalid` (bare, no clause).
- **Invariant you may rely on:** every `Address` M1 returns is T4-valid — *checked* by `validate`/`elem_addr`, *preserved* by `parent`/`document_of`/`checked_inc`. `Address.level()` is a derived constant, never stale.
- Field projections: `node_field` is always present (`&[Nat]`); `account_field` `Some` iff `zeros ≥ 1`; `document_field` iff `zeros ≥ 2`; `element_field` iff `zeros = 3`; `subspace` = `element_field[0]` (1=text, 2=link).
- Containment (`same_node`/`same_account`/`same_document`/`under_document`): **field-absence ⇒ `false`** — if either operand lacks the required field the answer is `false` (two Node addresses do **not** report "same account"). Decidable from the two addresses alone.

**Decomposition**
- `parent` — longest T4-valid proper prefix; `None` only for a single-component node. It is a single structural peel, **not** a guaranteed level-coarsening (an element may take two peels) and **not** the derivation parent.
- `document_of` — origin Document `Address`; `None` if `zeros(a) < 2`; a Document input returns itself. Use this (not `parent`) for I-address → origin Document.
- `depth(a)` is an alias of `a.level()`, not a numeric count.

**Position arithmetic**
- `action_point` — `None` iff `Zero(w)`. `sig` — last nonzero index, else `#t`.
- `add` (`⊕`) — precond `Pos(w) ∧ actionPoint(w) ≤ #a`, else `Err(AddPrecond)`. Many-to-one: the start is not recoverable from result+displacement in general.
- `sub` (`⊖`) — precond `a ≥ w`, else `Err(SubPrecond)`; the result may be a (non-address) Zero tumbler.
- `inc(t,k)` — pure, `k ≥ 0`: `k=0` next sibling (length-preserving); `k=1` same-zeros-level version; `k=2` descends one zeros-level; `k≥3` always breaks T4.
- `inc_preserves_t4` (TA5a gate): true for `k∈{0,1}`, `k=2` iff `zeros(t) ≤ 2`, `k≥3` never. **A minting producer (M3) MUST pass this before minting**; enforcement and the frontier are the producer's obligation, not M1's.
- `checked_inc` — `inc` + gate + reclassify; `Err(GateViolation)` if the gate fails; returns a T4-valid `Address`.
- `displacement(a,b)` — `Some(b⊖a)` only under D0–D2 (`a<b`, `divergence≤#a`, `#a≤#b`); otherwise `None` — **store the endpoints, do not recompute** (proper-prefix `a` is correctly excluded).

**Ordinal shift**
- `shift` — precond `n ≥ 1`; `shift(v,0)=v`. **PRIMITIVE hazard:** a raw shift of a `doc·0·subspace` base advances text→link — only call on a verified full element position, or go through `shift_ordinal`/`ElemPos`, which make the mis-shift unrepresentable for callers that use them.
- `elem_addr` — requires `p.doc.level()==Document` (else `DocNotDocument`), `subspace ≥ 1` (else `SubspaceZero`), `ordinal ≥ 1` (else `OrdinalZero`); returns a T4-valid `Address`.
- `shift_ordinal` — pure `ElemPos → ElemPos`, `ordinal += n` only; validity is re-discharged when materialized by `elem_addr`. `ElemPos` models only the 2-component `subspace·ordinal` field — longer element fields are built via `Tumbler::new(...)` + `validate`, so `elem_addr` is not the sole element-construction path.

**Spans**
- `Span::new` — `Err(T12Clause::{ZeroWidth | ActionPointTooDeep})`. The empty designation is `SpanSet::empty()`, never a zero-width span.
- `Span::from_endpoints(s,r)` — `Err(WfError::{NotIncreasing | LevelMismatch})`.
- `Span::reach` is a recomputed/cached derivation — never persist it as authoritative.
- `subtree_of` is total (returns `Span`, not `Result`); denotes exactly `p`'s subtree (every extension of `p`) for any prefix `p`.
- `classify_spans` — pure order, 5 mutually-exclusive cases, no level gate.
- `intersect` — `≤1`; self-guarding (disjoint ⇒ `Ok(None)`); `Err(LevelMismatch)` if not level-compatible.
- `merge` — `=1` when overlap/adjacent, `Ok(None)` when separated; `Err(LevelMismatch)`.
- `split(s,p)` — `p` strictly interior (`start<p<reach`) and `σ` level-uniform, else `Err(SplitError::{NotInterior | LevelMismatch})`; returns two adjacent spans.
- `difference` — `≤2` spans; `Err(LevelMismatch)`. No algebra result ever carries a zero-width member.

**Span-sets**
- **Level gate:** `intersect`/`merge`/`split`/`difference`/`normalize`/`canonical_key`/`equiv`/`intersect_sets`/`difference_sets` all require mutually level-compatible (equal-length) endpoints, else `LevelMismatch`.
- `union` — concatenation only; never normalizes, never fails. Commutative/associative (a join-semilattice within one tumbler length) — workers may accumulate/merge in any order; **you must normalize** for a canonical/minimal form.
- `intersect_sets`/`difference_sets` — normalize their inputs internally and emit normalized results; `difference_sets` has **no proven size bound**.
- `equiv` — normalize both and compare. `canonical_key` — the unique normalized form as `CanonicalForm` (`Hash + Eq`), the denotational dedup/cache key.
- **Identity:** raw `SpanSet` `Eq`/`Hash` are structural — never use as a dedup key; use `CanonicalForm`. `CanonicalForm` is **not** `Serialize`/`Deserialize` (in-memory, rebuilt by replay).
- `hull` — precond `#min P = #max P`; `None` if `P` empty or `#min ≠ #max`; covers even a mixed-length `P`.
- `cover` — one unit span per point, `|Σ|=|P|`, `⊇P` (a cover, not exact); **not normalized** (you normalize for a minimal form); admits mixed-length `P`; `cover(&[]) = empty()`.

**Serde:** `Tumbler`, `Address`, `Span`, `SpanSet`, `Level` derive `Serialize + Deserialize` — a store's keys/payloads journal/checkpoint through these; build `num-bigint` with its `serde` feature.

## Seams exposed downstream

- **`Tumbler`/`Address` → every module (M3–M10):** the universal key/endpoint/classification type. Flat `Tumbler` is the storage/journal key; `Address` is the past-the-door carried value, T4-valid by standing invariant.
- **`inc` + `inc_preserves_t4`/`checked_inc` → M3:** M3's per-(home,subspace) frontier allocator *calls* these. M1 owns neither the frontier, the active-allocator set, nor durability/recovery. Contract: `inc(t,0)` = next sibling, `inc(t,k>0)` = extend by `k`; M3 **must** pass `inc_preserves_t4` before minting. Over-shooting is harmless to M1; reuse is fatal — that durability invariant is M3's.
- **`classify`/`Level`/field projections/containment → M3, M5, M6, M8:** M3's `ω` longest-prefix owner resolver composes `same_account`/`under_document` over its principal registry (M1 gives the per-address predicates incl. field-absence⇒NO; the resolver is M3's). M6/M8 registered-empty-vs-unallocated query distinctions and M5's S3★ content-vs-link routing key on `classify`/`subspace`.
- **`subspace` → M5/M7/M8:** content-subspace (M4-targeted) vs link-subspace (M7-targeted) referential-integrity routing.
- **`Span`/`SpanSet`/`normalize`/`classify_spans`/`intersect`/`difference`/`canonical_key` → M5, M6, M7, M8:** M7's endsets/link values are span-sets; its link-dedup coverage-class key is derived from `canonical_key` (M1 computes the canonical form; M7 decides the class *policy* and supplies the key to M2's keyed critical section — M2 never computes it). M8's coverage/discovery and M6's extent queries consume `classify_spans`/`intersect`/`difference`/membership/`subtree_of`/`cover`.
- **`shift`/`ElemPos` → M3/M5:** I-stream element allocation and V-enfilade traversal; M1 supplies the pure value tool and the subspace-safe wrapper, the stateful allocation/traversal is upstream.
- **Field/origin projectors → M6:** SHOWORIGIN's pointwise origin attribution is the pure field/document-prefix projection here — `document_of` maps an I-address straight to its origin Document `Address` (no reassembly on M6's side). The SHOWORIGIN *operation* (reads arrangement state) is M6.

## Boundary — NOT provided here

- **Allocator** (M3): durable monotone frontier, active-allocator set, journaling, crash recovery. M1 supplies only pure `inc` and the TA5a gate *predicate* — enforcing the gate and persisting the frontier is M3's.
- **Inverse coverage index** "which spans cover *t*" / spanfilade, and any scale-up interval/segment index (M7/M8). M1 hands up span *values*, not the index.
- **Content↔byte mapping** (M4/M5).
- **Ownership resolution:** the `ω` longest-prefix owner over the principal registry (M3). M1 gives only the per-address containment predicates `ω` is built from.
- **Upstream dependencies:** none — M1 leans only on ℕ (`num-bigint`); it carries no edge to M2.
