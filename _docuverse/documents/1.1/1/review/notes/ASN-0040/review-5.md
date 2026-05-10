# Review of ASN-0040

## REVISE

### Issue 1: T4 registry-wide induction omits the sibling case

**ASN-0040, The contiguous prefix property**: "For the inductive step, any baptism(p, d) satisfying B6 has p satisfying T4 (condition (i)), and IncrementPreservesValidity (ASN-0034) gives that inc(p, d) satisfies T4 when d ∈ {1, 2} and zeros(p) + (d − 1) ≤ 3 (conditions (ii) and (iii)). This closes the chain"

**Problem**: The inductive step handles only the first-child case where hwm = 0 and the baptized element is c₁ = inc(p, d). When hwm = m > 0, baptism produces c_{m+1} = inc(c_m, 0) — a sibling increment with k = 0. The T4 input for this case is c_m (the previous sibling), not p (the parent). The proof never shows this case. The fact that IncrementPreservesValidity with k = 0 preserves T4 unconditionally makes the fix trivial, but the induction has two structurally distinct cases and only one is shown.

**Required**: Distinguish the two cases in the inductive step:
- hwm = 0: output is inc(p, d). p satisfies T4 by B6(i). IncrementPreservesValidity with k = d ∈ {1, 2} and zeros(p) + (d − 1) ≤ 3 gives T4.
- hwm > 0: output is inc(c_{hwm}, 0). c_{hwm} satisfies T4 by the inductive hypothesis (it was previously baptized). IncrementPreservesValidity with k = 0 gives T4 unconditionally.

## OUT_OF_SCOPE

(none)

VERDICT: REVISE
