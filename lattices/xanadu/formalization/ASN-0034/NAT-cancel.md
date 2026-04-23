**NAT-cancel (NatAdditionCancellation).** Addition on ℕ is cancellative on either side, and a sum equals one of its summands only when the other summand is zero.

- Left cancellation: `m + n = m + p ⟹ n = p` for every `m, n, p ∈ ℕ`.
- Right cancellation: `n + m = p + m ⟹ n = p` for every `m, n, p ∈ ℕ`.
- Summand absorption: `m + n = m ⟹ n = 0` for every `m, n ∈ ℕ`.

Each of these three clauses is independent of the remaining NAT-* axioms of this ASN. Left and right cancellation are independent of each other because the NAT-* axioms do not include commutativity of addition on ℕ — without `m + n = n + m`, neither cancellation form is derivable from the other. Summand absorption in the posited form `m + n = m ⟹ n = 0` is independent of cancellation because its derivation would require the right identity `m + 0 = m`, and NAT-closure supplies only the left identity `0 + n = n`; without commutativity, that left identity cannot be rearranged into the right identity that a cancellation-based derivation would need.

The mirror form `n + m = m ⟹ n = 0` is deliberately not listed as a separate clause because it is a theorem of the three clauses above together with NAT-closure. From the hypothesis `n + m = m` and NAT-closure's left identity `0 + m = m` we have `n + m = 0 + m`; right cancellation, instantiated at `p := 0`, then delivers `n = 0`. Listing it would make the axiom set non-minimal; the asymmetry with the posited form is itself a consequence of NAT-closure's decision to axiomatize only the left identity.

Two primitives appear in these clauses that are not introduced here. The binary operation `+` is the one posited by NAT-closure's signature clause `+ : ℕ × ℕ → ℕ`; all three clauses use `+` at exactly that arity. The literal `0` appearing on the right-hand side of the absorption clause is the `0 ∈ ℕ` posited by NAT-zero — NAT-cancel introduces no constant of its own, so without NAT-zero supplying the symbol the absorption conclusion `n = 0` would reference an ungrounded literal. NAT-closure and NAT-zero are therefore both declared in the Depends slot; NAT-zero is named directly rather than reached transitively through NAT-closure, matching the precedent NAT-closure itself sets where NAT-zero is declared as the supplier of the literal `0` appearing in its left-identity clause `0 + n = n`.

*Formal Contract:*
- *Axiom:* `(A m, n, p ∈ ℕ : m + n = m + p : n = p)` (left cancellation); `(A m, n, p ∈ ℕ : n + m = p + m : n = p)` (right cancellation); `(A m, n ∈ ℕ : m + n = m : n = 0)` (summand absorption).
- *Depends:*
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies the binary operation `+ : ℕ × ℕ → ℕ` used in all three axiom clauses.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal `0` on the right-hand side of the absorption clause `m + n = m ⟹ n = 0`; named directly rather than reached transitively through NAT-closure, following the same precedent NAT-closure uses to declare NAT-zero as the supplier of the literal `0` in its left-identity clause.
