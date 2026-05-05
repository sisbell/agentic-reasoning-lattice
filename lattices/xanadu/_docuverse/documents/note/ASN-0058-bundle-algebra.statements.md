# ASN-0058 Claim Statements

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

## Definition — BlockDecomposition

A *block decomposition* of the text-subspace arrangement of document `d` is a finite set `B = {β₁, ..., βₘ}` of mapping blocks satisfying:

(B1) *Coverage.* Every text-subspace V-position in `dom(M(d))` appears in exactly one block:

`(A v ∈ dom(M(d)) : v₁ ≥ 1 : (E! j : 1 ≤ j ≤ m : v ∈ V(βⱼ)))`

(B2) *Disjointness.* No two blocks share a V-position:

`(A i, j : 1 ≤ i < j ≤ m : V(βᵢ) ∩ V(βⱼ) = ∅)`

(B3) *Consistency.* Each block correctly describes `M(d)`:

`(A j : 1 ≤ j ≤ m : (A k : 0 ≤ k < nⱼ : M(d)(vⱼ + k) = aⱼ + k))`

---

## Definition — InteriorPoint

An integer `c` is *interior* to block `β = (v, a, n)` when `0 < c < n`.

---

## Definition — VAdjacent

Blocks `β₁ = (v₁, a₁, n₁)` and `β₂ = (v₂, a₂, n₂)` with `v₁ < v₂` are *V-adjacent* when `v₂ = v₁ + n₁` — the V-extent of `β₂` immediately follows that of `β₁`.

---

## Definition — IAdjacent

Blocks `β₁` and `β₂` (with `v₁ < v₂`) are *I-adjacent* when `a₂ = a₁ + n₁` — the I-extent of `β₂` immediately follows that of `β₁`.

---

## Definition — DecompositionEquivalence

Block decompositions `B` and `B'` of `M(d)` are *equivalent*, written `B ≡ B'`, when they denote the same mapping:

`⋃{⟦β⟧ : β ∈ B} = ⋃{⟦β⟧ : β ∈ B'}`

---

## Definition — MaximallyMerged

A block decomposition `B` is *maximally merged* when no two blocks in `B` satisfy the merge condition (M7). For every pair `βᵢ, βⱼ ∈ B` with `i ≠ j`: they are not V-adjacent, or they are not I-adjacent, or both.

---

## Definition — MaximalRun

A *maximal run* of `f` is a triple `(v, a, n)` such that:
1. `(A k : 0 ≤ k < n : f(v + k) = a + k)` — it is a correspondence run
2. `¬(E v' :: v' + 1 = v ∧ v' ∈ dom(f) ∧ f(v') + 1 = a)` — it cannot be extended left
3. `v + n ∉ dom(f)  ∨  f(v + n) ≠ a + n` — it cannot be extended right

---

## Definition — ContentReference

A *content reference* is a pair `(d_s, σ)` where `d_s ∈ D` and `σ = (u, ℓ)` is a level-uniform V-span satisfying:
- (i) `V_{u₁}(d_s) ≠ ∅` — the subspace contains at least one V-position
- (ii) T12 (ASN-0034) holds
- (iii) `#ℓ = #u = m`, where `m` is the common V-position depth in subspace `u₁` of `d_s` (S8-depth, ASN-0036)
- (iv) `m ≥ 2`

The content reference is well-formed when every depth-m position in the span's range belongs to `d_s`'s arrangement:

`{v ∈ T : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d_s))`

---

## Definition — ContentReferenceSequence

A *content reference sequence* is an ordered list `R = ⟨r₁, ..., rₚ⟩` of content references with `p ≥ 1`. Different references may name different source documents.

---

## Definition — Resolution

Given content reference `(d_s, σ)` with `σ = (u, ℓ)`, let `f = M(d_s)|⟦σ⟧` be the restriction of `M(d_s)` to positions in `⟦σ⟧`.

The decomposition of `f` (by C1a) yields `⟨β₁, ..., βₖ⟩` ordered by V-start. The *I-address sequence* is:

`resolve(d_s, σ) = ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩`

where `βⱼ = (vⱼ, aⱼ, nⱼ)`.

For a content reference sequence `R = ⟨r₁, ..., rₚ⟩`, the *composite resolution* concatenates:

