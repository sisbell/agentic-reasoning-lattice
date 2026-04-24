**NAT-closure (NatArithmeticClosureAndIdentity).** The binary operation `+ : ℕ × ℕ → ℕ` is posited directly on ℕ; the numeral `1` is in ℕ; and `0` is a left additive identity for `+`.

The axiom slot introduces `+` before constraining it: its first clause `+ : ℕ × ℕ → ℕ` posits the signature — fixing arity (binary) and codomain (ℕ). The numeral `1` is posited directly as a natural number: `1 ∈ ℕ`. The left additive identity holds: `0 + n = n` for every `n ∈ ℕ`; the literal `0` appearing in this clause is the `0 ∈ ℕ` posited by NAT-zero.

*Formal Contract:*
- *Axiom:* `+ : ℕ × ℕ → ℕ` (`+` is a binary operation on ℕ); `1 ∈ ℕ` (one is a natural number); `(A n ∈ ℕ :: 0 + n = n)` (left additive identity).
- *Depends:*
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal `0` appearing in the left-identity clause `0 + n = n`.
