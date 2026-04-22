**NAT-zero (NatZeroMinimum).** `0` is the minimum of ℕ: `0 ∈ ℕ` and `(A n ∈ ℕ :: 0 < n ∨ 0 = n)`.

In words: `0` is itself a natural number, and every natural number is either strictly above `0` or equal to it. The second clause is phrased with the primitives `<` and `=` rather than the defined `≤`, so NAT-zero is self-contained and does not presuppose NAT-order. The two clauses together identify `0` as the minimum — membership places `0` among the elements compared, and the disjunction ensures no element sits strictly below it under `<`.

*Formal Contract:*
- *Axiom:* `0 ∈ ℕ` (zero is a natural number); `(A n ∈ ℕ :: 0 < n ∨ 0 = n)` (no natural number lies strictly below zero).
