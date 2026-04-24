**NAT-addcompat (NatAdditionOrderAndSuccessor).** Addition on ℕ is compatible with the order on either side, and `n < n + 1` for every `n ∈ ℕ`.

- Left order compatibility: `p ≤ n ⟹ m + p ≤ m + n` for every `m, n, p ∈ ℕ`.
- Right order compatibility: `p ≤ n ⟹ p + m ≤ n + m` for every `m, n, p ∈ ℕ`.
- Strict successor inequality: `n < n + 1` for every `n ∈ ℕ`.

*Formal Contract:*
- *Axiom:* `(A m, n, p ∈ ℕ : p ≤ n : m + p ≤ m + n)` (left order compatibility); `(A m, n, p ∈ ℕ : p ≤ n : p + m ≤ n + m)` (right order compatibility); `(A n ∈ ℕ :: n < n + 1)` (strict successor inequality).
- *Depends:*
  - NAT-order (NatStrictTotalOrder) — supplies the primitive strict order `<` (used in the strict successor inequality `n < n + 1`) and its non-strict companion `≤` (defined by `m ≤ n ⟺ m < n ∨ m = n`, used in the antecedents `p ≤ n` and the consequents `m + p ≤ m + n` and `p + m ≤ n + m` of both compatibility clauses).
  - NAT-closure (NatArithmeticClosureAndIdentity) — posits `1 ∈ ℕ` and closes ℕ under addition, so every sum `m + p`, `m + n`, `p + m`, `n + m`, and `n + 1` appearing in the axiom lies in ℕ, and the successor inequality `n < n + 1` compares two ℕ-elements.
