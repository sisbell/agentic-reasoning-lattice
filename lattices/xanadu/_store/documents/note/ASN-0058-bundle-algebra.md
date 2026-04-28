# ASN-0058: Bundle Algebra

*2026-03-20, revised 2026-03-22*

## The Problem

ASN-0036 establishes that a document's arrangement `M(d)` is a partial function from V-positions to I-addresses (S2), and that this function decomposes into correspondence runs (S8). But S8 asserts only that a decomposition *exists*. We now ask: what is the algebra of these runs? How do they compose and decompose? What invariants must any valid representation of the arrangement preserve?

Nelson names the central data structure the *Permutation Of Order Matrix* — the POOM. The Istream records what exists; the Vstream records how it is arranged. The POOM mediates between the two orderings. We seek the abstract properties of this mediation — properties that any implementation must satisfy, regardless of its internal data structures.

## The Mapping Block

The arrangement pairs V-positions with I-addresses. These pairings are not arbitrary — they cluster into contiguous runs where consecutive V-positions map to consecutive I-addresses. Nelson identifies this clustering as the fundamental unit of representation:

> "An I-span (identity span) describes a contiguous set of elements in the document's v-stream which have contiguous identity (I-stream) addresses. A document may be described completely by a sequence of I-spans covering its entire v-stream." [LM 4/36]

We adopt the term *mapping block* to distinguish the abstract object from any particular representation.

**Definition (Mapping Block).** A mapping block `β = (v, a, n)` consists of:

