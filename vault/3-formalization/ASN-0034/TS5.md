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
- *Depends:* TS3 (ShiftComposition) — invoked at the proof's first reduction to express the larger shift as a composition ("We invoke TS3 (ShiftComposition), which states that for any tumbler u with #u = m and any pair of positive shifts a ≥ 1, b ≥ 1: shift(shift(u, a), b) = shift(u, a + b). [...] Therefore shift(shift(v, n₁), d) = shift(v, n₁ + d) = shift(v, n₂)"); without TS3 the rewrite of `shift(v, n₂)` as `shift(shift(v, n₁), d)` could not be performed. OrdinalShift (OrdinalShift) — invoked between the TS3 and TS4 calls to license `#u = m` for `u = shift(v, n₁)` ("By OrdinalShift, u is a tumbler with #u = m (shift preserves length)"); TS4's precondition `#u = m` depends on this length-preservation fact. TS4 (ShiftStrictIncrease) — invoked at the second reduction to convert the d-shift of `u` into a strict increase ("We invoke TS4 (ShiftStrictIncrease), which states that for any tumbler u with #u = m and any n ≥ 1: shift(u, n) > u. [...] Therefore shift(u, d) > u"); the substitution `shift(v, n₂) = shift(u, d) > u = shift(v, n₁)` collapses the two-step reduction into the desired strict ordering. NAT-sub (NatPartialSubtraction) — invoked at the opening sentences "Define d = n₂ − n₁. Since n₂ > n₁ and both are natural numbers, d ≥ 1. And since n₁ ≥ 1, we have n₂ = n₁ + d" at three sites: conditional closure (`m ≥ n ⟹ m − n ∈ ℕ`) discharges `d = n₂ − n₁ ∈ ℕ` under the precondition `n₂ ≥ n₁` (supplied from `n₂ > n₁` via NAT-order), strict positivity (`m > n ⟹ m − n ≥ 1`) discharges `d ≥ 1` directly from the hypothesis `n₂ > n₁`, and left-inverse characterisation (`n + (m − n) = m`) discharges the rewrite `n₂ = n₁ + d` that TS3's instantiation `b = d` requires; without NAT-sub these three steps would appeal to background ℕ arithmetic, contrary to T0's convention that proofs cite only the ℕ facts they use. NAT-order (NatStrictTotalOrder) — invoked at the same opening sentence to convert the strict inequality `n₂ > n₁` (the precondition) into the weak `n₂ ≥ n₁` required by NAT-sub's conditional-closure clause (via the definition of `≤` from `<`); without NAT-order the precondition for NAT-sub's conditional closure would not be discharged from the hypothesis.
- *Postconditions:* shift(v, n₁) < shift(v, n₂)
