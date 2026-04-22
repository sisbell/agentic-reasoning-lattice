**NAT-discrete (NatDiscreteness).** For every `m, n ∈ ℕ`, `m < n ⟹ m + 1 ≤ n`; equivalently, `m ≤ n < m + 1 ⟹ n = m`.

No natural number lies strictly between `n` and its successor `n + 1`: whenever `m < n`, the successor `m + 1` is already bounded above by `n`, so `m + 1 ≤ n`. This is the discreteness of ℕ.

*Formal Contract:*
- *Axiom:* `(A m, n ∈ ℕ :: m < n ⟹ m + 1 ≤ n)`; equivalently `(A m, n ∈ ℕ :: m ≤ n < m + 1 ⟹ n = m)` (discreteness).
