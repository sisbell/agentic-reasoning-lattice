# Proof Review — ASN-0034 (cycle 2)

*2026-04-15 18:56*

38 properties (D0, D1, Divergence, GlobalUniqueness, OrdinalDisplacement, OrdinalShift, PartitionMonotonicity, PositiveTumbler, Prefix, ReverseInverse, T1, T10, T10a, T10a.3, T10a.4, T2, T3, T4, T4a, T4b, T4c, T5, T6, T7, T8, TA-LC, TA-MTO, TA-RC, TA-assoc, TA1, TA3, TA3-strict, TA5-SigValid, TA5a, TA6, TS2, TS3, TumblerSub)

### TS3

## Verification of TS3 (ShiftComposition)

**Checklist 1 – Precondition completeness:** All inputs stated: v ∈ T, n₁ ≥ 1, n₂ ≥ 1, #v = m. The constraint m ≥ 1 is implicit from v ∈ T (by T0). Sufficient.

**Checklist 2 – Case coverage:** The proof handles the general case. The action point k = m is always within bounds since k = m ≤ m = #v. The second shift's precondition k = m ≤ m = #u is justified via the result-length identity. No edge cases are missed given n₁ ≥ 1, n₂ ≥ 1.

**Checklist 3 – Postcondition establishment:** Both sides are computed component-wise, shown to agree at every position (prefix copy from v, associativity of ℕ at position m), and T3 closes the equality. The postcondition is fully established.

**Checklist 4 – All conjuncts addressed:** Single claim. The frame condition (#shift(shift(v, n₁), n₂) = m) is established via #L = m in the left-side computation.

**Checklist 5 – Dependency correctness:** The proof invokes "By OrdinalShift" three times to expand `shift(v, n) = v ⊕ δ(n, m)` and relies on the definition of δ(n, m) = [0, ..., 0, n] of length m. **OrdinalShift is not listed as a dependency.** TumblerAdd and T3 are declared and used correctly.

**Checklist 6 – Formal contract:** Preconditions, postconditions, and frame all match the proof's narrative. No issues.

**Checklist 7 – Missing guarantees:** No missing guarantees beyond the undeclared dependency.

---

```
RESULT: FOUND

**Problem**: The proof invokes OrdinalShift three times ("By OrdinalShift, shift(v, n₁) = v ⊕ δ(n₁, m)") and depends on the definition of δ(n, m) throughout, but OrdinalShift is not declared as a dependency. Without it, the expansion of `shift` into `⊕` and δ is ungrounded.

**Required**: Add OrdinalShift (which defines both `shift` and `δ`) to the declared dependency list for TS3.
```

37 verified, 1 found.
