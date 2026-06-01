# Review of ASN-0047

## REVISE

### Issue 1: K.μ~ admissibility admits unrealisable link-subspace permutations

**ASN-0047, *Decomposition of K.μ~* (admissibility clauses and Step (A))**: "π is admissible iff (i) ... (ii) ... (iii) *length-preserving* ... (iv) *subspace-preserving* ..." and "the admissible and realisable classes coincide."

**Problem**: The four admissibility clauses do not exclude a non-trivial permutation *within* the link subspace. Take a document whose link subspace has two equal-depth positions `[2,1] ↦ ℓ₁` and `[2,2] ↦ ℓ₂` with `ℓ₁ ≠ ℓ₂`, and let π transpose `[2,1] ↔ [2,2]`. This π is:
- length-preserving (iii) — both depth 2;
- subspace-preserving (iv) — both `s_L`;
- non-trivial (ii) — `M'(d)([2,1]) = ℓ₂ ≠ ℓ₁`;
- shape-package-compatible (i) — clause (i) constrains V-position *domains*, which are unchanged.

So π is admissible. But the K.μ⁻ + K.μ⁺ full-clearance decomposition **cannot realise it**: K.μ⁺ (amended) writes only content-subspace positions, K.μ⁻ only removes link positions by suffix, and K.μ⁺_L is not part of the K.μ~ decomposition — there is no way to re-seat a link at a different V-position. Hence an admissible π exists that is not realisable, contradicting Step (A)'s coincidence claim.

This same π is also a counterexample to the **Link-subspace fixity** theorem as stated (`π(v) = v` for `v ∈ dom_L`): the fixity proof's step (3) (`M'(d)|_{dom_L} = M(d)|_{dom_L}`) silently assumes the full-clearance realization that fixes links, so the theorem is proved only for *realisable* π, not for the *admissible* class it quantifies over. Clause (iv)'s stated role — "what makes the realisable π coincide with the admissible π" — is therefore incomplete: it excludes cross-subspace permutations but not within-`s_L` permutations.

**Required**: Add an explicit admissibility clause (v) `(A v ∈ dom_L(M(d)) :: π(v) = v)` (π fixes the link subspace pointwise), reflecting the design intent that links carry permanent order-of-arrival and are not rearrangeable; or otherwise restrict the admissibility predicate so that the admissible class genuinely coincides with the realisable one. Restate Link-subspace fixity as a consequence of that clause rather than as a theorem over the current (too-broad) admissibility class. Step (A)'s reverse direction ("full-clearance realises every subspace-preserving π") must then be corrected — it is false for link-permuting subspace-preserving π.

### Issue 2: Full-clearance form re-stated in three places without added content

**ASN-0047, *Decomposition of K.μ~***: the full-clearance realization (`n'_{s_C} = 0`, clear content / retain links / rebuild) is described in the "Full-clearance form (canonical statement)" paragraph, again in the closing "Decomposition" paragraph and its bullet, and a third time in the Class (a) matrix note ("any cell not naming a cut point reads as full-clearance").

**Problem**: Carries the `review-mode.anti-bloat` classifier. Three separate prose statements of the identical mechanism force the reader to confirm they say the same thing. This is the "two paragraphs say the same thing in different words" pattern.

**Required**: State the full-clearance realization once (at the canonical-statement paragraph) and have the later "Decomposition" paragraph and matrix note point to it without re-describing the clear/retain/rebuild steps.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link withdrawal

**Why out of scope**: The inability to remove an interior link without suffix-only contraction is correctly deferred to the Open Questions (the `DELETEVSPAN` compaction-with-renumbering operation), and interior-withdrawal mechanics belong to a named-operation ASN, not this transition taxonomy. Note this is *distinct* from Issue 1, which is about the admissibility predicate over-generating, not about modelling a new contraction operation.

VERDICT: REVISE
