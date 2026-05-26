# Review of ASN-0075

## REVISE

### Issue 1: shift(·, 0) is not defined by ASN-0034's OrdinalShift

**ASN-0075, §D-ACT, "T1-minimum coincides with index-minimum" paragraph**: "So `C = {shift(min(C), 0), shift(min(C), 1), …, shift(min(C), |C| − 1)}` — exactly the address set the inverse reconstructs from the witness run `(min(C), |C|, d)`."

**Problem**: ASN-0034's OrdinalShift has precondition `n ≥ 1`, so `shift(min(C), 0)` is not formally defined by the foundation. The intent (`shift(t, 0) = t`) matches ASN-0058's OrdinalShiftBase convention, but OrdinalShiftBase extends only the `+` notation to `k = 0`, not the `shift(·, ·)` notation that ASN-0075 uses throughout. Elsewhere in the very same section, the inverse reconstruction is written as `{i_start, shift(i_start, 1), …, shift(i_start, ℓ − 1)}` and explicitly notes "(which is `{i_start}` when `ℓ = 1`)" — avoiding `shift(·, 0)` by listing `i_start` directly. The two formulations should be consistent.

**Required**: Either rewrite the offending line as `C = {min(C), shift(min(C), 1), …, shift(min(C), |C| − 1)}` to match the inverse-reconstruction form already used, or invoke ASN-0058's OrdinalShiftBase explicitly with a note extending the identity-case convention from `+ 0` to `shift(·, 0)`.

### Issue 2: Distinctness of shifts justified by an incomplete citation

**ASN-0075, §D-ACT, inverse-then-forward verification paragraph**: "The set is `{i_start, shift(i_start, 1), …, shift(i_start, ℓ−1)}`. min is `i_start` (since shift increases under T1 monotonically — TA-strict). `|set| = ℓ` since shifts are distinct."

**Problem**: The "shifts are distinct" claim requires `shift(i_start, k₁) ≠ shift(i_start, k₂)` for `0 ≤ k₁ < k₂ < ℓ`. This is exactly TS5 (ShiftAmountMonotonicity, ASN-0034) — `shift(v, n₁) < shift(v, n₂)` for `n₁ < n₂`. The ASN cites only TA-strict (StrictIncrease), which gives `shift(t, n) > t` for `n ≥ 1` but does not directly establish strict ordering among shifts at *different* amounts (only between the original and any shifted result). The cardinality conclusion `|set| = ℓ` is left without an explicit foundation citation closing this gap.

**Required**: Cite TS5 explicitly for the distinctness, or derive it from TS3 (ShiftComposition) + TA-strict in one step: `shift(i_start, k₂) = shift(shift(i_start, k₁), k₂ − k₁) > shift(i_start, k₁)`.

## OUT_OF_SCOPE

None.

VERDICT: REVISE
