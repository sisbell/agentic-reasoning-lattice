**NAT-addcompat (NatAdditionOrderAndSuccessor).** Addition on ℕ is compatible with the order on either side, and `n < n + 1` for every `n ∈ ℕ`.

- Left order compatibility: `p ≤ n ⟹ m + p ≤ m + n` for every `m, n, p ∈ ℕ`.
- Right order compatibility: `p ≤ n ⟹ p + m ≤ n + m` for every `m, n, p ∈ ℕ`.
- Strict successor inequality: `n < n + 1` for every `n ∈ ℕ`.

*Formal Contract:*
- *Axiom:* `(A m, n, p ∈ ℕ : p ≤ n : m + p ≤ m + n)` (left order compatibility); `(A m, n, p ∈ ℕ : p ≤ n : p + m ≤ n + m)` (right order compatibility); `(A n ∈ ℕ :: n < n + 1)` (strict successor inequality).
