# Cone Review — ASN-0034/T8 (cycle 2)

*2026-04-15 21:23*

I've thoroughly reviewed the ASN. The YAML dependency metadata is correctly maintained, but there's a gap where the formal contract text within the ASN document doesn't reflect a critical dependency that the proof explicitly names — and this gap creates an inconsistency with how other properties in the same document handle their contracts.

---

### T1 formal contract omits T3 (CanonicalRepresentation) as a dependency, despite the proof declaring it as a foundation

**Foundation**: T3 (CanonicalRepresentation) — "tumblers with the same length and identical components at every position are equal"
**ASN**: T1 (LexicographicOrder) formal contract — contains only Definition and Postconditions, with no Depends or Preconditions clause
**Issue**: The T1 proof opens with an explicit declaration: "The argument relies on the corresponding properties of `<` on ℕ and on T3 (canonical representation: tumblers with the same length and identical components at every position are equal)." T3 is then invoked substantively in two of the three trichotomy cases. Case 1 (no divergence): "m = n and aᵢ = bᵢ for all 1 ≤ i ≤ m, so `a = b` by T3" — the transition from component-wise agreement to tumbler equality requires T3. Case 3 (exhaustion): "`a ≠ b` by T3 (distinct lengths)" — the transition from unequal lengths to tumbler inequality requires the contrapositive of T3. Without T3, both transitions are ungrounded: the proof establishes component-level facts but cannot conclude tumbler-level equality or inequality. The formal contract exports trichotomy — `(A a,b ∈ T :: exactly one of a < b, a = b, b < a)` — but doesn't declare the T3 dependency that the `a = b` case requires. This creates a document-level inconsistency: T4's contract explicitly declares "T4b (UniqueParse) requires T3 (CanonicalRepresentation)" and T8's contract includes "Depends: NoDeallocation," but T1's contract — the most widely cited property in the ASN (27 properties reference it) — has no dependency declaration at all. A contract reader cannot trace T1's foundations without reading the proof body. (The YAML metadata correctly declares `depends: [T3]`, so the pipeline's dependency graph is sound; the gap is between the prose contract and the proof within the ASN document.)
**What needs resolving**: T1's formal contract must include a Depends or Preconditions clause declaring T3 (CanonicalRepresentation), consistent with the pattern established by T4 and T8's contracts in the same ASN. Specifically, postcondition (b) Trichotomy requires T3 for the equality case.
