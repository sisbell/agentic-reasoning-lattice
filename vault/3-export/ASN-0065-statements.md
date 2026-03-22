# ASN-0065 Formal Statements

*Source: ASN-0065-rearrange-operation.md (revised 2026-03-21) — Extracted: 2026-03-22*

## Definition — CutSequence

A *cut sequence* for document d in subspace S is a tuple C = (c₀, c₁, ..., c_{n−1}) of tumblers satisfying:

(CS1) n ∈ {3, 4} — exactly three or four cuts.

(CS2) c₀ < c₁ < ... < c_{n−1} under T1 (ASN-0034) — strictly ordered.

(CS3) subspace(cᵢ) = S for all i — all cuts in the same subspace.

(CS4) #cᵢ = 2 for all i — depth-2 positions.

---

## Definition — RegionPartition

Given a cut sequence C for document d in subspace S with V_S(d) ≠ ∅:

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

w_α = |α|, w_β = |β|, w_μ = |μ| for the region widths.

---

## Definition — PivotPostcondition

Given a 3-cut sequence C = (c₀, c₁, c₂) satisfying R-PRE, the *pivot* produces arrangement M'(d) defined by:

(R-EXT) For v ∈ V_S(d) with v < c₀ or v ≥ c₂:

`M'(d)(v) = M(d)(v)`

(R-P1) For 0 ≤ j < w_β:

`M'(d)(c₀ + j) = M(d)(c₁ + j)`

(R-P2) For 0 ≤ j < w_α:

`M'(d)(c₀ + w_β + j) = M(d)(c₀ + j)`

