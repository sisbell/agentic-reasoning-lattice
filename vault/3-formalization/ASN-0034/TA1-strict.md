**TA1-strict (StrictOrderPreservation).** `(A a, b, w : a < b ∧ Pos(w) ∧ actionPoint(w) ≤ min(#a, #b) ∧ actionPoint(w) ≥ divergence(a, b) : a ⊕ w < b ⊕ w)`.

When the action point falls before the divergence — `k < divergence(a, b)` — both operands agree at position `k`, both get the same `wₖ` added, and both copy the same tail from `w` afterward. The original divergence is erased and the results are equal. For example, `a = [1, 3]`, `b = [1, 5]` (diverge at position 2), `w = [2]` (action point at position 1): `a ⊕ w = [3] = b ⊕ w`. Order degrades to equality, never reversal.

*Proof.* We show that tumbler addition by `w` preserves the strict inequality `a < b` whenever the action point of `w` falls at or beyond the first disagreement between `a` and `b`.

Let `j = divergence(a, b)` and let `k` be the action point of `w`. The preconditions give `k ≥ j` and `k ≤ min(#a, #b)`. From these bounds, `j ≤ min(#a, #b)`, which rules out Divergence case (ii) — prefix divergence requires `j = min(#a, #b) + 1` — and places us in case (i): position `j` is shared by both tumblers, `aⱼ ≠ bⱼ`, and `aᵢ = bᵢ` for all `i < j`. Since `a < b`, the T1 case (i) direction gives `aⱼ < bⱼ`.

Recall TumblerAdd's constructive definition: for any tumbler `x` and positive displacement `w` with action point `k ≤ #x`, the result `x ⊕ w` is built component-wise as `(x ⊕ w)ᵢ = xᵢ` for `i < k` (prefix copy), `(x ⊕ w)ₖ = xₖ + wₖ` (single-component advance), and `(x ⊕ w)ᵢ = wᵢ` for `i > k` (tail from displacement). By TA0, both `a ⊕ w` and `b ⊕ w` are well-defined members of T, since `k ≤ min(#a, #b)` ensures the action point falls within both operands. Two cases arise from the relationship between `k` and `j`.

*Case 1: `k = j`.* For `i < k`: since `i < j`, the Divergence agreement property gives `aᵢ = bᵢ`, and TumblerAdd's prefix-copy rule gives `(a ⊕ w)ᵢ = aᵢ = bᵢ = (b ⊕ w)ᵢ`. At position `k = j`: TumblerAdd gives `(a ⊕ w)ₖ = aₖ + wₖ` and `(b ⊕ w)ₖ = bₖ + wₖ`. Since `aₖ < bₖ` (the divergence inequality) and natural-number addition preserves strict inequality, `aₖ + wₖ < bₖ + wₖ`. The results agree on all positions before `k` and diverge strictly at `k`. By T1 case (i), `a ⊕ w < b ⊕ w`.

*Case 2: `k > j`.* For `i < k`: TumblerAdd's prefix-copy rule gives `(a ⊕ w)ᵢ = aᵢ` and `(b ⊕ w)ᵢ = bᵢ`. Since `j < k`, position `j` lies in this prefix-copy region: `(a ⊕ w)ⱼ = aⱼ < bⱼ = (b ⊕ w)ⱼ` (the divergence inequality is preserved). For `i < j`: the Divergence agreement property gives `aᵢ = bᵢ`, so `(a ⊕ w)ᵢ = aᵢ = bᵢ = (b ⊕ w)ᵢ`. The original divergence at position `j` survives intact in the results — the action point, being deeper, does not touch positions at or above `j`. By T1 case (i), `a ⊕ w < b ⊕ w`.

In both cases, `a ⊕ w < b ⊕ w`. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, Pos(w), actionPoint(w) ≤ min(#a, #b), actionPoint(w) ≥ divergence(a, b)
- *Postconditions:* a ⊕ w < b ⊕ w

But TA1 alone does not guarantee that addition *advances* a position. It preserves relative order between two positions but is silent about the relationship between `a` and `a ⊕ w`. We need:
