**NAT-cancel (NatAdditionCancellation).** Addition on ℕ is cancellative on either side, and a sum equals one of its summands only when the other is zero.

- Left cancellation: `m + n = m + p ⟹ n = p` for every `m, n, p ∈ ℕ`.
- Right cancellation: `n + m = p + m ⟹ n = p` for every `m, n, p ∈ ℕ`.
- Summand absorption, standard form: `m + n = m ⟹ n = 0` for every `m, n ∈ ℕ`.
- Summand absorption, symmetric form: `n + m = m ⟹ n = 0` for every `m, n ∈ ℕ`.

Both summand-absorption forms are stated independently because the NAT-* axioms of this ASN do not include commutativity of addition on ℕ, so neither form is derivable from the other. The same reason governs the independent statement of left and right cancellation.

Two primitives appear in these clauses that are not introduced here. The binary operation `+` is the one posited by NAT-closure's signature clause `+ : ℕ × ℕ → ℕ`; all four clauses use `+` at exactly that arity. The literal `0` appearing on the right-hand side of both absorption clauses is the `0 ∈ ℕ` posited by NAT-zero — NAT-cancel introduces no constant of its own, so without NAT-zero supplying the symbol the absorption conclusions `n = 0` would reference an ungrounded literal. NAT-closure and NAT-zero are therefore both declared in the Depends slot; NAT-zero is named directly rather than reached transitively through NAT-closure, matching the precedent NAT-closure itself sets where NAT-zero is declared as the supplier of the literal `0` appearing in its left-identity clause `0 + n = n`.

*Formal Contract:*
- *Axiom:* `(A m, n, p ∈ ℕ : m + n = m + p : n = p)` (left cancellation); `(A m, n, p ∈ ℕ : n + m = p + m : n = p)` (right cancellation); `(A m, n ∈ ℕ : m + n = m : n = 0)` (summand absorption, standard form); `(A m, n ∈ ℕ : n + m = m : n = 0)` (summand absorption, symmetric form).
- *Depends:*
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies the binary operation `+ : ℕ × ℕ → ℕ` used in all four axiom clauses.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal `0` on the right-hand side of both absorption clauses `m + n = m ⟹ n = 0` and `n + m = m ⟹ n = 0`; named directly rather than reached transitively through NAT-closure, following the same precedent NAT-closure uses to declare NAT-zero as the supplier of the literal `0` in its left-identity clause.