`resolve(R) = resolve(r₁) ⌢ ... ⌢ resolve(rₚ)`

The *total width* of an I-address sequence `⟨(a₁, n₁), ..., (aₖ, nₖ)⟩` is:

`w(⟨(a₁, n₁), ..., (aₖ, nₖ)⟩) = (+ j : 1 ≤ j ≤ k : nⱼ)`

---

## Definition — SplitOperation

For a mapping block `β = (v, a, n)` and interior point `0 < c < n`, the *split at `c`* produces two blocks:

```
β_L = (v, a, c)
β_R = (v + c, a + c, n − c)
```

---

## Definition — MergeOperation

For blocks `β₁ = (v₁, a₁, n₁)` and `β₂ = (v₂, a₂, n₂)` satisfying the merge condition, the merged block is:

`β₁ ⊞ β₂ = (v₁, a₁, n₁ + n₂)`

---

## B1 — Coverage (PREDICATE, predicate)

`(A v ∈ dom(M(d)) : v₁ ≥ 1 : (E! j : 1 ≤ j ≤ m : v ∈ V(βⱼ)))`

Every text-subspace V-position in `dom(M(d))` appears in exactly one block.

---

## B2 — Disjointness (PREDICATE, predicate)

`(A i, j : 1 ≤ i < j ≤ m : V(βᵢ) ∩ V(βⱼ) = ∅)`

No two blocks share a V-position.

---

## B3 — Consistency (PREDICATE, predicate)

`(A j : 1 ≤ j ≤ m : (A k : 0 ≤ k < nⱼ : M(d)(vⱼ + k) = aⱼ + k))`

Each block correctly describes `M(d)`.

---

## M0 — WidthCoupling (LEMMA, lemma)

For every mapping block `β = (v, a, n)`:

`|V(β)| = |I(β)| = n`

Both projections have equal cardinality, both equal to the block's width.

---

## M1 — OrderPreservation (LEMMA, lemma)

Within a mapping block `β = (v, a, n)`, for all `j, k` with `0 ≤ j < k < n`:

`v + j < v + k  ∧  a + j < a + k`

The `j`-th V-position maps to the `j`-th I-address, and both orderings agree.

---

## M-aux — OrdinalIncrementAssociativity (LEMMA, lemma)

For any tumbler `v` and natural numbers `c, j`:

`(v + c) + j = v + (c + j)`

*Convention.* `v + 0 = v` — the identity of ordinal shift. For `c, j ≥ 1`, this is TS3 (ShiftComposition, ASN-0034): `shift(shift(v, c), j) = shift(v, c + j)`.

---

## M2 — DecompositionExistence (LEMMA, lemma)

Every arrangement `M(d)` admits a block decomposition of its text subspace.

---

## M3 — RepresentationInvariance (LEMMA, lemma)

If `B ≡ B'`, then for every `v ∈ dom(M(d))`, the I-address determined by `B` equals the I-address determined by `B'`.

---

## M4 — SplitDefinition (FUNCTION, function)

For a mapping block `β = (v, a, n)` and interior point `0 < c < n`, the *split at `c`* produces two blocks:

```
β_L = (v, a, c)
β_R = (v + c, a + c, n − c)
```

Preconditions: `c ≥ 1` and `n − c ≥ 1` (since `0 < c < n`). Both starts are valid tumblers by TA0 (ASN-0034).

---

## M5 — SplitPartition (LEMMA, lemma)

The split is exact — nothing lost, nothing duplicated:

(a) `⟦β_L⟧ ∪ ⟦β_R⟧ = ⟦β⟧`

(b) `⟦β_L⟧ ∩ ⟦β_R⟧ = ∅`

---

## M6 — SplitPreservation (LEMMA, lemma)

Each piece independently preserves every property that derives from I-address identity:

(a) *Width coupling.* `|V(β_L)| = |I(β_L)| = c` and `|V(β_R)| = |I(β_R)| = n − c`. Each piece is a mapping block, so M0 applies.

(b) *Order preservation.* Both `β_L` and `β_R` satisfy M1. Each is a mapping block; M1 holds for every mapping block.

