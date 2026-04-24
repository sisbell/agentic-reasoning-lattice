**NAT-closure (NatArithmeticClosureAndIdentity).** The binary operation `+ : ℕ × ℕ → ℕ` is posited directly on ℕ; the numeral `1` is in ℕ; and `0` is a two-sided additive identity for `+`.

The axiom slot introduces `+` before constraining it: its first clause `+ : ℕ × ℕ → ℕ` posits the signature — fixing arity (binary) and codomain (ℕ). The numeral `1` is posited directly as a natural number: `1 ∈ ℕ`. The additive identity holds on both sides: `0 + n = n` (left) and `n + 0 = n` (right) for every `n ∈ ℕ`; the literal `0` appearing in each clause is the `0 ∈ ℕ` posited by NAT-zero. Left and right identity are stated as independent clauses because the NAT-* axioms of this ASN do not declare commutativity of addition on ℕ — without `m + n = n + m`, neither identity is derivable from the other. This is a foundation-wide pattern: every NAT-* axiom or theorem in this ASN involving `+` that admits a left and a right variant states each variant as an independent clause, for the same reason. The rationale is recorded here, at the site where `+` is introduced, and is not repeated at each subsequent occurrence.

*Formal Contract:*
- *Axiom:* `+ : ℕ × ℕ → ℕ` (`+` is a binary operation on ℕ); `1 ∈ ℕ` (one is a natural number); `(A n ∈ ℕ :: 0 + n = n)` (left additive identity); `(A n ∈ ℕ :: n + 0 = n)` (right additive identity).
- *Depends:*
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal `0` appearing in the left-identity clause `0 + n = n` and the right-identity clause `n + 0 = n`.
