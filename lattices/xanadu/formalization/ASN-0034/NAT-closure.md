**NAT-closure (NatArithmeticClosureAndIdentity).** The binary operation `+ : ℕ × ℕ → ℕ` is posited directly on ℕ; the numeral `1` is in ℕ and is strictly above `0`; and `0` is a two-sided additive identity for `+`.

The signature `+ : ℕ × ℕ → ℕ` carries two load-bearing commitments. Its domain `ℕ × ℕ` makes `+` total on the naturals — every pair of naturals has a sum — and its codomain `ℕ` closes the operation under addition, so compositional terms like `(m + n) + p` re-enter the signature without a side condition. Totality rules out partial addition and closure rules out sums that escape ℕ; together they are what lets callers chain `+` across steps without carrying a well-definedness obligation at each application.

The pair `1 ∈ ℕ` and `0 < 1` names a second constant in ℕ and locates it in the strict order. `0 < 1` entails `0 ≠ 1` against NAT-order's exactly-one trichotomy, which forbids `0 < 1 ∧ 0 = 1`. Beyond distinctness, `0 < 1` pins `1` strictly above `0`.

*Formal Contract:*
- *Axiom:* `+ : ℕ × ℕ → ℕ` (`+` is a binary operation on ℕ); `1 ∈ ℕ` (one is a natural number); `0 < 1` (distinctness of the two named constants); `(A n ∈ ℕ :: 0 + n = n)` (left additive identity); `(A n ∈ ℕ :: n + 0 = n)` (right additive identity).
- *Depends:*
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal `0` appearing in the distinctness clause `0 < 1`, the left-identity clause `0 + n = n`, and the right-identity clause `n + 0 = n`.
  - NAT-order (NatStrictTotalOrder) — supplies the strict-order primitive `<` used in the distinctness clause `0 < 1`, and the exactly-one trichotomy Consequence (specifically the mutual-exclusion conjunct `¬(m < n ∧ m = n)`) used in the body to derive `0 ≠ 1` from `0 < 1`.