(c) *I-address fidelity.* For every pair `(v + k, a + k)` in `⟦β⟧`, the same pair appears in exactly one of `⟦β_L⟧` or `⟦β_R⟧`. No I-address is altered, dropped, or duplicated.

(d) *Origin traceability.* Each I-address `a + k` carries its origin permanently in its tumbler structure — `origin(a + k) = origin(a)`, since `a + k = a ⊕ δ(k, #a)` and TumblerAdd with action point `#a` copies `aᵢ` for all `i < #a`, preserving the document prefix `N.0.U.0.D`.

(e) *Structural independence.* Each piece is a self-contained mapping block whose well-formedness depends only on its own `(v, a, n)` triple — not on external state, not on the existence of the other piece.

---

## M6f — SplitFrame (LEMMA, lemma)

If `B` is a decomposition of `M(d)` containing `β`, then `(B \ {β}) ∪ {β_L, β_R}` is also a decomposition of `M(d)`, and the two decompositions are equivalent. All blocks in `B \ {β}` are unchanged.

---

## M7 — MergeCondition (LEMMA, lemma)

Two blocks `β₁ = (v₁, a₁, n₁)` and `β₂ = (v₂, a₂, n₂)` with `v₁ < v₂` may be merged into a single block if and only if they are both V-adjacent and I-adjacent:

`v₂ = v₁ + n₁  ∧  a₂ = a₁ + n₁`

When both conditions hold, the merged block is:

`β₁ ⊞ β₂ = (v₁, a₁, n₁ + n₂)`

---

## M7f — MergeFrame (LEMMA, lemma)

If `B` is a decomposition of `M(d)` containing both `β₁` and `β₂`, then `(B \ {β₁, β₂}) ∪ {β₁ ⊞ β₂}` is an equivalent decomposition. All blocks in `B \ {β₁, β₂}` are unchanged.

---

## M8 — MergeInformationLoss (LEMMA, lemma)

The merge is information-destroying with respect to the boundary. Given only `β₁ ⊞ β₂ = (v₁, a₁, n₁ + n₂)`, the individual widths `n₁` and `n₂` cannot be recovered. The merged block is indistinguishable from one that was never split.

---

## M9 — SplitMergeInverse (LEMMA, lemma)

For any mapping block `β = (v, a, n)` and interior point `0 < c < n`, the two pieces produced by split satisfy the merge condition and merge back to the original:

```
split(β, c) = (β_L, β_R)
  where β_L = (v, a, c) and β_R = (v + c, a + c, n − c)

V-adjacency: v + c = v + c  ✓
I-adjacency: a + c = a + c  ✓

β_L ⊞ β_R = (v, a, c + (n − c)) = (v, a, n) = β
```

---

## M10 — MergeSplitInverse (LEMMA, lemma)

For any blocks `β₁ = (v₁, a₁, n₁)` and `β₂ = (v₂, a₂, n₂)` satisfying the merge condition (`v₂ = v₁ + n₁`, `a₂ = a₁ + n₁`), splitting the merged block at the original boundary recovers both:

```
split(β₁ ⊞ β₂, n₁)
  = ((v₁, a₁, n₁), (v₁ + n₁, a₁ + n₁, n₂))
  = (β₁, β₂)
```

---

## M11 — CanonicalExistence (LEMMA, lemma)

Every arrangement `M(d)` admits a maximally merged block decomposition.

*Construction.* Start with any decomposition `B` (which exists by M2). While there exist `βᵢ, βⱼ ∈ B` satisfying the merge condition: replace them with `βᵢ ⊞ βⱼ` (by M7f, the result is an equivalent decomposition). Each merge reduces `|B|` by exactly 1 and preserves equivalence. The process terminates because `|B|` is finite and bounded below by 1 for non-empty `M(d)`.

---

## M12 — CanonicalUniqueness (LEMMA, lemma)

The maximally merged decomposition is unique.

The maximally merged decomposition equals the set of *maximal runs* of `f = M(d)`, and that set is uniquely determined by `f`.

Formally: a decomposition `B` is maximally merged iff it equals the set of maximal runs of `f`. Since the maximal runs are uniquely determined by `f`, and every maximally merged decomposition equals the set of maximal runs, the maximally merged decomposition is unique.

---

## M13 — SharedContent (LEMMA, lemma)

The arrangement `M(d)` permits multiple V-positions to share the same I-address:

