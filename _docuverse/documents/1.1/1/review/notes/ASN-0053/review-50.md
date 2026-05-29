# Review of ASN-0053

## REVISE

### Issue 1: S10's proof cites S9 alone for an inference that also requires S8
**ASN-0053, S10 (UnionOrderIndependence)**: "Since normalization depends only on the denotation (S9), normalize(Σ₁ ∪ Σ₂) = normalize(Σ₂ ∪ Σ₁)."
**Problem**: S9 establishes only *uniqueness* — that two normalized span-sets with equal denotation are identical. It does not establish that `normalize(X)` is a normalized span-set whose denotation equals `⟦X⟧`; that is S8. The inference is: let A = normalize(Σ₁∪Σ₂), B = normalize(Σ₂∪Σ₁); by **S8** both are normalized equivalents of their inputs, so `⟦A⟧ = ⟦Σ₁∪Σ₂⟧ = ⟦Σ₂∪Σ₁⟧ = ⟦B⟧`; then by **S9** A = B. As written the proof names only S9, omitting the denotation-preservation premise that makes the order-independence conclusion go through. "normalization depends only on the denotation" is precisely the conjunction of S8 (existence/preservation) and S9 (uniqueness), not S9 alone.
**Required**: Cite S8 for denotation-preservation alongside S9 for uniqueness, and note that S10's level-uniform/level-compatible hypothesis is what licenses S8 on the union span-sets.

### Issue 2: WR's precondition discharge mislabels D0 as a precondition
**ASN-0053, WR (WidthRecovery)**: "the divergence between s and reach(σ) is of type (i) with k ≤ #s … satisfying D0; #s ≤ #reach(σ) since both equal #s. Every D2 precondition is met."
**Problem**: D2's precondition is the proposition `divergence(a, b) ≤ #a`, not "D0." D0 is a theorem (DisplacementWellDefined), not a precondition slot to be satisfied. The discharge should name the proposition `divergence(s, reach(σ)) ≤ #s` directly. As written it conflates a foundation theorem with a precondition, which obscures exactly which D2 hypothesis is being discharged.
**Required**: Replace "satisfying D0" with the actual D2 precondition being discharged: `divergence(s, reach(σ)) = k ≤ #s`.

## OUT_OF_SCOPE

### Topic 1: Span algebra over non-level-uniform spans (#s ≠ #ℓ)
**Why out of scope**: Every theorem here is gated on level-uniformity/level-compatibility, and the worked failure after WR shows why (`[1,5] ⊖ [1,3,5] = [0,2,0]` does not round-trip). The general unequal-length case is genuinely new territory and is already acknowledged in the closing open question on width comparison by tumbler representation — it is not an error in this ASN.

### Topic 2: Span-set difference and its tight bound
**Why out of scope**: S11d bounds single-span difference at 2; the question of `|normalize(⟦Σ₁⟧ \ ⟦Σ₂⟧)|` for span-sets is correctly deferred to the open questions and belongs in a future ASN.

VERDICT: REVISE
