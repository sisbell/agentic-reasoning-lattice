## Correctness

### Issue 1: TA7a misapplied to an increment operation in Scenario 8

**Scenario**: Scenario 8, Step 3 / Properties exercised list
**Property**: TA7a
**Step**: "TA7a: inc(e_text, 0) preserves position-7 value 1; element-local shifts do not touch the subspace identifier ✓"
**Problem**: TA7a governs ⊕ and ⊖ in the ordinal-only formulation. Its formal statement is `(A o ∈ S, w > 0 : k ≤ #o ⟹ o ⊕ w ∈ S)` — shift arithmetic on ordinals, not hierarchical increment. The operation cited (`inc(e_text, 0)`) is governed by TA5(c): "when k = 0: #t' = #t, and t' differs from t only at position sig(t)." Since sig(e_text) = 8, position 7 is untouched — but this is a consequence of TA5(c), not TA7a. Invoking TA7a for an inc operation applies the wrong definition to the wrong case. The factual claim (position 7 is preserved) is correct; the property attribution is wrong.
**Correction**: Replace the TA7a bullet with: "TA5(c): inc(e_text, 0) differs from e_text only at sig(e_text) = 8; position 7 (the subspace identifier) is unchanged, confirming that allocation increments within a subspace do not cross subspace boundaries." TA7a remains genuinely exercised in Scenario 4 (the ordinal round-trip), where ⊕ and ⊖ on ordinals are the actual operations.

---

## Coverage gaps

None. All 25 properties from the Properties Introduced table are exercised non-vacuously across the eleven scenarios. The coverage matrix is complete.

---

```
VERDICT: REVISE
```