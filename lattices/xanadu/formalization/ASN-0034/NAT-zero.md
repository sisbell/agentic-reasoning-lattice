**NAT-zero (NatZeroMinimum).** `0` is the minimum of ℕ: `0 ∈ ℕ` and `(A n ∈ ℕ :: 0 < n ∨ 0 = n)`.

In words: `0` is itself a natural number, and every natural number is either strictly above `0` or equal to it. Combined with NAT-order's irreflexivity `¬(n < n)` and transitivity `m < n ∧ n < p ⟹ m < p`, these clauses identify `0` as the minimum: `(A n ∈ ℕ :: ¬(n < 0))`. Suppose some `n ∈ ℕ` did satisfy `n < 0`; the second clause forces `0 < n ∨ 0 = n`. In the first case, `0 < n` and `n < 0` together yield `0 < 0` by transitivity, contradicting irreflexivity. In the second case, `0 = n` rewrites `n < 0` to `0 < 0` by indiscernibility of `=` — a logical property of equality available throughout, not a property of `<` — again contradicting irreflexivity. The minimum predicate `(A n ∈ ℕ :: ¬(n < 0))` is therefore exported as a *Consequence:* of the formal contract, lifted from the axiom's disjunction by NAT-order's irreflexivity and transitivity (both branches collapse to `0 < 0`); NAT-order is declared in the Depends slot accordingly.

*Formal Contract:*
- *Axiom:* `0 ∈ ℕ` (zero is a natural number); `(A n ∈ ℕ :: 0 < n ∨ 0 = n)` (every natural number is strictly above or equal to zero).
- *Consequence:* `(A n ∈ ℕ :: ¬(n < 0))` (no natural number is strictly below zero — the minimum reading).
- *Depends:*
  - NAT-order (NatStrictTotalOrder) — supplies `<` for the axiom's second clause and the irreflexivity `¬(n < n)` + transitivity `m < n ∧ n < p ⟹ m < p` used in the body's derivation of the *Consequence:* bullet `¬(n < 0)`.
