# ASN-0058 Formal Statements

*Source: ASN-0058-permutation-model.md (revised 2026-03-22) — Extracted: 2026-03-22*

## Definition — MappingBlock

A mapping block `β = (v, a, n)` consists of:
- `v ∈ T` — the V-start
- `a ∈ T` — the I-start
- `n ∈ ℕ` with `n ≥ 1` — the width

It denotes the set of position-address pairs:

`⟦β⟧ = {(v + k, a + k) : 0 ≤ k < n}`

The *V-extent* is `V(β) = {v + k : 0 ≤ k < n}`; the *I-extent* is `I(β) = {a + k : 0 ≤ k < n}`.

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

## Definition — BlockDecomposition

A *block decomposition* of the text-subspace arrangement of document `d` is a finite set `B = {β₁, ..., βₘ}` of mapping blocks satisfying:

(B1) *Coverage.* `(A v ∈ dom(M(d)) : v₁ ≥ 1 : (E! j : 1 ≤ j ≤ m : v ∈ V(βⱼ)))`

(B2) *Disjointness.* `(A i, j : 1 ≤ i < j ≤ m : V(βᵢ) ∩ V(βⱼ) = ∅)`

(B3) *Consistency.* `(A j : 1 ≤ j ≤ m : (A k : 0 ≤ k < nⱼ : M(d)(vⱼ + k) = aⱼ + k))`

---

## Definition — DecompositionEquivalence

Block decompositions `B` and `B'` of `M(d)` are *equivalent*, written `B ≡ B'`, when:

`⋃{⟦β⟧ : β ∈ B} = ⋃{⟦β⟧ : β ∈ B'}`

---

## Definition — MaximallyMerged

A block decomposition `B` is *maximally merged* when no two blocks in `B` satisfy the merge condition (M7). For every pair `βᵢ, βⱼ ∈ B` with `i ≠ j`: they are not V-adjacent, or they are not I-adjacent, or both.

---

## Definition — MaximalRun

A *maximal run* of `f` is a triple `(v, a, n)` such that:
1. `(A k : 0 ≤ k < n : f(v + k) = a + k)`
2. `¬(E v' :: v' + 1 = v ∧ v' ∈ dom(f) ∧ f(v') + 1 = a)`
3. `v + n ∉ dom(f)  ∨  f(v + n) ≠ a + n`

---

## Definition — BlockMerge

When `β₁ = (v₁, a₁, n₁)` and `β₂ = (v₂, a₂, n₂)` satisfy the merge condition, the merged block is:

`β₁ ⊞ β₂ = (v₁, a₁, n₁ + n₂)`

---

## Definition — ContentReference

A *content reference* is a pair `(d_s, σ)` where `d_s ∈ D` and `σ = (u, ℓ)` is a level-uniform V-span satisfying:
- (i) `V_{u₁}(d_s) ≠ ∅`
- (ii) T12 (ASN-0034) holds
- (iii) `#ℓ = #u = m`, where `m` is the common V-position depth in subspace `u₁` of `d_s` (S8-depth, ASN-0036)
- (iv) `m ≥ 2`

The content reference is well-formed when:

`{v ∈ T : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d_s))`

---

## Definition — ContentReferenceSequence

A *content reference sequence* is an ordered list `R = ⟨r₁, ..., rₚ⟩` of content references with `p ≥ 1`. Different references may name different source documents.

---

## Definition — Resolution

Given content reference `(d_s, σ)` with `σ = (u, ℓ)`, let `f = M(d_s)|⟦σ⟧` be the restriction of `M(d_s)` to positions in `⟦σ⟧`.

The decomposition of `f` yields `⟨β₁, ..., βₖ⟩` ordered by V-start. The *I-address sequence* is:

`resolve(d_s, σ) = ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩`

where `βⱼ = (vⱼ, aⱼ, nⱼ)`.

For a content reference sequence `R = ⟨r₁, ..., rₚ⟩`:

`resolve(R) = resolve(r₁) ⌢ ... ⌢ resolve(rₚ)`

The *total width* of an I-address sequence `⟨(a₁, n₁), ..., (aₖ, nₖ)⟩` is:

`w(⟨(a₁, n₁), ..., (aₖ, nₖ)⟩) = (+ j : 1 ≤ j ≤ k : nⱼ)`

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

