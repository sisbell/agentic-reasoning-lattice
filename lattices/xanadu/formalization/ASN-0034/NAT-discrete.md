**NAT-discrete (NatDiscreteness).** For every `m, n ∈ ℕ`, `m < n ⟹ m + 1 ≤ n`; equivalently, `m ≤ n < m + 1 ⟹ n = m`.

No natural number lies strictly between `n` and its successor `n + 1`: whenever `m < n`, the successor `m + 1` is already bounded above by `n`, so `m + 1 ≤ n`. This is the discreteness of ℕ. The axiom body invokes two symbols beyond ℕ's primitive `<` and `=`: the non-strict companion `≤`, *defined* in NAT-order by `m ≤ n ⟺ m < n ∨ m = n`, and the successor term `m + 1`, whose summand `1 ∈ ℕ` and closure `m + 1 ∈ ℕ` are posited by NAT-closure. Both are declared in the Depends slot so that the axiom body can be read without silently importing foundations.

*Formal Contract:*
- *Axiom:* `(A m, n ∈ ℕ :: m < n ⟹ m + 1 ≤ n)`; equivalently `(A m, n ∈ ℕ :: m ≤ n < m + 1 ⟹ n = m)` (discreteness).
- *Depends:*
  - NAT-order (NatStrictTotalOrder) — supplies the non-strict companion `≤` (defined by `m ≤ n ⟺ m < n ∨ m = n`), used in both the consequent `m + 1 ≤ n` and the equivalent antecedent `m ≤ n`.
  - NAT-closure (NatArithmeticClosureAndIdentity, this ASN) — posits `1 ∈ ℕ` and closes ℕ under addition, so the successor `m + 1 ∈ ℕ` and the inequalities `m + 1 ≤ n` and `n < m + 1` are comparisons of two ℕ-elements.