- `v ∈ T` — the V-start (a position in the document's virtual stream)
- `a ∈ T` — the I-start (an address in the permanent content store)
- `n ∈ ℕ` with `n ≥ 1` — the width (count of positions mapped)

It denotes the set of position-address pairs:

`⟦β⟧ = {(v + k, a + k) : 0 ≤ k < n}`

where `v + k` is shorthand for `shift(v, k)` (OrdinalShift, ASN-0034) extended to `k = 0` as the identity, and likewise `a + k` for `shift(a, k)` — both denoting ordinal displacement at the tumbler's own depth. The *V-extent* is `V(β) = {v + k : 0 ≤ k < n}`; the *I-extent* is `I(β) = {a + k : 0 ≤ k < n}`.

This is the correspondence run of ASN-0036 S8, elevated to a first-class algebraic object. We now establish its properties.

### Width Coupling

The first property is the structural keystone on which the entire algebra rests. Nelson states it directly:

> "Their width is defined by a single difference tumbler (the same in both spaces), since the V-stream and the I-stream widths must be identical." [LM 4/36]

**M0 (WidthCoupling).** For every mapping block `β = (v, a, n)`:

`|V(β)| = |I(β)| = n`

Both projections have equal cardinality, both equal to the block's width. By TumblerAdd (ASN-0034), `v + j = [v₁, ..., v_m + j]` and `v + k = [v₁, ..., v_m + k]`; when `j ≠ k`, these differ at component `m`, so `v + j ≠ v + k` by T3 (CanonicalRepresentation, ASN-0034). Strict ordering follows from T1 at the last component: `v + j < v + k` for all `0 ≤ j < k < n`. The `n` values in `V(β)` are therefore distinct and `|V(β)| = n`. Likewise for `I(β)`.

This is not a convenience of representation. The Vstream is an *arrangement* of Istream content — each V-position references exactly one I-byte, and each reference is to exactly one byte. There is no compression, expansion, or transformation between the spaces. The mapping is positional and unit-ratio.

Gregory's implementation confirms the structural enforcement. Each POOM bottom crum stores separate V-width and I-width tumblers — the same integer count encoded at different hierarchical depths. The construction path in `insertpm` derives both from a shared integer `inc`: it extracts the byte count from the I-width via `tumblerintdiff`, then re-encodes that same count as V-width at the V-address depth via `tumblerincrement`. No subsequent operation writes to an existing crum's width fields — the coupling is established at creation and maintained by immutability.

### Order Preservation

**M1 (OrderPreservation).** Within a mapping block `β = (v, a, n)`, the mapping preserves ordinal position. For all `j, k` with `0 ≤ j < k < n`:

`v + j < v + k  ∧  a + j < a + k`

The `j`-th V-position maps to the `j`-th I-address, and both orderings agree.

Nelson's justification is structural:

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." [LM 4/25]

A span on the tumbler line is defined by its endpoints. The internal ordering follows from the total order T1 (ASN-0034). There is no reversal flag, no permutation within a span, no mechanism for a single mapping unit to represent anything other than ordinal correspondence. To represent content in reverse order requires multiple blocks, each individually monotone, arranged in the desired V-sequence.

M0 and M1 together characterize the mapping block: it is a *width-preserving monotone injection* from a contiguous V-range to a contiguous I-range. The word "injection" is precise — within a single block, distinct V-positions map to distinct I-addresses. Across blocks, the same I-address may appear at multiple V-positions; we return to this below.

**Remark (Span Algebra Connection).** A mapping block `β = (v, a, n)` induces two spans in the sense of ASN-0053: a V-span over `V(β)` and an I-span over `I(β)`. The block's split (M4 below) corresponds to simultaneous application of S4 (SplitPartition, ASN-0053) to both spans at corresponding positions. The merge (M7 below) corresponds to S3 (MergeEquivalence, ASN-0053) applied to both span pairs, subject to both being adjacent. Width coupling (M0) ensures that the two span operations remain synchronized — the cut point in V-space determines the cut point in I-space.

**M-aux (OrdinalIncrementAssociativity).** For any tumbler `v` and natural numbers `c, j`:

`(v + c) + j = v + (c + j)`

*Convention.* We define `v + 0 = v` — the identity of ordinal shift. At `k = 0` this is the base case of the correspondence run: `M(d)(v) = a`, no displacement, no arithmetic (cf. S8, ASN-0036).

For `c, j ≥ 1`, this is TS3 (ShiftComposition, ASN-0034): `shift(shift(v, c), j) = shift(v, c + j)`. The cases `c = 0` or `j = 0` follow from the convention. ∎

## The Arrangement as a Set of Blocks

A document's full arrangement is a collection of mapping blocks that together describe `M(d)`.

**Definition (Block Decomposition).** A *block decomposition* of the text-subspace arrangement of document `d` is a finite set `B = {β₁, ..., βₘ}` of mapping blocks satisfying:

(B1) *Coverage.* Every text-subspace V-position in `dom(M(d))` appears in exactly one block:

`(A v ∈ dom(M(d)) : v₁ ≥ 1 : (E! j : 1 ≤ j ≤ m : v ∈ V(βⱼ)))`

(B2) *Disjointness.* No two blocks share a V-position:

`(A i, j : 1 ≤ i < j ≤ m : V(βᵢ) ∩ V(βⱼ) = ∅)`

(B3) *Consistency.* Each block correctly describes `M(d)`:

`(A j : 1 ≤ j ≤ m : (A k : 0 ≤ k < nⱼ : M(d)(vⱼ + k) = aⱼ + k))`

B1 and B2 together assert that the V-extents partition the text-subspace portion of `dom(M(d))`. B3 asserts that the mapping within each block agrees with the global arrangement. The empty arrangement `M(d) = ∅` has `B = ∅` as its unique decomposition.

**M2 (DecompositionExistence).** Every arrangement `M(d)` admits a block decomposition of its text subspace.

This is S8 (SpanDecomposition, ASN-0036) restated in our vocabulary — both are explicitly scoped to text-subspace V-positions (`v₁ ≥ 1`). The question that S8 leaves open is: given that at least one decomposition exists, how many are there, and what relates them?

Nelson tells us:

> "There may be many representations of a given v-stream. The representation with the fewest I-spans is the most compact." [LM 4/37]

**Definition (Decomposition Equivalence).** Block decompositions `B` and `B'` of `M(d)` are *equivalent*, written `B ≡ B'`, when they denote the same mapping:

`⋃{⟦β⟧ : β ∈ B} = ⋃{⟦β⟧ : β ∈ B'}`

**M3 (RepresentationInvariance).** If `B ≡ B'`, then for every `v ∈ dom(M(d))`, the I-address determined by `B` equals the I-address determined by `B'`.

This is immediate — equivalent decompositions denote the same set of `(V, I)` pairs, which is a function by S2 (ArrangementFunctionality, ASN-0036). The arrangement `M(d)` is the invariant; the decomposition is a choice of representation.

## Splitting a Mapping Block

We now develop the operations that transform one decomposition into another. The first is splitting: given a mapping block and a cut point in its interior, we produce two smaller blocks that together are equivalent to the original.

**Definition (Interior Point).** An integer `c` is *interior* to block `β = (v, a, n)` when `0 < c < n`.

**M4 (SplitDefinition).** For a mapping block `β = (v, a, n)` and interior point `0 < c < n`, the *split at `c`* produces two blocks:

```
β_L = (v, a, c)
β_R = (v + c, a + c, n − c)
```

Both are well-formed mapping blocks: `c ≥ 1` and `n − c ≥ 1` (since `0 < c < n`), and both starts are valid tumblers (by TA0, ASN-0034: the action point of `δ(c, #v)` is `#v`, satisfying the precondition `k ≤ #v`; similarly for `δ(c, #a)` and `#a`).

**M5 (SplitPartition).** The split is exact — nothing lost, nothing duplicated:

(a) `⟦β_L⟧ ∪ ⟦β_R⟧ = ⟦β⟧`

(b) `⟦β_L⟧ ∩ ⟦β_R⟧ = ∅`

*Verification of (a).* `⟦β_L⟧ = {(v + k, a + k) : 0 ≤ k < c}` and `⟦β_R⟧ = {((v + c) + j, (a + c) + j) : 0 ≤ j < n − c}`. Setting `k = c + j` — so that `(v + c) + j = v + (c + j) = v + k` by M-aux — the union covers `{(v + k, a + k) : 0 ≤ k < n} = ⟦β⟧`. ∎

*Verification of (b).* `V(β_L) = {v + k : 0 ≤ k < c}` and `V(β_R) = {v + k : c ≤ k < n}`. The ranges `[0, c)` and `[c, n)` are disjoint, so the V-extents are disjoint, and by the functionality of the mapping within each block, the full denotations are disjoint. ∎

What does each piece preserve? Nelson states the principle directly: "splitting is a Vstream operation that must be invisible to Istream properties." We verify each aspect.

**M6 (SplitPreservation).** Each piece independently preserves every property that derives from I-address identity:

(a) *Width coupling.* `|V(β_L)| = |I(β_L)| = c` and `|V(β_R)| = |I(β_R)| = n − c`. Each piece is a mapping block, so M0 applies.

(b) *Order preservation.* Both `β_L` and `β_R` satisfy M1. Each is a mapping block; M1 holds for every mapping block.

(c) *I-address fidelity.* For every pair `(v + k, a + k)` in `⟦β⟧`, the same pair appears in exactly one of `⟦β_L⟧` or `⟦β_R⟧`. No I-address is altered, dropped, or duplicated. This is M5 restated.

(d) *Origin traceability.* Each I-address `a + k` carries its origin permanently in its tumbler structure — `origin(a + k) = origin(a)`, since `a + k = a ⊕ δ(k, #a)` and TumblerAdd with action point `#a` copies `aᵢ` for all `i < #a`, preserving the document prefix `N.0.U.0.D` (S7, ASN-0036). Since the split alters no I-address, each piece independently identifies the home document of its content.

(e) *Structural independence.* Each piece is a self-contained mapping block whose well-formedness depends only on its own `(v, a, n)` triple — not on external state, not on the existence of the other piece.

The split changes how the arrangement is *represented*, not what the arrangement *is*.

**M6f (SplitFrame).** If `B` is a decomposition of `M(d)` containing `β`, then `(B \ {β}) ∪ {β_L, β_R}` is also a decomposition of `M(d)`, and the two decompositions are equivalent. All blocks in `B \ {β}` are unchanged.

*Verification.* B1 (coverage) is preserved by M5(a). B2 (disjointness) is preserved because `V(β_L) ∪ V(β_R) = V(β)` (by M5(a)) and `V(β_L) ∩ V(β_R) = ∅` (by M5(b)), so the new blocks occupy exactly the V-extent vacated by `β`, which was disjoint from all other blocks. B3 (consistency) follows from the definition of `β_L` and `β_R` — each maps its V-positions to the same I-addresses as `β` did. ∎

Gregory's implementation confirms the exactness. The `slicecbcpm` function applies the same scalar count — the V-offset of the cut — to both dimensions, using each dimension's own tumbler exponent. The resulting pieces preserve exact I-displacements and I-widths. The developer's own comment `/* I really don't understand this loop */` notwithstanding, the loop is correct precisely because the mantissa invariant (same byte count in both dimensions) is maintained through exact integer arithmetic with no rounding or alignment.

## Merging Adjacent Blocks

The inverse of splitting is merging. Nelson states the necessary and sufficient condition:

> "Two adjacent I-spans in a document may be combined if they describe V-contiguous elements which are also I-contiguous." [LM 4/36]

He restates it concretely:

> "They can be merged if one end of the next I-span can also be described as one past one end of the first." [LM 4/36]

We formalize both conditions.

**Definition (V-Adjacent).** Blocks `β₁ = (v₁, a₁, n₁)` and `β₂ = (v₂, a₂, n₂)` with `v₁ < v₂` are *V-adjacent* when `v₂ = v₁ + n₁` — the V-extent of `β₂` immediately follows that of `β₁`.

**Definition (I-Adjacent).** Blocks `β₁` and `β₂` (with `v₁ < v₂`) are *I-adjacent* when `a₂ = a₁ + n₁` — the I-extent of `β₂` immediately follows that of `β₁`.

**M7 (MergeCondition).** Two blocks `β₁ = (v₁, a₁, n₁)` and `β₂ = (v₂, a₂, n₂)` with `v₁ < v₂` may be merged into a single block if and only if they are both V-adjacent and I-adjacent:

`v₂ = v₁ + n₁  ∧  a₂ = a₁ + n₁`

When both conditions hold, the merged block is:

`β₁ ⊞ β₂ = (v₁, a₁, n₁ + n₂)`

(We write `⊞` for block merge to distinguish it from tumbler addition `⊕` of ASN-0034.)

Both conditions are necessary. V-adjacency alone is insufficient: if the I-extents are not contiguous, the merged block `(v₁, a₁, n₁ + n₂)` would predict `M(d)(v₁ + n₁) = a₁ + n₁`, but the arrangement maps that position to `a₂ ≠ a₁ + n₁`, violating B3. I-adjacency alone is insufficient: if the V-extents are not adjacent, there is no contiguous V-range for the merged block to cover.

*Verification.* `⟦β₁ ⊞ β₂⟧ = {(v₁ + k, a₁ + k) : 0 ≤ k < n₁ + n₂}`. For `k < n₁`, this gives `⟦β₁⟧`. For `k ≥ n₁`, set `j = k − n₁`: then `v₁ + k = (v₁ + n₁) + j = v₂ + j` and similarly `a₁ + k = a₂ + j` (by M-aux), giving `⟦β₂⟧`. So `⟦β₁ ⊞ β₂⟧ = ⟦β₁⟧ ∪ ⟦β₂⟧`. ∎

Gregory's implementation confirms the bidimensional requirement. The `isanextensionnd` function checks `lockeq(reach.dsas, originptr->dsas, dspsize(POOM))` with `dspsize(POOM) = 2`, requiring exact tumbler equality in both I and V dimensions simultaneously. Neither dimension alone suffices.

**M7f (MergeFrame).** If `B` is a decomposition of `M(d)` containing both `β₁` and `β₂`, then `(B \ {β₁, β₂}) ∪ {β₁ ⊞ β₂}` is an equivalent decomposition. All blocks in `B \ {β₁, β₂}` are unchanged.

*Verification.* Analogous to M6f: the merged block occupies exactly `V(β₁) ∪ V(β₂)` and maps each position to the same I-address as before. ∎

**M8 (MergeInformationLoss).** The merge is information-destroying with respect to the boundary. Given only `β₁ ⊞ β₂ = (v₁, a₁, n₁ + n₂)`, the individual widths `n₁` and `n₂` cannot be recovered. The merged block is indistinguishable from one that was never split.

This follows from the definition — the merged block is a triple `(v, a, n)` with no record of internal boundaries. Gregory confirms: a POOM bottom crum stores only `{displacement, width, homedoc}`, with no operation count, sub-span list, or boundary history. The merge at `insertnd.c:251` reduces to `dspadd` — scalar addition on the width, not annotated, not logged, not reversible. Even the spanfilade coalesces adjacent I-spans from the same source document, erasing the boundary there as well.

## The Split-Merge Duality

Split and merge are inverse operations. This is the algebraic core of the permutation model, and it holds because width coupling (M0) forces both dimensions to split and merge at the same count.

**M9 (SplitMergeInverse).** For any mapping block `β = (v, a, n)` and interior point `0 < c < n`, the two pieces produced by split satisfy the merge condition and merge back to the original:

```
split(β, c) = (β_L, β_R)
  where β_L = (v, a, c) and β_R = (v + c, a + c, n − c)

V-adjacency: v + c = v + c  ✓
I-adjacency: a + c = a + c  ✓

β_L ⊞ β_R = (v, a, c + (n − c)) = (v, a, n) = β  ∎
```

**M10 (MergeSplitInverse).** For any blocks `β₁ = (v₁, a₁, n₁)` and `β₂ = (v₂, a₂, n₂)` satisfying the merge condition (`v₂ = v₁ + n₁`, `a₂ = a₁ + n₁`), splitting the merged block at the original boundary recovers both:

```
split(β₁ ⊞ β₂, n₁)
  = ((v₁, a₁, n₁), (v₁ + n₁, a₁ + n₁, n₂))
  = (β₁, β₂)  ∎
```

M9 and M10 together establish a bijection between `{block with interior cut point}` and `{pair of mergeable blocks}`. The algebra is clean — it works precisely because width coupling forces both dimensions to split and merge at the same ordinal count.

## The Canonical Decomposition

Among all equivalent decompositions of a given arrangement, there is a distinguished one — the one where every possible merge has been performed.

**Definition (Maximally Merged).** A block decomposition `B` is *maximally merged* when no two blocks in `B` satisfy the merge condition (M7). For every pair `βᵢ, βⱼ ∈ B` with `i ≠ j`: they are not V-adjacent, or they are not I-adjacent, or both.

**M11 (CanonicalExistence).** Every arrangement `M(d)` admits a maximally merged block decomposition.

*Construction.* Start with any decomposition `B` (which exists by M2). While there exist `βᵢ, βⱼ ∈ B` satisfying the merge condition: replace them with `βᵢ ⊞ βⱼ` (by M7f, the result is an equivalent decomposition). Each merge reduces `|B|` by exactly 1 and preserves equivalence. The process terminates because `|B|` is finite and bounded below by 1 for non-empty `M(d)`. ∎

We must now establish that the result is independent of merge order.

**M12 (CanonicalUniqueness).** The maximally merged decomposition is unique.

*Proof.* We show that every maximally merged decomposition equals the set of *maximal runs* of `f = M(d)`, and that this set is uniquely determined by `f`.

Define a *maximal run* of `f` as a triple `(v, a, n)` such that:
1. `(A k : 0 ≤ k < n : f(v + k) = a + k)` — it is a correspondence run
2. `¬(E v' :: v' + 1 = v ∧ v' ∈ dom(f) ∧ f(v') + 1 = a)` — it cannot be extended left
3. `v + n ∉ dom(f)  ∨  f(v + n) ≠ a + n` — it cannot be extended right

(Condition 2 uses only TumblerAdd, avoiding TumblerSub which is not well-defined for ordinal decrement at arbitrary tumbler depth. Leftward extension terminates because `dom(f)` is finite — the run cannot be extended beyond the leftmost position in `dom(f)`.)

The maximal runs partition `dom(f)`: every `v ∈ dom(f)` belongs to at least one maximal run (start with the trivial run `(v, f(v), 1)` and extend in both directions until conditions 2 and 3 are met). To see that `v` belongs to *exactly* one maximal run, suppose `v ∈ R₁ ∩ R₂` where `R₁ = (v₁, a₁, n₁)` and `R₂ = (v₂, a₂, n₂)` with `v₁ ≤ v₂`. Since V-extents are contiguous ranges at fixed depth (S8-depth), `v₁ ≤ v₂ ≤ v` and `v ∈ V(R₁)` imply `v₂ ∈ V(R₁)`, so `v₂ = v₁ + k₂` for some `0 ≤ k₂ < n₁`. Both runs map `v₂` through `f`, giving `a₂ = a₁ + k₂`. If `v₁ < v₂` — i.e., `k₂ ≥ 1` — set `v' = v₁ + (k₂ − 1)`, which is in `V(R₁)`. By M-aux, `v' + 1 = v₁ + k₂ = v₂`, and `f(v') + 1 = (a₁ + (k₂ − 1)) + 1 = a₁ + k₂ = a₂`. So `R₂` can be extended left, contradicting condition 2. Hence `v₁ = v₂` (and so `a₂ = a₁ + 0 = a₁`). For the lengths, suppose WLOG `n₁ < n₂`. Then `v₁ + n₁ ∈ V(R₂)` (at offset `n₁ < n₂` from `v₂ = v₁`), so `v₁ + n₁ ∈ dom(f)` and `f(v₁ + n₁) = a₂ + n₁ = a₁ + n₁` by condition 1 of `R₂`. But condition 3 of `R₁` requires `v₁ + n₁ ∉ dom(f) ∨ f(v₁ + n₁) ≠ a₁ + n₁` — contradiction. The symmetric case `n₂ < n₁` contradicts condition 3 of `R₂` by the same reasoning (with `R₁` supplying the witness). So `n₁ = n₂`. The maximal runs are therefore uniquely determined by `f`.

We show: a decomposition `B` is maximally merged iff it equals the set of maximal runs of `f`.

(⟹) Let `B` be maximally merged. Take `β = (v, a, n) ∈ B` and suppose `β` is not a maximal run — say condition 3 fails: `v + n ∈ dom(f)` and `f(v + n) = a + n`. Some block `β' ∈ B` covers `v + n`. We claim `β'` starts at `v + n`. If `β'` starts at `v' < v + n`, then `V(β') = {v' + k : 0 ≤ k < n'}` is a contiguous set containing `v + n` and starting before it; since `v + n − 1 ∈ V(β)`, we would have `v + n − 1 ∈ V(β')` when `v' ≤ v + n − 1`, contradicting B2 (disjointness). So `v' > v + n − 1`. Since all text-subspace V-positions in `dom(M(d))` share the same depth (S8-depth, ASN-0036), no V-position falls between `v + (n − 1)` and `v + n`, forcing `v' = v + n`. Then `β' = (v + n, a', n')` with `a' + 0 = f(v + n) = a + n`, so `a' = a + n`. Now `β` and `β'` are V-adjacent (`v + n = v + n`) and I-adjacent (`a + n = a + n`) — contradicting `B` being maximally merged.

Now suppose condition 2 fails: there exists `v'` with `v' + 1 = v`, `v' ∈ dom(f)`, and `f(v') + 1 = a`. Some block `β'' = (v'', a'', n'') ∈ B` covers `v'`. Since `v' + 1 = v ∈ V(β)`, if `v ∈ V(β'')` then `v ∈ V(β'') ∩ V(β)`, contradicting B2. So `v'` is the last position of `β''`: `v' = v'' + (n'' − 1)`. By M-aux, `v'' + n'' = v' + 1 = v` (V-adjacent). And `a'' + n'' = (a'' + (n'' − 1)) + 1 = f(v') + 1 = a` (I-adjacent, since `f(v') = a'' + (n'' − 1)` by B3). So `β''` and `β` satisfy the merge condition — contradicting `B` being maximally merged. Hence every block in `B` is a maximal run. Since the maximal runs partition `dom(f)` and `B` covers `dom(f)` (by B1) with disjoint blocks (by B2), `B` is exactly the set of maximal runs.

(⟸) The set of maximal runs is trivially maximally merged: any two V-adjacent maximal runs have a correspondence discontinuity at their boundary (by condition 3 of the left run), so they are not I-adjacent and cannot be merged.

Since the maximal runs are uniquely determined by `f`, and every maximally merged decomposition equals the set of maximal runs, the maximally merged decomposition is unique. ∎

Nelson observes: "The representation with the fewest I-spans is the most compact." [LM 4/37] The maximally merged decomposition is this most compact representation — uniquely determined by the arrangement `M(d)`, independent of any choice of representation or any history of how the arrangement was constructed.

### A Worked Example

Consider a document `d` with eight text-subspace V-positions, `[1, k]` for `k = 1, ..., 8`, arranged as follows (tumblers shown are element-field ordinals; the full document prefix `N.0.U.0.D.0.` is elided):

| V-position | I-address |
|------------|-----------|
| `[1, 1]` | `[1, 10]` |
| `[1, 2]` | `[1, 11]` |
| `[1, 3]` | `[1, 12]` |
| `[1, 4]` | `[1, 13]` |
| `[1, 5]` | `[1, 14]` |
| `[1, 6]` | `[1, 40]` |
| `[1, 7]` | `[1, 41]` |
| `[1, 8]` | `[1, 42]` |

We start with a three-block decomposition `B = {β₁, β₂, β₃}`:

- `β₁ = ([1, 1], [1, 10], 3)` — V: `[1, 1]..[1, 3]`, I: `[1, 10]..[1, 12]`
- `β₂ = ([1, 4], [1, 13], 2)` — V: `[1, 4]..[1, 5]`, I: `[1, 13]..[1, 14]`
- `β₃ = ([1, 6], [1, 40], 3)` — V: `[1, 6]..[1, 8]`, I: `[1, 40]..[1, 42]`

The V-extents partition `{[1, k] : 1 ≤ k ≤ 8}`, and each block correctly describes `M(d)` — B1–B3 are satisfied.

**Merge check.** We test the merge condition (M7) on each V-adjacent pair:

- `β₁` and `β₂`: V-adjacent? `v₂ = [1, 4] = [1, 1] + 3` ✓. I-adjacent? `a₂ = [1, 13] = [1, 10] + 3` ✓. Both conditions hold — the blocks merge to `β₁ ⊞ β₂ = ([1, 1], [1, 10], 5)`.

- `β₂` and `β₃`: V-adjacent? `v₃ = [1, 6] = [1, 4] + 2` ✓. I-adjacent? `a₃ = [1, 40] ≠ [1, 13] + 2 = [1, 15]` ✗. The I-extents are not contiguous — cannot merge.

After merging, the decomposition is `B' = {([1, 1], [1, 10], 5),\; ([1, 6], [1, 40], 3)}`.

**Canonicality check.** The surviving pair: V-adjacent? `[1, 6] = [1, 1] + 5` ✓. I-adjacent? `[1, 40] ≠ [1, 10] + 5 = [1, 15]` ✗. No mergeable pair remains, so `B'` is maximally merged. By M12, this is the unique canonical decomposition.

The boundary at V-position `[1, 6]` persists because V-adjacency holds but I-adjacency does not — confirming M7's necessity. The I-addresses jump from `[1, 14]` to `[1, 40]`, indicating that content at `[1, 6]..[1, 8]` was allocated at a different point in the Istream than content at `[1, 1]..[1, 5]`.

## Shared Content

We have been careful to call the V→I function a "mapping" rather than a "permutation" in the strict algebraic sense. The function `M(d)` is not necessarily injective — the same I-address can appear at multiple V-positions.

**M13 (SharedContent).** The arrangement `M(d)` permits multiple V-positions to share the same I-address:

`(E Σ : Σ satisfies S0–S3 : (E d, a :: |{v : M(d)(v) = a}| > 1))`

This is transclusion within a single document — the same content appearing at multiple points in the same arrangement. Nelson confirms the mechanism is unrestricted:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document." [LM 4/11]

The same content can be included at multiple positions. Each occurrence is a separate mapping block — the blocks share I-extents but have disjoint V-extents (by B2). This is consistent with S5 (UnrestrictedSharing, ASN-0036), which establishes that no bound limits the number of V-positions referencing a given I-address.

**M14 (IndependentOccurrences).** When two mapping blocks `β₁ = (v₁, a, n)` and `β₂ = (v₂, a, n)` in a decomposition share their I-start and width (with `v₁ ≠ v₂`), they are independent entries that cannot be merged.

*Verification.* The merge condition (M7) requires `a₂ = a₁ + n₁`. Here `a₂ = a₁ = a`, so the condition requires `a = a + n`. Since `n ≥ 1`, `a + n > a` by TA-strict (ASN-0034), so `a + n ≠ a`. The I-adjacency condition is unsatisfiable; the blocks cannot merge and are permanently distinct. ∎

More generally, any two blocks with partially overlapping I-extents at distinct V-positions are independently tracked. The mapping block algebra does not conflate shared content — it preserves each occurrence as a separate representational entity.

## Document Independence

Each document's arrangement is independently represented. This is a direct consequence of ASN-0036's framework — `M(d)` is per-document — but it has concrete consequences for the mapping block algebra.

**M15 (MappingIndependence).** For any two documents `d₁ ≠ d₂`:

(a) Block decompositions are per-document objects; membership of a triple `(v, a, n)` in a decomposition of `M(d₁)` entails no relationship to any decomposition of `M(d₂)`.

(b) Splitting or merging blocks in a decomposition of `M(d₁)` does not alter any block in any decomposition of `M(d₂)`.

Nelson states this unambiguously:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

If deletion — the most destructive arrangement operation — cannot affect other documents' mappings, then no arrangement operation can. Two documents may reference the same I-addresses (by transclusion), but their mapping blocks are separate objects in separate decompositions. Changes to one document's arrangement are invisible to every other document's.

## Cross-Origin Merge Impossibility

The merge condition (M7) interacts naturally with the tumbler address structure.

**M16 (CrossOriginMergeImpossibility).** If `origin(a₁) ≠ origin(a₂)` — the I-addresses in two blocks were allocated by different documents — then the blocks cannot satisfy I-adjacency:

`(A β₁, β₂ : origin(a₁) ≠ origin(a₂) : ¬(a₂ = a₁ + n₁))`

*Proof.* The ordinal shift `a₁ + n₁ = a₁ ⊕ δ(n₁, #a₁)` has action point `#a₁`. By TumblerAdd (ASN-0034), `rᵢ = (a₁)ᵢ` for all `i < #a₁` — every component before the action point is copied unchanged. For element-level I-addresses, the document prefix `N.0.U.0.D` occupies positions strictly before `#a₁`, so it is preserved. Therefore `origin(a₁ + n₁) = origin(a₁)`. If `origin(a₂) ≠ origin(a₁)`, then `origin(a₂) ≠ origin(a₁ + n₁)`. Since `origin` is a function on tumblers, equal tumblers have equal origins; by contrapositive, different origins imply different tumblers: `a₂ ≠ a₁ + n₁`. ∎

This is not an additional constraint imposed on the merge — it is a consequence of I-adjacency and the invariance of document origin under ordinal increment. Gregory's implementation includes an explicit `homedoc` guard as the first check in `isanextensionnd` — a cheap discriminant that avoids full I-address comparison. At the abstract level, the guard is redundant: the contrapositive of origin equality already prevents cross-origin I-adjacency. But its presence in the implementation reflects the abstract property and provides an efficient short-circuit.

The consequence is that the canonical decomposition naturally preserves origin boundaries. In a maximally merged decomposition, every block maps to a contiguous I-range under a single document prefix. Blocks spanning multiple origins cannot arise, because the I-addresses of distinct origins are never adjacent on the tumbler line.

## Content References

The block algebra characterizes how arrangements decompose into contiguous runs. We now define content references — a mechanism for identifying a span of positions within a document's arrangement — and resolution, which extracts the I-address runs from the block decomposition restricted to that span. The canonical decomposition (M11, M12) applies to any restriction of an arrangement satisfying the structural preconditions, and every resolved I-address satisfies referential integrity. We work with the content store C : T ⇀ Val and per-document arrangement M(d) : T ⇀ T from ASN-0036. Let D be the set of documents for which an arrangement is defined. The definitions below reference: S2 (ArrangementFunctionality), S3 (ReferentialIntegrity), S8-fin (FiniteArrangement), S8-depth (FixedDepthVPositions) from ASN-0036; T12 (SpanWellDefinedness) from ASN-0034; S6 (LevelConstraint) and ⟦σ⟧ (SpanDenotation) from ASN-0053.

**Definition (ContentReference).** A *content reference* is a pair (d_s, σ) where d_s ∈ D and σ = (u, ℓ) is a level-uniform V-span satisfying: (i) V_{u₁}(d_s) ≠ ∅ — the subspace contains at least one V-position; (ii) T12 (ASN-0034) holds; (iii) `#ℓ = #u = m`, where m is the common V-position depth in subspace u₁ of d_s (S8-depth, ASN-0036); and (iv) m ≥ 2. Precondition (i) is necessary: S8-depth is vacuously true for an empty subspace and does not determine a common depth, so m is well-defined only when at least one V-position exists. Precondition (iv) ensures subspace confinement — that ⟦σ⟧ does not cross subspace boundaries; the derivation follows from C0a below. The level-uniformity requirement ensures reach(σ) has depth m (S6, ASN-0053), so the position range is well-bounded and the span algebra (S1–S11, ASN-0053) applies. The content reference is well-formed when every depth-m position in the span's range belongs to d_s's arrangement:

`{v ∈ T : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d_s))`

By C0a (below), prefix confinement gives tⱼ = uⱼ for all j < m for every t ∈ ⟦σ⟧; in particular t₁ = u₁, so dom(M(d_s)) ∩ ⟦σ⟧ ⊆ V_{u₁}(d_s). By S8-depth, all V-positions in V_{u₁}(d_s) have depth m, and reach(σ) has depth m (S6), so the depth-m restriction is structurally guaranteed.

**C0 (OrdinalDisplacementNecessity).** For a well-formed content reference (d_s, σ) with σ = (u, ℓ), common depth m, and action point k of ℓ: k = m. Equivalently, ℓ = δ(ℓₘ, m) — an ordinal displacement.

*Derivation.* Suppose for contradiction that k < m. Consider the family of depth-m tumblers wⱼ = [u₁, ..., uₖ, uₖ₊₁, ..., u_{m−1}, j] for j > uₘ. Each wⱼ satisfies u < wⱼ: the two agree on components 1 through m − 1 and j > uₘ at component m, so wⱼ > u by T1(i) (ASN-0034). Each wⱼ satisfies wⱼ < reach(σ): at component k, uₖ < uₖ + ℓₖ (since ℓₖ ≥ 1, k being the action point), so wⱼ < reach(σ) by T1(i). Thus wⱼ ∈ ⟦σ⟧ for every j > uₘ. By T0(a) (ASN-0034), j ranges over unboundedly many values, yielding infinitely many depth-m tumblers in ⟦σ⟧. Well-formedness requires each to be in dom(M(d_s)), contradicting S8-fin (ASN-0036). Therefore k = m, and ℓ = [0, ..., 0, ℓₘ] = δ(ℓₘ, m). ∎

**C0a (PrefixConfinement).** For a well-formed content reference (d_s, σ) with σ = (u, ℓ) and m ≥ 2: every t ∈ ⟦σ⟧ satisfies tⱼ = uⱼ for all 1 ≤ j < m.

*Derivation.* By C0, the action point of ℓ is m. Since m ≥ 2, TumblerAdd gives reach(σ)ⱼ = uⱼ for all j < m. Fix any t ∈ ⟦σ⟧, so u ≤ t < reach(σ). Suppose for contradiction that J = {j : 1 ≤ j < m ∧ tⱼ ≠ uⱼ} is non-empty, and let j₀ = min(J). Then tᵢ = uᵢ for all 1 ≤ i < j₀, so the divergence of t and u is at position j₀. Since u ≤ t, T1(i) (ASN-0034) gives t_{j₀} > u_{j₀}. Since reach(σ)_{j₀} = u_{j₀} and tᵢ = uᵢ = reach(σ)ᵢ for all i < j₀, the divergence of t and reach(σ) is also at j₀ with t_{j₀} > reach(σ)_{j₀}. By T1(i), t > reach(σ), contradicting t < reach(σ). Therefore J = ∅. Moreover, #t ≥ m: if #t < m, then J = ∅ forces tⱼ = uⱼ for all 1 ≤ j ≤ #t, making t a proper prefix of u; T1(ii) gives t < u, contradicting u ≤ t. Hence tⱼ is defined for all 1 ≤ j < m, and J = ∅ gives tⱼ = uⱼ for all 1 ≤ j < m. In particular, t₁ = u₁ (subspace confinement). (At m = 1, the vacuous range 1 ≤ j < 1 yields no confinement; indeed the action point would be 1, giving reach(σ)₁ = u₁ + ℓ₁ ≠ u₁, and ⟦σ⟧ would span multiple subspaces.) ∎

**Definition (ContentReferenceSequence).** A *content reference sequence* is an ordered list R = ⟨r₁, ..., rₚ⟩ of content references with p ≥ 1. Different references may name different source documents.


## Resolution

To resolve a content reference, we extract the I-address runs corresponding to the named V-span. The source document's mapping may not be ordinal-contiguous across the full span — prior editing may have interleaved content from multiple allocations, fragmenting the V→I mapping into several contiguous I-address runs.

**Definition (Resolution).** Given content reference (d_s, σ) with σ = (u, ℓ), let f = M(d_s)|⟦σ⟧ be the restriction of M(d_s) to positions in ⟦σ⟧.

**C1a (RestrictionDecomposition).** M11 and M12 hold for any finite partial function f : T ⇀ T satisfying S2, S8-fin, and S8-depth. In particular, the restriction f = M(d_s)|⟦σ⟧ admits a unique maximally merged block decomposition.

*Verification that f satisfies the conditions.* (i) S2 (functionality): f is a restriction of M(d_s), which is functional by S2; a restriction of a function is a function. (ii) S8-fin (finite domain): dom(f) ⊆ dom(M(d_s)), which is finite by S8-fin; a subset of a finite set is finite. (iii) S8-depth (fixed depth): by C0a, every position in dom(f) has first component u₁, so dom(f) ⊆ V_{u₁}(d_s); by S8-depth, all positions in V_{u₁}(d_s) share the common depth m.

*Extension of M11/M12.* M11 (CanonicalExistence) constructs a maximally merged decomposition by iterating: while any two blocks satisfy the merge condition (M7), merge them. The initial singleton-block decomposition — one block (v, f(v), 1) per v ∈ dom(f) — satisfies B1, B2, and B3: B1 (coverage) holds because every v ∈ dom(f) has its own singleton block; B2 (disjointness) holds because singleton V-extents are pairwise disjoint; B3 (consistency) holds directly from S2 (f is a function, so each singleton block's I-address is uniquely determined). Termination follows from S8-fin since the block count is at most |dom(f)|. Each merge step preserves all three conditions by M7f (MergeFrame): M7f establishes that replacing β₁ and β₂ with β₁ ⊞ β₂ yields an equivalent decomposition, preserving B1 and B2 via V(β₁ ⊞ β₂) = V(β₁) ∪ V(β₂) (no V-position is gained or lost, and all blocks in B \ {β₁, β₂} are unchanged). For B3 specifically: if β₁ = (v₁, a₁, n₁) and β₂ = (v₂, a₂, n₂) each satisfy B3 and M7 holds (v₂ = v₁ + n₁, a₂ = a₁ + n₁), then β₁ ⊞ β₂ = (v₁, a₁, n₁ + n₂) satisfies B3 by case split — for 0 ≤ i < n₁, f(v₁ + i) = a₁ + i by B3 for β₁; for n₁ ≤ i < n₁ + n₂, f(v₁ + i) = f(v₂ + (i − n₁)) = a₂ + (i − n₁) = (a₁ + n₁) + (i − n₁) = a₁ + i, using B3 for β₂ and M-aux. M12 (CanonicalUniqueness) identifies the maximally merged decomposition with the set of maximal runs of f, using only pointwise evaluation of f — independent of whether f is a full arrangement or a restriction. Both proofs require no property of M(d) beyond S2, S8-fin, and S8-depth; they apply to f verbatim. ∎

The decomposition yields ⟨β₁, ..., βₖ⟩ ordered by V-start. The *I-address sequence* is:

`resolve(d_s, σ) = ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩`

where βⱼ = (vⱼ, aⱼ, nⱼ). The V-coordinates are discarded; only I-starts and widths are carried forward.

The ordering of runs within each resolution preserves the source document's V-ordering: if V-position p precedes V-position q in the source, the I-address at p precedes the I-address at q in the resolved sequence. This follows from the definition of resolve, which specifies the blocks ordered by V-start. The ordering is well-defined because V-extents are disjoint (B2), so the V-starts induce a total order on the blocks.

For a content reference sequence R = ⟨r₁, ..., rₚ⟩, the *composite resolution* concatenates:

`resolve(R) = resolve(r₁) ⌢ ... ⌢ resolve(rₚ)`

Each reference is resolved independently against its own source document's POOM. The *total width* of an I-address sequence ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩ is:

`w(⟨(a₁, n₁), ..., (aₖ, nₖ)⟩) = (+ j : 1 ≤ j ≤ k : nⱼ)`

For a content reference sequence R, the total width is w(resolve(R)).

**C1 (ResolutionIntegrity).** Every resolved I-address is in dom(C):

`(A j : 1 ≤ j ≤ k : (A i : 0 ≤ i < nⱼ : aⱼ + i ∈ dom(C)))`

*Derivation.* Fix any run (aⱼ, nⱼ) in the resolution and any i with 0 ≤ i < nⱼ. The corresponding block βⱼ = (vⱼ, aⱼ, nⱼ) satisfies B3: M(d_s)(vⱼ + i) = aⱼ + i. Since vⱼ + i ∈ dom(M(d_s)), S3 (ReferentialIntegrity, ASN-0036) gives M(d_s)(vⱼ + i) ∈ dom(C), hence aⱼ + i ∈ dom(C). ∎

**C2 (ResolutionWidthPreservation).** For a well-formed content reference (d_s, σ) with σ = (u, δ(ℓₘ, m)), the total resolved width equals ℓₘ:

`w(resolve(d_s, σ)) = (+ j : 1 ≤ j ≤ k : nⱼ) = ℓₘ`

*Derivation.* By C0, ℓ = δ(ℓₘ, m), so reach(σ) = u ⊕ δ(ℓₘ, m) = [u₁, ..., u_{m−1}, uₘ + ℓₘ]. The depth-m tumblers in [u, reach(σ)) are exactly {[u₁, ..., u_{m−1}, j] : uₘ ≤ j < uₘ + ℓₘ}: by C0a (PrefixConfinement), every t ∈ ⟦σ⟧ satisfies tⱼ = uⱼ for all 1 ≤ j < m, fixing the first m − 1 components; the m-th component then ranges over uₘ ≤ tₘ < uₘ + ℓₘ (from u ≤ t < reach(σ) at divergence point m). There are ℓₘ such tumblers; well-formedness places each in dom(f). Conversely, dom(f) contains no other elements: C0a fixes all components before m, and S8-depth ensures every position in V_{u₁}(d_s) has depth m, so the enumeration is exhaustive. Therefore |dom(f)| = ℓₘ. By B1 (coverage) and B2 (disjointness), the V-extents of the blocks partition dom(f). By M0 (width coupling), |V(βⱼ)| = nⱼ for each block. Therefore (+ j : 1 ≤ j ≤ k : nⱼ) = |dom(f)| = ℓₘ. ∎

### A Worked Example

We verify the definitions against a concrete scenario. Let document d have depth-2 V-positions in subspace 1 (m = 2) with canonical decomposition:

`B = {β₁ = ([1,1], a, 3),  β₂ = ([1,4], b, 2),  β₃ = ([1,6], c, 1)}`

where a, b, c are distinct I-addresses with `origin(a) ≠ origin(b) ≠ origin(c)` — three runs of content transcluded from three distinct source documents. The arrangement maps six V-positions: M(d)([1,1]) = a, M(d)([1,2]) = a+1, M(d)([1,3]) = a+2, M(d)([1,4]) = b, M(d)([1,5]) = b+1, M(d)([1,6]) = c.

**Content reference.** Take σ = ([1,2], δ(4, 2)) — start at V-position [1,2] with ordinal displacement [0,4]. Then reach(σ) = [1,2] ⊕ [0,4] = [1,6]. The span range is {v : [1,2] ≤ v < [1,6] ∧ #v = 2} = {[1,2], [1,3], [1,4], [1,5]}. Each is in dom(M(d)), so the reference is well-formed. The displacement is ordinal (action point 2 = m), consistent with C0.

**Restriction.** f = M(d)|⟦σ⟧ has domain {[1,2], [1,3], [1,4], [1,5]} with f([1,2]) = a+1, f([1,3]) = a+2, f([1,4]) = b, f([1,5]) = b+1.

**Decomposition (C1a).** We verify f satisfies the preconditions: (i) f is functional (restriction of a function); (ii) dom(f) has 4 elements (finite); (iii) all V-positions have depth 2. Starting from singleton blocks {([1,2], a+1, 1), ([1,3], a+2, 1), ([1,4], b, 1), ([1,5], b+1, 1)}, we merge:

- [1,2] and [1,3]: V-adjacent ([1,3] = [1,2]+1) and I-adjacent (a+2 = (a+1)+1). Merge → ([1,2], a+1, 2).
- [1,4] and [1,5]: V-adjacent ([1,5] = [1,4]+1) and I-adjacent (b+1 = b+1). Merge → ([1,4], b, 2).

No further merges: ([1,2], a+1, 2) and ([1,4], b, 2) are V-adjacent ([1,4] = [1,2]+2) but not I-adjacent. M16 gives b ≠ (a+1)+2: ordinal increment preserves the document prefix, so origin((a+1)+2) = origin(a), while origin(b) ≠ origin(a) by construction. The decomposition is maximally merged.

**Resolution.** resolve(d, σ) = ⟨(a+1, 2), (b, 2)⟩, ordered by V-start.

**C1 verification.** For run (a+1, 2): B3 gives M(d)([1,2]) = a+1 and M(d)([1,3]) = a+2; S3 gives a+1 ∈ dom(C) and a+2 ∈ dom(C). For run (b, 2): B3 gives M(d)([1,4]) = b and M(d)([1,5]) = b+1; S3 gives b ∈ dom(C) and b+1 ∈ dom(C). ✓

Total width: 2 + 2 = 4 = ℓₘ, confirming C2.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| M0 | WidthCoupling: `\|V(β)\| = \|I(β)\| = n` for mapping block `β = (v, a, n)` | introduced |
| M1 | OrderPreservation: within a block, the `k`-th V-position maps to the `k`-th I-address; both orderings agree | introduced |
| M-aux | OrdinalIncrementAssociativity: `(v + c) + j = v + (c + j)` — from TS3 (ShiftComposition, ASN-0034) extended with `v + 0 = v` | introduced |
| M2 | DecompositionExistence: every text-subspace arrangement admits a block decomposition | introduced |
| M3 | RepresentationInvariance: equivalent decompositions determine the same arrangement function | introduced |
| M4 | SplitDefinition: split at interior `c` produces `β_L = (v, a, c)` and `β_R = (v+c, a+c, n−c)` | introduced |
| M5 | SplitPartition: `⟦β_L⟧ ∪ ⟦β_R⟧ = ⟦β⟧` and `⟦β_L⟧ ∩ ⟦β_R⟧ = ∅` | introduced |
| M6 | SplitPreservation: each piece independently preserves width coupling, order, I-fidelity, origin, and structural independence | introduced |
| M6f | SplitFrame: the arrangement `M(d)` is unchanged; only the decomposition changes | introduced |
| M7 | MergeCondition: merge requires V-adjacency (`v₂ = v₁ + n₁`) AND I-adjacency (`a₂ = a₁ + n₁`); result is `(v₁, a₁, n₁ + n₂)` | introduced |
| M7f | MergeFrame: the arrangement `M(d)` is unchanged; only the decomposition changes | introduced |
| M8 | MergeInformationLoss: the internal boundary is irrecoverably lost; merged block is indistinguishable from one never split | introduced |
| M9 | SplitMergeInverse: splitting then merging recovers the original block | introduced |
| M10 | MergeSplitInverse: merging then splitting at the boundary recovers both original blocks | introduced |
| M11 | CanonicalExistence: every arrangement admits a maximally merged decomposition | introduced |
| M12 | CanonicalUniqueness: the maximally merged decomposition is unique (equals the set of maximal runs of `M(d)`) | introduced |
| M13 | SharedContent: multiple V-positions may map to the same I-address within a single arrangement | introduced |
| M14 | IndependentOccurrences: blocks sharing I-extent at distinct V-positions are independent and unmergeable | introduced |
| M15 | MappingIndependence: each document's block decomposition is independent of every other document's | introduced |
| M16 | CrossOriginMergeImpossibility: blocks whose I-addresses originate from different documents cannot satisfy I-adjacency | introduced |
| B1 | Coverage: blocks in a decomposition partition the text-subspace V-positions of `dom(M(d))` | introduced |
| B2 | Disjointness: no two blocks share a V-position | introduced |
| B3 | Consistency: each block correctly describes `M(d)` | introduced |
| ContentReference | (d_s, σ) with d_s ∈ D, V_{u₁}(d_s) ≠ ∅, m ≥ 2; σ level-uniform with #u = #ℓ = m; depth-m V-positions in span range ⊆ dom(M(d_s)) | introduced |
| C0 | OrdinalDisplacementNecessity: well-formed content references have ordinal displacements — action point of ℓ equals m | introduced |
| C0a | PrefixConfinement: every t ∈ ⟦σ⟧ satisfies tⱼ = uⱼ for all 1 ≤ j < m when m ≥ 2 (subspace confinement t₁ = u₁ is the j = 1 case) | introduced |
| ContentReferenceSequence | ordered list ⟨r₁, ..., rₚ⟩ with p ≥ 1 | introduced |
| resolve(d_s, σ) | Resolution: maximally merged I-address runs from `M(d_s)\|⟦σ⟧`, V-ordered | introduced |
| C1a | RestrictionDecomposition: M11/M12 hold for any finite partial function f : T ⇀ T satisfying S2, S8-fin, S8-depth; in particular `M(d_s)\|⟦σ⟧` | introduced |
| C1 | ResolutionIntegrity: every resolved I-address is in dom(C) | introduced |
| C2 | ResolutionWidthPreservation: total resolved width equals ordinal displacement — w(resolve(d_s, σ)) = ℓₘ | introduced |

## Open Questions

When two V-adjacent blocks in the canonical decomposition fail the merge condition, what is the precise structure of the I-space discontinuity at their boundary — must it be a forward gap, or can it be an arbitrary jump to an unrelated I-region?

Is the set of equivalent decompositions of a given arrangement a lattice under the refinement ordering, with the canonical decomposition as the coarsest element?

What constraints govern the relationship between the total V-extent of an arrangement and the number of blocks in its canonical decomposition?

Does width coupling (M0) entail constraints on the tumbler depth relationship between V-starts and I-starts within a single block?

Must the resolution ordering across a multi-source content reference sequence preserve the sequence order, or may an implementation reorder source references provided the placed content lands at the correct V-positions?
