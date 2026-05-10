# Proof Verification: S3

**Checking the proof against the verification checklist:**

1. **Precondition completeness** — Base case assumes `dom(Σ₀.M(d)) = ∅` for all `d` (reasonable initial-state assumption). Inductive step uses S1 and the arrangement axiom. ✓

2. **Case coverage** — Case 1 condition: `v ∈ dom(Σ.M(d)) ∧ Σ'.M(d)(v) = Σ.M(d)(v)`. Case 2 condition: `v ∉ dom(Σ.M(d)) ∨ Σ'.M(d)(v) ≠ Σ.M(d)(v)`. These are logical complements — exhaustive. ✓

3. **Postcondition establishment** — Both cases conclude `Σ'.M(d)(v) ∈ dom(Σ'.C)` for arbitrary `d, v`. ✓

4. **All conjuncts addressed** — Single universal quantification, no conjunction. ✓

5. **Dependency correctness** — S1 is declared and used in Case 1 (preserved mapping chain: `dom(Σ.C) ⊆ dom(Σ'.C)`). No undeclared dependencies used. ✓

6. **Formal contract** — Issue found. The proof explicitly relies on S1 in Case 1: without store monotonicity, a preserved mapping's I-address target could leave `dom(C)`, breaking referential integrity for unchanged mappings. The formal contract lists the arrangement axiom and the invariant but omits S1 as a precondition entirely. Compare with S1's own formal contract, which lists its dependency on S0 as a precondition: `"Preconditions: State transition Σ → Σ' in a system satisfying S0."` S3 should follow the same pattern.

7. **Missing guarantees** — The arrangement axiom is explicitly declared. No hidden assumptions. ✓

```
RESULT: FOUND

**Problem**: The formal contract omits the dependency on S1 (store monotonicity).
Case 1 of the inductive step chains through S1: `Σ.M(d)(v) ∈ dom(Σ.C) ⊆ dom(Σ'.C)` —
the subset inclusion `dom(Σ.C) ⊆ dom(Σ'.C)` IS S1. Without it, a preserved mapping's
target could vanish from `dom(C)` across a transition, and the case fails.
S1's own formal contract sets the precedent by listing its dependency on S0 as a
precondition. S3's contract should do likewise.

**Required**: Add a Preconditions field to the formal contract:

*Formal Contract:*
- *Preconditions:* State transitions satisfy S1 (store monotonicity).
- *Axiom:* Every arrangement-modifying operation introducing a mapping `M(d)(v) = a` ensures `a ∈ dom(Σ'.C)` in the post-state.
- *Invariant:* `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`
```
