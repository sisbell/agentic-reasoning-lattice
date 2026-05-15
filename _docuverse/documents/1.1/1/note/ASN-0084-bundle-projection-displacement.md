# ASN-0084: Cut-Point Rearrangements

*2026-04-10*

This ASN layers a class of arrangement rearrangements over the Strand Model (ASN-0036). The arrangement function M(d) is mutated by transposing regions of V-positions delimited by cut points: three cuts define two adjacent regions that exchange places (the *pivot*); four cuts define two outer regions exchanging across a fixed middle (the *swap*). The induced bijection π : dom(M(d)) → dom(M(d)) has a uniform displacement structure on each region, determined by region widths alone. The correspondence-run decomposition guaranteed by S8 (ASN-0036) transforms by splitting at cuts, classifying each run into a region, and reassembling with the per-region displacement. The proofs draw directly on ASN-0036 (Strand Model — correspondence runs, contiguity, sequential positions) and ASN-0034 (Tumbler Algebra — ordinal shift, shift composition); no property from ASN-0053 (Span Algebra) is invoked.


## State and Vocabulary

We work with the content store C : T ⇀ Val (Σ.C, ASN-0036) and the arrangement function M(d) : T ⇀ T for each document d (Σ.M(d), ASN-0036). The arrangement M(d) is the mutable layer; C is immutable (S0, ASN-0036).

For a V-position v with subspace(v) = v₁ and #v = m, the *ordinal* is ord(v) = [v₂, ..., vₘ] — the tumbler obtained by stripping the subspace identifier (per OrdinalExtraction, ASN-0036).

We restrict to depth-2 V-positions (#v = 2, ordinal depth 1) throughout this ASN. The depth-2 restriction is a strict scope boundary; we make no claim about deeper depths in this ASN. At depth 2, D-SEQ (ASN-0036) gives V_S(d) = {[S, k] : 1 ≤ k ≤ N} for some N ≥ 0, and each ord(v) is a singleton tumbler [k] with k ∈ ℕ⁺.

**Identification of singleton tumblers with natural numbers.** At depth 2, we identify the singleton tumbler [k] with the natural number k throughout the displacement and width arithmetic. The identification is licensed as follows. The set of singleton tumblers {[k] : k ∈ ℕ⁺} is in bijection with ℕ⁺ by the map [k] ↔ k (a singleton tumbler is determined by its single component). Under this bijection: T1's strict ordering on tumblers (ASN-0034) restricted to singletons coincides with the standard `<` on ℕ⁺ (lexicographic order on a single component reduces to comparison of that component); OrdinalShift on a singleton tumbler, `shift([k], j) = [k + j]` for j ∈ ℕ (ASN-0034), corresponds to NAT-add: `k + j ∈ ℕ⁺`; and NAT-sub `m − n` (partial, m ≥ n) corresponds to the unique j with shift([n], j) = [m] when [n] ≤ [m]. The width of an interval |[c, c')| = ord(c') − ord(c) (computed via NAT-sub, which is total here because c < c' under T1, hence ord(c) < ord(c'), hence ord(c') ≥ ord(c)) yields a natural number. We use this identification implicitly: expressions like `ord(c₀) + j`, `ord(c₁) = ord(c₀) + w_α`, and `w_β = ord(c₂) − ord(c₁)` are read as natural-number arithmetic over the identified domain.

We recall D-CTG (VContiguity, ASN-0036): within each subspace, V-positions form a contiguous ordinal range with no gaps.

An *arrangement rearrangement* is a state transition Σ → Σ' in which dom(M'(d)) = dom(M(d)), C' = C (S0, ASN-0036), M'(d') = M(d') for all d' ≠ d, and there exists a bijection π : dom(M(d)) → dom(M'(d)) such that M'(d)(π(v)) = M(d)(v) for all v ∈ dom(M(d)).

We derive that the I-address range is invariant and that multiplicities are preserved. Since π is a bijection from dom(M(d)) to dom(M'(d)) = dom(M(d)), every u ∈ dom(M'(d)) has the form u = π(v) for exactly one v ∈ dom(M(d)). Therefore: ran(M'(d)) = {M'(d)(u) : u ∈ dom(M'(d))} = {M'(d)(π(v)) : v ∈ dom(M(d))} = {M(d)(v) : v ∈ dom(M(d))} = ran(M(d)). The second equality uses surjectivity of π; the third uses the defining property M'(d)(π(v)) = M(d)(v). The multiset of I-addresses is also preserved: since π is a bijection, for each I-address a, the preimage {v : M(d)(v) = a} is in bijection with {π(v) : M(d)(v) = a} = {u : M'(d)(u) = a}, so the multiplicity of a is identical in M(d) and M'(d).

**R-RI** — S3 (referential integrity, ASN-0036) is preserved as a consequence: ran(M'(d)) = ran(M(d)) ⊆ dom(C) = dom(C'), where the inclusion is S3 for the pre-state and the equality is C' = C.

**Invariant preservation.** The following ASN-0036 invariants depend only on `dom(M(d))` and are preserved because `dom(M'(d)) = dom(M(d))`: D-CTG, D-MIN, S8-fin, S8a, S8-depth. S2 (arrangement functionality) holds because each u ∈ dom(M'(d)) has u = π(v) for exactly one v (bijectivity), so M'(d)(u) = M(d)(v) is uniquely determined. Together with R-RI (S3) and C' = C (S0, S1, S7a, S7b, S7c — all properties constraining the content store and its domain carry over from the identity C' = C), every ASN-0036 invariant is maintained by an arrangement rearrangement.

Any bijection qualifies; a rearrangement determined by cut points is one where the regions to exchange are identified by a tuple of cut positions. The properties in this ASN characterize this specific class of permutations.

Notation: at depth 2, V-positions have the form [S, p]. We write `c₀ + j` for the V-position [S, ord(c₀) + j] — that is, ordinal shift via OrdinalShift (ASN-0034): `c₀ + j = shift(c₀, j)`, consistent with the correspondence-run convention of ASN-0036. By convention, `c₀ + 0 = c₀` (identity). Associativity `(c₀ + j) + k = c₀ + (j + k)` follows from TS3 (ShiftComposition, ASN-0034): `shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂)`.


## Cut Points and the Region Partition

A *cut sequence* specifies the boundaries of regions to transpose. We formalize this as a tuple of tumblers within a single subspace. The cut positions are tumblers satisfying CS1–CS4 below; the last cut c_{n−1} serves as an exclusive upper bound and need not belong to V_S(d).

**Definition — CutSequence.** A *cut sequence* for document d in subspace S is a tuple C = (c₀, c₁, ..., c_{n−1}) of tumblers satisfying:

(CS1) n ∈ {3, 4} — exactly three or four cuts.

(CS2) c₀ < c₁ < ... < c_{n−1} under T1 (ASN-0034) — strictly ordered.

(CS3) subspace(cᵢ) = S for all i — all cuts in the same subspace.

(CS4) #cᵢ = 2 for all i — depth-2 positions.

The cut positions partition the V-positions of the affected range into regions. For n = 3 (the *pivot*), the cuts define two adjacent regions. For n = 4 (the *swap*), the cuts define two outer regions separated by a middle region.

**Definition — RegionPartition.** Given a cut sequence C for document d in subspace S with V_S(d) ≠ ∅:

For n = 3, the *affected range* A = {v ∈ V_S(d) : c₀ ≤ v < c₂} is partitioned:

```
α = {v ∈ V_S(d) : c₀ ≤ v < c₁}     — first region
β = {v ∈ V_S(d) : c₁ ≤ v < c₂}     — second region
```

For n = 4, the *affected range* A = {v ∈ V_S(d) : c₀ ≤ v < c₃} is partitioned:

```
α = {v ∈ V_S(d) : c₀ ≤ v < c₁}     — first region
μ = {v ∈ V_S(d) : c₁ ≤ v < c₂}     — middle region
β = {v ∈ V_S(d) : c₂ ≤ v < c₃}     — second region
```

Pairwise disjointness follows from the strict ordering of cut points and the trichotomy of T1. Exhaustiveness follows from every v ∈ A falling in exactly one inter-cut interval. Each region is a set of consecutive V-positions (by D-CTG, ASN-0036, restricted to the interval between its bounding cuts).

