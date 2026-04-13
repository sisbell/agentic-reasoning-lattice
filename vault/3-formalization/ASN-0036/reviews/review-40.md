# Proof Review — ASN-0036 (cycle 3)

*2026-04-12 17:12*

10 properties (D-CTG, D-CTG-depth, D-MIN, D-SEQ, OrdAddHom, OrdAddS8a, OrdShiftHom, S8, S8-depth, ValidInsertionPosition)

### D-CTG

I need to verify the D-CTG proof against the checklist.

**Tracing the proof logic:**

The derived postcondition (shared components 2..m−1 at depth ≥ 3) is proved by contradiction. Suppose v₁ < v₂ in V_S(d) first disagree at component j ∈ {2,…,m−1}. Construct w of length m: copy v₁ on components 1..j, set w_{j+1} = n for arbitrary n > (v₁)_{j+1}, set remaining components to 1.

- **w > v₁**: agrees through j, exceeds at j+1. ✓
- **w < v₂**: agrees through j−1, then w_j = (v₁)_j < (v₂)_j. ✓
- **subspace(w) = S, #w = m**: by construction. ✓
- **D-CTG forces w ∈ V_S(d)**: all quantifier conditions met. ✓
- **Infinitely many distinct w**: unbounded n (T0(a)), distinct at component j+1 (T3). ✓
- **Contradicts S8-fin**: infinitely many positions in dom(M(d)). ✓

The case j = m (last component) is correctly excluded from {2,…,m−1}, allowing positions to differ there. The postcondition is fully established.

**Checklist:**

1. **Precondition completeness** — All cases covered: any disagreement in {2,…,m−1} leads to contradiction; depth < 3 excluded by #v₁ ≥ 3 guard. ✓
2. **Case coverage** — All j ∈ {2,…,m−1} handled uniformly. Boundary cases (j=2, j=m−1) verified in the illustrative examples. ✓
3. **Postcondition establishment** — The contradiction proof fully establishes the shared-components claim. ✓
4. **All conjuncts addressed** — Axiom stated; postcondition proved. ✓
5. **Dependency correctness** — The proof cites **T1(i)** three times ("since v₁ < v₂ by T1(i)", "By T1(i), w > v₁", "By T1(i), w < v₂") to justify lexicographic ordering comparisons. T1(i) is **not listed as a dependency**. The proof's ordering arguments rely on the structural property that the first point of disagreement determines the ordering — this is exactly what T1(i) establishes and cannot be derived from S8-fin, S8-depth, T0(a), or T3 alone.
6. **Formal contract** — Axiom + Postconditions structure is appropriate and matches the narrative. ✓
7. **Missing guarantees** — No missing guarantees beyond the undeclared T1(i).

```
RESULT: FOUND

**Problem**: T1(i) (lexicographic ordering on tumblers) is cited three times in the proof but is not declared as a dependency. The proof uses T1(i) to establish both v₁ < w and w < v₂ by reasoning about the first point of component disagreement — this structural property of tumbler ordering is not derivable from the four listed dependencies (S8-fin, S8-depth, T0(a), T3).

**Required**: Add T1(i) from ASN-0034 to the dependency list for D-CTG.
```

### D-CTG-depth

I'll verify D-CTG-depth against the checklist.

**Proof strategy:** Contradiction — assume two positions disagree at some component j with 2 ≤ j ≤ m−1, construct infinitely many intermediates forced into V_S(d) by D-CTG, contradicting S8-fin.

**1. Precondition completeness** — All assumptions stated: V_S(d) non-empty, common depth m ≥ 3 (S8-depth), D-CTG, S8-fin. ✓

**2. Case coverage** — The construction handles all j ∈ {2, …, m−1}. When j = m−1, the "fill with 1" clause is vacuous (j+2 > m), and w_m = n — works correctly. ✓

**3. Postcondition establishment** — The contradiction shows no two positions can disagree at components 2 through m−1, so all positions share those components. Contiguity then reduces to the last component. Both postcondition conjuncts established. ✓

**4. All conjuncts addressed** — Shared-prefix result proved; reduction to last-component contiguity follows. ✓

**5. Dependency correctness** — The proof invokes **T1(i) (LexicographicOrder, ASN-0034)** three times:
- "the inequality follows from v₁ < v₂ by T1(i)"
- "by T1(i), w > v₁"
- "by T1(i), w < v₂"

T1(i) is **not declared** in the dependency list. The provided dependencies are D-CTG, S8-depth, S8-fin, T0(a), T3, T4. T4 is declared and used (Nelson paragraph on zero as field separator). All other declared dependencies are used. But T1(i) is used without being declared.

**6. Formal contract** — Preconditions list V_S(d) non-empty, m ≥ 3, D-CTG, S8-fin. Postconditions state the universal shared-prefix quantifier and the reduction claim. Matches the narrative. ✓

**7. Missing guarantees** — No missing guarantees beyond the undeclared T1(i). The proof's reasoning about lexicographic order is sound given T1(i)'s stated semantics. ✓

```
RESULT: FOUND

**Problem**: T1(i) (LexicographicOrder, ASN-0034) is used three times in the proof
but is not declared in the dependency list. The proof relies on it to establish
v₁ < v₂ ordering from the first disagreeing component, w > v₁ at component j+1,
and w < v₂ at component j — all critical steps in the contradiction argument.

**Required**: Add T1(i) (LexicographicOrder, ASN-0034) to the declared dependencies
of D-CTG-depth.
```

8 verified, 2 found.
