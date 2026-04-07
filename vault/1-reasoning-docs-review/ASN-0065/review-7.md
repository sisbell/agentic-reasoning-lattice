# Review of ASN-0065

## REVISE

### Issue 1: P4 preservation not derived

**ASN-0065, K.μ~ Preconditions and Arrangement Invariants**: The ASN explicitly verifies S2 (R-S2P), S3 (R-S3P), S8a/S8-depth/S8-fin (R-S8P), and D-CTG (R-DP), but does not state that P4 (ProvenanceBounds: Contains(Σ) ⊆ R) is preserved.

**Problem**: P4 is the most non-trivial of the frame-dependent invariants because its preservation requires R-CP (content preservation), not just the frame conditions. The argument is: Contains(Σ') = Contains(Σ) because ran(M'(d)) = ran(M(d)) (R-CP) and M'(d') = M(d') for d' ≠ d (R-XD), so Contains(Σ') = Contains(Σ) ⊆ R = R' (by pre-state P4 and J3). This three-step chain uses R-CP in a way the reader should see explicitly. The remaining invariants (P6, P7, P7a, P8) follow directly from the frame conditions alone, but the asymmetry — verifying S2/S3/S8* in detail while leaving P4 implicit — creates a completeness gap. Either verify all, or note that all are guaranteed by the ReachableStateInvariants theorem and give the non-trivial P4 derivation.

**Required**: Add a brief statement (one paragraph or a labeled lemma) deriving P4 preservation from R-CP, R-XD, and J3. Optionally note that P6, P7, P7a, P8 follow from R-CF alone.

### Issue 2: Incorrect position labels in composition discussion

**ASN-0065, The 3-Cut Pivot as the Fundamental Case**: "After this, α is at [c₁, c₂) and μ is at [c₀, c₁), and β is at its original position."

**Problem**: After a 3-cut pivot with cuts (c₀, c₁, c₂) swapping α = [c₀, c₁) and μ = [c₁, c₂), the pivot places the second region first: μ's content occupies [c₀, c₀ + w_μ) and α's content occupies [c₀ + w_μ, c₂). The stated positions [c₀, c₁) and [c₁, c₂) are correct only when w_α = w_μ (since c₁ = c₀ + w_α, and c₀ + w_μ = c₁ only if w_μ = w_α). In general, [c₁, c₂) has width w_μ while α has width w_α — these intervals don't match. The conclusion ("the content layout is [μ, α, β]") is correct regardless.

**Required**: Replace the position labels with "μ is at [c₀, c₀ + w_μ) and α is at [c₀ + w_μ, c₂)."

## OUT_OF_SCOPE

None. The Open Questions section comprehensively identifies the natural follow-on topics (k-cut generalization, composition closure, block-count bounds, depth generalization, front-end rendering, discovery index).

VERDICT: REVISE
