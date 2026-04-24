**NAT-addcompat (NatAdditionOrderAndSuccessor).** Addition on ℕ is compatible with the order on either side, and `n < n + 1` for every `n ∈ ℕ`.

- Left order compatibility: `p ≤ n ⟹ m + p ≤ m + n` for every `m, n, p ∈ ℕ`.
- Right order compatibility: `p ≤ n ⟹ p + m ≤ n + m` for every `m, n, p ∈ ℕ`.
- Strict successor inequality: `n < n + 1` for every `n ∈ ℕ`.

Left and right order compatibility are stated as independent clauses because the NAT-* axioms of this ASN do not declare commutativity of addition on ℕ — without `m + n = n + m`, neither compatibility form is derivable from the other. Both-sided coverage is the foundation's deliberate substitute for the absent commutativity axiom: downstream consumers that lift `p ≤ n` through left-addition (obtaining `m + p ≤ m + n`) versus right-addition (obtaining `p + m ≤ n + m`) cite their respective forms directly rather than routing through a single form plus commutativity, matching the same design choice NAT-sub makes for its right/left-inverse pair and NAT-cancel makes for its left/right cancellation pair.

The left/right compatibility clauses invoke the non-strict `≤` *defined* in NAT-order (by `m ≤ n ⟺ m < n ∨ m = n`) and the binary addition closed over ℕ by NAT-closure; the strict successor inequality uses NAT-order's primitive strict relation `<` together with that same closed addition and NAT-closure's `1 ∈ ℕ`. Both foundations are declared in the Depends slot so that the axiom body can be read without silently importing them.

*Formal Contract:*
- *Axiom:* `(A m, n, p ∈ ℕ : p ≤ n : m + p ≤ m + n)` (left order compatibility); `(A m, n, p ∈ ℕ : p ≤ n : p + m ≤ n + m)` (right order compatibility); `(A n ∈ ℕ :: n < n + 1)` (strict successor inequality).
- *Depends:*
  - NAT-order (NatStrictTotalOrder) — supplies the primitive strict order `<` (used in the strict successor inequality `n < n + 1`) and its non-strict companion `≤` (defined by `m ≤ n ⟺ m < n ∨ m = n`, used in the antecedents `p ≤ n` and the consequents `m + p ≤ m + n` and `p + m ≤ n + m` of both compatibility clauses).
  - NAT-closure (NatArithmeticClosureAndIdentity) — posits `1 ∈ ℕ` and closes ℕ under addition, so every sum `m + p`, `m + n`, `p + m`, `n + m`, and `n + 1` appearing in the axiom lies in ℕ, and the successor inequality `n < n + 1` compares two ℕ-elements.
