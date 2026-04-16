**TS4 (ShiftStrictIncrease).**

`(A v, n : n ≥ 1 ∧ #v = m : shift(v, n) > v)`

*Proof.* We show that every ordinal shift by a positive amount produces a result strictly greater than the original tumbler.

Fix v ∈ T with #v = m, and fix n ≥ 1. By OrdinalShift, shift(v, n) = v ⊕ δ(n, m), so we must show v ⊕ δ(n, m) > v.

We apply TA-strict (Strict increase) with start position a = v and displacement w = δ(n, m). TA-strict requires two preconditions: Pos(w), and actionPoint(w) ≤ #a. We verify each.

*First precondition: Pos(δ(n, m)).* By OrdinalDisplacement, δ(n, m) = [0, ..., 0, n] of length m, with n at position m. Since n ≥ 1, component m is positive, so δ(n, m) is not the zero tumbler — that is, Pos(δ(n, m)).

*Second precondition: actionPoint(δ(n, m)) ≤ #v.* By OrdinalDisplacement, the action point of δ(n, m) is m (position m is the first nonzero component, since positions 1 through m − 1 are zero and position m is n ≥ 1). Since #v = m, the precondition m ≤ m holds.

Both preconditions are satisfied. By TA-strict: v ⊕ δ(n, m) > v, that is, shift(v, n) > v. ∎

*Formal Contract:*
- *Preconditions:* v ∈ T, n ≥ 1, #v = m
- *Postconditions:* shift(v, n) > v