We write w_α = |α|, w_β = |β|, w_μ = |μ| for the region widths.


## Rearrangement Postconditions

The following precondition and postcondition clauses define the rearrangement operation. They are the assumed operational context for the properties introduced in this ASN.

**R-PRE — RearrangePrecondition.**

(i) M(d) is well-defined (the document's arrangement exists).

(ii) V_S(d) ≠ ∅ (the subspace is non-empty — one cannot rearrange nothing).

(iii) The cut sequence C = (c₀, ..., c_{n−1}) satisfies CS1–CS4.

(iv) The affected range lies entirely within the current arrangement:

`(A v : subspace(v) = S ∧ #v = 2 ∧ c₀ ≤ v < c_{n−1} : v ∈ V_S(d))`

(v) Both transposed regions are non-empty: w_α ≥ 1 and w_β ≥ 1.

Clause (iv) ensures that the affected range is covered: no gap exists within [c₀, c_{n−1}). Combined with D-CTG, this says the entire inter-cut range consists of valid V-positions in V_S(d). Clause (v) excludes degenerate cases where one region is empty.

**Consequences of R-PRE.** *Subspace confinement.* All cuts lie in subspace S by CS3, and every V-position in the affected range [c₀, c_{n−1}) ∩ V_S(d) has subspace S by membership in V_S(d). The rearrangement constructions in this ASN (PivotPostcondition, SwapPostcondition) only assign new I-addresses to V-positions in V_S(d) and leave all other positions fixed (R-FRAME-P, R-FRAME-S), so no position outside subspace S is ever produced. This is a derived consequence of CS3, CS4, and S8a (positivity of ordinals, ASN-0036), not a separate verification obligation.


### 3-Cut Pivot Postcondition

Three cuts produce two adjacent regions that exchange places. The operation is: place β's content where α was, then place α's content immediately after.

**Definition — PivotPostcondition.** Given a 3-cut sequence C = (c₀, c₁, c₂) satisfying R-PRE, the *pivot* produces arrangement M'(d) defined by:

(R-EXT) For v ∈ V_S(d) with v < c₀ or v ≥ c₂:

`M'(d)(v) = M(d)(v)`

(R-P1) For 0 ≤ j < w_β:

`M'(d)(c₀ + j) = M(d)(c₁ + j)`

(R-P2) For 0 ≤ j < w_α:

`M'(d)(c₀ + w_β + j) = M(d)(c₀ + j)`

The domain is dom(M'(d)) = dom(M(d)).

(R-FRAME-P) Frame conditions:

(a) For v ∈ dom(M(d)) with subspace(v) ≠ S: M'(d)(v) = M(d)(v).

(b) For all d' ≠ d: M'(d') = M(d').

(c) C' = C (S0, ASN-0036).

In words: the first w_β positions of the affected range receive the content that was in β (clause R-P1). The next w_α positions receive the content that was in α (clause R-P2). Everything outside the affected range is unchanged (clause R-EXT). Positions in other subspaces, other documents, and the content store are all preserved.


### 4-Cut Swap Postcondition

Four cuts produce two outer regions separated by a middle region. The semantics is a direct extension of the pivot: place β's content where α was, place μ's content immediately after, place α's content last.

**Definition — SwapPostcondition.** Given a 4-cut sequence C = (c₀, c₁, c₂, c₃) satisfying R-PRE, the *swap* produces M'(d) defined by:

(R-EXT) For v ∈ V_S(d) with v < c₀ or v ≥ c₃:

`M'(d)(v) = M(d)(v)`

(R-S1) For 0 ≤ j < w_β:

`M'(d)(c₀ + j) = M(d)(c₂ + j)`

(R-S2) For 0 ≤ j < w_μ:

`M'(d)(c₀ + w_β + j) = M(d)(c₁ + j)`

(R-S3) For 0 ≤ j < w_α:

`M'(d)(c₀ + w_β + w_μ + j) = M(d)(c₀ + j)`

The domain is dom(M'(d)) = dom(M(d)).

(R-FRAME-S) Frame conditions:

(a) For v ∈ dom(M(d)) with subspace(v) ≠ S: M'(d)(v) = M(d)(v).

(b) For all d' ≠ d: M'(d') = M(d').

(c) C' = C (S0, ASN-0036).

The arrangement is: region β content starting at c₀ (clause R-S1), then middle content (clause R-S2), then region α content (clause R-S3). Everything outside [c₀, c₃) is unchanged (clause R-EXT). Positions in other subspaces, other documents, and the content store are all preserved.

We must verify that the clauses cover [c₀, c₃) without overlap. The total width is w_β + w_μ + w_α. We need this to equal |[c₀, c₃)| = w_α + w_μ + w_β. Trivially: w_β + w_μ + w_α = w_α + w_μ + w_β. The three clause ranges are [c₀, c₀ + w_β), [c₀ + w_β, c₀ + w_β + w_μ), [c₀ + w_β + w_μ, c₀ + w_β + w_μ + w_α). By commutativity of natural-number addition, the last position is c₀ + (w_β + w_μ + w_α) = c₀ + (w_α + w_μ + w_β). And c₀ + (w_α + w_μ + w_β) has ordinal ord(c₀) + w_α + w_μ + w_β = ord(c₃), so the three ranges tile [c₀, c₃) exactly.


## Postcondition Well-Definedness

**R-PIV — PivotWellDefined (LEMMA, supporting).** The pivot postcondition defines a total function on dom(M(d)) (each position is assigned exactly one I-address).

*Proof.* We must show: (a) every v ∈ dom(M(d)) falls under exactly one clause, and (b) the right-hand sides are well-defined.

For v ∈ dom(M(d)) with subspace(v) ≠ S: R-FRAME-P(a) assigns M'(d)(v) = M(d)(v), and no other clause applies (R-EXT, R-P1, R-P2 operate only on subspace S positions).

It remains to show that every v ∈ V_S(d) falls under exactly one of R-EXT, R-P1, R-P2.

For (a): the positions addressed by R-EXT are those outside [c₀, c₂). The positions addressed by R-P1 are {c₀ + j : 0 ≤ j < w_β}. At depth 2, c₀ = [S, p] and c₀ + j = [S, p + j], so these positions have ordinals p, p + 1, ..., p + w_β − 1. By D-SEQ, these are distinct positions in V_S(d) (since R-PRE(iv) guarantees all ordinals from p to p + w_α + w_β − 1 are occupied). The positions addressed by R-P2 are {c₀ + w_β + j : 0 ≤ j < w_α} = {[S, p + w_β + j] : 0 ≤ j < w_α}, with ordinals p + w_β, ..., p + w_β + w_α − 1. By associativity of ordinal addition, c₀ + (w_β + j) = (c₀ + w_β) + j, so these are well-defined.

The R-P1 ordinal range is [p, p + w_β). The R-P2 ordinal range is [p + w_β, p + w_β + w_α). Since w_β ≥ 1, these ranges are disjoint. Their union is [p, p + w_β + w_α) = [p, p + w_α + w_β). And p + w_α + w_β is the ordinal of c₂ (since |[c₀, c₂)| = w_α + w_β, and by D-SEQ the ordinals are consecutive). So the union of R-P1 and R-P2 covers exactly [c₀, c₂) ∩ V_S(d). Together with R-EXT (covering V_S(d) \ [c₀, c₂)), every position is covered exactly once.

For (b): the right-hand sides reference M(d)(c₁ + j) for j < w_β and M(d)(c₀ + j) for j < w_α. By R-PRE(iv), all positions in [c₀, c₂) are in V_S(d) ⊆ dom(M(d)). The positions c₁ + j for j < w_β have ordinals in [ord(c₁), ord(c₂)) = the ordinals of β. The positions c₀ + j for j < w_α have ordinals in [ord(c₀), ord(c₁)) = the ordinals of α. Both sets are subsets of [c₀, c₂) ∩ V_S(d) ⊆ dom(M(d)). ∎


**R-SWP — SwapWellDefined (LEMMA, supporting).** The swap postcondition defines a total function on dom(M(d)).

*Proof.* We must show: (a) every v ∈ dom(M(d)) falls under exactly one clause, and (b) the right-hand sides are well-defined.

For v ∈ dom(M(d)) with subspace(v) ≠ S: R-FRAME-S(a) assigns M'(d)(v) = M(d)(v), and no other clause applies.

It remains to show that every v ∈ V_S(d) falls under exactly one of R-EXT, R-S1, R-S2, R-S3.

For (a): let p = ord(c₀). The positions addressed by each clause have the following ordinal ranges:

- R-EXT: ordinals outside [p, p + w_α + w_μ + w_β), i.e., ord(v) < p or ord(v) ≥ p + w_α + w_μ + w_β.
- R-S1: {c₀ + j : 0 ≤ j < w_β}, ordinals [p, p + w_β).
- R-S2: {c₀ + w_β + j : 0 ≤ j < w_μ}, ordinals [p + w_β, p + w_β + w_μ). By associativity, c₀ + (w_β + j) = (c₀ + w_β) + j, so these are well-defined.
- R-S3: {c₀ + w_β + w_μ + j : 0 ≤ j < w_α}, ordinals [p + w_β + w_μ, p + w_β + w_μ + w_α). Similarly well-defined by associativity.

Pairwise disjointness: the four ordinal ranges are [p, p + w_β), [p + w_β, p + w_β + w_μ), [p + w_β + w_μ, p + w_β + w_μ + w_α), and the exterior. Since w_β ≥ 1 and w_μ ≥ 1 (CS2 forces c₁ < c₂, so w_μ ≥ 1) and w_α ≥ 1, the half-open intervals are non-empty and their left endpoints are strictly increasing: p < p + w_β < p + w_β + w_μ < p + w_β + w_μ + w_α. Hence no two intervals overlap, and none overlaps with the exterior.

Exhaustiveness: the union of R-S1, R-S2, R-S3 covers ordinals [p, p + w_β + w_μ + w_α). And p + w_β + w_μ + w_α = p + w_α + w_μ + w_β = ord(c₃) (since |[c₀, c₃)| = w_α + w_μ + w_β and ordinals are consecutive by D-SEQ). So the union of all four clauses covers V_S(d).

For (b): the right-hand sides reference M(d)(c₂ + j) for j < w_β (ordinals of β), M(d)(c₁ + j) for j < w_μ (ordinals of μ), and M(d)(c₀ + j) for j < w_α (ordinals of α). All three sets are subsets of [c₀, c₃) ∩ V_S(d) ⊆ dom(M(d)) by R-PRE(iv). ∎


## The 3-Cut Pivot Permutation

**R-PPERM — PivotPermutation (LEMMA).** The bijection π : dom(M(d)) → dom(M'(d)) satisfying M'(d)(π(v)) = M(d)(v) is:

```
         ⎧ v                   if v < c₀ or v ≥ c₂     (exterior)
π(v) =  ⎨ c₀ + w_β + j        if v = c₀ + j, 0 ≤ j < w_α  (α → end)
         ⎩ c₀ + j              if v = c₁ + j, 0 ≤ j < w_β  (β → start)
```

*Proof.* We verify M'(d)(π(v)) = M(d)(v) in each case. For v ∈ dom(M(d)) with subspace(v) ≠ S: π(v) = v, and M'(d)(v) = M(d)(v) by R-FRAME-P(a). For v ∈ V_S(d) with v < c₀ or v ≥ c₂: π(v) = v, and M'(d)(v) = M(d)(v) by R-EXT. For v = c₀ + j in α: π(v) = c₀ + w_β + j, and M'(d)(c₀ + w_β + j) = M(d)(c₀ + j) = M(d)(v) by R-P2. For v = c₁ + j in β: π(v) = c₀ + j, and M'(d)(c₀ + j) = M(d)(c₁ + j) = M(d)(v) by R-P1.

Injectivity: within each case, the mapping is injective (the exterior is the identity; the α case maps distinct j to distinct c₀ + w_β + j; the β case maps distinct j to distinct c₀ + j). Across cases: the four image sets — {v ∈ dom(M(d)) : subspace(v) ≠ S}, V_S(d) \ [c₀, c₂), {c₀ + w_β + j : 0 ≤ j < w_α}, {c₀ + j : 0 ≤ j < w_β} — are pairwise disjoint (the first is disjoint from the rest by subspace separation; the remaining three are pairwise disjoint as shown in R-PIV). Surjectivity: non-S positions map to themselves under the identity, and the three V_S(d) image sets cover V_S(d) (shown in R-PIV); together they cover dom(M(d)). ∎

The pivot postcondition preserves dom(M(d)) (R-PIV), preserves C (R-FRAME-P(c)), and admits the bijection π satisfying M'(d)(π(v)) = M(d)(v) (R-PPERM); it therefore constitutes an arrangement rearrangement, and the invariant preservation established above applies.


## The 4-Cut Swap Permutation

**R-SPERM — SwapPermutation (LEMMA).** The bijection π satisfying M'(d)(π(v)) = M(d)(v) is:

```
         ⎧ v                        if v < c₀ or v ≥ c₃               (exterior)
         ⎪ c₀ + w_β + w_μ + j       if v = c₀ + j, 0 ≤ j < w_α        (α → end)
π(v) =  ⎨ c₀ + w_β + j             if v = c₁ + j, 0 ≤ j < w_μ        (μ → middle)
         ⎩ c₀ + j                   if v = c₂ + j, 0 ≤ j < w_β        (β → start)
```

*Proof.* We verify M'(d)(π(v)) = M(d)(v) in each case.

For v ∈ dom(M(d)) with subspace(v) ≠ S: π(v) = v, and M'(d)(v) = M(d)(v) by R-FRAME-S(a).

For v ∈ V_S(d) with v < c₀ or v ≥ c₃: π(v) = v, and M'(d)(v) = M(d)(v) by R-EXT.

For v = c₀ + j in α (0 ≤ j < w_α): π(v) = c₀ + w_β + w_μ + j, and M'(d)(c₀ + w_β + w_μ + j) = M(d)(c₀ + j) = M(d)(v) by R-S3.

For v = c₁ + j in μ (0 ≤ j < w_μ): π(v) = c₀ + w_β + j, and M'(d)(c₀ + w_β + j) = M(d)(c₁ + j) = M(d)(v) by R-S2.

For v = c₂ + j in β (0 ≤ j < w_β): π(v) = c₀ + j, and M'(d)(c₀ + j) = M(d)(c₂ + j) = M(d)(v) by R-S1.

Injectivity: within each case, the mapping is injective (the exterior is the identity; the α case maps distinct j to distinct c₀ + w_β + w_μ + j; the μ case maps distinct j to distinct c₀ + w_β + j; the β case maps distinct j to distinct c₀ + j). Across cases: the five image sets — {v ∈ dom(M(d)) : subspace(v) ≠ S}, V_S(d) \ [c₀, c₃), {c₀ + w_β + w_μ + j : 0 ≤ j < w_α}, {c₀ + w_β + j : 0 ≤ j < w_μ}, {c₀ + j : 0 ≤ j < w_β} — are pairwise disjoint (the first is disjoint from the rest by subspace separation; the remaining four are pairwise disjoint as shown in R-SWP). Surjectivity: non-S positions map to themselves under the identity, and the four V_S(d) image sets cover V_S(d) (shown in R-SWP); together they cover dom(M(d)). ∎

The swap postcondition preserves dom(M(d)) (R-SWP), preserves C (R-FRAME-S(c)), and admits the bijection π satisfying M'(d)(π(v)) = M(d)(v) (R-SPERM); it therefore constitutes an arrangement rearrangement, and the invariant preservation established above applies.

We observe the structural relationship between the two forms: the 4-cut postcondition formulas (R-S1, R-S2, R-S3) reduce to the 3-cut formulas (R-P1, R-P2) when w_μ is set to zero in the expressions — R-S2 vanishes, and R-S3 becomes R-P2. However, the preconditions prevent this degenerate case from arising: CS2 requires c₁ < c₂, so w_μ ≥ 1. The two forms are distinct primitives. The 3-cut pivot transposes two *adjacent* regions; the 4-cut swap transposes two regions separated by at least one middle position.


## Displacement Analysis

The permutations R-PPERM and R-SPERM can be characterized by ordinal displacements — how far each position moves within its subspace. These displacements illuminate the structure and connect to the correspondence-run decomposition transformation.

**Definition — PermutationDisplacement.** For a position v ∈ dom(M(d)), define Δ(v) as a signed magnitude `(σ, n) ∈ {+, −, 0} × ℕ` capturing the ordinal shift induced by π. The carrier is a pair to avoid relying on a signed integer type that the foundation does not provide; NAT-sub (ASN-0034) suffices once direction is recorded by σ. The cases are:

```
Δ(v) = (0, 0)                               if π(v) = v       (no displacement)
Δ(v) = (+, ord(π(v)) − ord(v))              if ord(π(v)) > ord(v)
Δ(v) = (−, ord(v) − ord(π(v)))              if ord(π(v)) < ord(v)
```

All three cases use NAT-sub on its defined domain: the (+) case requires ord(π(v)) ≥ ord(v); the (−) case requires ord(v) ≥ ord(π(v)); the (0, 0) case sidesteps subtraction. We write `+n` for `(+, n)`, `−n` for `(−, n)`, and `0` for `(0, 0)` when no ambiguity arises, and lift the natural ordering on ℕ to the signed-magnitude carrier as `−m < 0 < +n`. We say Δ(v₁) = Δ(v₂) when their signs and magnitudes are componentwise equal. Sums `+m + (−n)` and the total-displacement zero identity are interpreted under this carrier — see the closing paragraph of this section.

On the exterior, π(v) = v, so Δ(v) = 0.

For the 3-cut pivot, from R-PPERM:

```
Δ(v) = +w_β      if v ∈ α     (shifts forward by width of β)
Δ(v) = −w_α      if v ∈ β     (shifts backward by width of α)
Δ(v) = 0         otherwise
```

For the 4-cut swap, from R-SPERM:

```
Δ(v) = +(w_β + w_μ)        if v ∈ α   (shifts forward past middle and β)
Δ(v) = sign(w_β − w_α) · |w_β − w_α|   if v ∈ μ   (depends on width comparison; see below)
Δ(v) = −(w_α + w_μ)        if v ∈ β   (shifts backward past middle and α)
Δ(v) = 0                   otherwise
```

The μ case splits on the comparison of w_β and w_α (both ∈ ℕ⁺): when w_β > w_α, Δ(v) = +(w_β − w_α); when w_β < w_α, Δ(v) = −(w_α − w_β); when w_β = w_α, Δ(v) = 0. Each branch invokes NAT-sub on its defined domain.

We observe a symmetry in the 3-cut case: the forward displacement of α equals the width of β, and vice versa. Counting positions and signed magnitudes: w_α positions shift by +w_β, w_β positions shift by −w_α. The forward total `w_α · w_β` equals the backward total `w_β · w_α`, so the signed totals cancel — a necessary consequence of π being a bijection on a contiguous range.

In the 4-cut case, the symmetry is more subtle. The forward displacement of α is w_β + w_μ, while the backward displacement of β is w_α + w_μ. These are equal only when w_α = w_β. The middle absorbs the imbalance: w_μ middle positions shift by `|w_β − w_α|` in the direction of the wider region. Counting signed totals: forward total = w_α · (w_β + w_μ) + (μ-forward when w_β > w_α: w_μ · (w_β − w_α), else 0); backward total = w_β · (w_α + w_μ) + (μ-backward when w_β < w_α: w_μ · (w_α − w_β), else 0). In the case w_β > w_α, forward = w_α w_β + w_α w_μ + w_μ w_β − w_μ w_α = w_α w_β + w_μ w_β = w_β (w_α + w_μ) = backward. By symmetry of the case split, the totals match in the case w_β < w_α as well. When w_β = w_α, the μ displacement is 0 and the totals are w_α(w_β + w_μ) = w_α · w_β + w_α · w_μ on each side. In every case, forward and backward totals are equal.

The displacement formulation makes it clear that every position in the affected range shifts by a value determined solely by the region widths — the displacement does not depend on the position's location within its region. All positions in α shift by the same amount; all positions in β shift by the same amount. We state this formally:

**R-DISP — DisplacementUniformity (LEMMA).** Let C be a cut sequence satisfying R-PRE, and let π be the permutation from R-PPERM (3-cut) or R-SPERM (4-cut). For all v₁, v₂ in the same region (exterior, α, μ, or β):

`Δ(v₁) = Δ(v₂)`

with the common value given by: for 3-cut, Δ = +w_β on α, Δ = −w_α on β, Δ = 0 on exterior; for 4-cut, Δ = +(w_β + w_μ) on α, Δ on μ depends on the comparison of w_β and w_α (the three sub-cases above), Δ = −(w_α + w_μ) on β, Δ = 0 on exterior.

*Proof.* The result follows from the explicit R-PPERM and R-SPERM formulas, in which the offset j within a region cancels. We show each region; each case identifies the sign of ord(π(v)) − ord(v) before applying NAT-sub on its defined domain.

*Exterior (both forms):* π(v) = v, so ord(π(v)) = ord(v), and Δ(v) = 0 by the (0, 0) branch.

*3-cut α:* For v = c₀ + j with 0 ≤ j < w_α: π(v) = c₀ + w_β + j, so ord(π(v)) = ord(c₀) + w_β + j and ord(v) = ord(c₀) + j. Since w_β ≥ 1, ord(π(v)) > ord(v); the (+) branch applies, giving Δ(v) = +((ord(c₀) + w_β + j) − (ord(c₀) + j)) = +w_β.

*3-cut β:* For v = c₁ + j with 0 ≤ j < w_β: π(v) = c₀ + j, so ord(π(v)) = ord(c₀) + j and ord(v) = ord(c₁) + j = ord(c₀) + w_α + j. Since w_α ≥ 1, ord(v) > ord(π(v)); the (−) branch applies, giving Δ(v) = −((ord(c₀) + w_α + j) − (ord(c₀) + j)) = −w_α.

*4-cut α:* For v = c₀ + j with 0 ≤ j < w_α: π(v) = c₀ + w_β + w_μ + j, so ord(π(v)) = ord(c₀) + w_β + w_μ + j and ord(v) = ord(c₀) + j. Since w_β + w_μ ≥ 2, ord(π(v)) > ord(v); the (+) branch applies, giving Δ(v) = +(w_β + w_μ).

*4-cut μ:* For v = c₁ + j with 0 ≤ j < w_μ: π(v) = c₀ + w_β + j, so ord(π(v)) = ord(c₀) + w_β + j and ord(v) = ord(c₁) + j = ord(c₀) + w_α + j. The comparison of ord(π(v)) and ord(v) reduces to the comparison of w_β and w_α. When w_β > w_α: (+) branch, Δ(v) = +(w_β − w_α). When w_β < w_α: (−) branch, Δ(v) = −(w_α − w_β). When w_β = w_α: ord(π(v)) = ord(v), Δ(v) = 0. In all three sub-cases, j cancels.

*4-cut β:* For v = c₂ + j with 0 ≤ j < w_β: π(v) = c₀ + j, so ord(π(v)) = ord(c₀) + j and ord(v) = ord(c₂) + j = ord(c₀) + w_α + w_μ + j. Since w_α + w_μ ≥ 2, ord(v) > ord(π(v)); the (−) branch applies, giving Δ(v) = −(w_α + w_μ).

In every case, j cancels and the common value depends only on region widths. ∎


## Correspondence-Run Decomposition Transformation

We recall from S8 (SpanDecomposition, ASN-0036) that for every v ∈ dom(M(d)) there exists a unique correspondence run (v_s, a_s, n) with v ∈ {v_s + k : 0 ≤ k < n} and M(d)(v_s + k) = a_s + k for all 0 ≤ k < n. Equivalently, S8 yields a finite partition of dom(M(d)) into correspondence runs. We layer three new operations (Split, Merge, and a canonical decomposition) over the foundation's runs. Throughout this section, when we say *run* we mean a correspondence run (v, a, n) with n ≥ 1, and write V(v, a, n) = {v + k : 0 ≤ k < n} for its V-extent; the labels S8(a) and S8(b) refer respectively to the uniqueness-of-containing-run clause and the consistency clause M(d)(v + k) = a + k that the foundation already exports.

**Split.** Given a run b = (v, a, n) under some arrangement A and an interior offset c with 1 ≤ c < n, the *split* at c produces two runs: (v, a, c) and (v + c, a + c, n − c). Their V-extents (ordinal ranges [ord(v), ord(v) + c) and [ord(v) + c, ord(v) + n)) are disjoint and partition b's V-extent.

Both pieces inherit S8(b) (consistency under A). For the first piece (v, a, c), we need A(v + k) = a + k for 0 ≤ k < c; this holds by restricting the original S8(b) to the subrange k < c < n. For the second piece (v + c, a + c, n − c), we need A((v + c) + k) = (a + c) + k for 0 ≤ k < n − c. When k ≥ 1, associativity (TS3) gives (v + c) + k = v + (c + k); when k = 0, (v + c) + 0 = v + c by the identity convention. In both cases, c + k < n, so the original S8(b) yields A(v + (c + k)) = a + (c + k). The same associativity/identity argument gives (a + c) + k = a + (c + k), completing the derivation: A((v + c) + k) = a + (c + k) = (a + c) + k. The proof is arrangement-parametric: it uses only S8(b) of the original run and TS3, with no property specific to a particular arrangement.

**Merge.** Two runs (v₁, a₁, n₁) and (v₂, a₂, n₂) under arrangement A are *mergeable* when v₂ = v₁ + n₁ (V-adjacent) and a₂ = a₁ + n₁ (I-adjacent). The merged run is (v₁, a₁, n₁ + n₂). We verify S8(b) for the merged run — that A(v₁ + k) = a₁ + k for 0 ≤ k < n₁ + n₂ — by two cases. For 0 ≤ k < n₁: this is S8(b) of the first run directly. For n₁ ≤ k < n₁ + n₂: write k = n₁ + k' with 0 ≤ k' < n₂. When k' ≥ 1, TS3 gives v₁ + k = v₁ + (n₁ + k') = (v₁ + n₁) + k' = v₂ + k'; when k' = 0, v₁ + n₁ = v₂ by the adjacency condition. By S8(b) of the second run, A(v₂ + k') = a₂ + k'. The same associativity/identity argument gives a₁ + k = a₁ + (n₁ + k') = (a₁ + n₁) + k' = a₂ + k', so A(v₁ + k) = a₂ + k' = a₁ + k. As with Split, this proof is arrangement-parametric: it depends only on S8(b) of the two constituents and TS3. In particular, when R-BLK applies Merge to the post-rearrangement arrangement M'(d), the verification holds because the reassembled runs already satisfy S8(b) for M'(d) (established in Phase 3).

**Canonical decomposition.** The *canonical run decomposition* of M(d) is the unique partition of dom(M(d)) into *maximal* runs — runs that cannot be extended by merging with a V-adjacent, I-adjacent neighbor. Although S8 already guarantees existence and uniqueness of the containing run for each position, we re-derive the global uniqueness here in terms of maximality, which is the form used by R-BLK. We establish uniqueness through four steps.

*(a) The maximal run containing any v ∈ dom(M(d)) is uniquely determined.* Fix v. Define the *forward extent* f(v) = max{k ≥ 0 : (A j : 0 ≤ j ≤ k : v + j ∈ dom(M(d)) ∧ M(d)(v + j) = M(d)(v) + j)}. This maximum exists because dom(M(d)) is finite (S8-fin). Define the *backward extent* r(v) = max{k ≥ 0 : [S, ord(v) − k] ∈ V_S(d) ∧ (A i : 0 ≤ i ≤ k : M(d)([S, ord(v) − k + i]) = shift(M(d)([S, ord(v) − k]), i))}, where the identity convention covers i = 0 and OrdinalShift applies for i ≥ 1. The membership requirement [S, ord(v) − k] ∈ V_S(d) demands ord(v) − k ≥ 1 (since V-positions have positive ordinals by S8a) and is checked at the tentative start; for each intermediate offset i with 0 ≤ i ≤ k, the position [S, ord(v) − k + i] lies in V_S(d) automatically. To see this, note v ∈ V_S(d) gives ord(v) ∈ {1, ..., N} where V_S(d) = {[S, j] : 1 ≤ j ≤ N} by D-SEQ (ASN-0036), and [S, ord(v) − k] ∈ V_S(d) gives ord(v) − k ≥ 1; the intermediate ordinals ord(v) − k + i lie in [ord(v) − k, ord(v)] ⊆ [1, N], so [S, ord(v) − k + i] ∈ V_S(d). The inner consistency conjunct in r(v) is therefore well-formed at every offset. This formulation checks S8(b) forward from the tentative run start [S, ord(v) − k], avoiding subtraction on I-addresses. Both f(v) and r(v) are determined by M(d) and v alone — M(d) is a function (S2), so for each candidate position the correspondence either holds or does not, with no ambiguity. Writing v_s = [S, ord(v) − r(v)] for the start position, the maximal run containing v is (v_s, M(d)(v_s), r(v) + 1 + f(v)), and it is uniquely determined by the values of r(v) and f(v).

*(b) Two maximal runs sharing a V-position are identical.* Let b₁ = (v₁, a₁, n₁) and b₂ = (v₂, a₂, n₂) be maximal runs with some w ∈ V(b₁) ∩ V(b₂). Since w ∈ V(b₁), we have w = v₁ + k₁ and M(d)(w) = a₁ + k₁ for some 0 ≤ k₁ < n₁; similarly w = v₂ + k₂ and M(d)(w) = a₂ + k₂. We show b₁ = b₂ by establishing v₁ = v₂, a₁ = a₂, and n₁ = n₂ — each by contradiction with maximality, using only forward-defined operations.

*v₁ = v₂:* Suppose v₂ < v₁ (the case v₁ < v₂ is symmetric). Then k₂ ≥ 1 (since ord(v₂) < ord(v₁) ≤ ord(w) = ord(v₂) + k₂). Let p = ord(v₁) − ord(v₂) ≥ 1. The position [S, ord(v₁) − 1] lies in V(b₂): ord(v₂) ≤ ord(v₁) − 1 < ord(v₂) + n₂. By S8(b) of b₂ at offsets p − 1 and p: M(d)([S, ord(v₁) − 1]) = a₂ + (p − 1) and M(d)(v₁) = a₂ + p = a₁. Now shift(a₂ + (p − 1), 1) = a₂ + p by TS3 (when p ≥ 2) or the identity convention (when p = 1), so shift(M(d)([S, ord(v₁) − 1]), 1) = a₁ = M(d)(v₁). This shows b₁ can be extended backward while maintaining S8(b), contradicting maximality. Therefore v₁ = v₂.

*a₁ = a₂:* With v₁ = v₂, w = v₁ + k₁ = v₁ + k₂ gives k₁ = k₂ (by TS5: if k₁ ≠ k₂ with both ≥ 1, then shift(v₁, k₁) ≠ shift(v₁, k₂), contradicting equality; when one is 0, TS4 forces the other to be 0). Hence a₁ + k₁ = M(d)(w) = a₂ + k₁. When k₁ = 0: a₁ = a₂ directly. When k₁ ≥ 1: shift(a₁, k₁) = shift(a₂, k₁) with #a₁ = #a₂ (from equal result lengths), so TS2 gives a₁ = a₂.

*n₁ = n₂:* Suppose n₂ > n₁. Then v₁ + n₁ ∈ V(b₂) (since n₁ < n₂ and v₁ = v₂), and S8(b) of b₂ gives M(d)(v₁ + n₁) = a₂ + n₁ = a₁ + n₁. This extends b₁ forward at offset n₁, contradicting maximality. By symmetry, n₁ > n₂ is excluded. Therefore n₁ = n₂, and b₁ = b₂.

*(c) Merge-order independence.* Start from any partition of dom(M(d)) into runs (existence guaranteed by S8). The exhaustive merge process repeatedly finds a mergeable pair and merges them, reducing the run count by one. Termination: dom(M(d)) is finite (S8-fin), so the initial run count is finite, and each merge strictly reduces it, so the process terminates. At termination, no mergeable pair remains — every run is maximal, since a non-maximal run would have a V-adjacent, I-adjacent neighbor forming a mergeable pair. By (b), the partition into maximal runs is unique, so every termination state is the same partition regardless of merge order.

*(d) Maximal runs admit no merge.* Two maximal runs cannot be simultaneously V-adjacent and I-adjacent: if b₁ = (v₁, a₁, n₁) and b₂ = (v₂, a₂, n₂) satisfy v₂ = v₁ + n₁ and a₂ = a₁ + n₁, then (v₁, a₁, n₁ + n₂) is a valid run (by Merge) whose V-extent strictly contains V(b₁), contradicting b₁'s maximality. This is precisely the condition checked in (c) — at termination, no such pair exists, confirming that the exhaustive merge reaches the maximal-run partition.

**R-COMM — PermutationShiftCommutativity (LEMMA).** Let π be a cut-point permutation (R-PPERM or R-SPERM) for a cut sequence C satisfying R-PRE. For any V-position v and offset k ≥ 0 such that v and v + k lie in the same region (exterior, α, μ, or β):

`π(v + k) = π(v) + k`

In words: the cut-point permutation commutes with ordinal shift within each region. Every position in a region receives the same ordinal displacement, so shifting within the region before or after applying π yields the same result.

*Proof.* We verify each region case using the explicit R-PPERM and R-SPERM formulas, with associativity of natural-number addition at the ordinal level as the sole algebraic tool.

*Exterior (both forms):* π(v + k) = v + k = π(v) + k, since π is the identity on the exterior.

*3-cut α:* v = c₀ + j' for some 0 ≤ j' < w_α. Then v + k = c₀ + (j' + k), and by R-PPERM: π(v + k) = c₀ + w_β + (j' + k). Also π(v) + k = (c₀ + w_β + j') + k = c₀ + w_β + (j' + k) by associativity.

*3-cut β:* v = c₁ + j' for some 0 ≤ j' < w_β. Then v + k = c₁ + (j' + k), and by R-PPERM: π(v + k) = c₀ + (j' + k). Also π(v) + k = (c₀ + j') + k = c₀ + (j' + k) by associativity.

*4-cut α:* v = c₀ + j' for some 0 ≤ j' < w_α. Then v + k = c₀ + (j' + k), and by R-SPERM: π(v + k) = c₀ + w_β + w_μ + (j' + k). Also π(v) + k = (c₀ + w_β + w_μ + j') + k = c₀ + w_β + w_μ + (j' + k) by associativity.

*4-cut μ:* v = c₁ + j' for some 0 ≤ j' < w_μ. Then v + k = c₁ + (j' + k), and by R-SPERM: π(v + k) = c₀ + w_β + (j' + k). Also π(v) + k = (c₀ + w_β + j') + k = c₀ + w_β + (j' + k) by associativity.

*4-cut β:* v = c₂ + j' for some 0 ≤ j' < w_β. Then v + k = c₂ + (j' + k), and by R-SPERM: π(v + k) = c₀ + (j' + k). Also π(v) + k = (c₀ + j') + k = c₀ + (j' + k) by associativity. ∎

**R-BLK — RunDecompositionTransformation (LEMMA).** Let B = {b₁, ..., bₘ} be a run partition of M(d) (per S8). Let the cut sequence C have cut positions c₀, ..., c_{n−1}. The rearranged arrangement M'(d) admits a run partition B' obtained by:

*Phase 1: Split.* Process cut positions in index order (c₀, c₁, ..., c_{n−1}), maintaining the partition as it is progressively refined. For each cut position cᵢ, classify by whether cᵢ falls within some run's V-extent:

- *Interior of a run:* if cᵢ ∈ V(bₖ) for some bₖ = (vₖ, aₖ, nₖ) with cᵢ ≠ vₖ, split bₖ at the offset c = ord(cᵢ) − ord(vₖ), producing (vₖ, aₖ, c) and (vₖ + c, aₖ + c, nₖ − c). The two new runs partition the V-extent of the original.
- *Boundary of a run:* if cᵢ ∈ V(bₖ) and cᵢ = vₖ, no split is needed — the cut already coincides with a run boundary.
- *Outside ⋃_k V(bₖ):* no split is performed. This occurs only for the last cut c_{n−1} when c_{n−1} > max(V_S(d)) (CS2 forces c₀ < ... < c_{n−1}, and R-PRE(iv) guarantees every position in [c₀, c_{n−1}) ∩ V_S(d) lies in some run, so only c_{n−1}, which serves as an exclusive upper bound, may exceed every V-position in V_S(d)). In this case, c_{n−1} ∉ dom(M(d)), so the right-exterior region {v ∈ V_S(d) : v ≥ c_{n−1}} is empty, and no run can possibly straddle c_{n−1}.

When a later cut falls in a run already split by an earlier (strictly smaller) cut, it necessarily falls in the right-hand piece — CS2's strict ordering guarantees this. The process is well-defined because S8(a)/(b) are maintained after each split (uniqueness of containing run carries over from the partition property, consistency by the Split lemma). After all cuts are processed, no run straddles any cut position in [c₀, c_{n−1}].

*Phase 2: Classify.* Each run in the post-split partition lies entirely within one region (exterior left, α, μ if 4-cut, β, or exterior right), because no run crosses a cut boundary. When c_{n−1} > max(V_S(d)), the exterior-right region is empty and no run is classified there; the classification by Phase 1 of the remaining cuts covers all runs.

*Phase 3: Reassemble.* Apply the permutation to each run's V-start:

- Exterior runs: unchanged.
- α runs: (vₖ, aₖ, nₖ) becomes (π(vₖ), aₖ, nₖ) — the V-start shifts by the α displacement, the I-start and width are preserved.
- β runs: V-start shifts by the β displacement.
- μ runs (4-cut only): V-start shifts by the μ displacement (which is +(w_β − w_α), −(w_α − w_β), or 0 per the three sub-cases of Δ on μ; in all sub-cases the displacement is uniform across the region).

The I-start and width of each run are preserved because the rearrangement modifies no I-addresses and the displacement is uniform within each region (R-DISP).

*Contiguity of reassembled runs.* Within each region, π applies a uniform ordinal displacement. After Phase 1, every run lies entirely in a single region, so for each run (vⱼ, aⱼ, nⱼ) and 0 ≤ k < nⱼ, positions vⱼ and vⱼ + k are in the same region and receive the same displacement. By R-COMM (π(vⱼ + k) = π(vⱼ) + k), consecutive V-positions in the original run map to consecutive V-positions, so each reassembled run (π(vⱼ), aⱼ, nⱼ) occupies a contiguous V-position range and is therefore a valid run.

The resulting runs satisfy S8(b) (consistency under M'(d)): for each reassembled run (π(vⱼ), aⱼ, nⱼ) and 0 ≤ k < nⱼ: M'(d)(π(vⱼ) + k) = M'(d)(π(vⱼ + k)) = M(d)(vⱼ + k) = aⱼ + k. The second equality uses the permutation definition M'(d)(π(v)) = M(d)(v); the first uses R-COMM.

Uniqueness of the containing run (S8(a)) for M'(d): π is a bijection on dom(M(d)) = dom(M'(d)), so the V-extents of the reassembled runs are pairwise disjoint (from the disjointness of the pre-reassembly partition and injectivity of π) and cover dom(M'(d)) (from coverage and surjectivity of π); together these yield the E! quantification of S8(a).

The partition B' is valid but not necessarily maximal. After rearrangement, runs that were in different regions may become V-adjacent and I-adjacent, satisfying the merge condition. The canonical (maximal) run partition of M'(d) may therefore have fewer runs than B'.


## Worked Example: 3-Cut Pivot on a 5-Position Document

We trace a concrete 3-cut pivot to verify the postconditions against explicit values. Let document d have subspace S = 1 with V_S(d) = {[1,1], [1,2], [1,3], [1,4], [1,5]}, and let the arrangement be:

```
M(d)([1,1]) = 3.0.1.0.1.0.1.1    (I-address A)
M(d)([1,2]) = 3.0.1.0.1.0.1.2    (I-address B)
M(d)([1,3]) = 3.0.1.0.1.0.1.3    (I-address C)
M(d)([1,4]) = 5.0.2.0.1.0.1.1    (I-address D)
M(d)([1,5]) = 5.0.2.0.1.0.1.2    (I-address E)
```

Content A–C originates from document 3.0.1.0.1 (origin 3.0.1.0.1); D–E from document 5.0.2.0.1 (origin 5.0.2.0.1). The canonical run partition has two runs: b₁ = ([1,1], 3.0.1.0.1.0.1.1, 3) and b₂ = ([1,4], 5.0.2.0.1.0.1.1, 2).

We apply a 3-cut pivot with C = ([1,2], [1,4], [1,5]): c₀ = [1,2], c₁ = [1,4], c₂ = [1,5]. The affected range is [c₀, c₂) = {[1,2], [1,3], [1,4]}. Region α = {[1,2], [1,3]} (w_α = 2), region β = {[1,4]} (w_β = 1).

**R-PRE verification.** (i) M(d) well-defined. (ii) V_S(d) ≠ ∅. (iii) CS1: n = 3; CS2: [1,2] < [1,4] < [1,5]; CS3: all subspace 1; CS4: all depth 2. (iv) All positions in [[1,2], [1,5)) are in V_S(d). (v) w_α = 2 ≥ 1, w_β = 1 ≥ 1. ✓

**Applying the postconditions.** We compute M'(d) position by position:

R-EXT: M'(d)([1,1]) = M(d)([1,1]) = A. M'(d)([1,5]) = M(d)([1,5]) = E.

R-P1 (j = 0): M'(d)(c₀ + 0) = M'(d)([1,2]) = M(d)(c₁ + 0) = M(d)([1,4]) = D.

R-P2 (j = 0): M'(d)(c₀ + 1 + 0) = M'(d)([1,3]) = M(d)(c₀ + 0) = M(d)([1,2]) = B.

R-P2 (j = 1): M'(d)(c₀ + 1 + 1) = M'(d)([1,4]) = M(d)(c₀ + 1) = M(d)([1,3]) = C.

**Result:**

```
M'(d)([1,1]) = A     (exterior, unchanged)
M'(d)([1,2]) = D     (was β, now at start of affected range)
M'(d)([1,3]) = B     (was α position 1, shifted forward by w_β = 1)
M'(d)([1,4]) = C     (was α position 2, shifted forward by w_β = 1)
M'(d)([1,5]) = E     (exterior, unchanged)
```

**R-PPERM verification.** The permutation π: π([1,1]) = [1,1] (exterior), π([1,2]) = [1,3] (α: c₀ + 0 → c₀ + w_β + 0 = [1,3]), π([1,3]) = [1,4] (α: c₀ + 1 → c₀ + w_β + 1 = [1,4]), π([1,4]) = [1,2] (β: c₁ + 0 → c₀ + 0 = [1,2]), π([1,5]) = [1,5] (exterior). We check: M'(d)(π([1,2])) = M'(d)([1,3]) = B = M(d)([1,2]) ✓. M'(d)(π([1,4])) = M'(d)([1,2]) = D = M(d)([1,4]) ✓.

**Run partition after rearrangement.** The new canonical partition has four runs: ([1,1], A, 1), ([1,2], D, 1), ([1,3], B, 2), ([1,5], E, 1). Run ([1,3], B, 2) is valid because B = 3.0.1.0.1.0.1.2 and C = 3.0.1.0.1.0.1.3 = B + 1. Run ([1,5], E, 1) is exterior, unchanged by R-EXT. D = 5.0.2.0.1.0.1.1 cannot merge with A = 3.0.1.0.1.0.1.1 (different origins — origin(D) = 5.0.2.0.1 ≠ 3.0.1.0.1 = origin(A), so I-adjacency fails) nor with B = 3.0.1.0.1.0.1.2 (not I-adjacent: D + 1 ≠ B). Run ([1,3], B, 2) cannot merge with ([1,5], E, 1): C + 1 = 3.0.1.0.1.0.1.4 ≠ E = 5.0.2.0.1.0.1.2 (different origins). The cut at [1,2] (c₀, interior to b₁ at offset 1) split the original run b₁ into ([1,1], A, 1) and ([1,2], B, 2), and the rearrangement inserted the single-element run for D between them.


## Worked Example: 4-Cut Swap on an 8-Position Document

We trace a 4-cut swap with unequal region widths. Let document d have subspace S = 1 with V_S(d) = {[1,1], ..., [1,8]}, and let the arrangement be:

```
M(d)([1,1]) = 3.0.1.0.1.0.1.1    (I-address A)
M(d)([1,2]) = 3.0.1.0.1.0.1.2    (I-address B)
M(d)([1,3]) = 3.0.1.0.1.0.1.3    (I-address C)
M(d)([1,4]) = 7.0.1.0.1.0.1.1    (I-address D)
M(d)([1,5]) = 5.0.2.0.1.0.1.1    (I-address E)
M(d)([1,6]) = 5.0.2.0.1.0.1.2    (I-address F)
M(d)([1,7]) = 5.0.2.0.1.0.1.3    (I-address G)
M(d)([1,8]) = 3.0.1.0.1.0.1.4    (I-address H)
```

Content A–C originates from document 3.0.1.0.1; D from document 7.0.1.0.1; E–G from document 5.0.2.0.1; H from document 3.0.1.0.1. The canonical run partition has four runs: b₁ = ([1,1], A, 3), b₂ = ([1,4], D, 1), b₃ = ([1,5], E, 3), b₄ = ([1,8], H, 1).

We apply a 4-cut swap with C = ([1,2], [1,4], [1,5], [1,8]): c₀ = [1,2], c₁ = [1,4], c₂ = [1,5], c₃ = [1,8]. The affected range is [c₀, c₃) = {[1,2], ..., [1,7]}. Region α = {[1,2], [1,3]} (w_α = 2), middle μ = {[1,4]} (w_μ = 1), region β = {[1,5], [1,6], [1,7]} (w_β = 3). Since w_α = 2 ≠ w_β = 3, the middle displacement w_β − w_α = 1 is nonzero.

**R-PRE verification.** (i) M(d) well-defined. (ii) V_S(d) ≠ ∅. (iii) CS1: n = 4; CS2: [1,2] < [1,4] < [1,5] < [1,8]; CS3: all subspace 1; CS4: all depth 2. (iv) All positions in [[1,2], [1,8)) are in V_S(d). (v) w_α = 2 ≥ 1, w_β = 3 ≥ 1. ✓

**Applying the postconditions.** We compute M'(d) position by position:

R-EXT: M'(d)([1,1]) = M(d)([1,1]) = A. M'(d)([1,8]) = M(d)([1,8]) = H.

R-S1 (j = 0): M'(d)(c₀ + 0) = M'(d)([1,2]) = M(d)(c₂ + 0) = M(d)([1,5]) = E.

R-S1 (j = 1): M'(d)(c₀ + 1) = M'(d)([1,3]) = M(d)(c₂ + 1) = M(d)([1,6]) = F.

R-S1 (j = 2): M'(d)(c₀ + 2) = M'(d)([1,4]) = M(d)(c₂ + 2) = M(d)([1,7]) = G.

R-S2 (j = 0): M'(d)(c₀ + 3 + 0) = M'(d)([1,5]) = M(d)(c₁ + 0) = M(d)([1,4]) = D.

R-S3 (j = 0): M'(d)(c₀ + 3 + 1 + 0) = M'(d)([1,6]) = M(d)(c₀ + 0) = M(d)([1,2]) = B.

R-S3 (j = 1): M'(d)(c₀ + 3 + 1 + 1) = M'(d)([1,7]) = M(d)(c₀ + 1) = M(d)([1,3]) = C.

**Result:**

```
M'(d)([1,1]) = A     (exterior, unchanged)
M'(d)([1,2]) = E     (from β via R-S1)
M'(d)([1,3]) = F     (from β via R-S1)
M'(d)([1,4]) = G     (from β via R-S1)
M'(d)([1,5]) = D     (from μ via R-S2)
M'(d)([1,6]) = B     (from α via R-S3)
M'(d)([1,7]) = C     (from α via R-S3)
M'(d)([1,8]) = H     (exterior, unchanged)
```

The three swap clauses tile [c₀, c₃) = [[1,2], [1,8]) exactly: R-S1 covers ordinals 2–4 (w_β = 3 positions), R-S2 covers ordinal 5 (w_μ = 1 position), R-S3 covers ordinals 6–7 (w_α = 2 positions). Total: 3 + 1 + 2 = 6 = |[c₀, c₃)|. ✓

**R-SPERM verification.** The permutation π:

- π([1,1]) = [1,1] (exterior).
- π([1,2]) = c₀ + w_β + w_μ + 0 = [1,6] (α: j = 0). Check: M'(d)([1,6]) = B = M(d)([1,2]) ✓.
- π([1,3]) = c₀ + w_β + w_μ + 1 = [1,7] (α: j = 1). Check: M'(d)([1,7]) = C = M(d)([1,3]) ✓.
- π([1,4]) = c₀ + w_β + 0 = [1,5] (μ: j = 0). Check: M'(d)([1,5]) = D = M(d)([1,4]) ✓.
- π([1,5]) = c₀ + 0 = [1,2] (β: j = 0). Check: M'(d)([1,2]) = E = M(d)([1,5]) ✓.
- π([1,6]) = c₀ + 1 = [1,3] (β: j = 1). Check: M'(d)([1,3]) = F = M(d)([1,6]) ✓.
- π([1,7]) = c₀ + 2 = [1,4] (β: j = 2). Check: M'(d)([1,4]) = G = M(d)([1,7]) ✓.
- π([1,8]) = [1,8] (exterior).

**Displacement verification.** Reading Δ as a signed magnitude: Δ([1,2]) = +(6 − 2) = +4 = +(w_β + w_μ) ✓. Δ([1,3]) = +(7 − 3) = +4 ✓. Δ([1,4]) = +(5 − 4) = +1 = +(w_β − w_α), the μ-branch with w_β > w_α ✓. Δ([1,5]) = −(5 − 2) = −3 = −(w_α + w_μ) ✓. Δ([1,6]) = −(6 − 3) = −3 ✓. Δ([1,7]) = −(7 − 4) = −3 ✓. The middle-region displacement is +1, confirming the asymmetric structure when w_α ≠ w_β.

**Run decomposition via R-BLK.** *Phase 1 (Split):* c₀ = [1,2] is interior to b₁ = ([1,1], A, 3) at offset 1. Split: ([1,1], A, 1) and ([1,2], B, 2). The remaining cuts c₁ = [1,4], c₂ = [1,5], c₃ = [1,8] coincide with run boundaries (c₁ = b₂'s start, c₂ = b₃'s start, c₃ = b₄'s start), so no further splits. Post-split partition: {([1,1], A, 1), ([1,2], B, 2), ([1,4], D, 1), ([1,5], E, 3), ([1,8], H, 1)}.

*Phase 2 (Classify):* ([1,1], A, 1) → exterior left. ([1,2], B, 2) → α. ([1,4], D, 1) → μ. ([1,5], E, 3) → β. ([1,8], H, 1) → exterior right.

*Phase 3 (Reassemble):* Apply region displacements:

- ([1,1], A, 1) → ([1,1], A, 1) (exterior, Δ = 0)
- ([1,2], B, 2) → ([1,6], B, 2) (α, Δ = +4)
- ([1,4], D, 1) → ([1,5], D, 1) (μ, Δ = +1)
- ([1,5], E, 3) → ([1,2], E, 3) (β, Δ = −3)
- ([1,8], H, 1) → ([1,8], H, 1) (exterior, Δ = 0)

Sorted by V-start: {([1,1], A, 1), ([1,2], E, 3), ([1,5], D, 1), ([1,6], B, 2), ([1,8], H, 1)}. Checking S8(b): for run ([1,2], E, 3), M'(d)([1,2]) = E, M'(d)([1,3]) = F = E + 1, M'(d)([1,4]) = G = E + 2 ✓.

*Merge check:* ([1,6], B, 2) and ([1,8], H, 1) are V-adjacent (6 + 2 = 8) and I-adjacent (B + 2 = 3.0.1.0.1.0.1.4 = H). Merge: ([1,6], B, 3). No other pair satisfies both conditions — ([1,1], A, 1) and ([1,2], E, 3) differ in origin; ([1,2], E, 3) and ([1,5], D, 1) differ in origin; ([1,5], D, 1) and ([1,6], B, 2) differ in origin.

**Canonical partition:** {([1,1], A, 1), ([1,2], E, 3), ([1,5], D, 1), ([1,6], B, 3)}. The rearrangement brought B, C (formerly at [1,2]–[1,3]) adjacent to H (at [1,8]), and since B + 2 = H, they merge into a single run of width 3. Meanwhile A, formerly part of a width-3 run with B and C, is now isolated.


## Properties Introduced

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| CutSequence | DEF | Tuple (c₀, ..., c_{n−1}) with n ∈ {3,4}, strictly ordered, same subspace, depth 2 (CS1–CS4) | introduced |
| RegionPartition | DEF | Partition of affected range into regions α, β (3-cut) or α, μ, β (4-cut) by cut positions | introduced |
| R-PRE | DEF | Precondition: M(d) exists, V_S(d) non-empty, cuts satisfy CS1–CS4, affected range covered, regions non-empty | introduced |
| PivotPostcondition | DEF | 3-cut rearrangement: β content placed at c₀, then α content, exterior unchanged (R-EXT, R-P1, R-P2) | introduced |
| SwapPostcondition | DEF | 4-cut rearrangement: β at c₀, then μ, then α, exterior unchanged (R-EXT, R-S1, R-S2, R-S3) | introduced |
| ArrangementRearrangement | DEF | State transition with dom(M'(d)) = dom(M(d)), C' = C, M'(d') = M(d') for d' ≠ d, and bijection π with M'(d)(π(v)) = M(d)(v) | introduced |
| PermutationDisplacement | DEF | Signed magnitude Δ(v) ∈ {+, −, 0} × ℕ recording the ordinal shift from v to π(v); each branch uses NAT-sub on its defined domain | introduced |
| R-DISP | LEMMA | For all v₁, v₂ in the same region, Δ(v₁) = Δ(v₂); common value determined by region widths alone | introduced |
| Split | DEF | Correspondence run (v, a, n) at interior offset c yields (v, a, c) and (v + c, a + c, n − c) | introduced |
| Merge | DEF | V-adjacent and I-adjacent correspondence runs (v₁, a₁, n₁), (v₂, a₂, n₂) combine to (v₁, a₁, n₁ + n₂) | introduced |
| CanonicalRunDecomposition | DEF | Unique partition of dom(M(d)) into maximal correspondence runs — no two V-adjacent, I-adjacent runs remain unmerged | introduced |
| R-PIV | LEMMA | Pivot postcondition is a total function on dom(M(d)) | supporting |
| R-SWP | LEMMA | Swap postcondition is a total function on dom(M(d)) | supporting |
| R-PPERM | LEMMA | Bijection π for 3-cut pivot: α shifts forward by w_β, β shifts backward by w_α | introduced |
| R-SPERM | LEMMA | Bijection π for 4-cut swap: α shifts forward by w_β + w_μ, μ shifts by w_β − w_α, β shifts backward by w_α + w_μ | introduced |
| R-FRAME-P | FRAME | Pivot: other subspaces, other documents, and content store are preserved | introduced |
| R-FRAME-S | FRAME | Swap: other subspaces, other documents, and content store are preserved | introduced |
| R-RI | LEMMA | Rearrangement preserves S3 (referential integrity): ran(M'(d)) = ran(M(d)) ⊆ dom(C) = dom(C') | introduced |
| R-COMM | LEMMA | π(v + k) = π(v) + k when v and v + k lie in the same region: cut-point permutation commutes with ordinal shift | introduced |
| R-BLK | LEMMA | Run partition transforms by split-at-cuts then displace-per-region, preserving S8(a)/(b) under M'(d) | introduced |


## Open Questions

Does the 4-cut swap definition generalize to k-cut rearrangements for k > 4, and if so, what is the natural class of permutations that "rearrangement by cut points" can express?

What must a well-formed editing sequence guarantee about the composition of multiple rearrangements — is the composition of two rearrangements always expressible as a single rearrangement, or can sequences of rearrangements produce arrangements unreachable by any single operation?

Under what conditions can a rearrangement cause the number of correspondence runs in the canonical partition to increase, and is there an upper bound on the increase relative to the number of cut points?

What constraints, if any, must cut points satisfy relative to the run boundaries of the canonical partition, or are arbitrary cut positions within the V-span always valid?
