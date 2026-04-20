**NAT-addcompat (NatAdditionOrderAndSuccessor).** Addition on ℕ is compatible with the order on either side, and `n < n + 1` for every `n ∈ ℕ`.

- Left order compatibility: `n ≥ p ⟹ m + n ≥ m + p` for every `m, n, p ∈ ℕ`.
- Right order compatibility: `n ≥ p ⟹ n + m ≥ p + m` for every `m, n, p ∈ ℕ`.
- Strict successor inequality: `n < n + 1` for every `n ∈ ℕ`.

*Formal Contract:*
- *Axiom:* `(A m, n, p ∈ ℕ : n ≥ p : m + n ≥ m + p)` (left order compatibility); `(A m, n, p ∈ ℕ : n ≥ p : n + m ≥ p + m)` (right order compatibility); `(A n ∈ ℕ :: n < n + 1)` (strict successor inequality).