`(E Σ : Σ satisfies S0–S3 : (E d, a :: |{v : M(d)(v) = a}| > 1))`

---

## M14 — IndependentOccurrences (LEMMA, lemma)

When two mapping blocks `β₁ = (v₁, a, n)` and `β₂ = (v₂, a, n)` in a decomposition share their I-start and width (with `v₁ ≠ v₂`), they are independent entries that cannot be merged.

The merge condition (M7) requires `a₂ = a₁ + n₁`. Here `a₂ = a₁ = a`, so the condition requires `a = a + n`. Since `n ≥ 1`, `a + n > a` by TA-strict (ASN-0034), so `a + n ≠ a`. The I-adjacency condition is unsatisfiable; the blocks cannot merge and are permanently distinct.

---

## M15 — MappingIndependence (LEMMA, lemma)

For any two documents `d₁ ≠ d₂`:

(a) Block decompositions are per-document objects; membership of a triple `(v, a, n)` in a decomposition of `M(d₁)` entails no relationship to any decomposition of `M(d₂)`.

(b) Splitting or merging blocks in a decomposition of `M(d₁)` does not alter any block in any decomposition of `M(d₂)`.

---

## M16 — CrossOriginMergeImpossibility (LEMMA, lemma)

If `origin(a₁) ≠ origin(a₂)` — the I-addresses in two blocks were allocated by different documents — then the blocks cannot satisfy I-adjacency:

`(A β₁, β₂ : origin(a₁) ≠ origin(a₂) : ¬(a₂ = a₁ + n₁))`

*Proof.* The ordinal shift `a₁ + n₁ = a₁ ⊕ δ(n₁, #a₁)` has action point `#a₁`. By TumblerAdd (ASN-0034), `rᵢ = (a₁)ᵢ` for all `i < #a₁` — every component before the action point is copied unchanged. For element-level I-addresses, the document prefix `N.0.U.0.D` occupies positions strictly before `#a₁`, so it is preserved. Therefore `origin(a₁ + n₁) = origin(a₁)`. If `origin(a₂) ≠ origin(a₁)`, then `origin(a₂) ≠ origin(a₁ + n₁)`. Since `origin` is a function on tumblers, equal tumblers have equal origins; by contrapositive, different origins imply different tumblers: `a₂ ≠ a₁ + n₁`.

---

## C0 — OrdinalDisplacementNecessity (LEMMA, lemma)

For a well-formed content reference `(d_s, σ)` with `σ = (u, ℓ)`, common depth `m`, and action point `k` of `ℓ`: `k = m`. Equivalently, `ℓ = δ(ℓₘ, m)` — an ordinal displacement.

*Derivation.* Suppose for contradiction that `k < m`. Consider the family of depth-m tumblers `wⱼ = [u₁, ..., uₖ, uₖ₊₁, ..., u_{m−1}, j]` for `j > uₘ`. Each `wⱼ` satisfies `u < wⱼ` (by T1(i), ASN-0034). Each `wⱼ` satisfies `wⱼ < reach(σ)` (at component `k`, `uₖ < uₖ + ℓₖ` since `ℓₖ ≥ 1`). Thus `wⱼ ∈ ⟦σ⟧` for every `j > uₘ`. By T0(a) (ASN-0034), `j` ranges over unboundedly many values, yielding infinitely many depth-m tumblers in `⟦σ⟧`. Well-formedness requires each to be in `dom(M(d_s))`, contradicting S8-fin (ASN-0036). Therefore `k = m`, and `ℓ = [0, ..., 0, ℓₘ] = δ(ℓₘ, m)`.

---

## C0a — PrefixConfinement (LEMMA, lemma)

For a well-formed content reference `(d_s, σ)` with `σ = (u, ℓ)` and `m ≥ 2`: every `t ∈ ⟦σ⟧` satisfies `tⱼ = uⱼ` for all `1 ≤ j < m`.

