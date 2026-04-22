**NAT-order (NatStrictTotalOrder).** The binary relation `<` on ℕ is a strict total order, with non-strict companion `≤` defined by `m ≤ n ⟺ m < n ∨ m = n`.

Strict total order on ℕ means three properties hold jointly:
- Irreflexivity: `¬(n < n)` for every `n ∈ ℕ`
- Transitivity: `m < n ∧ n < p ⟹ m < p` for every `m, n, p ∈ ℕ`
- Trichotomy: for any `m, n ∈ ℕ`, exactly one of `m < n`, `m = n`, `n < m` holds

*Formal Contract:*
- *Axiom:* `(A n ∈ ℕ :: ¬(n < n))` (irreflexivity); `(A m, n, p ∈ ℕ : m < n ∧ n < p : m < p)` (transitivity); `(A m, n ∈ ℕ :: (m < n ∧ ¬(m = n) ∧ ¬(n < m)) ∨ (¬(m < n) ∧ m = n ∧ ¬(n < m)) ∨ (¬(m < n) ∧ ¬(m = n) ∧ n < m))` (trichotomy). The non-strict relation `≤` on ℕ is defined by `m ≤ n ⟺ m < n ∨ m = n`.
- *Depends:* (none). NAT-order is the root of the NAT foundation: the strict-order primitive `<` is posited directly on ℕ, not derived from an earlier axiom, and the non-strict companion `≤` is defined using only `<` and logical equality.
