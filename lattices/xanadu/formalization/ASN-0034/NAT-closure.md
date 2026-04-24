**NAT-closure (NatArithmeticClosureAndIdentity).** The binary operation `+ : ℕ × ℕ → ℕ` is posited directly on ℕ; the numeral `1` is in ℕ; and `0` is a two-sided additive identity for `+`.

The axiom slot introduces `+` before constraining it: its first clause `+ : ℕ × ℕ → ℕ` posits the signature — fixing arity (binary) and codomain (ℕ). The numeral `1` is posited directly as a natural number: `1 ∈ ℕ`. The additive identity holds on both sides: `0 + n = n` (left) and `n + 0 = n` (right) for every `n ∈ ℕ`; the literal `0` appearing in each clause is the `0 ∈ ℕ` posited by NAT-zero. Left and right identity are stated as independent clauses because the NAT-* axioms of this ASN do not declare commutativity of addition on ℕ — without `m + n = n + m`, neither identity is derivable from the other. Both-sided coverage is the foundation's deliberate substitute for the absent commutativity axiom, matching the same design choice NAT-sub makes for its right/left-inverse and right/left-telescoping pairs, NAT-addcompat makes for its left/right compatibility pair, NAT-cancel makes for its left/right cancellation pair, and NAT-addbound makes for its right/left-dominance pair.

*Formal Contract:*
- *Axiom:* `+ : ℕ × ℕ → ℕ` (`+` is a binary operation on ℕ); `1 ∈ ℕ` (one is a natural number); `(A n ∈ ℕ :: 0 + n = n)` (left additive identity); `(A n ∈ ℕ :: n + 0 = n)` (right additive identity).
- *Depends:*
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal `0` appearing in the left-identity clause `0 + n = n` and the right-identity clause `n + 0 = n`.
