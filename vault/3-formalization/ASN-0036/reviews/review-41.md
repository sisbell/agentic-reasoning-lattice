# Proof Review — ASN-0036 (cycle 4)

*2026-04-12 17:17*

5 properties (D-CTG, D-CTG-depth, D-MIN, D-SEQ, ValidInsertionPosition)

### D-CTG

## Verification

The proof's construction is correct: given two positions v₁ < v₂ disagreeing at a non-last component j, the family of witnesses w (parameterized by n) are properly shown to satisfy v₁ < w < v₂ with matching subspace and depth, yielding the desired contradiction with S8-fin via T0(a) and T3. Case coverage is complete (j = m would mean they already share components 2..m−1, and j = 1 is excluded by shared subspace). The formal contract matches the narrative.

However, the proof invokes **T1(i)** three times — to justify that the first point of disagreement determines the ordering of v₁ vs v₂, w vs v₁, and w vs v₂ — yet T1(i) is not listed among the declared dependencies.

```
RESULT: FOUND

**Problem**: T1(i) is used but not declared as a dependency.
The proof text references T1(i) in three places:
  1. "(v₁)ⱼ < (v₂)ⱼ (since v₁ < v₂ by T1(i))"
  2. "By T1(i), w > v₁"
  3. "By T1(i), w < v₂"
All three ordering claims depend on T1(i) providing the lexicographic comparison
rule for tumblers (first differing component determines order). Without T1(i) as
ground truth, these steps cannot be verified from the declared dependencies alone.

**Required**: Add T1(i) (lexicographic ordering of tumblers, ASN-0034) to the
dependency list for D-CTG.
```

4 verified, 1 found.
