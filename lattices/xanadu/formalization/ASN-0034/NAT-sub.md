**NAT-sub (NatPartialSubtraction).** Subtraction on ℕ is a partial binary operation: whenever `m, n ∈ ℕ` satisfy `m ≥ n`, the difference `m − n` is the unique natural number characterised by `(m − n) + n = m`.

Several related facts are stated together as one axiom because they all concern this partial subtraction operation and its interaction with addition and order on ℕ:

- Conditional closure: `m ≥ n ⟹ m − n ∈ ℕ` for every `m, n ∈ ℕ`.
- Right-inverse characterisation: `m ≥ n ⟹ (m − n) + n = m` for every `m, n ∈ ℕ`.
- Left-inverse characterisation: `m ≥ n ⟹ n + (m − n) = m` for every `m, n ∈ ℕ`.
- Strict positivity: `m > n ⟹ m − n ≥ 1` for every `m, n ∈ ℕ`.
- Right telescoping: `(m + n) − n = m` for every `m, n ∈ ℕ`.
- Strict monotonicity: `m ≥ p ∧ n ≥ p ∧ m < n ⟹ m − p < n − p` for every `m, n, p ∈ ℕ`.

Both inverse forms are stated explicitly because downstream proofs supply the fixed summand on either side: TA4's round-trip cancels `wₖ` on the right of `(aₖ + wₖ) − wₖ = aₖ` (right telescoping), while D1's round-trip supplies `aₖ` on the left of `aₖ + (bₖ − aₖ) = bₖ` (left-inverse characterisation). Without both forms stated as axioms, those citations would tacitly assume commutativity of addition on ℕ, breaking the citation policy that the other NAT-* axioms enforce (NAT-addcompat bundles left and right order-compatibility for the same reason). Strict positivity is used in TumblerSub's positivity postcondition at the zpd point (`rₖ = aₖ − wₖ ≥ 1`) and in D1/D2's verification that the displacement is Pos. Strict monotonicity is used in TA3 and TA3-strict to lift `a_d < b_d` through subtraction of a common subtrahend (`a_d − w_d < b_d − w_d`).

These are standard properties of ℕ, stated here as an axiom so downstream proofs can cite them directly. The ASN's convention (T0) is that each proof cites only the ℕ facts it actually uses; without an explicit axiom for partial subtraction, the roughly one dozen proof steps that write `rₖ = aₖ − wₖ` at a divergence point would appeal to background arithmetic, breaking the citation policy that the other NAT-* axioms enforce.

*Formal Contract:*
- *Axiom:* `(A m, n ∈ ℕ : m ≥ n : m − n ∈ ℕ)` (conditional closure); `(A m, n ∈ ℕ : m ≥ n : (m − n) + n = m)` (right-inverse characterisation); `(A m, n ∈ ℕ : m ≥ n : n + (m − n) = m)` (left-inverse characterisation); `(A m, n ∈ ℕ : m > n : m − n ≥ 1)` (strict positivity); `(A m, n ∈ ℕ :: (m + n) − n = m)` (right telescoping); `(A m, n, p ∈ ℕ : m ≥ p ∧ n ≥ p ∧ m < n : m − p < n − p)` (strict monotonicity).
