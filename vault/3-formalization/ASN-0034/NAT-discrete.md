**NAT-discrete (NatDiscreteness).** For every `m, n ∈ ℕ`, `m ≤ n < m + 1 ⟹ n = m`.

In words: no natural number lies strictly between `n` and its successor `n + 1`. This is the discreteness of ℕ — an independent axiom, not derivable from strict total order alone (ℤ with the usual `<` is totally ordered and discrete, ℝ is totally ordered but not discrete).

Downstream proofs cite NAT-discrete when converting a strict inequality `k > 0` into `k ≥ 1`, or when showing that a nonzero natural number is at least 1, or when arguing that an interval `[m, m+1)` in ℕ contains only the point `m`.

*Formal Contract:*
- *Axiom:* `(A m, n ∈ ℕ :: m ≤ n < m + 1 ⟹ n = m)` (discreteness).
