**NAT-closure (NatArithmeticClosureAndIdentity).** The binary operation `+ : ℕ × ℕ → ℕ` is posited directly on ℕ; the numeral `1` is in ℕ; `0` is a two-sided additive identity for `+`; and the addition-based successor `n + 1` is strictly above `0` for every `n ∈ ℕ`.

The signature `+ : ℕ × ℕ → ℕ` makes `+` total on `ℕ × ℕ` and closes its result in ℕ.

The membership clause `1 ∈ ℕ` names a second constant in ℕ.

The clause `(A n ∈ ℕ :: 0 < n + 1)` is the Peano no-predecessor-of-zero condition phrased for the addition-based successor: no `n ∈ ℕ` has `n + 1 = 0`. The strict-order placement of `1` falls out as a consequence: instantiating successor-positivity at `n := 0` gives `0 < 0 + 1`; the left-identity clause `(A n ∈ ℕ :: 0 + n = n)` at `n := 1` gives `0 + 1 = 1`; substitutivity of `=` then rewrites the right-hand side of the inequality, yielding `0 < 1`. This derivation pins down only the single sum `0 + 1`; without the universal clause, a model could satisfy the signature, the identity laws, and the bare `0 < 1` while still permitting `m + 1 = 0` at some `m ≥ 1`. The universal clause closes that gap uniformly across ℕ.

*Formal Contract:*
- *Axiom:* `+ : ℕ × ℕ → ℕ` (`+` is a binary operation on ℕ); `1 ∈ ℕ` (one is a natural number); `(A n ∈ ℕ :: 0 + n = n)` (left additive identity); `(A n ∈ ℕ :: n + 0 = n)` (right additive identity); `(A n ∈ ℕ :: 0 < n + 1)` (successor positivity — the addition-based successor is never `0`).
- *Consequence:* `0 < 1` (the named constants `0` and `1` are distinct in the strict order) — derived from the successor-positivity clause `(A n ∈ ℕ :: 0 < n + 1)` instantiated at `n := 0`, the left-identity clause `(A n ∈ ℕ :: 0 + n = n)` instantiated at `n := 1`, and substitutivity of `=`, as shown in the preceding prose.
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set appearing as the domain `ℕ × ℕ` and codomain `ℕ` of the signature `+ : ℕ × ℕ → ℕ`, in the membership clause `1 ∈ ℕ`, and over which the bounded quantifiers `(A n ∈ ℕ :: 0 + n = n)`, `(A n ∈ ℕ :: n + 0 = n)`, and `(A n ∈ ℕ :: 0 < n + 1)` of the left-identity, right-identity, and successor-positivity clauses range.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal `0` appearing in the left-identity clause `0 + n = n`, the right-identity clause `n + 0 = n`, the successor-positivity clause `0 < n + 1`, and the *Consequence:* `0 < 1`.
  - NAT-order (NatStrictTotalOrder) — supplies the strict-order primitive `<` used in the successor-positivity clause `0 < n + 1` and in the *Consequence:* `0 < 1`.
