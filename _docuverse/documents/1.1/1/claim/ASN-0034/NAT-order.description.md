The natural numbers are strictly totally ordered by `<`: no number precedes itself (irreflexivity), the order is
transitive, and any two naturals are related by at least one of `<`, `=`, `>` (at-least-one trichotomy). The
three axiom clauses together with indiscernibility of `=` export two Consequences. First, *exactly-one
trichotomy*: for any two naturals, exactly one of less-than, equality, or greater-than holds. The implicational
form `m < n ⟹ m ≠ n` is the mutual-exclusion conjunct `¬(m < n ∧ m = n)` rewritten by the classical
equivalence `¬(A ∧ B) ⟺ (A ⟹ ¬B)` — a derivable restatement of that conjunct, not a separately
exported Consequence; consumers needing the implicational form cite the exactly-one trichotomy bullet. Second,
`≤`-*transitivity*: `m ≤ n ∧ n ≤ p ⟹ m ≤ p`, derived by four-way case analysis on the defining disjunction
`x ≤ y ⟺ x < y ∨ x = y` against `<`-transitivity and indiscernibility of `=`. The non-strict companion `≤`
is defined from `<` directly, and the reverse companions `≥` and `>` are defined as the converses of `≤` and
`<`; all three defined relations inherit the strict-total-order guarantees through their unfoldings.
