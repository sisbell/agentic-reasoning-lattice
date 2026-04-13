# Proof Review — ASN-0036 (cycle 4)

*2026-04-12 19:38*

5 properties (D-CTG, D-CTG-depth, D-MIN, D-SEQ, ValidInsertionPosition)

### D-CTG

Looking at the proof against the verification checklist:

**1–4, 6–7: Sound.** The contradiction argument is correctly constructed — the intermediate tumblers w are well-defined, the ordering v₁ < w < v₂ holds, and distinct n values yield infinitely many distinct positions via T3, contradicting S8-fin. Case coverage is complete (j ranges over {2,…,m−1}; the j=m case is the non-contradictory scenario where positions already agree on 2..m−1). The formal contract accurately reflects the axiom and postcondition.

**5: Dependency correctness — gap found.**

T1(i) (lexicographic ordering from ASN-0034) is used three times in the proof:
- "since v₁ < v₂ by T1(i)" in the setup
- "By T1(i), w > v₁" — ordering at component j+1
- "By T1(i), w < v₂" — ordering at component j

Yet T1(i) is not listed in the dependency set. The entire ordering argument — establishing v₁ < w < v₂ so that D-CTG's universal quantifier applies to w — depends on T1(i)'s lexicographic comparison rule. T0(a) and T3 from the same ASN are declared; T1(i) was omitted.

```
RESULT: FOUND

**Problem**: T1(i) (LexicographicOrder, ASN-0034) is used three times in the proof
to establish the critical ordering relations v₁ < w and w < v₂, but is not declared
as a dependency. Without T1(i), the proof cannot justify that the constructed
intermediate w falls strictly between v₁ and v₂.

**Required**: Add T1(i) (ASN-0034) to the dependency list for D-CTG.
```

### D-SEQ

Looking at the D-SEQ proof carefully against the checklist:

**1. Precondition completeness** — All preconditions stated and used. ✓

**2. Case coverage** — m = 2 and m ≥ 3 cover all m ≥ 2. Single-element case (n = 1) handled: Step 3 is vacuously satisfied, assembly works. ✓

**3. Postcondition establishment** — Steps 1–4 plus assembly establish the claimed set equality. ✓

**4. All conjuncts addressed** — Single main claim fully proved. ✓

**5. Dependency correctness** — Two issues:

- **T1(i) (LexicographicOrder, ASN-0034) is used directly in Step 3 but not declared as a dependency.** Step 3 explicitly invokes "By T1(i) (LexicographicOrder, ASN-0034), v₁ < v₂ since they agree on components 1 through m − 1 and differ first at component m where k₁ < k₂" and again for v₁ < w < v₂. This is a direct invocation, not mediated through D-CTG or D-CTG-depth. The proof cannot establish the ordering of intermediate tuples without T1(i).

- **ValidInsertionPosition is declared as a dependency but never referenced in the proof.** The proof text never mentions ValidInsertionPosition; it is unused.

**6. Formal contract** — Preconditions and postconditions match the narrative. T1(i) is a general theorem (always true), so omitting it from preconditions is defensible — but it should be tracked as a dependency. ✓

**7. Missing guarantees** — No missing guarantees; all invoked properties are sound for their usage. ✓

---

```
RESULT: FOUND

**Problem**: Dependency list mismatch. T1(i) (LexicographicOrder, ASN-0034) is directly
invoked in Step 3 — "By T1(i) (LexicographicOrder, ASN-0034), v₁ < v₂ since they agree
on components 1 through m − 1 and differ first at component m where k₁ < k₂" — but is
not declared as a dependency of D-SEQ. The proof's ordering argument for intermediate
tuples (v₁ < w < v₂) depends on it and cannot proceed without it. Separately,
ValidInsertionPosition is declared as a dependency but never referenced in the proof.

**Required**: (1) Add T1(i) (LexicographicOrder, ASN-0034) to D-SEQ's dependency list.
(2) Remove ValidInsertionPosition from D-SEQ's dependency list (it is not used).
```

3 verified, 2 found.
