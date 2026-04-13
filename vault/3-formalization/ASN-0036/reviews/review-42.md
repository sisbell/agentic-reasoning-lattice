# Proof Review — ASN-0036 (cycle 5)

*2026-04-12 17:21*

5 properties (D-CTG, D-CTG-depth, D-MIN, D-SEQ, ValidInsertionPosition)

### D-CTG

**Checking the proof against the verification checklist:**

1. **Precondition completeness** — Fine. Assumes v₁, v₂ ∈ V_S(d) with v₁ < v₂ and depth m ≥ 3 (from S8-depth). The contradiction target (first disagreement at j ∈ {2,…,m−1}) correctly captures the negation of the postcondition.

2. **Case coverage** — Fine. If j = m−1 then j+1 = m (last component), and the "w_i = 1 for j+2 ≤ i ≤ m" clause is vacuous. If j = 2, the construction fills components 4..m with 1. Both edge cases work.

3. **Postcondition establishment** — Fine. Contradiction from S8-fin rules out any disagreement at components 2 through m−1, establishing the postcondition.

4. **All conjuncts addressed** — Fine. The axiom is stated as a design requirement; the postcondition is proved.

5. **Dependency correctness** — **Problem found.** The proof invokes **T1(i)** three times:
   - "(v₁)ⱼ < (v₂)ⱼ (since v₁ < v₂ by T1(i))"
   - "By T1(i), w > v₁"
   - "By T1(i), w < v₂"

   T1(i) — the lexicographic ordering definition for tumblers — is **used but not declared** in the dependency list. The provided dependencies are S8-fin, S8-depth, T0(a), and T3. T1(i) is not derivable from any of these; it is a separate property from ASN-0034.

6. **Formal contract** — Correct. Axiom + Postconditions is the right shape. The postcondition formula matches what the proof establishes.

7. **Missing guarantees** — No missing guarantees beyond the undeclared T1(i).

```
RESULT: FOUND

**Problem**: T1(i) (lexicographic ordering of tumblers, ASN-0034) is used three times in the proof but is not declared as a dependency. The proof relies on T1(i) to establish both that the first disagreement component satisfies (v₁)ⱼ < (v₂)ⱼ, and that the constructed intermediate w satisfies v₁ < w < v₂.
**Required**: Add T1(i) from ASN-0034 to the declared dependency list for D-CTG.
```

### D-CTG-depth

Looking at the proof against the verification checklist:

**1. Precondition completeness** — All required conditions are stated: V_S(d) non-empty, common depth m ≥ 3, D-CTG, S8-fin. ✓

**2. Case coverage** — The contradiction proof handles all j with 2 ≤ j ≤ m − 1. Boundary j = m − 1 means j + 1 = m, so the "wᵢ = 1 for j + 2 ≤ i ≤ m" clause is vacuous — handled correctly by the parenthetical. Component count: j + 1 + (m − j − 1) = m. ✓

**3. Postcondition establishment** — The contradiction establishes shared components 2 through m − 1. Since component 1 is the subspace (shared by definition), only component m can vary, so contiguity reduces to the last component. ✓

**4. All conjuncts** — Both parts of the postcondition (shared prefix and reduction to last-component contiguity) are addressed. ✓

**5. Dependency correctness** — T1(i) (LexicographicOrder, ASN-0034) is invoked three times in the proof:
- to establish (v₁)ⱼ < (v₂)ⱼ at the first disagreeing component,
- to show w > v₁ (first disagreement at j + 1, where wⱼ₊₁ = n > (v₁)ⱼ₊₁),
- to show w < v₂ (first disagreement at j, where wⱼ = (v₁)ⱼ < (v₂)ⱼ).

T1(i) is **not declared as a dependency**. Without it, none of the three ordering arguments are grounded.

Additionally, T4 (HierarchicalParsing) is declared as a dependency but is only referenced in post-∎ commentary ("position 0 is structurally unavailable since zero serves as a field separator (T4, ASN-0034)"), not in the proof itself.

**6. Formal contract** — Preconditions and postconditions match the proof's assumptions and conclusions. The contract correctly uses Preconditions + Postconditions fields. ✓

**7. Missing guarantees** — The lexicographic ordering guarantee used three times is not established by any of the provided dependencies. T1(i) is the missing property. ✗

```
RESULT: FOUND

**Problem**: T1(i) (LexicographicOrder, ASN-0034) is used three times in the proof but is not declared as a dependency. The proof invokes it to establish (v₁)ⱼ < (v₂)ⱼ ("the inequality follows from v₁ < v₂ by T1(i)"), w > v₁ ("By T1(i), w > v₁"), and w < v₂ ("By T1(i), w < v₂"). These are the three critical ordering steps; without T1(i), the proof has no grounding for any of them. Separately, T4 (HierarchicalParsing) is declared as a dependency but appears only in post-∎ commentary, not in the proof.

**Required**: Add T1(i) (LexicographicOrder, ASN-0034) to the dependency list. Remove T4 from the dependency list (or relocate the T4 reference into the proof body if it is needed).
```

3 verified, 2 found.

## Result

Not converged after 5 cycles. 0 findings remain.

*Elapsed: 2860s*
