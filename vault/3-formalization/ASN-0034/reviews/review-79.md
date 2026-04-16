# Cone Review — ASN-0034/T9 (cycle 1)

*2026-04-16 10:03*

### T9's `allocated_before` depends on implicit allocator uniqueness
**Foundation**: T10a (AllocatorDiscipline) — defines `dom(A)` and `same_allocator(a, b) ≡ ∃A : a ∈ dom(A) ∧ b ∈ dom(A)`.
**ASN**: T9 (ForwardAllocation), Formal Contract — "`allocated_before(a, b) ≡ a = tᵢ ∧ b = tⱼ ∧ i < j` in T10a's enumeration of `dom(A)`. The predicate is well-defined on pairs `a, b` satisfying `same_allocator(a, b)` (T10a)."
**Issue**: Well-definedness is asserted but not established. `same_allocator` is existential over allocators, so the witness `A` — and therefore the enumeration indices `i, j` — is only unique if any tumbler belongs to at most one allocator's domain. The ASN does not state or prove domain disjointness as a property. It is derivable (T10a.3 gives length separation on ancestor–descendant lineages; T10a.5 gives prefix-incomparability elsewhere, and distinct prefix-incomparable tumblers are unequal), but the ASN does not assemble this argument nor list disjointness as a consequence of T10a. If two allocators could share an element, `allocated_before(a, b)` would be ambiguous (different witnessing allocators could disagree on the `i < j` verdict), and T9's proof — which silently picks "the allocator" — would lose its referent.
**What needs resolving**: Either add a T10a consequence asserting `dom(X) ∩ dom(Y) = ∅` for distinct allocators `X, Y` (with a pointer to the two length/prefix arguments that establish it) and cite it from T9's well-definedness claim; or reformulate `allocated_before` so the witnessing allocator is a visible parameter rather than a silent existential.
