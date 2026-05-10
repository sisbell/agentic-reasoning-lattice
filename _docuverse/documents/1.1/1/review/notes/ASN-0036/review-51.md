# Proof Verification: ValidInsertionPosition

## Verification of ValidInsertionPosition

Working through the checklist:

**1. Precondition completeness** — The property assumes d satisfies D-CTG, D-MIN, S8-depth, and S8a. The document-level precondition names only D-CTG ("document d satisfying D-CTG") but freely uses D-MIN, S8-depth, and S8a throughout. This is tolerable for the narrative but would need to be explicit in a formal contract.

**2. Case coverage** — Exhaustive: V_S(d) is either empty or non-empty. The j=0 case correctly handles the OrdinalShift precondition n ≥ 1 by defining it separately as v = min(V_S(d)).

**3. Postcondition establishment** — All structural claims are established with explicit reasoning:
- Explicit form via D-MIN + OrdinalShift + TumblerAdd ✓
- Distinctness via distinct last components + T3 ✓
- Depth preservation via OrdinalShift result-length identity (j ≥ 1) and D-MIN (j = 0) ✓
- Subspace identity via action point m ≥ 2 keeping component 1 unchanged ✓
- S8a consistency via all components strictly positive ✓
- The m ≥ 2 lower bound is justified by the counterexample at m = 1 ✓

**4. All conjuncts addressed** — Each claimed property (distinctness, depth, subspace, S8a, count) is proved.

**5. Dependency correctness** — All declared dependencies are used: D-CTG (constraint on d), D-MIN (minimum position form), S8-depth (common depth), S8a (well-formedness), OrdinalShift (shift definition and result-length), TumblerAdd (component-wise behavior), T3 (distinctness), T4/hierarchical structure (subspace identifier semantics). No undeclared dependencies.

**6. Formal contract** — Missing.

**7. Missing guarantees** — No missing guarantees from dependencies. The reasoning is sound given the provided axioms and definitions.

---

```
RESULT: FOUND

**Problem**: The property has no formal contract section. ValidInsertionPosition is
a definition with verified structural postconditions, but the required
`*Formal Contract:*` block is absent. The checklist requires: "If the formal
contract is missing or incomplete, flag as FOUND."

**Required**: Add a formal contract after the S8a consistency paragraph (before the
examples). It should capture the definition, its preconditions, and the verified
structural guarantees. For example:

*Formal Contract:*
- *Preconditions:* d satisfies D-CTG, D-MIN, S8-depth, S8a; S ≥ 1 (subspace
  identifier).
- *Definition:* v is a valid insertion position in subspace S of d when:
  (1) V_S(d) ≠ ∅ with |V_S(d)| = N: v = min(V_S(d)) or v = shift(min(V_S(d)), j)
  for 1 ≤ j ≤ N; (2) V_S(d) = ∅: v = [S, 1, …, 1] of depth m ≥ 2.
- *Postconditions:* #v = m (depth preservation); v₁ = S (subspace identity);
  zeros(v) = 0 ∧ v > 0 (S8a consistency); in the non-empty case, exactly N + 1
  valid positions, pairwise distinct by T3.
```
