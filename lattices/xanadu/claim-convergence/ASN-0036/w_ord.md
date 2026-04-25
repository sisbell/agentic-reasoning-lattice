**w_ord** — *OrdinalDisplacementProjection* (DEF, function). For a displacement w with `w₁ = 0` and `#w = m ≥ 2`, the *ordinal projection* is:

`w_ord = [w₂, ..., wₘ]`

of length m − 1. We verify that this construction is well-formed and that its postconditions hold.

The sequence `[w₂, ..., wₘ]` has m − 1 components. Since m ≥ 2, m − 1 ≥ 1, so `w_ord` is a non-empty finite sequence of natural numbers; by T0, `w_ord ∈ T`, and `#w_ord = m − 1 = #w − 1`.

Suppose `w > 0`. Since `w₁ = 0`, positivity of w requires some `wⱼ > 0` with `2 ≤ j ≤ m`. That component appears in `w_ord` at position `j − 1`, so `w_ord > 0`.

For the action point: when `w > 0`, `actionPoint(w)` is the least index i with `wᵢ > 0`. Since `w₁ = 0`, we have `actionPoint(w) ≥ 2`. In `w_ord`, position k holds `w_{k+1}`. For any `k < actionPoint(w) − 1`, we have `k + 1 < actionPoint(w)`, so `w_{k+1} = 0` by minimality of `actionPoint(w)`, giving `(w_ord)_k = 0`. At `k = actionPoint(w) − 1`, we have `(w_ord)_k = w_{actionPoint(w)} > 0`. Hence `actionPoint(w_ord) = actionPoint(w) − 1`.

The condition `w₁ = 0` is structurally necessary: it ensures `actionPoint(w) ≥ 2`, so by TumblerAdd all positions before the action point are copied from the operand — position 1 (the subspace identifier) is preserved by any addition `v ⊕ w`. This is the mechanism by which arithmetic stays within a subspace. At the restricted depth m = 2, w = [0, c] for positive integer c, and w_ord = [c]. ∎

*Formal Contract:*
- *Preconditions:* `w ∈ T`, `#w ≥ 2`, `w₁ = 0`.
- *Definition:* `w_ord = [w₂, ..., wₘ]` where `m = #w`.
- *Postconditions:* `w_ord ∈ T` (length `m - 1 ≥ 1`, satisfying T0). `#w_ord = #w - 1`. When `w > 0`, `w_ord > 0` — since `w₁ = 0`, positivity of `w` requires some `wᵢ > 0` with `i ≥ 2`, which appears in `w_ord`. When `w > 0`: `actionPoint(w_ord) = actionPoint(w) - 1`.
- *Frame:* Pure function on the component sequence of `w` — no state is read or modified.
