# Review of ASN-0053

## REVISE

### Issue 1: S9's Case 1 / Case 3 edge case handling is bundled and informal
**ASN-0053, S9 (NormalizationUniqueness)**: "Let i be the smallest index where αᵢ ≠ βᵢ (if one sequence is shorter, take i past the shorter one's end)." Case 1 then states "start(αᵢ) < start(βᵢ) (or βᵢ does not exist)"; Case 3 says only "Symmetric to Case 1."
**Problem**: Case 1 explicitly conditions "for j ≥ i (only possible when βᵢ exists)", which is good — but Case 3's symmetric edge case (where αᵢ doesn't exist because Σ̂₁ is the shorter sequence) is left entirely to the reader. Under strict reading, a proof of uniqueness must not silently delegate one of its sub-cases to "symmetric." The case structure also conflates two distinct shapes: (a) both αᵢ and βᵢ exist with start(αᵢ) < start(βᵢ), and (b) αᵢ exists but βᵢ does not.
**Required**: Split Case 1 into Case 1a (both exist) and Case 1b (αᵢ exists, βᵢ does not — the "for j ≥ i" range is vacuous). Spell out Case 3's symmetric structure explicitly (Case 3a, Case 3b), so a reader can verify both edge cases without re-deriving them.

### Issue 2: S6's intermediate length formula is redundant
**ASN-0053, S6 (LevelConstraint)**: "since the action point k satisfies 1 ≤ k ≤ #s = #ℓ, we have #(s ⊕ ℓ) = max(k − 1, 0) + (#ℓ − k + 1) = #ℓ = #s."
**Problem**: TA0 (WellDefinedAddition) supplies #(a ⊕ w) = #w directly. Combined with level-uniformity #s = #ℓ, the result #(s ⊕ ℓ) = #s follows in one step. The same paragraph already states this cleanly two sentences earlier ("#(s ⊕ ℓ) = #ℓ = #s by the result-length identity"). The max(k − 1, 0) + (#ℓ − k + 1) formula recomputes by summing region sizes — adding clutter and inviting an unnecessary case split on max — when a direct citation of TA0 already settles the matter.
**Required**: Remove the intermediate formula. The earlier TA0 citation suffices.

### Issue 3: S5's "three conditions" framing conflates TA-assoc preconditions with TA0 well-definedness obligations
**ASN-0053, S5 (SplitWidthComposition)**: "For the right side s ⊕ (d ⊕ d'), three conditions need verification: (a) d ⊕ d' is positive, and its action point is m = min(k_d, k_{d'}); (b) The action point of d ⊕ d' is at most #s; (c) The action point of d' falls within #d."
**Problem**: (a) and (b) are postconditions of TA-assoc (Pos(b ⊕ c), action-point identification) and conditions for TA0 on s ⊕ (d ⊕ d'); (c) is a precondition of TA-assoc (k_c ≤ #b). The proof bundles them as "three conditions for the right side", obscuring the role of each. The case analysis re-derives (a) and (b) independently when TA-assoc would already deliver them as postconditions under its preconditions. A reader cannot tell whether the case analysis is necessary for the proof to close, or whether it parallels TA-assoc's guaranteed output.
**Required**: Restructure: (i) verify TA-assoc's preconditions Pos(d), Pos(d'), k_d ≤ #s, k_{d'} ≤ #d; (ii) cite TA-assoc to obtain associativity, Pos(d ⊕ d'), and actionPoint(d ⊕ d') = min(k_d, k_{d'}); (iii) discharge TA-LC's preconditions and apply. Keep the case analysis as a parallel direct derivation if it serves clarity, but flag it as such rather than presenting it as the load-bearing step.

VERDICT: REVISE
