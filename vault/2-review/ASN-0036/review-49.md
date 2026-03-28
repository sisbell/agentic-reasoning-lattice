# Proof Verification: S3

RESULT: FOUND

**Problem**: The proof explicitly introduces an axiom in Case 2 — "We take this as an axiom: every arrangement-modifying operation that introduces a mapping `M(d)(v) = a` ensures `a ∈ dom(Σ'.C)` in the post-state" — but the formal contract does not reflect it. The contract lists only the invariant:

```
*Formal Contract:*
- *Invariant:* `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`
```

This axiom is load-bearing: without it, Case 2 has no justification and the inductive step fails. The narrative describes it as "a design constraint on all arrangement-modifying operations, parallel to S0's constraint on content-store operations," yet unlike S0 (which is a standalone property that S1 depends on), this constraint exists only as inline prose within the proof. It is neither a declared dependency nor captured in the formal contract.

Two checklist items are violated:

- **#6 (Formal contract)**: The narrative states an axiom; the formal contract omits it. The contract does not match the conditions stated in the proof.
- **#7 (Missing guarantees)**: The proof assumes a guarantee — that arrangement-modifying operations ensure target I-addresses exist in `dom(Σ'.C)` — that no provided dependency (S1) establishes. S1 gives domain monotonicity of `C`, but says nothing about what arrangement operations must do.

**Required**: Either:

(a) Add the axiom to the formal contract, e.g.:
```
*Formal Contract:*
- *Axiom:* Every arrangement-modifying operation introducing `M(d)(v) = a` ensures `a ∈ dom(Σ'.C)`.
- *Invariant:* `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`
```

or (b) factor the constraint out as a standalone property (the arrangement analog of S0) and declare it as a dependency of S3 — then add it to the formal contract as a precondition, following the pattern S1 uses for S0.
