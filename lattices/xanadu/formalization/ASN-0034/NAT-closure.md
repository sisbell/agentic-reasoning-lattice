**NAT-closure (NatArithmeticClosureAndIdentity).** The numeral `1` is in ℕ, and ℕ is closed under successor and addition, with `0` as the left additive identity.

The numeral `1` is posited directly as a natural number: `1 ∈ ℕ`. For every `n ∈ ℕ`, the successor `n + 1 ∈ ℕ`. For every `m, n ∈ ℕ`, the sum `m + n ∈ ℕ`. The left additive identity holds: `0 + n = n` for every `n ∈ ℕ`, where the literal `0` in this clause is the `0 ∈ ℕ` posited by NAT-zero — NAT-closure itself introduces only the numeral `1`, so without NAT-zero supplying the constant the left-identity clause would reference an ungrounded symbol; NAT-zero is therefore declared in the Depends slot, and no circularity arises because NAT-zero depends on NAT-order rather than on NAT-closure. The mirrored clause `n + 0 = n` is not axiomatized here; commutativity of `+` is not enumerated, so the right-identity form is not derivable from this axiom alone.

*Formal Contract:*
- *Axiom:* `1 ∈ ℕ` (one is a natural number); `(A n ∈ ℕ :: n + 1 ∈ ℕ)` (successor closure); `(A m, n ∈ ℕ :: m + n ∈ ℕ)` (addition closure); `(A n ∈ ℕ :: 0 + n = n)` (left additive identity).
- *Depends:*
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal `0` appearing in the left-identity clause `0 + n = n`.