*Derivation.* By C0, the action point of `ℓ` is `m`. Since `m ≥ 2`, TumblerAdd gives `reach(σ)ⱼ = uⱼ` for all `j < m`. Fix any `t ∈ ⟦σ⟧`, so `u ≤ t < reach(σ)`. Suppose for contradiction that `J = {j : 1 ≤ j < m ∧ tⱼ ≠ uⱼ}` is non-empty, and let `j₀ = min(J)`. Then `tᵢ = uᵢ` for all `1 ≤ i < j₀`. Since `u ≤ t`, T1(i) gives `t_{j₀} > u_{j₀}`. Since `reach(σ)_{j₀} = u_{j₀}` and `tᵢ = uᵢ = reach(σ)ᵢ` for all `i < j₀`, the divergence of `t` and `reach(σ)` is also at `j₀` with `t_{j₀} > reach(σ)_{j₀}`. By T1(i), `t > reach(σ)`, contradicting `t < reach(σ)`. Therefore `J = ∅`.

Moreover, `#t ≥ m`: if `#t < m`, then `J = ∅` forces `tⱼ = uⱼ` for all `1 ≤ j ≤ #t`, making `t` a proper prefix of `u`; T1(ii) gives `t < u`, contradicting `u ≤ t`. Hence `tⱼ` is defined for all `1 ≤ j < m`, and `J = ∅` gives `tⱼ = uⱼ` for all `1 ≤ j < m`. In particular, `t₁ = u₁` (subspace confinement).

---

## C1a — RestrictionDecomposition (LEMMA, lemma)

M11 and M12 hold for any finite partial function `f : T ⇀ T` satisfying S2, S8-fin, and S8-depth. In particular, the restriction `f = M(d_s)|⟦σ⟧` admits a unique maximally merged block decomposition.

*Verification that f satisfies the conditions.*
- S2 (functionality): `f` is a restriction of `M(d_s)`, which is functional by S2; a restriction of a function is a function.
- S8-fin (finite domain): `dom(f) ⊆ dom(M(d_s))`, which is finite by S8-fin; a subset of a finite set is finite.
- S8-depth (fixed depth): by C0a, every position in `dom(f)` has first component `u₁`, so `dom(f) ⊆ V_{u₁}(d_s)`; by S8-depth, all positions in `V_{u₁}(d_s)` share the common depth `m`.

---

## C1 — ResolutionIntegrity (LEMMA, lemma)

Every resolved I-address is in `dom(C)`:

`(A j : 1 ≤ j ≤ k : (A i : 0 ≤ i < nⱼ : aⱼ + i ∈ dom(C)))`

*Derivation.* Fix any run `(aⱼ, nⱼ)` in the resolution and any `i` with `0 ≤ i < nⱼ`. The corresponding block `βⱼ = (vⱼ, aⱼ, nⱼ)` satisfies B3: `M(d_s)(vⱼ + i) = aⱼ + i`. Since `vⱼ + i ∈ dom(M(d_s))`, S3 (ReferentialIntegrity, ASN-0036) gives `M(d_s)(vⱼ + i) ∈ dom(C)`, hence `aⱼ + i ∈ dom(C)`.

---

## C2 — ResolutionWidthPreservation (LEMMA, lemma)

For a well-formed content reference `(d_s, σ)` with `σ = (u, δ(ℓₘ, m))`, the total resolved width equals `ℓₘ`:

`w(resolve(d_s, σ)) = (+ j : 1 ≤ j ≤ k : nⱼ) = ℓₘ`

*Derivation.* By C0, `ℓ = δ(ℓₘ, m)`, so `reach(σ) = u ⊕ δ(ℓₘ, m) = [u₁, ..., u_{m−1}, uₘ + ℓₘ]`. The depth-m tumblers in `[u, reach(σ))` are exactly `{[u₁, ..., u_{m−1}, j] : uₘ ≤ j < uₘ + ℓₘ}`: by C0a, every `t ∈ ⟦σ⟧` satisfies `tⱼ = uⱼ` for all `1 ≤ j < m`, fixing the first `m − 1` components; the `m`-th component ranges over `uₘ ≤ tₘ < uₘ + ℓₘ`. There are `ℓₘ` such tumblers; well-formedness places each in `dom(f)`. Therefore `|dom(f)| = ℓₘ`. By B1 and B2, the V-extents of the blocks partition `dom(f)`. By M0, `|V(βⱼ)| = nⱼ` for each block. Therefore `(+ j : 1 ≤ j ≤ k : nⱼ) = |dom(f)| = ℓₘ`.