where `c₀ + j` and `c₁ + j` denote j ordinal increments via TA5(c) (ASN-0034), and `c₀ + 0 = c₀` by the M-aux convention (ASN-0058). The domain is dom(M'(d)) = dom(M(d)).

---

## Definition — SwapPostcondition

Given a 4-cut sequence C = (c₀, c₁, c₂, c₃) satisfying R-PRE, the *swap* produces M'(d) defined by:

(R-EXT) For v ∈ V_S(d) with v < c₀ or v ≥ c₃:

`M'(d)(v) = M(d)(v)`

(R-S1) For 0 ≤ j < w_β:

`M'(d)(c₀ + j) = M(d)(c₂ + j)`

(R-S2) For 0 ≤ j < w_μ:

`M'(d)(c₀ + w_β + j) = M(d)(c₁ + j)`

(R-S3) For 0 ≤ j < w_α:

`M'(d)(c₀ + w_β + w_μ + j) = M(d)(c₀ + j)`

with dom(M'(d)) = dom(M(d)).

---

## Definition — PermutationDisplacement

For a position v in the affected range, define Δ(v) = ord(π(v)) − ord(v) (an integer, possibly negative).

For the 3-cut pivot:

```
Δ(v) = +w_β      if v ∈ α     (shifts forward by width of β)
Δ(v) = −w_α      if v ∈ β     (shifts backward by width of α)
Δ(v) = 0         otherwise
```

For the 4-cut swap:

```
Δ(v) = +(w_β + w_μ)        if v ∈ α   (shifts forward past middle and β)
Δ(v) = +(w_β − w_α)        if v ∈ μ   (adjusts by width difference)
Δ(v) = −(w_α + w_μ)        if v ∈ β   (shifts backward past middle and α)
Δ(v) = 0                   otherwise
```

---

## R-PRE — RearrangePrecondition (PRE, requires)

(i) d ∈ E_doc

(ii) V_S(d) ≠ ∅

(iii) The cut sequence C = (c₀, ..., c_{n−1}) satisfies CS1–CS4.

(iv) `(A v : subspace(v) = S ∧ #v = 2 ∧ c₀ ≤ v < c_{n−1} : v ∈ V_S(d))`

(v) w_α ≥ 1 and w_β ≥ 1

(vi) All cuts and all resulting positions remain within subspace S. At depth 2, satisfied automatically when all cut ordinals are positive.

---

## R-EXT — ExteriorUnchanged (INV, ensures)

For v ∈ V_S(d) with v < c₀ or v ≥ c_{n−1}:

`M'(d)(v) = M(d)(v)`

(n−1 = 2 for 3-cut pivot; n−1 = 3 for 4-cut swap)

---

## R-P1 — PivotBetaToStart (INV, ensures)

`(A j : 0 ≤ j < w_β : M'(d)(c₀ + j) = M(d)(c₁ + j))`

---

## R-P2 — PivotAlphaToEnd (INV, ensures)

`(A j : 0 ≤ j < w_α : M'(d)(c₀ + w_β + j) = M(d)(c₀ + j))`

---

## R-S1 — SwapBetaToStart (INV, ensures)

`(A j : 0 ≤ j < w_β : M'(d)(c₀ + j) = M(d)(c₂ + j))`

---

## R-S2 — SwapMuToMiddle (INV, ensures)

`(A j : 0 ≤ j < w_μ : M'(d)(c₀ + w_β + j) = M(d)(c₁ + j))`

---

## R-S3 — SwapAlphaToEnd (INV, ensures)

`(A j : 0 ≤ j < w_α : M'(d)(c₀ + w_β + w_μ + j) = M(d)(c₀ + j))`

---

## R-PIV — PivotWellDefined (LEMMA, lemma)

The pivot postcondition defines a total function on V_S(d) (each position is assigned exactly one I-address).

Proof key: the R-P1 ordinal range is [p, p + w_β) and the R-P2 ordinal range is [p + w_β, p + w_β + w_α); these are disjoint and their union covers [c₀, c₂) ∩ V_S(d). Together with R-EXT (covering V_S(d) \ [c₀, c₂)), every position is covered exactly once.

---

## R-PPERM — PivotPermutation (LEMMA, lemma)

The bijection π : dom(M(d)) → dom(M'(d)) satisfying M'(d)(π(v)) = M(d)(v) is:

```
         ⎧ v                   if v < c₀ or v ≥ c₂          (exterior)
π(v) =  ⎨ c₀ + w_β + j        if v = c₀ + j, 0 ≤ j < w_α   (α → end)
         ⎩ c₀ + j              if v = c₁ + j, 0 ≤ j < w_β   (β → start)
```

---

## R-SWP — SwapWellDefined (LEMMA, lemma)

The swap postcondition defines a total function on V_S(d).

The three clause ranges [c₀, c₀ + w_β), [c₀ + w_β, c₀ + w_β + w_μ), [c₀ + w_β + w_μ, c₀ + w_β + w_μ + w_α) partition [c₀, c₃) (total width w_β + w_μ + w_α = w_α + w_μ + w_β = |[c₀, c₃)|). The right-hand sides reference M(d) at positions within dom(M(d)) by R-PRE(iv).

---

## R-SPERM — SwapPermutation (LEMMA, lemma)

The bijection π satisfying M'(d)(π(v)) = M(d)(v) is:

```
         ⎧ v                        if v < c₀ or v ≥ c₃                (exterior)
         ⎪ c₀ + w_β + w_μ + j       if v = c₀ + j, 0 ≤ j < w_α        (α → end)
π(v) =  ⎨ c₀ + w_β + j             if v = c₁ + j, 0 ≤ j < w_μ        (μ → middle)
         ⎩ c₀ + j                   if v = c₂ + j, 0 ≤ j < w_β        (β → start)
```

---

## R-CP — ContentPreservation (INV, ensures)

`ran(M'(d)) = ran(M(d))`

as multisets (that is, for every I-address a, the multiplicity |{v : M'(d)(v) = a}| = |{v : M(d)(v) = a}|).

Corollary (R-CP-set): `{a : (E v :: M'(d)(v) = a)} = {a : (E v :: M(d)(v) = a)}`

---

## R-CF — RearrangeFrame (INV, ensures)

(a) C' = C — the content store is unchanged.

(b) E' = E — the entity set is unchanged.

(c) R' = R — the provenance relation is unchanged.

---

## R-XD — CrossDocumentIsolation (INV, ensures)

For all d' ≠ d:

`M'(d') = M(d')`

---

## R-XS — SubspaceConfinement (INV, ensures)

For all v with subspace(v) ≠ S:

`M'(d)(v) = M(d)(v)`

---

## R-IID — DocumentIdentityPreservation (INV, ensures)

`d ∈ E'_doc`

Follows from E' = E (R-CF(b)).

---

## R-KMU — KMuTildePreVerification (LEMMA, lemma)

REARRANGE satisfies the K.μ~ preconditions:

(i) d ∈ E_doc — from R-PRE(i).

(ii) π maps dom(M(d)) to itself — dom(M'(d)) = dom(M(d)); every v ∈ dom(M(d)) satisfies S8a in the pre-state, and π(v) ∈ dom(M(d)), so every image under π satisfies S8a.

(iii) M'(d) satisfies S8-depth — since dom(M'(d)) = dom(M(d)), the depth profile is unchanged.

---

## R-S2P — FunctionalityPreservation (LEMMA, lemma)

REARRANGE preserves S2 (ArrangementFunctionality).

R-PIV and R-SWP establish that the postcondition defines a total function on V_S(d) — each V-position is assigned exactly one I-address. For positions outside subspace S, M'(d)(v) = M(d)(v) by R-XS, which is uniquely determined by S2 in the pre-state.

---

## R-S3P — ReferentialIntegrityPreservation (LEMMA, lemma)

REARRANGE preserves S3 (ReferentialIntegrity).

By R-CP, ran(M'(d)) = ran(M(d)). By S3 in the pre-state, ran(M(d)) ⊆ dom(C). By R-CF(a), C' = C, so dom(C') = dom(C). Therefore:

`ran(M'(d)) = ran(M(d)) ⊆ dom(C) = dom(C')`

---

## R-S8P — StructuralPreservation (LEMMA, lemma)

REARRANGE preserves S8a, S8-depth, and S8-fin.

All three properties are predicates on dom(M(d)). Since dom(M'(d)) = dom(M(d)), each is inherited from the pre-state:

- S8a (VPositionWellFormedness): every v ∈ dom(M'(d)) = dom(M(d)) satisfies zeros(v) = 0 ∧ v > 0.
- S8-depth (FixedDepthVPositions): all V-positions in each subspace share depth, unchanged by domain equality.
- S8-fin (FiniteArrangement): |dom(M'(d))| = |dom(M(d))| < ∞.

---

## R-P4P — ProvenanceBoundsPreservation (LEMMA, lemma)

REARRANGE preserves P4 (ProvenanceBounds: Contains(Σ) ⊆ R).

Contains(Σ') = {(a, d') : d' ∈ E'_doc ∧ a ∈ ran(M'(d'))}.

For the target document d: ran(M'(d)) = ran(M(d)) by R-CP.
For all other d' ≠ d: M'(d') = M(d') by R-XD, so ran(M'(d')) = ran(M(d')).

Therefore Contains(Σ') = Contains(Σ). By P4 in the pre-state, Contains(Σ) ⊆ R. By J3 (ReorderingIsolation, ASN-0047), R' = R. Hence:

`Contains(Σ') = Contains(Σ) ⊆ R = R'`

---

## R-DP — ContiguityPreservation (LEMMA, lemma)

If V_S(d) satisfies D-CTG before rearrangement, then V_S'(d) satisfies D-CTG after rearrangement.

dom(M'(d)) ∩ {v : subspace(v) = S} = dom(M(d)) ∩ {v : subspace(v) = S} = V_S(d).

Since V_S'(d) = V_S(d) as a set of positions, contiguity is inherited.

---

## R-WR — WidthPreservation (LEMMA, lemma)

`|V_S'(d)| = |V_S(d)|`

Follows from V_S'(d) = V_S(d) (same positions, different content mapping).

---

## R-BLK — BlockDecompositionTransformation (LEMMA, lemma)

Let B = {β₁, ..., βₘ} be a block decomposition of M(d) satisfying B1–B3 (ASN-0058). Let the cut sequence C have cut positions c₀, ..., c_{n−1}. The rearranged arrangement M'(d) admits a block decomposition B' obtained by:

*Phase 1 (Split).* For each cut position cᵢ, if cᵢ falls in the interior of some block βₖ = (vₖ, aₖ, nₖ) — meaning cᵢ ∈ V(βₖ) and cᵢ ≠ vₖ — split βₖ at c = ord(cᵢ) − ord(vₖ) via M4 (SplitDefinition, ASN-0058), producing (vₖ, aₖ, c) and (vₖ + c, aₖ + c, nₖ − c). After all splits, no block straddles any cut position.

*Phase 2 (Classify).* Each block in the post-split decomposition lies entirely within one region (exterior left, α, μ if 4-cut, β, or exterior right).

*Phase 3 (Reassemble).* Apply the permutation to each block's V-start:
- Exterior blocks: unchanged.
- α blocks: βₖ = (vₖ, aₖ, nₖ) becomes (π(vₖ), aₖ, nₖ).
- β blocks: V-start shifts by the β displacement; I-start and width preserved.
- μ blocks (4-cut only): V-start shifts by the μ displacement; I-start and width preserved.

Each reassembled block (π(vⱼ), aⱼ, nⱼ) satisfies B3: for each offset k with 0 ≤ k < nⱼ:

`M'(d)(π(vⱼ) + k) = M'(d)(π(vⱼ + k)) = M(d)(vⱼ + k) = aⱼ + k`

The second equality holds because π(vⱼ + k) = π(vⱼ) + k — the uniform displacement means ordinal increment commutes with the permutation within each region.

---

## R-LS — LinkSurvivability (LEMMA, lemma)

If a link's endset references I-address a, and a ∈ ran(M(d)), then a ∈ ran(M'(d)) after any rearrangement.

`ran(M'(d)) = ran(M(d))`

by R-CP, so a ∈ ran(M(d)) implies a ∈ ran(M'(d)).
