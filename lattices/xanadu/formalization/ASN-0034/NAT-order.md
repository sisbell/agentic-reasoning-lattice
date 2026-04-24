**NAT-order (NatStrictTotalOrder).** The binary relation `<` on ℕ is a strict total order, with non-strict companion `≤` defined by `m ≤ n ⟺ m < n ∨ m = n` and reverse companions `≥` and `>` defined by `m ≥ n ⟺ n ≤ m` and `m > n ⟺ n < m`.

Strict total order on ℕ means three clauses hold jointly:
- Irreflexivity: `¬(n < n)` for every `n ∈ ℕ`
- Transitivity: `m < n ∧ n < p ⟹ m < p` for every `m, n, p ∈ ℕ`
- At-least-one trichotomy: for any `m, n ∈ ℕ`, at least one of `m < n`, `m = n`, `n < m` holds

Together the three clauses yield *exactly-one trichotomy*: for any `m, n ∈ ℕ`, exactly one of `m < n`, `m = n`, `n < m` holds. Exactly-one is the at-least-one disjunction conjoined with three pairwise mutual-exclusion clauses. `¬(m < n ∧ n < m)` follows from transitivity — which chains `m < n` and `n < m` to `m < m` — against irreflexivity. `¬(m < n ∧ m = n)` follows by substituting `m = n` into `m < n` via indiscernibility of `=`, rewriting to `m < m`, which irreflexivity at `n := m` rules out. `¬(m = n ∧ n < m)` follows by the same substitution applied to `n < m`: rewriting under `m = n` yields `m < m`, again against irreflexivity. The familiar implicational form `m < n ⟹ m ≠ n` is the mutual-exclusion conjunct `¬(m < n ∧ m = n)` rewritten by the classical equivalence `¬(A ∧ B) ⟺ (A ⟹ ¬B)`.

*Formal Contract:*
- *Axiom:* `< ⊆ ℕ × ℕ` (`<` is a binary relation on ℕ); `(A n ∈ ℕ :: ¬(n < n))` (irreflexivity); `(A m, n, p ∈ ℕ : m < n ∧ n < p : m < p)` (transitivity); `(A m, n ∈ ℕ :: m < n ∨ m = n ∨ n < m)` (at-least-one trichotomy).
- *Consequence:* Exactly-one trichotomy: `(A m, n ∈ ℕ :: (m < n ∨ m = n ∨ n < m) ∧ ¬(m < n ∧ n < m) ∧ ¬(m < n ∧ m = n) ∧ ¬(m = n ∧ n < m))`. The disjunction is the at-least-one axiom clause directly; `¬(m < n ∧ n < m)` follows from transitivity and irreflexivity; `¬(m < n ∧ m = n)` follows by substituting `m = n` into `m < n` via indiscernibility of `=`, rewriting to `m < m` against irreflexivity at `n := m`; `¬(m = n ∧ n < m)` follows by the same substitution applied to `n < m`.
- *Definition:* `(A m, n ∈ ℕ :: m ≤ n ⟺ m < n ∨ m = n)`; `(A m, n ∈ ℕ :: m ≥ n ⟺ n ≤ m)`; `(A m, n ∈ ℕ :: m > n ⟺ n < m)`.
- *Depends:* (none).
