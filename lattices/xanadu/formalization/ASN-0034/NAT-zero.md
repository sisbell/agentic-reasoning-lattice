**NAT-zero (NatZeroMinimum).** `0` is the minimum of ℕ: `0 ∈ ℕ` and `(A n ∈ ℕ :: 0 < n ∨ 0 = n)`.

In words: `0` is itself a natural number, and every natural number is either strictly above `0` or equal to it. Combined with NAT-order's irreflexivity `¬(n < n)` and transitivity `m < n ∧ n < p ⟹ m < p`, these clauses identify `0` as the minimum — that no `n ∈ ℕ` satisfies `n < 0`. Suppose some `n ∈ ℕ` did satisfy `n < 0`; the second clause forces `0 < n ∨ 0 = n`. In the first case, `0 < n` and `n < 0` together yield `0 < 0` by transitivity, contradicting irreflexivity. In the second case, `0 = n` rewrites `n < 0` to `0 < 0`, again contradicting irreflexivity. So the minimum reading of NAT-zero rests on NAT-order's irreflexivity and transitivity; NAT-order is declared in the Depends slot accordingly.

*Formal Contract:*
- *Axiom:* `0 ∈ ℕ` (zero is a natural number); `(A n ∈ ℕ :: 0 < n ∨ 0 = n)` (every natural number is strictly above or equal to zero).
- *Depends:*
  - NAT-order (NatStrictTotalOrder) — supplies the strict-order primitive `<` used in the second clause; its irreflexivity `¬(n < n)` and transitivity `m < n ∧ n < p ⟹ m < p` are what lift the disjunction `0 < n ∨ 0 = n` to the minimum reading `¬(n < 0)`.
