# Review of ASN-0093

## REVISE

### Issue 1: TA5(c)/TA5(d) cited for T4-preservation when TA5a is the foundation claim

**ASN-0093, C1c and L1c chain exhibitions (Discharge of stated invariants section), recurrent in worked example Steps 2, 4, and 8**:

The chain exhibitions repeatedly attribute T4-preservation to TA5(c) or TA5(d):

- C1c first-emit, t₁ = inc(d, 2): "TA5(d) at k = 2 yields zeros(t₁) = 2 + (2 − 1) = 3 and #t₁ = #d + 2, T4-valid."
- C1c first-emit, t₂ = inc(b_C(d), 1): "TA5(d) at k = 1 has no zero-count side condition; ... zeros(t₂) = 3 + 0 = 3 (k = 1 introduces no new zero), T4-valid"
- C1c subsequent-emit: "Per-step admissibility of the new step t_{n+1} = inc(a_prev, 0): TA5(c) at k = 0 is unconditionally T4-preserving"
- L1c first-emit, t₂ = inc(b_C(d), 0): "TA5(c) at k = 0 is unconditionally T4-preserving and length-preserving"
- L1c first-emit, t₃ = inc(b_L(d), 1): "TA5(d) at k = 1 has no zero-count side condition; zeros(t₃) = 3 + 0 = 3, T4-valid"
- L1c subsequent-emit: "Per-step admissibility of the new step t_{n+1} = inc(ℓ_prev, 0): TA5(c) at k = 0 is unconditionally T4-preserving"

**Problem**: TA5(c) is TA5's postcondition about length and value at sig position when k = 0 ("When k = 0: #t' = #t, t'_{sig(t)} = t_{sig(t)} + 1"). TA5(d) is the analogous postcondition for k > 0 (length extension and new-position structure). Neither claims T4-preservation. T4-preservation under inc is the content of TA5a (IncrementPreservesT4, ASN-0034): "inc(t, k) satisfies T4 iff k ∈ {0, 1}, or k = 2 ∧ zeros(t) ≤ 2." The ASN cites TA5a correctly in ChainElementT4Validity's proof ("TA5a (IncrementPreservesT4, ASN-0034) applies at k = 0 unconditionally"); the chain exhibitions should follow the same precision. Future readers consulting TA5(c) for the cited T4-preservation claim will find it doesn't say what's attributed to it.

**Required**: In each chain exhibition step, cite TA5a for T4-preservation (with the appropriate side condition `zeros(t) ≤ 2` cited from M0 at the k = 2 step), while continuing to cite TA5(c)/TA5(d) for structural form (length preservation, single-position modification, position of new components). The underlying T4-preservation does hold; only the citation chain is wrong.

### Issue 2: L14 matrix entry parenthetical incomplete for subsequent-emit case

**ASN-0093, L14 row of discharge matrix (K.α and K.λ columns)**:

"StoreT4Validity at a is discharged from ChainElementT4Validity applied to A_C(d) (whose first emission is T4-valid by FirstEmission)"

**Problem**: The parenthetical "(whose first emission is T4-valid by FirstEmission)" anchors ChainElementT4Validity's base case at the first emission. But the L14 discharge applies to both first-emit and subsequent-emit branches of K.α (resp. K.λ). For subsequent emissions, the new key is a later chain element on A_C(d) (resp. A_L(d)), not the first emission. ChainElementT4Validity holds for every chain element by chain induction regardless of position, so the conclusion still transfers — but the parenthetical's specific mention of "first emission" reads as if scoped to the first-emit branch only and is misleading for subsequent emissions.

**Required**: Rephrase the parenthetical to indicate ChainElementT4Validity holds for every chain element by chain induction (with FirstEmission grounding the base case). For example: "(every chain element is T4-valid by chain induction grounded at FirstEmission's T4-valid first emission)".

## OUT_OF_SCOPE

None.

VERDICT: REVISE
