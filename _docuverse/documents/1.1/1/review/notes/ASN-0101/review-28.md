# Review of ASN-0101

This is a thorough, largely rigorous specification. The hard part — that the gap-closure shift `σ_d` re-tiles `V_S` into a contiguous prefix `{[S,1,...,1,k] : 1 ≤ k ≤ n_S − n}` with no gap and no overlap (Λ supplying last components `1..p−1`, Q supplying `p..n_S−n`) — is actually proved (D1), not hand-waved, and the boundary routing in D8 (vacuous vs. `σ_d`-witness vs. inherited) is correctly partitioned. The wp derivations and the three worked examples (content depth-3, link depth-2, cross-document transclusion) check out arithmetically. Two defects remain.

## REVISE

### Issue 1: Worked-example wp statements drop the enabledness conjunct that D11 makes load-bearing
**ASN-0101, "Verification of D11" (worked example) and cross-document D11 verification**: "`wp(DEL[d, σ], Q_disc(ℓ_0, d)) ≡ (E i : project(L(ℓ_0).eᵢ, d, Σ) ⊄ X)`" and "`wp(DEL[d, σ], discoverable_from(ℓ_0, d', ·)) ≡ discoverable_from(ℓ_0, d', Σ) = true`".

**Problem**: D11 deliberately defines every wp as `enabled(DEL[d, σ]) ∧ (pullback)`, justifying the conjunct at length ("Because DEL is partial, each weakest precondition for total correctness conjoins `enabled(DEL[d, σ])` ... exactly as LP12a conjoins `enabled(K.μ⁻[d, R])`; without the guard ... the predicate would not be the weakest precondition for total correctness"). The worked verifications then write the definitional equivalence `≡` with only the pullback clause. As stated, these are a strictly weaker predicate than D11's, contradicting the ASN's own emphasis that the guard is necessary. The verifications happen to evaluate `true` only because enabledness silently holds at the chosen pre-state.

**Required**: Restore the `enabled(DEL[d, σ]) ∧ ...` conjunct in each worked-example wp statement (or note explicitly that enabledness is discharged by the example's applicability and the residual equivalence is the pullback factor only).

### Issue 2: LP-family catalogue mis-names LP11
**ASN-0101, D10, LP-family extension catalogue**: "LP9 (ExtensionMonotonicity), LP10 (ContractionMonotonicity), LP11 (ReorderingRebinding) similarly concern K.μ⁺/K.μ⁺_L, K.μ⁻, and K.μ~ respectively."

**Problem**: ASN-0098's LP11 is **ReorderingBijection**, not "ReorderingRebinding." The catalogue is presented as the authoritative DEL row of LP-Comp's case analysis, so an incorrect lemma name undermines its claim to be the exhaustive dispatch. (Relatedly, "LP2★ (MultiStepSlotInvariance)" names a lemma ASN-0098 supplies only implicitly via the Closure schema (★) applied to LP2 (SlotInvariance); LP2★ is not an explicitly named ASN-0098 lemma the way LP3★ is. Confirm the intended reference.)

**Required**: Correct "ReorderingRebinding" to "ReorderingBijection," and verify the LP2★ reference resolves to a named ASN-0098 result (or cite it as "LP2 under the Closure schema").

## OUT_OF_SCOPE

None. The ASN correctly confines itself to DELETE mechanics; recoverability/versioning, INSERT-at-same-position recovery, and causal ordering across documents are appropriately parked in Open Questions rather than claimed.

VERDICT: REVISE
