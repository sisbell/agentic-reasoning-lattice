# Proof Verification: S7b

## Verification of S7b

**S7b** is a design requirement (axiom) stating that every Istream address has exactly 3 zeros, placing it at the element level of the tumbler hierarchy. The formal contract correctly classifies this as an Axiom, and the axiom statement `(A a ∈ dom(Σ.C) :: zeros(a) = 3)` matches the narrative exactly.

**Checklist walkthrough:**

1. **Precondition completeness** — As an axiom, no preconditions needed beyond the domain `dom(Σ.C)`. Fine.
2. **Case coverage** — N/A for an axiom.
3. **Postcondition establishment** — N/A for an axiom; it is asserted by design.
4. **All conjuncts addressed** — Single conjunct (`zeros(a) = 3`). Covered.
5. **Dependency correctness** — The narrative justification says: *"By T4's field correspondence, `zeros(a) = 3` means all four identifying fields — node, user, document, element — are present."* This uses **T4** only. The sentence *"With S7a and S7b established, we can state structural attribution"* is a forward-looking remark about what S7a+S7b together enable — it is not S7b using S7a in its own reasoning. **S7a is declared as a dependency but never used.**
6. **Formal contract** — Present, uses the correct `Axiom` field, statement matches the narrative verbatim.
7. **Missing guarantees** — None; axiom needs no derivation.

```
RESULT: FOUND

**Problem**: S7a is listed as a dependency of S7b but is not referenced in S7b's
reasoning or justification. S7b's narrative uses only T4 ("By T4's field
correspondence, zeros(a) = 3 means all four identifying fields...are present").
The only mention of S7a is the transitional sentence "With S7a and S7b
established, we can state structural attribution" — this describes what the two
companion axioms jointly enable downstream, not a use of S7a in establishing S7b.

**Required**: Remove S7a from S7b's dependency list. The sole dependency is T4,
which defines zeros(t) and the field correspondence that gives zeros(a) = 3 its
semantic meaning as "element-level."
```
