**NAT-closure (NatArithmeticClosureAndIdentity).** The binary operation `+ : ℕ × ℕ → ℕ` is posited directly on ℕ; the numeral `1` is in ℕ and is strictly above `0`; and `0` is a two-sided additive identity for `+`.

The signature `+ : ℕ × ℕ → ℕ` makes `+` total on `ℕ × ℕ` and closes its result in ℕ.

The pair `1 ∈ ℕ` and `0 < 1` names a second constant in ℕ and locates it in the strict order.

*Formal Contract:*
- *Axiom:* `+ : ℕ × ℕ → ℕ` (`+` is a binary operation on ℕ); `1 ∈ ℕ` (one is a natural number); `0 < 1` (distinctness of the two named constants); `(A n ∈ ℕ :: 0 + n = n)` (left additive identity); `(A n ∈ ℕ :: n + 0 = n)` (right additive identity).
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set appearing as the domain `ℕ × ℕ` and codomain `ℕ` of the signature `+ : ℕ × ℕ → ℕ`, in the membership clause `1 ∈ ℕ`, and over which the bounded quantifiers `(A n ∈ ℕ :: 0 + n = n)` and `(A n ∈ ℕ :: n + 0 = n)` of the left- and right-identity clauses range.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal `0` appearing in the distinctness clause `0 < 1`, the left-identity clause `0 + n = n`, and the right-identity clause `n + 0 = n`.
  - NAT-order (NatStrictTotalOrder) — supplies the strict-order primitive `<` used in the distinctness clause `0 < 1`.
