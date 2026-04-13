# Proof Review — ASN-0036 (cycle 5)

*2026-04-12 19:44*

5 properties (D-CTG, D-CTG-depth, D-MIN, D-SEQ, ValidInsertionPosition)

### D-CTG

**Checking the proof of D-CTG...**

The axiom is a design requirement (stated, not derived). The proof targets the postcondition: D-CTG + S8-fin + S8-depth force all depth-≥-3 V-positions in a subspace to share components 2 through m−1.

**Proof structure review:**

- Contradiction setup: assume v₁ < v₂ disagree at component j ∈ {2, …, m−1}. Component 1 excluded since both share subspace S. Component m excluded since it's the last (allowed to differ). Correct and exhaustive.
- Construction of w: well-defined for all j in range. When j = m−1, the "wᵢ = 1 for j+2 ≤ i ≤ m" clause is vacuous — correctly noted as "(if any such positions exist)".
- **w > v₁**: agrees on 1…j, at j+1: n > (v₁)\_{j+1}. Lexicographic ordering gives w > v₁. ✓
- **w < v₂**: agrees on 1…j−1 (inherited from v₁/v₂ agreement), at j: wⱼ = (v₁)ⱼ < (v₂)ⱼ. ✓
- D-CTG forces w ∈ V\_S(d). Unboundedly many n (T0(a)) produce distinct tumblers (T3), contradicting S8-fin. ✓

**Checklist results:**

1. **Precondition completeness** — ✓. S8-depth provides equal depth; the case split on j covers exactly {2, …, m−1}.
2. **Case coverage** — ✓. j=1 excluded by shared subspace, j=m is the last component (permitted to differ), both boundary values of j in range handled.
3. **Postcondition establishment** — ✓. Shows disagreement at any middle component is impossible, so all pairs agree on components 2 through m−1.
4. **All conjuncts addressed** — ✓. Axiom stated as design requirement; postcondition proved by contradiction.
5. **Dependency correctness** — **ISSUE.** The proof invokes **T1(i)** (lexicographic ordering) three times — to establish the first-disagreement characterization, to show w > v₁, and to show w < v₂ — but T1(i) is not declared as a dependency.
6. **Formal contract** — ✓. Axiom matches the stated universal contiguity condition. Postcondition correctly captures the derived restriction for depth ≥ 3, with S8-depth implicitly guaranteeing #v₂ = #v₁.
7. **Missing guarantees** — Covered by item 5 (T1(i)).

```
RESULT: FOUND

**Problem**: The proof references T1(i) (lexicographic ordering of tumblers, ASN-0034) three times — for the first-disagreement characterization of v₁ < v₂, for w > v₁, and for w < v₂ — but T1(i) is not listed as a dependency. All three ordering arguments are essential to the contradiction.

**Required**: Add T1(i) (ASN-0034) to the declared dependencies of D-CTG.
```

### D-CTG-depth

## Verification of D-CTG-depth (SharedPrefixReduction)

**Logical structure**: The contradiction argument is sound. The construction of intermediates w, the ordering verification (v₁ < w < v₂), and the infinity argument via T0(a)/T3 are all correct. Case coverage is complete: the edge case j = m − 1 (empty tail range) is acknowledged, and the argument works uniformly for all j ∈ {2, …, m − 1}.

**Checklist item 5 — Dependency correctness**: The proof invokes **T1(i) (LexicographicOrder, ASN-0034)** three times, but T1(i) is not listed in the dependency section:

1. *"the inequality follows from v₁ < v₂ by T1(i)"* — deriving (v₁)ⱼ < (v₂)ⱼ from v₁ < v₂
2. *"by T1(i), w > v₁"* — from agreement on 1..j and w_{j+1} > (v₁)_{j+1}
3. *"by T1(i), w < v₂"* — from agreement on 1..j−1 and w_j < (v₂)_j

These ordering arguments are the backbone of the proof — they establish the v₁ < w < v₂ sandwich that triggers D-CTG. All other dependencies (D-CTG, S8-depth, S8-fin, T0(a), T3, T4) are both declared and used correctly.

```
RESULT: FOUND

**Problem**: T1(i) (LexicographicOrder, ASN-0034) is used three times in the proof
for the critical ordering arguments (v₁ < w and w < v₂) but is not declared in the
dependency list. The five ASN-0034 dependencies listed are T0(a), T3, and T4 — T1(i)
is missing.

**Required**: Add T1(i) (LexicographicOrder, ASN-0034) to the declared dependencies
for D-CTG-depth.
```

3 verified, 2 found.

## Result

Not converged after 5 cycles. 0 findings remain.

*Elapsed: 1894s*
