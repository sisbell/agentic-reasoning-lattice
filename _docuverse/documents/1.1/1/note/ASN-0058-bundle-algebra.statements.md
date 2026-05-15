# ASN-0058 Claim Statements

*Source: ASN-0058-bundle-algebra.md (revised 2026-03-22) — Extracted: 2026-05-15*

## Definition — MappingBlock

A mapping block `β = (v, a, n)` consists of:
- `v ∈ T` — the V-start (a position in the document's virtual stream)
- `a ∈ T` — the I-start (an address in the permanent content store)
- `n ∈ ℕ` with `n ≥ 1` — the width (count of positions mapped)

It denotes the set of position-address pairs:

`⟦β⟧ = {(v + k, a + k) : 0 ≤ k < n}`

The *V-extent* is `V(β) = {v + k : 0 ≤ k < n}`; the *I-extent* is `I(β) = {a + k : 0 ≤ k < n}`.

---

## OrdinalShiftBase — OrdinalShiftBase (CONVENTION, axiom)

For any tumbler `t` and natural number `k ≥ 0`:
- For `k ≥ 1`, `t + k` denotes `shift(t, k)` — the OrdinalShift of ASN-0034 at the tumbler's own depth.
- For `k = 0`, `t + 0 = t` by definition — the identity of ordinal shift.

---

## M0 — WidthCoupling (LEMMA, lemma)

For every mapping block `β = (v, a, n)`:

`|V(β)| = |I(β)| = n`

---

## M1 — OrderPreservation (LEMMA, lemma)

Within a mapping block `β = (v, a, n)`, the mapping preserves ordinal position. For all `j, k` with `0 ≤ j < k < n`:

`v + j < v + k  ∧  a + j < a + k`

---

## M-aux — OrdinalIncrementAssociativity (LEMMA, lemma)

For any tumbler `v` and natural numbers `c, j ≥ 0`:

`(v + c) + j = v + (c + j)`

---

## M-sub — SubspaceConfinement (LEMMA, lemma)

For a mapping block `β = (v, a, n)`:

(a) When `#v ≥ 2`, every V-position of `β` shares the V-subspace of `v`:

`(A k : 0 ≤ k < n : subspace(v + k) = subspace(v))`

(b) When `a ∈ dom(C)`, every I-address of `β` shares the I-subspace of `a`:

`(A k : 0 ≤ k < n : subspace_I(a + k) = subspace_I(a))`

---

## M-int — TumblerIntervalCharacterization (LEMMA, lemma)

Let `x, y ∈ dom(M(d))` and `n ≥ 1`. If `x ≤ y < x + n`, then writing `m = #x`:

- *Subspace agreement* — `subspace(y) = subspace(x)` (equivalently `(y)_1 = (x)_1`);
- *Depth equality* — `#y = m`;
- *Prefix agreement* — `(y)_j = (x)_j` for all `1 ≤ j < m`;
- *Component-`m` reduction* — `y = x + k` where `k = (y)_m − (x)_m` and `0 ≤ k < n`.

---

## Definition — BlockDecomposition

A *block decomposition* of the arrangement of document `d` is a finite set `B = {β₁, ..., βₘ}` of mapping blocks satisfying B1, B2, and B3 (below). The empty arrangement `M(d) = ∅` has `B = ∅` as its unique decomposition.

---

## B1 — Coverage (INV, predicate)

Every V-position in `dom(M(d))` appears in exactly one block:

`(A v ∈ dom(M(d)) :: (E! j : 1 ≤ j ≤ m : v ∈ V(βⱼ)))`

---

## B2 — Disjointness (INV, predicate)

No two blocks share a V-position:

`(A i, j : 1 ≤ i < j ≤ m : V(βᵢ) ∩ V(βⱼ) = ∅)`

---

## B3 — Consistency (INV, predicate)

Each block correctly describes `M(d)`:

`(A j : 1 ≤ j ≤ m : (A k : 0 ≤ k < nⱼ : M(d)(vⱼ + k) = aⱼ + k))`

---

## M2 — DecompositionExistence (LEMMA, lemma)

Under the standing preconditions S8-fin, S2, S3, S8a, S8-depth, S7b, and S7c (ASN-0036), every arrangement `M(d)` admits a block decomposition.

---

## Definition — DecompositionEquivalence

Block decompositions `B` and `B'` of `M(d)` are *equivalent*, written `B ≡ B'`, when they denote the same mapping:

`⋃{⟦β⟧ : β ∈ B} = ⋃{⟦β⟧ : β ∈ B'}`

---

## M3 — RepresentationInvariance (LEMMA, lemma)

If `B ≡ B'`, then for every `v ∈ dom(M(d))`, the I-address determined by `B` equals the I-address determined by `B'`.

---

## Definition — InteriorPoint

An integer `c` is *interior* to block `β = (v, a, n)` when `0 < c < n`.

---

## M4 — SplitDefinition (DEF, function)

For a mapping block `β = (v, a, n)` and interior point `0 < c < n`, the *split at `c`* produces two blocks:

```
β_L = (v, a, c)
β_R = (v + c, a + c, n − c)
```

Both are well-formed mapping blocks: `c ≥ 1` and `n − c ≥ 1` (since `0 < c < n`).

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

(d) *Structural independence.* Each piece is a self-contained mapping block whose well-formedness depends only on its own `(v, a, n)` triple — not on external state, not on the existence of the other piece.

---

## M6f — SplitFrame (LEMMA, lemma)

If `B` is a decomposition of `M(d)` containing `β`, then `(B \ {β}) ∪ {β_L, β_R}` is also a decomposition of `M(d)`, and the two decompositions are equivalent. All blocks in `B \ {β}` are unchanged.

---

## Definition — VAdjacent

Blocks `β₁ = (v₁, a₁, n₁)` and `β₂ = (v₂, a₂, n₂)` with `v₁ < v₂` are *V-adjacent* when `v₂ = v₁ + n₁` — the V-extent of `β₂` immediately follows that of `β₁`.

---

## Definition — IAdjacent

Blocks `β₁` and `β₂` (with `v₁ < v₂`) are *I-adjacent* when `a₂ = a₁ + n₁` — the I-extent of `β₂` immediately follows that of `β₁`.

---

## M7 — MergeCondition (LEMMA, lemma)

Let `B` be a decomposition of `M(d)`, and let `β₁ = (v₁, a₁, n₁)` and `β₂ = (v₂, a₂, n₂)` be blocks in `B` with `v₁ < v₂`. They may be merged into a single block compatible with `M(d)` if and only if they are both V-adjacent and I-adjacent:

`v₂ = v₁ + n₁  ∧  a₂ = a₁ + n₁`

When both conditions hold, the merged block is:

`β₁ ⊞ β₂ = (v₁, a₁, n₁ + n₂)`

---

## M7-cov — NonOverlap (LEMMA, lemma)

Let `B` be a decomposition of `M(d)` and let `β₁ = (v₁, a₁, n₁)` and `β₂ = (v₂, a₂, n₂)` be distinct blocks in `B` with `v₁ < v₂`. Then `v₂ ≥ v₁ + n₁`.

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

## Definition — MaximallyMerged

A block decomposition `B` is *maximally merged* when no two blocks in `B` satisfy the merge condition (M7). For every pair `βᵢ, βⱼ ∈ B` with `i ≠ j`: they are not V-adjacent, or they are not I-adjacent, or both.

---

## M11 — CanonicalExistence (LEMMA, lemma)

Every arrangement `M(d)` admits a maximally merged block decomposition.

---

## Definition — MaximalRun

A *maximal run* of `f = M(d)` is a triple `(v, a, n)` such that:

1. `(A k : 0 ≤ k < n : f(v + k) = a + k)` — it is a correspondence run
2. `¬(E v' :: v' + 1 = v ∧ v' ∈ dom(f) ∧ f(v') + 1 = a)` — it cannot be extended left
3. `v + n ∉ dom(f)  ∨  f(v + n) ≠ a + n` — it cannot be extended right

---

## M12 — CanonicalUniqueness (LEMMA, lemma)

The maximally merged decomposition is unique.

---

## M12a — RunDisjointness (LEMMA, lemma)

Maximal runs of `f` pairwise have disjoint V-extents: if `R₁ = (v₁, a₁, n₁)` and `R₂ = (v₂, a₂, n₂)` are maximal runs of `f` with `V(R₁) ∩ V(R₂) ≠ ∅`, then `(v₁, a₁, n₁) = (v₂, a₂, n₂)`.

---

## M12b — NoExtensionInMaximallyMerged (LEMMA, lemma)

Let `B` be a maximally merged decomposition of `M(d)`. Every block `β = (v, a, n) ∈ B` satisfies conditions 2 and 3 of being a maximal run of `f = M(d)`: it cannot be left-extended or right-extended in `f`.

---

## M13 — SharedContent (LEMMA, lemma)

`(E Σ : Σ satisfies S0–S3 : (E d, a :: |{v : M(d)(v) = a}| > 1))`

---

## M14 — IndependentOccurrences (LEMMA, lemma)

When two mapping blocks `β₁ = (v₁, a, n)` and `β₂ = (v₂, a, n)` in a decomposition share their I-start and width (with `v₁ ≠ v₂`), they are independent entries that cannot be merged.

The merge condition (M7) requires `a₂ = a₁ + n₁`. Here `a₂ = a₁ = a`, so the condition requires `a = a + n`. Since `n ≥ 1`, `a + n > a` by TA-strict (ASN-0034), so `a + n ≠ a`. The I-adjacency condition is unsatisfiable.

---

## M15 — MappingIndependence (LEMMA, lemma)

For any two documents `d₁ ≠ d₂`:

(a) Block decompositions are per-document objects; membership of a triple `(v, a, n)` in a decomposition of `M(d₁)` entails no relationship to any decomposition of `M(d₂)`.

(b) *Frame condition.* The split frame M6f and the merge frame M7f, applied to a decomposition `B` of `M(d₁)`, name and modify only `B` itself; no block of any decomposition of `M(d₂)` is named, read, or modified by either operation. In particular, every block in every decomposition of `M(d₂)` is unchanged by any split or merge on `B`.

---

## M16a — OriginInvarianceUnderShift (LEMMA, lemma)

For any `a ∈ dom(C)` and any `k ≥ 0` with `a + k ∈ dom(C)`:

`origin(a + k) = origin(a)`

---

## M16b — SplitOriginTraceability (LEMMA, lemma)

When mapping block `β = (v, a, n)` belongs to a decomposition `B` of `M(d)`, every I-address in `I(β)` shares `β`'s origin:

`(A k : 0 ≤ k < n : origin(a + k) = origin(a))`

Consequently, after splitting `β` at any interior point `c` (M4) into `β_L = (v, a, c)` and `β_R = (v + c, a + c, n − c)`, each piece independently identifies the home document of its content — `β_L`'s I-addresses and `β_R`'s I-addresses all share `origin(a)`.

---

## M16 — CrossOriginMergeImpossibility (LEMMA, lemma)

Let `β₁ = (v₁, a₁, n₁)` and `β₂ = (v₂, a₂, n₂)` be blocks with `a₁, a₂ ∈ dom(C)`. If `origin(a₁) ≠ origin(a₂)` — the I-addresses were allocated by different documents — then the blocks cannot satisfy I-adjacency:

`(A β₁, β₂ : a₁, a₂ ∈ dom(C) ∧ origin(a₁) ≠ origin(a₂) : ¬(a₂ = a₁ + n₁))`

---

## ContentReference — ContentReference (DEF, datatype)

A *content reference* is a pair `(d_s, σ)` where `d_s ∈ D` and `σ = (u, ℓ)` is a level-uniform V-span satisfying:

(i) `V_{u₁}(d_s) ≠ ∅` — the subspace contains at least one V-position;

(ii) T12 (ASN-0034) holds (equivalently: `Pos(ℓ)` and `actionPoint(ℓ) ≤ #u`);

(iii) `#ℓ = #u = m`, where `m` is the common V-position depth in subspace `u₁` of `d_s` (S8-depth, ASN-0036).

The content reference is well-formed when every depth-`m` position in the span's range belongs to `d_s`'s arrangement:

`{v ∈ T : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d_s))`

For a subspace identifier S and a document `d ∈ D`, `V_S(d) := {v ∈ dom(M(d)) : subspace(v) = S}`.

---

## C0 — OrdinalDisplacementNecessity (LEMMA, lemma)

For a well-formed content reference `(d_s, σ)` with `σ = (u, ℓ)`, common depth `m`, and action point `k` of `ℓ`: `k = m`. Equivalently, `ℓ = δ(ℓₘ, m)` — an ordinal displacement.

---

## C0a — PrefixConfinement (LEMMA, lemma)

For a well-formed content reference `(d_s, σ)` with `σ = (u, ℓ)` and `m ≥ 2`: every `t ∈ ⟦σ⟧` satisfies `tⱼ = uⱼ` for all `1 ≤ j < m`.

---

## ContentReferenceSequence — ContentReferenceSequence (DEF, datatype)

A *content reference sequence* is an ordered list `R = ⟨r₁, ..., rₚ⟩` of content references with `p ≥ 1`. Different references may name different source documents.

For a content reference sequence `R = ⟨r₁, ..., rₚ⟩`, the *composite resolution* concatenates:

`resolve(R) = resolve(r₁) ⌢ ... ⌢ resolve(rₚ)`

The *total width* of an I-address sequence `⟨(a₁, n₁), ..., (aₖ, nₖ)⟩` is:

`w(⟨(a₁, n₁), ..., (aₖ, nₖ)⟩) = (+ j : 1 ≤ j ≤ k : nⱼ)`

---

## resolve(d_s, σ) — Resolution (DEF, function)

Given content reference `(d_s, σ)` with `σ = (u, ℓ)`, let `f = M(d_s)|⟦σ⟧` be the restriction of `M(d_s)` to positions in `⟦σ⟧`.

The decomposition of `f` (by C1a) yields `⟨β₁, ..., βₖ⟩` ordered by V-start. The *I-address sequence* is:

`resolve(d_s, σ) = ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩`

where `βⱼ = (vⱼ, aⱼ, nⱼ)`. The V-coordinates are discarded; only I-starts and widths are carried forward.

---

## C1a — RestrictionDecomposition (LEMMA, lemma)

M11 and M12 hold for any finite partial function `f : T ⇀ T` satisfying (i) functionality, (ii) finite domain, and (iii) common depth `m ≥ 2` across its domain. In particular, the restriction `f = M(d_s)|⟦σ⟧` satisfies these three conditions and admits a unique maximally merged block decomposition.

Verification that `f = M(d_s)|⟦σ⟧` satisfies the three conditions:

(i) *Functionality:* `f` is a restriction of `M(d_s)`, which is functional by S2 (ASN-0036).

(ii) *Finite domain:* `dom(f) ⊆ dom(M(d_s))`, which is finite by S8-fin (ASN-0036).

(iii) *Common depth `m ≥ 2` on `dom(f)`:* by C0a, every position in `dom(f)` has first component `u₁`, so `dom(f) ⊆ V_{u₁}(d_s)`; by S8-depth (ASN-0036) applied to `d_s` in subspace `u₁`, all positions share common depth `m`. The bound `m ≥ 2` is derived from content reference well-formedness via S8a (ASN-0036).

---

## C1b — ResolutionSequenceOrder (LEMMA, lemma)

The runs in `resolve(d_s, σ) = ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩` are listed in strictly increasing order of the V-start of their underlying blocks:

`(A i, j : 1 ≤ i < j ≤ k : vᵢ < vⱼ)`

---

## C1 — ResolutionIntegrity (LEMMA, lemma)

Every resolved I-address is in `dom(C)`:

`(A j : 1 ≤ j ≤ k : (A i : 0 ≤ i < nⱼ : aⱼ + i ∈ dom(C)))`

---

## C2 — ResolutionWidthPreservation (LEMMA, lemma)

For a well-formed content reference `(d_s, σ)` with `σ = (u, δ(ℓₘ, m))`, the total resolved width equals `ℓₘ`:

`w(resolve(d_s, σ)) = (+ j : 1 ≤ j ≤ k : nⱼ) = ℓₘ`
