**NAT-closure (NatArithmeticClosureAndIdentity).** The binary operation `+ : ℕ × ℕ → ℕ` is posited directly on ℕ; the numeral `1` is in ℕ and is strictly above `0`; and `0` is a two-sided additive identity for `+`.

The axiom slot introduces `+` before constraining it: its first clause `+ : ℕ × ℕ → ℕ` posits the signature — fixing arity (binary) and codomain (ℕ). The numeral `1` is posited directly as a natural number: `1 ∈ ℕ`. Alongside `1 ∈ ℕ` we post the distinctness clause `0 < 1`, which separates the two named constants — without it, the remaining NAT-* clauses admit a model interpreting `1` as `0`. The clause uses the strict-order primitive `<` supplied by NAT-order and the literal `0` supplied by NAT-zero. The additive identity holds on both sides: `0 + n = n` (left) and `n + 0 = n` (right) for every `n ∈ ℕ`; the literal `0` appearing in each clause is the `0 ∈ ℕ` posited by NAT-zero, the same constant that appears in the distinctness clause.

*Formal Contract:*
- *Axiom:* `+ : ℕ × ℕ → ℕ` (`+` is a binary operation on ℕ); `1 ∈ ℕ` (one is a natural number); `0 < 1` (distinctness of the two named constants); `(A n ∈ ℕ :: 0 + n = n)` (left additive identity); `(A n ∈ ℕ :: n + 0 = n)` (right additive identity).
- *Depends:*
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal `0` appearing in the distinctness clause `0 < 1`, the left-identity clause `0 + n = n`, and the right-identity clause `n + 0 = n`.
  - NAT-order (NatStrictTotalOrder) — supplies the strict-order primitive `<` used in the distinctness clause `0 < 1`.
