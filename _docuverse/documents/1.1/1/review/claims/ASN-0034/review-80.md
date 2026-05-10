# Cone Review — ASN-0034/T9 (cycle 2)

*2026-04-16 10:13*

### Within-allocator enumeration injectivity is assumed but not established
**Foundation**: T10a (AllocatorDiscipline), postcondition T10a.6 — "same_allocator(a, b) determines its witnessing allocator A and the enumeration indices i, j with a = tᵢ, b = tⱼ uniquely as functions of (a, b), so any predicate phrased over those indices — T9's allocated_before in particular — is well-defined."
**ASN**: T9 (ForwardAllocation), Definitions — "`allocated_before(a, b) ≡ a = tᵢ ∧ b = tⱼ ∧ i < j` in T10a's enumeration of `dom(A)`. The predicate is well-defined on pairs `a, b` satisfying `same_allocator(a, b)` (T10a): T10a.6 (DomainDisjointness) makes the witnessing allocator `A` — and hence the enumeration indices `i, j` — unique functions of `(a, b)`".
**Issue**: Well-definedness of `allocated_before` requires two independent properties: (1) cross-allocator witness uniqueness — a unique A with a, b ∈ dom(A); (2) within-allocator index uniqueness — given A, a unique n such that a = tₙ. T10a.6 establishes (1) via disjointness but does not address (2). The ASN's "so ... indices i, j ... are functions of (a, b)" reads as if (2) follows from (1), but it does not: even with A fixed, one needs the enumeration n ↦ tₙ to be injective. That injectivity is derivable (TA5(a) gives tₙ₊₁ > tₙ, and T1 irreflexivity plus transitivity yield distinctness), but neither T10a.6 nor any other listed postcondition states it or cites the chain. A future reader auditing T9's well-definedness claim will find disjointness covered and injectivity silently assumed.
**What needs resolving**: Either extend T10a.6 (or add a separate T10a consequence) to record that each allocator's enumeration t₀, t₁, t₂, … is injective, with a pointer to TA5(a) and T1 as the source; or rephrase the well-definedness justification to make the two-part structure explicit and cite both the disjointness result and the enumeration-injectivity fact.

## Result

Cone converged after 3 cycles.

*Elapsed: 1594s*
