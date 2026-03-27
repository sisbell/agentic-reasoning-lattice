### [REVIEW-32] [FOUND] T3
Looking at T3's proof against the verification checklist:

**1. Precondition completeness** — Fine. Requires a, b ∈ T.

**2. Case coverage** — Both directions of the biconditional are addressed.

**3. Postcondition establishment** — Both directions are explicitly shown with clear reasoning.

**4. All conjuncts addressed** — Forward and reverse both proved. ✓

**5. Dependency correctness** — The proof explicitly states: "By T0, T is the set of all finite sequences over ℕ." This is the load-bearing premise — the entire argument rests on the carrier set definition from T0. Yet the dependency list declares **(none)**.

Furthermore, the formal contract labels T3 as an **Axiom**, but the proof itself *derives* T3 from T0: "T3 is not derived from other properties; it holds by the definition of the carrier set. By T0, T is the set of all finite sequences over ℕ." These two claims are in tension — the proof simultaneously says it is not derived and then derives it from T0. Either T3 is an axiom (needing no justification from T0) or it is a consequence of T0 (making it derived, not axiomatic, and requiring T0 as a declared dependency).

**6. Formal contract** — The formal contract content accurately captures the property statement. The biconditional matches. However, the **Axiom** label is inconsistent with the proof's own derivation from T0.

**7. Missing guarantees** — No guarantees are assumed beyond T0.

```
RESULT: FOUND

**Problem**: The proof invokes T0 ("By T0, T is the set of all finite sequences over ℕ") as its central justification, but declares no dependencies. The formal contract labels T3 as an *Axiom*, which contradicts the proof body's own derivation from T0. The proof cannot simultaneously claim "not derived from other properties" and then cite T0 as the ground on which it stands.

**Required**: Either (a) declare T0 as a dependency, change the formal contract from *Axiom* to a derived form (e.g., *Postconditions* or a simple theorem statement), and remove the claim "T3 is not derived from other properties"; or (b) if T3 is genuinely intended as an axiom that stands independently, remove the appeal to T0 from the proof and state that sequence extensionality is adopted as a primitive design commitment, not derived from the carrier-set definition.
```

### [REVIEW-33] [FOUND] T3
## Verification

**Checklist walkthrough:**

1. **Precondition completeness** — The proof requires `a, b ∈ T` and that T is the set of finite sequences over ℕ (from T0). Complete.

2. **Case coverage** — Both directions of the biconditional are proved. Empty sequences (length 0) are handled: forward direction holds vacuously (no components to compare, lengths both 0), reverse direction trivially. Fine.

3. **Postcondition establishment** — Forward direction: extensional sequence equality. Reverse direction: Leibniz's law. Both sound and explicitly shown. The "no quotient/normalization" design commitment is addressed in the concluding paragraph. Matches the formal contract.

4. **All conjuncts addressed** — Two directions of the biconditional, both proved. ✓

5. **Dependency correctness** — The proof explicitly states: *"T3 is derived from T0's characterisation of the carrier set. By T0, T is the set of all finite sequences over ℕ."* Yet the dependency list declares **(none)**. T0 is used but not declared.

6. **Formal contract** — The postcondition `a = b ⟺ #a = #b ∧ (∀ i : 1 ≤ i ≤ #a : aᵢ = bᵢ)` matches the property statement. The "Postconditions" label is reasonable for a derived property (consistent with the recent Axiom→Postconditions revision). Contract matches narrative.

7. **Missing guarantees** — The proof's correctness depends entirely on T0 defining T as bare finite sequences over ℕ with no quotient structure. Without T0 declared, this cannot be verified against the actual statement.

---

```
RESULT: FOUND

**Problem**: The proof explicitly derives T3 from T0 — "T3 is derived from T0's
characterisation of the carrier set. By T0, T is the set of all finite sequences
over ℕ" — but the dependency list declares (none). T0 is the sole load-bearing
dependency and is undeclared.

**Required**: Add T0 (carrier set definition) as a declared dependency of T3.
```
