# Review of ASN-0076

## REVISE

### Issue 1: Numerical error in element-level address minimum length

**ASN-0076, §E0 (proof, supersession step, L3 discharge)**: "*For `E_from`:* `#ℓ_old ≥ 1` by T0 (every tumbler in T has length ≥ 1, ASN-0034); concretely `#ℓ_old ≥ 6` since `ℓ_old` is element-level with `#E ≥ 2` (L1, L1b). *For `E_to`:* `#ℓ_new ≥ 1` by T0; concretely `#ℓ_new ≥ 6` for the same reason."

**Problem**: The "concretely ≥ 6" bound is incorrect in both places. An element-level address has `zeros = 3` (L1), giving four fields (N, U, D, E) separated by three zeros. By T4's field-segment constraint, each of N, U, D has at least one component; by L1b, E has at least two. Minimum total: 3 (separators) + 1 + 1 + 1 (N, U, D) + 2 (E) = 8, not 6. The worked example's own `ℓ_old = [3.0.5.0.7.0.2.1]` exhibits the minimum and has length 8.

**Required**: Correct to ≥ 8 in both places, or drop the parentheticals entirely — the proof only needs the `≥ 1` from T0 to discharge T12.

### Issue 2: E0 supersession step elides the max-recovery argument

**ASN-0076, §E0 (proof, supersession step)**: "Since `inc(·, 0)` strictly increases its argument by TA5(a), `ℓ_new` is the maximum of `A_L(d_new)`'s outputs in `dom(Σ_1.L)`, so the rule fixes `ℓ_sup = inc(ℓ_new, 0)`."

**Problem**: When step 1 was a subsequent-emission, identifying `ℓ_new` as the new maximum requires showing `ℓ_new > ℓ'` for *every* prior output `ℓ'` of `A_L(d_new)`, not just the immediate predecessor `prev_max`. TA5(a) supplies only the per-step inequality `ℓ_new > prev_max`. Lifting this to all prior outputs requires either T1 transitivity together with the prior-state max characterization, or a direct appeal to T10a.7 (EnumerationInjectivity), which already supplies strict monotonicity of the full enumeration. As written, the one-sentence citation is incomplete for the case it must cover.

**Required**: Either split the supersession-step discharge into the same first-emission / subsequent-emission sub-cases used for step 1, or replace the TA5(a) citation with T10a.7 (which discharges the strict-monotonicity-of-the-enumeration claim in one citation).

## OUT_OF_SCOPE

None. The ASN's own Open Questions section appropriately defers downstream topics (supersession chains and cycles, retraction semantics, multi-link supersessions, the `τ_sup` type-convention itself, discovery operations against `covers(Σ, ·)`, and content-link interaction during edits).

VERDICT: REVISE
