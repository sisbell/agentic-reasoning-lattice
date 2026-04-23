**NAT-sub (NatPartialSubtraction).** Subtraction on ℕ is a partial binary operation: whenever `m, n ∈ ℕ` satisfy `m ≥ n`, the difference `m − n` is the unique natural number characterised by `(m − n) + n = m`.

The following facts about partial subtraction and its interaction with addition and order on ℕ are stated together:

- Conditional closure: `m ≥ n ⟹ m − n ∈ ℕ` for every `m, n ∈ ℕ`.
- Right-inverse characterisation: `m ≥ n ⟹ (m − n) + n = m` for every `m, n ∈ ℕ`.
- Left-inverse characterisation: `m ≥ n ⟹ n + (m − n) = m` for every `m, n ∈ ℕ`.
- Strict positivity: `m > n ⟹ m − n ≥ 1` for every `m, n ∈ ℕ`.
- Right telescoping: `(m + n) − n = m` for every `m, n ∈ ℕ`.
- Strict monotonicity: `m ≥ p ∧ n ≥ p ∧ m < n ⟹ m − p < n − p` for every `m, n, p ∈ ℕ`.

Both inverse forms are stated because citing either one without commutativity of addition would otherwise be tacit.

The axiom body invokes symbols beyond ℕ's primitive membership. The strict order `<` together with its non-strict companion `≤` and reverse companions `≥`, `>` — all defined in NAT-order by `m ≤ n ⟺ m < n ∨ m = n`, `m ≥ n ⟺ n ≤ m`, `m > n ⟺ n < m` — appear in the antecedents `m ≥ n`, `m > n`, `m ≥ p ∧ n ≥ p ∧ m < n` of the conditional-closure, inverse-characterisation, strict-positivity, and strict-monotonicity clauses and in the consequents `m − n ≥ 1` and `m − p < n − p`. The binary addition `+` closed over ℕ by NAT-closure appears in the sums `(m − n) + n`, `n + (m − n)`, and `m + n`, and the numeral `1 ∈ ℕ` posited by NAT-closure grounds the lower bound of `m − n ≥ 1`. Both foundations are declared in the Depends slot so that the axiom body can be read without silently importing them.

*Formal Contract:*
- *Axiom:* `(A m, n ∈ ℕ : m ≥ n : m − n ∈ ℕ)` (conditional closure); `(A m, n ∈ ℕ : m ≥ n : (m − n) + n = m)` (right-inverse characterisation); `(A m, n ∈ ℕ : m ≥ n : n + (m − n) = m)` (left-inverse characterisation); `(A m, n ∈ ℕ : m > n : m − n ≥ 1)` (strict positivity); `(A m, n ∈ ℕ :: (m + n) − n = m)` (right telescoping); `(A m, n, p ∈ ℕ : m ≥ p ∧ n ≥ p ∧ m < n : m − p < n − p)` (strict monotonicity).
- *Depends:*
  - NAT-order (NatStrictTotalOrder) — supplies the strict order `<` and its companions `≤`, `≥`, `>` (defined by `m ≤ n ⟺ m < n ∨ m = n`, `m ≥ n ⟺ n ≤ m`, `m > n ⟺ n < m`), used in the antecedents `m ≥ n`, `m > n`, `m ≥ p ∧ n ≥ p ∧ m < n` and in the consequents `m − n ≥ 1` and `m − p < n − p`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — posits `1 ∈ ℕ` and closes ℕ under addition, so the literal `1` appearing in the strict-positivity consequent `m − n ≥ 1` is grounded and every sum `(m − n) + n`, `n + (m − n)`, `m + n` appearing in the inverse-characterisation and right-telescoping clauses is an ℕ-element.
