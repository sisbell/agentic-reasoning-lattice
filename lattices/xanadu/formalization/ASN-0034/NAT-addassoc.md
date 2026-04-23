**NAT-addassoc (NatAdditionAssociative).** Addition on ℕ is associative: `(m + n) + p = m + (n + p)` for every `m, n, p ∈ ℕ`.

Two primitives appear in the axiom that are not introduced here. The binary operation `+` is the one posited by NAT-closure's signature clause `+ : ℕ × ℕ → ℕ`; the associativity equation uses `+` at exactly that arity, and without NAT-closure supplying the signature the left- and right-hand sides would reference an ungrounded symbol. The carrier `ℕ` governing the quantifier range is reached through NAT-closure's own Depends chain — NAT-closure depends on NAT-zero, and NAT-zero depends on NAT-order, which is where `ℕ` originates. A single Depends entry on NAT-closure therefore suffices: it grounds `+` directly and `ℕ` transitively, matching the precedent NAT-closure itself sets where only immediate suppliers (NAT-zero for the literal `0`) are named and the carrier is reached through the chain rather than re-declared.

*Formal Contract:*
- *Axiom:* `(A m, n, p ∈ ℕ :: (m + n) + p = m + (n + p))` (associativity of addition on ℕ).
- *Depends:*
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies the binary operation `+ : ℕ × ℕ → ℕ` whose associativity is here posited, and carries the carrier `ℕ` for the quantifier range transitively through its own dependency on NAT-zero and NAT-order.
