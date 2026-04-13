# Proof Review — ASN-0036 (cycle 2)

*2026-04-12 19:28*

11 properties (D-CTG, D-CTG-depth, D-MIN, D-SEQ, S3, S5, S8, S8-fin, S8a, S9, ValidInsertionPosition)

### S8-fin

RESULT: FOUND

**Problem**: The base case relies on an initial-state axiom — "The initial-state axiom (Σ.M(d)) establishes that dom(Σ₀.M(d)) = ∅ for every document d" — but the dependencies section lists "(none)." Whatever property or axiom establishes that every document's mapping domain is empty in the initial state is used but undeclared.

**Required**: Add the initial-state axiom (the property that establishes `dom(Σ₀.M(d)) = ∅` for every document `d`) as an explicit dependency. Additionally, the parenthetical reference "(Σ.M(d))" appears to be a garbled axiom label — it should be corrected to cite the actual label of the axiom being invoked.

### D-CTG

I need to verify the D-CTG proof against the checklist.

**1. Precondition completeness** — The proof assumes v₁, v₂ ∈ V_S(d) with depth m ≥ 3, which follows from S8-depth. The constructed w uses components from v₁ plus positive integers (n > (v₁)ⱼ₊₁ ≥ 1, and padding with 1), so w ∈ T is implicit but correct. ✓

**2. Case coverage** — The proof handles j ∈ {2, …, m−1}. If j = m (disagreement only at the last component), positions already share components 2 through m−1, so the postcondition holds trivially. j = 1 is excluded since both positions have subspace S. ✓

**3. Postcondition establishment** — The contradiction (infinitely many positions via S8-fin) is properly derived. ✓

**4. All conjuncts addressed** — The formal contract's postcondition (shared components 2 through m−1) is fully proved. The narrative mention of "contiguous block at last component" follows from applying the axiom to positions that now share all but the last component — no separate proof needed. ✓

**5. Dependency correctness** — All four declared dependencies are used:
- S8-fin: the contradiction target ✓
- S8-depth: uniform depth within a subspace ✓
- T0(a): unboundedly many n ✓
- T3: distinct n → distinct tumblers ✓

However, **T1(i)** (lexicographic ordering) is cited three times in the proof — "since v₁ < v₂ by T1(i)", "By T1(i), w > v₁", "By T1(i), w < v₂" — but is **not declared as a dependency**.

**6. Formal contract** — Axiom + Postconditions fields are appropriate. The quantified statements match the narrative. ✓

**7. Missing guarantees** — No guarantee is assumed beyond what the dependencies provide (once T1(i) is added).

```
RESULT: FOUND

**Problem**: T1(i) (lexicographic ordering of tumblers, ASN-0034) is used three times in the proof — to establish v₁ < v₂, w > v₁, and w < v₂ — but is not declared as a dependency.

**Required**: Add T1(i) from ASN-0034 to the dependency list for D-CTG.
```

9 verified, 2 found.
