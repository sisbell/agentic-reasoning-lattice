**NAT-sub (NatPartialSubtraction).** Subtraction on ℕ is a partial binary operation: whenever `m, n ∈ ℕ` satisfy `m ≥ n`, the difference `m − n` is the unique natural number characterised by `(m − n) + n = m`.

The following facts about partial subtraction and its interaction with addition and order on ℕ are stated together:

- Conditional closure: `m ≥ n ⟹ m − n ∈ ℕ` for every `m, n ∈ ℕ`.
- Right-inverse characterisation: `m ≥ n ⟹ (m − n) + n = m` for every `m, n ∈ ℕ`.
- Left-inverse characterisation: `m ≥ n ⟹ n + (m − n) = m` for every `m, n ∈ ℕ`.
- Strict positivity: `m > n ⟹ m − n ≥ 1` for every `m, n ∈ ℕ`.
- Right telescoping: `(m + n) − n = m` for every `m, n ∈ ℕ`.
- Strict monotonicity: `m ≥ p ∧ n ≥ p ∧ m < n ⟹ m − p < n − p` for every `m, n, p ∈ ℕ`.

Both inverse forms are stated because citing either one without commutativity of addition would otherwise be tacit.

*Formal Contract:*
- *Axiom:* `(A m, n ∈ ℕ : m ≥ n : m − n ∈ ℕ)` (conditional closure); `(A m, n ∈ ℕ : m ≥ n : (m − n) + n = m)` (right-inverse characterisation); `(A m, n ∈ ℕ : m ≥ n : n + (m − n) = m)` (left-inverse characterisation); `(A m, n ∈ ℕ : m > n : m − n ≥ 1)` (strict positivity); `(A m, n ∈ ℕ :: (m + n) − n = m)` (right telescoping); `(A m, n, p ∈ ℕ : m ≥ p ∧ n ≥ p ∧ m < n : m − p < n − p)` (strict monotonicity).
