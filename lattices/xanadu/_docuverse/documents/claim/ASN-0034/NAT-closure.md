**NAT-closure (NatArithmeticClosureAndIdentity).** The binary operation `+ : ℕ × ℕ → ℕ` is posited directly on ℕ; the numeral `1` is in ℕ and is strictly above `0`; `0` is a two-sided additive identity for `+`; and the addition-based successor `n + 1` is strictly above `0` for every `n ∈ ℕ`.

The signature `+ : ℕ × ℕ → ℕ` makes `+` total on `ℕ × ℕ` and closes its result in ℕ.

The pair `1 ∈ ℕ` and `0 < 1` names a second constant in ℕ and locates it in the strict order.

The clause `(A n ∈ ℕ :: 0 < n + 1)` is the Peano no-predecessor-of-zero condition phrased for the addition-based successor: no `n ∈ ℕ` has `n + 1 = 0`. The earlier distinctness clause `0 < 1` is recovered as the case `n := 0` together with the left-identity rewrite `0 + 1 = 1`, but it pins down only the single sum `0 + 1`. Without the universal clause, a model could satisfy the signature, the identity laws, and `0 < 1` while still permitting `m + 1 = 0` at some `m ≥ 1`; the new clause closes that gap uniformly across ℕ.

*Formal Contract:*
- *Axiom:* `+ : ℕ × ℕ → ℕ` (`+` is a binary operation on ℕ); `1 ∈ ℕ` (one is a natural number); `0 < 1` (distinctness of the two named constants); `(A n ∈ ℕ :: 0 + n = n)` (left additive identity); `(A n ∈ ℕ :: n + 0 = n)` (right additive identity); `(A n ∈ ℕ :: 0 < n + 1)` (successor positivity — the addition-based successor is never `0`).
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set appearing as the domain `ℕ × ℕ` and codomain `ℕ` of the signature `+ : ℕ × ℕ → ℕ`, in the membership clause `1 ∈ ℕ`, and over which the bounded quantifiers `(A n ∈ ℕ :: 0 + n = n)`, `(A n ∈ ℕ :: n + 0 = n)`, and `(A n ∈ ℕ :: 0 < n + 1)` of the left-identity, right-identity, and successor-positivity clauses range.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal `0` appearing in the distinctness clause `0 < 1`, the left-identity clause `0 + n = n`, the right-identity clause `n + 0 = n`, and the successor-positivity clause `0 < n + 1`.
  - NAT-order (NatStrictTotalOrder) — supplies the strict-order primitive `<` used in the distinctness clause `0 < 1` and in the successor-positivity clause `0 < n + 1`.
