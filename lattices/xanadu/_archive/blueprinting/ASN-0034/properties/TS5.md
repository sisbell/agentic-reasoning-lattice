**TS5 (ShiftAmountMonotonicity).**

`(A v, n₁, n₂ : n₁ ≥ 1 ∧ n₂ > n₁ ∧ #v = m : shift(v, n₁) < shift(v, n₂))`

*Proof.* We show that shifting a tumbler by a larger amount produces a strictly greater result: if n₂ exceeds n₁, then the shift by n₂ overshoots the shift by n₁.

Fix v ∈ T with #v = m, and fix n₁ ≥ 1 and n₂ > n₁. We must prove shift(v, n₁) < shift(v, n₂).

Define d = n₂ − n₁. Since n₂ > n₁ and both are natural numbers, d ≥ 1. And since n₁ ≥ 1, we have n₂ = n₁ + d with both n₁ ≥ 1 and d ≥ 1.

We invoke TS3 (ShiftComposition), which states that for any tumbler u with #u = m and any pair of positive shifts a ≥ 1, b ≥ 1: shift(shift(u, a), b) = shift(u, a + b). Here u = v, a = n₁, b = d. The preconditions are n₁ ≥ 1 (given) and d ≥ 1 (established above), both satisfied. Therefore shift(shift(v, n₁), d) = shift(v, n₁ + d) = shift(v, n₂). This expresses the larger shift as a composition: first shift by n₁, then shift the result by d.

Let u = shift(v, n₁). By OrdinalShift, u is a tumbler with #u = m (shift preserves length). Then shift(v, n₂) = shift(u, d). We invoke TS4 (ShiftStrictIncrease), which states that for any tumbler u with #u = m and any n ≥ 1: shift(u, n) > u. Here u = shift(v, n₁) and n = d. The preconditions are d ≥ 1 (established above) and #u = m (just noted), both satisfied. Therefore shift(u, d) > u.

Substituting back: shift(v, n₂) = shift(u, d) > u = shift(v, n₁), that is, shift(v, n₁) < shift(v, n₂). ∎

*Worked example.* Let v = [2, 3, 7] (m = 3) and n = 4. Then δ(4, 3) = [0, 0, 4] with action point 3. TA0: k = 3 ≤ 3 = #v. By TumblerAdd: shift(v, 4) = [2, 3, 7 + 4] = [2, 3, 11].

For TS1: take v₁ = [2, 3, 5] < v₂ = [2, 3, 9] with n = 4. Then shift(v₁, 4) = [2, 3, 9] < [2, 3, 13] = shift(v₂, 4). ✓

For TS3: shift(shift([2, 3, 7], 4), 3) = shift([2, 3, 11], 3) = [2, 3, 14] = shift([2, 3, 7], 7). ✓

*Formal Contract:*
- *Preconditions:* v ∈ T, n₁ ≥ 1, n₂ > n₁, #v = m
- *Postconditions:* shift(v, n₁) < shift(v, n₂)
