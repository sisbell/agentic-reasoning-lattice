**NAT-closure (NatArithmeticClosureAndIdentity).** ℕ is closed under successor and addition, with `0` as the additive identity.

For every `n ∈ ℕ`, the successor `n + 1 ∈ ℕ`. For every `m, n ∈ ℕ`, the sum `m + n ∈ ℕ`. The additive identity holds: `0 + n = n` for every `n ∈ ℕ`.

These are standard properties of ℕ, stated here as an axiom so downstream proofs can cite them directly without appealing to an implicit "standard properties of natural numbers" clause.

*Formal Contract:*
- *Axiom:* `(A n ∈ ℕ :: n + 1 ∈ ℕ)` (successor closure); `(A m, n ∈ ℕ :: m + n ∈ ℕ)` (addition closure); `(A n ∈ ℕ :: 0 + n = n)` (additive identity).
