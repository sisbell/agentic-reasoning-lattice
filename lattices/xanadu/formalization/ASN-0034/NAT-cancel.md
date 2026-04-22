**NAT-cancel (NatAdditionCancellation).** Addition on ℕ is cancellative on either side, and a sum equals one of its summands only when the other is zero.

- Left cancellation: `m + n = m + p ⟹ n = p` for every `m, n, p ∈ ℕ`.
- Right cancellation: `n + m = p + m ⟹ n = p` for every `m, n, p ∈ ℕ`.
- Summand absorption, standard form: `m + n = m ⟹ n = 0` for every `m, n ∈ ℕ`.
- Summand absorption, symmetric form: `n + m = m ⟹ n = 0` for every `m, n ∈ ℕ`.

Both summand-absorption forms are stated independently because the NAT-* axioms of this ASN do not include commutativity of addition on ℕ, so neither form is derivable from the other. The same reason governs the independent statement of left and right cancellation.

*Formal Contract:*
- *Axiom:* `(A m, n, p ∈ ℕ : m + n = m + p : n = p)` (left cancellation); `(A m, n, p ∈ ℕ : n + m = p + m : n = p)` (right cancellation); `(A m, n ∈ ℕ : m + n = m : n = 0)` (summand absorption, standard form); `(A m, n ∈ ℕ : n + m = m : n = 0)` (summand absorption, symmetric form).
