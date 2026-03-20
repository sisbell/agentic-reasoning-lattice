# ASN-0058: The Permutation Model

*2026-03-20*

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

where `v + k` and `a + k` denote `k` ordinal increments via TA5(c) (ASN-0034). The *V-extent* is `V(β) = {v + k : 0 ≤ k < n}`; the *I-extent* is `I(β) = {a + k : 0 ≤ k < n}`.

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

*Convention.* We define `v + 0 = v` — the identity of ordinal shift. At `k = 0` this is the base case of the correspondence run: `M(d)(v) = a`, no displacement, no arithmetic (cf. S8, ASN-0036). The cases `c = 0` or `j = 0` in the identity above follow immediately from this convention.

*Derivation (c, j ≥ 1).* Recall that `v + k` for `k ≥ 1` denotes `v ⊕ w_k` where `w_k = [0, ..., 0, k]` has length `#v` and action point at position `#v`. By TA-assoc (ASN-0034), `(v ⊕ w_c) ⊕ w_j = v ⊕ (w_c ⊕ w_j)`. By TumblerAdd, `w_c` and `w_j` share their action point at position `#v`, so `(w_c ⊕ w_j)` has value `c + j` at that position and zero elsewhere — that is, `w_c ⊕ w_j = w_{c+j}`. Therefore `(v + c) + j = v ⊕ w_{c+j} = v + (c + j)`. ∎

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

Both are well-formed mapping blocks: `c ≥ 1` and `n − c ≥ 1` (since `0 < c < n`), and both starts are valid tumblers (by TA5, ASN-0034).

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

(d) *Origin traceability.* Each I-address `a + k` carries its origin permanently in its tumbler structure — `origin(a + k) = origin(a)`, since ordinal increment via TA5(c) changes only the element field, preserving the document prefix (S7, ASN-0036). Since the split alters no I-address, each piece independently identifies the home document of its content.

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

Both conditions are necessary. V-adjacency alone is insufficient: if the I-extents are not contiguous, the merged range would map consecutive V-positions to non-consecutive I-addresses, violating M1. I-adjacency alone is insufficient: if the V-extents are not adjacent, there is no contiguous V-range for the merged block to cover.

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

(Condition 2 uses only TumblerAdd, avoiding TumblerSub which is not well-defined for ordinal decrement at arbitrary tumbler depth. The condition is vacuously satisfied when the last component of `v` equals 1: the only candidate `v'` would require a zero last component, placing it outside `dom(f)` by S8a, ASN-0036.)

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

*Proof.* Ordinal increment via TA5(c) (ASN-0034) changes only the last significant component of a tumbler, which for element-level addresses falls in the element field. The document prefix — the `N.0.U.0.D` portion — is invariant under ordinal increment. Therefore `origin(a₁ + n₁) = origin(a₁)`. If `origin(a₂) ≠ origin(a₁)`, then `origin(a₂) ≠ origin(a₁ + n₁)`. Since `origin` is a function on tumblers, equal tumblers have equal origins; by contrapositive, different origins imply different tumblers: `a₂ ≠ a₁ + n₁`. ∎

This is not an additional constraint imposed on the merge — it is a consequence of I-adjacency and the invariance of document origin under ordinal increment. Gregory's implementation includes an explicit `homedoc` guard as the first check in `isanextensionnd` — a cheap discriminant that avoids full I-address comparison. At the abstract level, the guard is redundant: the contrapositive of origin equality already prevents cross-origin I-adjacency. But its presence in the implementation reflects the abstract property and provides an efficient short-circuit.

The consequence is that the canonical decomposition naturally preserves origin boundaries. In a maximally merged decomposition, every block maps to a contiguous I-range under a single document prefix. Blocks spanning multiple origins cannot arise, because the I-addresses of distinct origins are never adjacent on the tumbler line.

## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| M0 | WidthCoupling: `\|V(β)\| = \|I(β)\| = n` for mapping block `β = (v, a, n)` | introduced |
| M1 | OrderPreservation: within a block, the `k`-th V-position maps to the `k`-th I-address; both orderings agree | introduced |
| M-aux | OrdinalIncrementAssociativity: `(v + c) + j = v + (c + j)` for ordinal increments | introduced |
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

## Open Questions

When two V-adjacent blocks in the canonical decomposition fail the merge condition, what is the precise structure of the I-space discontinuity at their boundary — must it be a forward gap, or can it be an arbitrary jump to an unrelated I-region?

Is the set of equivalent decompositions of a given arrangement a lattice under the refinement ordering, with the canonical decomposition as the coarsest element?

What constraints govern the relationship between the total V-extent of an arrangement and the number of blocks in its canonical decomposition?

Does width coupling (M0) entail constraints on the tumbler depth relationship between V-starts and I-starts within a single block?
