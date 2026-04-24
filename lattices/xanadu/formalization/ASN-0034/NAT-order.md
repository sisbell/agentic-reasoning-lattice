**NAT-order (NatStrictTotalOrder).** The binary relation `<` on ℕ is a strict total order, with non-strict companion `≤` defined by `m ≤ n ⟺ m < n ∨ m = n` and reverse companions `≥` and `>` defined by `m ≥ n ⟺ n ≤ m` and `m > n ⟺ n < m`.

Strict total order on ℕ means three clauses hold jointly:
- Irreflexivity: `¬(n < n)` for every `n ∈ ℕ`
- Transitivity: `m < n ∧ n < p ⟹ m < p` for every `m, n, p ∈ ℕ`
- At-least-one trichotomy: for any `m, n ∈ ℕ`, at least one of `m < n`, `m = n`, `n < m` holds

The three clauses jointly export *exactly-one trichotomy* as a Consequence: for any `m, n ∈ ℕ`, exactly one of `m < n`, `m = n`, `n < m` holds. Exactly-one is the at-least-one disjunction conjoined with three pairwise mutual-exclusion clauses. `¬(m < n ∧ n < m)` follows from transitivity — which chains `m < n` and `n < m` to `m < m` — against irreflexivity. `¬(m < n ∧ m = n)` follows by substituting `m = n` into `m < n` via indiscernibility of `=` — a logical property of equality available throughout, not a property of `<` — rewriting to `m < m`, which irreflexivity at `n := m` rules out. `¬(m = n ∧ n < m)` follows by the same substitution applied to `n < m`: rewriting under `m = n` yields `m < m`, again against irreflexivity. The familiar disjointness form `m < n ⟹ m ≠ n` is the contrapositive of `¬(m < n ∧ m = n)` and is therefore also a Consequence — retaining it in the axiom slot would launder the irreflexivity-plus-indiscernibility derivation through a non-minimal axiom clause.

The axiom slot introduces `<` before constraining it: the first clause `< ⊆ ℕ × ℕ` posits `<` as a binary relation on ℕ, and the three strict-total-order clauses that follow then constrain that relation. NAT-closure follows the same register for the arithmetic primitive, opening its axiom slot with the signature `+ : ℕ × ℕ → ℕ` before the unit-membership and left-identity clauses.

The Definition slot introduces the non-strict companion `≤` from `<` and logical equality, and the reverse companions `≥` and `>` as the converses of `≤` and `<` respectively. These are notational definitions, not additional axioms: every downstream occurrence of `m ≥ n`, `m > n` unfolds to `n ≤ m`, `n < m` and inherits the strict-total-order properties through that unfolding.

*Formal Contract:*
- *Axiom:* `< ⊆ ℕ × ℕ` (`<` is a binary relation on ℕ); `(A n ∈ ℕ :: ¬(n < n))` (irreflexivity); `(A m, n, p ∈ ℕ : m < n ∧ n < p : m < p)` (transitivity); `(A m, n ∈ ℕ :: m < n ∨ m = n ∨ n < m)` (at-least-one trichotomy).
- *Consequence:* Exactly-one trichotomy: `(A m, n ∈ ℕ :: (m < n ∨ m = n ∨ n < m) ∧ ¬(m < n ∧ n < m) ∧ ¬(m < n ∧ m = n) ∧ ¬(m = n ∧ n < m))`. The disjunction is the at-least-one axiom clause directly; `¬(m < n ∧ n < m)` follows from transitivity and irreflexivity; `¬(m < n ∧ m = n)` follows by substituting `m = n` into `m < n` via indiscernibility of `=`, rewriting to `m < m` against irreflexivity at `n := m`; `¬(m = n ∧ n < m)` follows by the same substitution applied to `n < m`. The disjointness form `(A m, n ∈ ℕ : m < n : m ≠ n)` is the contrapositive of `¬(m < n ∧ m = n)` and is exported alongside exactly-one trichotomy as a Consequence.
- *Definition:* `(A m, n ∈ ℕ :: m ≤ n ⟺ m < n ∨ m = n)`; `(A m, n ∈ ℕ :: m ≥ n ⟺ n ≤ m)`; `(A m, n ∈ ℕ :: m > n ⟺ n < m)`.
- *Depends:* (none). NAT-order is the root of the NAT foundation: the strict-order primitive `<` is posited directly on ℕ by the axiom's first clause, not derived from an earlier axiom, and the non-strict companion `≤` together with the reverse companions `≥` and `>` are defined using only `<` and logical equality.