---

## M5 — SplitPartition (LEMMA, lemma)

(a) `⟦β_L⟧ ∪ ⟦β_R⟧ = ⟦β⟧`

(b) `⟦β_L⟧ ∩ ⟦β_R⟧ = ∅`

---

## M6 — SplitPreservation (LEMMA, lemma)

Each piece independently preserves:

(a) *Width coupling.* `|V(β_L)| = |I(β_L)| = c` and `|V(β_R)| = |I(β_R)| = n − c`

(b) *Order preservation.* Both `β_L` and `β_R` satisfy M1.

(c) *I-address fidelity.* For every pair `(v + k, a + k)` in `⟦β⟧`, the same pair appears in exactly one of `⟦β_L⟧` or `⟦β_R⟧`. No I-address is altered, dropped, or duplicated.

(d) *Origin traceability.* `origin(a + k) = origin(a)` for each piece, since ordinal increment preserves the document prefix.

(e) *Structural independence.* Each piece is a self-contained mapping block whose well-formedness depends only on its own `(v, a, n)` triple.

---

## M6f — SplitFrame (LEMMA, lemma)

If `B` is a decomposition of `M(d)` containing `β`, then `(B \ {β}) ∪ {β_L, β_R}` is also a decomposition of `M(d)`, and the two decompositions are equivalent. All blocks in `B \ {β}` are unchanged.

---

## M7 — MergeCondition (INV, predicate)

Two blocks `β₁ = (v₁, a₁, n₁)` and `β₂ = (v₂, a₂, n₂)` with `v₁ < v₂` may be merged into a single block if and only if:

`v₂ = v₁ + n₁  ∧  a₂ = a₁ + n₁`

When both conditions hold: `β₁ ⊞ β₂ = (v₁, a₁, n₁ + n₂)`

---

## M7f — MergeFrame (LEMMA, lemma)

If `B` is a decomposition of `M(d)` containing both `β₁` and `β₂`, then `(B \ {β₁, β₂}) ∪ {β₁ ⊞ β₂}` is an equivalent decomposition. All blocks in `B \ {β₁, β₂}` are unchanged.

---

## M8 — MergeInformationLoss (INV, predicate)

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

For any blocks `β₁ = (v₁, a₁, n₁)` and `β₂ = (v₂, a₂, n₂)` satisfying `v₂ = v₁ + n₁` and `a₂ = a₁ + n₁`:

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

The maximally merged decomposition is unique.

Specifically: every maximally merged decomposition equals the set of maximal runs of `f = M(d)`, and the maximal runs are uniquely determined by `f`. A decomposition `B` is maximally merged iff it equals the set of maximal runs of `f`.

---

## M13 — SharedContent (LEMMA, lemma)

`(E Σ : Σ satisfies S0–S3 : (E d, a :: |{v : M(d)(v) = a}| > 1))`

---

## M14 — IndependentOccurrences (LEMMA, lemma)

When two mapping blocks `β₁ = (v₁, a, n)` and `β₂ = (v₂, a, n)` in a decomposition share their I-start and width (with `v₁ ≠ v₂`), they cannot satisfy the merge condition and are permanently distinct.

The I-adjacency condition requires `a = a + n`; since `n ≥ 1`, `a + n > a` by TA-strict (ASN-0034), so `a + n ≠ a`. The condition is unsatisfiable.

---

## M15 — MappingIndependence (INV, predicate)

For any two documents `d₁ ≠ d₂`:

(a) Membership of a triple `(v, a, n)` in a decomposition of `M(d₁)` entails no relationship to any decomposition of `M(d₂)`.

(b) Splitting or merging blocks in a decomposition of `M(d₁)` does not alter any block in any decomposition of `M(d₂)`.

---

## M16 — CrossOriginMergeImpossibility (LEMMA, lemma)

`(A β₁, β₂ : origin(a₁) ≠ origin(a₂) : ¬(a₂ = a₁ + n₁))`

*Proof basis:* Ordinal increment via TA5(c) preserves the document prefix, so `origin(a₁ + n₁) = origin(a₁)`. If `origin(a₂) ≠ origin(a₁)`, then `origin(a₂) ≠ origin(a₁ + n₁)`, hence `a₂ ≠ a₁ + n₁`.

