# Cone Review — ASN-0034/T9 (cycle 1)

*2026-04-16 09:38*

### `dom(A)` vs `dom_s(A)` — unreconciled state parameterization
**Foundation**: T8 (AllocationPermanence) — "`allocated(s) = ⋃{domₛ(A) : A activated in s}` is the union of realized allocator domains"
**ASN**: T9 (ForwardAllocation) — "`dom(A) = {tₙ : n ≥ 0} where t₀ is the base address and tₙ₊₁ = inc(tₙ, 0)`"
**Issue**: T8 uses a state-indexed `dom_s(A)` representing what has actually been realized in state s. T9 defines `dom(A)` unindexed as the infinite theoretical chain of all possible `inc(·, 0)` iterates. The ASN never relates the two (e.g., `dom_s(A) ⊆ dom(A)` with a frontier condition), yet T9's claim about `allocated_before` is a statement about realized history, not the theoretical chain. The predicates `same_allocator` and `allocated_before` are defined against the unindexed `dom(A)`, so they cannot directly be applied to reason about `allocated(s)` in T8's sense without a translation.
**What needs resolving**: The ASN must either unify the two domain concepts under a single notation with an explicit state parameter (and identify `dom(A)` as the limit/closure), or provide a bridge lemma showing how `dom_s(A)` embeds into `dom(A)` so that properties proven over `dom(A)` transfer to realized allocations in any reachable state.

### `same_allocator` used by T10a.2 but defined in T9
**Foundation**: T10a (AllocatorDiscipline), postcondition T10a.2 — "same_allocator(a, b) ∧ a ≠ b → a and b are prefix-incomparable"
**ASN**: T9 (ForwardAllocation), Definitions — "`same_allocator(a, b) ≡ ∃A : a ∈ dom(A) ∧ b ∈ dom(A)`"
**Issue**: T10a.2's formal contract references `same_allocator` as a predicate, but the predicate is formally introduced only in T9's contract. T9 in turn depends on T10a (its `dom(A)` definition is "justified by T10a"). The predicate that T10a uses is defined by a property that depends on T10a — a circular reference within the ASN. T10a's own Depends list does not include any carrier for `same_allocator` or `dom(A)`.
**What needs resolving**: Either (a) lift `dom(A)` and `same_allocator` into T10a (where the allocator discipline that makes them well-defined lives) and have T9 cite them from there, or (b) restate T10a.2 without appealing to `same_allocator` (e.g., quantify over "any two outputs produced by a single allocator under T10a's discipline") so the postcondition is self-contained relative to T10a's own dependencies.
