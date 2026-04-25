# Cone Review — ASN-0036/S8 (cycle 4)

*2026-04-14 18:07*

Looking at this carefully, checking every precondition chain, quantifier scope, and cross-property dependency against the foundation statements.

### ℕ discreteness invoked from T0 but not provided by T0's formal contract

**Foundation**: T0 (CarrierSetDefinition: "ℕ is closed under successor and addition")
**ASN**: S8 proof, within-subspace uniqueness (j = m case): `"Since tumbler components are natural numbers (T0, ASN-0034), v_m ≤ t_m < v_m + 1 forces t_m = v_m."` Also S8 proof, m = 1 cross-subspace case: `"S ≤ k < S + 1 with k ∈ ℕ (T0, ASN-0034) forces k = S"` and `"if t₁ > S₁ then t₁ ≥ S₁ + 1 (since t₁, S₁ ∈ ℕ by T0, ASN-0034)"`
**Issue**: S8's partition proof relies on ℕ discreteness in at least three places — the property that no natural number lies strictly between n and n+1. Each invocation cites T0. But T0's formal contract states only that ℕ is closed under successor and addition. Discreteness (equivalently: for m, n ∈ ℕ, m > n implies m ≥ n + 1) is a consequence of the Peano induction axiom, which T0 does not state. The gap is distinct from finding #4 (which is about T0 being absent from S8's dependency *enumeration*): even if T0 were properly enumerated — resolving finding #4 — a formalizer tracing the chain from T0's contract to "v_m ≤ t_m < v_m + 1 forces t_m = v_m" would find no stated axiom that closes the step. The inference depends on the convention that the symbol "ℕ" imports the full Peano theory, but the formal contract restricts itself to two closure properties and leaves the rest implicit.
**What needs resolving**: Either T0's formal contract should state the properties of ℕ that downstream proofs actually use (at minimum discreteness, or equivalently induction/well-ordering), or the proof should derive discreteness from stated axioms rather than citing T0 as if it provides it directly.
