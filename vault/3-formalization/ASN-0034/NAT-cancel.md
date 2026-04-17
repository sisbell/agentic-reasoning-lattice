**NAT-cancel (NatAdditionCancellation).** Addition on ℕ is cancellative on either side, and a sum equals one of its summands only when the other is zero.

Three related facts are stated together as one axiom because they all extract constraints on a summand from an identity between sums:

- Left cancellation: `m + n = m + p ⟹ n = p` for every `m, n, p ∈ ℕ`.
- Right cancellation: `n + m = p + m ⟹ n = p` for every `m, n, p ∈ ℕ`.
- Summand absorption: `m + n = m ⟹ n = 0` for every `m, n ∈ ℕ` (and symmetrically, `n + m = m ⟹ n = 0`).

These are standard properties of ℕ, stated here as an axiom so downstream proofs can cite them directly. The ASN's convention (T0) is that each proof cites only the ℕ facts it actually uses; cancellation is used in TA-LC (both to pass from `aₖ + xₖ = aₖ + yₖ` to `xₖ = yₖ` at the common action point, and to pass from `a_{k₁} + x_{k₁} = a_{k₁}` to `x_{k₁} = 0` in the case-contradictions that eliminate unequal action points) and in TA-MTO (to pass from `aₖ + wₖ = bₖ + wₖ` to `aₖ = bₖ`). Without an explicit axiom those citations would appeal to background arithmetic, breaking the citation policy that the other NAT-* axioms enforce.

*Formal Contract:*
- *Axiom:* `(A m, n, p ∈ ℕ : m + n = m + p : n = p)` (left cancellation); `(A m, n, p ∈ ℕ : n + m = p + m : n = p)` (right cancellation); `(A m, n ∈ ℕ : m + n = m : n = 0)` and `(A m, n ∈ ℕ : n + m = m : n = 0)` (summand absorption).
