# ASN-0084 Claim Statements

*Source: ASN-0084-bundle-projection-displacement.md (revised 2026-04-10) — Extracted: 2026-05-15*

## Definition — CutSequence

A *cut sequence* for document d in subspace S is a tuple K = (c₀, c₁, ..., c_{n−1}) of tumblers satisfying:

(CS1) n ∈ {3, 4} — exactly three or four cuts.

(CS2) c₀ < c₁ < ... < c_{n−1} under T1 (ASN-0034) — strictly ordered.

(CS3) subspace(cᵢ) = S = 1 for all i — all cuts in the text subspace.

(CS4) #cᵢ = 2 for all i — depth-2 positions.

---

## Definition — RegionPartition

Given a cut sequence K for document d in subspace S with V_S(d) ≠ ∅:

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

Region widths: w_α = |α|, w_β = |β|, w_μ = |μ|.

Width-ordinal identities: w_α = ord(c₁) − ord(c₀); w_β = ord(c₂) − ord(c₁) for n = 3 and ord(c₃) − ord(c₂) for n = 4; w_μ = ord(c₂) − ord(c₁) for n = 4.

---

## R-PRE — RearrangePrecondition (DEF, precondition)

(i) M(d) is well-defined (the document's arrangement exists).

(ii) V_S(d) ≠ ∅ (the subspace is non-empty).

(iii) The cut sequence K = (c₀, ..., c_{n−1}) satisfies CS1–CS4.

(iv) The affected range lies entirely within the current arrangement:

`(A v : subspace(v) = S ∧ #v = 2 ∧ c₀ ≤ v < c_{n−1} : v ∈ V_S(d))`

*Derived consequence — Width positivity:* w_α ≥ 1 and w_β ≥ 1 in both forms; additionally w_μ ≥ 1 when n = 4.

---

## Definition — PivotPostcondition

Given a 3-cut sequence K = (c₀, c₁, c₂) satisfying R-PRE, the *pivot* produces arrangement M'(d) defined by:

(R-EXT) For v ∈ V_S(d) with v < c₀ or v ≥ c₂:

`M'(d)(v) = M(d)(v)`

(R-P1) For 0 ≤ j < w_β:

`M'(d)(c₀ + j) = M(d)(c₁ + j)`

(R-P2) For 0 ≤ j < w_α:

`M'(d)(c₀ + w_β + j) = M(d)(c₀ + j)`

The domain is dom(M'(d)) = dom(M(d)).

---

## Definition — SwapPostcondition

Given a 4-cut sequence K = (c₀, c₁, c₂, c₃) satisfying R-PRE, the *swap* produces M'(d) defined by:

(R-EXT) For v ∈ V_S(d) with v < c₀ or v ≥ c₃:

`M'(d)(v) = M(d)(v)`

(R-S1) For 0 ≤ j < w_β:

`M'(d)(c₀ + j) = M(d)(c₂ + j)`

(R-S2) For 0 ≤ j < w_μ:

`M'(d)(c₀ + w_β + j) = M(d)(c₁ + j)`

(R-S3) For 0 ≤ j < w_α:

`M'(d)(c₀ + w_β + w_μ + j) = M(d)(c₀ + j)`

The domain is dom(M'(d)) = dom(M(d)).

---

## REARRANGE_K — RearrangeK (OPERATION, method)

REARRANGE_K(Σ, d) is the state transition Σ → Σ' that produces Σ' satisfying PivotPostcondition (when n = 3) or SwapPostcondition (when n = 4) together with the corresponding frame conditions R-FRAME-P (n = 3) or R-FRAME-S (n = 4).

*Precondition:* R-PRE(K).

*Runtime signature:* (Σ, d) ↦ Σ'.

*Partiality:* REARRANGE_K is defined exactly on those (Σ, d) for which R-PRE(K) holds against Σ.M(d); on inputs that violate R-PRE(K), REARRANGE_K is undefined.

The intra-document arrangement Σ.M(d) is the only mutated component: Σ.C, all other documents' arrangements Σ.M(d') for d' ≠ d, and the within-d non-S subspace portion of Σ.M(d) are preserved by the frame conditions; dom(M'(d)) = dom(M(d)) is asserted by the postconditions.

---

## Definition — ArrangementRearrangement

An *arrangement rearrangement* is a state transition Σ → Σ' in which:

- dom(M'(d)) = dom(M(d))
- C' = C (S0, ASN-0036)
- M'(d') = M(d') for all d' ≠ d
- there exists a bijection π : dom(M(d)) → dom(M'(d)) such that M'(d)(π(v)) = M(d)(v) for all v ∈ dom(M(d))

*Derived:* ran(M'(d)) = ran(M(d)); for each I-address a, the multiplicity of a in M(d) and M'(d) is identical.

---

## Definition — PermutationDisplacement

For a position v ∈ dom(M(d)), define Δ(v) as a signed magnitude (σ, n) ∈ {+, −, 0} × ℕ:

```
Δ(v) = (0, 0)                               if subspace(v) ≠ S
Δ(v) = (0, 0)                               if v ∈ V_S(d) and π(v) = v
Δ(v) = (+, ord(π(v)) − ord(v))              if v ∈ V_S(d) and ord(π(v)) > ord(v)
Δ(v) = (−, ord(v) − ord(π(v)))              if v ∈ V_S(d) and ord(π(v)) < ord(v)
```

For 3-cut pivot (from R-PPERM):

```
Δ(v) = +w_β      if v ∈ α
Δ(v) = −w_α      if v ∈ β
Δ(v) = 0         otherwise
```

For 4-cut swap (from R-SPERM):

```
Δ(v) = +(w_β + w_μ)        if v ∈ α
Δ(v) = +(w_β − w_α)        if v ∈ μ and w_β > w_α
Δ(v) = −(w_α − w_β)        if v ∈ μ and w_β < w_α
Δ(v) = 0                   if v ∈ μ and w_β = w_α
Δ(v) = −(w_α + w_μ)        if v ∈ β
Δ(v) = 0                   otherwise
```

---

## R-DISP — DisplacementUniformity (LEMMA, lemma)

*Preconditions:* Cut sequence K satisfying R-PRE; π the permutation from R-PPERM (3-cut) or R-SPERM (4-cut).

*Statement:* For all v₁, v₂ in the same region — where the regions partition dom(M(d)) into the non-S domain {v ∈ dom(M(d)) : subspace(v) ≠ S}, the subspace-S exterior {v ∈ V_S(d) : v < c₀ or v ≥ c_{n−1}}, α, β, and (for 4-cut) μ:

`Δ(v₁) = Δ(v₂)`

with common values:

- Δ = 0 on the non-S domain
- 3-cut: Δ = +w_β on α; Δ = −w_α on β; Δ = 0 on the subspace-S exterior
- 4-cut: Δ = +(w_β + w_μ) on α; Δ = −(w_α + w_μ) on β; Δ = 0 on the subspace-S exterior; on μ: Δ = +(w_β − w_α) when w_β > w_α, Δ = −(w_α − w_β) when w_β < w_α, Δ = 0 when w_β = w_α

---

## Definition — Split

Given a run b = (v, a, n) under some arrangement A and an interior offset c with 1 ≤ c < n, the *split* at c produces two runs:

`(v, a, c)` and `(v + c, a + c, n − c)`

Their V-extents (ordinal ranges [ord(v), ord(v) + c) and [ord(v) + c, ord(v) + n)) are disjoint and partition b's V-extent.

Both pieces inherit S8(b) under A:
- For (v, a, c): A(v + k) = a + k for 0 ≤ k < c, by restricting original S8(b) to k < c.
- For (v + c, a + c, n − c): A((v + c) + k) = (a + c) + k for 0 ≤ k < n − c, via associativity/identity applied to the original S8(b).

---

## Definition — Merge

Two runs (v₁, a₁, n₁) and (v₂, a₂, n₂) under arrangement A are *mergeable* when:

- v₂ = v₁ + n₁ (V-adjacent)
- a₂ = a₁ + n₁ (I-adjacent)

The merged run is (v₁, a₁, n₁ + n₂).

S8(b) for the merged run — A(v₁ + k) = a₁ + k for 0 ≤ k < n₁ + n₂ — holds by:
- For 0 ≤ k < n₁: S8(b) of the first run directly.
- For n₁ ≤ k < n₁ + n₂: write k = n₁ + k', use adjacency conditions and S8(b) of the second run: A(v₂ + k') = a₂ + k' = a₁ + k.

---

## Definition — CanonicalRunDecomposition

The *canonical run decomposition* of M(d) is the unique partition of dom(M(d)) into *maximal* runs — runs that cannot be extended by merging with a V-adjacent, I-adjacent neighbor.

A run b = (v_b, a_b, n_b) is *maximal* iff no valid correspondence run b* with V(b*) ⊋ V(b) exists.

Uniqueness established by four steps:
- (a) For each v ∈ V_S(d), the maximal run containing v is uniquely determined by f(v) = max{k ≥ 0 : (A j : 0 ≤ j ≤ k : v + j ∈ V_S(d) ∧ M(d)(v + j) = M(d)(v) + j)} and r(v) = max{k ≥ 0 : [S, ord(v) − k] ∈ V_S(d) ∧ (A i : 0 ≤ i ≤ k : M(d)([S, ord(v) − k + i]) = shift(M(d)([S, ord(v) − k]), i))}.
- (b) Two maximal runs sharing a V-position are identical.
- (c) The exhaustive merge process terminates at the unique maximal-run partition regardless of merge order.
- (d) Maximal runs admit no merge: if v₂ = v₁ + n₁ and a₂ = a₁ + n₁ then (v₁, a₁, n₁ + n₂) strictly contains V(b₁), contradicting maximality.

---

## R-PIV — PivotWellDefined (LEMMA, supporting lemma)

*Statement:* The pivot postcondition defines a total function on dom(M(d)) — each position is assigned exactly one I-address.

*Formal content:*

(a) Every v ∈ dom(M(d)) falls under exactly one of R-EXT, R-P1, R-P2 (or R-FRAME-P(a) for non-S positions).

- R-P1 ordinal range: [ord(c₀), ord(c₀) + w_β) — non-empty since w_β ≥ 1.
- R-P2 ordinal range: [ord(c₀) + w_β, ord(c₀) + w_β + w_α) — non-empty since w_α ≥ 1.
- Ranges disjoint; union = [ord(c₀), ord(c₀) + w_α + w_β) = [c₀, c₂) ∩ V_S(d).
- R-EXT covers V_S(d) \ [c₀, c₂).

(b) Right-hand sides are well-defined: M(d)(c₁ + j) for j < w_β and M(d)(c₀ + j) for j < w_α are all in dom(M(d)) by R-PRE(iv).

---

## R-SWP — SwapWellDefined (LEMMA, supporting lemma)

*Statement:* The swap postcondition defines a total function on dom(M(d)).

*Formal content:*

(a) Every v ∈ dom(M(d)) falls under exactly one of R-EXT, R-S1, R-S2, R-S3 (or R-FRAME-S(a) for non-S positions). Ordinal ranges:

- R-S1: [ord(c₀), ord(c₀) + w_β)
- R-S2: [ord(c₀) + w_β, ord(c₀) + w_β + w_μ)
- R-S3: [ord(c₀) + w_β + w_μ, ord(c₀) + w_β + w_μ + w_α)
- R-EXT: ordinals outside [ord(c₀), ord(c₀) + w_α + w_μ + w_β)

Left endpoints strictly increasing: ord(c₀) < ord(c₀) + w_β < ord(c₀) + w_β + w_μ < ord(c₀) + w_β + w_μ + w_α (since w_α, w_β, w_μ ≥ 1). Union = [ord(c₀), ord(c₃)) = [c₀, c₃) ∩ V_S(d).

(b) Right-hand sides M(d)(c₂ + j), M(d)(c₁ + j), M(d)(c₀ + j) are all in dom(M(d)) by R-PRE(iv).

---

## R-PPERM — PivotPermutation (LEMMA, lemma)

*Statement:* The cut-point-induced bijection π : dom(M(d)) → dom(M'(d)) satisfying M'(d)(π(v)) = M(d)(v) is:

```
         ⎧ v                   if subspace(v) ≠ S
         ⎪ v                   if v ∈ V_S(d) and (v < c₀ or v ≥ c₂)
π(v) =  ⎨ c₀ + w_β + j        if v = c₀ + j, 0 ≤ j < w_α              (α → end)
         ⎩ c₀ + j              if v = c₁ + j, 0 ≤ j < w_β              (β → start)
```

*Verification:* M'(d)(π(v)) = M(d)(v) in each case:
- Non-S: π(v) = v and M'(d)(v) = M(d)(v) by R-NS(NS-π).
- Exterior: π(v) = v and M'(d)(v) = M(d)(v) by R-EXT.
- α (v = c₀ + j): π(v) = c₀ + w_β + j; M'(d)(c₀ + w_β + j) = M(d)(c₀ + j) = M(d)(v) by R-P2.
- β (v = c₁ + j): π(v) = c₀ + j; M'(d)(c₀ + j) = M(d)(c₁ + j) = M(d)(v) by R-P1.

*Bijectivity:* Four image sets are pairwise disjoint; π is a self-injection on finite dom(M(d)), hence a bijection.

---

## R-SPERM — SwapPermutation (LEMMA, lemma)

*Statement:* The cut-point-induced bijection π satisfying M'(d)(π(v)) = M(d)(v) is:

```
         ⎧ v                        if subspace(v) ≠ S
         ⎪ v                        if v ∈ V_S(d) and (v < c₀ or v ≥ c₃)
         ⎪ c₀ + w_β + w_μ + j       if v = c₀ + j, 0 ≤ j < w_α              (α → end)
π(v) =  ⎨ c₀ + w_β + j             if v = c₁ + j, 0 ≤ j < w_μ              (μ → middle)
         ⎩ c₀ + j                   if v = c₂ + j, 0 ≤ j < w_β              (β → start)
```

*Verification:* M'(d)(π(v)) = M(d)(v) in each case:
- Non-S: by R-NS(NS-π).
- Exterior: by R-EXT.
- α (v = c₀ + j): π(v) = c₀ + w_β + w_μ + j; M'(d)(c₀ + w_β + w_μ + j) = M(d)(c₀ + j) by R-S3.
- μ (v = c₁ + j): π(v) = c₀ + w_β + j; M'(d)(c₀ + w_β + j) = M(d)(c₁ + j) by R-S2.
- β (v = c₂ + j): π(v) = c₀ + j; M'(d)(c₀ + j) = M(d)(c₂ + j) by R-S1.

*Bijectivity:* Five image sets are pairwise disjoint; π is a self-injection on finite dom(M(d)), hence a bijection.

---

## R-FRAME-P — FramePivot (FRAME, frame conditions)

Frame conditions for the pivot (n = 3):

(a) For v ∈ dom(M(d)) with subspace(v) ≠ S: `M'(d)(v) = M(d)(v)`

(b) For all d' ≠ d: `M'(d') = M(d')`

(c) `C' = C` (S0, ASN-0036)

---

## R-FRAME-S — FrameSwap (FRAME, frame conditions)

Frame conditions for the swap (n = 4):

(a) For v ∈ dom(M(d)) with subspace(v) ≠ S: `M'(d)(v) = M(d)(v)`

(b) For all d' ≠ d: `M'(d') = M(d')`

(c) `C' = C` (S0, ASN-0036)

---

## R-NS — NonSubspaceInvariance (LEMMA, lemma)

*Preconditions:* π the cut-point-induced bijection (R-PPERM for n = 3, R-SPERM for n = 4); B a correspondence-run partition of M(d).

*Statement:* The following hold jointly:

*(NS-π) Pointwise identity on non-S.* For every v ∈ dom(M(d)) with subspace(v) ≠ S:

`π(v) = v` and `M'(d)(v) = M(d)(v)`

*(NS-run) Non-S runs carry verbatim into B'.* For every run b = (v_b, a_b, n_b) ∈ B with subspace(v_b) = S' ≠ S, the same triple (v_b, a_b, n_b) appears unchanged in B' = R-BLK(B), with:

`M'(d)(v_b + k) = a_b + k` for 0 ≤ k < n_b

*(NS-inv) ASN-0036 invariants on non-S positions transport trivially.* Every ASN-0036 invariant evaluated at a V-position v with subspace(v) ≠ S — or at a run whose V-extent lies in some subspace S' ≠ S — that depends only on dom(M restricted to non-S positions) and on M restricted to non-S positions is preserved unchanged on M'(d).

---

## R-RI — RearrangementReferentialIntegrity (LEMMA, lemma)

*Preconditions:* M(d) is well-defined; M'(d) results from an arrangement rearrangement of M(d) (dom(M'(d)) = dom(M(d)), C' = C, M'(d') = M(d') for d' ≠ d, bijection π with M'(d)(π(v)) = M(d)(v)); ASN-0036 S3 holds on the pre-state.

*Postcondition:*

`ran(M'(d)) ⊆ dom(C')`

*Proof chain:* ran(M'(d)) = ran(M(d)) [by bijection π] ⊆ dom(C) [by S3 pre-state] = dom(C') [by C' = C].

---

## R-COMM — PermutationShiftCommutativity (LEMMA, lemma)

*Preconditions:* π a cut-point permutation (R-PPERM or R-SPERM) for cut sequence K satisfying R-PRE; v ∈ dom(M(d)), offset k ≥ 0, v + k ∈ dom(M(d)), and v, v + k lie in the same region — where the regions are: non-S subspace ({v ∈ dom(M(d)) : subspace(v) ≠ S}), subspace-S exterior, α, μ, or β.

*Statement:*

`π(v + k) = π(v) + k`

Per region (using v = c_i + j' for the applicable start):
- Non-S: π(v + k) = v + k = π(v) + k by R-NS(NS-π).
- Exterior: π(v + k) = v + k = π(v) + k.
- 3-cut α (v = c₀ + j', 0 ≤ j' + k < w_α): π(v + k) = c₀ + w_β + (j' + k) = (c₀ + w_β + j') + k = π(v) + k.
- 3-cut β (v = c₁ + j', 0 ≤ j' + k < w_β): π(v + k) = c₀ + (j' + k) = (c₀ + j') + k = π(v) + k.
- 4-cut α (v = c₀ + j', 0 ≤ j' + k < w_α): π(v + k) = c₀ + w_β + w_μ + (j' + k) = π(v) + k.
- 4-cut μ (v = c₁ + j', 0 ≤ j' + k < w_μ): π(v + k) = c₀ + w_β + (j' + k) = π(v) + k.
- 4-cut β (v = c₂ + j', 0 ≤ j' + k < w_β): π(v + k) = c₀ + (j' + k) = π(v) + k.

---

## R-BLK — RunDecompositionTransformation (LEMMA, lemma)

*Preconditions:* B = {b₁, ..., bₘ} a run partition of M(d) per S8; cut sequence K with positions c₀, ..., c_{n−1} satisfying R-PRE.

*Statement:* The rearranged arrangement M'(d) admits a run partition B' obtained by three phases:

**Phase 1 — Split.** Process cuts in index order c₀, ..., c_{n−1}. For each cᵢ:
- *Interior of a run:* if cᵢ ∈ V(bₖ) and cᵢ ≠ vₖ, split bₖ = (vₖ, aₖ, nₖ) at offset c = ord(cᵢ) − ord(vₖ), producing (vₖ, aₖ, c) and (vₖ + c, aₖ + c, nₖ − c).
- *Boundary of a run:* if cᵢ ∈ V(bₖ) and cᵢ = vₖ, no split.
- *Outside ⋃_k V(bₖ):* no split. Occurs only for c_{n−1} when c_{n−1} ∉ V_S(d).

After Phase 1, no run straddles any cut position cᵢ for 0 ≤ i ≤ n − 1.

**Phase 2 — Classify.** Each run in the post-split partition is assigned to exactly one region: non-S, exterior left, α, μ (4-cut only), β, or exterior right.

**Phase 3 — Reassemble.** Each run (vₖ, aₖ, nₖ) becomes (π(vₖ), aₖ, nₖ): V-start replaced by π(vₖ); I-start aₖ and width nₖ preserved.

Per region:
- Non-S runs: π(vₖ) = vₖ by R-NS(NS-π); triple unchanged.
- Exterior runs: π(vₖ) = vₖ; triple unchanged.
- α, β, μ runs: π(vₖ) computed by R-PPERM or R-SPERM branch.

*S8(b) for reassembled subspace-S runs:* For each (π(vⱼ), aⱼ, nⱼ) and 0 ≤ k < nⱼ:

`M'(d)(π(vⱼ) + k) = M'(d)(π(vⱼ + k)) = M(d)(vⱼ + k) = aⱼ + k`

(First equality by R-COMM; second by the defining property of π; third by pre-state S8(b).)

*S8(a) for B':* V-extents of reassembled subspace-S runs are pairwise disjoint and cover V_S(d) (from bijectivity of π on V_S(d)); combined with R-NS(NS-run) for non-S runs, the V-extents of B' partition dom(M'(d)).

---

## R-SP — RearrangeSufficientPrecondition (LEMMA, lemma)

Let Q be the postcondition:

> M'(d) satisfies every ASN-0036 invariant carried by an arrangement transition — S0, S1, S2, S3, S4, S5, S7 (≡ S7a ∧ S7b ∧ S7c ∧ S7d), S7a, S7b, S7c, S7d, S9, D-CTG, D-CTG-depth, D-MIN, D-SEQ, S8a (VPositionWellFormedness), S8-fin, S8-depth, and S8 (SpanDecomposition) with clauses S8(a) (uniqueness of containing run) and S8(b) (consistency under M'(d)) — with the constructive witness B' = R-BLK(B) discharging the S8 existence clause.

*Statement (sufficiency only; necessity not claimed):*

`wp(REARRANGE_K, Q) ⇐ R-PRE(K) ∧ ASN-0036-invariants(Σ, d) ∧ (B is a correspondence-run partition of dom(M(d)) under M(d))`

*Discharge of Q clause-by-clause:*

- S0, S1, S4, S7a, S7b, S7c, S7d, S9: C' = C transports each verbatim.
- S2: each u = π(v) for exactly one v by bijectivity; M'(d)(u) = M(d)(v) uniquely determined.
- S3: R-RI gives ran(M'(d)) ⊆ dom(C').
- S5: bijection π preserves I-address multiplicities.
- D-CTG, D-CTG-depth, D-MIN, D-SEQ, S8a, S8-fin, S8-depth: each depends only on dom(M(d)); dom(M'(d)) = dom(M(d)) carries them verbatim.
- S8(a), S8(b): discharged constructively via B' = R-BLK(B), using R-COMM for the S8(b) equality chain and bijectivity of π for the S8(a) partition property.
