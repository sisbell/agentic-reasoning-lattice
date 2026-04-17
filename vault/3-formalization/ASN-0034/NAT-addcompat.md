**NAT-addcompat (NatAdditionOrderCompatibility).** Addition on ℕ is compatible with the order on either side, and `n < n + 1` for every `n ∈ ℕ`.

Three related facts are stated together as one axiom because they all concern the interaction between addition and `<` on ℕ:

- Left order compatibility: `n ≥ p ⟹ m + n ≥ m + p` for every `m, n, p ∈ ℕ`. Adding the same natural number on the left preserves the order.
- Right order compatibility: `n ≥ p ⟹ n + m ≥ p + m` for every `m, n, p ∈ ℕ`. Adding the same natural number on the right preserves the order.
- Strict successor inequality: `n < n + 1` for every `n ∈ ℕ`. The successor is strictly greater.

Both order-compatibility forms are stated explicitly because downstream proofs supply the fixed summand on either side: TumblerAdd, TA5, T10a-N, and T0(a) add the fixed term on the left of the variable summands, while TA1's sub-case `j = k` adds the fixed increment `wₖ` on the right of the variable summands `aₖ`, `bₖ` to promote `aₖ < bₖ` into `aₖ + wₖ < bₖ + wₖ`. The ASN's convention (T0) is that each proof cites only the ℕ facts it actually uses; without the right-addition clause stated as an axiom, TA1's right-added step would tacitly assume commutativity of addition on ℕ, breaking the citation policy that the other NAT-* axioms enforce. Downstream proofs use the order-compatibility facts to lift inequalities through arithmetic and the strict successor inequality to bound lengths or indices under incrementing operations.

*Formal Contract:*
- *Axiom:* `(A m, n, p ∈ ℕ : n ≥ p : m + n ≥ m + p)` (left order compatibility); `(A m, n, p ∈ ℕ : n ≥ p : n + m ≥ p + m)` (right order compatibility); `(A n ∈ ℕ :: n < n + 1)` (strict successor inequality).
