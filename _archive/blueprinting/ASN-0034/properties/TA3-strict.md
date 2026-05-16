**TA3-strict (OrderPreservationUnderSubtractionStrict).** `(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b : a ⊖ w < b ⊖ w)`.

We prove that subtracting a common lower bound from two equal-length tumblers preserves strict order: if `a` precedes `b`, both dominate `w`, and `#a = #b`, then `a ⊖ w` strictly precedes `b ⊖ w`.

*Proof.* We are given `a, b, w ∈ T` with `a < b`, `a ≥ w`, `b ≥ w`, and `#a = #b`. We must show `a ⊖ w < b ⊖ w`.

**Preliminaries.** We recall the definitions on which the argument depends. T1 defines `a < b` by: there exists a least `k ≥ 1` with `aᵢ = bᵢ` for all `i < k`, and either (i) `k ≤ min(#a, #b)` with `aₖ < bₖ`, or (ii) `k = #a + 1 ≤ #b` (`a` a proper prefix of `b`). TumblerSub defines `x ⊖ w` (for `x ≥ w`) by zero-padding both operands to length `max(#x, #w)` and scanning for the first position where the padded sequences disagree. If no disagreement exists (*zero-padded equality*), the result is the zero tumbler of length `max(#x, #w)`. If divergence occurs at position `d`, the result `r` satisfies: `rᵢ = 0` for `i < d`, `r_d = x_d - w_d`, and `rᵢ = xᵢ` for `i > d`, with `#r = max(#x, #w)`.

**The form of `a < b`.** Since `#a = #b`, T1 case (ii) is impossible — it requires `#a < #b`. So `a < b` holds by case (i): there exists a least `j` with `1 ≤ j ≤ #a` such that `aᵢ = bᵢ` for all `i < j` and `aⱼ < bⱼ`. We fix this `j` throughout.

**Well-formedness.** By TA2, both `a ⊖ w` and `b ⊖ w` are well-defined members of `T`.

We proceed by exhaustive case analysis on the divergence structure of the pairs `(a, w)` and `(b, w)` under zero-padding.

**Case A: `a` is zero-padded-equal to `w`.** By TumblerSub, `a ⊖ w` is the zero tumbler of length `max(#a, #w)`. For `i < j`: `b_i = a_i` (from T1) and `a_i = w_i` (zero-padded equality), so `b_i = w_i`. At position `j`: `w_j = a_j` (zero-padded equality) and `b_j > a_j` (from `a < b`), giving `b_j > w_j`. So `(b, w)` diverges at position `j`, and TumblerSub yields `(b ⊖ w)_j = b_j - w_j > 0`. Since `a ⊖ w` is a zero tumbler and `b ⊖ w` has a positive component, TA6 gives `a ⊖ w < b ⊖ w`.

**Setup for remaining cases.** Since `a` is not zero-padded-equal to `w`, the divergence `d_a = div(a, w)` is well-defined. Since `a ≥ w` and `a` is not zero-padded-equal to `w`, we have `a > w`, and T1 at the first zero-padded divergence gives `a_{d_a} > w_{d_a}`. We verify that `d_b = div(b, w)` also exists: if `b` were zero-padded-equal to `w`, then `b_{d_a} = w_{d_a} < a_{d_a}`, and since `b_i = w_i = a_i` for `i < d_a`, T1 gives `a > b` — contradicting `a < b`. So `d_b` is well-defined, with `b_{d_b} > w_{d_b}` by the same reasoning from `b > w`.

**Case 1: `d_a = d_b = d`.** Both pairs diverge from `w` at position `d`. By TumblerSub, `(a ⊖ w)_i = 0` and `(b ⊖ w)_i = 0` for all `i < d`. Since `a` and `b` both agree with `w` before `d`, they agree with each other, so `j ≥ d`.

*Subcase `j = d`:* `(a ⊖ w)_d = a_d - w_d` and `(b ⊖ w)_d = b_d - w_d`. From `j = d`: `a_d < b_d`. Since `a_d > w_d` and `b_d > w_d` (established in setup), both differences are positive and `a_d - w_d < b_d - w_d`. The results agree before `d` (both zero) and first disagree at `d`. By T1 case (i), `a ⊖ w < b ⊖ w`.

*Subcase `j > d`:* `a_d = b_d` (since `j > d`), so `(a ⊖ w)_d = a_d - w_d = b_d - w_d = (b ⊖ w)_d`. For `d < i < j`: both results are in TumblerSub's tail-copy phase, giving `(a ⊖ w)_i = a_i` and `(b ⊖ w)_i = b_i`; since `a_i = b_i` (`i < j`), the results agree. At position `j`: `(a ⊖ w)_j = a_j` and `(b ⊖ w)_j = b_j` (still tail-copy), with `a_j < b_j`. The results first disagree at `j`. By T1 case (i), `a ⊖ w < b ⊖ w`.

**Case 2: `d_a < d_b`.** At position `d_a`: `a_{d_a} ≠ w_{d_a}` but `b_{d_a} = w_{d_a}` (since `d_a < d_b`). Both agree with `w` — hence with each other — before `d_a`, and disagree at `d_a` (since `a_{d_a} ≠ w_{d_a} = b_{d_a}`), so `j = d_a`. From `a < b` by T1: `a_{d_a} < b_{d_a} = w_{d_a}`. But `a_{d_a} > w_{d_a}` (from setup) — contradiction. This case is impossible.

**Case 3: `d_a > d_b`.** At position `d_b`: `b_{d_b} ≠ w_{d_b}` but `a_{d_b} = w_{d_b}` (since `d_b < d_a`). Both agree with `w` — hence with each other — before `d_b`, and disagree at `d_b` (since `b_{d_b} ≠ w_{d_b} = a_{d_b}`), so `j = d_b`. From `a < b`: `a_{d_b} < b_{d_b}`, i.e., `w_{d_b} < b_{d_b}` — consistent with `b_{d_b} > w_{d_b}`.

For `a ⊖ w`: position `d_b` falls before `d_a`, placing it in the pre-divergence zero phase, so `(a ⊖ w)_{d_b} = 0`. For `b ⊖ w`: `d_b` is the divergence point, so `(b ⊖ w)_{d_b} = b_{d_b} - w_{d_b} > 0`. At all positions `i < d_b`, both results are zero (pre-divergence for both). The first disagreement is at `d_b` with `0 < b_{d_b} - w_{d_b}`. By T1 case (i), `a ⊖ w < b ⊖ w`.

In every case, `a ⊖ w < b ⊖ w` is established. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w, #a = #b
- *Postconditions:* a ⊖ w < b ⊖ w
