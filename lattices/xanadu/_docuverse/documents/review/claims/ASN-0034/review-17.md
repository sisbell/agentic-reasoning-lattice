# Contract Review — ASN-0034 (cycle 1)

*2026-04-08 23:28*

### T4

`

- `MISSING_PRECONDITION: The proof explicitly states "T3 is essential for T4b: canonical representation guarantees that the component sequence of t is fixed, so the separator positions computed by scanning for zeros are uniquely determined. Without T3, two representations of the same tumbler might yield different separator sets, and uniqueness of the parse would not follow." The formal contract lists only the T4 axiom constraints as the basis for all three postconditions, but T4b's uniqueness claim additionally requires T3 (CanonicalRepresentation). T3 should appear as an explicit precondition scoped to the T4b postcondition, not merely as a named dependency outside the contract.`

### T4b

- `MISSING_PRECONDITION: The proof explicitly invokes T3 (CanonicalRepresentation) as a load-bearing assumption: "The canonical representation of T3 ensures that the components of t are fixed — there is no alternative encoding of the same tumbler with different component values. The separator positions are therefore uniquely determined." The parent T4 narrative reinforces this: "T3 is essential for T4b: canonical representation guarantees that the component sequence of t is fixed, so the separator positions computed by scanning for zeros are uniquely determined. Without T3, two representations of the same tumbler might yield different separator sets, and uniqueness of the parse would not follow." The contract lists only the T4 constraints as preconditions; the T3 dependency is absent.`

### T8

- `MISSING_POSTCONDITION`: Case 3 of the proof establishes `allocated(s') = allocated(s) ∪ {a_new}` for allocation transitions (via T10a). This result is absent from the Frame and from every clause of the contract. The Frame covers only the two identity cases; the one case where the set actually changes is unrepresented.

- `INACCURATE`: The Depends clause names only NoDeallocation, but T10a is an equally essential dependency. NoDeallocation establishes that no removal operation exists (making the case analysis exhaustive); T10a establishes that the allocation operation is specifically an insert-only frontier advance. The proof explicitly invokes T10a to characterize Case 3. A contract that omits T10a from Depends misrepresents which assumptions the proof rests on.

3 mismatches.
