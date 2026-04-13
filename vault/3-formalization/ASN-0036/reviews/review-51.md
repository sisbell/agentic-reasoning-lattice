# Proof Review — ASN-0036 (cycle 3)

*2026-04-12 19:34*

7 properties (D-CTG, D-CTG-depth, D-MIN, D-SEQ, S8, S8-fin, ValidInsertionPosition)

### D-CTG

## Verification of D-CTG

The proof structure is sound: assume two positions v₁ < v₂ disagree at some component j ∈ {2, …, m−1}, construct infinitely many intermediate w's by varying component j+1, invoke D-CTG to force them all into V_S(d), and contradict S8-fin.

The ordering arguments are correct:
- **w > v₁**: agrees on 1..j, wins at j+1 since n > (v₁)_{j+1}. ✓
- **w < v₂**: agrees on 1..j−1, loses at j since w_j = (v₁)_j < (v₂)_j. ✓

The case that j = m (last component) is the complement — it means all components 2 through m−1 agree, which is exactly the postcondition. Coverage is complete.

S8-fin, S8-depth, T0(a), and T3 are all used as claimed. The formal contract correctly separates the axiom (contiguity as a design requirement) from the derived postcondition (shared components for depth ≥ 3).

However, the proof explicitly invokes **T1(i)** three times — once in the setup ("since v₁ < v₂ by T1(i)") and twice in the ordering verification ("By T1(i), w > v₁" and "By T1(i), w < v₂") — to establish that lexicographic comparison is determined by the first point of disagreement. T1(i) is not listed among the declared dependencies.

```
RESULT: FOUND

**Problem**: T1(i) (lexicographic ordering of tumblers, ASN-0034) is used three times in the proof but is not declared as a dependency. The entire contradiction argument relies on T1(i) to establish v₁ < w and w < v₂ from component-wise comparisons at the first point of disagreement.

**Required**: Add T1(i) to the dependency list for D-CTG.
```

### D-CTG-depth

## Verification of D-CTG-depth (SharedPrefixReduction)

**1. Precondition completeness** — All stated: V_S(d) non-empty, common depth m ≥ 3 (S8-depth), D-CTG, S8-fin. Sufficient for the proof. ✓

**2. Case coverage** — The proof handles arbitrary j ∈ {2, …, m−1}. At j = m−1, the range j+2 ≤ i ≤ m is empty (acknowledged in the proof). At j = 2, the construction fills components 3 through m. Component j+1 always exists since j ≤ m−1 implies j+1 ≤ m. ✓

**3. Postcondition establishment** — The contradiction argument correctly shows no two positions can disagree at any component j with 2 ≤ j ≤ m−1, establishing the shared-prefix result. The reduction to last-component contiguity follows immediately: if components 1 through m−1 are fixed, only component m can vary. ✓

**4. All conjuncts addressed** — Both parts of the postcondition (shared components 2 through m−1; reduction to last-component contiguity) are established. ✓

**5. Dependency correctness** — **Issue found.** The proof invokes T1(i) (LexicographicOrder, ASN-0034) three times:
- To conclude (v₁)_j < (v₂)_j from v₁ < v₂ at first disagreement j
- To establish w > v₁ (agreement through j, then n > (v₁)_{j+1} at component j+1)
- To establish w < v₂ (agreement through j−1, then (v₁)_j < (v₂)_j at component j)

T1(i) is not declared in the dependency list and its text is not provided among the dependencies.

**6. Formal contract** — Preconditions and postconditions match the proof's structure. The formal quantified statement correctly captures the shared-prefix result. ✓

**7. Missing guarantees** — No guarantee gaps beyond the undeclared T1(i) dependency.

---

```
RESULT: FOUND

**Problem**: T1(i) (LexicographicOrder, ASN-0034) is used three times in the proof
but is not declared as a dependency. The proof relies on it to establish ordering
at the first point of disagreement: "(v₁)ⱼ < (v₂)ⱼ (the inequality follows from
v₁ < v₂ by T1(i))", "By T1(i), w > v₁", and "By T1(i), w < v₂".

**Required**: Add T1(i) (LexicographicOrder, ASN-0034) to the declared dependency
list for D-CTG-depth.
```

5 verified, 2 found.
