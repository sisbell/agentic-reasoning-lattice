**NAT-order (NatStrictTotalOrder).** The binary relation `<` on ℕ is a strict total order, with non-strict companion `≤` defined by `m ≤ n ⟺ m < n ∨ m = n` and reverse companions `≥` and `>` defined by `m ≥ n ⟺ n ≤ m` and `m > n ⟺ n < m`.

Strict total order on ℕ means three clauses hold jointly:
- Irreflexivity: `¬(n < n)` for every `n ∈ ℕ`
- Transitivity: `m < n ∧ n < p ⟹ m < p` for every `m, n, p ∈ ℕ`
- At-least-one trichotomy: for any `m, n ∈ ℕ`, at least one of `m < n`, `m = n`, `n < m` holds

Together the three clauses yield *exactly-one trichotomy*: for any `m, n ∈ ℕ`, exactly one of `m < n`, `m = n`, `n < m` holds. Exactly-one is the at-least-one disjunction conjoined with three pairwise mutual-exclusion clauses. `¬(m < n ∧ n < m)` follows from transitivity — which chains `m < n` and `n < m` to `m < m` — against irreflexivity. `¬(m < n ∧ m = n)` follows by substituting `m = n` into `m < n` via indiscernibility of `=`, rewriting to `m < m`, which irreflexivity at `n := m` rules out. `¬(m = n ∧ n < m)` follows by the same substitution applied to `n < m`: rewriting under `m = n` yields `m < m`, again against irreflexivity.

The non-strict companion `≤` inherits transitivity from `<` and `=` jointly: `m ≤ n ∧ n ≤ p ⟹ m ≤ p`. Unfolding each hypothesis against the defining disjunction `x ≤ y ⟺ x < y ∨ x = y` yields four cases, and each discharges to `m ≤ p`. If both are strict — `m < n ∧ n < p` — `<`-transitivity gives `m < p`, so `m ≤ p` by the definition. If the first is strict and the second is equality — `m < n ∧ n = p` — indiscernibility of `=` substitutes `n = p` into `m < n` to yield `m < p`. The symmetric case `m = n ∧ n < p` substitutes `m = n` into `n < p` to yield `m < p`. If both are equalities — `m = n ∧ n = p` — transitivity of `=` gives `m = p`, so `m ≤ p`.

*Formal Contract:*
- *Axiom:* `< ⊆ ℕ × ℕ` (`<` is a binary relation on ℕ); `(A n ∈ ℕ :: ¬(n < n))` (irreflexivity); `(A m, n, p ∈ ℕ : m < n ∧ n < p : m < p)` (transitivity); `(A m, n ∈ ℕ :: m < n ∨ m = n ∨ n < m)` (at-least-one trichotomy).
- *Consequence:* Exactly-one trichotomy: `(A m, n ∈ ℕ :: (m < n ∨ m = n ∨ n < m) ∧ ¬(m < n ∧ n < m) ∧ ¬(m < n ∧ m = n) ∧ ¬(m = n ∧ n < m))`. The disjunction is the at-least-one axiom clause directly; `¬(m < n ∧ n < m)` follows from transitivity and irreflexivity; `¬(m < n ∧ m = n)` follows by substituting `m = n` into `m < n` via indiscernibility of `=`, rewriting to `m < m` against irreflexivity at `n := m`; `¬(m = n ∧ n < m)` follows by the same substitution applied to `n < m`.
- *Consequence:* `≤`-transitivity: `(A m, n, p ∈ ℕ : m ≤ n ∧ n ≤ p : m ≤ p)`. Unfolding each hypothesis by the definition `x ≤ y ⟺ x < y ∨ x = y` yields four cases. `m < n ∧ n < p` gives `m < p` by `<`-transitivity, hence `m ≤ p`. `m < n ∧ n = p` gives `m < p` by substituting `n = p` into `m < n` via indiscernibility of `=`, hence `m ≤ p`. `m = n ∧ n < p` gives `m < p` by substituting `m = n` into `n < p`, hence `m ≤ p`. `m = n ∧ n = p` gives `m = p` by transitivity of `=`, hence `m ≤ p`.
- *Definition:* `(A m, n ∈ ℕ :: m ≤ n ⟺ m < n ∨ m = n)`; `(A m, n ∈ ℕ :: m ≥ n ⟺ n ≤ m)`; `(A m, n ∈ ℕ :: m > n ⟺ n < m)`.
- *Depends:* (none).
