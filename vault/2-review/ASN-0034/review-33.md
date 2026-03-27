# Proof Verification: T3

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
