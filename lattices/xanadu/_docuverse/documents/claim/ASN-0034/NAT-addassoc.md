**NAT-addassoc (NatAdditionAssociative).** Addition on ℕ is associative: `(m + n) + p = m + (n + p)` for every `m, n, p ∈ ℕ`.

Two primitives appear in the axiom that are not introduced here. The binary operation `+` is the one posited by NAT-closure's signature clause `+ : ℕ × ℕ → ℕ`; the associativity equation uses `+` at exactly that arity, and without NAT-closure supplying the signature the left- and right-hand sides would reference an ungrounded symbol. The carrier `ℕ` governing the quantifier range is the set introduced by NAT-carrier; both prereqs are listed directly, matching the convention the surrounding NAT-* claims follow of naming every directly-used predecessor rather than relying on transitive reachability.

*Formal Contract:*
- *Axiom:* `(A m, n, p ∈ ℕ :: (m + n) + p = m + (n + p))` (associativity of addition on ℕ).
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set over which the bounded universal `(A m, n, p ∈ ℕ :: (m + n) + p = m + (n + p))` of the associativity axiom ranges.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies the binary operation `+ : ℕ × ℕ → ℕ` whose associativity is here posited, ensuring every sum `m + n`, `n + p`, `(m + n) + p`, and `m + (n + p)` appearing in the axiom is an ℕ-element.