---

## B1 — Coverage (INV, predicate)

`(A v ∈ dom(M(d)) : v₁ ≥ 1 : (E! j : 1 ≤ j ≤ m : v ∈ V(βⱼ)))`

---

## B2 — Disjointness (INV, predicate)

`(A i, j : 1 ≤ i < j ≤ m : V(βᵢ) ∩ V(βⱼ) = ∅)`

---

## B3 — Consistency (INV, predicate)

`(A j : 1 ≤ j ≤ m : (A k : 0 ≤ k < nⱼ : M(d)(vⱼ + k) = aⱼ + k))`

---

## ContentReference — ContentReferenceWellFormed (PRE, requires)

A content reference `(d_s, σ)` with `σ = (u, ℓ)` is well-formed when:
- `d_s ∈ D`
- `V_{u₁}(d_s) ≠ ∅`
- T12 (ASN-0034) holds for `σ`
- `#ℓ = #u = m`, where `m` is the common V-position depth in subspace `u₁` of `d_s`
- `m ≥ 2`
- `{v ∈ T : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d_s))`

---

## C0 — OrdinalDisplacementNecessity (LEMMA, lemma)

For a well-formed content reference `(d_s, σ)` with `σ = (u, ℓ)`, common depth `m`, and action point `k` of `ℓ`:

`k = m`

Equivalently, `ℓ = δ(ℓₘ, m)` — an ordinal displacement.

*Contrapositive basis:* If `k < m`, then `⟦σ⟧` contains infinitely many depth-`m` tumblers (one for each `j > uₘ`), contradicting S8-fin.

---

## C0a — PrefixConfinement (LEMMA, lemma)

For a well-formed content reference `(d_s, σ)` with `σ = (u, ℓ)` and `m ≥ 2`: every `t ∈ ⟦σ⟧` satisfies:

`tⱼ = uⱼ` for all `1 ≤ j < m`

In particular, `t₁ = u₁` (subspace confinement).

---

## C1a — RestrictionDecomposition (LEMMA, lemma)

M11 and M12 hold for any finite partial function `f : T ⇀ T` satisfying S2, S8-fin, and S8-depth. In particular, the restriction `f = M(d_s)|⟦σ⟧` admits a unique maximally merged block decomposition.

Preconditions verified for `f = M(d_s)|⟦σ⟧`:
- S2 (functionality): restriction of a function is a function
- S8-fin: `dom(f) ⊆ dom(M(d_s))`, finite by S8-fin; subset of finite set is finite
- S8-depth: by C0a, every position in `dom(f)` has first component `u₁`, so `dom(f) ⊆ V_{u₁}(d_s)`; by S8-depth, all positions in `V_{u₁}(d_s)` share depth `m`

---

## C1 — ResolutionIntegrity (LEMMA, lemma)

`(A j : 1 ≤ j ≤ k : (A i : 0 ≤ i < nⱼ : aⱼ + i ∈ dom(C)))`

*Derivation:* For any run `(aⱼ, nⱼ)` and index `i`, block `βⱼ` satisfies B3: `M(d_s)(vⱼ + i) = aⱼ + i`. Since `vⱼ + i ∈ dom(M(d_s))`, S3 (ReferentialIntegrity) gives `aⱼ + i ∈ dom(C)`.

---

## C2 — ResolutionWidthPreservation (LEMMA, lemma)

For a well-formed content reference `(d_s, σ)` with `σ = (u, δ(ℓₘ, m))`:

`w(resolve(d_s, σ)) = (+ j : 1 ≤ j ≤ k : nⱼ) = ℓₘ`

*Derivation basis:* By C0, `ℓ = δ(ℓₘ, m)`, so `reach(σ) = [u₁, ..., u_{m−1}, uₘ + ℓₘ]`. By C0a, the depth-`m` tumblers in `⟦σ⟧` are exactly `{[u₁, ..., u_{m−1}, j] : uₘ ≤ j < uₘ + ℓₘ}` — giving `|dom(f)| = ℓₘ`. By B1, B2, and M0, `(+ j : 1 ≤ j ≤ k : nⱼ) = |dom(f)| = ℓₘ`.
