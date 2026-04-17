**NAT-addcompat (NatAdditionOrderCompatibility).** Addition on ℕ is compatible with the order, and `n < n + 1` for every `n ∈ ℕ`.

Two related facts are stated together as one axiom because they are both about the interaction between addition and `<` on ℕ:

- Order compatibility: `n ≥ p ⟹ m + n ≥ m + p` for every `m, n, p ∈ ℕ`. Adding the same natural number to both sides preserves the order.
- Strict successor inequality: `n < n + 1` for every `n ∈ ℕ`. The successor is strictly greater.

Downstream proofs use the first fact to lift inequalities through arithmetic and the second to bound lengths or indices under incrementing operations.

*Formal Contract:*
- *Axiom:* `(A m, n, p ∈ ℕ : n ≥ p : m + n ≥ m + p)` (order-compatibility of addition); `(A n ∈ ℕ :: n < n + 1)` (strict successor inequality).
