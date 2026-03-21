# ASN-0058 Formal Statements

*Source: ASN-0058-permutation-model.md (revised 2026-03-20) — Extracted: 2026-03-20*

## Definition — MappingBlock

A mapping block `β = (v, a, n)` consists of:
- `v ∈ T` — the V-start (a position in the document's virtual stream)
- `a ∈ T` — the I-start (an address in the permanent content store)
- `n ∈ ℕ` with `n ≥ 1` — the width (count of positions mapped)

It denotes the set of position-address pairs:

`⟦β⟧ = {(v + k, a + k) : 0 ≤ k < n}`

where `v + k` and `a + k` denote `k` ordinal increments via TA5(c) (ASN-0034). The *V-extent* is `V(β) = {v + k : 0 ≤ k < n}`; the *I-extent* is `I(β) = {a + k : 0 ≤ k < n}`.

---

## Definition — BlockDecomposition

A *block decomposition* of the text-subspace arrangement of document `d` is a finite set `B = {β₁, ..., βₘ}` of mapping blocks satisfying:

(B1) *Coverage.* `(A v ∈ dom(M(d)) : v₁ ≥ 1 : (E! j : 1 ≤ j ≤ m : v ∈ V(βⱼ)))`

(B2) *Disjointness.* `(A i, j : 1 ≤ i < j ≤ m : V(βᵢ) ∩ V(βⱼ) = ∅)`

(B3) *Consistency.* `(A j : 1 ≤ j ≤ m : (A k : 0 ≤ k < nⱼ : M(d)(vⱼ + k) = aⱼ + k))`

The empty arrangement `M(d) = ∅` has `B = ∅` as its unique decomposition.

---

## Definition — DecompositionEquivalence

Block decompositions `B` and `B'` of `M(d)` are *equivalent*, written `B ≡ B'`, when:

`⋃{⟦β⟧ : β ∈ B} = ⋃{⟦β⟧ : β ∈ B'}`

---

## Definition — InteriorPoint

An integer `c` is *interior* to block `β = (v, a, n)` when `0 < c < n`.

---

## Definition — VAdjacent

Blocks `β₁ = (v₁, a₁, n₁)` and `β₂ = (v₂, a₂, n₂)` with `v₁ < v₂` are *V-adjacent* when `v₂ = v₁ + n₁`.

---

## Definition — IAdjacent

Blocks `β₁` and `β₂` (with `v₁ < v₂`) are *I-adjacent* when `a₂ = a₁ + n₁`.

---

## Definition — MaximallyMerged

A block decomposition `B` is *maximally merged* when no two blocks in `B` satisfy the merge condition (M7). For every pair `βᵢ, βⱼ ∈ B` with `i ≠ j`: they are not V-adjacent, or they are not I-adjacent, or both.

---

## Definition — MaximalRun

A *maximal run* of `f = M(d)` is a triple `(v, a, n)` such that:
1. `(A k : 0 ≤ k < n : f(v + k) = a + k)`
2. `¬(E v' :: v' + 1 = v ∧ v' ∈ dom(f) ∧ f(v') + 1 = a)`
3. `v + n ∉ dom(f)  ∨  f(v + n) ≠ a + n`

(Condition 2 uses only TumblerAdd, avoiding TumblerSub. The condition is vacuously satisfied when the last component of `v` equals 1.)

---

## Definition — BlockMerge

`β₁ ⊞ β₂ = (v₁, a₁, n₁ + n₂)`

(`⊞` denotes block merge, distinct from tumbler addition `⊕`.)

---

## M0 — WidthCoupling (INV, predicate)

For every mapping block `β = (v, a, n)`:

`|V(β)| = |I(β)| = n`

---

## M1 — OrderPreservation (INV, predicate)

Within a mapping block `β = (v, a, n)`, for all `j, k` with `0 ≤ j < k < n`:

`v + j < v + k  ∧  a + j < a + k`

---

## M-aux — OrdinalIncrementAssociativity (LEMMA, lemma)

For any tumbler `v` and natural numbers `c, j`:

`(v + c) + j = v + (c + j)`

*Convention:* `v + 0 = v`.

---

## M2 — DecompositionExistence (LEMMA, lemma)

Every arrangement `M(d)` admits a block decomposition of its text subspace.

---

## M3 — RepresentationInvariance (LEMMA, lemma)

If `B ≡ B'`, then for every `v ∈ dom(M(d))`, the I-address determined by `B` equals the I-address determined by `B'`.

---

## M4 — SplitDefinition (DEF, function)

For a mapping block `β = (v, a, n)` and interior point `0 < c < n`, the *split at `c`* produces:

```
β_L = (v, a, c)
β_R = (v + c, a + c, n − c)
```

Both are well-formed mapping blocks: `c ≥ 1` and `n − c ≥ 1` (since `0 < c < n`).

---

## M5 — SplitPartition (LEMMA, lemma)

(a) `⟦β_L⟧ ∪ ⟦β_R⟧ = ⟦β⟧`

(b) `⟦β_L⟧ ∩ ⟦β_R⟧ = ∅`

---

## M6 — SplitPreservation (LEMMA, lemma)

Each piece independently preserves:

(a) *Width coupling.* `|V(β_L)| = |I(β_L)| = c` and `|V(β_R)| = |I(β_R)| = n − c`.

(b) *Order preservation.* Both `β_L` and `β_R` satisfy M1.

(c) *I-address fidelity.* For every pair `(v + k, a + k)` in `⟦β⟧`, the same pair appears in exactly one of `⟦β_L⟧` or `⟦β_R⟧`. No I-address is altered, dropped, or duplicated.

(d) *Origin traceability.* `origin(a + k) = origin(a)` for all `k`, since ordinal increment preserves the document prefix. Since the split alters no I-address, each piece independently identifies the home document of its content.

(e) *Structural independence.* Each piece is a self-contained mapping block whose well-formedness depends only on its own `(v, a, n)` triple.

---

## M6f — SplitFrame (LEMMA, lemma)

If `B` is a decomposition of `M(d)` containing `β`, then `(B \ {β}) ∪ {β_L, β_R}` is also a decomposition of `M(d)`, and the two decompositions are equivalent. All blocks in `B \ {β}` are unchanged.

---

## M7 — MergeCondition (DEF, function)

Two blocks `β₁ = (v₁, a₁, n₁)` and `β₂ = (v₂, a₂, n₂)` with `v₁ < v₂` may be merged into a single block if and only if:

`v₂ = v₁ + n₁  ∧  a₂ = a₁ + n₁`

When both conditions hold: `β₁ ⊞ β₂ = (v₁, a₁, n₁ + n₂)`

---

## M7f — MergeFrame (LEMMA, lemma)

If `B` is a decomposition of `M(d)` containing both `β₁` and `β₂` satisfying M7, then `(B \ {β₁, β₂}) ∪ {β₁ ⊞ β₂}` is an equivalent decomposition. All blocks in `B \ {β₁, β₂}` are unchanged.

---

## M8 — MergeInformationLoss (LEMMA, lemma)

Given only `β₁ ⊞ β₂ = (v₁, a₁, n₁ + n₂)`, the individual widths `n₁` and `n₂` cannot be recovered. The merged block is indistinguishable from one that was never split.

---

## M9 — SplitMergeInverse (LEMMA, lemma)

For any mapping block `β = (v, a, n)` and interior point `0 < c < n`:

```
split(β, c) = (β_L, β_R)
  where β_L = (v, a, c) and β_R = (v + c, a + c, n − c)

V-adjacency: v + c = v + c  ✓
I-adjacency: a + c = a + c  ✓

β_L ⊞ β_R = (v, a, c + (n − c)) = (v, a, n) = β
```

---

## M10 — MergeSplitInverse (LEMMA, lemma)

For any blocks `β₁ = (v₁, a₁, n₁)` and `β₂ = (v₂, a₂, n₂)` satisfying the merge condition (`v₂ = v₁ + n₁`, `a₂ = a₁ + n₁`):

```
split(β₁ ⊞ β₂, n₁)
  = ((v₁, a₁, n₁), (v₁ + n₁, a₁ + n₁, n₂))
  = (β₁, β₂)
```

---

## M11 — CanonicalExistence (LEMMA, lemma)

Every arrangement `M(d)` admits a maximally merged block decomposition.

---

## M12 — CanonicalUniqueness (LEMMA, lemma)

The maximally merged decomposition is unique (equals the set of maximal runs of `M(d)`).

Specifically:
- The maximal runs partition `dom(f)`: every `v ∈ dom(f)` belongs to exactly one maximal run.
- A decomposition `B` is maximally merged iff it equals the set of maximal runs of `f`.
- The maximal runs are uniquely determined by `f = M(d)`.

*Uniqueness of maximal runs:* Suppose `v ∈ R₁ ∩ R₂` where `R₁ = (v₁, a₁, n₁)` and `R₂ = (v₂, a₂, n₂)` with `v₁ ≤ v₂`. Then `v₁ = v₂`, `a₁ = a₂`, and `n₁ = n₂`.

---

## M13 — SharedContent (LEMMA, lemma)

`(E Σ : Σ satisfies S0–S3 : (E d, a :: |{v : M(d)(v) = a}| > 1))`

---

## M14 — IndependentOccurrences (LEMMA, lemma)

When two mapping blocks `β₁ = (v₁, a, n)` and `β₂ = (v₂, a, n)` in a decomposition share their I-start and width (with `v₁ ≠ v₂`), they cannot be merged.

*Condition:* The merge condition (M7) requires `a₂ = a₁ + n₁`. Here `a₂ = a₁ = a`, so the condition requires `a = a + n`. Since `n ≥ 1`, `a + n > a` by TA-strict (ASN-0034), so `a + n ≠ a`. The I-adjacency condition is unsatisfiable.

---

## M15 — MappingIndependence (LEMMA, lemma)

For any two documents `d₁ ≠ d₂`:

(a) Membership of a triple `(v, a, n)` in a decomposition of `M(d₁)` entails no relationship to any decomposition of `M(d₂)`.

(b) Splitting or merging blocks in a decomposition of `M(d₁)` does not alter any block in any decomposition of `M(d₂)`.

---

## M16 — CrossOriginMergeImpossibility (LEMMA, lemma)

`(A β₁, β₂ : origin(a₁) ≠ origin(a₂) : ¬(a₂ = a₁ + n₁))`

*Key fact used:* Ordinal increment via TA5(c) changes only the last significant component of a tumbler; the document prefix (`N.0.U.0.D` portion) is invariant under ordinal increment. Therefore `origin(a₁ + n₁) = origin(a₁)`. If `origin(a₂) ≠ origin(a₁)`, then `a₂ ≠ a₁ + n₁`.

---

## B1 — Coverage (INV, predicate)

Every text-subspace V-position in `dom(M(d))` appears in exactly one block:

`(A v ∈ dom(M(d)) : v₁ ≥ 1 : (E! j : 1 ≤ j ≤ m : v ∈ V(βⱼ)))`

---

## B2 — Disjointness (INV, predicate)

No two blocks share a V-position:

`(A i, j : 1 ≤ i < j ≤ m : V(βᵢ) ∩ V(βⱼ) = ∅)`

---

## B3 — Consistency (INV, predicate)

Each block correctly describes `M(d)`:

`(A j : 1 ≤ j ≤ m : (A k : 0 ≤ k < nⱼ : M(d)(vⱼ + k) = aⱼ + k))`
