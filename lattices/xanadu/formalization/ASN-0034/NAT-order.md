**NAT-order (NatStrictTotalOrder).** The binary relation `<` on ℕ is a strict total order, with non-strict companion `≤` defined by `m ≤ n ⟺ m < n ∨ m = n` and reverse companions `≥` and `>` defined by `m ≥ n ⟺ n ≤ m` and `m > n ⟺ n < m`.

Strict total order on ℕ means four clauses hold jointly:
- Irreflexivity: `¬(n < n)` for every `n ∈ ℕ`
- Transitivity: `m < n ∧ n < p ⟹ m < p` for every `m, n, p ∈ ℕ`
- At-least-one trichotomy: for any `m, n ∈ ℕ`, at least one of `m < n`, `m = n`, `n < m` holds
- Disjointness of `<` and `=`: for any `m, n ∈ ℕ` with `m < n`, `m ≠ n`

The four clauses jointly export *exactly-one trichotomy* as a Consequence: for any `m, n ∈ ℕ`, exactly one of `m < n`, `m = n`, `n < m` holds. Exactly-one is the at-least-one disjunction conjoined with three pairwise mutual-exclusion clauses. `¬(m < n ∧ n < m)` follows from transitivity — which chains `m < n` and `n < m` to `m < m` — against irreflexivity. `¬(m < n ∧ m = n)` follows from disjointness at `(m, n)`: the hypothesis `m < n` forces `m ≠ n`, contradicting `m = n`. `¬(m = n ∧ n < m)` follows from disjointness at `(n, m)`: the hypothesis `n < m` forces `n ≠ m`, which contradicts `m = n` (equivalently `n = m`).

The axiom slot introduces `<` before constraining it: the first clause `< ⊆ ℕ × ℕ` posits `<` as a binary relation on ℕ, and the four strict-total-order clauses that follow then constrain that relation. NAT-closure follows the same register for the arithmetic primitive, opening its axiom slot with the signature `+ : ℕ × ℕ → ℕ` before the unit-membership and left-identity clauses.

The Definition slot introduces the non-strict companion `≤` from `<` and logical equality, and the reverse companions `≥` and `>` as the converses of `≤` and `<` respectively. These are notational definitions, not additional axioms: every downstream occurrence of `m ≥ n`, `m > n` unfolds to `n ≤ m`, `n < m` and inherits the strict-total-order properties through that unfolding.

*Formal Contract:*
- *Axiom:* `< ⊆ ℕ × ℕ` (`<` is a binary relation on ℕ); `(A n ∈ ℕ :: ¬(n < n))` (irreflexivity); `(A m, n, p ∈ ℕ : m < n ∧ n < p : m < p)` (transitivity); `(A m, n ∈ ℕ :: m < n ∨ m = n ∨ n < m)` (at-least-one trichotomy); `(A m, n ∈ ℕ : m < n : m ≠ n)` (disjointness of `<` and `=`).
- *Consequence:* Exactly-one trichotomy: `(A m, n ∈ ℕ :: (m < n ∨ m = n ∨ n < m) ∧ ¬(m < n ∧ n < m) ∧ ¬(m < n ∧ m = n) ∧ ¬(m = n ∧ n < m))`. The disjunction is the at-least-one axiom clause directly; `¬(m < n ∧ n < m)` follows from transitivity and irreflexivity; `¬(m < n ∧ m = n)` follows from the disjointness axiom at `(m, n)`; `¬(m = n ∧ n < m)` follows from the disjointness axiom at `(n, m)`.
- *Definition:* `(A m, n ∈ ℕ :: m ≤ n ⟺ m < n ∨ m = n)`; `(A m, n ∈ ℕ :: m ≥ n ⟺ n ≤ m)`; `(A m, n ∈ ℕ :: m > n ⟺ n < m)`.
- *Depends:* (none). NAT-order is the root of the NAT foundation: the strict-order primitive `<` is posited directly on ℕ by the axiom's first clause, not derived from an earlier axiom, and the non-strict companion `≤` together with the reverse companions `≥` and `>` are defined using only `<` and logical equality.
