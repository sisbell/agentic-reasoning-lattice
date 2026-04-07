# Review of ASN-0053

## REVISE

### Issue 1: D0/D1 — unproven informal claim and garbled prose
**ASN-0053, "The reach function"**: "It does not guarantee round-trip faithfulness — the identity a ⊕ (b ⊖ a) = b additionally requires #a ≤ #b, since TumblerSubtract produces a result of length max(#a, #b), which differs from b ⊖ a when #a > #b."

**Problem**: Two issues in one passage.

(a) The sentence "which differs from b ⊖ a when #a > #b" is garbled — the result of TumblerSubtract *is* b ⊖ a, so the sentence compares a quantity with itself. The intended meaning (the round-trip a ⊕ (b ⊖ a) yields a tumbler of length max(#a, #b) ≠ #b, so it cannot equal b by T3) is correct but not what the sentence says.

(b) The text claims "#a ≤ #b" suffices for the round-trip, but D1 is stated and proven only for #a = #b. The #a < #b case is true (the proof generalizes straightforwardly: when a < b with type (i) divergence at k ≤ #a < #b, TumblerSubtract produces w of length #b, and TumblerAdd yields a result matching b component-wise at length #b). But the ASN does not prove it. By standard 6, a claim requiring a multi-step argument must show the steps.

Since every subsequent result uses level-uniform spans (#s = #ℓ, hence #start = #reach), the missing case has no downstream impact. But the prose makes a promise the formal development does not keep.

**Required**: Either (i) strengthen D1 to cover #a ≤ #b with an explicit proof for the #a < #b sub-case, or (ii) change the prose to say "additionally requires #a = #b" (matching what D1 actually proves) and note that the #a < #b case, while true, is not needed here. Either way, rewrite the garbled sentence — e.g., "since TumblerSubtract produces a displacement of length max(#a, #b), the round-trip a ⊕ (b ⊖ a) yields a tumbler of length max(#a, #b); when #a > #b, this length exceeds #b, so the result cannot equal b (by T3)."

### Issue 2: S3 — no concrete example for merge
**ASN-0053, S3 (MergeEquivalence)**: The proof is correct and complete, but no concrete example verifies the merge postcondition against a specific scenario. S1 (intersection) and S4/S5 (split + width composition) both include worked numerical examples. S3 is equally fundamental — normalization (S8) depends on it — and warrants the same treatment.

**Problem**: The review standard requires key postconditions to be verified against at least one concrete scenario. Merge is a key operation. The proof constructs γ = (s, r ⊖ s) and argues about denotations, but never instantiates the construction with actual tumblers.

**Required**: Add a concrete merge example. The spans from S1's example serve directly: α = ([1, 3], [0, 4]) and β = ([1, 5], [0, 6]) overlap (reach(α) = [1, 7] > start(β) = [1, 5]). The merge is γ = ([1, 3], [1, 11] ⊖ [1, 3]) = ([1, 3], [0, 8]) with reach [1, 11]. Verify: ⟦α⟧ ∪ ⟦β⟧ = {t : [1,3] ≤ t < [1,7]} ∪ {t : [1,5] ≤ t < [1,11]} = {t : [1,3] ≤ t < [1,11]} = ⟦γ⟧.

## OUT_OF_SCOPE

### Topic 1: General span-set difference
S11 handles set difference only for the containment case (⟦β⟧ ⊆ ⟦α⟧). The general case — given normalized span-sets Σ₁ and Σ₂, compute normalize(⟦Σ₁⟧ \ ⟦Σ₂⟧) — is a natural extension needed for operations like "all positions in this designation but not in that one." The bound on the result size (at most |Σ₁| + |Σ₂| spans before normalization) and the sweep-line construction generalize straightforwardly from S8 and S11, but this belongs in a future ASN.

**Why out of scope**: This is new territory — S11 establishes the primitive (two-span containment difference), and the general case builds on it with additional machinery.

VERDICT: REVISE
