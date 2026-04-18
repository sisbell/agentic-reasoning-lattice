**NAT-cancel (NatAdditionCancellation).** Addition on ℕ is cancellative on either side, and a sum equals one of its summands only when the other is zero.

Four related facts are stated together as one axiom because they all extract constraints on a summand from an identity between sums:

- Left cancellation: `m + n = m + p ⟹ n = p` for every `m, n, p ∈ ℕ`.
- Right cancellation: `n + m = p + m ⟹ n = p` for every `m, n, p ∈ ℕ`.
- Summand absorption, standard form: `m + n = m ⟹ n = 0` for every `m, n ∈ ℕ`. When the candidate-zero summand `n` appears on the right of `m`, the equality `m + n = m` forces `n = 0`.
- Summand absorption, symmetric form: `n + m = m ⟹ n = 0` for every `m, n ∈ ℕ`. When the candidate-zero summand `n` appears on the left of `m`, the equality `n + m = m` forces `n = 0`.

Both summand-absorption forms are stated as independent axiom clauses because T0's exhaustive NAT-* enumeration does not include commutativity of addition on ℕ, so neither form is derivable from the other within this axiom system. The bundling parallels NAT-addcompat, whose left and right order-compatibility clauses are likewise stated independently because the two cannot be collapsed in the absence of commutativity — "summand absorption" is understood here to cover both placements of the zero-forced summand, just as "order compatibility of addition on either side" covers both placements of the fixed summand.

These are standard properties of ℕ, stated here as an axiom so downstream proofs can cite them directly. The ASN's convention (T0) is that each proof cites only the ℕ facts it actually uses; cancellation is used in TA-LC (both to pass from `aₖ + xₖ = aₖ + yₖ` to `xₖ = yₖ` at the common action point, and to pass from `a_{k₁} + x_{k₁} = a_{k₁}` to `x_{k₁} = 0` in the case-contradictions that eliminate unequal action points — each via summand absorption's standard form), in TA-MTO (to pass from `aₖ + wₖ = bₖ + wₖ` to `aₖ = bₖ` via right cancellation), and in TumblerAdd's dominance proof (to rule out the equality disjunct `aₖ + wₖ = wₖ` via summand absorption's symmetric form, instantiated at `n = aₖ, m = wₖ` — the right-side route through NAT-closure's additive-identity rewrite of `aₖ + wₖ = wₖ` into `aₖ + wₖ = 0 + wₖ` followed by right cancellation is available but not taken, because the symmetric form is stated as an axiom and consumes the equality in a single step). Without an explicit axiom those citations would appeal to background arithmetic, breaking the citation policy that the other NAT-* axioms enforce.

*Formal Contract:*
- *Axiom:* `(A m, n, p ∈ ℕ : m + n = m + p : n = p)` (left cancellation); `(A m, n, p ∈ ℕ : n + m = p + m : n = p)` (right cancellation); `(A m, n ∈ ℕ : m + n = m : n = 0)` (summand absorption, standard form); `(A m, n ∈ ℕ : n + m = m : n = 0)` (summand absorption, symmetric form).
