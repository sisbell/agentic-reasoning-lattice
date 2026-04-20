# Proof Verification: OrdinalDisplacement

Looking at the **OrdinalDisplacement** property:

This is a pure **definition** — it constructs δ(n, m) = [0, ..., 0, n] of length m with action point m, given n ≥ 1 and m ≥ 1.

**Checklist**:

1. **Precondition completeness** — n ≥ 1, m ≥ 1 are stated. Complete.
2. **Case coverage** — N/A (definition, not a case proof).
3. **Postcondition establishment** — N/A (definition).
4. **All conjuncts addressed** — The definition specifies: length m, zeros at positions 1..m−1, n at position m, action point m. All parts stated.
5. **Dependency correctness** — No dependencies declared, none used. Consistent.
6. **Formal contract** — No `*Formal Contract:*` section present.
7. **Missing guarantees** — None.

```
RESULT: FOUND

**Problem**: The property section has no `*Formal Contract:*` block. As a definition, it requires:

```
*Formal Contract:*
- *Definition:* δ(n, m) = [0, ..., 0, n] of length m, action point m
```

**Required**: Append the formal contract to the OrdinalDisplacement property section.
```
